---
layout: post
title: "API Gateway ile Merkezi Kimlik Doğrulama ve Rate Limiting Mimarisi"
math: true
categories: 
  - Bilgi
tags: 
  - api-gateway
  - mikroservis
  - kimlik-doğrulama
  - rate-limiting
  - siber-güvenlik
  - dağıtık-sistemler
toc: true
image: /img/api-gateway-ile-44.png
---

Onlarca mikroservisin bulunduğu bir sistemde her servise ayrı ayrı kimlik doğrulama, yetkilendirme ve trafik sınırlama kodu eklemek kısa sürede bakım kâbusuna dönüşebilir. API Gateway, dış dünyadan gelen istekleri tek noktada karşılayarak bu ortak sorumlulukları merkezileştirir. Ancak kapıya güçlü bir kilit takarken herkesin aynı kapıda kuyruk oluşturabileceğini de unutmamak gerekir.
``

## API Gateway neyi merkezileştirir?

API Gateway; istemci ile mikroservisler arasında çalışan bir ters proxy ve politika uygulama katmanıdır. İstek önce gateway'e ulaşır, güvenlik ve trafik kurallarından geçerse ilgili servise yönlendirilir.

Tipik akış şöyledir:

1. İstemci erişim belirteciyle istek gönderir.
2. Gateway belirtecin geçerliliğini denetler.
3. Kullanıcının rolü veya kapsamı kontrol edilir.
4. Rate limiting sayacı güncellenir.
5. İstek uygun mikroservise yönlendirilir.
6. Servis yanıtı gateway üzerinden istemciye döner.

Bu yaklaşım servislerin iş mantığına odaklanmasını sağlar. Yine de mikroservislerin gateway'e körü körüne güvenmesi doğru değildir. İç ağdan gelebilecek saldırılara karşı servis seviyesinde temel yetkilendirme ve servisler arası kimlik doğrulama korunmalıdır. Bu yaklaşım genellikle **zero trust** düşüncesiyle desteklenir.

## Kimlik doğrulama seçenekleri

Gateway, JWT gibi kendi içinde doğrulanabilen belirteçleri yerel olarak kontrol edebilir. JWT imzası açık anahtarla doğrulandığı için her istekte kimlik sunucusuna gidilmez. Opak belirteçlerde ise introspection servisine sorgu göndermek gerekebilir.

| Yöntem | Avantaj | Dezavantaj |
|---|---|---|
| JWT doğrulama | Hızlıdır, harici çağrı gerektirmez | İptal edilen token süresi dolana kadar geçerli kalabilir |
| Token introspection | Merkezi iptal ve oturum kontrolü sağlar | Kimlik sunucusunda ek yük ve gecikme oluşturur |
| API anahtarı | Makineden makineye kullanımda basittir | Kullanıcı yetkilendirmesi için tek başına yetersizdir |
| mTLS | Servis kimliğini güçlü biçimde doğrular | Sertifika yönetimi karmaşıktır |

JWT doğrulamasında `exp`, `iss`, `aud` ve imza alanlarının tamamı kontrol edilmelidir. Yalnızca token içindeki kullanıcı adına bakmak, üzerinde üniforma bulunan herkesi polis sanmaya benzer.

## Rate limiting matematiği

En basit model sabit zaman penceresidir. Bir istemcinin pencere içindeki istek sayısı $N$, izin verilen sınır $L$ ise istek şu koşulda kabul edilir:

$$N < L$$

Ancak pencere sınırlarında ani trafik patlamaları oluşabilir. Örneğin kullanıcı bir dakikanın son saniyesinde 100, sonraki dakikanın ilk saniyesinde 100 istek göndererek iki saniyede 200 isteğe ulaşabilir.

Token Bucket algoritması daha esnektir. Kova en fazla $B$ token tutar ve saniyede $r$ token ile dolar. Geçen süre $\Delta t$ olduğunda yeni miktar:

$$T_{yeni} = \min(B, T_{eski} + r\Delta t)$$

Her istek bir token tüketir. Böylece kısa süreli sıçramalara izin verilirken uzun dönem ortalaması sınırlandırılır.

```javascript
async function rateLimit(clientId) {
  const key = `limit:${clientId}`;
  const count = await redis.incr(key);

  if (count === 1) {
    await redis.expire(key, 60);
  }

  if (count > 100) {
    throw new Error("429 Too Many Requests");
  }
}
```

Bu örnek, istemci başına dakikada 100 istek sınırı uygular. Redis kullanılması, birden fazla gateway örneğinin ortak sayaç görmesini sağlar. Üretimde `INCR` ve süre ayarının atomik bir Lua betiğiyle çalıştırılması daha güvenlidir.

## Merkezi kapının darboğaz riski

Gateway tek örnek olarak çalıştırılırsa hem performans darboğazı hem de tek hata noktası olur. Çözüm, durum tutmayan birden fazla gateway örneğini yük dengeleyici arkasında çalıştırmaktır. Sayaçlar Redis gibi dağıtık bir depoda tutulabilir; fakat bu kez Redis kritik bağımlılığa dönüşür.

| Risk | Önlem |
|---|---|
| Gateway çökmesi | Çoklu bölge ve yatay ölçekleme |
| Redis gecikmesi | Yerel kota, kümeleme ve zaman aşımı |
| Kimlik servisi çökmesi | JWT, anahtar önbelleği ve circuit breaker |
| Yoğun log trafiği | Asenkron loglama ve örnekleme |

Sonuç olarak API Gateway güvenlik politikalarında tutarlılık ve operasyonel kolaylık sağlar. Başarılı mimari, yalnızca kapıyı merkezileştirmez; kapının çoğaltılmasını, gözlemlenmesini ve bağımlılıkları çöktüğünde nasıl davranacağını da tasarlar. Çünkü dijital kalede en gösterişli kapı bile menteşeleri kadar güvenilirdir.

![api-gateway-ile-44](/img/api-gateway-ile-44.svg)

