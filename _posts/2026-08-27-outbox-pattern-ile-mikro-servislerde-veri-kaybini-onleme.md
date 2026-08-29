---
layout: post
title: "Outbox Pattern ile Mikro Servislerde Veri Kaybını Önleme"
math: true
categories: 
  - Bilgi
tags: 
  - mikro servisler
  - outbox pattern
  - mesajlaşma
  - veri tutarlılığı
toc: true
---

Mikro servis mimarisinde bir siparişi veritabanına kaydedip ardından `OrderCreated` olayını mesaj kuyruğuna göndermek basit görünür. Fakat veritabanı işlemi başarılı olurken broker bağlantısı koparsa ne olur? Sipariş vardır, olay yoktur ve stok, ödeme ya da bildirim servisleri bu siparişi hiç öğrenemez. Outbox Pattern, bu can sıkıcı “yarım kalmış başarı” durumunu güvenilir ve izlenebilir bir akışa dönüştürür.
``

## Temel problem: çift yazma çıkmazı

Bir uygulama iki farklı sisteme yazıyorsa—örneğin PostgreSQL ve Kafka—tek bir iş adımı aslında iki ayrı dayanıklılık alanına bölünür. Uygulama şu iki işlemi sırayla yapar:

1. İş verisini veritabanına kaydeder.
2. Entegrasyon olayını mesaj aracısına yayınlar.

Bu işlemler arasında oluşan hata, tutarsızlık üretir. Kabaca başarı olasılığı şöyle düşünülebilir:

$$P(başarı) = P(DB\ yazma) \times P(Broker\ yayınlama)$$

Her iki sistem de %99,9 güvenilir olsa bile birleşik başarı oranı yaklaşık $0.999 \times 0.999 = 0.998001$ olur. Yoğun sistemlerde küçük görünen bu fark, zamanla kayıp olaylara dönüşür.

| Yaklaşım | Güçlü yanı | Kritik riski |
|---|---|---|
| Önce DB, sonra mesaj | İş verisi korunur | Mesaj kaybolabilir |
| Önce mesaj, sonra DB | Olay erken yayılır | Hayalet olay oluşabilir |
| Dağıtık transaction (2PC) | Teorik atomiklik | Karmaşıklık, gecikme, sınırlı destek |
| Outbox Pattern | Yerel transaction ile dayanıklılık | Tekrarları yönetmek gerekir |

## Outbox Pattern nasıl çalışır?

Desen, iş kaydıyla birlikte aynı veritabanında bir **outbox** tablosuna olay kaydı ekler. İki ekleme aynı yerel transaction içinde gerçekleştiği için ya ikisi de kalıcı olur ya da ikisi de geri alınır. Ardından ayrı bir yayınlayıcı süreç, henüz gönderilmemiş outbox kayıtlarını okuyup broker’a iletir.

Örnek bir şema aşağıdaki gibi olabilir:

```sql
CREATE TABLE outbox_events (
  id UUID PRIMARY KEY,
  aggregate_type VARCHAR(100) NOT NULL,
  aggregate_id UUID NOT NULL,
  event_type VARCHAR(150) NOT NULL,
  payload JSONB NOT NULL,
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  published_at TIMESTAMPTZ NULL,
  retry_count INT NOT NULL DEFAULT 0
);
```

Sipariş oluşturma kodunda önemli nokta, iki yazmanın **aynı transaction** sınırında olmasıdır:

```python
with db.transaction():
    order = create_order(customer_id, items)
    db.insert("orders", order)

    event = {
        "id": uuid4(),
        "type": "OrderCreated",
        "aggregate_id": order.id,
        "payload": {"orderId": str(order.id), "total": order.total}
    }
    db.insert("outbox_events", event)
```

Arka plandaki worker, `published_at IS NULL` kayıtlarını seçer, Kafka veya RabbitMQ’ya yollar ve başarılı gönderimden sonra kaydı işaretler. Worker çökerse olay silinmediği için sonraki çalışmada yeniden denenir. İşte dayanıklılık sihri burada saklıdır.

## En az bir kez teslim ve idempotency

Outbox, çoğunlukla **at-least-once delivery** sağlar: aynı olay birden fazla kez gönderilebilir. Örneğin broker mesajı kabul eder, ancak yayınlayıcı başarı yanıtını almadan çöker. Worker yeniden başladığında mesajı tekrar yollar. Bu hata değil, tasarımın doğal sonucudur.

Bu nedenle tüketiciler idempotent olmalıdır; yani aynı olayı iki kez işleseler bile sonuç değişmemelidir. Yaygın çözüm, işlenen olay kimliklerini saklamaktır:

```sql
INSERT INTO processed_events(event_id, processed_at)
VALUES (:event_id, NOW())
ON CONFLICT (event_id) DO NOTHING;
```

Ekleme başarılıysa olay işlenir; çakışma varsa tüketici daha önce çalışmıştır ve güvenle atlanır.

## Uygulama seçenekleri ve pratik notlar

Outbox tablosu periyodik sorgulamayla (polling) okunabilir veya Change Data Capture araçlarıyla izlenebilir. Debezium gibi araçlar veritabanı transaction logunu takip ederek daha düşük gecikme sunar.

| Seçenek | Ne zaman tercih edilir? |
|---|---|
| Polling publisher | Küçük ekipler, hızlı başlangıç, basit altyapı |
| CDC + Debezium | Yüksek hacim, düşük gecikme, operasyonel olgunluk |
| Broker transaction | Broker merkezli özel senaryolar |

Son olarak outbox kayıtlarını sonsuza dek tutmayın: yayınlanan olayları belirli bir saklama süresinden sonra arşivleyin veya temizleyin. Sıralama gerekiyorsa aynı aggregate için sıralı işleme, kilitleme ya da partition anahtarı stratejisi belirleyin. Outbox Pattern sihirli değnek değildir; fakat veri kaybı riskini görünür, ölçülebilir ve yönetilebilir hale getiren en sağlam mikro servis tekniklerinden biridir.
