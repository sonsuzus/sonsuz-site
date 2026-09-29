---
layout: post
title: "Event-Driven Architecture: Servisler Dans mı Etsin, Şefi mi İzlesin?"
math: true
categories: 
  - Bilgi
tags: 
  - event-driven architecture
  - eda
  - mikroservisler
  - koreografi
  - orkestrasyon
  - dağıtık sistemler
toc: true
image: /img/event-driven-architecture-44.png
---

![event-driven-architecture-44](/img/event-driven-architecture-44.svg)


Bir e-ticaret siparişi düşünün: ödeme alınacak, stok düşülecek, kargo hazırlanacak ve müşteriye bildirim gönderilecek. Bu servisler aynı sahneyi paylaşır; fakat hareketlerini kim belirlemelidir? Event-Driven Architecture dünyasında cevap genellikle iki yaklaşım arasında salınır: Her servisin olayları dinleyerek bağımsız hareket ettiği **koreografi** veya süreci merkezi bir bileşenin yönettiği **orkestrasyon**.

``

## EDA’nın temel mantığı

Event-Driven Architecture (EDA), sistemde meydana gelen anlamlı durum değişikliklerini **olay** olarak yayımlar. `OrderCreated`, geçmişte gerçekleşmiş ve artık değiştirilemeyecek bir gerçeği temsil eder. Bu yönüyle olay, “Siparişi oluştur” biçimindeki bir komuttan farklıdır.

Bir olayın basitleştirilmiş modeli şöyle gösterilebilir:

$$E = (id, type, timestamp, payload, metadata)$$

Burada `id` olayın kimliği, `type` olay türü, `payload` iş verisi ve `metadata` izleme bilgileridir. Üretici olayın Kafka, RabbitMQ veya benzeri bir aracı üzerinden kim tarafından tüketileceğini bilmez. Böylece servisler arasındaki bağımlılık azalır.

Bu gevşek bağlılığın bedeli ise **nihai tutarlılıktır**. Bir olayın tüm tüketiciler tarafından işlenmesi zaman alabileceğinden, sistemin tutarlı hâle gelmesi kabaca şöyle düşünülebilir:

$$T_{tutarlılık} \approx \max(T_1, T_2, \ldots, T_n) + T_{iletişim}$$

Yani dağıtık sistemlerde “hemen şimdi” yerine çoğu zaman “birazdan tutarlı” yaklaşımı vardır.

## Koreografi: Her servis kendi figürünü bilir

Koreografide merkezi yönetici bulunmaz. Sipariş servisi `OrderCreated` olayını yayımlar; ödeme servisi bunu dinleyip ödemeyi alır ve `PaymentCompleted` yayımlar. Stok servisi de bu yeni olaya tepki verir. Dansçılar birbirlerine bakarak sıradaki hareketi çıkarır.

```javascript
// Ödeme servisi, sipariş olayına bağımsız biçimde tepki verir.
eventBus.on('OrderCreated', async event => {
  const payment = await charge(event.customerId, event.total);

  await eventBus.publish('PaymentCompleted', {
    orderId: event.orderId,
    paymentId: payment.id
  });
});
```

Bu model küçük ve doğal olay akışlarında son derece esnektir. Yeni bir bildirim servisi eklemek için sipariş servisini değiştirmek gerekmez. Ancak süreç büyüdükçe olay zincirini zihinde takip etmek, görünmez domino taşlarını izlemeye dönüşebilir.

## Orkestrasyon: Baton merkezi şefte

Orkestrasyonda bir **orchestrator**, sürecin hangi adımlarla ilerleyeceğine karar verir. Servisler kendi işlerini yapar fakat sıradaki adımı merkezi süreç yöneticisi belirler.

```javascript
// Orchestrator, iş akışını ve telafi adımlarını görünür kılar.
async function processOrder(order) {
  const payment = await paymentService.charge(order);

  try {
    await inventoryService.reserve(order);
    await shippingService.createShipment(order);
  } catch (error) {
    await paymentService.refund(payment.id); // Telafi işlemi
    throw error;
  }
}
```

Bu yaklaşım özellikle **Saga** deseninde işe yarar. Dağıtık bir ACID transaction yerine her başarılı adımın gerektiğinde çalışacak bir telafi işlemi bulunur. Örneğin stok ayrılamazsa ödeme iade edilir.

| Ölçüt | Koreografi | Orkestrasyon |
|---|---|---|
| Kontrol | Servislere dağıtılmıştır | Merkezi yöneticidedir |
| Bağımlılık | Düşüktür | Orchestrator’a bağımlılık vardır |
| Akışı izleme | Süreç büyüdükçe zorlaşır | Akış tek yerde görülebilir |
| Değişiklik | Yerel değişiklikler kolaydır | Merkezi akış güncellenebilir |
| Hata telafisi | Dağınık olabilir | Açıkça modellenebilir |
| Tek hata noktası | Daha az belirgindir | Dayanıksız şef risk oluşturur |

## Hangisini seçmeliyiz?

Basit olay reaksiyonları, bağımsız ekipler ve sık genişleyen tüketici sayısı için koreografi güçlü bir seçimdir. Uzun süren, iş kuralları yoğun, adımları sıralı ve telafi gerektiren süreçlerde orkestrasyon daha anlaşılır olur.

Gerçek sistemler çoğunlukla hibrittir: Sipariş tamamlama Saga’sı orkestre edilirken analitik, e-posta ve denetim servisleri sonuç olaylarını koreografik biçimde dinleyebilir. Kritik nokta, her olayı merkezi şefe bağlamamak ve her iş akışını da kontrolsüz bir partiye çevirmemektir. İyi mimari, dansın ne zaman özgürleşeceğini ve orkestranın ne zaman batona bakacağını bilmektir.
