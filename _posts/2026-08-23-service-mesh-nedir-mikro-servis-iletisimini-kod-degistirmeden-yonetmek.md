---
layout: post
title: "Service Mesh Nedir? Mikro Servis İletişimini Kod Değiştirmeden Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - service mesh
  - mikro servisler
  - kubernetes
image: /img/service-mesh-nedir-91.png
---

Mikro servis mimarisi büyüdükçe asıl zorluk yalnızca servis yazmak değildir; servislerin birbirini güvenli, hızlı ve gözlemlenebilir biçimde çağırmasını sağlamaktır. Service mesh, bu iletişim katmanını uygulama kodundan ayıran altyapı yaklaşımıdır. Böylece Java, Go, Python ya da Node.js ile yazılmış servisler; tekrar tekrar istemci kütüphanesi eklemeden ortak ağ politikalarından yararlanabilir.
``

Klasik bir yapıda `Sipariş Servisi`, `Ödeme Servisi`ne HTTP isteği atar. Zaman aşımı, yeniden deneme, TLS sertifikası, çağrı izleme ve hata durumunda devre kesici gibi ayrıntılar çoğunlukla uygulama koduna veya ayrı SDK'lara dağılır. Bu yaklaşım başlangıçta pratiktir; fakat onlarca servis ve ekip olduğunda kuralların tutarlı kalması zorlaşır.

Service mesh bu sorunu **data plane** ve **control plane** ayrımıyla ele alır. Data plane, her servisin yanında çalışan proxy'lerden oluşur; Kubernetes dünyasında bu proxy çoğu zaman bir *sidecar container* olarak çalışır. Uygulama, ağ trafiğini doğrudan hedef servise göndermek yerine yerel proxy üzerinden geçirir. Proxy; yönlendirme, şifreleme, metrik toplama ve hata politikalarını uygular. Control plane ise bu proxy'lere merkezi kuralları dağıtır.

Bir isteğin basitleştirilmiş yolculuğu şöyledir:

```text
Sipariş Uygulaması -> Yerel Proxy -> Ağ -> Ödeme Proxy'si -> Ödeme Uygulaması
```

Bu ek katman ilk bakışta karmaşık görünebilir. Ancak amaç, çapraz kesen ağ sorumluluklarını tek bir standartta toplamaktır. Örneğin başarı oranını şu basit oranla izleyebilirsiniz:

$$Başarı\ Oranı = \frac{Başarılı\ İstek}{Toplam\ İstek} \times 100$$

Proxy'ler her isteğin gecikmesini, durum kodunu ve hedefini bildirdiğinde bu oran tüm servislerde aynı tanımla hesaplanır. Dağıtık izleme için de istek kimliği proxy'ler arasında taşınabilir; böylece bir siparişin hangi çağrı zincirinde yavaşladığı görünür olur.

| Özellik | Uygulama içi yaklaşım | Service mesh yaklaşımı |
|---|---|---|
| Yeniden deneme | Her dilde ayrı kod/SDK | Merkezi politika ile proxy'de |
| mTLS | Sertifika yönetimi uygulamaya yük olur | Servisler arası otomatik şifreleme |
| Gözlemlenebilirlik | Elle metrik ve trace eklenir | Trafikten standart telemetri üretilir |
| Trafik bölme | Özel yönlendirme kodu gerekir | Canary ve sürüm kurallarıyla yapılır |

Örneğin ödeme servisinin yeni `v2` sürümünü tüm kullanıcılara bir anda açmak risklidir. Mesh üzerinde trafiğin %10'unu `v2`ye, kalanını `v1`e yönlendirebilirsiniz. Hata oranı yükselirse kural geri alınır; uygulama imajını değiştirmek gerekmez. Istio benzeri bir yapıda kavram şu YAML ile ifade edilebilir:

```yaml
http:
  - route:
      - destination:
          host: payment
          subset: v1
        weight: 90
      - destination:
          host: payment
          subset: v2
        weight: 10
```

Bu yapı, `payment` hedefine giden isteklerin ağırlıklı dağıtımını tanımlar. Kodunuz hâlâ normal HTTP veya gRPC çağrısı yapar; yönlendirme kararını mesh verir. Aynı mekanizma ile belirli kullanıcılara, bölgelere veya HTTP başlıklarına göre trafik kuralları oluşturulabilir.

Elbette service mesh sihirli değnek değildir. Proxy'ler CPU ve bellek tüketir, ağ yoluna küçük de olsa gecikme ekler ve operasyon ekibinin yeni kavramları öğrenmesini gerektirir. Az sayıda servis, basit trafik ve sınırlı güvenlik ihtiyacı olan bir sistemde mesh gereksiz ağır olabilir. Buna karşılık çok ekipli Kubernetes ortamlarında; mTLS, trafik kontrolü, ayrıntılı metrikler ve tutarlı dayanıklılık politikaları ihtiyaç hâline geldiyse güçlü bir yatırım olur.

Özetle service mesh, iş mantığını ağ mühendisliğinden ayırır. Uygulamanız “ödeme yap” demeye devam eder; güvenli bağlantı, deneme stratejisi, gözlem ve kontrollü dağıtım gibi zor detayları ise ortak altyapı katmanı üstlenir.

![service-mesh-nedir-91](/img/service-mesh-nedir-91.svg)

