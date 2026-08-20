---
layout: post
title: "Kong ve Traefik ile Rate Limiting, Circuit Breaker ve Retry Politikaları"
math: true
categories: 
  - Bilgi
tags: 
  - apı gateway
  - kong
  - traefik
---

Modern mikroservis mimarisinde API Gateway yalnızca istekleri doğru servise yönlendiren bir trafik polisi değildir; aynı zamanda sistemin kapısındaki güvenlik görevlisi, tamponu ve kriz yöneticisidir. Kong ve Traefik gibi gateway'ler üzerinden rate limiting, circuit breaker ve retry politikaları tanımlamak; ani trafik patlamalarının, geçici ağ hatalarının ve domino etkisi yaratan servis arızalarının tüm platformu devirmesini engeller.
``

Bu üç mekanizmayı birlikte anlamak önemlidir. **Rate limiting** gelen talebi sınırlar, **retry** geçici hatalarda kontrollü yeniden deneme yapar, **circuit breaker** ise sorunlu bağımlılığa giden çağrıları bir süre keser. Amaç yalnızca hata sayısını azaltmak değil, kuyrukların büyümesini, bağlantı havuzlarının tükenmesini ve gecikmenin zincirleme yayılmasını önlemektir.

## Dayanıklılık matematiği: neden sınırsız retry tehlikelidir?

Bir isteğin başarısız olma olasılığı $p$ ise, en fazla $n$ denemede başarısız kalma olasılığı yaklaşık olarak $p^n$ olur. İlk bakışta retry harika görünür: $p=0.2$ ve $n=3$ için nihai başarısızlık $0.2^3=0.008$ seviyesine iner. Ancak her başarısız istek üç kez daha yük oluşturuyorsa, zaten zorlanan servis daha da zorlanır. Bu durumun adı **retry storm**'dur.

Üstel geri çekilme (exponential backoff) bu riski azaltır:

$$t_k = \min(t_{max}, t_0 \times 2^k) + jitter$$

Buradaki `jitter`, aynı anda hata alan binlerce istemcinin aynı milisaniyede tekrar saldırmasını engelleyen rastgele gecikmedir.

| Mekanizma | Koruduğu şey | Tipik tepki | Yanlış kullanım riski |
|---|---|---|---|
| Rate limiting | Gateway ve backend kapasitesi | 429 Too Many Requests | Meşru kullanıcıların engellenmesi |
| Retry | Geçici ağ/5xx hataları | Gecikmeli yeniden deneme | Trafik çarpanı oluşması |
| Circuit breaker | Hatalı bağımlılıktan izolasyon | Fast-fail veya fallback | Sorun çözülse bile gereksiz kesinti |

## Kong tarafında trafik freni

Kong'da rate limiting çoğunlukla bir plugin üzerinden uygulanır. Aşağıdaki örnek, `orders-api` servisine tüketici başına dakikada 100 istek sınırı koyar. `redis` politikası, birden fazla Kong düğümünde ortak sayaç kullanmak için özellikle uygundur.

```yaml
_format_version: "3.0"
services:
  - name: orders-api
    url: http://orders-service:8080
    routes:
      - name: orders-route
        paths: ["/orders"]
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: redis
          redis_host: redis
          redis_port: 6379
          limit_by: consumer
          fault_tolerant: true
```

`limit_by: consumer`, API anahtarıyla tanınan kullanıcıları ayrı ayrı sınırlar. Herkesin tek bir kotayı paylaşmasını istemiyorsanız IP yerine consumer bazlı yaklaşım daha adildir. Ayrıca ödeme oluşturma gibi yan etkili uçlarda retry politikası çok dikkatli ele alınmalıdır: aynı ödeme iki kez işlenmemelidir. Bu tür işlemlerde `Idempotency-Key` kullanmak güçlü bir savunmadır.

## Traefik ile retry ve devre kesme

Traefik middlewares yaklaşımıyla benzer korumalar sunar. Aşağıdaki dinamik yapılandırma, kısa süreli ağ problemlerinde iki yeniden deneme yapar; hata oranı yükselirse circuit breaker yeni çağrıları hızla reddeder.

```yaml
http:
  middlewares:
    api-retry:
      retry:
        attempts: 3
        initialInterval: 100ms
    orders-breaker:
      circuitBreaker:
        expression: "ResponseCodeRatio(500, 600, 0, 600) > 0.25"

  routers:
    orders:
      rule: "PathPrefix(`/orders`)"
      service: orders-service
      middlewares:
        - api-retry
        - orders-breaker
```

Bu ifade, 5xx yanıtlarının oranı %25'i geçtiğinde devreyi açar. Circuit breaker'ın klasik durumları şöyledir: **Closed** normal trafiktir; **Open** istekleri backend'e göndermeden başarısız döner; **Half-Open** ise sınırlı sayıda deneme ile servisin toparlanıp toparlanmadığını ölçer.

| Senaryo | Önerilen politika |
|---|---|
| Herkese açık arama API'si | Sıkı rate limit, kısa retry |
| Sipariş oluşturma | Idempotency, çok sınırlı retry |
| Yavaşlayan harici ödeme servisi | Circuit breaker, fallback mesajı |
| Okuma ağırlıklı katalog servisi | Cache + rate limit + retry |

Son olarak ölçemediğiniz korumayı yönetemezsiniz. 429, 5xx, retry sayısı, breaker açık kalma süresi ve p95 gecikme metriklerini Prometheus/Grafana ile izleyin. Eşik değerlerini tahminle değil, yük testleri ve gerçek trafik verileriyle ayarlayın. Sağlam gateway yapılandırması, hatayı yok etmez; hatanın kontrollü, görünür ve sınırlı kalmasını sağlar.
