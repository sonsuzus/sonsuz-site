---
layout: post
title: "Mikroservislerde Veri Tutarlılığı: Eventual Consistency ile Dans Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - mikroservis
  - eventual consistency
  - dağıtık sistemler
image: /img/mikroservislerde-veri-tutarliligi-25.png
---

![mikroservislerde-veri-tutarliligi-25](/img/mikroservislerde-veri-tutarliligi-25.svg)


Mikroservis mimarisi, uygulamayı bağımsız geliştirilebilen küçük servislere böler; fakat bu özgürlüğün bir bedeli vardır: veri artık tek bir veritabanında, tek bir atomik işlemle yönetilmez. Sipariş, ödeme ve stok servislerinin kendi veritabanlarına sahip olduğunu düşünün. Bir sipariş verildiğinde tüm kayıtların aynı milisaniyede güncellenmesini beklemek hem pahalı hem de çoğu zaman gereksizdir. İşte **eventual consistency** (nihai tutarlılık), dağıtık dünyanın bu gerçeğini yönetmek için devreye girer.
``

Klasik bir monolitik sistemde ACID işlemleri yaygındır: işlem ya tamamen başarılı olur ya da geri alınır. Mikroservislerde ise ağ gecikmesi, servis kesintisi ve bağımsız veritabanları nedeniyle küresel bir veritabanı kilidi kullanmak sistemi kırılganlaştırır. CAP teoremi bunu özetler: Ağ bölünmesi olasılığı bulunan dağıtık bir sistemde aynı anda hem güçlü tutarlılık hem de kesintisiz erişilebilirlik garanti edilemez.

Basit bir bakışla sistemin tutarlılık durumu şöyle ifade edilebilir:

$$\lim_{t \to \infty} S_1(t) = \lim_{t \to \infty} S_2(t) = \dots = V$$

Burada $S_i(t)$, farklı servislerdeki verinin zamana bağlı durumunu; $V$ ise sistem sakinleştiğinde ulaşılması beklenen ortak değeri temsil eder. “Eventually” kelimesi kritik bir ayrıntı taşır: Bu yakınsamanın süresi garanti edilen sabit bir sayı değildir.

| Özellik | Güçlü Tutarlılık | Eventual Consistency |
|---|---|---|
| Okuma sonucu | Her an en güncel veri | Kısa süre eski veri dönebilir |
| Erişilebilirlik | Ağ sorunlarında azalabilir | Genellikle daha yüksektir |
| Ölçeklenebilirlik | Koordinasyon maliyetlidir | Bağımsız ölçeklenmeye uygundur |
| Uygun örnek | Banka bakiyesi transferi | Ürün kataloğu, bildirimler |

Bu modelin en yaygın uygulaması olay güdümlü mimaridir. Örneğin Sipariş Servisi önce kendi veritabanına siparişi `PENDING` durumunda yazar, ardından `OrderCreated` olayı yayınlar. Stok Servisi bu olayı tüketir, rezervasyon yapar ve sonucu yeni bir olayla bildirir. Ödeme başarısız olursa Sipariş Servisi, süreci telafi eden bir işlem başlatır. Bu akışın adı genellikle **Saga** desenidir.

Ancak burada meşhur “veritabanına yazdım ama mesaj yayınlanamadı” problemi ortaya çıkar. Çözüm olarak **Transactional Outbox** kullanılır. İş kaydı ve yayınlanacak olay aynı yerel veritabanı işlemi içinde saklanır; ayrı bir yayıncı süreç outbox tablosunu mesaj aracısına güvenle taşır.

```sql
BEGIN;

INSERT INTO orders (id, customer_id, status)
VALUES ('ord-42', 'cus-9', 'PENDING');

INSERT INTO outbox_events (event_type, payload, published)
VALUES (
  'OrderCreated',
  '{"orderId":"ord-42","items":["sku-7"]}',
  false
);

COMMIT;
```

Bu SQL bloğu sipariş ile olayı birlikte kalıcılaştırır. Arka plandaki worker, `published = false` kayıtlarını Kafka ya da RabbitMQ gibi bir aracıya gönderir. Böylece servis çökse bile olay kaybolmaz.

Mesajlaşma altyapıları çoğunlukla **en az bir kez teslimat** sunar. Dolayısıyla tüketici aynı olayı iki kez alabilir. Bunun ilacı idempotency, yani aynı komut tekrar uygulandığında sonucun değişmemesidir. Tüketici, olay kimliğini işlenmiş olaylar tablosunda saklayabilir veya benzersiz anahtarlarla tekrarları etkisiz kılabilir.

| Sorun | Dayanıklı yaklaşım |
|---|---|
| Çift mesaj teslimi | İdempotent tüketici ve olay kimliği |
| Geç gelen olay | Sürüm numarası veya zaman damgası |
| Kısmi başarısızlık | Saga telafi adımları |
| Olayın kaybolması | Transactional Outbox |

Son olarak kullanıcı deneyimini unutmayın. “Siparişiniz hazırlanıyor” gibi ara durumlar göstermek, nihai tutarlılığı kullanıcı için anlaşılır hale getirir. Eventual consistency bir hata toleransı değil; doğru sınırlar, gözlemlenebilirlik, tekrar deneme politikaları ve telafi işlemleriyle tasarlanması gereken bilinçli bir mimari tercihtir.
