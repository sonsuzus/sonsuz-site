---
layout: post
title: "OCaml ile Tip Güvenli Derleyici Ön Ucu: Lexer, Parser ve Çıkarımın Gücü"
math: true
categories: 
  - Proje
tags: 
  - OCaml
  - derleyici
  - tip çıkarımı
---

Bir derleyicinin ön ucu, kaynak kodun dağınık karakterlerini anlamlı ve güvenilir bir programa dönüştüren ilk savunma hattıdır. OCaml bu iş için özellikle keyifli bir seçimdir: cebirsel veri tipleri sentaks ağacını açıkça modeller, pattern matching her olasılığı düşünmeye zorlar ve Hindley-Milner tabanlı tip çıkarımı pek çok tasarım hatasını program daha çalışmadan yakalar. Sonuçta sadece çalışan değil, yanlış durumları temsil etmesi zor bir lexer ve parser geliştirirsiniz.
``
Ön ucun klasik akışı şöyledir: metin önce **token** dizisine ayrılır, tokenlar gramer kurallarıyla eşleştirilir ve sonunda bir **soyut sentaks ağacı**na (AST) dönüşür. Örneğin `let x = 2 + 3` satırı, karakter dizisi olmaktan çıkar; bağlama, sayı sabitine ve toplama düğümüne sahip yapısal bir veriye dönüşür. Bu ayrım önemlidir: lexer karakterlerle, parser ise dilin yapısıyla ilgilenir.

| Katman | Girdi | Çıktı | Sorumluluk |
|---|---|---|---|
| Lexer | Karakter akışı | `IDENT`, `INT`, `PLUS` tokenları | Yazım birimlerini tanımak |
| Parser | Token akışı | AST | Gramer ve öncelik kurallarını uygulamak |
| Tip denetleyici | AST | Tiplenmiş AST veya hata | İşlemlerin anlamını doğrulamak |

Küçük bir ifade dili için tokenları kapalı bir varyant tipiyle tanımlamak, geçersiz token türlerini en baştan engeller:

```ocaml
type token =
  | Int of int
  | Ident of string
  | Let
  | Eq
  | Plus
  | LParen
  | RParen
  | EOF

type expr =
  | EInt of int
  | EVar of string
  | EAdd of expr * expr
  | ELet of string * expr * expr
```

Bu tanımın güzelliği şudur: `EAdd` yalnızca iki `expr` kabul eder; yanlışlıkla ham bir metni veya tokenı toplama düğümüne koyamazsınız. OCaml derleyicisi, `match` ifadelerinde unutulan yapıcıları bildirerek parser yazarken görünmeyen yolları da aydınlatır. Bu, derleyici yazımındaki en değerli “bedava testlerden” biridir.

Lexer tarafında kaynak konumunu da taşımak iyi bir yatırımdır. Her tokena satır ve sütun eklemek, `Beklenen )` yerine `Satır 4, sütun 12: beklenen )` diyebilmenizi sağlar. Kullanıcı için küçük, dil aracınızın ciddiyeti için dev bir farktır. `ocamllex` düzenli ifadelerle hızlı bir başlangıç sunarken, el yazımı lexer karakter ilerletme mantığını öğrenmek için daha öğreticidir.

Parser’da özyinelemeli iniş yaklaşımı, küçük diller için okunaklıdır. Toplama işleminin sol birleşimli olmasını sağlamak üzere önce atomları, sonra art arda gelen `+` işlemlerini işleyebilirsiniz:

```ocaml
let rec parse_add st =
  let left = parse_atom st in
  let rec loop acc =
    match peek st with
    | Plus ->
        ignore (consume st);
        let right = parse_atom st in
        loop (EAdd (acc, right))
    | _ -> acc
  in
  loop left
```

Bu kod, `1 + 2 + 3` ifadesini `EAdd (EAdd (1, 2), 3)` biçiminde kurar. Yani işlem sırası sadece bir yorum değil, ağacın şekline gömülmüş bir garantidir. Daha karmaşık dillerde Menhir gibi parser üreteçleri; grameri bildirime dayalı yazmak, çakışmaları raporlamak ve hata kurtarma eklemek açısından güçlüdür.

Tip çıkarımının teorik kalbi, bilinmeyen tiplere değişken atamak ve kısıtları birleştirmektir. `fun x -> x + 1` için `x` başlangıçta $\alpha$ olsun. `+` işleci iki tamsayı istediğinden $\alpha = int$ kısıtı doğar; fonksiyonun tipi böylece $int \to int$ olur. Kimlik fonksiyonunda ise `fun x -> x` için hiçbir ek kısıt yoktur ve en genel tip $\forall \alpha.\; \alpha \to \alpha$ elde edilir.

| İfade | Çıkarılan tip | Neden |
|---|---|---|
| `1 + 2` | `int` | Her iki operand tamsayıdır |
| `fun x -> x` | `'a -> 'a` | Girdi ve çıktı aynı bilinmeyen tiptedir |
| `fun x -> x + 1` | `int -> int` | `+` işleci `x`i `int` olmaya zorlar |

Pratikte tip denetleyiciniz bir ortam taşır: `string -> typ`. `let x = 10 in x + 1` işlenirken `x`, ortamda `int` ile eşlenir. Birleştirme algoritması iki tipi uyumlu hale getirir; örneğin $\alpha$ ile $int$ birleşince $\alpha$ artık $int$tir. Occurs check de $\alpha = \alpha \to int$ gibi sonsuz tipleri reddeder.

Son dokunuş testtir. Lexer için boşluklar, bilinmeyen karakterler ve çok basamaklı sayılar; parser için parantezler ve öncelik; tip sistemi için gölgelenen değişkenler ve hatalı toplamalar test edilmelidir. OCaml’in tip sistemi testlerin yerini tutmaz, fakat hataların büyük kısmını derleme anına çeker. İşte tip güvenli bir ön ucun büyüsü burada: AST’niz yalnızca veri değil, dilinizin kurallarını taşıyan bir sözleşme olur.
