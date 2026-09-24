---
layout: post
title: "CQRS: Okuma ve Yazma Modellerini Neden Ayırıyoruz?"
math: true
categories: 
  - Bilgi
tags: 
  - cqrs
  - yazılım mimarisi
  - domain driven design
  - eventual consistency
  - backend
  - ölçeklenebilirlik
toc: true
image: /img/cqrs-okuma-ve-67.png
---

Bir e-ticaret uygulamasında ürün satın almak ile ürün listesini görüntülemek aynı veri üzerinde çalışıyor gibi görünür. Ancak satın alma işlemi stok kontrolü, ödeme ve iş kuralları gerektirirken listeleme işlemi yalnızca hızlı ve zengin bir görünüm ister. CQRS, bu iki farklı ihtiyacı tek bir modelin omuzlarına yüklemek yerine okuma ve yazma taraflarını birbirinden ayırır.


![cqrs-okuma-ve-67](/img/cqrs-okuma-ve-67.svg)

``

## CQRS tam olarak nedir?

CQRS, **Command Query Responsibility Segregation**, yani Komut ve Sorgu Sorumluluklarının Ayrılması anlamına gelir. Temel fikir basittir:

- **Command**, sistemin durumunu değiştiren istektir: sipariş oluştur, adres güncelle, ürünü iptal et.
- **Query**, sistemin durumunu değiştirmeden veri okuyan istektir: siparişleri listele, ürün detayını getir.

Bu ayrım yalnızca `CreateOrder()` ve `GetOrders()` metotlarını farklı dosyalara koymak değildir. Gerçek CQRS yaklaşımında iki tarafın modelleri, servisleri ve gerekirse veri depoları farklı olabilir.

| Özellik | Yazma modeli | Okuma modeli |
|---|---|---|
| Ana hedef | Tutarlılık ve iş kuralları | Hızlı veri sunumu |
| Model yapısı | Davranış odaklı domain modeli | Ekrana uygun DTO veya görünüm |
| Veri biçimi | Normalize edilmiş olabilir | Denormalize edilebilir |
| Ölçekleme | Yazma trafiğine göre | Okuma trafiğine göre |
| Doğrulama | Yoğun iş kuralı kontrolü | Genellikle daha hafif |

## Tek model neden her zaman yeterli değildir?

Klasik CRUD yaklaşımında aynı model hem kaydedilir hem de kullanıcıya gösterilir. Küçük projelerde bu son derece mantıklıdır. Sistem büyüdüğünde ise okuma ekranları tablolar arasında çok sayıda `JOIN` isterken yazma tarafı güçlü tutarlılık kurallarına ihtiyaç duyar.

Bir sistemde saniyedeki okuma sayısı $R$, yazma sayısı $W$ olsun. Çoğu uygulamada:

$$R \gg W$$

Örneğin $R=10.000$ ve $W=200$ olabilir. Tek veritabanını iki iş yükü için aynı biçimde ölçeklemek, yalnızca okumalar yüzünden pahalı yazma altyapısı kurmak anlamına gelebilir. CQRS sayesinde okuma tarafına önbellek, arama motoru veya salt okunur replikalar eklenebilir.

## Basit bir uygulama örneği

Aşağıdaki C# örneğinde komut, sipariş oluşturma niyetini; sorgu ise arayüzün ihtiyaç duyduğu sonucu temsil eder:

```csharp
public record CreateOrderCommand(
    Guid CustomerId,
    IReadOnlyList<OrderItem> Items);

public record GetOrderSummaryQuery(Guid OrderId);

public sealed class CreateOrderHandler
{
    public async Task<Guid> Handle(CreateOrderCommand command)
    {
        var order = Order.Create(command.CustomerId, command.Items);
        await orderRepository.Save(order);
        await eventBus.Publish(new OrderCreated(order.Id));
        return order.Id;
    }
}
```

Burada `Order.Create` stok, müşteri ve toplam tutar gibi kuralları korur. Okuma tarafı ise aynı domain nesnesini yeniden kurmak zorunda değildir:

```csharp
public async Task<OrderSummaryDto?> Handle(GetOrderSummaryQuery query)
{
    return await readDatabase.OrderSummaries
        .SingleOrDefaultAsync(x => x.Id == query.OrderId);
}
```

`OrderSummaryDto`, ekranın istediği müşteri adı, toplam tutar ve durum bilgisini önceden birleştirilmiş şekilde taşıyabilir. Böylece sorgu hem sadeleşir hem hızlanır.

## Peki iki taraf nasıl senkron kalır?

Yazma tamamlandığında `OrderCreated` gibi bir olay yayımlanır. Bu olayı dinleyen süreç, okuma modelini günceller. Güncelleme anlık değilse sistem kısa süreliğine eski veri gösterebilir. Buna **eventual consistency**, yani nihai tutarlılık denir.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Aynı veritabanı | Yönetimi kolay | Modeller birbirine bağımlı kalabilir |
| Ayrı veritabanları | Bağımsız ölçekleme | Senkronizasyon karmaşıklığı |
| Mesaj kuyruğu | Dayanıklı olay aktarımı | Tekrar işleme ve sıralama sorunları |

Bu nedenle olay tüketicileri idempotent tasarlanmalıdır. Aynı olay iki kez işlendiğinde iki sipariş özeti üretmemelidir.

## CQRS her projede kullanılmalı mı?

Hayır. Basit yönetim panellerinde veya küçük CRUD servislerinde CQRS; ek sınıflar, mesaj altyapısı ve operasyonel yük getirerek gereksiz karmaşıklık yaratabilir. Okuma ve yazma ihtiyaçları belirgin biçimde farklıysa, yoğun trafik varsa ya da domain kuralları karmaşıksa güçlü bir seçenektir.

Kısacası CQRS, “iki veritabanı kullanalım” modası değildir. Amaç, farklı problemlere farklı modellerle yaklaşmaktır. Doğru yerde kullanıldığında performans, ölçeklenebilirlik ve kod okunabilirliği kazandırır; yanlış yerde kullanıldığında ise mimariyi küçük bir uzay programına çevirebilir.
