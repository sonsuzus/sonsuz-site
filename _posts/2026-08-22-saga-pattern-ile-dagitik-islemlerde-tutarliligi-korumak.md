---
layout: post
title: "Saga Pattern ile Dağıtık İşlemlerde Tutarlılığı Korumak"
math: true
categories: 
  - Bilgi
tags: 
  - saga pattern
  - mikroservisler
  - dağıtık sistemler
---

Mikroservis mimarisinde tek bir kullanıcı işlemi; ödeme, stok, sipariş ve kargo gibi bağımsız servisleri aynı anda etkileyebilir. Tek veritabanlı sistemlerde alıştığımız `BEGIN` ve `COMMIT` yaklaşımı burada yetersiz kalır: Her servis kendi verisini yönetir, ağ gecikebilir ve bir servis geçici olarak erişilemez olabilir. Saga Pattern, bu karmaşayı dağıtık bir işlemi küçük yerel adımlara bölerek ve hata durumunda telafi işlemleri çalıştırarak yönetir.
``

Saga, klasik anlamda atomik bir işlem değildir. Bunun yerine **nihai tutarlılık** (eventual consistency) hedefler. Her adım kendi servisinin veritabanında başarıyla tamamlanır; sonraki adım başarısız olursa önceki adımlar geri alınmaz, onları mantıksal olarak dengeleyen telafi adımları uygulanır. Örneğin ödeme iadesi, kayıt satırını silmek yerine yeni bir iade kaydı oluşturan iş kuralıdır.

Bir sipariş akışını düşünelim:

1. Sipariş servisi siparişi oluşturur.
2. Stok servisi ürünleri rezerve eder.
3. Ödeme servisi tahsilatı gerçekleştirir.
4. Kargo servisi gönderi kaydı açar.

Kargo adımı başarısız olursa saga ters yönde ilerleyebilir: ödeme iade edilir, stok rezervasyonu kaldırılır ve sipariş `CANCELLED` durumuna çekilir. Başarı olasılığını kabaca $p_i$ ile gösterirsek, bağımsız adımlar için tüm akışın ilk denemedeki başarı olasılığı $P=\prod_{i=1}^{n}p_i$ olur. Adım sayısı arttıkça hata ve telafi tasarımı daha kritik hâle gelir.

| Yaklaşım | Koordinasyon | Güçlü yanı | Önemli risk |
|---|---|---|---|
| ACID dağıtık işlem | Merkezi, sıkı kilitler | Anlık tutarlılık | Gecikme ve düşük erişilebilirlik |
| Saga - Choreography | Servisler olaylarla haberleşir | Gevşek bağlılık | Akışı takip etmek zorlaşır |
| Saga - Orchestration | Orkestratör adımları yönetir | Görünür ve denetlenebilir akış | Orkestratörün aşırı büyümesi |

**Choreography** modelinde servisler olay yayınlar. `OrderCreated` olayını gören stok servisi rezervasyon yapar ve `StockReserved` yayınlar. Bu model doğal ve dağıtık görünür; fakat servis sayısı büyüdükçe “bu olayı kim dinliyor?” sorusu mimari dedektifliğe dönüşebilir. **Orchestration** modelinde ise bir saga orkestratörü, hangi komutun ne zaman gönderileceğini açıkça belirler. İş kuralları tek yerde okunabildiği için sipariş, rezervasyon ve ödeme gibi kritik akışlarda sık tercih edilir.

Aşağıdaki yalın TypeScript örneği, orkestratörün telafi mantığını gösterir:

```ts
async function createOrderSaga(input: OrderInput) {
  const order = await orderService.create(input);

  try {
    const reservation = await inventory.reserve(order.items);
    const payment = await payment.charge(order.customerId, order.total);
    await shipping.createShipment(order.id, order.address);

    return orderService.confirm(order.id, payment.id);
  } catch (error) {
    // Telafi adımları, tamamlanan adımlar için güvenli olmalıdır.
    await payment.refundIfCharged(order.id);
    await inventory.releaseIfReserved(order.id);
    await orderService.cancel(order.id, String(error));
    throw error;
  }
}
```

Bu kodun kritik ayrıntısı `refundIfCharged` ve `releaseIfReserved` adlarıdır: Telafi işlemleri **idempotent** olmalıdır. Aynı mesaj iki kez geldiyse sonuç değişmemeli, yani matematiksel olarak $f(f(x))=f(x)$ davranışı beklenmelidir. Mesaj kuyrukları çoğunlukla “en az bir kez teslim” garantisi verdiğinden bu özellik lüks değil, zorunluluktur.

| Tasarım ihtiyacı | Pratik çözüm |
|---|---|
| Yinelenen mesajlar | Idempotency key ve işlenmiş olay tablosu |
| Veritabanı + olay tutarlılığı | Transactional Outbox deseni |
| Geçici ağ hataları | Üstel geri çekilme ile retry |
| Uzun süren adımlar | Timeout, durum makinesi ve telafi |
| İzlenebilirlik | Correlation ID, dağıtık tracing ve audit log |

Son olarak, Saga Pattern her işlemi saga yapma çağrısı değildir. Tek servis içinde kalabilen veriler için yerel ACID işlemi daha basit ve daha güvenlidir. Saga; gerçekten birden fazla bağımsız veri sahibi, uzun süren süreçler ve hata toleransı gerektiğinde parlar. Başarılı bir tasarımın sırrı da “geri alma”yı teknik silme işlemi gibi değil, iş dünyasında anlamlı bir **telafi eylemi** olarak modellemektir.
