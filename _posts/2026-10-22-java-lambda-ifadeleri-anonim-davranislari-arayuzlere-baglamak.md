---
layout: post
title: "Java Lambda İfadeleri: Anonim Davranışları Arayüzlere Bağlamak"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - lambda
  - fonksiyonel programlama
  - fonksiyonel arayüz
  - stream api
toc: true
image: /img/java-lambda-ifadeleri-62.png
---

Java 8 ile hayatımıza giren lambda ifadeleri, davranışı veri gibi taşımanın kısa ve güçlü bir yoludur. Başka bir deyişle, yalnızca değerleri değil, çalıştırılacak işlemleri de metotlara gönderebiliriz. Bu yaklaşım; tekrar eden kodu azaltır, koleksiyon işlemlerini okunabilir hâle getirir ve Java’ya fonksiyonel programlama dünyasından kullanışlı araçlar kazandırır.

``

## Lambda ifadesinin teorik temeli

Klasik nesne yönelimli programlamada davranışlar genellikle sınıfların metotları içinde bulunur. Fonksiyonel yaklaşımda ise bir işlem, başka bir işleme parametre olarak aktarılabilir veya sonuç olarak döndürülebilir. Matematikteki bir fonksiyonu şöyle gösterebiliriz:

$$f(x) = x \times 2$$

Java’daki karşılığı `(x) -> x * 2` biçiminde yazılabilir. Burada sol taraf parametreleri, `->` operatörü bağlantıyı, sağ taraf ise çalıştırılacak gövdeyi temsil eder.

Genel lambda söz dizimi şöyledir:

```java
(parametreler) -> ifade
```

Birden fazla komut varsa süslü parantez ve gerektiğinde `return` kullanılır:

```java
(a, b) -> {
    int toplam = a + b;
    return toplam;
}
```

Lambda kendi başına havada duran isimsiz bir metot değildir. Java, lambdanın hangi parametreleri alacağını ve hangi türü döndüreceğini bir **fonksiyonel arayüzün** tek soyut metodundan öğrenir. Bu ilişkiye hedef tipleme denir.

## Fonksiyonel arayüz nedir?

Yalnızca bir soyut metoda sahip arayüzler fonksiyonel arayüz olarak kullanılabilir. `@FunctionalInterface` zorunlu değildir; ancak yanlışlıkla ikinci bir soyut metot eklenmesini engellediği için önerilir.

```java
@FunctionalInterface
interface Hesaplayici {
    int hesapla(int a, int b);
}
```

Bu arayüze farklı davranışlar bağlayabiliriz:

```java
Hesaplayici topla = (a, b) -> a + b;
Hesaplayici carp = (a, b) -> a * b;

System.out.println(topla.hesapla(4, 3)); // 7
System.out.println(carp.hesapla(4, 3));  // 12
```

Aynı arayüz iki farklı algoritmayı temsil eder. Böylece “hangi işlem yapılacak?” kararı, işlemi kullanan koddan ayrılır.

## Anonim sınıf ile lambda karşılaştırması

Lambda ifadelerinden önce aynı davranış çoğunlukla anonim sınıfla yazılırdı:

```java
Hesaplayici topla = new Hesaplayici() {
    @Override
    public int hesapla(int a, int b) {
        return a + b;
    }
};
```

| Özellik | Anonim sınıf | Lambda |
|---|---|---|
| Kod uzunluğu | Daha fazla | Daha kısa |
| Hedef | Sınıf veya arayüz | Fonksiyonel arayüz |
| `this` anlamı | Anonim nesneyi gösterir | Dış kapsamdaki nesneyi gösterir |
| Okunabilirlik | Basit işlemlerde düşük | Küçük davranışlarda yüksek |

![java-lambda-ifadeleri-62](/img/java-lambda-ifadeleri-62.svg)


Lambda her zaman daha iyi değildir. İşlem uzuyor, çok sayıda koşul içeriyor veya yeniden kullanılacak hâle geliyorsa isimlendirilmiş bir metot daha anlaşılır olabilir.

## Hazır fonksiyonel arayüzler

Java, `java.util.function` paketinde sık kullanılan arayüzleri hazır sunar:

| Arayüz | Girdi | Çıktı | Amaç |
|---|---:|---:|---|
| `Predicate<T>` | `T` | `boolean` | Koşul sınamak |
| `Function<T, R>` | `T` | `R` | Dönüştürmek |
| `Consumer<T>` | `T` | Yok | Değeri tüketmek |
| `Supplier<T>` | Yok | `T` | Değer üretmek |

```java
Predicate<Integer> ciftMi = sayi -> sayi % 2 == 0;
Function<String, Integer> uzunluk = metin -> metin.length();
Consumer<String> yazdir = metin -> System.out.println(metin);
Supplier<Double> rastgele = () -> Math.random();
```

Örneğin çiftlik kontrolü matematiksel olarak $n \bmod 2 = 0$ koşuluna dayanır. `Predicate`, bu koşulu yeniden kullanılabilir bir davranışa dönüştürür.

## Stream API ile kullanım

Lambdaların en eğlenceli sahnesi Stream API’dir:

```java
List<String> isimler = List.of("Ada", "Ahmet", "Ece", "Mehmet");

isimler.stream()
      .filter(isim -> isim.length() >= 4)
      .map(String::toUpperCase)
      .forEach(System.out::println);
```

`filter` eleme, `map` dönüştürme, `forEach` ise sonuçları tüketme davranışını alır. `String::toUpperCase` bir metot referansıdır ve uygun lambda ifadesinin daha kısa gösterimidir.

Sonuç olarak lambda ifadeleri yalnızca sözdizimsel şeker değildir; davranışları arayüzler üzerinden aktararak gevşek bağlı, test edilebilir ve ifade gücü yüksek kod yazmamızı sağlar. Kısa işlemlerde lambda, karmaşık iş kurallarında ise anlamlı isimlere sahip metotlar kullanmak en dengeli yaklaşımdır.
