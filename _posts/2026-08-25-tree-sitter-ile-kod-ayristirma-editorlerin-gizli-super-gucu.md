---
layout: post
title: "Tree-sitter ile Kod Ayrıştırma: Editörlerin Gizli Süper Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - tree-sitter
  - kod ayrıştırma
  - AST
  - programlama dilleri
---

Bir kod editörünün yazarken hataları anında kırmızıyla işaretlemesi, fonksiyonları katlaması veya imlecin altındaki yapıyı seçmesi sihir değildir: arka planda kodu anlayan bir ayrıştırıcı çalışır. Tree-sitter, bu işi onlarca dil için hızlı, dayanıklı ve artımlı biçimde yapan açık kaynaklı bir ayrıştırma kütüphanesidir. Özellikle eksik, hatalı ya da henüz yazılmakta olan kodla başa çıkabilmesi onu modern editörler, analiz araçları ve geliştirici deneyimi projeleri için güçlü bir aday yapar.
``
## Ayrıştırma neden önemlidir?

Kaynak kod, bilgisayar için yalnızca karakter dizisidir. Ayrıştırıcının görevi bu diziyi dilin gramer kurallarına göre anlamlı bir yapıya dönüştürmektir. Bu yapı genellikle **Soyut Sözdizimi Ağacı** (AST) olarak adlandırılır. Örneğin `toplam(a, b)` ifadesi; çağrı, fonksiyon adı ve argümanlar gibi düğümlere ayrılır.

Bir dilin gramerini kabaca $G = (N, T, P, S)$ ile ifade edebiliriz. Burada $N$ non-terminal sembolleri, $T$ terminal sembolleri, $P$ üretim kurallarını ve $S$ başlangıç sembolünü temsil eder. Tree-sitter, bu kurallardan yararlanarak kodun somut sözdizimi ağacını üretir; yani yorumlar ve noktalama işaretleri gibi editör açısından değerli ayrıntıları da korur.

| Yaklaşım | Güçlü yanı | Sınırlaması |
|---|---|---|
| Regex ile tarama | Hızlı başlangıç, basit desenler | İç içe yapılar ve bağlam zorlaşır |
| Geleneksel derleyici ayrıştırıcısı | Kesin sözdizimi denetimi | Hatalı/yarım kodda çoğunlukla durur |
| Tree-sitter | Hata toleransı ve artımlı güncelleme | Gramer kurulumu öğrenme ister |

## Tree-sitter'ı farklı kılan artımlı analiz

Klasik bir ayrıştırıcıda tek karakter eklemek, belgenin büyük bölümünün yeniden ayrıştırılmasına yol açabilir. Tree-sitter ise önceki ağacı saklar ve değişiklik aralığını kullanarak yalnızca etkilenen bölgeleri hesaplar. Belge boyutu $n$, değişen alan $k$ olsun. Gerçek performans gramer ve ağaç yapısına bağlı olsa da amaç, maliyeti tüm metinden çok değişen bölgeye yaklaştırmaktır: $O(k)$ benzeri güncellemeler etkileşimli editörler için idealdir.

Bu yaklaşım, kullanıcı `if (` yazıp henüz koşulu tamamlamamışken bile işe yarar. Tree-sitter hata düğümleri oluşturur, fakat ağacın geri kalanını kullanılabilir tutar. Dolayısıyla sözdizimi renklendirme veya kod gezinme özelliği, tek bir yazım hatası yüzünden tamamen çökmez.

## JavaScript ile ilk ağaç

Node.js ortamında `tree-sitter` ve hedef dil paketi kurulabilir:

```bash
npm install tree-sitter tree-sitter-javascript
```

Aşağıdaki örnek JavaScript kodunu ayrıştırır ve ağacı ekrana basar:

```javascript
const Parser = require('tree-sitter');
const JavaScript = require('tree-sitter-javascript');

const parser = new Parser();
parser.setLanguage(JavaScript);

const source = `function selam(isim) {
  return "Merhaba, " + isim;
}`;

const tree = parser.parse(source);
console.log(tree.rootNode.toString());
```

Çıktıda `program`, `function_declaration`, `identifier` ve `return_statement` gibi düğümler görülür. Bu düğümler, metni satır satır tahmin etmek yerine yapısal olarak sorgulamanızı sağlar. Örneğin yalnızca fonksiyon adlarını bulmak için Tree-sitter'ın sorgu dilinden yararlanabilirsiniz:

```javascript
const Query = require('tree-sitter').Query;
const query = new Query(JavaScript, `
  (function_declaration name: (identifier) @fonksiyon)
`);

for (const match of query.matches(tree.rootNode)) {
  console.log(match.captures[0].node.text);
}
```

Bu kodun amacı, AST içindeki `function_declaration` düğümlerinin `name` alanını seçmektir. Regex ile benzer bir görev başlanabilir görünse de yorumlar, satır kırılımları, async fonksiyonlar ve karmaşık söz dizimleri eklendiğinde yapısal sorgu çok daha güvenilir kalır.

## Nerelerde kullanılır?

Tree-sitter; Neovim ve Helix gibi editörlerde renklendirme, GitHub benzeri platformlarda kod analizi, özel linter'lar, belge üreticileri ve kod dönüştürme araçlarında kullanılabilir. C, Rust, Python, Go, Java, TypeScript ve daha pek çok dil için topluluk gramerleri bulunur. Yeni bir dil veya DSL desteklemek isterseniz JavaScript tabanlı gramer tanımını yazıp ayrıştırıcıyı üretebilirsiniz.

Özetle Tree-sitter, kodu yalnızca metin olarak değil, canlı ve sorgulanabilir bir yapı olarak ele alır. Çok dilli bir araç geliştiriyorsanız, hata toleransına ihtiyaç duyuyorsanız ve kullanıcıyı bekletmeden analiz yapmak istiyorsanız, araç çantanızda kesinlikle yer açmaya değer.
