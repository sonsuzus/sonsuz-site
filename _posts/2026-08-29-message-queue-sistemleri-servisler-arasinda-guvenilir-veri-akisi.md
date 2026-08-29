---
layout: post
title: "Message Queue Sistemleri: Servisler Arasında Güvenilir Veri Akışı"
math: true
categories: 
  - Bilgi
tags: 
  - message queue
  - mikroservis
  - rabbitmq
---

Modern uygulamalarda servislerin birbirini doğrudan ve anında çağırması ilk bakışta pratik görünür. Ancak trafik arttığında, bir servis bakımdayken veya anlık hata yaşadığında bu sıkı bağlantı zincirleme sorunlara dönüşür. Message Queue (mesaj kuyruğu) sistemleri, servisler arasına dayanıklı bir posta merkezi koyarak veriyi zamandan bağımsız ve güvenli biçimde taşır.

``

Temel fikir basittir: **producer** bir mesaj üretir, mesajı kuyruk ya da topic'e gönderir; **consumer** ise uygun olduğunda bu mesajı işler. Producer'ın consumer'ın ayakta olup olmadığını bilmesine gerek kalmaz. Böylece sistemdeki zamansal bağımlılık azalır. Örneğin sipariş servisi, ödeme tamamlandığında e-posta servisini doğrudan çağırmak yerine `order.paid` olayını yayınlayabilir.

Bu yaklaşımın teorik temeli, **asenkron iletişim** ve **gevşek bağlılık** kavramlarıdır. Doğrudan HTTP iletişiminde gecikme yaklaşık olarak çağrı zincirindeki sürelerin toplamıdır:

$$T_{toplam} = T_{sipariş} + T_{ödeme} + T_{bildirim}$$

Kuyruklu mimaride sipariş servisi mesajı teslim ettikten sonra kendi işini bitirebilir. Bildirim işlemi daha sonra gerçekleşir. Kullanıcının gördüğü kritik yanıt süresi ise kabaca $T_{sipariş} + T_{mesaj\_yayınlama}$ seviyesine iner.

| Özellik | Senkron HTTP Çağrısı | Message Queue |
|---|---|---|
| Bağımlılık | Servisler aynı anda çalışmalı | Consumer daha sonra çalışabilir |
| Hata etkisi | Hata çağrı zincirini kesebilir | Mesaj yeniden denenebilir |
| Ölçekleme | Her çağrı anlık kapasite ister | Consumer sayısı artırılabilir |
| Uygun kullanım | Anlık sorgular | Olaylar ve uzun süren işler |

Güvenilirlik denildiğinde üç teslim garantisi öne çıkar. **At-most-once** mesajı en fazla bir kez işler; hızlıdır ama kayıp riski taşır. **At-least-once** mesajın kaybolmamasını hedefler, fakat aynı mesaj tekrar gelebilir. **Exactly-once** ise ideal görünse de dağıtık sistemlerde maliyetli ve karmaşıktır. Pratikte en yaygın reçete, at-least-once teslimat ile **idempotent consumer** tasarlamaktır. Yani aynı mesaj iki kez işlense bile sonuç değişmemelidir.

| Teslim Modeli | Mesaj Kaybı | Tekrar İşleme | Tipik Strateji |
|---|---:|---:|---|
| At-most-once | Mümkün | Beklenmez | Telemetri, önemsiz loglar |
| At-least-once | Çok düşük | Mümkün | Sipariş, ödeme olayları |
| Exactly-once | Hedeflenir | Hedeflenmez | Yüksek maliyetli özel senaryolar |

Aşağıdaki Python örneği, RabbitMQ ile kalıcı bir sipariş mesajı yayınlar. `delivery_mode=2`, broker yeniden başlasa bile mesajın kalıcı olmasına yardımcı olur; gerçek dayanıklılık için kuyruk da durable tanımlanmalıdır.

```python
import json
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()
channel.queue_declare(queue="orders", durable=True)

order = {"eventId": "evt-42", "orderId": 901, "total": 349.90}
channel.basic_publish(
    exchange="",
    routing_key="orders",
    body=json.dumps(order),
    properties=pika.BasicProperties(delivery_mode=2)
)
connection.close()
```

Consumer tarafında mesaj işlendikten **sonra** onay (`ack`) vermek kritik bir ayrıntıdır. İşlem sırasında uygulama çökerse broker, onaylanmamış mesajı tekrar dağıtabilir. Bu nedenle consumer, `eventId` gibi benzersiz bir kimliği veritabanında takip ederek yinelenen olayları atlamalıdır. Başarısız mesajlar için sınırsız tekrar denemek yerine **retry queue**, artan bekleme süresi ve **dead-letter queue (DLQ)** kullanılmalıdır. DLQ, zehirli mesajları ana akışı durdurmadan incelemeye alır.

RabbitMQ genellikle görev kuyrukları ve karmaşık yönlendirme için; Kafka ise yüksek hacimli olay akışları, kayıtların tekrar okunması ve analitik senaryoları için tercih edilir. Araç seçimi moda göre değil; sıralama ihtiyacı, mesaj hacmi, saklama süresi ve tüketici modeline göre yapılmalıdır. Doğru tasarlanmış bir kuyruk, servislerin arasındaki trafiği yalnızca taşımakla kalmaz; sistemin zor günlerde de sakin kalmasını sağlar.
