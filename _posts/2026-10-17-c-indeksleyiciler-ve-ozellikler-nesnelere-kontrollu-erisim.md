---
layout: post
title: "C# İndeksleyiciler ve Özellikler: Nesnelere Kontrollü Erişim"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - indeksleyiciler
  - özellikler
  - nesne yönelimli programlama
  - kapsülleme
toc: true
image: /img/c-indeksleyiciler-ve-77.png
---

C#’ta bir nesnenin içindeki verilere erişmek için her zaman uzun metot çağrıları yazmak gerekmez. **Özellikler (properties)** alanları güvenli biçimde yönetirken, **indeksleyiciler (indexers)** nesnelerin dizi veya sözlük gibi kullanılmasını sağlar. Böylece hem okunabilir hem de kapsülleme ilkesine uygun sınıflar tasarlayabiliriz.

``

## Özellikler neden gereklidir?

Bir sınıftaki alanı `public` yapmak, dışarıdaki kodun bu alanı hiçbir denetim olmadan değiştirebilmesine yol açar. Örneğin bir ürünün fiyatı negatif olmamalıdır. Alanı gizleyip erişimi bir özellik üzerinden yönetmek bu sorunu çözer.

```csharp
public class Urun
{
    private decimal _fiyat;

    public string Ad { get; set; } = string.Empty;

    public decimal Fiyat
    {
        get => _fiyat;
        set
        {
            if (value < 0)
                throw new ArgumentOutOfRangeException(
                    nameof(value), "Fiyat negatif olamaz.");

            _fiyat = value;
        }
    }
}
```

Burada `Ad`, otomatik uygulanan bir özelliktir. Derleyici gerekli gizli alanı kendisi oluşturur. `Fiyat` ise özel bir doğrulama kuralına sahiptir. `value` anahtar sözcüğü, özelliğe atanmak istenen yeni değeri temsil eder.

Fiyat doğrulamasını matematiksel olarak şöyle ifade edebiliriz:

$$Fiyat \in [0, \infty)$$

Yani kabul edilen fiyat, sıfırdan büyük veya sıfıra eşit olmalıdır. Kullanım ise sıradan bir alan kadar sadedir:

```csharp
var kahve = new Urun
{
    Ad = "Filtre Kahve",
    Fiyat = 95.50m
};

Console.WriteLine(kahve.Fiyat);
```

## `get`, `set` ve `init` arasındaki fark

Bir özelliğin nasıl kullanılabileceği erişimcileriyle belirlenir.

| Erişimci | Görevi | Tipik kullanım |
|---|---|---|
| `get` | Değeri okur | Hesaplanan veya salt okunur veri |
| `set` | Değeri değiştirir | Sonradan güncellenebilen veri |
| `init` | Yalnızca oluşturma sırasında değer alır | Değişmez nesne modelleri |
| `private set` | Dışarıya okuma, sınıfa yazma izni verir | Kimlik ve durum alanları |

Örneğin `public int Id { get; private set; }` tanımı, kimliğin dışarıdan okunmasına izin verir; fakat değiştirilmesini sınıfın kendi metotlarıyla sınırlar.

## İndeksleyici nedir?

İndeksleyici, bir nesneye `nesne[indeks]` biçiminde erişilmesini sağlayan özel bir üyedir. Metot adı yerine `this` anahtar sözcüğü kullanılır. Aşağıdaki sınıf, öğrencilerin notlarını saklayan küçük bir koleksiyon gibi davranır:

```csharp
public class NotDefteri
{
    private readonly Dictionary<string, int> _notlar = new();

    public int this[string ogrenci]
    {
        get
        {
            if (!_notlar.TryGetValue(ogrenci, out int not))
                throw new KeyNotFoundException("Öğrenci bulunamadı.");

            return not;
        }
        set
        {
            if (value is < 0 or > 100)
                throw new ArgumentOutOfRangeException(nameof(value));

            _notlar[ogrenci] = value;
        }
    }
}
```

Bu indeksleyici `string` türünde bir anahtar alır ve `int` döndürür. Notların geçerli aralığı şu koşulla tanımlanır:

$$0 \leq not \leq 100$$

Nesne artık sözlük benzeri bir sözdizimiyle kullanılabilir:

```csharp
var defter = new NotDefteri();
defter["Ada"] = 92;
defter["Mert"] = 78;

Console.WriteLine(defter["Ada"]); // 92
```

## Özellik mi, indeksleyici mi?

| Yapı | Erişim biçimi | En uygun senaryo |
|---|---|---|
| Özellik | `nesne.Fiyat` | Tek ve anlamlı bir değere erişmek |
| İndeksleyici | `nesne[anahtar]` | Bir veri grubundaki elemana ulaşmak |
| Metot | `nesne.Bul(anahtar)` | Karmaşık işlem veya yan etki oluşturmak |

Bir sınıf birden fazla indeksleyici tanımlayabilir; örneğin hem sayısal sıra hem de metinsel anahtar kabul edebilir. Ancak aşırı kullanım, nesnenin davranışını belirsizleştirir. İndeksleyiciyi yalnızca sınıf gerçekten koleksiyon benzeri bir anlam taşıyorsa seçmek daha doğrudur.

Özetle özellikler, veriye kontrollü bir kapı açar; indeksleyiciler ise bu kapıya numara veya anahtar etiketi ekler. Doğrulama kurallarını bu üyelerde merkezileştirmek, hatalı durumların oluşmasını engeller ve sınıfın iç yapısını dış dünyadan saklar.

![c-indeksleyiciler-ve-77](/img/c-indeksleyiciler-ve-77.svg)

