---
layout: post
title: "Servis Ağları: Istio ile Mikroservis Trafiğini Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - istio
  - service-mesh
  - mikroservis
  - kubernetes
  - envoy
  - devops
  - güvenlik
toc: true
image: /img/servis-aglari-istio-58.png
---

Mikroservis mimarisinde servis sayısı arttıkça ağ trafiği küçük bir şehir merkezine dönüşür: İstekler farklı rotalara sapar, bazı servisler yavaşlar ve güvenlik kontrolleri her köşede yeniden yazılır. Service Mesh, uygulama kodunu değiştirmeden bu karmaşayı yöneten bir trafik katmanıdır. Istio ise Envoy proxy'lerini kullanarak güvenlik, gözlemlenebilirlik ve akıllı yönlendirme özelliklerini Kubernetes ortamına taşır.


![servis-aglari-istio-58](/img/servis-aglari-istio-58.svg)

``

## Service Mesh neden gereklidir?

Bir `siparis` servisinin `odeme` servisini çağırdığını düşünelim. Geleneksel yaklaşımda zaman aşımı, yeniden deneme, TLS ve metrik toplama kodları uygulamanın içine eklenir. On farklı programlama dili kullanılıyorsa aynı ağ mantığı on farklı biçimde uygulanabilir.

Service Mesh yaklaşımında bu sorumluluklar altyapıya aktarılır. Her uygulama pod'una bir **sidecar**, yani “yan araba” proxy eklenir. Uygulama normal şekilde HTTP isteği gönderir; Kubernetes ağ kuralları trafiği Envoy'a yönlendirir. Böylece servis, proxy'nin varlığından haberdar olmadan politikalarla yönetilir.

| Özellik | Uygulama içinde | Istio Service Mesh ile |
|---|---|---|
| TLS yönetimi | Her serviste kodlanır | Otomatik mTLS uygulanır |
| Yeniden deneme | Kütüphaneye bağlıdır | Trafik politikasıyla tanımlanır |
| Metrikler | Manuel entegrasyon gerekir | Proxy üzerinden üretilir |
| Yönlendirme | Uygulama mantığına girer | VirtualService ile yönetilir |
| Dil bağımlılığı | Yüksektir | Düşüktür |

## Sidecar mekaniği

Istio'nun klasik mimarisi iki düzlemden oluşur. **Data plane**, pod'ların yanındaki Envoy proxy'lerinden meydana gelir ve gerçek trafiği taşır. **Control plane** bileşeni `istiod` ise yapılandırmaları üretir, sertifikaları dağıtır ve proxy'lerin hangi kuralları uygulayacağını bildirir.

Bir isteğin toplam gecikmesini basitleştirerek şöyle gösterebiliriz:

$$T_{toplam} = T_{uygulama} + T_{ag} + T_{proxy-gidis} + T_{proxy-donus}$$

Proxy eklemek sıfır maliyetli değildir. Buna karşılık merkezi güvenlik ve görünürlük sağlar. Başarı oranı da genellikle şu metrikle izlenir:

$$Basari\ Orani = \frac{2xx\ ve\ 3xx\ yanitlari}{tum\ yanitlar} \times 100$$

Istio sidecar enjeksiyonu bir namespace için şu şekilde etkinleştirilebilir:

```bash
kubectl label namespace magazam istio-injection=enabled
kubectl apply -f deployment.yaml
```

Etiket sayesinde Istio admission webhook'u, oluşturulan pod tanımına Envoy konteynerini otomatik olarak ekler. Mevcut pod'ların yeniden oluşturulması gerektiği unutulmamalıdır.

## Akıllı trafik yönlendirme

Yeni bir ödeme sürümünü kullanıcıların yalnızca yüzde 10'una açmak isteyelim. Aşağıdaki `VirtualService`, trafiği ağırlıklı biçimde dağıtır:

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: odeme
spec:
  hosts:
    - odeme
  http:
    - route:
        - destination:
            host: odeme
            subset: v1
          weight: 90
        - destination:
            host: odeme
            subset: v2
          weight: 10
```

Bu yapılandırma bir **canary deployment** senaryosudur. `DestinationRule` içinde tanımlanan `v1` ve `v2` alt kümeleri arasında trafik bölünür. Sorun görülürse v2 ağırlığı sıfırlanarak hızlıca geri dönüş yapılabilir.

## Güvenlik ve izlenebilirlik

Istio'nun mTLS özelliği, servisler arası trafiği şifreler ve iki tarafın kimliğini doğrular. Böylece ağ içinde bulunmanın otomatik güven anlamına gelmediği **Zero Trust** yaklaşımı desteklenir. `AuthorizationPolicy` ile “yalnızca sipariş servisi ödeme servisine erişebilir” gibi kurallar uygulanabilir.

Envoy ayrıca istek sayısı, gecikme ve hata oranı gibi telemetri verileri üretir. Prometheus metrikleri saklar, Grafana grafikleştirir, Jaeger dağıtık izleri gösterir ve Kiali servisler arasındaki ilişkiyi haritaya dönüştürür.

Elbette Service Mesh sihirli değnek değildir. Proxy'ler CPU ve bellek tüketir; hatalı yeniden deneme politikaları yoğunluğu artırabilir. Örneğin her isteğin en fazla $r$ kez denenmesi durumunda teorik istek yükü $N(r+1)$ seviyesine çıkabilir. Bu nedenle Istio, karmaşık ve çok servisli sistemlerde güçlüdür; birkaç servisten oluşan küçük projelerde ise operasyonel maliyeti faydasını aşabilir. Doğru ölçekte kullanıldığında mikroservis trafiğinin gerçekten disiplinli trafik polisine dönüşür.
