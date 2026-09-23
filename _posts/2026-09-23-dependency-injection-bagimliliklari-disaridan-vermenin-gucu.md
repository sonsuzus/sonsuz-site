---
layout: post
title: "Dependency Injection: Bağımlılıkları Dışarıdan Vermenin Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - dependency injection
  - yazılım mimarisi
  - solid
  - test edilebilirlik
  - nesne yönelimli programlama
toc: true
---

Bir sınıfın ihtiyaç duyduğu nesneleri kendi içinde üretmesi ilk bakışta oldukça doğal görünür. Sonuçta kahve isteyen bir `OfisCalisani`, kahve makinesini de çalıştırabilir! Ancak sistem büyüdükçe sınıfların hem kendi işlerini yapması hem de bağımlılıklarını oluşturması; değişiklik, test ve bakım maliyetlerini yükseltir. Dependency Injection, yani Bağımlılık Enjeksiyonu, tam bu noktada devreye girer: Bir nesneye ihtiyaçları hazır olarak dışarıdan verilir.
``
## Önce bağımlılık nedir?

Bir sınıf görevini yerine getirirken başka bir nesneye ihtiyaç duyuyorsa, o nesne sınıfın bağımlılığıdır. Örneğin `SiparisServisi`, ödeme alabilmek için bir ödeme sağlayıcısına ihtiyaç duyabilir.

Bağımlılığın sınıf içinde oluşturulduğu yaklaşımı düşünelim:

```csharp
public class SiparisServisi
{
    private readonly KrediKartiOdeme odeme;

    public SiparisServisi()
    {
        odeme = new KrediKartiOdeme();
    }

    public void SiparisVer(decimal tutar)
    {
        odeme.Ode(tutar);
    }
}
```

Bu kod çalışır; fakat `SiparisServisi`, doğrudan `KrediKartiOdeme` sınıfına bağlanmıştır. Yarın ödeme yöntemi havale olursa sınıfı değiştirmek gerekir. Test sırasında gerçekten ödeme yapılmasını engellemek de ayrı bir maceraya dönüşür.

## Dependency Injection neyi değiştirir?

DI yaklaşımında sınıf, bağımlılığını üretmez. Hangi somut nesnenin kullanılacağına dışarıdaki kod karar verir:

```csharp
public interface IOdeme
{
    void Ode(decimal tutar);
}

public class SiparisServisi
{
    private readonly IOdeme odeme;

    // Bağımlılık constructor üzerinden dışarıdan alınır.
    public SiparisServisi(IOdeme odeme)
    {
        this.odeme = odeme;
    }

    public void SiparisVer(decimal tutar)
    {
        odeme.Ode(tutar);
    }
}
```

Artık servis, ödemenin kredi kartıyla mı, havaleyle mi yoksa test amaçlı sahte bir sınıfla mı gerçekleştirildiğini bilmez. Yalnızca `IOdeme` sözleşmesine güvenir.

| Özellik | Bağımlılığı içeride oluşturmak | Bağımlılığı dışarıdan vermek |
|---|---|---|
| Bağlılık | Somut sınıfa yüksek bağlılık | Arayüze düşük bağlılık |
| Test | Gerçek servisleri ayırmak zor | Sahte nesne vermek kolay |
| Değişiklik | Tüketen sınıf da değişir | Yeni implementasyon eklenir |
| Sorumluluk | İş mantığı ve nesne üretimi karışır | Sorumluluklar ayrılır |

## Neden matematiksel olarak da avantajlı?

Bir sınıfın değişme maliyetini kabaca bağımlılık sayısı ve bağlılık derecesiyle modelleyebiliriz:

$$M = n \times b$$

Burada $M$ değişiklik maliyetini, $n$ bağımlılık sayısını, $b$ ise bağımlılıkların ne kadar sıkı olduğunu temsil eder. DI bağımlılık sayısını sihirli biçimde azaltmaz; fakat $b$ değerini düşürür. Böylece sistem büyüdüğünde değişikliklerin zincirleme etkisi daha sınırlı kalır.

Bu fikir, SOLID ilkelerindeki Dependency Inversion Principle ile yakından ilişkilidir: Üst seviye iş kuralları, alt seviye teknik ayrıntılara değil, soyutlamalara bağlı olmalıdır.

## Testlerde sağladığı rahatlık

Gerçek ödeme sistemine bağlanmadan davranışı sınamak için sahte bir bağımlılık yazabiliriz:

```csharp
public class SahteOdeme : IOdeme
{
    public bool Cagrildi { get; private set; }

    public void Ode(decimal tutar)
    {
        Cagrildi = true;
    }
}

var sahte = new SahteOdeme();
var servis = new SiparisServisi(sahte);

servis.SiparisVer(250);
Console.WriteLine(sahte.Cagrildi); // True
```

Bu test hızlıdır, internete ihtiyaç duymaz ve yanlışlıkla gerçek kredi kartından para çekmez. Test ekibinin kalp sağlığı açısından önemli bir ayrıntı!

## Enjeksiyon yöntemleri

| Yöntem | Kullanım alanı | Not |
|---|---|---|
| Constructor injection | Zorunlu bağımlılıklar | En güvenli ve yaygın yöntem |
| Property injection | İsteğe bağlı bağımlılıklar | Nesne eksik yapılandırılabilir |
| Method injection | Tek bir işlemde gereken bağımlılık | Kullanım alanı sınırlıdır |

Modern .NET, Spring ve NestJS gibi çatılar, bağımlılıkları bir DI container üzerinden otomatik eşleştirebilir. Yine de DI yalnızca bir kütüphane özelliği değildir; nesne oluşturma sorumluluğunu iş mantığından ayıran bir tasarım yaklaşımıdır.

Kısacası Dependency Injection, kodu gereksiz yere büyütmek için değil, parçaların birbirine kaynak yapılması yerine değiştirilebilir fişlerle bağlanması için kullanılır. Küçük projede fazladan birkaç satır gibi görünse de büyüyen sistemlerde test edilebilirlik, esneklik ve bakım kolaylığı olarak karşılığını fazlasıyla verir.
