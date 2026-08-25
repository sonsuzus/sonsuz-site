---
layout: post
title: "AST Tabanlı Kod Dönüştürme ile Akıllı Yeniden Düzenleme Araçları"
math: true
categories: 
  - Proje
tags: 
  - AST
  - Kod Dönüştürme
  - Derleyici
  - JavaScript
  - Otomasyon
---

Kaynak kodunu metin olarak bul-değiştir yapmak ilk bakışta caziptir; ancak bir fonksiyon adını yorum satırında, metin içinde veya farklı bir kapsamda yanlışlıkla değiştirmek saniyeler içinde karmaşaya dönüşebilir. AST (Abstract Syntax Tree / Soyut Sözdizim Ağacı) tabanlı dönüşüm araçları, kodu karakter dizisi olarak değil, anlamlı program yapıları olarak ele alır. Böylece güvenli yeniden adlandırma, modern sözdizimine geçiş ve ekip standartlarına otomatik uyum mümkün olur.
``

## AST Neyi Temsil Eder?

Bir derleyici ya da ayrıştırıcı, `const total = price * 1.2;` satırını tek parça metin olarak tutmaz. Bunu değişken tanımı, atama, ikili işlem, tanımlayıcı ve sayı sabiti gibi düğümlerden oluşan ağaca çevirir. Örneğin kavramsal olarak:

```text
VariableDeclaration
└── VariableDeclarator: total
    └── BinaryExpression: *
        ├── Identifier: price
        └── NumericLiteral: 1.2
```

Bu yaklaşımda dönüşümün temel akışı şöyledir: **parse et, dolaş, değiştir, yeniden üret**. Kaynak kodu $S$, ayrıştırma işlemi $P$, dönüşüm kuralı $T$ ve üretici $G$ olsun. Yeni kod şu şekilde ifade edilebilir:

$$S' = G(T(P(S)))$$

Buradaki önemli ayrıntı, $T$ işleminin metni değil düğüm türlerini hedeflemesidir. Örneğin yalnızca `CallExpression` düğümlerini değiştirmek, yorumları ve ilgisiz ifadeleri doğal olarak korur.

| Yaklaşım | Hedefleme biçimi | Risk | Uygun kullanım |
|---|---|---:|---|
| Regex | Karakter örüntüsü | Yüksek | Basit, kontrollü metinler |
| Metin tabanlı replace | Tam dizgi | Orta-yüksek | Tek seferlik küçük değişiklikler |
| AST dönüşümü | Sözdizimsel düğüm | Düşük | Büyük kod tabanları ve codemod'lar |

## JavaScript İçin Mini Codemod

JavaScript ekosisteminde Babel; ayrıştırma, ağaç üzerinde gezinme ve kod üretme işlerini güçlü paketlerle sağlar. Aşağıdaki örnek, eski `var` bildirimlerini `let` olarak dönüştürür. Gerçek projede `const` analizi gibi kapsam kuralları da eklenebilir; bu örnek ise dönüşüm mekanizmasını görünür kılar.

```js
import { parse } from "@babel/parser";
import traverse from "@babel/traverse";
import generate from "@babel/generator";

const source = `
var count = 0;
var message = "Merhaba";
console.log(message, count);
`;

const ast = parse(source, { sourceType: "module" });

traverse(ast, {
  VariableDeclaration(path) {
    if (path.node.kind === "var") {
      path.node.kind = "let";
    }
  }
});

const result = generate(ast, { comments: true }).code;
console.log(result);
```

Kodda `parse`, metni AST'ye çevirir. `traverse`, her düğümü ziyaret eder; `VariableDeclaration` ziyaretçisi yalnızca değişken bildirimleriyle ilgilenir. Son olarak `generate`, değiştirilmiş ağacı yeniden okunabilir JavaScript koduna dönüştürür. Bu, "her `var` metnini değiştir" yaklaşımından çok daha bilinçlidir.

## Sağlam Bir Dönüştürücü Tasarlamak

Dönüşüm aracı yazarken ilk kural, **idempotent** olmaktır: Araç ikinci kez çalıştığında yeni bir değişiklik üretmemelidir. Matematiksel olarak:

$$T(T(S)) = T(S)$$

Örneğin `var` zaten `let` olmuşsa ziyaretçi onu tekrar değiştirmez. İkinci kural ise kapsam farkındalığıdır. Bir fonksiyon içindeki `name` ile dış kapsamdaki `name`, aynı metne sahip olsa bile aynı sembol olmayabilir. Yeniden adlandırma için Babel scope API'leri veya TypeScript Compiler API gibi sembol çözümleyen araçlar tercih edilmelidir.

| Tasarım kararı | Neden önemlidir? | Pratik öneri |
|---|---|---|
| Test dosyaları | Yanlış dönüşümü erken yakalar | Girdi/çıktı fixture'ları kullanın |
| Biçim koruma | Gereksiz diff'leri azaltır | Prettier ile son biçimlendirme yapın |
| Kademeli çalışma | Büyük değişikliklerde güven sağlar | Önce dry-run ve rapor üretin |
| Geri alma | Hatalı toplu işlemden kurtarır | Git dalı ve küçük commit'ler kullanın |

AST tabanlı araçlar; API göçleri, `require`-`import` dönüşümü, güvenlik düzeltmeleri ve kod standardizasyonu için özellikle değerlidir. Başlangıçta ağaç düğümleri biraz ürkütücü görünse de, kodun gerçek yapısını hedefleme gücü kısa sürede vazgeçilmez olur. İyi bir codemod, geliştiricinin saatlerini kurtarırken kod inceleme ekranını da gereksiz değişiklik çöplüğüne çevirmeyen sessiz bir ekip arkadaşıdır.
