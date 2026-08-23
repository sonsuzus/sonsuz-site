---
layout: post
title: "Envoy Proxy Kullanımı: Modern Servis Ağlarının Görünmez Trafik Polisi"
math: true
categories: 
  - Program
tags: 
  - Envoy Proxy
  - Mikroservisler
  - Service Mesh
---

Mikroservis mimarisinde her servis yalnızca iş mantığını çözmez; istek yönlendirme, TLS, yeniden deneme, gözlemlenebilirlik ve hata toleransı gibi ağ sorumluluklarıyla da uğraşır. Envoy Proxy, bu tekrar eden görevleri uygulama kodundan ayıran yüksek performanslı bir L7 proxy'dir. Basitçe söylemek gerekirse, servislerin önünde veya yanında duran, trafiği akıllıca yöneten görünmez bir trafik polisidir.

``

## Envoy neden gereklidir?

Dağıtık bir sistemde bir isteğin başarı olasılığı, çağırdığı bileşenlerin başarı olasılıklarının çarpımına yakındır. Örneğin üç bağımlılığın sırasıyla $0.99$, $0.98$ ve $0.97$ erişilebilirliğe sahip olduğunu varsayalım:

$$A_{toplam} = 0.99 \times 0.98 \times 0.97 \approx 0.941$$

Yani her servis tek başına oldukça güvenilir görünse de uçtan uca başarı oranı yaklaşık %94,1 olur. Timeout, retry, devre kesici ve yük dengeleme gibi ağ politikaları bu nedenle yalnızca "ekstra özellik" değildir. Envoy, bunları merkezi ve tutarlı şekilde uygular.

Envoy çoğunlukla iki modelde çalışır: API Gateway olarak dış dünyadan gelen trafiği karşılar veya **sidecar** olarak her uygulama podunun yanında çalışır. Sidecar yaklaşımı Istio gibi service mesh çözümlerinin temel taşlarından biridir.

| Özellik | Geleneksel uygulama içi çözüm | Envoy Proxy |
|---|---|---|
| Retry ve timeout | Her dilde ayrı kod gerekir | Yapılandırmadan yönetilir |
| Metrikler | Uygulama entegrasyonuna bağlıdır | Standartlaştırılmış istatistikler sunar |
| TLS/mTLS | Uygulamanın sorumluluğundadır | Proxy katmanında uygulanabilir |
| Trafik bölme | Genellikle karmaşık | Route ve weight ile kolaydır |

## Temel trafik modeli

Envoy yapılandırmasında üç kavram sık görülür: **listener**, **route** ve **cluster**. Listener bir portu dinler. Route, gelen isteğin nereye gideceğini belirler. Cluster ise hedef servislerin mantıksal grubudur. İstek akışı şu şekildedir:

`İstemci → Listener → Route → Cluster → Hedef Servis`

Aşağıdaki örnek, Envoy'un `8080` portundan gelen `/api` isteklerini `backend-service` adlı hedefe iletmesini sağlar:

```yaml
static_resources:
  listeners:
    - name: http_listener
      address:
        socket_address:
          address: 0.0.0.0
          port_value: 8080
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress_http
                route_config:
                  name: local_route
                  virtual_hosts:
                    - name: backend
                      domains: ["*"]
                      routes:
                        - match: { prefix: "/api" }
                          route: { cluster: backend_service }
                http_filters:
                  - name: envoy.filters.http.router
  clusters:
    - name: backend_service
      connect_timeout: 1s
      type: LOGICAL_DNS
      load_assignment:
        cluster_name: backend_service
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: backend
                      port_value: 3000
```

Bu yapılandırmada `LOGICAL_DNS`, hedef adresin DNS üzerinden çözülmesini sağlar; özellikle container ortamlarında pratiktir. `connect_timeout: 1s` ise bağlantı kurulamazsa isteğin sonsuza kadar beklemesini engeller.

## Dayanıklılık politikaları

Envoy'un gücü yalnızca yönlendirme değildir. Örneğin geçici ağ hatalarında sınırlı retry kullanabilirsiniz. Ancak retry sayısı kontrolsüz artarsa sorun büyür: Bir servis yavaşladığında tekrar denemeler ek yük oluşturur. Yaklaşık yük etkisi $L = R \times N$ ile düşünülebilir; burada $R$ istek sayısı, $N$ ise ortalama deneme sayısıdır. Bu yüzden retry'ı timeout ve circuit breaker ile birlikte tasarlayın.

Canary dağıtımında da Envoy oldukça kullanışlıdır. Trafiğin %90'ını kararlı sürüme, %10'unu yeni sürüme yönlendirebilir; metrikleri izledikten sonra oranı artırabilirsiniz. Böylece "Cuma günü production'a basalım" heyecanı, ölçülebilir ve geri alınabilir bir sürece dönüşür.

Son olarak, Envoy yönetim arayüzünü yalnızca güvenli ağlarda açın; yapılandırma hataları tüm trafiği etkileyebilir. Sağlık kontrolleri, erişim logları ve Prometheus metrikleriyle birlikte kullanıldığında Envoy, modern servis ağınızın hem navigasyonu hem de emniyet kemeri olur.
