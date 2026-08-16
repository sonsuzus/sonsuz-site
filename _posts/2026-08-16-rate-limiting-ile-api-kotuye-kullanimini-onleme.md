---
layout: post
title: "Rate Limiting ile API Kötüye Kullanımını Önleme"
math: true
categories: 
  - Bilgi
tags: 
  - API Güvenliği
  - Rate Limiting
  - Node.js
  - Sistem Tasarımı
---

Bir API, internetin açık kapısı gibidir: doğru kullanıcılar için hızlı ve kullanışlı olmalı, fakat kapıyı saniyede binlerce kez çalan botlara da dayanmalıdır. Rate limiting (istek hız sınırlama), bir istemcinin belirli zaman aralığında yapabileceği istek sayısını kısıtlayarak servis kesintilerini, kaba kuvvet saldırılarını ve maliyet patlamalarını azaltır. Ancak tek başına “429 Too Many Requests” döndürmek sihirli bir kalkan değildir; doğru algoritma, doğru anahtar ve iyi gözlemlenebilirlik gerekir.
``

Temel problem kapasiteyle ilgilidir. Servisiniz saniyede $\mu$ istek işleyebilsin; gelen ortalama trafik ise $\lambda$ olsun. Eğer uzun süre boyunca $\lambda > \mu$ ise kuyruk büyür, gecikme artar ve en sonunda zaman aşımı zinciri oluşur. Basit bir kuyruk modelinde sistemin kullanım oranı $\rho = \lambda / \mu$ olarak ifade edilir. $\rho$ değeri 1’e yaklaştıkça, teorik olarak bekleme süresi doğrusal değil, çok daha sert biçimde yükselir. Bu yüzden sınırlandırma, yalnızca saldırı savunması değil, normal kullanıcı deneyimini koruma aracıdır.

## Kimi sınırlamalıyız?

En yaygın anahtar IP adresidir; fakat ortak Wi-Fi, NAT ve vekil sunucular nedeniyle masum kullanıcıları aynı sepete koyabilir. Kimliği doğrulanmış API’lerde kullanıcı veya API anahtarı daha iyi bir seçimdir. Hassas uç noktalarda ise anahtarları birleştirmek mantıklıdır: `kullanıcı + IP + endpoint`.

| Anahtar | Avantajı | Riski | Uygun senaryo |
|---|---|---|---|
| IP adresi | Kimlik doğrulama gerekmez | NAT altında yanlış engelleme | Genel, anonim uç noktalar |
| API anahtarı | Müşteri bazlı kota | Anahtar sızıntısı | B2B API’ler |
| Kullanıcı kimliği | Adil kullanım takibi | Anonim trafiği kapsamaz | Giriş yapılmış uygulamalar |
| Endpoint | Kritik işlemi korur | Yönetimi karmaşıklaştırır | Giriş, ödeme, parola sıfırlama |

## Algoritmalar: sayaçtan kovaya

**Fixed window**, örneğin her dakika 100 istek sayar. Ucuzdur ama pencere sınırında kullanıcı 12:00:59’da 100, 12:01:00’da bir 100 istek daha gönderebilir. **Sliding window**, yakın geçmişi daha hassas hesaplar; adildir fakat depolama ve hesaplama maliyeti yüksektir.

Pratikte en sevilen yaklaşımlardan biri **token bucket** modelidir. Kovaya sabit hızla jeton eklenir; her istek bir jeton tüketir. Kova doluysa kısa süreli patlamalara izin verir, boşsa istek reddedilir. Yeniden dolum yaklaşık olarak şöyle düşünülebilir:

$$T(t) = \min(B, T_0 + r \cdot \Delta t)$$

Burada $B$ kova kapasitesi, $r$ saniye başına jeton sayısı, $T_0$ mevcut jeton ve $\Delta t$ geçen süredir. Örneğin $B=20$ ve $r=5$ ise istemci anlık 20 istek atabilir, ardından sürdürülebilir hızı saniyede 5 istektir.

| Algoritma | Patlama toleransı | Adalet | Uygulama zorluğu |
|---|---:|---:|---:|
| Fixed window | Yüksek, kontrolsüz | Orta | Düşük |
| Sliding window | Düşük | Yüksek | Orta-Yüksek |
| Token bucket | Kontrollü | Yüksek | Orta |
| Leaky bucket | Çok düşük | Yüksek | Orta |

## Dağıtık sistemde Redis neden önemlidir?

Uygulamanız birden fazla sunucuda çalışıyorsa süreç içi sayaçlar güvenilir değildir: saldırgan istekleri farklı pod’lara dağıtabilir. Redis gibi merkezi ve hızlı bir veri deposu, sayacı tüm örnekler arasında ortaklaştırır. Kritik nokta atomikliktir; “say, artır, süre ata” işlemleri yarış koşuluna karşı tek adımda yapılmalıdır.

Aşağıdaki Express örneği, Redis tabanlı bir dakika penceresi uygular. Gerçek projede API anahtarıyla birlikte güvenilir proxy yapılandırmasını da değerlendirin.

```js
import express from "express";
import Redis from "ioredis";

const app = express();
const redis = new Redis(process.env.REDIS_URL);
const LIMIT = 60;
const WINDOW_SECONDS = 60;

app.use(async (req, res, next) => {
  const clientId = req.get("X-API-Key") || req.ip;
  const key = `rate:${clientId}:${Math.floor(Date.now() / 60000)}`;
  const count = await redis.incr(key);

  if (count === 1) await redis.expire(key, WINDOW_SECONDS);
  res.set("X-RateLimit-Limit", String(LIMIT));
  res.set("X-RateLimit-Remaining", String(Math.max(0, LIMIT - count)));

  if (count > LIMIT) {
    res.set("Retry-After", "60");
    return res.status(429).json({ error: "Çok fazla istek" });
  }
  next();
});
```

Bu örnek öğreticidir; `INCR` ve `EXPIRE` arasındaki nadir hata durumları için Lua betiği veya hazır bir limiter kütüphanesi tercih edilebilir. Ayrıca 429 yanıtlarını, limit aşımlarını, IP/API anahtarı dağılımını ve gecikmeyi izleyin. Son olarak katmanlı savunma kurun: CDN/WAF ile volumetrik trafiği kenarda süzün, uygulamada endpoint kotası uygulayın, pahalı işlemler için kuyruk kullanın. Böylece botlar duvara çarparken gerçek kullanıcılar kapıdan rahatça geçer.
