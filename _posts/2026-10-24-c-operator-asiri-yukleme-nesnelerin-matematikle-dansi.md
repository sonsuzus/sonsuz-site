---
layout: post
title: "C# Operatör Aşırı Yükleme: Nesnelerin Matematikle Dansı"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - operatör-aşırı-yükleme
  - nesne-yönelimli-programlama
  - dotnet
  - operator-overloading
toc: true
image: /img/c-operator-asiri-55.png
---

![c-operator-asiri-55](/img/c-operator-asiri-55.svg)


C# ile geliştirdiğimiz özel sınıflar, varsayılan olarak `+`, `-`, `>`, `==` gibi operatörlerin ne anlama geldiğini bilmez. Örneğin iki vektörü `vektor1 + vektor2` biçiminde toplamak istersek derleyici doğal olarak şaşırır. Operatör aşırı yükleme, bu sembollere kendi nesnelerimiz için anlam kazandırmamızı sağlar. Böylece kod hem matematiksel gösterime yaklaşır hem de daha okunabilir hâle gelir.

``

## Operatör aşırı yükleme nedir?

Operatör aşırı yükleme, mevcut bir operatörün özel bir tür üzerindeki davranışını tanımlamaktır. Burada yeni bir operatör icat etmeyiz; C# tarafından desteklenen operatörlerden birini yeniden anlamlandırırız.

Örneğin iki boyutlu bir vektörümüz şu şekilde gösterilsin:

$$
\vec{v} = (x, y)
$$

İki vektörün toplamı ise bileşenlerin ayrı ayrı toplanmasıyla bulunur:

$$
(x_1, y_1) + (x_2, y_2) = (x_1+x_2, y_1+y_2)
$$

Bu matematiksel kuralı C# sınıfına taşıyarak `+` operatörünü programlayabiliriz.

## Temel söz dizimi

Aşırı yüklenen operatörler `public` ve `static` olarak tanımlanmalıdır. Metot adı yerine `operator` anahtar sözcüğü ve ilgili sembol kullanılır.

```csharp
public class Vektor
{
    public double X { get; }
    public double Y { get; }

    public Vektor(double x, double y)
    {
        X = x;
        Y = y;
    }

    public static Vektor operator +(Vektor sol, Vektor sag)
    {
        return new Vektor(sol.X + sag.X, sol.Y + sag.Y);
    }

    public override string ToString()
    {
        return $"({X}, {Y})";
    }
}
```

Bu metot iki `Vektor` nesnesini alır ve toplamı temsil eden yeni bir nesne döndürür. Mevcut nesneleri değiştirmemek, özellikle matematiksel değer türlerinde daha güvenli ve tahmin edilebilir bir tasarımdır.

```csharp
var a = new Vektor(2, 3);
var b = new Vektor(4, 1);
var toplam = a + b;

Console.WriteLine(toplam); // (6, 4)
```

Normalde `Vektor.Topla(a, b)` gibi bir metot yazılabilirdi. Ancak `a + b`, işlemin niyetini çok daha hızlı anlatır.

\vert  Yaklaşım \vert  Kullanım \vert  Okunabilirlik \vert  Matematiksel uyum \vert 
\vert ---\vert ---\vert ---:\vert ---:\vert 
\vert  Normal metot \vert  `Vektor.Topla(a, b)` \vert  Orta \vert  Düşük \vert 
\vert  Operatör \vert  `a + b` \vert  Yüksek \vert  Yüksek \vert 
\vert  Elle hesaplama \vert  `new Vektor(a.X+b.X, a.Y+b.Y)` \vert  Düşük \vert  Orta \vert 

## İlişkisel operatörleri yüklemek

Vektörleri büyüklüklerine göre karşılaştırabiliriz. Bir vektörün uzunluğu Pisagor bağıntısıyla hesaplanır:

$$
\vert \vec{v}\vert  = \sqrt{x^2+y^2}
$$

Karşılaştırma sırasında karekök almaya gerek yoktur. Çünkü pozitif değerlerde $a^2 > b^2$ ise $a > b$ olur.

```csharp
public double UzunlukKaresi => X * X + Y * Y;

public static bool operator >(Vektor sol, Vektor sag)
{
    return sol.UzunlukKaresi > sag.UzunlukKaresi;
}

public static bool operator <(Vektor sol, Vektor sag)
{
    return sol.UzunlukKaresi < sag.UzunlukKaresi;
}
```

C# bazı operatörlerin çiftler hâlinde tanımlanmasını ister. `<` ekleniyorsa `>`, `<=` ekleniyorsa `>=`, `==` ekleniyorsa `!=` de tanımlanmalıdır. Derleyici bu konuda “Birini çağırdıysan arkadaşını da getir!” yaklaşımındadır.

| Operatör | Zorunlu eşi | Örnek anlam |
|---|---|---|
| `==` | `!=` | Değer eşitliği |
| `<` | `>` | Büyüklük karşılaştırması |
| `<=` | `>=` | Sıralama ve eşitlik |
| `true` | `false` | Mantıksal değerlendirme |

## Eşitlikte dikkat edilmesi gerekenler

`==` operatörü yüklendiğinde `Equals` ve `GetHashCode` metotları da uyumlu biçimde ezilmelidir. Aksi hâlde operatöre göre eşit olan iki nesne, bir `Dictionary` veya `HashSet` içinde farklı kabul edilebilir. Eşitlik tanımı uygulamanın her noktasında aynı mantığı izlemelidir.

Operatör aşırı yükleme güçlüdür; fakat yalnızca operatörün anlamı kullanıcı için doğal olduğunda tercih edilmelidir. Bir `Musteri` nesnesini başka bir müşteriyle toplamak belirsizken, para, tarih aralığı, karmaşık sayı veya vektörleri toplamak oldukça anlaşılırdır. Ayrıca operatörün önceliği ve operand sayısı değiştirilemez. Doğru kullanıldığında bu özellik, C++'taki benzer yaklaşım gibi özel nesneleri dilin doğal parçalarıymış gibi kullanmamızı sağlar.
