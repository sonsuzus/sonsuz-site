---
layout: post
title: "Telegram Webhook ve Queue Mimarisiyle Saniyede Binlerce Mesajı Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - telegram
  - webhook
  - queue
  - ölçeklenebilirlik
  - nodejs
  - redis
  - bot
toc: true
image: /img/telegram-webhook-ve-44.png
---

Bir Telegram botu küçükken polling gayet masum görünür: “Yeni mesaj var mı?” diye düzenli aralıklarla Telegram’a sorarsınız. Bot büyüdüğünde ise bu yaklaşım, kapıyı saniyede yüzlerce kez çalıp postacı geldi mi diye kontrol etmeye benzer. Webhook mimarisinde roller değişir; bir olay oluştuğunda Telegram güncellemeyi doğrudan sunucunuza gönderir. Arkasına eklenen kuyruk ise ani trafik darbelerini emerek sistemin nefes almasını sağlar.

``

## Polling ve webhook arasındaki temel fark

Polling modelinde uygulama `getUpdates` metodunu tekrar tekrar çağırır. İsteklerin önemli bir bölümü boş dönebilir. Webhook modelindeyse Telegram, tanımladığınız HTTPS adresine yalnızca yeni bir güncelleme bulunduğunda POST isteği yollar.

| Özellik | Polling | Webhook |
|---|---|---|
| Trafik modeli | Sürekli sorgulama | Olay oluşunca bildirim |
| Gecikme | Sorgu aralığına bağlı | Genellikle çok düşük |
| Kaynak tüketimi | Boş istekler üretir | Gerçek olaylara odaklanır |
| Ölçeklendirme | Uzun polling bağlantıları zorlaştırabilir | Yatay ölçeklemeye uygundur |
| Kurulum | Daha kolay | HTTPS ve erişilebilir adres gerekir |

Ortalama olay geliş hızı saniyede $\lambda$, sistemin işleme kapasitesi ise $\mu$ olsun. Kararlı çalışma için temel beklenti şudur:

$$\lambda < \mu$$

Ancak kampanya duyurusu gibi anlarda kısa süreliğine $\lambda > \mu$ olabilir. Kuyruk tam burada devreye girer: mesajları kaybetmek yerine bekletir. Yaklaşık kuyruk büyümesi, darbe süresi $t$ için şöyle düşünülebilir:

$$Q \approx (\lambda - \mu)t$$

Örneğin saniyede 5.000 güncelleme gelirken worker’lar 3.000 güncelleme işliyorsa 10 saniyelik dalgada yaklaşık 20.000 iş kuyrukta birikir.

## Hızlı kabul et, sonra işle

Webhook endpoint’inin görevi mesajı bütünüyle işlemek değildir. Güncellemeyi doğrulamalı, kuyruğa bırakmalı ve Telegram’a mümkün olduğunca hızlı `200 OK` dönmelidir. Veritabanı sorguları, yapay zekâ çağrıları veya dosya indirme işlemleri endpoint içinde yapılırsa zaman aşımı ve tekrar teslim riski artar.

```js
import Fastify from 'fastify';
import { Queue } from 'bullmq';

const app = Fastify();
const updates = new Queue('telegram-updates', {
  connection: { host: 'redis', port: 6379 }
});

app.post('/telegram/webhook', async (request, reply) => {
  const secret = request.headers['x-telegram-bot-api-secret-token'];

  if (secret !== process.env.WEBHOOK_SECRET) {
    return reply.code(401).send({ ok: false });
  }

  const update = request.body;

  await updates.add('process-update', update, {
    jobId: String(update.update_id),
    attempts: 5,
    backoff: { type: 'exponential', delay: 1000 }
  });

  return reply.code(200).send({ ok: true });
});

app.listen({ port: 3000, host: '0.0.0.0' });
```

Bu örnek, Telegram’ın secret token başlığını doğrular ve güncellemeyi BullMQ üzerinden Redis’e yazar. `update_id` değerinin iş kimliği yapılması aynı güncellemenin iki kez kuyruğa eklenmesini önlemeye yardımcı olur. Üstel geri çekilme ise geçici hatalarda sistemi yumruklamak yerine bekleyerek yeniden dener.

## Worker filosu ve darbe emilimi

Kuyruktaki işleri bağımsız worker süreçleri tüketir. Trafik yükseldiğinde worker sayısı artırılabilir; düştüğünde azaltılabilir.

| Bileşen | Sorumluluk |
|---|---|
| Load balancer | Webhook trafiğini dağıtmak |
| Webhook servisi | Doğrulamak, kuyruğa yazmak, hızlı yanıtlamak |
| Redis/RabbitMQ/Kafka | Trafik darbelerini tamponlamak |
| Worker | Komutları ve iş kurallarını çalıştırmak |
| Veritabanı | Kalıcı durum ve idempotency kaydı tutmak |

Worker sayısı $n$, tek worker kapasitesi $r$ ise toplam teorik kapasite yaklaşık $\mu = n \times r$ olur. Gerçekte veritabanı bağlantıları ve Telegram gönderim limitleri bu değeri aşağı çeker. Bu nedenle otomatik ölçekleme yalnızca CPU’ya değil, kuyruk uzunluğu ve en eski işin bekleme süresine de bakmalıdır.

Son olarak sistem “en az bir kez teslim” ihtimaline göre tasarlanmalıdır. İşlemler idempotent olmalı, başarısız işler dead-letter kuyruğuna taşınmalı, metrikler izlenmeli ve kullanıcıya mesaj gönderirken Telegram’ın `429` yanıtındaki bekleme süresine uyulmalıdır. Böylece webhook kapıyı hızla açar, kuyruk kalabalığı düzenler, worker’lar da binlerce mesajı paniğe kapılmadan işler.

![telegram-webhook-ve-44](/img/telegram-webhook-ve-44.svg)

