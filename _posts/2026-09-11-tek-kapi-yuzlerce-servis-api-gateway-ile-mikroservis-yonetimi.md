---
layout: post
title: "Tek Kapı, Yüzlerce Servis: API Gateway ile Mikroservis Yönetimi"
math: true
categories: 
  - Bilgi
tags: 
  - apı gateway
  - mikroservis
  - yetkilendirme
toc: true
---

Bir e-ticaret sisteminde kullanıcı, sipariş, ödeme ve stok servislerinin farklı sunucularda çalıştığını düşünün. İstemcinin bütün bu adresleri bilmesi; güvenlik, sürüm yönetimi ve hata takibi açısından kısa sürede kabusa dönüşür. API Gateway modeli, yüzlerce servisin önüne tek bir giriş kapısı koyarak bu karmaşayı yönetilebilir hâle getirir. Kısacası mikroservis mahallesinin güvenlik görevlisi, trafik polisi ve danışma masası aynı noktada buluşur.

``

## API Gateway tam olarak nedir?

API Gateway, istemciler ile mikroservisler arasında bulunan bir **ters vekil (reverse proxy)** katmanıdır. Mobil uygulama veya web istemcisi doğrudan servislerle konuşmak yerine tüm istekleri ağ geçidine gönderir. Gateway isteğin yolunu, kimliğini, hızını ve hedefini değerlendirerek uygun servise yönlendirir.

Temel akış şöyledir:

1. İstemci `api.example.com/orders` adresine istek gönderir.
2. Gateway erişim belirtecini doğrular.
3. İstemcinin istek kotasını kontrol eder.
4. İsteği uygun sipariş servisine yönlendirir.
5. Servisten gelen yanıtı istemciye iletir ve işlemi kaydeder.

Bu yaklaşım, servislerin internete doğrudan açılmasını engeller. Böylece güvenlik kuralları her serviste tekrar tekrar yazılmak yerine merkezî olarak uygulanabilir.

## Gateway kullanılan ve kullanılmayan yapı

| Özellik | Doğrudan servis erişimi | API Gateway modeli |
|---|---|---|
| Servis adresleri | İstemci tüm adresleri bilir | İstemci yalnızca Gateway'i bilir |
| Yetkilendirme | Her serviste uygulanır | Merkezî olarak yönetilir |
| Hız sınırı | Dağınık kurallar gerekir | Tek noktadan uygulanır |
| Sürüm geçişi | İstemci değişikliği gerekebilir | Yönlendirme ile gizlenebilir |
| Gözlemlenebilirlik | Loglar farklı yerlerdedir | Ortak metrik üretilebilir |
| Arıza etkisi | Servise göre değişir | Gateway kritik bağımlılıktır |

## Yetkilendirme ve hız sınırlandırma

Gateway, JWT gibi bir erişim belirtecinin imzasını doğrulayabilir ve belirteç içindeki rol bilgisini inceleyebilir. Örneğin `/admin` yolu yalnızca `admin` rolüne açılabilir. Buradaki önemli ayrım şudur: Gateway kaba erişim kontrolünü yaparken, “Bu kullanıcı yalnızca kendi siparişini görebilir mi?” gibi iş kuralları ilgili mikroserviste kalmalıdır.

Hız sınırlandırmada sık kullanılan yöntemlerden biri **token bucket** algoritmasıdır. Kovadaki en fazla jeton sayısı $B$, saniyede eklenen jeton sayısı $r$ ve geçen süre $t$ ise kullanılabilir jeton sayısı yaklaşık olarak şöyle hesaplanır:

$$T_{yeni} = \min(B, T_{eski} + r \cdot t)$$

Her istek bir jeton tüketir. Jeton kalmadığında Gateway genellikle `429 Too Many Requests` yanıtı döndürür. Bu mekanizma hem kötü niyetli trafiği hem de yanlışlıkla sonsuz döngüye giren istemcileri dizginler.

## Basit bir Gateway örneği

Aşağıdaki Express örneği, kullanıcı bazında hız sınırı uygular ve istekleri sipariş servisine aktarır:

```javascript
import express from 'express';
import rateLimit from 'express-rate-limit';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();

const limiter = rateLimit({
  windowMs: 60 * 1000,
  limit: 100,
  keyGenerator: (req) => req.headers['x-user-id'] || req.ip,
  standardHeaders: true
});

app.use('/orders', limiter, createProxyMiddleware({
  target: 'http://orders-service:8080',
  changeOrigin: true,
  pathRewrite: { '^/orders': '' }
}));

app.listen(3000, () => console.log('Gateway 3000 portunda hazır'));
```

Bu kod, her kullanıcıya dakikada 100 istek hakkı verir. Ardından `/orders` yolunu farklı bir sunucuda veya konteynerde çalışan sipariş servisine yönlendirir. Gerçek sistemlerde buna JWT doğrulama, zaman aşımı, yeniden deneme ve dağıtık sayaç için Redis eklenir.

## Darboğaza dönüşmesini önlemek

Gateway tek giriş noktası olduğu için aynı zamanda tek hata noktası olmamalıdır. Birden fazla Gateway örneği yük dengeleyicinin arkasında çalıştırılmalı; sağlık kontrolleri, otomatik ölçeklendirme ve merkezi loglama kullanılmalıdır. Ayrıca yavaş servislerin kaynakları tüketmesini önlemek için timeout ve circuit breaker kuralları tanımlanmalıdır.

Doğru tasarlanmış bir API Gateway, mikroservisleri görünmez bir orkestra gibi yönetir: İstemci yalnızca şefi görür, fakat arkada yüzlerce servis uyum içinde çalışır.
