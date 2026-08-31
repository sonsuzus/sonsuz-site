---
layout: post
title: "Telegram Botlarında Rate Limiting: Kuyruklarla Güvenli Toplu Bildirim"
math: true
categories: 
  - Program
tags: 
  - telegram-bot
  - rate-limiting
  - kuyruk-sistemleri
toc: true
---

Telegram botunuz yüz kullanıcıya mesaj gönderirken gayet sakin çalışabilir; ancak kullanıcı sayısı binlere ulaştığında Bot API aniden `429 Too Many Requests` yanıtları vermeye başlayabilir. Çözüm, döngüye biraz `sleep` serpiştirmek değil; gönderim hızını ölçen, mesajları sıraya alan ve geçici hataları yeniden deneyen kontrollü bir dağıtım sistemi kurmaktır.

``

## Telegram neden hız sınırı uygular?

Rate limiting, Telegram altyapısının kötüye kullanımı ve aşırı yükü engellemek için belirli zaman aralıklarında kabul ettiği istek sayısını sınırlamasıdır. Pratikte bot başına genel gönderim limiti, aynı sohbet için uygulanan limit ve grup mesajlarına ilişkin ek kısıtlamalar birlikte değerlendirilmelidir.

Telegram’ın sınırları kullanım türüne ve güncel politikalara göre değişebildiğinden, internetteki rakamları kesin sözleşmeler gibi görmemek gerekir. Yaygın başlangıç varsayımı saniyede yaklaşık 30 genel mesajdır; üretimde 20–25 mesaj/saniye gibi güvenli bir değer seçmek ve API’nin `retry_after` bilgisini esas almak daha sağlıklıdır.

| Yaklaşım | Avantaj | Sorun |
|---|---|---|
| Herkese aynı anda gönderim | Uygulaması kolaydır | Ani trafik ve çok sayıda 429 üretir |
| Her mesajda sabit bekleme | Basittir | Gereksiz yavaş veya hâlâ riskli olabilir |
| Token Bucket ve kuyruk | Kontrollü, ölçeklenebilir | Biraz altyapı gerektirir |
| Dağıtık kuyruk | Birden fazla sunucuyu destekler | Redis/RabbitMQ operasyonu gerekir |

## Token Bucket mantığı

Token Bucket algoritmasında kovaya saniyede $r$ adet token eklenir ve kapasite $C$ ile sınırlandırılır. Her API isteği bir token tüketir. Geçen süre $\Delta t$ ise yeni token miktarı şöyle hesaplanır:

$$T_{yeni} = \min(C, T_{eski} + r \cdot \Delta t)$$

Token yoksa tahmini bekleme süresi:

$$t_{bekleme} = \frac{1-T}{r}$$

Kapasite değeri kısa süreli patlamalara izin verirken, $r$ uzun dönem ortalama hızı belirler. Örneğin $r=25$ ve $C=5$, kısa bir başlangıç hızlanmasına izin verir fakat sürekli gönderimi saniyede 25 mesaj civarında tutar.

## Python ile kuyruklu gönderim

Aşağıdaki örnek, `aiogram` ile mesajları bir öncelik kuyruğuna koyar. Telegram bekleme süresi bildirirse mesaj silinmez; gelecekte tekrar işlenmek üzere kuyruğa eklenir.

```python
import asyncio
import itertools
import time
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError

bot = Bot(token="BOT_TOKEN")
queue = asyncio.PriorityQueue()
sequence = itertools.count()

class TokenBucket:
    def __init__(self, rate=25, capacity=5):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.updated_at = time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self):
        while True:
            async with self.lock:
                now = time.monotonic()
                elapsed = now - self.updated_at
                self.tokens = min(
                    self.capacity,
                    self.tokens + elapsed * self.rate
                )
                self.updated_at = now

                if self.tokens >= 1:
                    self.tokens -= 1
                    return

                delay = (1 - self.tokens) / self.rate
            await asyncio.sleep(delay)

limiter = TokenBucket()

async def enqueue(chat_id, text, delay=0):
    available_at = time.monotonic() + delay
    await queue.put((available_at, next(sequence), chat_id, text))

async def worker():
    while True:
        available_at, _, chat_id, text = await queue.get()
        try:
            await asyncio.sleep(max(0, available_at - time.monotonic()))
            await limiter.acquire()
            await bot.send_message(chat_id, text)
        except TelegramRetryAfter as error:
            await enqueue(chat_id, text, error.retry_after + 1)
        except TelegramForbiddenError:
            print(f"Bot engellenmiş: {chat_id}")
        finally:
            queue.task_done()
```

Birden fazla worker başlatılabilir; fakat hepsinin aynı limiter nesnesini kullanması önemlidir. Aksi durumda beş worker’ın her biri 25 mesaj/saniye göndererek toplam sınırı kolayca aşar.

## Üretim ortamında dikkat edilmesi gerekenler

Bellek içi `asyncio.Queue`, süreç yeniden başladığında görevleri kaybeder. Kritik bildirimlerde Redis Streams, RabbitMQ, SQS veya Kafka gibi kalıcı sistemler kullanılmalıdır. Her görev için benzersiz kimlik tutmak da aynı mesajın iki kez gönderilmesini önleyen idempotency kontrolünü mümkün kılar.

Ayrıca kullanıcı botu engellediyse ilgili kimliği pasif duruma getirin; kalıcı hataları sonsuza kadar yeniden denemeyin. Başarı oranı, kuyruk uzunluğu, 429 sayısı, ortalama bekleme süresi ve gönderim gecikmesi gibi metrikleri izleyin. Böylece toplu bildirim sistemi, Telegram’ın kapısını yumruklayan sabırsız bir ziyaretçi değil, sırasını bilen düzenli bir misafir gibi çalışır.
