---
layout: post
title: "Java Sınıflarına Yakından Bakış: Metotlar, Statik Üyeler ve Çöp Toplayıcı"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - sınıflar
  - metotlar
  - statik-üyeler
  - garbage-collector
  - jvm
toc: true
image: /img/java-siniflarina-yakindan-87.png
---

Java’da bir sınıfı yalnızca alanlar ve metotlarla doldurulmuş bir kutu gibi görmek kolaydır. Oysa sınıflar; nesnelerin davranışlarını tanımlar, sınıf seviyesinde ortak durumları yönetir ve JVM’nin bellek mekanizmasıyla sürekli etkileşim hâlinde çalışır. Metot tanımlamalarından `static` üyelerin yaşam döngüsüne, çöp toplayıcının erişilemeyen nesneleri nasıl belirlediğine kadar uzanan bu yolculukta sınıfların kaputunu açıyoruz.
``

## Metot tanımlamasının anatomisi

Bir Java metodu; erişim belirleyici, isteğe bağlı değiştiriciler, dönüş türü, ad ve parametre listesinden oluşur:

```java
public static int topla(int a, int b) {
    return a + b;
}
```

Burada `public` erişim seviyesini, `static` metodun nesneye değil sınıfa ait olduğunu, `int` ise dönüş türünü belirtir. Metodun zaman karmaşıklığı sabit sayıda toplama işlemi yaptığı için $T(n)=O(1)$ olarak ifade edilir.

Java, metot imzasını metodun adı ve parametre türleri üzerinden değerlendirir. Dönüş türü tek başına imzayı farklılaştırmaz. Bu nedenle aşağıdaki iki metot aynı sınıfta bulunamaz:

```java
int hesapla(int sayi) { return sayi * 2; }
double hesapla(int sayi) { return sayi * 2.0; } // Derleme hatası
```

Buna karşılık parametre türleri veya sayısı değiştirilirse **metot aşırı yükleme**, yani overloading yapılabilir:

```java
int hesapla(int sayi) { return sayi * 2; }
double hesapla(double sayi) { return sayi * 2; }
```

| Özellik | Overloading | Overriding |
|---|---|---|
| Gerçekleştiği yer | Genellikle aynı sınıf | Alt sınıf |
| Parametre listesi | Farklı olmalı | Aynı olmalı |
| Seçim zamanı | Derleme zamanı | Çalışma zamanı |
| Temel amaç | Kullanım kolaylığı | Polimorfizm |

![java-siniflarina-yakindan-87](/img/java-siniflarina-yakindan-87.svg)


## Statik üyeler: Her nesneye ayrı ayrı vermeyelim

Bir örnek alanı her nesne için ayrı değer taşırken `static` alan sınıf seviyesinde tek bir değer tutar. Oluşturulan nesne sayısını izlemek bunun klasik örneğidir:

```java
class Kullanici {
    private static int toplamKullanici = 0;
    private final String ad;

    Kullanici(String ad) {
        this.ad = ad;
        toplamKullanici++;
    }

    static int toplamKullaniciSayisi() {
        return toplamKullanici;
    }

    String getAd() {
        return ad;
    }
}
```

`toplamKullanici`, bütün `Kullanici` nesneleri tarafından paylaşılır. Statik metotlar bir nesne referansı olmadan `Kullanici.toplamKullaniciSayisi()` biçiminde çağrılabilir. Ancak ortada belirli bir nesne bulunmadığından statik metot içinde doğrudan `this` kullanılamaz ve örnek alanlarına erişilemez.

| Üye türü | Sahibi | Erişim biçimi | Yaklaşık kopya sayısı |
|---|---|---|---|
| Örnek alanı | Nesne | `nesne.getAd()` | $N$ nesne için $N$ |
| Statik alan | Sınıf | `Kullanici.toplamKullaniciSayisi()` | Sınıf başına $1$ |
| Statik sabit | Sınıf | `Math.PI` | Paylaşılan tek değer |

Statik değişkenler ortak olduğundan çok iş parçacıklı uygulamalarda yarış koşullarına dikkat edilmelidir. `toplamKullanici++` atomik değildir; eşzamanlı kullanımda `AtomicInteger` daha güvenli olabilir.

## Garbage Collector nasıl karar verir?

Java’da nesneler çoğunlukla heap üzerinde oluşturulur. Bir nesnenin işi bittiğinde geliştirici `free` çağırmaz; JVM’nin Garbage Collector mekanizması devreye girer. Temel ölçüt, nesnenin **GC root** noktalarından erişilebilir olup olmadığıdır. Aktif iş parçacıklarının yerel değişkenleri, statik alanlar ve JNI referansları başlıca köklerdir.

```java
Kullanici kullanici = new Kullanici("Ada");
kullanici = null; // Önceki nesne erişilemez hâle gelebilir
```

Referansın `null` yapılması nesneyi anında silmez; yalnızca başka erişim yolu yoksa nesneyi toplanmaya uygun hâle getirir. Basitleştirilmiş olarak heap kullanımı şöyle düşünülebilir:

$$H_{kalan}=H_{önceki}-H_{erişilemeyen}+H_{yeni}$$

Modern toplayıcılar nesilleri, paralel işleme ve işaretle-süpür gibi teknikleri kullanabilir. `System.gc()` ise kesin bir emir değil, JVM’ye iletilen bir öneridir. Ayrıca `finalize()` güvenilmez ve kullanımdan kaldırılmıştır; dosya veya bağlantı gibi kaynaklar için `try-with-resources` tercih edilmelidir.

Sonuç olarak metotlar davranışı, statik üyeler ortak sınıf durumunu, Garbage Collector ise bellek yaşam döngüsünü yönetir. Bu üç yapıyı birlikte anlamak, hem daha temiz sınıflar tasarlamayı hem de gizemli bellek problemlerini daha sakin karşılamayı sağlar.
