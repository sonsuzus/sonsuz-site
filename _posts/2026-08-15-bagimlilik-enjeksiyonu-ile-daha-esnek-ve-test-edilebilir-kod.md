---
layout: post
title: "Bağımlılık Enjeksiyonu ile Daha Esnek ve Test Edilebilir Kod"
math: true
categories: 
  - Bilgi
tags: 
  - dependency ınjection
  - yazılım mimarisi
  - birim testi
---

Bir sınıfın çalışmak için ihtiyaç duyduğu nesneleri kendi içinde üretmesi, ilk bakışta pratik görünür: `new` yazılır ve iş biter. Ancak uygulama büyüdükçe bu küçük kolaylık; değiştirmesi zor, testleri pahalı ve bileşenleri birbirine yapışmış bir mimariye dönüşür. Bağımlılık Enjeksiyonu (Dependency Injection, DI), sınıfın ihtiyaç duyduğu bağımlılıkları oluşturmak yerine dışarıdan almasını sağlayarak bu yapışkanlığı azaltan güçlü bir tasarım tekniğidir.

``

## Sorun: Sınıfın Her Şeyi Kendisinin Yapması

Bir `OrderService` sınıfının sipariş kaydetmek için doğrudan `SqlOrderRepository` oluşturduğunu düşünelim. Servis artık yalnızca sipariş kurallarından değil, hangi veritabanı altyapısının kullanılacağından da sorumludur. Üstelik test sırasında gerçek SQL bağlantısı kurmak zorunda kalabilirsiniz. Bu, **sıkı bağımlılık** olarak adlandırılır.

```csharp
public class OrderService
{
    private readonly SqlOrderRepository repository;

    public OrderService()
    {
        repository = new SqlOrderRepository();
    }

    public void Create(Order order)
    {
        repository.Save(order);
    }
}
```

Buradaki asıl problem `OrderService` sınıfının somut bir sınıfa bağımlı olmasıdır. Kod, “siparişlerin saklanması gerekir” fikrine değil, “siparişler SQL ile saklanmalıdır” ayrıntısına bağlanmıştır.

| Yaklaşım | Bağımlılık türü | Test kolaylığı | Değişime direnç |
|---|---|---:|---:|
| Sınıf içinde `new` kullanmak | Somut sınıfa | Düşük | Düşük |
| DI ile arayüz almak | Soyutlamaya | Yüksek | Yüksek |

## Çözüm: Bağımlılığı Dışarıdan Vermek

DI yaklaşımında servis, ihtiyaç duyduğu depolama mekanizmasını bir arayüz üzerinden ister. Bu bağımlılık yapıcı metoda (constructor) gönderilir. Böylece servis, verinin SQL'de mi, bellekte mi, yoksa bir web servisinde mi tutulduğunu bilmek zorunda değildir.

```csharp
public interface IOrderRepository
{
    void Save(Order order);
}

public class OrderService
{
    private readonly IOrderRepository repository;

    public OrderService(IOrderRepository repository)
    {
        this.repository = repository;
    }

    public void Create(Order order)
    {
        if (order.Total <= 0)
            throw new ArgumentException("Sipariş tutarı pozitif olmalıdır.");

        repository.Save(order);
    }
}
```

Bu örnekte `OrderService`, yalnızca `IOrderRepository` sözleşmesini bilir. Matematiksel olarak bağımlılık ağını yönlü bir grafik gibi düşünürsek, sıkı yapıda $Service \rightarrow ConcreteRepository$ ilişkisi vardır. DI sonrasında ilişki $Service \rightarrow Interface$ olur; somut uygulamanın seçimi ise uygulamanın kurulum katmanına taşınır. Böylece yüksek seviyeli iş kuralları, düşük seviyeli altyapı detaylarından ayrılır.

## Testlerde Kazanılan Hız

DI'ın en sevilen tarafı, sahte bağımlılıkların kolayca verilebilmesidir. Testte gerçek veritabanı yerine bellekte çalışan küçük bir depo kullanabiliriz:

```csharp
public class FakeOrderRepository : IOrderRepository
{
    public List<Order> SavedOrders { get; } = new();

    public void Save(Order order)
    {
        SavedOrders.Add(order);
    }
}

// Test senaryosu
var fakeRepository = new FakeOrderRepository();
var service = new OrderService(fakeRepository);
service.Create(new Order { Total = 250 });

Assert.Single(fakeRepository.SavedOrders);
```

Bu test, ağ bağlantısı, SQL sunucusu veya karmaşık başlangıç verisi gerektirmez. Test süresini kabaca $T = T_{kurulum} + T_{çalışma}$ şeklinde ele alırsak, dış kaynakları kaldırmak özellikle $T_{kurulum}$ değerini dramatik biçimde düşürür.

## Enjeksiyon Yöntemleri ve Denge

| Yöntem | Kullanım alanı | Not |
|---|---|---|
| Constructor injection | Zorunlu bağımlılıklar | En güvenli ve yaygın yöntemdir. |
| Setter/property injection | İsteğe bağlı bağımlılıklar | Nesne eksik yapılandırılabilir. |
| Method injection | Tek seferlik ihtiyaçlar | Bağımlılık yalnızca ilgili çağrıda kullanılır. |

Constructor injection genellikle varsayılan seçim olmalıdır; nesne oluşturulduğu anda geçerli ve kullanılabilir kalır. .NET gibi platformlarda DI container'ları, `IOrderRepository` için hangi somut sınıfın üretileceğini merkezi olarak kaydeder. Yine de her sınıfa arayüz eklemek bir erdem yarışması değildir. Değişme ihtimali olmayan küçük değer nesneleri için doğrudan kullanım makul olabilir. Ama veritabanı, e-posta, saat, dosya sistemi ve harici API gibi sınır bağımlılıklarında DI, kodunuzun emniyet kemeridir.
