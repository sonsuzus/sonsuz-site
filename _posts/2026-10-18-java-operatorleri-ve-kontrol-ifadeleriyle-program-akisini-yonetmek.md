---
layout: post
title: "Java Operatörleri ve Kontrol İfadeleriyle Program Akışını Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - operatörler
  - kontrol-akışı
  - döngüler
  - karar-yapıları
  - programlama
toc: true
image: /img/java-operatorleri-ve-60.png
---

Bir Java programı yalnızca yukarıdan aşağıya çalışan komutlardan oluşsaydı, hesap makinesinden biraz daha heyecanlı uygulamalar geliştirmek zor olurdu. Operatörler verileri işlerken kontrol ifadeleri programın hangi yolu izleyeceğine karar verir. Başka bir deyişle operatörler soruları hazırlar, karar yapıları cevapları değerlendirir, döngüler ise gerekli işleri sabırla tekrarlar.
``
## Operatörler: Programın hesaplama araçları

Operatörler, bir veya daha fazla değer üzerinde işlem yapan sembollerdir. Örneğin `+` toplama yaparken `>` iki değeri karşılaştırır. Bir ifadenin sonucu başka bir operatörün girdisi olabilir. Bu nedenle işlem önceliğini anlamak önemlidir.

Örneğin aşağıdaki matematiksel ifade Java'da da aynı öncelik mantığıyla değerlendirilir:

$$sonuc = 10 + 4 \times 2 = 18$$

Çarpma önce çalışır. Sonucun `28` olması isteniyorsa parantez kullanılmalıdır: `(10 + 4) * 2`.

| Operatör grubu | Örnekler | Görevi |
|---|---|---|
| Aritmetik | `+`, `-`, `*`, `/`, `%` | Matematiksel işlem yapar |
| Karşılaştırma | `==`, `!=`, `<`, `>=` | `boolean` sonuç üretir |
| Mantıksal | `&&`, `||`, `!` | Koşulları birleştirir veya tersine çevirir |
| Atama | `=`, `+=`, `-=` | Değişkene değer atar veya günceller |
| Artırma-azaltma | `++`, `--` | Sayıyı bir artırır veya azaltır |

![java-operatorleri-ve-60](/img/java-operatorleri-ve-60.svg)


Mod alma operatörü `%`, özellikle çift-tek kontrolünde kullanışlıdır. Bir $n$ sayısı için $n \bmod 2 = 0$ ise sayı çifttir.

## Karar yapıları: Yol ayrımındaki Java

`if`, `else if` ve `else`, koşullara göre farklı kod blokları çalıştırır. Koşulun sonucu mutlaka `true` veya `false` olmalıdır.

```java
int puan = 78;

if (puan >= 85) {
    System.out.println("Pekiyi");
} else if (puan >= 50) {
    System.out.println("Geçti");
} else {
    System.out.println("Kaldı");
}
```

Bu kod, karşılaştırma operatörleriyle puanı sınıflandırır. Koşullar yukarıdan aşağıya sınanır ve ilk doğru bloğun ardından yapı sona erer. Dolayısıyla daha özel veya yüksek eşikli koşulların önce yazılması önemlidir.

Sabit seçeneklerin bulunduğu durumlarda `switch` daha okunaklı olabilir:

```java
String rol = "editor";

switch (rol) {
    case "admin" -> System.out.println("Tam yetki");
    case "editor" -> System.out.println("İçerik düzenleme yetkisi");
    default -> System.out.println("Sınırlı yetki");
}
```

| Yapı | En uygun kullanım | Güçlü yönü |
|---|---|---|
| `if-else` | Aralıklar ve karmaşık koşullar | Esneklik |
| `switch` | Belirli, ayrık seçenekler | Okunabilirlik |
| Üçlü operatör | Kısa değer seçimi | Az kod |

Üçlü operatörün biçimi `koşul ? doğruDeğer : yanlışDeğer` şeklindedir. Örneğin `yas >= 18 ? "Yetişkin" : "Çocuk"` ifadesi kısa bir karar üretir; ancak iç içe kullanılırsa okunabilirliği hızla düşürür.

## Döngüler: Tekrarın kontrollü hâli

Döngüler, aynı işlemi belirli bir koşul sağlandığı sürece tekrarlar. `for` tekrar sayısı bilindiğinde, `while` koşul ön planda olduğunda, `do-while` ise bloğun en az bir kez çalışması gerektiğinde tercih edilir.

```java
int toplam = 0;

for (int i = 1; i <= 5; i++) {
    toplam += i;
}

System.out.println(toplam); // 15
```

Bu döngü $1+2+3+4+5=15$ toplamını hesaplar. Başlangıç değeri, devam koşulu ve artış işlemi aynı satırda görüldüğü için akış kolayca izlenebilir.

`break` döngüyü tamamen sonlandırırken `continue` yalnızca mevcut turu atlar. Bunlar güçlü araçlardır; gereğinden fazla kullanılmaları akışı takip etmeyi zorlaştırabilir.

## Kısa devre değerlendirmesi

Mantıksal `&&` operatörü ilk koşul yanlışsa ikinci koşulu çalıştırmaz. `||` ise ilk koşul doğruysa devamını değerlendirmez:

```java
if (kullanici != null && kullanici.isActive()) {
    System.out.println("Giriş başarılı");
}
```

Burada önce `null` kontrolü yapılır. Böylece var olmayan bir nesne üzerinde metot çağrılması ve `NullPointerException` oluşması engellenir.

Sonuç olarak operatörler veriyi dönüştürür, karar ifadeleri uygun yolu seçer ve döngüler tekrarları yönetir. Sağlam bir Java programında bu üçlü birlikte çalışır: doğru koşul kurulur, akış bilinçli biçimde yönlendirilir ve her tekrarın ne zaman biteceği açıkça tanımlanır.
