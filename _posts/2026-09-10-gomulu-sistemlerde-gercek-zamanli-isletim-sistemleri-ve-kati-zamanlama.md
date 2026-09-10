---
layout: post
title: "Gömülü Sistemlerde Gerçek Zamanlı İşletim Sistemleri ve Katı Zamanlama"
math: true
categories: 
  - Bilgi
tags: 
  - rtos
  - gömülü sistemler
  - gerçek zamanlı programlama
toc: true
---

Bir hava yastığının “birazdan açılması”, motor kontrol ünitesinin ateşleme sinyalini uygun olduğunda göndermesi veya kalp pilinin birkaç saniyeliğine düşünmesi kabul edilemez. Gömülü sistemlerde başarı yalnızca doğru sonucu üretmek değil, bu sonucu belirlenen zaman sınırı içinde üretmektir. Gerçek Zamanlı İşletim Sistemleri, yani RTOS’lar, görevleri olabildiğince hızlı koşturmaktan ziyade davranışlarını öngörülebilir hâle getirir.

``

## Gerçek zamanlı olmak ne demektir?

Genel amaçlı bir işletim sistemi ortalama performansı, kullanıcı deneyimini ve toplam işlem kapasitesini önemser. RTOS ise **determinizme** odaklanır. Bir görevin en kötü koşullarda ne kadar sürede tamamlanacağının hesaplanabilmesi gerekir.

Bir periyodik görev için temel zamanlama koşulu şöyle gösterilebilir:

$$R_i \leq D_i$$

Burada $R_i$ görevin en kötü durum yanıt süresini, $D_i$ ise son teslim zamanını belirtir. Görev çok hızlı çalışsa bile zaman zaman $D_i$ sınırını aşıyorsa katı gerçek zamanlı sistem için uygun değildir.

| Sistem türü | Deadline kaçırılırsa | Örnek |
|---|---|---|
| Katı gerçek zamanlı | Sistem başarısız kabul edilir | Hava yastığı, uçuş kontrolü |
| Esnek gerçek zamanlı | Kalite düşer ancak çalışma sürer | Video konferans, ses akışı |
| Genel amaçlı | Gecikme çoğunlukla performans sorunudur | Metin düzenleyici, web tarayıcı |

## Görev, öncelik ve kesme üçgeni

RTOS uygulamaları birbirinden bağımsız **görevlere** ayrılır. Zamanlayıcı, işlemciyi bu görevler arasında paylaştırır. Öncelikli ve kesilebilir bir zamanlayıcıda yüksek öncelikli görev hazır olduğunda düşük öncelikli görev durdurulur. Böylece kritik iş, market kuyruğunda alarm veren bir itfaiyeci gibi öne geçer.

Kesme servis rutinleri donanım olaylarına hızlı tepki verir; fakat uzun tutulmaları diğer görevleri geciktirir. Bu nedenle kesme içinde yalnızca gerekli veri alınmalı, ağır işlem bir göreve bildirim gönderilerek ertelenmelidir.

Yaygın zamanlama yaklaşımları şunlardır:

| Algoritma | Öncelik mantığı | Güçlü yönü |
|---|---|---|
| Rate Monotonic | Kısa periyot yüksek öncelik | Basit ve analiz edilebilir |
| Deadline Monotonic | Kısa deadline yüksek öncelik | Deadline’lar periyottan farklıysa etkilidir |
| Earliest Deadline First | En yakın deadline önce | Yüksek işlemci kullanımı sağlar |

Rate Monotonic altında $n$ bağımsız görev için yeterli işlemci kullanım sınırı yaklaşık olarak şöyledir:

$$U=\sum_{i=1}^{n}\frac{C_i}{T_i} \leq n(2^{1/n}-1)$$

$C_i$ en kötü çalışma süresi, $T_i$ görev periyodudur. Bu eşitsizlik sağlanıyorsa görev kümesi zamanlanabilir kabul edilir; sağlanmaması ise otomatik olarak başarısız olduğu anlamına gelmez, daha ayrıntılı yanıt süresi analizi gerekir.

## FreeRTOS ile periyodik görev

Aşağıdaki görev, sensörü her 10 milisaniyede bir okur. `vTaskDelayUntil`, sıradan gecikmenin aksine önceki uyanma zamanını temel alarak periyot kaymasını azaltır.

```c
void SensorTask(void *argument)
{
    TickType_t lastWake = xTaskGetTickCount();
    const TickType_t period = pdMS_TO_TICKS(10);

    for (;;) {
        int sample = read_sensor();
        process_sample(sample);

        vTaskDelayUntil(&lastWake, period);
    }
}
```

Kodun periyodik olması tek başına garanti sağlamaz. `read_sensor()` fonksiyonunun en kötü çalışma süresi, kesme gecikmeleri, bağlam değiştirme maliyeti ve daha yüksek öncelikli görevlerin etkisi ölçülmelidir.

## Gizli düşmanlar

Öncelik terslenmesi, düşük öncelikli bir görevin kilit tuttuğu için kritik görevi bekletmesidir. **Priority inheritance** mekanizması, kilidi tutan görevin önceliğini geçici olarak yükselterek sorunu sınırlar. Dinamik bellek tahsisi, belirsiz süreli döngüler, bloklayan sürücüler ve önbellek davranışı da jitter oluşturabilir.

Katı gerçek zamanlı tasarımın özeti şudur: Ortalama süreye değil **WCET** değerine bak, paylaşılan kaynakları sınırla, görev önceliklerini matematiksel olarak analiz et ve gerçek donanım üzerinde ölçüm yap. RTOS zamanı büyütmez; zamanı disipline eder.
