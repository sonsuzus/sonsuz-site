---
layout: post
title: "Observability Üçlüsü: Log, Metric ve Trace ile Sistemin Röntgenini Çekmek"
math: true
categories: 
  - Bilgi
tags: 
  - observability
  - log
  - metric
  - trace
  - opentelemetry
  - devops
toc: true
image: /img/observability-uclusu-log-93.png
---

Bir uygulamanın çalışıyor olması, sağlıklı olduğu anlamına gelmez. Kullanıcılar yavaşlıktan yakınırken sunucunun neşeyle “200 OK” demesi mümkündür. Observability, yani gözlemlenebilirlik; sistemin iç durumunu dışarıya ürettiği sinyallerden anlayabilme yeteneğidir. Bu sinyallerin klasik üçlüsü **log, metric ve trace** verileridir. Tek başlarına faydalı, birlikte kullanıldıklarında ise dijital bir dedektif ekibi kadar etkilidirler.


![observability-uclusu-log-93](/img/observability-uclusu-log-93.svg)

``

## Monitoring ile observability aynı şey mi?

Monitoring, önceden belirlediğimiz sorulara cevap verir: “CPU kullanımı yüzde 80'i geçti mi?” Observability ise daha önce düşünmediğimiz soruları da araştırmamızı sağlar: “Yalnızca mobil kullanıcıların ödeme isteği neden cuma akşamları yavaşlıyor?”

Bir sistemin gözlemlenebilirliğini teorik olarak, iç durumların dış sinyallerden ayırt edilebilirliği şeklinde düşünebiliriz. Basitleştirilmiş bir sağlık skoru şöyle modellenebilir:

$$
H = w_m M + w_l L + w_t T
$$

Burada $M$ metric, $L$ log, $T$ trace görünürlüğünü; $w$ değerleri ise her sinyalin bağlama göre ağırlığını temsil eder. Amaç gerçekten tek bir skor hesaplamak değil, hiçbir sinyalin bütün resmi tek başına göstermediğini vurgulamaktır.

## Üç sinyal ne anlatır?

| Sinyal | Cevapladığı soru | Güçlü yanı | Örnek |
|---|---|---|---|
| Metric | Ne oluyor? | Sayısal eğilimleri hızla gösterir | Hata oranı %4 oldu |
| Log | Neden olmuş olabilir? | Olayın ayrıntılarını taşır | Veritabanı zaman aşımı oluştu |
| Trace | Nerede oldu? | Dağıtık isteğin yolculuğunu gösterir | Gecikme ödeme servisinde başladı |

### Metric: Gösterge panelinin ikaz lambası

Metric, zaman boyunca ölçülen sayısal veridir. İstek sayısı, hata oranı, bellek tüketimi ve yanıt süresi buna örnektir. Özellikle **RED yöntemi** servisler için kullanışlıdır: Rate, Errors ve Duration.

Bir servisin hata oranı şu şekilde hesaplanabilir:

$$
E = \frac{\text{hatalı istek sayısı}}{\text{toplam istek sayısı}} \times 100
$$

Metric anomaliyi hızla gösterir; ancak belirli bir isteğin neden bozulduğunu çoğunlukla söylemez.

### Log: Olay yerindeki tanık

Log, belirli bir anda gerçekleşen olaya ait bağlamsal kayıttır. Yapılandırılmış log kullanmak, düz metin içinde define aramaktan daha kolaydır:

```json
{
  "level": "error",
  "service": "payment-api",
  "trace_id": "7fa21c",
  "message": "Banka servisi zaman aşımına uğradı",
  "duration_ms": 3021
}
```

Bu kayıt; hatanın seviyesini, servisini, süresini ve ilişkili trace kimliğini belirtir. Parola, erişim anahtarı veya kart numarası gibi hassas bilgiler ise loglanmamalıdır. Loglar yardımcı olmalı; güvenlik ekibine yeni bir korku filmi yaşatmamalıdır.

### Trace: İsteğin seyahat günlüğü

Trace, bir isteğin dağıtık sistemde geçtiği servisleri gösterir. Her işlem parçasına **span** denir. Örneğin istek sırasıyla API Gateway, Sipariş Servisi, Ödeme Servisi ve veritabanından geçebilir.

```text
POST /orders              840 ms
├── order-service         120 ms
├── payment-service       650 ms
│   └── bank-api          610 ms
└── database               70 ms
```

Bu görünüm, toplam gecikmenin büyük bölümünün `bank-api` çağrısından kaynaklandığını açıkça gösterir.

## Birlikte nasıl çalışırlar?

Senaryomuzda metric paneli ödeme hatalarının arttığını bildirir. İlgili zaman aralığındaki trace verileri filtrelenir ve yavaş isteklerin Ödeme Servisi üzerinde toplandığı görülür. Trace içindeki `trace_id` ile loglara geçildiğinde banka servisinin zaman aşımına uğradığı anlaşılır.

Akış kısaca şöyledir:

1. **Metric** alarmı başlatır.
2. **Trace** sorunun konumunu daraltır.
3. **Log** teknik nedeni ayrıntılandırır.

Bu bağlantıyı kurmanın anahtarı ortak alanlardır: `service.name`, `environment`, `trace_id` ve `span_id`. OpenTelemetry gibi standartlar, sinyallerin aynı bağlamla üretilmesini kolaylaştırır.

İyi observability, her şeyi sınırsızca kaydetmek değildir. Anlamlı sinyal üretmek, örnekleme uygulamak, saklama maliyetini yönetmek ve ekiplerin gerçekten kullanabileceği paneller tasarlamaktır. Metric dumanı, trace dumanın geldiği odayı, log ise kibriti kimin çaktığını gösterir. Üçü birleştiğinde sistem artık karanlık bir kutu olmaktan çıkar.
