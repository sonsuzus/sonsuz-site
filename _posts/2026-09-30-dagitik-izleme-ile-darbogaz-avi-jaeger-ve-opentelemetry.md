---
layout: post
title: "Dağıtık İzleme ile Darboğaz Avı: Jaeger ve OpenTelemetry"
math: true
categories: 
  - Bilgi
tags: 
  - dağıtık izleme
  - jaeger
  - opentelemetry
  - mikroservis
  - performans
  - gözlemlenebilirlik
toc: true
image: /img/dagitik-izleme-ile-26.png
---

Bir kullanıcı “Satın Al” düğmesine tıkladığında perde arkasında API Gateway, kimlik doğrulama, sepet, stok, ödeme ve bildirim gibi birçok servis harekete geçebilir. Ekranın dönüp durduğu üç saniye boyunca hangi servisin zaman kaybettirdiğini yalnızca loglara bakarak bulmak, samanlıkta iğne aramaya benzer. Dağıtık izleme ise bu yolculuğu tek bir harita üzerinde göstererek performans dedektifliğini oldukça keyifli hâle getirir.


![dagitik-izleme-ile-26](/img/dagitik-izleme-ile-26.svg)

``

## Trace, span ve context üçlüsü

Dağıtık izlemenin temel birimi **trace** olarak adlandırılır. Trace, tek bir kullanıcı isteğinin sistem boyunca yaptığı yolculuğun tamamıdır. Yolculuktaki her işlem ise bir **span** ile temsil edilir. Örneğin ödeme servisinin veri tabanını sorgulaması ayrı, bankanın API’sini çağırması ayrı bir span olabilir.

Her span genellikle şu bilgileri taşır:

- Başlangıç ve bitiş zamanı
- Servis ve operasyon adı
- Başarı veya hata durumu
- HTTP metodu, durum kodu ve özel etiketler
- Üst span ile olan ebeveyn-çocuk ilişkisi

Bir isteğin toplam süresi kabaca kritik yol üzerindeki işlemlerle belirlenir:

$$T_{istek} \approx \sum_{i=1}^{n} T_{kritik\ span_i}$$

Ancak paralel çalışan iki işlem varsa süreler doğrudan toplanmaz. Örneğin stok kontrolü 200 ms, fiyat sorgusu 300 ms sürüyor ve ikisi paralel çalışıyorsa katkıları yaklaşık $\max(200, 300)=300$ ms olur.

Servisler arasındaki bağlantıyı koruyan unsur **trace context** bilgisidir. OpenTelemetry, `traceparent` gibi HTTP başlıklarıyla aynı trace kimliğini bir servisten diğerine aktarır. Bu aktarım koparsa haritada birbirinden habersiz küçük adacıklar oluşur.

## OpenTelemetry ve Jaeger ne yapar?

| Araç | Temel görevi | Benzetme |
|---|---|---|
| OpenTelemetry | Telemetri üretir, işler ve dışa aktarır | Olay yerindeki muhabir |
| OTel Collector | Veriyi alır, dönüştürür ve yönlendirir | Trafik kontrol merkezi |
| Jaeger | Trace verisini saklar ve görselleştirir | Dedektifin kanıt panosu |

OpenTelemetry satıcıdan bağımsız bir standarttır; Jaeger ise toplanan trace’leri inceleyebileceğimiz popüler bir arayüzdür. Böylece uygulama kodunu belirli bir izleme ürününe zincirlemeyiz.

## Python servisini izlemeye hazırlamak

Aşağıdaki örnek, Flask uygulamasını otomatik olarak enstrümante eder ve span verilerini OTLP üzerinden Collector’a yollar:

```python
from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

app = Flask(__name__)
trace.set_tracer_provider(TracerProvider())

exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))
FlaskInstrumentor().instrument_app(app)

@app.get("/checkout")
def checkout():
    return {"status": "started"}
```

`FlaskInstrumentor`, gelen HTTP isteği için otomatik span oluşturur. `BatchSpanProcessor` ise her span’i tek tek göndermek yerine gruplandırarak uygulama üzerindeki ağ yükünü azaltır. Üretimde servis adını bir resource niteliği olarak eklemek de Jaeger ekranındaki ayrımı kolaylaştırır.

Collector tarafında veriyi Jaeger uyumlu bir hedefe yönlendiren sade bir yapılandırma kullanılabilir:

```yaml
receivers:
  otlp:
    protocols:
      grpc:

exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [otlp/jaeger]
```

Collector kullanmak; örnekleme, hassas alanları temizleme ve veriyi birden fazla sisteme gönderme gibi kararları uygulamalardan merkezi bir noktaya taşır.

## Darboğaz nasıl yakalanır?

Jaeger’da ilgili servisi ve operasyonu seçip yavaş bir trace açtığımızda zaman çizelgesi görünür. On servislik zincirde `payment-service` 1,8 saniye sürerken diğer servisler 50–100 ms aralığındaysa ilk şüpheli bellidir. Fakat yalnızca en uzun span’e bakmak yetmez; ödeme servisinin içindeki veri tabanı veya harici banka çağrısı incelenmelidir.

Karşılaştırma için p95 gecikmesi yararlıdır. İsteklerin yüzde 95’i $L$ süresinden hızlı tamamlanıyorsa:

$$P(T \leq L)=0.95$$

Ortalama değer sakin görünürken p95’in yükselmesi, az sayıdaki kullanıcının ciddi yavaşlık yaşadığını gösterebilir. Hata etiketleri, tekrar denemeler ve seri çalışan sorgular da zaman çizelgesinde aranmalıdır.

Son olarak her isteği kaydetmek maliyetli olabilir. Sağlıklı isteklerde düşük oranlı, hatalı veya yavaş isteklerde yüksek oranlı örnekleme uygulanabilir. Kişisel verileri span etiketlerine koymamak, servis adlarını standartlaştırmak ve loglara trace kimliği eklemek de avı hızlandırır. Böylece “Sistem yavaş” şikâyeti, “stok servisindeki üçüncü sorgu 740 ms sürüyor” gibi ölçülebilir bir bulguya dönüşür.
