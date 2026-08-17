---
layout: post
title: "Saga Deseni ile Dağıtık İşlemler: Orchestration ve Choreography Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - Saga
  - Microservices
  - Distributed Transactions
---

Mikroservis mimarisinde bir siparişin oluşturulması, ödemenin alınması ve stok rezervasyonu tek bir veritabanı işlemi değildir; her servis kendi verisine sahiptir. Klasik ACID transaction yaklaşımını servisler arasında yaymak hem pahalı hem de kırılgandır. Saga deseni, büyük işlemi yerel işlemlere böler ve bir adım başarısız olduğunda önceki adımları geri almak için **telafi edici işlemler** (compensating transactions) çalıştırır. Böylece sistem, anlık tutarlılık yerine kontrollü bir **eventual consistency** modeli benimser.

``

Bir Saga'yı matematiksel olarak adımlar dizisi şeklinde düşünebiliriz. Başarılı yol şu olsun:

$$S = T_1 \rightarrow T_2 \rightarrow T_3$$

Burada $T_1$ sipariş oluşturma, $T_2$ stok ayırma ve $T_3$ ödeme alma olabilir. $T_3$ başarısız olursa geri dönüş zinciri ters sırada işletilir:

$$C = C_2 \rightarrow C_1$$

$C_2$ stok rezervasyonunu kaldırır, $C_1$ ise siparişi iptal eder. Önemli ayrıntı şudur: Telafi işlemi veriyi geçmişteki byte-byte durumuna döndürmek zorunda değildir; iş açısından eşdeğer sonucu üretmelidir. Örneğin ödeme iadesi, karttan hiç çekim yapılmamış olmasıyla aynı teknik durum değildir ama müşteri açısından doğru iş sonucudur.

## İki Saga yaklaşımı

| Özellik | Orchestration | Choreography |
|---|---|---|
| Akış kontrolü | Merkezi bir orchestrator yönetir | Servisler olaylara tepki verir |
| İletişim | Komut ve cevap ağırlıklı | Event broker üzerinden olay ağırlıklı |
| Görünürlük | Süreç tek noktadan izlenir | Akış servisler arasına dağılır |
| Bağımlılık riski | Orchestrator karmaşıklaşabilir | Event zinciri anlaşılması zorlaşabilir |
| Uygun senaryo | Karmaşık, çok adımlı iş akışları | Basit ve gevşek bağlı süreçler |

**Orchestration** modelinde `OrderSagaOrchestrator`, hangi servisin ne zaman çağrılacağını bilir. Başarısızlıkta hangi telafinin çalışacağını da o belirler. Bu yapı, ödeme, kargo, kupon ve faturalama gibi çok sayıda koşul içeren checkout süreçlerinde oldukça pratiktir.

```python
class OrderSaga:
    def create_order(self, order):
        order_id = self.order_service.create(order)

        try:
            self.inventory.reserve(order_id, order.items)
            self.payment.charge(order_id, order.total)
            self.shipping.create_shipment(order_id)
            return {"status": "COMPLETED", "orderId": order_id}
        except PaymentError:
            self.inventory.release(order_id)
            self.order_service.cancel(order_id)
            return {"status": "CANCELLED", "orderId": order_id}
```

Bu örnekte orchestrator, hata sınırını belirler. Gerçek sistemde çağrılar çoğunlukla asenkron yapılır; saga durumu `PENDING`, `STOCK_RESERVED`, `PAID` gibi bir state machine olarak kalıcı depolanır. Servis yeniden başlasa bile işlem nerede kaldığını bilir.

**Choreography** yaklaşımında merkezi yönetici yoktur. Order servisi `OrderCreated` olayı yayınlar. Inventory servisi bunu dinler, rezervasyon başarılıysa `StockReserved` yayınlar. Payment servisi ikinci olayı dinler. Bir hata meydana geldiğinde de `PaymentFailed` gibi bir olay, ilgili telafi davranışlarını tetikler.

```javascript
broker.on("StockReserved", async (event) => {
  try {
    await payment.charge(event.orderId, event.total);
    broker.publish("PaymentCompleted", event);
  } catch (error) {
    broker.publish("PaymentFailed", {
      orderId: event.orderId,
      reason: error.message
    });
  }
});

broker.on("PaymentFailed", async (event) => {
  await inventory.release(event.orderId);
  await orders.cancel(event.orderId);
});
```

Bu kodda servisler birbirini doğrudan çağırmaz; broker, Kafka veya RabbitMQ gibi bir altyapı olabilir. Ancak olayların kim tarafından tüketildiğini belgelemek kritiktir. Aksi halde küçük bir `OrderCancelled` olayı, beklenmedik servislerde zincirleme etki yaratabilir.

Her iki yaklaşımda da mesajlar en az bir kez teslim edilebilir. Bu nedenle tüketiciler **idempotent** olmalıdır: Aynı `PaymentCompleted` olayı iki kez gelirse ödeme iki kez işlenmemelidir. Yaygın çözüm, her mesaj için benzersiz `eventId` saklamak ve daha önce işlenmiş kimlikleri atlamaktır. Ayrıca Outbox deseni ile veritabanı değişikliği ve event yayını güvenli biçimde ilişkilendirilir.

Başlangıç için karmaşık sipariş akışlarında orchestration seçmek, gözlemlenebilirlik ve hata yönetimi açısından daha güvenlidir. Servisler arası etkileşimler olgunlaştığında, bağımsız ve kısa akışları choreography ile event tabanlı hale getirmek iyi bir evrim stratejisidir.
