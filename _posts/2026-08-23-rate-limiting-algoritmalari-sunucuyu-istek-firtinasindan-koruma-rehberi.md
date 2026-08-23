---
layout: post
title: "Rate Limiting Algoritmaları: Sunucuyu İstek Fırtınasından Koruma Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - rate limiting
  - sistem tasarımı
  - algoritmalar
toc: true
---

Bir API’nin başarısı bazen aldığı istek sayısıyla ölçülür; fakat kontrolsüz trafik, başarı hikâyesini saniyeler içinde kesinti raporuna dönüştürebilir. Rate limiting, belirli bir kullanıcı, IP adresi, API anahtarı veya uç nokta için kabul edilen istek miktarını sınırlayan savunma katmanıdır. Amaç yalnızca kötü niyetli botları engellemek değildir: adil kaynak paylaşımı sağlamak, maliyetleri öngörülebilir tutmak ve veritabanı gibi hassas bağımlılıkları korumaktır.
``

Temel problem basittir: Bir zaman aralığında en fazla $L$ isteğe izin verilsin. Ortalama sürdürülebilir hız kabaca $r = L/T$ olarak yazılabilir; burada $T$ pencere uzunluğudur. Ancak gerçek dünyada trafik düzenli akmaz. Kullanıcılar sayfayı yeniler, istemciler hata sonrası yeniden dener ve kampanyalar ani zirveler üretir. Bu nedenle algoritma seçimi, yalnızca ortalamayı değil, **ani patlamalara ne kadar tolerans verileceğini** de belirler.

## Sabit pencere: Basit, hızlı, ama sınırda cömert

Fixed Window Counter, örneğin her dakika için bir sayaç tutar. Sayaç $L$ değerine ulaşınca yeni istekleri reddeder; yeni dakika başlayınca sıfırlanır. Redis üzerinde `INCR` ve anahtarın yaşam süresiyle uygulanabildiği için oldukça pratiktir. Ne var ki pencere sınırında çift patlama oluşabilir: Kullanıcı 12:00:59’da $L$ istek, 12:01:00’da bir $L$ istek daha gönderebilir. Bir saniyede teorik olarak $2L$ istek kabul edilir.

## Kayan pencere: Daha adil ölçüm

Sliding Window Log, her isteğin zaman damgasını saklar ve son $T$ saniyedeki kayıtları sayar. Böylece “herhangi bir ardışık $T$ aralığında en fazla $L$ istek” kuralına yaklaşır. Adalet yüksektir; fakat yüksek trafikte her istek için zaman damgası depolamak bellek ve sorgu maliyeti doğurur. Sliding Window Counter ise komşu iki pencerenin sayaçlarını ağırlıklandırarak yaklaşık sonuç üretir. Örneğin önceki pencerenin etkisi $w$ ise tahmini kullanım:

$$C = C_{mevcut} + w \times C_{önceki}$$

Bu yaklaşım, günlük API trafiğinde doğruluk ile maliyet arasında iyi bir uzlaşmadır.

| Algoritma | Patlama toleransı | Bellek maliyeti | Güçlü tarafı | Risk |
|---|---:|---:|---|---|
| Sabit pencere | Yüksek | Düşük | Kolay dağıtım | Sınır patlaması |
| Kayan pencere günlüğü | Düşük | Yüksek | Çok adil | Yoğun trafikte pahalı |
| Kayan pencere sayacı | Orta | Düşük | Dengeli yaklaşım | Yaklaşık hesap |
| Token Bucket | Ayarlanabilir | Düşük | Patlama dostu | Doğru parametre ister |
| Leaky Bucket | Düşük | Düşük | Düzgün çıkış hızı | Gecikme yaratabilir |

## Token Bucket ve Leaky Bucket: Trafik mühendisliği ikilisi

Token Bucket’ta kovaya saniyede $r$ token eklenir; kovanın kapasitesi $b$ kadardır. Her istek bir token harcar. Token varsa istek geçer, yoksa reddedilir veya bekletilir. Uzun vadeli oran $r$, izin verilen ani patlama büyüklüğü ise yaklaşık $b$ olur. Bu nedenle mobil istemciler veya kısa süreli yoğunluk yaşayan API’ler için çok uygundur.

Leaky Bucket ise istekleri bir kuyruğa alır ve sabit hızla dışarı sızdırır. Çıkış hızı düzenlidir; arka servisi korumak için harikadır. Ancak kuyruk büyürse kullanıcı gecikme hisseder; kuyruk dolarsa istek düşürülür. Kısacası Token Bucket girişte esneklik, Leaky Bucket çıkışta disiplin sağlar.

Aşağıdaki Python örneği, token bucket’ın çekirdek mantığını gösterir. Üretimde paylaşımlı durum için süreç içi sözlük yerine Redis ve atomik Lua betikleri tercih edilmelidir.

```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_per_second):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_per_second
        self.updated_at = time.monotonic()

    def allow(self):
        now = time.monotonic()
        elapsed = now - self.updated_at
        self.tokens = min(self.capacity,
                          self.tokens + elapsed * self.refill_rate)
        self.updated_at = now

        if self.tokens < 1:
            return False
        self.tokens -= 1
        return True
```

`allow()` önce geçen zamana göre token üretir, sonra istek için bir token tüketir. Sonuç `False` ise HTTP `429 Too Many Requests` döndürmek, ayrıca istemciye `Retry-After` başlığını eklemek iyi bir API vatandaşlığıdır.

Son seçim trafik karakterine bağlıdır: basit yönetim panellerinde sabit pencere yeterli olabilir; ödeme, giriş ve herkese açık API’lerde kayan pencere veya token bucket daha güvenli davranır. Her durumda limitleri kullanıcı kimliği ve uç nokta bazında ayrı düşünün, ölçüm ekleyin ve limit aşımını izleyin. Rate limiting bir duvar değil; sistemin nefes almasını sağlayan ritimdir.
