---
layout: post
title: "Process Scheduler Algoritmaları: CPU Zamanını Kim Hak Ediyor?"
math: true
categories: 
  - Bilgi
tags: 
  - işletim sistemi
  - cpu
  - process scheduler
  - algoritma
  - round robin
  - performans
toc: true
---

Bilgisayarınızda müzik çalarken kod derleyebiliyor, tarayıcıda sekmeler arasında dolaşabiliyor ve arka planda dosya indirebiliyorsanız bunu CPU’nun gizli trafik polisi olan **process scheduler**’a borçlusunuz. İşlemci aynı anda sınırlı sayıda işi yürütebildiği için scheduler, hazır durumdaki process’lerden hangisinin ne zaman ve ne kadar süre çalışacağını belirler. Kısacası soru şudur: CPU zamanını kim hak ediyor?

``

## Scheduler neden gereklidir?

Bir process; **ready**, **running**, **waiting** ve **terminated** gibi durumlar arasında dolaşır. CPU boşaldığında scheduler, ready queue içinden bir process seçer. Seçilen process’in yüklenmesi sırasında yapılan register ve bellek bağlamı değişimine **context switch** denir.

Context switch faydalıdır fakat bedava değildir. Bir process’in çalışma süresi $t$, geçiş maliyeti de $c$ ise CPU’nun yararlı çalışma oranı yaklaşık olarak şöyledir:

$$
\text{Verimlilik} = \frac{t}{t+c}
$$

Zaman dilimini aşırı küçültmek sistemi daha tepkisel gösterirken geçiş maliyetini artırır. Büyük tutmak ise kısa işlerin uzun süre beklemesine neden olabilir. Scheduler’ın görevi hız, adalet ve tepki süresi arasında denge kurmaktır.

## Temel ölçütler

Bir algoritmanın başarısı yalnızca “işler bitti mi?” sorusuyla ölçülmez:

- **Turnaround time:** Process’in sisteme girişinden tamamlanmasına kadar geçen süre.
- **Waiting time:** Ready queue içinde beklenen toplam süre.
- **Response time:** İlk CPU erişimine kadar geçen süre.
- **Throughput:** Birim zamanda tamamlanan process sayısı.
- **Fairness:** Process’lerin CPU’ya makul biçimde erişebilmesi.

Bir process için bekleme süresi şu şekilde ifade edilebilir:

$$
W = T_{tamamlanma} - T_{varış} - T_{çalışma}
$$

## Popüler scheduling algoritmaları

| Algoritma | Seçim mantığı | Güçlü yanı | Temel sorunu |
|---|---|---|---|
| FCFS | İlk gelen önce çalışır | Basit ve düşük maliyetli | Convoy effect |
| SJF | En kısa iş seçilir | Ortalama beklemeyi azaltır | Süreyi önceden bilmek zordur |
| Priority | En yüksek öncelik seçilir | Kritik işler hızlı çalışır | Starvation oluşabilir |
| Round Robin | Her işe zaman dilimi verir | Adil ve etkileşimli sistemlere uygun | Fazla context switch |
| MLFQ | İşleri farklı kuyruklara taşır | Davranışa uyum sağlar | Ayarlanması karmaşıktır |

### FCFS ve SJF

**First Come, First Served**, banka kuyruğu gibi davranır. Ancak öndeki process çok uzunsa arkadaki kısa işler bekler; buna **convoy effect** denir.

**Shortest Job First** ise kısa işleri öne geçirerek ortalama bekleme süresini düşürür. Ne var ki scheduler geleceği göremez. CPU burst süresi genellikle geçmiş davranıştan üstel ortalamayla tahmin edilir:

$$
\tau_{n+1} = \alpha t_n + (1-\alpha)\tau_n
$$

Burada $t_n$ son gerçek süreyi, $\tau_n$ önceki tahmini temsil eder.

### Round Robin simülasyonu

Aşağıdaki Python kodu, process’lere sırayla belirli bir **quantum** kadar CPU zamanı verir:

```python
from collections import deque

def round_robin(processes, quantum):
    queue = deque(processes)
    elapsed = 0

    while queue:
        name, remaining = queue.popleft()
        used = min(quantum, remaining)
        remaining -= used
        elapsed += used

        print(f"{name}: {used} birim çalıştı, zaman={elapsed}")

        if remaining > 0:
            queue.append((name, remaining))
        else:
            print(f"{name} tamamlandı")

round_robin([("P1", 5), ("P2", 3), ("P3", 7)], quantum=2)
```

Kod, kuyruğun başındaki process’i alır, en fazla iki zaman birimi çalıştırır ve bitmediyse kuyruğun sonuna ekler. Böylece hiçbir process CPU’yu sonsuza kadar işgal edemez.

## Peki CPU zamanını gerçekten kim hak ediyor?

Tek bir kusursuz algoritma yoktur. Sunucularda throughput, masaüstünde response time, gerçek zamanlı sistemlerde ise deadline önemlidir. Modern işletim sistemleri bu nedenle tek bir basit kural yerine öncelik, geçmiş CPU kullanımı ve etkileşimli davranış gibi verileri birleştirir.

İyi scheduler, CPU’yu en çok isteyen process’e değil, sistem hedeflerine göre **en uygun** process’e verir. Yani mesele hak etmekten çok; adalet, hız ve maliyet arasında akıllıca pazarlık yapmaktır.
