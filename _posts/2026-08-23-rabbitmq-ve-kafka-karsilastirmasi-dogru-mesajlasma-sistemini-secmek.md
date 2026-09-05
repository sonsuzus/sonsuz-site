---
layout: post
title: "RabbitMQ ve Kafka Karşılaştırması: Doğru Mesajlaşma Sistemini Seçmek"
math: true
categories: 
  - Bilgi
tags: 
  - rabbitmq
  - apache kafka
  - mesaj kuyruğu
toc: true
image: /img/rabbitmq-ve-kafka-20.png
---

Dağıtık sistemlerde servislerin birbirini beklemeden iletişim kurması, hem performans hem de dayanıklılık için kritik önemdedir. RabbitMQ ve Apache Kafka bu ihtiyacı karşılayan iki güçlü araçtır; ancak aynı problemi farklı felsefelerle çözerler. Biri görev dağıtan hızlı bir postacı, diğeri ise olayların değişmez tarihçesini tutan dev bir günlük gibi düşünülebilir.

``

## Temel zihniyet farkı

RabbitMQ, klasik **mesaj aracısıdır** (message broker). Bir üretici mesajı bir exchange'e yollar, exchange kurallara göre mesajı uygun kuyruklara dağıtır ve tüketici mesajı işler. Mesaj başarıyla onaylandığında genellikle kuyruktan silinir. Bu yapı, bir işi doğru çalışan servise ulaştırmak için idealdir.

Kafka ise dağıtık bir **olay akışı platformudur**. Mesajlar topic içindeki partition'lara sıralı kayıtlar olarak eklenir. Tüketiciler mesajı silmek yerine kendi okuma konumlarını, yani offset'lerini takip eder. Aynı olay geçmişi, farklı tüketici grupları tarafından tekrar tekrar okunabilir. Bu nedenle Kafka'da asıl değer yalnızca mesajın iletilmesi değil, olayın saklanmasıdır.

Basitçe, RabbitMQ'da soru genellikle “Bu işi kim yapacak?” iken Kafka'da “Bu olay gerçekleşti; kimler bundan haberdar olmak ister?” şeklindedir.

| Özellik | RabbitMQ | Apache Kafka |
|---|---|---|
| Ana model | Kuyruk ve yönlendirme | Dağıtık, eklemeli log |
| Mesaj ömrü | Onay sonrası silinebilir | Retention süresince saklanır |
| Tüketim | Mesaj tüketiciye dağıtılır | Her grup kendi offset'iyle okur |
| Güçlü olduğu alan | İş kuyrukları, komutlar | Event streaming, analitik |
| Sıralama | Kuyruk bazında | Partition bazında |

## Teslimat garantileri ve sıralama

Her iki sistemde de “mesaj kaybolmasın” hedefi, yapılandırmaya bağlıdır. RabbitMQ'da kalıcı kuyruk, persistent mesaj ve publisher confirm birlikte düşünülmelidir. Tüketici, işlem tamamlanmadan `ack` göndermemelidir. Aksi durumda ağ kopması veya servis çökmesi mesajın yeniden teslim edilmesine yol açabilir.

Kafka'da dayanıklılık replication factor ve producer acknowledgment ayarlarıyla ilişkilidir. Örneğin `acks=all`, liderin yanı sıra senkron replikaların da kaydı doğrulamasını ister. Bir topic'in teorik yazma kapasitesi kabaca partition sayısıyla büyür:

$$Throughput_{toplam} \approx P \times Throughput_{partition}$$

Buradaki bedel şudur: Aynı partition içindeki sıralama korunurken, partition'lar arasında küresel sıralama garantisi yoktur. Sipariş olaylarını `orderId` anahtarıyla göndermek, aynı siparişe ait olayların aynı partition'a düşmesini sağlar.

## Hangi senaryoda hangisi?

RabbitMQ; e-posta gönderme, PDF oluşturma, ödeme sonrası fatura kesme veya arka plan işçilerine görev dağıtma gibi durumlarda çok rahattır. Exchange türleri sayesinde esnek routing sunar: `direct` tam eşleşme, `topic` desen eşleşmesi, `fanout` ise herkese yayın için kullanılır.

Kafka; kullanıcı tıklamaları, sipariş olayları, IoT telemetrisi, log toplama, gerçek zamanlı analiz ve veri göllerini besleme gibi yüksek hacimli akışlarda öne çıkar. Aynı `OrderCreated` olayı hem stok servisi, hem bildirim sistemi, hem analitik ekip tarafından bağımsız biçimde okunabilir. Yeni bir tüketici eklemek, geçmiş retention süresi içindeki veriyi yeniden oynatabilmesi açısından özellikle değerlidir.

| Senaryo | Daha uygun seçim | Gerekçe |
|---|---|---|
| Görsel işleme görevi | RabbitMQ | İş dağıtımı ve ack modeli |
| Mikroservis komutu | RabbitMQ | Hedefli routing ve düşük gecikme |
| Tıklama akışı analizi | Kafka | Yüksek hacim ve tekrar okuma |
| Denetim kaydı | Kafka | Kalıcı olay geçmişi |
| Gecikmeli görev | RabbitMQ | TTL ve dead-letter mekanizmaları |

## Küçük bir Kafka üretici örneği

Aşağıdaki Python kodu, sipariş olayını anahtar ile Kafka'ya yollar. Anahtar, aynı siparişin olay sırasını korumaya yardımcı olur.

```python
from confluent_kafka import Producer
import json

producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "acks": "all"
})

event = {"orderId": "A-42", "status": "CREATED"}
producer.produce(
    "orders",
    key=event["orderId"],
    value=json.dumps(event)
)
producer.flush()
```

Son karar “hangisi daha iyi?” değildir. Komutları güvenilir biçimde dağıtmak istiyorsanız RabbitMQ, olayları uzun süre saklayıp birçok sistemin kullanmasını istiyorsanız Kafka seçin. Hatta olgun mimarilerde ikisini birlikte kullanmak da son derece mantıklıdır.

![rabbitmq-ve-kafka-20](/img/rabbitmq-ve-kafka-20.svg)

