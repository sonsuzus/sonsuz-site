---
layout: post
title: "Java Dize İşlemleri: String, StringBuilder ve StringBuffer Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - string
  - stringbuilder
  - stringbuffer
  - bellek
  - performans
toc: true
image: /img/java-dize-islemleri-82.png
---

Java’da metinlerle çalışmak ilk bakışta oldukça basittir: Bir `String` tanımlar, birkaç kelimeyi birleştirir ve sonucu ekrana yazdırırız. Ancak perde arkasında nesne üretimi, bellek kullanımı, eşzamanlılık ve performans gibi önemli ayrıntılar bulunur. Özellikle döngü içinde binlerce metni birleştiriyorsanız doğru sınıfı seçmek, programınızı kaplumbağadan yarış arabasına dönüştürebilir.

``

## String neden değiştirilemez?

Java’daki `String` nesneleri **immutable**, yani değiştirilemez yapıdadır. Bir `String` oluşturulduktan sonra içindeki karakter dizisi aynı nesne üzerinde değiştirilemez. Yapılan her değişiklik yeni bir `String` nesnesi üretir.

```java
String mesaj = "Merhaba";
mesaj = mesaj + " Java";

System.out.println(mesaj); // Merhaba Java
```

Burada ilk nesne büyütülmez. `"Merhaba Java"` değerini taşıyan yeni bir nesne oluşturulur ve `mesaj` değişkeni artık onu gösterir. Eski nesneye başka bir referans yoksa nesne daha sonra çöp toplayıcı tarafından temizlenebilir.

Değiştirilemezlik; güvenlik, çok iş parçacıklı kullanım ve hash kodunun önbelleğe alınması açısından avantaj sağlar. Ayrıca Java, aynı sabit metinleri **String Pool** içinde paylaşabilir:

```java
String a = "kahve";
String b = "kahve";

System.out.println(a == b); // Genellikle true
System.out.println(a.equals(b)); // true
```

`==` referansları, `equals()` ise metinsel içeriği karşılaştırır. İçerik karşılaştırmalarında doğru tercih çoğunlukla `equals()` metodudur.

## Birleştirme maliyeti

Tek tük birleştirmelerde `+` kullanmak okunaklı ve uygundur. Fakat bir döngüde sürekli kullanıldığında çok sayıda geçici nesne oluşturabilir. Her adımda büyüyen metnin yeniden kopyalandığını düşünürsek yaklaşık maliyet şu toplamla ifade edilebilir:

$$1 + 2 + 3 + \dots + n = \frac{n(n+1)}{2} = O(n^2)$$

Derleyici basit ifadeleri optimize edebilse de dinamik döngülerde `StringBuilder` daha güvenilir bir performans seçeneğidir.

## StringBuilder: Hızlı ve dinamik

`StringBuilder`, değiştirilebilir bir karakter tamponu tutar. `append()`, `insert()`, `delete()` ve `reverse()` gibi metotlar çoğunlukla aynı nesne üzerinde çalışır.

```java
StringBuilder sonuc = new StringBuilder();

for (int i = 1; i <= 5; i++) {
    sonuc.append("Ürün ")
         .append(i)
         .append("\n");
}

String metin = sonuc.toString();
System.out.println(metin);
```

Bu kod, ürün satırlarını tek bir dinamik tamponda biriktirir. İşlem tamamlandığında `toString()` ile normal bir `String` elde edilir. Başlangıç boyutu biliniyorsa kapasite vermek yeniden boyutlandırma sayısını azaltabilir:

```java
StringBuilder rapor = new StringBuilder(1024);
rapor.append("Aylık rapor: ").append(2026);
```

Kapasite, metnin gerçek uzunluğundan farklıdır. Uzunluk kullanılan karakter sayısını, kapasite ise yeni bellek ayrılmadan tutulabilecek yaklaşık karakter miktarını belirtir.

## StringBuffer: Kilitli ama güvenli

`StringBuffer`, kullanım biçimi bakımından `StringBuilder` ile neredeyse aynıdır. Temel fark, metotlarının eşzamanlı erişime karşı senkronize edilmesidir. Birden fazla iş parçacığı aynı tamponu değiştiriyorsa bu koruma faydalı olabilir. Buna karşılık kilitleme maliyeti nedeniyle tek iş parçacıklı kodlarda genellikle daha yavaştır.

| Özellik | String | StringBuilder | StringBuffer |
|---|---|---|---|
| Değiştirilebilir mi? | Hayır | Evet | Evet |
| Thread-safe mi? | Değişmezliği sayesinde güvenli | Hayır | Evet |
| Birleştirme performansı | Yoğun işlemlerde düşük | Genellikle en hızlı | Kilit nedeniyle daha yavaş |
| Tipik kullanım | Sabit metinler | Döngüler ve metin üretimi | Paylaşılan eşzamanlı tampon |

![java-dize-islemleri-82](/img/java-dize-islemleri-82.svg)


## Hangisini seçmeliyiz?

Metin değişmeyecekse veya yalnızca birkaç basit işlem yapılacaksa `String` tercih edilmelidir. Döngü içinde JSON, SQL, rapor ya da dosya içeriği üretiliyorsa `StringBuilder` daha uygundur. Aynı değiştirilebilir tampon gerçekten birden fazla iş parçacığı tarafından paylaşılıyorsa `StringBuffer` düşünülebilir.

Kısacası, `String` güvenli ve sade bir kasa; `StringBuilder` hızlı çalışan bir atölye; `StringBuffer` ise kapısında güvenlik görevlisi bulunan bir atölyedir. Doğru araç, metnin ne kadar değişeceğine ve kimler tarafından kullanılacağına bağlıdır.
