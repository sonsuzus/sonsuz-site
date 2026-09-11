---
layout: post
title: "OpenTelemetry ile Bir İsteğin Ağdaki Macerasını Uçtan Uca İzlemek"
math: true
categories: 
  - Bilgi
tags: 
  - opentelemetry
  - gözlemlenebilirlik
  - dağıtık izleme
toc: true
---

Bir kullanıcı “Satın Al” düğmesine bastığında istek API ağ geçidine, kimlik servisine, sipariş uygulamasına, veri tabanına ve ödeme sağlayıcısına uğrayabilir. Geleneksel metin günlükleri bu duraklarda ayrı ayrı iz bırakır; ancak parçaları birleştirmek çoğu zaman dedektiflik işidir. OpenTelemetry ise isteğe ortak bir kimlik vererek yolculuğu tek bir zaman çizelgesinde görmemizi sağlar.
``

## Günlük Tutmak Neden Tek Başına Yetmez?

Bir hata günlüğü bize “ödeme zaman aşımına uğradı” diyebilir. Fakat gecikmenin ödeme servisinde mi, DNS çözümlemesinde mi, veri tabanında mı oluştuğunu söylemeyebilir. Üstelik yüzlerce sunucunun bulunduğu bir sistemde zaman damgalarını elle karşılaştırmak, samanlıkta iğne aramaya benzer.

Gözlemlenebilirlik üç temel sinyal üzerine kurulur:

| Sinyal | Yanıtladığı soru | Örnek |
|---|---|---|
| Log | Ne oldu? | “Kart doğrulama başarısız” |
| Metric | Ne kadar sık veya ne kadar fazla? | Hata oranı, CPU kullanımı |
| Trace | İstek nereden geçti, nerede bekledi? | API → Sipariş → Ödeme |

OpenTelemetry, kısaca OTel, bu sinyalleri üretmek ve dışarı aktarmak için satıcıdan bağımsız API’ler, SDK’lar ve araçlar sunar. Kendisi bir depolama ya da görselleştirme ürünü değildir. Verileri Jaeger, Grafana, Tempo, Prometheus veya farklı bir gözlemlenebilirlik platformuna gönderebilir.

## Trace, Span ve Context Mantığı

Bir isteğin bütün yolculuğuna **trace** denir. Yolculuktaki her işlem ise bir **span** ile temsil edilir. Örneğin ana span HTTP isteğini, alt span’ler SQL sorgusunu ve ödeme servisi çağrısını gösterebilir.

Her trace benzersiz bir `trace_id`, her span ise bir `span_id` taşır. Servisler arası HTTP çağrılarında `traceparent` başlığı aktarılır. Böylece ödeme servisi, gelen isteğin hangi yolculuğa ait olduğunu bilir. Bu işleme **context propagation** adı verilir.

Basitleştirilmiş seri bir akışta toplam gecikme şöyle düşünülebilir:

$$T_{toplam} \approx \sum_{i=1}^{n} T_{span_i}$$

Ancak paralel işlemlerde süreler doğrudan toplanmaz; kullanıcı deneyimini genellikle en uzun bağımlılık zinciri, yani kritik yol belirler.

| Kavram | Kapsam | Tipik bilgi |
|---|---|---|
| Trace | Uçtan uca istek | Tüm servis rotası |
| Span | Tek operasyon | Başlangıç, süre, durum |
| Attribute | Span ayrıntısı | HTTP metodu, rota |
| Event | Anlık olay | Yeniden deneme başladı |
| Baggage | Servisler arası bağlam | Bölge veya tenant bilgisi |

## Node.js ile Temel Enstrümantasyon

Aşağıdaki örnek, otomatik enstrümantasyonu etkinleştirip span’leri OTLP protokolüyle bir OpenTelemetry Collector’a yollar:

```js
// telemetry.js
const { NodeSDK } = require("@opentelemetry/sdk-node");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-http");
const { getNodeAutoInstrumentations } = require("@opentelemetry/auto-instrumentations-node");

const sdk = new NodeSDK({
  serviceName: "siparis-api",
  traceExporter: new OTLPTraceExporter({
    url: "http://otel-collector:4318/v1/traces"
  }),
  instrumentations: [getNodeAutoInstrumentations()]
});

sdk.start();
```

Bu dosya uygulama modüllerinden **önce** yüklenmelidir:

```bash
node --require ./telemetry.js app.js
```

Otomatik enstrümantasyon; Express isteklerini, HTTP çağrılarını ve desteklenen veri tabanı işlemlerini kodu baştan yazmadan izleyebilir. İş alanına özgü adımlar için elle span eklemek de mümkündür:

```js
const span = tracer.startSpan("stok-rezerve-et");
try {
  await reserveStock();
  span.setAttribute("order.item_count", 3);
} catch (error) {
  span.recordException(error);
  span.setStatus({ code: 2 });
  throw error;
} finally {
  span.end();
}
```

## Collector ve Üretim İpuçları

Collector, uygulamalar ile gözlemlenebilirlik platformu arasında trafik polisi gibi çalışır. Veriyi alır, toplu gönderir, hassas alanları temizler ve farklı hedeflere yönlendirir. Böylece uygulamanın belirli bir sağlayıcıya bağımlılığı azalır.

Üretimde her trace’i saklamak pahalı olabilir. **Sampling** ile isteklerin belirli oranı seçilebilir; hatalı veya aşırı yavaş trace’ler ise öncelikli tutulabilir. Parola, kart numarası ve erişim belirteci gibi sırlar attribute olarak kaydedilmemelidir. Doğru adlandırılmış span’ler, kontrollü örnekleme ve merkezi Collector sayesinde “sistem yavaş” şikâyeti, “ödeme servisindeki TLS bağlantısı 840 ms sürdü” gibi eyleme dönük bir teşhise dönüşür.
