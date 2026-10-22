---
layout: post
title: "C# Diziler ve String İşlemleri: Veriyi Düzenlemenin Akıllı Yolları"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - diziler
  - string
  - jagged-array
  - stringbuilder
  - programlama
toc: true
image: /img/c-diziler-ve-74.png
---

C# dünyasında diziler ve metinler, veriyi saklamanın ve işlemenin temel araçlarıdır. Bir sınıftaki notları, oyun haritasındaki hücreleri veya bir metindeki kelimeleri yönetirken bu yapılarla karşılaşırız. Diziler düzenli veri kutuları gibiyken `string`, karakterlerden oluşan özel ve değiştirilemez bir koleksiyondur. Gelin bu araçların teorisini ve pratik kullanımını birlikte inceleyelim.

``

## Dizilerin temel mantığı

Dizi, aynı türden belirli sayıda elemanı ardışık indekslerle saklayan veri yapısıdır. İndeksler sıfırdan başladığı için uzunluğu $n$ olan bir dizinin geçerli indeks aralığı $0 \le i < n$ şeklindedir. Bir elemana indeksle erişmenin zaman karmaşıklığı sabittir:

$$T(n)=O(1)$$

Buna karşılık aranan değerin konumu bilinmiyorsa tüm elemanların gezilmesi gerekebilir ve doğrusal aramanın maliyeti $O(n)$ olur.

```csharp
int[] notlar = { 75, 90, 68, 100 };
int toplam = 0;

foreach (int not in notlar)
{
    toplam += not;
}

double ortalama = (double)toplam / notlar.Length;
Console.WriteLine($"Ortalama: {ortalama:F2}");
```

Bu örnek tek boyutlu diziyi dolaşır. Tür dönüşümü yapılmasaydı iki `int` değerin bölümü tam sayı üretirdi; `(double)` dönüşümü küsuratı korur.

## Çok boyutlu ve düzensiz diziler

Çok boyutlu diziler satır ve sütunları eşit olan dikdörtgen tabloları temsil eder. Düzensiz, yani jagged diziler ise her satırında farklı sayıda eleman taşıyabilen dizilerin dizisidir.

| Yapı | Tanım | Uygun kullanım | Erişim biçimi |
|---|---|---|---|
| Tek boyutlu | Doğrusal eleman listesi | Notlar, fiyatlar | `dizi[i]` |
| Çok boyutlu | Dikdörtgen matris | Tahta, tablo, piksel alanı | `dizi[i, j]` |
| Jagged | Satır uzunlukları değişken yapı | Gruplar, değişken seviyeler | `dizi[i][j]` |

```csharp
int[,] harita =
{
    { 1, 0, 1 },
    { 0, 1, 0 }
};

int[][] gruplar =
{
    new[] { 10, 20 },
    new[] { 30, 40, 50 },
    new[] { 60 }
};

Console.WriteLine(harita[1, 1]); // 1
Console.WriteLine(gruplar[1][2]); // 50
```

`int[,]` tek bir dikdörtgen bloktur. `int[][]` içindeki her satır ise bağımsız bir dizidir. Bu esneklik bellek kullanımını azaltabilir; ancak satırların ayrı ayrı oluşturulması ve kontrol edilmesi gerekir.

## String: Karakter dizisinden daha fazlası

`string`, kavramsal olarak karakter dizisine benzese de **immutable**, yani değiştirilemez bir referans türüdür. Birleştirme veya değiştirme işlemi mevcut metni düzenlemez; yeni bir `string` üretir.

```csharp
string mesaj = "  C# diziler eğlencelidir  ";
string temiz = mesaj.Trim();
string[] kelimeler = temiz.Split(' ', StringSplitOptions.RemoveEmptyEntries);
string sonuc = string.Join(" | ", kelimeler).ToUpperInvariant();

Console.WriteLine(sonuc);
```

Burada `Trim` kenar boşluklarını kaldırır, `Split` metni parçalara ayırır, `Join` parçaları yeniden birleştirir. `ToUpperInvariant`, sonucu kullanıcının bölgesel dil ayarlarından bağımsız biçimde büyük harfe dönüştürür.

| İşlem | Yöntem | Sonuç |
|---|---|---|
| Arama | `Contains`, `IndexOf` | Metin veya konum bulur |
| Parçalama | `Split`, `Substring` | Alt metin üretir |
| Değiştirme | `Replace` | Yeni metin döndürür |
| Doğrulama | `StartsWith`, `EndsWith` | `bool` değer üretir |

## Çok sayıda birleştirmede StringBuilder

Döngü içinde `+` kullanmak çok sayıda geçici nesne oluşturabilir. Bu durumda `StringBuilder`, değiştirilebilir bir karakter tamponu sunar:

```csharp
using System.Text;

var rapor = new StringBuilder();
foreach (int not in notlar)
{
    rapor.Append("Not: ").AppendLine(not.ToString());
}

Console.WriteLine(rapor.ToString());
```

Az sayıdaki birleştirmede string interpolation okunaklıdır; yoğun işlemlerde ise `StringBuilder` daha verimlidir. Özetle doğru dizi türünü veri şekline, doğru metin aracını da işlem yoğunluğuna göre seçmek hem performansı hem kod okunabilirliğini artırır.

![c-diziler-ve-74](/img/c-diziler-ve-74.svg)

