---
layout: post
title: "CQRS Tasarım Deseni: Okuma ve Yazmayı Ayırarak Ölçeklenebilir Sistemler"
math: true
categories: 
  - Bilgi
tags: 
  - cqrs
  - yazılım mimarisi
  - mikroservisler
---

Modern uygulamalarda her isteği aynı veri modeliyle karşılamak başlangıçta pratiktir; ancak kullanıcı sayısı, raporlama ihtiyacı ve işlem yoğunluğu arttıkça bu yaklaşım zorlanır. CQRS (Command Query Responsibility Segregation), yani Komut ve Sorgu Sorumluluklarının Ayrılması, veriyi değiştiren işlemlerle veriyi okuyan işlemleri bilinçli biçimde ayırır. Böylece sistem, “sipariş oluştur” ile “son 30 günün sipariş raporunu göster” gibi tamamen farklı ihtiyaçlara kendi kurallarıyla hizmet eder.
``
CQRS’nin temel teorisi oldukça nettir: Bir metodun ya **komut** ya da **sorgu** olması beklenir. Komutlar sistemin durumunu değiştirir; sipariş oluşturmak, ödeme almak veya kullanıcı profilini güncellemek bunlara örnektir. Sorgular ise yan etkisiz olmalıdır; yalnızca bilgi döndürürler. Bu ayrım, Bertrand Meyer’in *Command-Query Separation* ilkesinden beslenir: Bir işlem hem sonuç döndürüp hem de görünür bir durum değişikliği yapıyorsa, davranışını anlamak zorlaşır.

| Özellik | Command (Komut) | Query (Sorgu) |
|---|---|---|
| Amaç | Sistemin durumunu değiştirmek | Sistemin durumunu okumak |
| Yan etki | Vardır | Olmamalıdır |
| Dönüş değeri | Genellikle kimlik, durum veya boş sonuç | Görüntülenecek veri |
| Örnek | `CreateOrder` | `GetOrderSummary` |
| Ölçekleme | Yazma tutarlılığına göre | Okuma trafiğine göre |

Geleneksel CRUD yaklaşımında tek bir `Order` modeli hem yazma doğrulamalarını hem de ekranların okuma ihtiyaçlarını taşır. Ancak yönetim paneli; müşteri adı, toplam tutar, teslimat durumu ve ürün sayısını tek çağrıda isterken, yazma tarafı stok, indirim ve ödeme kurallarını titizlikle uygular. CQRS’de bu iki dünyanın veri şekli farklı olabilir. Yazma modeli alan kuralları açısından zengin, okuma modeli ise ekran için optimize edilmiş ve düz bir DTO olabilir.

Örneğin bir sipariş komutunu ele alalım. Komut işleyicisi önce iş kurallarını kontrol eder, ardından veriyi kalıcı hâle getirir:

```csharp
public sealed record CreateOrderCommand(Guid CustomerId, List<Guid> ProductIds);

public sealed class CreateOrderHandler
{
    private readonly IOrderRepository _repository;

    public async Task<Guid> Handle(CreateOrderCommand command)
    {
        if (command.ProductIds.Count == 0)
            throw new InvalidOperationException("Sipariş boş olamaz.");

        var order = Order.Create(command.CustomerId, command.ProductIds);
        await _repository.AddAsync(order);
        return order.Id;
    }
}
```

Bu kodun görevi ekran için veri hazırlamak değil, siparişin geçerli olup olmadığını garanti etmektir. Okuma tarafı ise daha hafif bir projeksiyon kullanabilir:

```csharp
public sealed record OrderSummary(Guid Id, string Customer, decimal Total, string Status);

public async Task<OrderSummary?> GetOrderSummary(Guid id)
{
    return await _readDb.Orders
        .Where(x => x.Id == id)
        .Select(x => new OrderSummary(x.Id, x.CustomerName, x.TotalAmount, x.Status))
        .FirstOrDefaultAsync();
}
```

CQRS’nin güçlü yanı bağımsız ölçeklemedir. Okuma isteği sayısı $R$, yazma isteği sayısı $W$ olsun. Çoğu iş uygulamasında $R \gg W$ olur. Tek veritabanı ve tek modelde kapasite planlaması yaklaşık olarak $C \geq R + W$ ihtiyacına göre yapılırken, CQRS ile okuma ve yazma kaynakları ayrı planlanabilir. Örneğin okuma tarafına önbellek, arama motoru veya read-replica eklemek; yazma tarafında ise tutarlı ilişkisel veritabanını korumak mümkündür.

Bununla birlikte CQRS her projeye serpilmesi gereken mimari maydanoz değildir. Ayrı modeller, senkronizasyon, hata takibi ve operasyonel maliyet getirir. Özellikle Event Sourcing ile birlikte kullanıldığında okuma modeli olaylardan asenkron güncellenebilir. Bu durumda kullanıcı kısa süreliğine eski veri görebilir; buna **eventual consistency** denir. Matematiksel olarak okuma modelinin gecikmesi $\Delta t > 0$ ise, yazma tamamlandıktan hemen sonra yapılan sorgu yeni durumu göstermeyebilir.

| Ne zaman tercih edilmeli? | Ne zaman kaçınılmalı? |
|---|---|
| Okuma ve yazma yükleri çok farklıysa | Basit CRUD ekranları varsa |
| Karmaşık iş kuralları bulunuyorsa | Küçük ekip operasyon yükünü taşıyamıyorsa |
| Raporlama ve arama yoğun ise | Anlık güçlü tutarlılık her ekranda şartsa |

Başlamak için iki ayrı sınıf, ayrı DTO’lar ve net komut/sorgu sınırları yeterlidir; hemen iki veritabanı kurmak gerekmez. Sistem büyüdükçe mesaj kuyruğu, projeksiyonlar ve bağımsız okuma depoları eklenebilir. CQRS’nin asıl kazancı teknoloji değil, zihinsel netliktir: Veriyi değiştiren kod ile veriyi sunan kod birbirinin işini yapmayı bırakır.
