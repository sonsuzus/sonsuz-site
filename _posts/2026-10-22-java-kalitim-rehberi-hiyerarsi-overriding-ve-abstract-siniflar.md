---
layout: post
title: "Java Kalıtım Rehberi: Hiyerarşi, Overriding ve Abstract Sınıflar"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - kalıtım
  - inheritance
  - overriding
  - abstract
  - nesne-yönelimli-programlama
toc: true
image: /img/java-kalitim-rehberi-26.png
---

Java’da kalıtım, ortak davranışları tek bir üst sınıfta toplayarak daha düzenli ve tekrar kullanılabilir kod yazmamızı sağlar. Bir aile ağacı gibi çalışan bu yapı sayesinde alt sınıflar üst sınıfın özelliklerini devralabilir, gerektiğinde davranışları değiştirebilir ve kendi yeteneklerini ekleyebilir. Ancak güç beraberinde sorumluluk getirir: Yanlış tasarlanan bir hiyerarşi, kodu kısa sürede dijital bir makarna tabağına dönüştürebilir.

![java-kalitim-rehberi-26](/img/java-kalitim-rehberi-26.svg)

``
## Kalıtımın temel mantığı

Kalıtım, bir sınıfın başka bir sınıftaki erişilebilir alanları ve metotları edinmesidir. Java’da bunun için `extends` anahtar kelimesi kullanılır. Üst sınıfa **superclass**, ondan türeyen sınıfa ise **subclass** denir.

Bir `Kedi`, aynı zamanda bir `Hayvan` kabul edilebiliyorsa aralarında “is-a”, yani “bir türüdür” ilişkisi vardır. Bu ilişki mantıksal olarak şöyle gösterilebilir:

$$Kedi \subseteq Hayvan$$

Başka bir ifadeyle her kedi bir hayvandır; fakat her hayvan kedi değildir. Kalıtım kararında bu küçük test oldukça değerlidir.

| Kavram | Görevi | Java karşılığı |
|---|---|---|
| Üst sınıf | Ortak durum ve davranışları tanımlar | `class Hayvan` |
| Alt sınıf | Üst sınıfı genişletir | `class Kedi extends Hayvan` |
| Metot ezme | Devralınan davranışı değiştirir | `@Override` |
| Soyut sınıf | Eksik bırakılabilen ortak şablon sunar | `abstract class` |

## Sınıflar arası hiyerarşi

Basit bir hayvan hiyerarşisi oluşturalım:

```java
class Hayvan {
    protected String isim;

    public Hayvan(String isim) {
        this.isim = isim;
    }

    public void sesCikar() {
        System.out.println("Genel bir hayvan sesi!");
    }
}

class Kedi extends Hayvan {
    public Kedi(String isim) {
        super(isim); // Üst sınıfın kurucusunu çalıştırır.
    }

    public void mirildan() {
        System.out.println(isim + " mırıldanıyor.");
    }
}
```

`Kedi`, `isim` alanını ve `sesCikar()` metodunu miras alır. `super(isim)` ifadesi üst sınıfın constructor metodunu çağırır. Constructor’lar doğrudan miras alınmaz; alt sınıf, nesnenin üst sınıfa ait bölümünün nasıl kurulacağını belirtir.

## Metot ezme: Aynı sözleşme, farklı davranış

Alt sınıf, miras aldığı bir metodu kendi ihtiyacına göre yeniden yazabilir. Buna **overriding** denir.

```java
class Kopek extends Hayvan {
    public Kopek(String isim) {
        super(isim);
    }

    @Override
    public void sesCikar() {
        System.out.println(isim + ": Hav hav!");
    }
}

Hayvan hayvan = new Kopek("Karabaş");
hayvan.sesCikar(); // Karabaş: Hav hav!
```

Referansın türü `Hayvan`, gerçek nesnenin türü `Kopek` olmasına rağmen çalışma zamanında `Kopek` içindeki metot seçilir. Bu mekanizma **dinamik çok biçimlilik** olarak adlandırılır.

| Overloading | Overriding |
|---|---|
| Aynı isim, farklı parametreler | Aynı metot imzası |
| Genellikle aynı sınıfta yapılır | Alt ve üst sınıf arasında yapılır |
| Derleme zamanında belirlenir | Çalışma zamanında belirlenir |

`@Override` zorunlu değildir; fakat imza hatalarını derleyiciye yakalattığı için mutlaka kullanılması önerilir.

## Soyut sınıflar ne zaman kullanılır?

Bazı üst sınıflar gerçek bir nesneyi değil, ortak bir fikri temsil eder. Örneğin genel bir `Sekil` nesnesinin alanı hesaplanamaz; hesaplama şeklin türüne bağlıdır. Böyle durumlarda soyut sınıflar kullanılır.

```java
abstract class Sekil {
    public abstract double alanHesapla();

    public void bilgiyiYazdir() {
        System.out.println("Alan: " + alanHesapla());
    }
}

class Daire extends Sekil {
    private final double yaricap;

    public Daire(double yaricap) {
        this.yaricap = yaricap;
    }

    @Override
    public double alanHesapla() {
        return Math.PI * yaricap * yaricap;
    }
}
```

Dairenin alan formülü $A = \pi r^2$ şeklindedir. `Sekil` doğrudan örneklenemez; fakat normal metotlara, alanlara ve constructor’a sahip olabilir. Alt sınıf, soyut metodu uygulamakla yükümlüdür.

## Sağlıklı kalıtım için kısa reçete

Kalıtımı yalnızca kod tekrarını azaltmak amacıyla kullanmayın; gerçek bir “bir türüdür” ilişkisi arayın. Hiyerarşiyi gereksiz yere derinleştirmeyin, alanları mümkün olduğunca `private` tutun ve dışarıya kontrollü metotlar sunun. Kalıtım uygun değilse nesneleri bir araya getiren composition yaklaşımını değerlendirin. Doğru kullanıldığında kalıtım, overriding ve soyut sınıflar Java uygulamalarına hem esneklik hem de anlaşılır bir mimari kazandırır.
