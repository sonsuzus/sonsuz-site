---
layout: post
title: "C# Veri Tipleri ve Literaller: Stack, Heap ve Kimlik Meselesi"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - veri tipleri
  - struct
  - class
  - bellek yönetimi
  - literaller
toc: true
image: /img/c-veri-tipleri-44.png
---

C#’ta bir değişken tanımlarken yalnızca hangi veriyi saklayacağımızı değil, o verinin nasıl kopyalanacağını, nerede tutulacağını ve yaşam döngüsünün nasıl yönetileceğini de seçeriz. Bu seçimin merkezinde değer tipleri (`struct`) ile referans tipleri (`class`) bulunur. İkisi bazen aynı görünebilir; fakat atama işlemi gerçekleştiğinde sahne arkasında bambaşka davranırlar.

``

## Tip Sistemi ve Bellek Mantığı

C# güçlü ve statik tipli bir dildir. Her değişkenin derleme zamanında bilinen bir tipi vardır. Temel ayrım şöyledir:

- **Değer tipleri:** Verinin kendisini temsil eder. `int`, `double`, `bool`, `char`, `enum` ve kullanıcı tanımlı `struct` türleri bu gruptadır.
- **Referans tipleri:** Bir nesneye erişmek için kullanılan referansı temsil eder. `class`, `string`, diziler, delegeler ve arayüzler bu gruptadır.

“Değer tipleri daima stack’te, referans tipleri daima heap’te bulunur” açıklaması öğretici ama eksiktir. Yerleşim, değişkenin kullanıldığı bağlama bağlıdır. Bir sınıfın alanı olan `int`, sınıf nesnesiyle birlikte yönetilen bellekte bulunabilir. Esas fark **konum değil, semantiktir**: değer tipi kopyalandığında veri; referans tipi kopyalandığında referans kopyalanır.

| Özellik | Değer tipi (`struct`) | Referans tipi (`class`) |
|---|---|---|
| Atamada kopyalanan | Değerin tamamı | Nesne referansı |
| Varsayılan değer | Sıfırlanmış değer | `null` |
| Kimlik kavramı | Genellikle yoktur | Nesne kimliği vardır |
| Kalıtım | Başka struct’tan kalıtım alamaz | Sınıf kalıtımını destekler |
| Uygun kullanım | Küçük, tek parça değerler | Kimliği ve davranışı olan nesneler |

## Kopyalama Davranışı

Aşağıdaki örnek farkı görünür hâle getirir:

```csharp
public struct Point
{
    public int X;
}

public class Player
{
    public int Score;
}

Point p1 = new Point { X = 10 };
Point p2 = p1;
p2.X = 99;

Player a = new Player { Score = 10 };
Player b = a;
b.Score = 99;

Console.WriteLine(p1.X);      // 10
Console.WriteLine(a.Score);   // 99
```

`p2`, `p1` değerinin bağımsız kopyasıdır. Buna karşılık `a` ve `b`, aynı `Player` nesnesini gösterir. Bunu basitçe şöyle düşünebiliriz:

$$p2 = copy(p1)$$

$$b = reference(a)$$

Büyük struct’ların sık kopyalanması maliyet oluşturabilir. Salt okunur parametrelerde `in`, kopyalama ihtiyacını azaltabilir. Yine de performans kararı ölçüm yapılarak verilmelidir; “struct her zaman hızlıdır” diye sihirli bir kural yoktur.

## Literaller: Değerleri Kodda Yazmak

Literal, bir değerin kaynak kodundaki doğrudan gösterimidir. C# farklı türler için çeşitli literal biçimleri sunar:

```csharp
int decimalNumber = 42;
int binaryNumber = 0b_101010;
int hexNumber = 0x2A;
long population = 8_000_000_000L;
float ratio = 1.5F;
decimal price = 19.99M;
char letter = 'A';
string message = "Merhaba";
bool isReady = true;
object? missing = null;
```

Alt çizgiler sayının okunmasını kolaylaştırır ve değeri değiştirmez. `F`, `M`, `L` gibi sonekler ise literal türünü belirtir. Örneğin `1.5` varsayılan olarak `double`, `1.5F` ise `float` kabul edilir.

| Literal | Varsayılan veya belirtilen tip | Not |
|---|---|---|
| `42` | `int` | Tam sayı |
| `42L` | `long` | `L` soneki kullanır |
| `3.14` | `double` | Varsayılan ondalıklı tip |
| `3.14M` | `decimal` | Finansal hesaplara uygundur |
| `'C'` | `char` | Tek tırnak kullanır |
| `"C#"` | `string` | Çift tırnak kullanır |

## Boxing ve Unboxing

Değer tipi, `object` veya bir arayüz türüne dönüştürüldüğünde **boxing** gerçekleşebilir:

```csharp
int score = 100;
object boxed = score;       // Boxing: değer nesne olarak paketlenir
int restored = (int)boxed;  // Unboxing: değer geri çıkarılır
```

Boxing ek tahsis ve kopyalama oluşturabileceği için yoğun döngülerde önem kazanabilir. Generic koleksiyonlar bu maliyeti çoğu durumda önler; `ArrayList` yerine `List<int>` kullanmak buna güzel bir örnektir.

Özetle `struct`, koordinat veya renk gibi küçük ve değer odaklı modellerde; `class` ise kullanıcı ya da sipariş gibi kimliği, paylaşılan durumu ve yaşam döngüsü bulunan modellerde güçlüdür. Doğru seçim, yalnızca belleğin nerede olduğuna değil, modellediğiniz kavramın “değer mi, nesne mi?” olduğuna bağlıdır.

![c-veri-tipleri-44](/img/c-veri-tipleri-44.svg)

