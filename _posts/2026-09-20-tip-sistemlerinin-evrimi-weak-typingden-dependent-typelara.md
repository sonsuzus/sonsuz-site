---
layout: post
title: "Tip Sistemlerinin Evrimi: Weak Typing’den Dependent Type’lara"
math: true
categories: 
  - Bilgi
tags: 
  - tip sistemleri
  - weak typing
  - static typing
  - dependent types
  - programlama dilleri
  - type theory
toc: true
image: /img/tip-sistemlerinin-evrimi-49.png
---

Tip sistemleri, programlarımızın hangi değerlerle hangi işlemleri yapabileceğini belirleyen görünmez trafik kurallarıdır. İlk bakışta yalnızca “bu değişken sayı mı, metin mi?” sorusuyla ilgileniyor gibi görünürler. Oysa weak typing’den dependent type’lara uzanan yolculuk; hataları ne zaman yakaladığımızı, kod hakkında neleri kanıtlayabildiğimizi ve derleyiciye ne kadar sorumluluk verdiğimizi anlatır.
``
## Tip sistemi neyi çözer?

Bir tip sistemi, değerleri sınıflandırır ve geçerli işlemleri tanımlar. En basit hâliyle bir ifade için şu yargıyı üretir:

$$\Gamma \vdash e : T$$

Burada $\Gamma$ mevcut değişkenler ve tiplerinden oluşan bağlamı, $e$ ifadeyi, $T$ ise ifadenin tipini temsil eder. Sözel karşılığı şudur: “Bu bağlam altında, `e` ifadesi `T` tipindedir.”

Tip sistemlerini tek bir doğru üzerinde sıralamak yanıltıcıdır. **Statik-dinamik** ayrımı kontrolün zamanını, **strong-weak** ayrımı ise dillerin uyumsuz değerler arasında ne kadar kolay dönüşüm yaptığına ilişkin genel davranışı anlatır.

| Yaklaşım | Kontrol zamanı | Tipik özellik | Örnek diller |
|---|---|---|---|
| Weak typing | Derleme veya çalışma zamanı | Örtük dönüşümler daha serbesttir | C, JavaScript |
| Dynamic typing | Çalışma zamanı | Değişken değil, değer tip taşır | Python, Ruby |
| Static typing | Derleme zamanı | Hatalar çalıştırmadan yakalanabilir | Java, Rust |
| Hindley–Milner | Derleme zamanı | Güçlü tip çıkarımı sağlar | Haskell, ML |
| Dependent types | Derleme zamanı | Tipler değerlere bağlı olabilir | Idris, Agda, Lean |

![tip-sistemlerinin-evrimi-49](/img/tip-sistemlerinin-evrimi-49.svg)


## Weak typing: “Ben bunu dönüştürürüm” dönemi

Weak typing kesin sınırları olan akademik bir kategori değildir; çoğunlukla bol miktarda örtük dönüşüm yapan dilleri tanımlar. JavaScript’in meşhur davranışı iyi bir örnektir:

```javascript
console.log("5" + 1); // "51": sayı metne dönüştürülür
console.log("5" - 1); // 4: metin sayıya dönüştürülür
```

Dil burada programcı adına karar verir. Bu yaklaşım hızlı prototiplemeyi kolaylaştırabilir; ancak aynı değerin operatöre göre farklı yorumlanması sürprizlere yol açar. C’deki işaretçi dönüşümleri ise esneklik ve donanıma yakınlık sağlarken bellek güvenliği riskleri doğurabilir.

## Statik tipler ve tip çıkarımı

Statik tipli diller, birçok uyumsuzluğu program çalışmadan önce bulur. Fakat bu, her değişkenin tipini elle yazmamız gerektiği anlamına gelmez. Hindley–Milner ailesindeki tip çıkarımı, ifadelerden genel tipler türetebilir:

```haskell
identity x = x
```

Derleyici bu fonksiyonun tipini şöyle çıkarır:

$$identity : \forall a.\ a \rightarrow a$$

Yani fonksiyon herhangi bir $a$ tipini alır ve aynı tipte değer döndürür. Parametrik polimorfizm sayesinde kod hem genel hem güvenlidir. Java generics, Rust trait’leri ve TypeScript union tipleri de farklı yöntemlerle daha zengin modeller kurar.

## Cebirsel veri tipleri: imkânsız durumları azaltmak

Modern tip tasarımında amaç yalnızca hataları yakalamak değil, geçersiz durumların ifade edilmesini zorlaştırmaktır:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

Bu yapı, bir işlemin ya başarılı değer ya da hata ürettiğini açıkça belirtir. `null` veya belirsiz dönüş değerleri yerine olasılıklar tip düzeyinde modellenir. Derleyici de iki durumu ele alıp almadığımızı kontrol eder.

## Dependent type: değerler tipe girerse

Dependent type sistemlerinde bir tip, bir değere bağlı olabilir. Uzunluğu tipinde bulunan vektör klasik örnektir:

$$Vector(A, n)$$

Burada $A$ eleman tipini, $n$ ise uzunluğu belirtir. Toplama fonksiyonu yalnızca aynı uzunluktaki vektörleri kabul edebilir:

```idris
add : Vect n Int -> Vect n Int -> Vect n Int
```

`Vect 3 Int` ile `Vect 4 Int` toplamak daha program çalışmadan reddedilir. Böylece “indeks sınırlar içinde mi?” gibi bazı çalışma zamanı kontrolleri, derleme zamanı kanıtlarına dönüşür.

Curry–Howard ilişkisine göre tipler önerme, programlar ise kanıt gibi yorumlanabilir:

$$\text{Tip} \leftrightarrow \text{Önerme}, \qquad \text{Program} \leftrightarrow \text{Kanıt}$$

Bunun bedeli daha karmaşık tip ifadeleri, zor hata mesajları ve bazen kanıt yazma yüküdür. Dolayısıyla dependent type’lar her uygulamanın varsayılan tercihi değildir; güvenliğin kritik olduğu protokoller, derleyiciler ve doğrulanmış algoritmalar için özellikle değerlidir.

Tip sistemlerinin evrimi, esneklikten güvenliğe doğru basit bir yarış değildir. Asıl mesele, hataların maliyeti ile geliştirici deneyimi arasında doğru dengeyi kurmaktır. Bazen dinamik bir betik yeterlidir; bazen de derleyicinin yalnızca kodu çevirmesini değil, matematik öğretmeni gibi kanıt istemesini tercih ederiz.
