---
layout: post
title: "OpenTelemetry ile Dağıtık Sistem Gözlemlenebilirliği"
math: true
categories: 
  - Bilgi
tags: 
  - opentelemetry
  - gözlemlenebilirlik
  - dağıtık sistemler
toc: true
---

Modern uygulamalar nadiren tek bir sunucuda yaşayan, tek parça yapılar hâlindedir. Bir kullanıcı isteği; API Gateway, kimlik doğrulama servisi, ödeme sistemi, mesaj kuyruğu ve veritabanı arasında dolaşabilir. Sorun çıktığında ise klasik “sunucu çalışıyor mu?” sorusu yetersiz kalır. OpenTelemetry (OTel), bu karmaşık yolculuğu iz, metrik ve log sinyallerini ortak bir standart altında birleştirerek görünür hâle getirir.

``

## Neden gözlemlenebilirlik?

Monitoring genellikle önceden tanımlı sorulara yanıt verir: CPU yüzde kaç? Hata oranı arttı mı? Gözlemlenebilirlik ise bilinmeyen soruları da sorabilmeyi hedefler: “Sadece Avrupa’daki kullanıcıların ödeme isteği neden yavaş?”, “Gecikme Redis’ten mi, yoksa üçüncü taraf servisten mi kaynaklanıyor?”

Bu yaklaşımın üç temel sinyali vardır:

| Sinyal | Ne anlatır? | Tipik kullanım |
|---|---|---|
| Trace (iz) | Bir isteğin servisler arasındaki uçtan uca yolculuğu | Gecikme ve bağımlılık analizi |
| Metric (metrik) | Zaman içinde sayısallaştırılmış ölçümler | Alarm, kapasite ve trend takibi |
| Log | Olayın bağlamını taşıyan ayrıntılı kayıtlar | Hata ayıklama ve denetim |

Bir isteğin toplam süresini kabaca şöyle düşünebiliriz: $T_{toplam}=T_{gateway}+T_{servis}+T_{veritabanı}+T_{harici}$. Trace verisi, bu terimlerin hangisinin büyüdüğünü gösterir. Metrikler bunun ne sıklıkta gerçekleştiğini, loglar ise hatanın ayrıntısını açıklar.

## Trace ve span: İsteğin seyahat günlüğü

OpenTelemetry’de bir **trace**, tek bir iş akışının tamamıdır. Her servis veya operasyon bu trace içinde bir **span** üretir. Span; başlangıç zamanı, bitiş zamanı, durum, öznitelikler ve ebeveyn ilişkisi taşır. Böylece API’nin başlattığı bir isteğin ödeme sağlayıcısında beklediği 2,4 saniye kolayca fark edilir.

Önemli nokta, `trace_id` bilgisinin servisler arasında taşınmasıdır. HTTP başlıkları, gRPC metadata’sı veya mesaj kuyruğu header’ları bu bağlamı iletebilir. Bağlam koparsa sistemdeki her parça ayrı hikâye anlatır; bağlam korunursa tek bir uçtan uca anlatı oluşur.

Aşağıdaki Node.js örneği, bir işleme ait özel span ve öznitelik ekler:

```javascript
const { trace, SpanStatusCode } = require('@opentelemetry/api');

async function createOrder(order) {
  const tracer = trace.getTracer('order-service');

  return tracer.startActiveSpan('order.create', async (span) => {
    try {
      span.setAttribute('order.id', order.id);
      span.setAttribute('payment.method', order.paymentMethod);

      const result = await saveOrder(order);
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error) {
      span.recordException(error);
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      throw error;
    } finally {
      span.end();
    }
  });
}
```

Bu kod, otomatik enstrümantasyonun yakalayamadığı iş alanı bilgisini ekler. Ancak `email`, kart numarası veya erişim anahtarı gibi hassas veriler span özniteliği ve loglara yazılmamalıdır.

## Collector: Telemetri trafiğinin kontrol kulesi

Uygulamaların doğrudan her gözlemleme aracına veri göndermesi yerine OpenTelemetry Collector kullanmak yaygın bir mimaridir. Collector; veriyi alır, örnekler, dönüştürür, filtreler ve Jaeger, Prometheus, Grafana Tempo veya farklı bir ticari platforma yönlendirir.

| Doğrudan dışa aktarma | Collector üzerinden dışa aktarma |
|---|---|
| Uygulama yapılandırması karmaşıklaşır | Tek merkezden yönlendirme yapılır |
| Backend değişimi kod etkileyebilir | Backend değişimi daha izole olur |
| Filtreleme sınırlıdır | Örnekleme ve veri maskeleme yapılabilir |

Özellikle yüksek trafikte her trace’i saklamak pahalıdır. Örnekleme oranı $p$ ise, yaklaşık saklanan trace sayısı $N_{saklanan}=p \times N_{toplam}$ olur. Hata içeren veya çok yavaş trace’leri önceliklendiren tail sampling, maliyet ile teşhis gücü arasında daha akıllı bir denge kurar.

## Darboğaz avı için pratik akış

Önce servislerin RED metriklerini izleyin: **Rate** (istek hızı), **Errors** (hata oranı) ve **Duration** (süre). Ardından p95 veya p99 gecikmesi yükseldiğinde ilgili trace’leri açın. Ortalama süre aldatıcı olabilir; çünkü birkaç çok yavaş istek kullanıcı deneyimini ciddi biçimde bozabilir. Son olarak aynı `trace_id` ile ilişkilendirilmiş logları inceleyin.

OpenTelemetry’nin asıl gücü, tek bir panel sağlaması değil; veriyi üreticiden bağımsız, bağlamı korunmuş ve ilişkilendirilebilir şekilde toplamasıdır. Doğru adlandırılmış span’lar, anlamlı metrik etiketleri ve yapılandırılmış loglar sayesinde “sistem yavaş” şikâyeti, ölçülebilir ve çözülebilir bir mühendislik problemine dönüşür.
