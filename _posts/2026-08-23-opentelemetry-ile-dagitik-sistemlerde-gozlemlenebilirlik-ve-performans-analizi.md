---
layout: post
title: "OpenTelemetry ile Dağıtık Sistemlerde Gözlemlenebilirlik ve Performans Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - OpenTelemetry
  - Gözlemlenebilirlik
  - Dağıtık Sistemler
---

Dağıtık uygulamalarda bir isteğin nerede yavaşladığını bulmak, tek sunuculu günlerin rahatlığını özletebilir. Kullanıcı "sipariş ver" düğmesine basar; istek API ağ geçidinden ödeme servisine, stok servisine, kuyruk sistemine ve veritabanına uğrar. Hata ekranı ise yalnızca 500 döndürür. OpenTelemetry (OTel), bu karmaşık yolculuğu standart araçlarla görünür hâle getirerek izleme, hata ayıklama ve kapasite planlama süreçlerini aynı dilde buluşturur.
``

OpenTelemetry bir izleme aracı değil, **telemetri üretme ve taşıma standardıdır**. Uygulamanın ürettiği verileri OTLP protokolüyle bir Collector'a gönderir; Collector da Jaeger, Grafana Tempo, Prometheus, Elasticsearch veya bulut sağlayıcısı gibi arka uçlara aktarabilir. Bu ayrım önemlidir: enstrümantasyon kodunuz kalırken analiz platformunu gerektiğinde değiştirebilirsiniz.

Gözlemlenebilirliğin üç temel sinyali vardır:

| Sinyal | Sorduğu soru | Tipik örnek |
|---|---|---|
| Trace (iz) | İstek sistemde hangi yollardan geçti? | `checkout` isteğinin servis zinciri |
| Metric (metrik) | Sistem genel olarak ne durumda? | Saniyedeki istek, CPU, hata oranı |
| Log (günlük) | Belirli anda ne oldu? | Ödeme sağlayıcısının hata mesajı |

Bir trace, tek bir kullanıcı isteğinin uçtan uca kimliğidir; içindeki her işlem ise **span** olarak adlandırılır. Örneğin HTTP isteği, SQL sorgusu ve harici ödeme çağrısı ayrı span'lerdir. Span'ler arasındaki ebeveyn-çocuk ilişkisi, gecikmenin hangi katmanda biriktiğini gösterir. Toplam süre kabaca şöyle modellenebilir:

$$T_{istek} = T_{API} + T_{stok} + T_{ödeme} + T_{veritabanı} + T_{ağ}$$

Ancak paralel çağrılarda sürelerin toplanmadığını unutmayın. Stok ve kampanya kontrolleri eşzamanlıysa kritik yol belirleyicidir: $T_{istek} \approx \max(T_{stok}, T_{kampanya}) + T_{ödeme}$. Trace görünümü, bu kritik yolu tahmin yerine ölçerek gösterir.

Python tarafında manuel span eklemek oldukça basittir. Otomatik enstrümantasyon HTTP istemcileri ve framework'ler için çok iş görse de, iş kurallarını anlatan span'leri elle eklemek tanı koyma kalitesini artırır:

```python
from opentelemetry import trace

tracer = trace.get_tracer("order-service")

def reserve_stock(order_id: str, product_id: str):
    # İş adımını trace üzerinde görünür kılar.
    with tracer.start_as_current_span("stock.reserve") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("product.id", product_id)
        try:
            result = warehouse.reserve(product_id)
            span.set_attribute("stock.reserved", result)
            return result
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
            raise
```

Burada `order.id` gibi öznitelikler filtreleme için değerlidir; fakat e-posta, kart numarası, erişim belirteci ve tam adres gibi hassas verileri span'e koymak ciddi bir güvenlik hatasıdır. Collector üzerinde maskeleme ve örnekleme politikaları uygulanmalıdır.

| Yaklaşım | Avantajı | Riski veya maliyeti |
|---|---|---|
| %100 trace örnekleme | Her hatayı inceleme olanağı | Yüksek depolama ve ağ maliyeti |
| Head sampling | Başta hızlı karar verir | Nadir hatalar kaçabilir |
| Tail sampling | Hatalı ve yavaş trace'leri saklar | Collector kaynak ihtiyacı artar |

Performans analizinde yalnızca ortalama gecikmeye güvenmeyin. Ortalama 120 ms görünürken kullanıcıların bir bölümü saniyelerce bekliyor olabilir. Bu nedenle p95 ve p99 yüzdeliklerini izleyin: $p95 = 95\%$ isteğin bu süreden hızlı tamamlandığı eşiktir. Hata oranını da $error\_rate = errors / total\_requests$ formülüyle, endpoint ve sürüm etiketleri üzerinden takip edin.

Sağlıklı bir başlangıç için HTTP, veritabanı ve mesajlaşma istemcilerinde otomatik enstrümantasyonu açın; ardından ödeme, stok ayırma ve fatura oluşturma gibi iş açısından kritik adımlara manuel span ekleyin. Loglara `trace_id` ilişkilendirmesi koyduğunuzda, bir alarmdan ilgili metriğe, oradan trace'e ve en sonunda hata günlüğüne geçebilirsiniz. İşte gözlemlenebilirliğin sihri budur: "sistem yavaş" şikâyetini, kanıtlanabilir ve çözülebilir bir teknik hikâyeye dönüştürmek.
