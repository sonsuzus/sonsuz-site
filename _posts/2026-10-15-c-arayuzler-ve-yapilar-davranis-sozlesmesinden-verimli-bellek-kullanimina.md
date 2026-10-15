---
layout: post
title: "C# Arayüzler ve Yapılar: Davranış Sözleşmesinden Verimli Bellek Kullanımına"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - arayüzler
  - struct
  - değer-tipleri
  - oop
  - bellek-yönetimi
toc: true
image: /img/c-arayuzler-ve-77.png
---

C# dünyasında `interface` ve `struct`, benzer görünen problemlere tamamen farklı yönlerden yaklaşır. Arayüzler bir türün **ne yapması gerektiğini** söylerken yapılar küçük verileri düşük maliyetle temsil etmeyi amaçlar. Biri davranış sözleşmesi, diğeri değer semantiği sunar. Doğru yerde kullanıldıklarında kodu hem esnek hem de hızlı hâle getirirler; yanlış tercihler ise kutulama, gereksiz kopyalama ve karmaşık tasarım gibi sürprizler doğurabilir.

![c-arayuzler-ve-77](/img/c-arayuzler-ve-77.svg)

``

## Arayüz: Davranışın sözleşmesi

Arayüz, onu uygulayan türlerin sunması gereken üyeleri tanımlar. Genellikle durum saklamaz ve doğrudan örneklenemez. Böylece kod, belirli bir sınıfa değil davranışa bağımlı olur. Bu yaklaşım bağımlılıkların tersine çevrilmesini ve birim testlerini kolaylaştırır.

```csharp
public interface IBildirimGonderici
{
    void Gonder(string alici, string mesaj);
}

public class EpostaGonderici : IBildirimGonderici
{
    public void Gonder(string alici, string mesaj)
    {
        Console.WriteLine($"E-posta gönderildi: {alici} - {mesaj}");
    }
}
```

Burada `IBildirimGonderici`, gönderimin nasıl yapılacağını açıklamaz; yalnızca `Gonder` davranışını zorunlu kılar. Daha sonra SMS veya mobil bildirim sınıfları aynı arayüzü uygulayabilir. Çağıran kodun hangi somut sınıfı kullandığını bilmesine gerek kalmaz.

Modern C# sürümlerinde arayüzler varsayılan metot gövdeleri ve statik üyeler içerebilse de temel amaçları hâlâ ortak davranış sınırı oluşturmaktır. Arayüzü, “Bu etiketi taşıyorsan şu yetenekleri sunmalısın” diyen bir kulüp üyeliği gibi düşünebiliriz.

## Struct: Küçük ama ciddi bir değer tipi

`struct`, sınıflardan farklı olarak bir **değer tipidir**. Bir yapı değişkene atandığında çoğunlukla referansı değil, içindeki değerler kopyalanır.

```csharp
public readonly struct Nokta
{
    public double X { get; }
    public double Y { get; }

    public Nokta(double x, double y)
    {
        X = x;
        Y = y;
    }

    public double Uzaklik() => Math.Sqrt(X * X + Y * Y);
}
```

Bu yapı iki boyutlu bir noktayı temsil eder. Öklid uzaklığı şu formülle hesaplanır:

$$d = \sqrt{x^2 + y^2}$$

`readonly struct`, oluşturulduktan sonra değerin değişmeyeceğini belirtir. Bu özellik hem niyeti açıklar hem de derleyicinin bazı gereksiz savunma kopyalarını azaltmasına yardımcı olabilir.

## Temel farklar

\vert  Özellik \vert  Interface \vert  Struct \vert 
\vert ---\vert ---\vert ---\vert 
\vert  Ana amacı \vert  Davranış sözleşmesi tanımlamak \vert  Küçük bir değeri temsil etmek \vert 
\vert  Örneklenebilir mi? \vert  Hayır \vert  Evet \vert 
\vert  Semantik \vert  Uygulayan türe bağlı \vert  Değer semantiği \vert 
\vert  Kalıtım \vert  Bir tür birden fazla arayüz uygulayabilir \vert  Başka sınıf veya struct kalıtamaz \vert 
\vert  Durum \vert  Normal örnek alanı taşımaz \vert  Alan ve özellik taşıyabilir \vert 
\vert  `null` değeri \vert  Referans üzerinden mümkün \vert  Yalnızca `Nullable<T>` ile \vert 

## Birlikte kullanılabilirler mi?

Elbette! Bir yapı da arayüz uygulayabilir:

```csharp
public interface IAlanHesaplayici
{
    double AlanHesapla();
}

public readonly struct Dikdortgen : IAlanHesaplayici
{
    public double En { get; }
    public double Boy { get; }

    public Dikdortgen(double en, double boy) => (En, Boy) = (en, boy);

    public double AlanHesapla() => En * Boy;
}
```

Ancak yapı, arayüz türündeki bir değişkene atanırsa **boxing** oluşabilir. Boxing sırasında değer, yönetilen yığında bir nesne içine sarılır. Yaklaşık maliyeti yalnızca veri boyutu $S$ değil, nesne başlığı $H$ ile birlikte kabaca $S + H$ olarak düşünülebilir. Sık çalışan döngülerde bu tahsisler çöp toplayıcı üzerinde baskı yaratır. Generic kısıtlar, bazı senaryolarda boxing maliyetini önleyebilir.

## Sınırlar ve seçim rehberi

Struct; küçük, mantıksal olarak tek bir değer olan ve tercihen değişmez veri modellerinde uygundur. Koordinat, renk, tarih aralığı veya ölçü birimi iyi adaylardır. Büyük struct’lar her atamada kopyalanabileceği için performansı tersine çevirebilir. Kimliği olan, uzun yaşayan veya sık değişen nesnelerde sınıf tercih edilmelidir.

Arayüz ise farklı türlerin ortak bir yeteneği paylaşması, bağımlılıkların soyutlanması veya test doubles kullanılması gerektiğinde güçlüdür. Kısacası arayüz **“ne yapabilir?”**, struct ise **“hangi değeri temsil eder?”** sorusuna cevap verir. Bu ayrımı korumak, hem temiz mimarinin hem de bilinçli bellek kullanımının anahtarıdır.
