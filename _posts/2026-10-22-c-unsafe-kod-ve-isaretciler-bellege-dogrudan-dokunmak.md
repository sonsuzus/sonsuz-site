---
layout: post
title: "C# Unsafe Kod ve İşaretçiler: Belleğe Doğrudan Dokunmak"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - unsafe
  - işaretçiler
  - bellek-yönetimi
  - performans
  - dotnet
toc: true
image: /img/c-unsafe-kod-73.png
---

![c-unsafe-kod-73](/img/c-unsafe-kod-73.svg)


C# çoğunlukla güvenli ve yönetilen bir dünyada çalışır: Belleği çöp toplayıcı düzenler, dizilerin sınırları denetlenir ve geliştirici adres hesaplarıyla uğraşmaz. Ancak görüntü işleme, oyun motorları, yerel kütüphane entegrasyonu veya çok düşük gecikmeli sistemler söz konusu olduğunda bu konforun küçük bir performans maliyeti olabilir. `unsafe` kod, C# geliştiricisine C++ benzeri işaretçilerle belleğe doğrudan erişim imkânı verir. Güçlüdür; fakat emniyet kemerini çıkarmaya benzediği için dikkatli kullanılmalıdır.

``

## Yönetilen bellekten işaretçilere

Normal C# referansı bir nesneyi gösterir, ancak nesnenin fiziksel adresini geliştiriciye açmaz. İşaretçi ise bellekteki adresi doğrudan tutar. `int*` ifadesi, bir `int` değerinin adresini taşıyan işaretçi anlamına gelir.

Bir işaretçinin kaba bellek modeli şöyle ifade edilebilir:

$$\text{hedef adres} = \text{başlangıç adresi} + i \times \text{veri tipi boyutu}$$

Örneğin `int` 4 baytsa `p + 3`, başlangıçtan yaklaşık $3 \times 4 = 12$ bayt ilerideki elemana ulaşır. İşaretçi aritmetiği bayt yerine hedef türün boyutunu hesaba kattığından kullanışlıdır.

| Özellik | Güvenli C# | Unsafe C# |
|---|---|---|
| Bellek erişimi | Referanslar üzerinden | Doğrudan adres üzerinden |
| Sınır kontrolü | Genellikle var | İşaretçide yok |
| Çöp toplayıcı uyumu | Otomatik | Sabitleme gerekebilir |
| Hata riski | Daha düşük | Bellek bozulması mümkün |
| Tipik kullanım | İş uygulamaları | Yerel API, medya, oyun, optimizasyon |

## Unsafe kodu etkinleştirme

Önce proje dosyasına aşağıdaki ayar eklenir:

```xml
<PropertyGroup>
  <AllowUnsafeBlocks>true</AllowUnsafeBlocks>
</PropertyGroup>
```

Visual Studio kullanılıyorsa aynı seçenek proje özelliklerindeki **Build > Allow code that uses the unsafe keyword** alanından etkinleştirilebilir. Ardından yalnızca gerekli metot veya blok `unsafe` olarak işaretlenmelidir; tüm sınıfı tehlike bölgesine çevirmek şart değildir.

```csharp
unsafe static void DegeriDegistir()
{
    int sayi = 10;
    int* adres = &sayi;

    *adres = 42;
    Console.WriteLine(sayi);
}
```

Burada `&sayi`, değişkenin adresini alır. `*adres` ise o adresteki değere erişir; buna **dereference** işlemi denir. Sonuç `42` olur. Yanlış veya artık geçerli olmayan bir adres kullanılırsa çalışma zamanı her zaman sizi kurtaramaz.

## GC hareketine karşı `fixed`

Çöp toplayıcı, belleği sıkıştırırken yönetilen nesnelerin yerini değiştirebilir. Bir dizi işaretçiyle işlenirken taşınırsa işaretçi eski adresi göstermeye devam eder. `fixed`, nesneyi blok süresince yerine sabitler:

```csharp
unsafe static int Topla(int[] sayilar)
{
    int toplam = 0;

    fixed (int* baslangic = sayilar)
    {
        for (int i = 0; i < sayilar.Length; i++)
            toplam += *(baslangic + i);
    }

    return toplam;
}
```

Bu kod dizinin başlangıç adresini alır ve işaretçi aritmetiğiyle elemanları gezer. `fixed` blokları kısa tutulmalıdır; uzun süre sabitlenen nesneler çöp toplayıcının belleği verimli düzenlemesini zorlaştırabilir.

## `stackalloc` ve modern alternatifler

Küçük, geçici tamponlar yığında oluşturulabilir:

```csharp
unsafe static int KarelerToplami(int adet)
{
    int* tampon = stackalloc int[adet];
    int toplam = 0;

    for (int i = 0; i < adet; i++)
    {
        tampon[i] = i * i;
        toplam += tampon[i];
    }

    return toplam;
}
```

`stackalloc`, çöp toplayıcıya yük bindirmez; ancak yığın kapasitesi sınırlıdır. Büyük veya kullanıcı tarafından kontrol edilen boyutlar yığın taşmasına yol açabilir. Ayrıca pek çok senaryoda `Span<T>` aynı performans hedefini daha güvenli sınır kontrolleriyle karşılar.

| Araç | Güvenlik | Uygun senaryo |
|---|---:|---|
| Dizi | Yüksek | Genel amaçlı veri |
| `Span<T>` | Yüksek | Hızlı dilimleme ve tamponlar |
| `stackalloc` | Orta | Küçük, kısa ömürlü tampon |
| Ham işaretçi | Düşük | Yerel API ve özel optimizasyon |

Unsafe kod otomatik olarak daha hızlı değildir. JIT derleyicisi güvenli kodu zaten güçlü biçimde optimize eder. Önce BenchmarkDotNet gibi araçlarla ölçüm yapılmalı, darboğaz kanıtlanmalı ve yalnızca kritik bölüm unsafe hâle getirilmelidir. Kural basit: Ölçmeden işaretçiye sarılmayın; kullandığınızda adresleri, sınırları ve nesne ömürlerini titizlikle yönetin.
