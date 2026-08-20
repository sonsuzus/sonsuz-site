---
layout: post
title: "API Gateway ve Servis Ağı: Mikroservis Trafiğinin Kontrol Kulesi"
math: true
categories: 
  - Bilgi
tags: 
  - mikroservisler
  - api gateway
  - service mesh
toc: true
---

Mikroservis mimarisinde her servis kendi başına küçük ve bağımsız görünür; fakat sistem büyüdükçe aralarındaki iletişim hızla karmaşıklaşır. Bir kullanıcının tek isteği, kimlik doğrulama, katalog, stok, ödeme ve bildirim servislerine uğrayabilir. API Gateway dış dünyadan gelen trafiğin kontrol kulesiyken, servis ağı (service mesh) iç ağdaki servisler arası konuşmanın trafik polisi gibidir. Birlikte kullanıldıklarında güvenlik, yönlendirme, hata toleransı ve gözlemlenebilirlik için düzenli bir omurga oluştururlar.

``

## İki Katman, İki Farklı Sorumluluk

API Gateway, istemcilerin mikroservislerin iç yapısını bilmesini engelleyen bir **giriş noktasıdır**. Mobil uygulama ya da web arayüzü tek bir uç noktaya istek atar; gateway isteği uygun servislere yönlendirir, token doğrular, hız sınırı uygular ve gerekirse yanıtları birleştirir. Bu yaklaşım, istemciyi servis sayısındaki değişimlerden korur.

Servis ağı ise genellikle küme içindeki doğu-batı trafiğine odaklanır. Istio, Linkerd veya Consul gibi çözümlerde her uygulama podunun yanında çalışan bir *sidecar proxy* bulunur. Servis kodu doğrudan ağ politikalarıyla uğraşmaz; proxy, çağrıları yakalar ve merkezi kuralları uygular. Böylece Java, Go veya Python ile yazılmış servisler aynı iletişim standartlarından yararlanır.

| Özellik | API Gateway | Servis Ağı |
|---|---|---|
| Trafik yönü | Kuzey-güney, dışarıdan içeri | Doğu-batı, servisler arası |
| Ana kullanıcı | İstemci uygulamaları | İç servisler ve platform ekibi |
| Tipik görev | Kimlik doğrulama, API sürümleme | mTLS, retry, trafik bölme |
| Konum | Küme veya sistem sınırı | Uygulama podları arasında |

## Güvenlik: Kim Konuşuyor, Ne Kadar Konuşuyor?

Gateway, OAuth 2.0/JWT doğrulaması yaparak dış kullanıcının kimliğini denetler. Servis ağı ise **mTLS** ile iki servisin de kimliğini karşılıklı doğrular ve trafiği şifreler. Bu ayrım önemlidir: Kullanıcının geçerli token taşıması, ödeme servisinin katalog servisine her koşulda erişebilmesi anlamına gelmez.

Hız sınırlama da gateway tarafında yaygındır. Basit bir sabit pencere yaklaşımında izin verilen istek sayısı şu koşulla ifade edilir:

$$R(t) \leq L$$

Burada $R(t)$ belirli zaman penceresindeki istek sayısını, $L$ ise limiti temsil eder. Ancak dağıtık sistemlerde token bucket gibi yöntemler ani trafik patlamalarını daha dengeli karşılar. Servis ağında ise yetkilendirme politikalarıyla `payment` servisinin yalnızca `order` tarafından çağrılması sağlanabilir.

## Dayanıklılık ve Akıllı Yönlendirme

Bir servisin geçici olarak yavaşlaması, tüm sistemi durdurmamalıdır. Proxy katmanında timeout, retry ve circuit breaker kuralları tanımlanabilir. Yine de retry dikkat ister: Başarısızlık olasılığı $p$ olan bir çağrıda en fazla $n$ deneme için başarı olasılığı kabaca $1-p^n$ olur; fakat fazla tekrar, zaten zorlanan servise ek yük bindirebilir. Bu nedenle yalnızca idempotent işlemler için sınırlı retry uygulanmalıdır.

Aşağıdaki Istio VirtualService örneği, trafiğin %90'ını kararlı sürüme, %10'unu yeni sürüme yollar. Bu, canary dağıtımının güvenli başlangıcıdır:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts:
    - catalog
  http:
    - route:
        - destination:
            host: catalog
            subset: stable
          weight: 90
        - destination:
            host: catalog
            subset: v2
          weight: 10
      retries:
        attempts: 2
        perTryTimeout: 500ms
```

Bu yapılandırma uygulama kodunu değiştirmeden sürüm bazlı trafik dağıtımı ve kontrollü tekrar denemesi sağlar.

## Gözlemlenebilirlik: Trafiğin Hikâyesini Okumak

Gateway ve mesh, metrik, log ve distributed trace üretmek için ideal noktalardır. Gecikme yüzdelikleri özellikle değerlidir: ortalama gecikme iyi görünürken kullanıcıların küçük bir kısmı çok kötü deneyim yaşayabilir. Bu yüzden p95 ve p99 değerlerini izlemek gerekir. Örneğin p99 gecikmesinin 800 ms olması, isteklerin %99'unun bu sürenin altında tamamlandığını söyler.

| Sinyal | Sorulacak soru | Örnek araç |
|---|---|---|
| Metrik | Hata ve gecikme artıyor mu? | Prometheus, Grafana |
| Log | Hangi istekte ne oldu? | Loki, ELK |
| Trace | Çağrı zinciri nerede yavaşladı? | Jaeger, Tempo |

Sonuç olarak gateway ve servis ağı rakip değil, tamamlayıcıdır. Gateway sınırı korur; servis ağı içeride güvenli ve ölçülebilir bir iletişim dili kurar. Küçük sistemlerde yalnızca gateway yeterli olabilir. Servis sayısı, ekip sayısı ve dağıtım sıklığı arttığında ise mesh, karmaşıklığı uygulama kodundan altyapı katmanına taşıyarak ciddi bir standartlaşma sağlar.
