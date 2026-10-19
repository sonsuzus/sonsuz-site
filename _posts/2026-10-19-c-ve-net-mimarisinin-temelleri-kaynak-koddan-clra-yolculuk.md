---
layout: post
title: "C# ve .NET Mimarisinin Temelleri: Kaynak Koddan CLR’a Yolculuk"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - dotnet
  - clr
  - derleme
  - jit
  - programlama
toc: true
image: /img/c-ve-net-45.png
---

Bir C# programında `Console.WriteLine` yazıp çalıştır düğmesine bastığımızda perde arkasında küçük bir teknoloji festivali başlar. Kaynak kod derlenir, ara dile çevrilir, çalışma zamanı tarafından incelenir ve makine koduna dönüştürülür. C# ile .NET arasındaki ilişkiyi anlamak; performans, hata ayıklama ve taşınabilirlik gibi konuları ezberden değil, sağlam bir mimari üzerinden değerlendirmeyi sağlar.

``

## C# nereden geldi?

C#, Microsoft tarafından .NET platformunun temel dillerinden biri olarak geliştirildi. Dilin baş mimarı Anders Hejlsberg’dir; ilk sürüm 2000 yılında duyurulmuş, .NET Framework ile birlikte 2002 yılında yaygın kullanıma açılmıştır. C++, Java ve Delphi gibi dillerden fikirler taşısa da zamanla kendine özgü, modern bir kimlik kazanmıştır.

C# başlangıçta Windows uygulamalarıyla özdeşleşse de günümüzde açık kaynaklı ve platformlar arası .NET üzerinde çalışır. Web uygulamalarından oyunlara, masaüstü yazılımlarından bulut servislerine kadar geniş bir kullanım alanına sahiptir.

| Kavram | C# | .NET | CLR |
|---|---|---|---|
| Temel görevi | Programlama dili sunmak | Geliştirme platformu sağlamak | Kodu çalıştırmak |
| İçeriği | Sözdizimi ve dil kuralları | Kütüphaneler, araçlar ve çalışma zamanı | JIT, GC ve tür güvenliği |
| Benzetme | Tarif | Mutfak | Aşçı |

![c-ve-net-45](/img/c-ve-net-45.svg)


Bu ayrım önemlidir: C# bir **dildir**, .NET bir **platformdur**, CLR ise bu platformun çalışma zamanı motorudur.

## Derleme süreci nasıl işler?

C# kaynak kodu doğrudan işlemcinin anlayacağı makine koduna çevrilmez. Önce Roslyn derleyicisi tarafından **Common Intermediate Language** olarak bilinen CIL’e dönüştürülür. CIL, işlemciden büyük ölçüde bağımsız bir ara dildir. Derleme sonucunda `.dll` veya `.exe` uzantılı bir **assembly** oluşur.

Bir assembly yalnızca CIL komutlarını içermez. Türler, metotlar, sürüm bilgileri ve bağımlılıklar gibi **metadata** bilgilerini de taşır. Çalıştırma sırasında CLR içindeki Just-In-Time derleyicisi, ihtiyaç duyulan metotların CIL kodunu hedef işlemcinin makine koduna çevirir.

Süreci şöyle özetleyebiliriz:

```text
C# kaynak kodu
      ↓ Roslyn
CIL + metadata içeren assembly
      ↓ CLR ve JIT
Makine kodu
      ↓
İşlemci
```

Toplam çalışma maliyeti basitleştirilmiş biçimde şu şekilde düşünülebilir:

$$T_{toplam} = T_{yükleme} + T_{JIT} + T_{çalıştırma}$$

JIT maliyeti ilk çağrıda hissedilebilir; ancak üretilen yerel kod sonraki çağrılarda yeniden kullanılabilir. .NET ayrıca uygulamayı önceden yerel koda yaklaştıran ReadyToRun ve Native AOT gibi seçenekler de sunar.

## CLR hangi işleri üstlenir?

CLR, yalnızca kodu çalıştıran pasif bir katman değildir. Bellek yönetimi, hata işleme, güvenlik kontrolleri, iş parçacıkları ve tür güvenliği gibi sorumlulukları üstlenir. En bilinen bileşenlerinden biri **Garbage Collector**, yani çöp toplayıcıdır. Artık erişilemeyen nesnelerin belleğini otomatik olarak geri kazanır.

```csharp
using System;

public sealed class Urun
{
    public string Ad { get; }
    public decimal Fiyat { get; }

    public Urun(string ad, decimal fiyat)
    {
        Ad = ad;
        Fiyat = fiyat;
    }

    public decimal KdvliFiyat(decimal oran) => Fiyat * (1 + oran);
}

var urun = new Urun("Klavye", 1200m);
Console.WriteLine(urun.KdvliFiyat(0.20m));
```

Bu örnekte `Urun` nesnesi yönetilen bellekte oluşturulur. CLR nesnenin yaşam döngüsünü izler; nesneye erişim kalmadığında ayrılan alan GC tarafından temizlenebilir. Geliştiricinin çoğu durumda belleği elle serbest bırakması gerekmez.

## CTS ve CLS neden önemlidir?

**Common Type System**, .NET dillerinin ortak tür modelini tanımlar. Örneğin C# dilindeki `int`, CLR düzeyinde `System.Int32` türüne karşılık gelir. **Common Language Specification** ise farklı .NET dillerinin birbiriyle uyumlu çalışabilmesi için takip etmesi gereken kuralları belirler.

| Bileşen | Sağladığı avantaj |
|---|---|
| CIL | İşlemci bağımsız ara temsil |
| Metadata | Tür ve bağımlılık bilgilerinin taşınması |
| JIT | Hedef sisteme uygun makine kodu |
| GC | Otomatik bellek yönetimi |
| CTS ve CLS | Diller arası uyumluluk |

Sonuç olarak C# kodu tek başına yolculuk etmez. Roslyn, CIL, assembly, JIT ve CLR katmanları birlikte çalışarak taşınabilir, güvenli ve yönetilebilir bir yürütme ortamı oluşturur. Bu mimariyi bilmek, yalnızca kod yazmayı değil, kodun gerçekte nasıl hayata geçtiğini de anlamaktır.
