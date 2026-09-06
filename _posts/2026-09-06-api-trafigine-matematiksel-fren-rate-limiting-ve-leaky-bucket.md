---
layout: post
title: "API Trafiğine Matematiksel Fren: Rate Limiting ve Leaky Bucket"
math: true
categories: 
  - Bilgi
tags: 
  - rate-limiting
  - api-güvenliği
  - leaky-bucket
toc: true
---

Bir API herkese açık bir kapıysa rate limiting, kapıdaki soğukkanlı güvenlik görevlisidir. İstemciler saniyeler içinde binlerce istek gönderdiğinde CPU, bellek, ağ bağlantıları ve veritabanı havuzu tükenebilir. Hız sınırlama algoritmaları, normal kullanıcıları cezalandırmadan bu trafik selini matematiksel kurallarla kontrol altında tutar.
``
## Neden hız sınırına ihtiyaç duyarız?

Sunucunun saniyede işleyebildiği en yüksek istek sayısını $C$, gelen istek hızını ise $λ$ ile gösterelim. Sistem kararlı kalmak için uzun vadede şu koşula ihtiyaç duyar:

$$λ < C$$

Eğer $λ > C$ durumu uzun sürerse işlenemeyen istekler kuyrukta birikir. Yaklaşık kuyruk değişimi şöyle ifade edilebilir:

$$Q(t+Δt)=\max(0, Q(t)+(λ-C)Δt)$$

Kuyruk büyüdükçe yanıt süreleri artar, zaman aşımı yaşayan istemciler tekrar istek gönderir ve sistem bir **yeniden deneme fırtınasına** girebilir. Rate limiter, istekleri uygulamanın pahalı bölümlerine ulaşmadan önce reddederek veya geciktirerek bu döngüyü kırar.

## Leaky Bucket nasıl çalışır?

Leaky Bucket algoritmasını altı delik bir kova gibi düşünebiliriz. Gelen istekler kovaya düzensiz biçimde dolar; istekler kovadan sabit bir hızla çıkar. Kovanın kapasitesi $B$, mevcut doluluğu $q$, çıkış hızı da saniyede $r$ istek olsun.

$Δt$ saniye sonra kovada kalan miktar:

$$q'=\max(0,q-rΔt)$$

Yeni bir istek geldiğinde $q' < B$ ise istek kovaya eklenir. Kova doluysa istek reddedilir ve genellikle HTTP `429 Too Many Requests` yanıtı döndürülür. Böylece ani trafik patlamaları emilirken sunucuya ulaşan trafik daha düzenli olur.

| Algoritma | Ani trafik desteği | Bellek ihtiyacı | Temel özellik |
|---|---:|---:|---|
| Fixed Window | Orta | Çok düşük | Zaman aralığı başına sayaç tutar |
| Sliding Window | İyi | Orta/yüksek | Hareketli zaman aralığını izler |
| Token Bucket | Çok iyi | Düşük | Biriken jetonlar kadar patlamaya izin verir |
| Leaky Bucket | Sınırlı | Düşük | Trafiği sabit hızda dışarı aktarır |

Fixed Window basittir ancak iki pencerenin sınırında beklenenden fazla isteğe izin verebilir. Token Bucket kısa süreli patlamalar konusunda daha esnektir. Leaky Bucket ise öngörülebilir çıkış hızı gereken ödeme, raporlama veya mesaj işleme servislerinde özellikle kullanışlıdır.

## JavaScript ile basit uygulama

Aşağıdaki Express middleware’i her IP adresi için ayrı bir kova tutar. Örnek, isteği fiziksel bir kuyrukta bekletmek yerine kovanın hesaplanan doluluğuna göre kabul veya reddeder:

```js
const buckets = new Map();

function leakyBucket({ capacity, leakRate }) {
  return (req, res, next) => {
    const key = req.ip;
    const now = Date.now() / 1000;
    const bucket = buckets.get(key) ?? { level: 0, updatedAt: now };

    const elapsed = now - bucket.updatedAt;
    bucket.level = Math.max(0, bucket.level - elapsed * leakRate);
    bucket.updatedAt = now;

    if (bucket.level + 1 > capacity) {
      const wait = Math.ceil((bucket.level + 1 - capacity) / leakRate);
      res.set("Retry-After", String(wait));
      buckets.set(key, bucket);
      return res.status(429).json({ error: "Çok fazla istek" });
    }

    bucket.level += 1;
    buckets.set(key, bucket);
    next();
  };
}

app.use(leakyBucket({ capacity: 20, leakRate: 5 }));
```

Burada kova en fazla 20 birim taşır ve saniyede 5 birim boşalır. `Retry-After` başlığı, istemciye yeniden denemeden önce ne kadar beklemesi gerektiğini bildirir.

## Üretimde dikkat edilmesi gerekenler

Bellekte tutulan `Map`, tek sunuculu örnekler için yeterlidir; birden fazla uygulama örneğinde sayaçlar birbirinden habersiz kalır. Dağıtık sistemlerde Redis ve atomik Lua betikleri kullanılabilir. Anahtar olarak yalnızca IP seçmek de NAT arkasındaki kullanıcıları topluca cezalandırabilir. Kullanıcı kimliği, API anahtarı, endpoint ve abonelik paketi birlikte değerlendirilmelidir.

Son olarak rate limiting, kimlik doğrulamanın veya DDoS korumasının yerine geçmez. En iyi sonuç; ters proxy, önbellek, zaman aşımı, kuyruk ve gözlemlenebilirlik araçlarıyla birlikte kullanıldığında alınır. Ama doğru ayarlanmış küçük bir kova bile sunucunun boğulmasıyla sakin biçimde yüzmesi arasındaki fark olabilir.
