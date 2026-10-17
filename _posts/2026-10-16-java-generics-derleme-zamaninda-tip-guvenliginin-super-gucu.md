---
layout: post
title: "Java Generics: Derleme Zamanında Tip Güvenliğinin Süper Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - generics
  - tip güvenliği
  - jenerik programlama
  - yazılım geliştirme
toc: true
image: /img/java-generics-derleme-22.png
---

![java-generics-derleme-22](/img/java-generics-derleme-22.svg)


Java’da genel türler, yani *Generics*, farklı veri tipleriyle çalışabilen sınıflar ve metotlar yazarken tip güvenliğini korumamızı sağlar. Bir koleksiyonun içine yanlışlıkla ilgisiz bir nesne koyup hatayı çalışma zamanında keşfetmek yerine, derleyicinin erkenden alarm vermesini sağlar. Kısacası Generics, kodun kapısında duran ve “Listede yalnızca belirtilen tipler girebilir!” diyen ciddi ama faydalı bir güvenlik görevlisidir.

``

## Generics neden gereklidir?

Generics bulunmasaydı farklı türleri saklamak için çoğunlukla `Object` kullanmamız gerekirdi. Ancak `Object`, neredeyse her şeyi kabul ettiği için derleyici nesnenin gerçek türünü bilemez. Bu durumda açık tür dönüşümü yapılır ve yanlış dönüşümler `ClassCastException` hatasına neden olabilir.

```java
List<String> isimler = new ArrayList<>();
isimler.add("Ada");
isimler.add("Linus");

String ilkIsim = isimler.get(0);
```

Burada `List<String>`, listenin yalnızca `String` değerleri kabul edeceğini belirtir. `isimler.add(42)` yazılırsa program daha çalıştırılmadan derleme hatası oluşur. Ayrıca `get()` sonucunu `String` türüne dönüştürmek gerekmez.

| Özellik | `Object` yaklaşımı | Generics yaklaşımı |
|---|---|---|
| Tip kontrolü | Çalışma zamanına kalabilir | Derleme zamanında yapılır |
| Tür dönüşümü | Genellikle gereklidir | Çoğunlukla gerekmez |
| Hata riski | Daha yüksek | Daha düşük |
| Okunabilirlik | Belirsiz olabilir | Beklenen tip açıktır |
| Yeniden kullanım | Var, fakat güvensiz | Hem esnek hem güvenli |

Bir programdaki olası tip uyuşmazlığı sayısını $n$ kabul edersek, çalışma zamanında kontrol edilen bir tasarımda bu hataların test edilmesi çok sayıda yürütme yolu gerektirebilir. Generics sayesinde kontrollerin önemli kısmı derleyiciye taşınır:

$$\text{Çalışma zamanı tip hatası riski} \downarrow \quad \text{Derleme zamanı doğrulaması} \uparrow$$

## Jenerik sınıf oluşturmak

Tür parametreleri çoğunlukla `T`, `E`, `K` ve `V` harfleriyle gösterilir. Bunlar sırasıyla *Type*, *Element*, *Key* ve *Value* anlamlarında kullanılan geleneksel adlardır.

```java
class Kutu<T> {
    private T deger;

    public void koy(T deger) {
        this.deger = deger;
    }

    public T al() {
        return deger;
    }
}

Kutu<Integer> sayiKutusu = new Kutu<>();
sayiKutusu.koy(21);
System.out.println(sayiKutusu.al() * 2);
```

`Kutu<T>` sınıfı herhangi bir referans tipiyle kullanılabilir. Fakat belirli bir nesne oluşturulduğunda `T` somutlaşır. `Kutu<Integer>` için `koy()` metodu yalnızca `Integer` kabul eder ve `al()` metodu `Integer` döndürür.

## Sınırlandırılmış türler

Bazen “her tür olabilir” demek fazla özgürlüktür. Örneğin yalnızca sayısal değerlerle çalışan bir sınıf için üst sınır tanımlanabilir:

```java
class Hesaplayici<T extends Number> {
    public double kare(T sayi) {
        double deger = sayi.doubleValue();
        return deger * deger;
    }
}
```

`T extends Number`, türün `Number` veya onun alt sınıflarından biri olmasını zorunlu kılar. Böylece `Integer` ve `Double` kullanılabilirken `String` reddedilir.

## Wildcard ve PECS ilkesi

`?`, kesin türün bilinmediği durumlarda kullanılan wildcard işaretidir. Özellikle koleksiyon API’lerinde şu kısa kural çok kullanışlıdır: **Producer Extends, Consumer Super (PECS)**.

```java
static double toplam(List<? extends Number> sayilar) {
    double sonuc = 0;
    for (Number sayi : sayilar) {
        sonuc += sayi.doubleValue();
    }
    return sonuc;
}

static void tamSayiEkle(List<? super Integer> hedef) {
    hedef.add(10);
}
```

| İfade | Amaç | Güvenli işlem |
|---|---|---|
| `? extends Number` | Değer üretmek ve okumak | `Number` olarak okuma |
| `? super Integer` | Değer tüketmek ve eklemek | `Integer` ekleme |
| `<?>` | Türden bağımsız işlem | `Object` olarak okuma |

Java, Generics bilgisinin büyük bölümünü derleme sonrasında **type erasure** ile siler. Bu nedenle çalışma zamanında `List<String>` ile `List<Integer>` çoğunlukla aynı ham sınıfı paylaşır. Yine de derleme aşamasındaki kontroller, daha temiz API’ler, daha az dönüşüm ve daha erken hata tespiti sağlar. Generics öğrenmenin özü şudur: Türleri gizlemek yerine ilişkilerini açıkça ifade et; gerisini derleyiciye bırak.
