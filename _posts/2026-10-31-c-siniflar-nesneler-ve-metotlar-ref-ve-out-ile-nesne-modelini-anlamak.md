---
layout: post
title: "C# Sınıflar, Nesneler ve Metotlar: ref ve out ile Nesne Modelini Anlamak"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - nesne-yönelimli-programlama
  - sınıflar
  - nesneler
  - metotlar
  - ref
  - out
toc: true
image: /img/c-siniflar-nesneler-62.png
---

![c-siniflar-nesneler-62](/img/c-siniflar-nesneler-62.svg)


Bir banka hesabını programlamak istediğinizi düşünün: hesabın bakiyesi vardır, para çekilebilir ve işlemin sonucu öğrenilebilir. C# bu dünyayı sınıflar, nesneler ve metotlarla temsil eder. İşin eğlenceli kısmı, aynı hesaba iki farklı değişkenle ulaşabilmenizdir. Ancak bir nesneyi değiştirmekle, değişkenin gösterdiği nesneyi değiştirmek aynı şey değildir!

``

## Sınıf plan, nesne çalışan örnektir

**Sınıf**, verileri ve davranışları bir araya getiren tür tanımıdır. **Nesne**, bu sınıftan oluşturulan somut örnektir. **Metot** ise bir nesnenin gerçekleştirebildiği işlemi tanımlar; ayrıca sınıfa ait statik metotlar da bulunabilir.

Bir sınıftan oluşturulan iki nesnenin bakiyeleri birbirinden bağımsız olabilir. Buna karşılık iki değişken aynı nesneye bağlanabilir. Aynı televizyonu yöneten iki kumanda düşünün: kumandalar farklıdır, fakat değiştirilen televizyon aynıdır.

| Kavram | Banka örneği | Görevi |
|---|---|---|
| Sınıf | `Hesap` | Yapıyı ve davranışları tanımlar |
| Nesne | Oluşturulan müşteri hesabı | Durumu taşır |
| Özellik | `Bakiye` | Veriye kontrollü erişim sağlar |
| Metot | `ParaCek` | İşlem gerçekleştirir |

C# sınıfları **referans türüdür**. Bir sınıf değişkeninin değeri, nesnenin kendisi değil, ona erişmeyi sağlayan referanstır. Referansı kopyalamak, nesneyi çoğaltmaz.

## Durumu davranışla korumak

Aşağıdaki sınıf, bakiyenin dışarıdan doğrudan değiştirilmesini engeller. Kurucu metot başlangıç durumunu oluşturur; `ParaCek` ise çekim kurallarını uygular ve sonucu bildirir.

```csharp
using System;

public class Hesap
{
    public decimal Bakiye { get; private set; }

    public Hesap(decimal bakiye)
    {
        if (bakiye < 0)
            throw new ArgumentOutOfRangeException(nameof(bakiye));

        Bakiye = bakiye;
    }

    public bool ParaCek(decimal tutar, out decimal kalan)
    {
        kalan = Bakiye;

        if (tutar <= 0 || tutar > Bakiye)
            return false;

        Bakiye -= tutar;
        kalan = Bakiye;
        return true;
    }
}
```

`private set`, bakiyenin yalnızca sınıf içinden atanabilmesini sağlar. Bu yaklaşım **kapsülleme** olarak adlandırılır: veriyi saklamaktan çok, geçerli durumları korumak önemlidir. Negatif başlangıç bakiyesi reddedilir; geçersiz çekim ise hesabı değiştirmez.

Başarılı çekimin matematiksel modeli şöyledir:

$$B_{son} = B_{ilk} - T$$

Burada $T$ çekilen tutardır; işlemin kabul koşulu $0 < T \leq B_{ilk}$ şeklindedir. Kod, bu koşulu denetleyerek nesnenin tutarlılığını korur. Para hesaplarında `decimal`, ondalık değerleri temsil etmek için genellikle `double` türünden daha uygundur.

## Varsayılan aktarım, ref ve out

C# parametreleri varsayılan olarak **değer ile** aktarır. `decimal` parametresinde sayısal değer kopyalanır. `Hesap` parametresinde ise referansın değeri kopyalanır. Bu yüzden normal bir parametre üzerinden nesnenin özelliklerini değiştirmek mümkündür; bunun için `ref` gerekmez.

Ancak metot içinde normal parametreye `new Hesap(...)` atamak, çağıranın değişkenini başka nesneye yönlendirmez. Yalnızca parametrenin yerel kopyası değişir. İşte `ref`, çağıranın değişkenine erişim sağlayarak bu ayrımı görünür kılar.

| Aktarım | Çağrıdan önce değer gerekli mi? | Metodun atama zorunluluğu | Amaç |
|---|---|---|---|
| Normal | Evet | Yok | Değerin kopyasıyla çalışmak |
| `ref` | Evet | Yok | Mevcut değişkeni okuyup değiştirmek |
| `out` | Hayır | Her normal dönüş yolunda var | Sonuç üretmek |

`ref` ve `out`, hem metot bildiriminde hem çağrıda belirtilir. `out` parametresi, metot içinde okunmadan önce atanmalıdır. Örneğimizde `kalan` başlangıçta atanır; böylece başarısız çekimde bile kullanılabilir bir sonuç döner.

## Referansı değiştirmek başka bir iştir

.NET 6+ konsol projesinde aşağıdaki üst düzey kullanım kodunu sınıf bildiriminden önce yerleştirebilirsiniz:

```csharp
var hesap = new Hesap(100m);
var ortak = hesap;

bool basarili = hesap.ParaCek(30m, out decimal kalan);
Console.WriteLine($"Başarılı: {basarili}, kalan: {kalan}");

ortak.ParaCek(10m, out kalan);
Console.WriteLine(hesap.Bakiye); // 60

Yenile(ref hesap);
Console.WriteLine(hesap.Bakiye); // 0
Console.WriteLine(ortak.Bakiye); // 60

static void Yenile(ref Hesap hedef)
{
    hedef = new Hesap(0m);
}
```

İlk atamada `ortak` ve `hesap` aynı nesneyi gösterir. Dolayısıyla `ortak` üzerinden yapılan çekim, `hesap` üzerinden görülen bakiyeyi de değiştirir. `Yenile` ise `ref` sayesinde doğrudan `hesap` değişkeninin referansını değiştirir. `ortak`, eski nesneyi göstermeyi sürdürür; nesne topluca sıfırlanmamıştır.

## Küçük bir seçim rehberi

Tek sonuç için çoğunlukla dönüş değerini kullanın. Başarı bilgisiyle ek sonuç gerekiyorsa `out` kullanışlıdır; `int.TryParse` bunun klasik örneğidir. Çağıranın mevcut değişkenini değiştirmek gerekiyorsa `ref` düşünülebilir. Son kontrol sorunuz şu olsun: “Nesnenin durumunu mu, değişkenin değerini mi değiştiriyorum?” Bu ayrım, referans karmaşasının büyük bölümünü çözer.
