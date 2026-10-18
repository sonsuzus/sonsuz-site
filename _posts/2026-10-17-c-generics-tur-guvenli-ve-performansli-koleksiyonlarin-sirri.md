---
layout: post
title: "C# Generics: Tür Güvenli ve Performanslı Koleksiyonların Sırrı"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - generics
  - koleksiyonlar
  - tür güvenliği
  - performans
  - dotnet
toc: true
image: /img/c-generics-tur-63.png
---

Bir kutuya kalem koyup daha sonra içinden kahve kupası çıkarmayı beklemezsiniz. C# koleksiyonlarında da benzer bir düzen gerekir: Eklenen ve alınan değerlerin türü önceden bilinmelidir. Genel türler, yani *generics*, bu düzeni derleme zamanında sağlayarak çalışma anındaki sürpriz tür dönüşümü hatalarını azaltır ve özellikle değer türlerinde daha iyi performans sunar.

``

## Generic yapı nedir?

Generic yapı; sınıf, metot, arayüz veya temsilcinin çalışacağı veri türünü baştan sabitlemek yerine bir tür parametresiyle tanımlamaktır. En yaygın gösterim olan `T`, İngilizce *type* kelimesinden gelir; ancak zorunlu bir isim değildir.

```csharp
public class Kutu<T>
{
    public T Deger { get; set; }

    public Kutu(T deger)
    {
        Deger = deger;
    }
}

var sayiKutusu = new Kutu<int>(42);
var metinKutusu = new Kutu<string>("Merhaba");
```

Burada aynı `Kutu<T>` sınıfı hem `int` hem de `string` ile kullanılabilir. Buna rağmen iki kutunun kuralları birbirinden ayrıdır. Örneğin `sayiKutusu.Deger` özelliğine metin atanması derleme aşamasında engellenir.

## Eski yaklaşım ve tür güvenliği

Generic koleksiyonlardan önce farklı türleri saklamak için sıklıkla `ArrayList` kullanılırdı. Bu koleksiyon elemanları `object` olarak tuttuğu için hemen her şeyi kabul eder.

```csharp
using System.Collections;

var liste = new ArrayList();
liste.Add(10);
liste.Add("yirmi");

int toplam = (int)liste[0] + (int)liste[1]; // Çalışma zamanı hatası
```

Kod derlenir; fakat ikinci eleman `int` olmadığı için `InvalidCastException` oluşur. `List<int>` kullanıldığında yanlış değer daha program çalışmadan yakalanır:

```csharp
var sayilar = new List<int>();
sayilar.Add(10);
// sayilar.Add("yirmi"); // Derleme hatası

int toplam = sayilar[0]; // Dönüşüm gerekmiyor
```

| Özellik | `ArrayList` | `List<T>` |
|---|---|---|
| Eleman türü | `object` | Belirlenen `T` |
| Hata tespiti | Çalışma zamanında | Derleme zamanında |
| Açık dönüşüm | Genellikle gerekli | Gerekli değil |
| Değer türü maliyeti | Boxing/unboxing olabilir | Genellikle önlenir |
| Kod okunabilirliği | Daha düşük | Daha yüksek |

![c-generics-tur-63](/img/c-generics-tur-63.svg)


## Performans neden artar?

`int`, `double` ve `bool` gibi değer türleri doğrudan değer taşır. Bunların `object` değişkenine yerleştirilmesine **boxing**, yeniden özgün türe çevrilmesine **unboxing** denir. Her boxing işlemi yönetilen bellekte ek bir nesne oluşturabilir ve dönüşüm maliyeti doğurabilir.

Basitleştirilmiş biçimde, $n$ elemanın boxing maliyeti $b$, unboxing maliyeti $u$ ise ek işlem yükü şöyle düşünülebilir:

$$C_{eski} \approx n(b + u)$$

Generic bir `List<int>` için bu dönüşümlerin çoğu ortadan kalktığından yaklaşık ek yük:

$$C_{generic} \approx 0$$

Gerçek performans donanıma, .NET sürümüne ve kullanım şekline bağlıdır; dolayısıyla bu eşitlik bir ölçüm değil, maliyet farkını anlatan zihinsel modeldir.

## Generic metotlar ve kısıtlar

Generics yalnızca koleksiyonlara özgü değildir. Metotlar da tür parametresi alabilir:

```csharp
static T IlkElemaniGetir<T>(IEnumerable<T> kaynak)
{
    return kaynak.First();
}

int ilkSayi = IlkElemaniGetir(new[] { 7, 8, 9 });
string ilkAd = IlkElemaniGetir(new[] { "Ada", "Linus" });
```

Bazen `T` tamamen serbest bırakılmamalıdır. `where` kısıtları, kabul edilen türlerin sahip olması gereken özellikleri belirtir:

```csharp
static T YeniOlustur<T>() where T : class, new()
{
    return new T();
}
```

Bu metot yalnızca referans türleriyle çalışır ve parametresiz kurucu ister. Yaygın kısıtlar arasında `class`, `struct`, `notnull`, `new()` ve belirli bir arayüz bulunur.

## Hangi koleksiyon seçilmeli?

| İhtiyaç | Generic koleksiyon |
|---|---|
| Sıralı eleman listesi | `List<T>` |
| Anahtar-değer eşleşmesi | `Dictionary<TKey, TValue>` |
| Benzersiz elemanlar | `HashSet<T>` |
| İlk giren ilk çıkar | `Queue<T>` |
| Son giren ilk çıkar | `Stack<T>` |

Generics; tekrar kullanılabilirliği, tür güvenliğini ve okunabilirliği aynı yapıda buluşturur. En önemli kazanç yalnızca hız değildir: Hataları kullanıcıya ulaşmadan derleyicide durdurmaktır. Kısacası `T`, küçük bir harf olsa da C# dünyasında oldukça büyük bir güvenlik görevlisidir.
