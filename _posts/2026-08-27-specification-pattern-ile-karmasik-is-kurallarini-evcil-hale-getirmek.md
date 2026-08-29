---
layout: post
title: "Specification Pattern ile Karmaşık İş Kurallarını Evcil Hale Getirmek"
math: true
categories: 
  - Bilgi
tags: 
  - specification pattern
  - tasarım desenleri
  - c#
  - domain-driven design
---

İş kuralları büyüdükçe kod tabanında küçük bir canavar belirir: her yerde çoğalan `if` koşulları. “Müşteri aktif mi?”, “Sepet tutarı yeterli mi?”, “Ürün stokta mı?” gibi sorular önce masum görünür; sonra aynı kontroller servis, API ve rapor katmanlarında kopyalanır. Specification Pattern, bu kuralları isimlendirilmiş, test edilebilir ve birleştirilebilir nesnelere dönüştürerek canavarı evcilleştirir.

``

Desenin temel fikri basittir: Bir specification, belirli bir nesnenin kurala uyup uymadığını söyler. Matematiksel açıdan bir kuralı, bir küme üzerinde çalışan önerme olarak düşünebiliriz. Bir müşteri kümesi $M$ için “aktif müşteri” kuralı şu fonksiyondur:

$$S_{aktif}: M \rightarrow \{true, false\}$$

Asıl güç, bu önermelerin mantıksal operatörlerle birleştirilmesidir. Örneğin indirim için müşteri hem aktif **ve** sadakat puanı yüksek olmalıdır:

$$S_{indirim} = S_{aktif} \land S_{sadik}$$

Böylece iş dili doğrudan koda yaklaşır: `aktifVeSadikMi`. Bu yaklaşım, kuralın nasıl çalıştığından çok ne anlattığını öne çıkarır.

| Geleneksel yaklaşım | Specification Pattern |
|---|---|
| Koşullar servis metoduna gömülür | Her kural bağımsız bir sınıftır |
| Aynı `if` blokları kopyalanabilir | Kurallar tekrar kullanılabilir |
| Test için büyük akış hazırlanır | Her kural tek başına test edilir |
| Yeni kombinasyonlar karmaşıklaşır | `And`, `Or`, `Not` ile kurulur |

C# tarafında önce küçük bir sözleşme tanımlayalım. `IsSatisfiedBy`, aday nesnenin kurala uygunluğunu döndürür. Ayrıca `And` metodu iki kuralı okunabilir biçimde bir araya getirir.

```csharp
public interface ISpecification<T>
{
    bool IsSatisfiedBy(T candidate);

    ISpecification<T> And(ISpecification<T> other)
        => new AndSpecification<T>(this, other);
}

public sealed class AndSpecification<T> : ISpecification<T>
{
    private readonly ISpecification<T> left;
    private readonly ISpecification<T> right;

    public AndSpecification(ISpecification<T> left, ISpecification<T> right)
        => (this.left, this.right) = (left, right);

    public bool IsSatisfiedBy(T candidate)
        => left.IsSatisfiedBy(candidate) && right.IsSatisfiedBy(candidate);
}
```

Şimdi kuralları somutlaştıralım. Buradaki sınıflar yalnızca karar verir; indirim uygulamak, e-posta göndermek veya veritabanına yazmak gibi yan etkiler içermez. Bu ayrım, testleri hızlı ve güvenilir yapar.

```csharp
public record Customer(bool IsActive, int LoyaltyPoints);

public sealed class ActiveCustomerSpecification : ISpecification<Customer>
{
    public bool IsSatisfiedBy(Customer customer) => customer.IsActive;
}

public sealed class MinimumLoyaltySpecification : ISpecification<Customer>
{
    private readonly int minimumPoints;

    public MinimumLoyaltySpecification(int minimumPoints)
        => this.minimumPoints = minimumPoints;

    public bool IsSatisfiedBy(Customer customer)
        => customer.LoyaltyPoints >= minimumPoints;
}

var eligibleForDiscount = new ActiveCustomerSpecification()
    .And(new MinimumLoyaltySpecification(1_000));

bool canReceiveDiscount = eligibleForDiscount.IsSatisfiedBy(customer);
```

Bu kodun güzelliği, iş analistinin cümlesine yakın okunmasıdır: “Aktif müşteri ve en az 1000 sadakat puanı.” Yeni bir “VIP müşteri” kuralı geldiğinde mevcut servisleri ameliyat etmek yerine yeni bir specification eklersiniz.

Yine de her `if` için sınıf üretmek şart değildir. Tek kullanımlık, basit doğrulamalar için doğrudan koşul daha ekonomiktir. Specification Pattern; kural tekrar kullanılıyorsa, farklı biçimlerde birleştirilecekse, ayrı test edilmesi gerekiyorsa veya sorguya dönüştürülecekse parıldar. Özellikle DDD projelerinde domain dilini kodda görünür kılar.

Son bir not: Kurallar veri tabanı sorgularında da kullanılacaksa `Func<T, bool>` yerine `Expression<Func<T, bool>>` tabanlı bir varyasyon düşünün. Böylece aynı kural hem bellek içinde çalışabilir hem de ORM tarafından SQL’e çevrilebilir. Kısacası Specification Pattern, koşulları yok etmez; onları isim, sınır ve karakter sahibi küçük bileşenlere dönüştürür.
