---
layout: post
title: "RabbitMQ ile Mesaj Kuyruğu Mimarisi: Üretici-Tüketici Modeli"
math: true
categories: 
  - Proje
tags: 
  - rabbitmq
  - mesaj kuyruğu
  - node.js
---

Mikroservisler birbirini doğrudan ve senkron çağırdığında, küçük bir gecikme bile zincirleme arızaya dönüşebilir. RabbitMQ bu bağı gevşetir: sipariş servisi işi bir kuyruğa bırakır, bildirim servisi uygun olduğunda alır. Böylece servisler farklı hızlarda çalışabilir, yoğunluk dalgaları daha yönetilebilir hâle gelir.
``

Bu yaklaşımın temelinde **üretici-tüketici** modeli bulunur. Üretici (*producer*) mesajı doğrudan tüketiciye göndermez; bir **exchange** üzerinden yönlendirir. Exchange, mesajı routing key ve binding kurallarına göre bir veya daha fazla kuyruğa dağıtır. Tüketici (*consumer*) ise kuyruğu dinler, mesajı işler ve başarılı olduğunda onay (*acknowledgement*) verir.

Basit bir kapasite hesabı mimari kararları netleştirir. Üretim hızı $\lambda$, tek tüketicinin işleme hızı $\mu$ olsun. Sistem kararlı kalmak için genel olarak $\lambda < n\mu$ koşulu gerekir; burada $n$ tüketici sayısıdır. Bu koşul sağlanmazsa kuyruk uzunluğu büyür, gecikme artar. RabbitMQ sorunu sihirli biçimde yok etmez; işi tamponlar ve ölçekleme için zaman kazandırır.

| Kavram | Görevi | Pratik örnek |
|---|---|---|
| Producer | Mesaj üretir | Sipariş oluşturma servisi |
| Exchange | Mesajı yönlendirir | `orders` topic exchange'i |
| Queue | Mesajı saklar | `email.notifications` |
| Consumer | Mesajı işler | E-posta gönderici worker |
| Ack | Başarılı işlemi bildirir | Mesajın güvenle silinmesi |

Örnekte Node.js ve `amqplib` kullanacağız. Önce bağımlılığı yükleyin: `npm install amqplib`. Ardından RabbitMQ'yu Docker ile ayağa kaldırabilirsiniz: `docker run -d --hostname rabbit --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management`. Yönetim arayüzü `http://localhost:15672` adresindedir.

Üretici, dayanıklı bir exchange ve kuyruk tanımlar; sonra sipariş olayını JSON olarak yayınlar:

```js
// producer.js
const amqp = require('amqplib');

async function publishOrder() {
  const connection = await amqp.connect('amqp://localhost');
  const channel = await connection.createChannel();
  await channel.assertExchange('orders', 'topic', { durable: true });
  await channel.assertQueue('email.notifications', { durable: true });
  await channel.bindQueue('email.notifications', 'orders', 'order.created');

  const order = { id: 'ORD-42', email: 'ada@example.com', total: 799 };
  channel.publish('orders', 'order.created', Buffer.from(JSON.stringify(order)), {
    persistent: true
  });
  console.log('Sipariş olayı yayınlandı');
  await channel.close();
  await connection.close();
}
publishOrder().catch(console.error);
```

`durable: true`, broker yeniden başlasa bile exchange ve kuyruğun tanımını korur. `persistent: true` ise mesajın diske yazılması isteğini belirtir. Yine de kritik senaryolarda yayın onayı (*publisher confirm*) ve tekrar deneme stratejisi eklemek gerekir.

Tüketicide `prefetch(1)` kullanmak, bir worker'ın bitirmeden çok sayıda mesaj almasını engeller. İşleme başarısız olursa `nack` ile mesajı yeniden kuyruğa koyabiliriz:

```js
// consumer.js
const amqp = require('amqplib');

async function consume() {
  const connection = await amqp.connect('amqp://localhost');
  const channel = await connection.createChannel();
  await channel.assertQueue('email.notifications', { durable: true });
  channel.prefetch(1);

  channel.consume('email.notifications', async (msg) => {
    if (!msg) return;
    try {
      const order = JSON.parse(msg.content.toString());
      console.log(`E-posta hazırlanıyor: ${order.email}`);
      // await sendEmail(order);
      channel.ack(msg);
    } catch (error) {
      console.error(error.message);
      channel.nack(msg, false, true);
    }
  });
}
consume().catch(console.error);
```

| Teslimat tercihi | Davranış | Dikkat edilmesi gereken |
|---|---|---|
| Auto-ack | Mesaj anında silinir | Worker çökerse veri kaybı |
| Manual ack | İş bitince silinir | Kodda `ack` unutulmamalı |
| Requeue | Hata sonrası yeniden dener | Sonsuz hata döngüsü riski |

Gerçek sistemlerde tüketiciyi **idempotent** tasarlayın: aynı `order.id` iki kez gelirse ikinci e-posta gönderilmemeli. Zehirli mesajlar için sınırlı retry ve dead-letter queue kullanın. Böylece RabbitMQ, yalnızca mesaj taşıyan bir araç değil; hata toleranslı, ölçülebilir asenkron mimarinin güvenilir omurgası olur.
