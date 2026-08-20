---
layout: post
title: "ANTLR ile Özel Dil Derleyicisi: LL(*) Gücüyle DSL Tasarlamak"
math: true
categories: 
  - Proje
tags: 
  - antlr
  - dsl
  - derleyici
  - ll ayrıştırma
  - java
---

Her problemin çözümü genel amaçlı bir programlama diliyle yazılmak zorunda değildir. Bir raporlama sistemi için sorgu dili, oyunlar için diyalog betik dili veya otomasyon için görev tanım dili tasarlamak; kullanıcıya daha okunabilir, daha güvenli ve alanın kavramlarına yakın bir deneyim sunar. İşte bu tür dillere **alan özgü dil** ya da DSL (*Domain-Specific Language*) denir. ANTLR, gramerinizi yazarak lexer ve parser üretmenizi sağlayan güçlü bir araçtır; özellikle LL(*) yaklaşımı sayesinde karmaşık alternatifleri yönetmeyi kolaylaştırır.
``
Bir derleyicinin ilk iki aşaması çoğu zaman **sözcüksel analiz** ve **sözdizimsel analiz**dir. Lexer, karakter akışını `IDENTIFIER`, `NUMBER`, `PLUS` gibi token'lara dönüştürür. Parser ise bu token'ların gramer kurallarına uyup uymadığını kontrol eder ve genellikle bir ayrıştırma ağacı üretir. Örneğin `toplam 5 + 3` ifadesinde lexer kelimeleri ve sembolleri etiketler; parser da bunun geçerli bir komut ve ifade olduğunu anlar.

| Bileşen | Girdi | Çıktı | Sorumluluk |
|---|---|---|---|
| Lexer | Karakterler | Token akışı | Boşluk, sayı, anahtar kelime ve sembolleri ayırmak |
| Parser | Token akışı | Parse tree / AST | Gramer kurallarını doğrulamak |
| Visitor | Parse tree | İş sonucu | Yorumlama, kod üretimi veya doğrulama yapmak |

LL ayrıştırıcıları girdiyi soldan sağa (**L**eft-to-right) okur ve en soldaki türetimi (**L**eftmost derivation) kurar. Klasik LL(1), hangi kuralın seçileceğine yalnızca bir token ileri bakarak karar verir. ANTLR'nin LL(*) yaklaşımı ise sabit bir ileri bakış sınırına mahkûm değildir: Karar vermek için gerektiği kadar token'ı, teorik olarak `*` ile temsil edilen değişken uzunlukta inceleyebilir. Basitleştirilmiş biçimde karar mekanizmasını şöyle düşünebiliriz:

$$\text{Karar} = f(t_i, t_{i+1}, \ldots, t_{i+k})$$

Burada $k$, gramerdeki alternatifleri ayırmak için gereken ileri bakış miktarıdır. Bu özellik, ortak önekle başlayan kurallarda el ile karmaşık bakış kodu yazma ihtiyacını azaltır.

Örnek olarak küçük bir hesaplama DSL'i oluşturalım. Kullanıcı `hesapla 12 * (4 + 2);` yazabilsin. Aşağıdaki ANTLR4 grameri, hem parser hem lexer kurallarını aynı `.g4` dosyasında barındırır:

```antlr
grammar Hesap;

program : komut* EOF ;
komut   : 'hesapla' ifade ';' ;

ifade
    : ifade ('*' | '/') ifade
    | ifade ('+' | '-') ifade
    | NUMBER
    | '(' ifade ')'
    ;

NUMBER : [0-9]+ ;
WS     : [ \t\r\n]+ -> skip ;
```

Bu gramerde küçük harfle başlayan kurallar parser, büyük harfle başlayanlar lexer kurallarıdır. `WS` kuralındaki `-> skip`, boşlukların token akışına gönderilmemesini sağlar. `ifade` kuralı soldan özyinelemelidir; ANTLR4, uygun ifade kalıplarında bunu öncelik yönetimi için dönüştürebilir. Böylece çarpma ve bölme, toplama ve çıkarmadan daha yüksek öncelik kazanır.

Grameri Java hedefi için üretmek adına şu komut yeterlidir:

```bash
antlr4 -Dlanguage=Java Hesap.g4
javac -cp "antlr-4.x-complete.jar:." Hesap*.java
```

Üretilen parser'ı doğrudan kullanmak mümkün olsa da asıl değer, parse tree üzerinde gezen bir `Visitor` yazınca ortaya çıkar. Aşağıdaki parça, sayısal düğümleri değerlendiren yorumlayıcının temelini gösterir:

```java
@Override
public Integer visitIfade(HesapParser.IfadeContext ctx) {
    if (ctx.NUMBER() != null) return Integer.parseInt(ctx.NUMBER().getText());
    if (ctx.getChildCount() == 3 && "(".equals(ctx.getChild(0).getText())) {
        return visit(ctx.ifade(0));
    }
    int sol = visit(ctx.ifade(0));
    int sag = visit(ctx.ifade(1));
    return switch (ctx.getChild(1).getText()) {
        case "+" -> sol + sag; case "-" -> sol - sag;
        case "*" -> sol * sag; default -> sol / sag;
    };
}
```

Gerçek bir DSL'de hata mesajları en az gramer kadar önemlidir. ANTLR'nin varsayılan hata dinleyicisini özelleştirerek “satır 3: `;` bekleniyordu” gibi insan dostu mesajlar üretebilirsiniz. Ayrıca grameri küçük tutmak, anahtar kelimeleri açıkça tanımlamak ve geçerli/geçersiz örneklerle test etmek uzun vadede büyük fark yaratır. ANTLR, dil tasarımındaki fikrinizi token'lara, kurallara ve çalışabilir bir araca dönüştüren üretken bir köprüdür.
