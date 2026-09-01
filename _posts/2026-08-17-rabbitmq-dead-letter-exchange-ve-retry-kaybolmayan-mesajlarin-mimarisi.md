---
layout: post
title: "RabbitMQ Dead Letter Exchange ve Retry: Kaybolmayan Mesajların Mimarisi"
math: true
categories: 
  - Bilgi
tags: 
  - rabbitmq
  - dead letter exchange
  - retry
  - mesaj kuyrukları
toc: true
image: /img/rabbitmq-dead-letter-26.png
---

Dağıtık sistemlerde bir mesajın tüketiciye ulaşması, başarıyla işlendiği anlamına gelmez. Veritabanı geçici olarak kapalı olabilir, üçüncü taraf API'si hata verebilir ya da mesajın verisi gerçekten bozuk olabilir. RabbitMQ'nun **Dead Letter Exchange (DLX)** ve gecikmeli yeniden deneme kurgusu, bu durumlarda mesajları kaybetmeden kontrollü biçimde yönetmeyi sağlar. Amaç, aynı hatalı mesajı sonsuza kadar ana kuyruğu kilitleyecek şekilde tüketmek değil; geçici hatalara zaman tanımak, kalıcı hataları ise görünür ve incelenebilir hale getirmektir.
``

## Temel fikir: Başarısızlık da bir mesaj akışıdır

RabbitMQ'da tüketici bir mesajı işleyemediğinde genellikle `basic.nack` veya `basic.reject` gönderir. Mesaj `requeue=true` ile geri kuyruğa bırakılırsa hemen tekrar tüketilebilir. Bu ilk bakışta pratik görünür; fakat hata kalıcıysa aynı mesaj saniyede yüzlerce kez dönerek **hot loop** oluşturur. CPU yükselir, loglar dolar ve sağlıklı mesajlar arka sıraya itilir.

DLX yaklaşımında başarısız mesaj, ana kuyruktan başka bir exchange'e yönlendirilir. Bu yönlendirme; mesajın reddedilmesi, süresinin dolması (`TTL`) veya kuyruk uzunluğu sınırının aşılması gibi olaylarda çalışabilir. RabbitMQ ayrıca mesajın geçtiği ölü mektup yollarını `x-death` başlığında saklar. Böylece bir mesajın kaç kez ve hangi kuyruklarda başarısız olduğunu izlemek mümkündür.

Bir retry döngüsünün teorik akışı şöyledir:

$$\text{Ana Kuyruk} \rightarrow \text{Consumer} \rightarrow \text{Retry Kuyruğu} \xrightarrow{TTL} \text{Ana Kuyruk}$$

Deneme sayısı $n$ ve sabit bekleme süresi $d$ ise toplam bekleme yaklaşık olarak $T=n \times d$ olur. Daha nazik bir yaklaşım olan üstel geri çekilmede ise gecikme:

$$d_n = \min(d_0 \times 2^n, d_{max})$$

şeklinde artırılabilir. Bu sayede geçici arızalarda servise tekrar tekrar yük bindirmek yerine sistemin toparlanmasına fırsat verilir.

| Yaklaşım | Avantajı | Riski | Uygun senaryo |
|---|---|---|---|
| `requeue=true` | Çok basit | Sonsuz hızlı döngü | Çok kısa süreli ağ kesintisi |
| Retry + TTL + DLX | Kontrollü bekleme | Daha fazla kuyruk yönetimi | Geçici servis hataları |
| Final DLQ | Hatalı veriyi korur | Manuel müdahale gerektirir | Şema ve iş kuralı hataları |

![rabbitmq-dead-letter-26](/img/rabbitmq-dead-letter-26.svg)


## Önerilen topoloji

Pratikte üç katman yeterlidir: `orders.main`, `orders.retry.30s` ve `orders.dlq`. Ana kuyruk başarısız mesajları retry exchange'ine yollar. Retry kuyruğu 30 saniyelik TTL tutar; süre dolunca DLX üzerinden tekrar ana exchange'e döner. Belirlenen deneme sınırı aşıldığında tüketici mesajı artık retry'a göndermek yerine final DLQ'ya yayınlar.

Aşağıdaki Python örneği, `pika` ile kuyruk argümanlarının temelini gösterir:

```python
import pika

channel = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
).channel()

channel.exchange_declare("orders", "direct", durable=True)
channel.exchange_declare("orders.retry", "direct", durable=True)

channel.queue_declare(
    "orders.main",
    durable=True,
    arguments={
        "x-dead-letter-exchange": "orders.retry",
        "x-dead-letter-routing-key": "retry.30s"
    }
)

channel.queue_declare(
    "orders.retry.30s",
    durable=True,
    arguments={
        "x-message-ttl": 30000,
        "x-dead-letter-exchange": "orders",
        "x-dead-letter-routing-key": "order.created"
    }
)

channel.queue_bind("orders.main", "orders", "order.created")
channel.queue_bind("orders.retry.30s", "orders.retry", "retry.30s")
```

Buradaki kritik nokta, TTL'nin mesajı silmemesi; TTL dolunca mesajın yeniden ana exchange'e dead-letter edilmesidir. Tüketici tarafında `x-death` başlığını okuyarak deneme sayısını hesaplamak mümkündür. Örneğin sınır $3$ ise dördüncü başarısızlıkta mesajı `orders.dlq` kuyruğuna yönlendirmek güvenli bir politikadır.

## Operasyonel kurallar

DLQ bir çöp kutusu değildir; bir gözlem alanıdır. Kuyruk derinliği, en eski mesaj yaşı ve hata türleri için alarm kurun. Mesaj işleyicilerini mümkün olduğunca **idempotent** tasarlayın: aynı sipariş mesajı iki kez gelirse iki kez tahsilat yapılmamalıdır. Son olarak, yalnızca geçici hataları yeniden deneyin. JSON ayrıştırma hatası veya eksik zorunlu alan gibi deterministik problemler doğrudan DLQ'ya gitmelidir. Böylece RabbitMQ akışınız hem dayanıklı hem de teşhis edilebilir kalır.
