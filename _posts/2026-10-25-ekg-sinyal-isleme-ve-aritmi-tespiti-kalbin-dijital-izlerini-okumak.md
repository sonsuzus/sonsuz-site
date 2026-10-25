---
layout: post
title: "EKG Sinyal İşleme ve Aritmi Tespiti: Kalbin Dijital İzlerini Okumak"
math: true
categories: 
  - Bilgi
tags: 
  - ekg
  - sinyal işleme
  - aritmi
  - python
  - biyomedikal
  - makine öğrenmesi
toc: true
image: /img/ekg-sinyal-isleme-60.png
---

Kalp, elektriksel darbelerle çalışan etkileyici bir pompa; EKG ise bu darbelerin zamana karşı çizilmiş hikâyesidir. Ne var ki ham EKG verisi, kas hareketleri, elektrot teması ve şebeke gürültüsü nedeniyle her zaman tertemiz görünmez. Sayısal sinyal işleme teknikleri bu karmaşayı temizleyerek kalp atımlarını bulmamızı, ritmi ölçmemizi ve olası aritmileri işaretlememizi sağlar.

``

## EKG dalgası bize ne anlatır?

Tipik bir EKG çevrimi P dalgası, QRS kompleksi ve T dalgasından oluşur. P dalgası kulakçıkların, QRS kompleksi karıncıkların depolarizasyonunu; T dalgası ise karıncıkların toparlanmasını temsil eder. Aritmi tespitinde özellikle yüksek ve keskin **R tepeleri** önemlidir. Ardışık iki R tepesi arasındaki süreye RR aralığı denir.

RR aralığı saniye cinsindense yaklaşık kalp hızı şöyle hesaplanır:

$$BPM = 60 / RR$$

Örneğin RR aralığı $0.8$ saniye olduğunda kalp hızı $75$ BPM olur. Ancak yalnızca BPM yeterli değildir. Atımlar arasındaki düzensizlik, QRS genişliği ve beklenmeyen erken vuruşlar da incelenmelidir.

| Özellik | Normal beklenti | Olası anormallik işareti |
|---|---|---|
| Kalp hızı | 60–100 BPM | Bradikardi veya taşikardi |
| RR aralığı | Görece düzenli | Atriyal fibrilasyon gibi düzensizlikler |
| QRS süresi | Genellikle 120 ms'den kısa | İletim bozukluğu veya ventriküler atım |
| Erken vuruş | Beklenmez | Prematüre kasılma |

## Önce gürültüyü susturalım

Bir EKG sistemi, analog sinyali $f_s$ örnekleme frekansıyla sayısallaştırır. Nyquist ilkesine göre incelenmek istenen en yüksek frekans $f_{max}$ ise $f_s > 2f_{max}$ olmalıdır. Uygulamada 250 Hz veya 500 Hz gibi hızlar sık kullanılır.

Ham sinyalde üç yaygın sorun bulunur: yavaş taban çizgisi kayması, yüksek frekanslı kas gürültüsü ve 50/60 Hz elektrik şebekesi paraziti. Bunlar sırasıyla yüksek geçiren, alçak geçiren ve çentik filtrelerle azaltılabilir.

| Filtre | Bastırdığı bileşen | EKG'deki amacı |
|---|---|---|
| Yüksek geçiren | Çok düşük frekanslar | Taban çizgisi kaymasını giderme |
| Alçak geçiren | Yüksek frekanslar | Kas ve ölçüm gürültüsünü azaltma |
| Çentik | Dar bir frekans bandı | 50/60 Hz şebeke parazitini bastırma |
| Bant geçiren | Belirli aralık dışı | QRS kompleksini belirginleştirme |

Basit bir sonlu dürtü yanıtlı filtrenin çıkışı şu biçimdedir:

$$y[n] = \sum_{k=0}^{M} b_k x[n-k]$$

Burada $x[n]$ ham EKG'yi, $b_k$ filtre katsayılarını, $y[n]$ ise temizlenmiş sinyali temsil eder.

## Python ile R tepelerini yakalamak

Aşağıdaki örnek, EKG'yi bant geçiren filtreyle temizler ve R tepelerini bulur. `distance` parametresi, fizyolojik olarak imkânsız derecede yakın tepelerin seçilmesini önler.

```python
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

fs = 250  # Örnekleme frekansı

def bandpass(ecg, low=5, high=20):
    nyquist = fs / 2
    b, a = butter(4, [low / nyquist, high / nyquist], btype='band')
    return filtfilt(b, a, ecg)

filtered = bandpass(ecg)
threshold = np.mean(filtered) + 0.8 * np.std(filtered)
peaks, _ = find_peaks(
    filtered,
    height=threshold,
    distance=int(0.25 * fs)
)

rr = np.diff(peaks) / fs
bpm = 60 / rr
print('Ortalama BPM:', np.mean(bpm))
```

Bu yaklaşım öğretici olsa da gerçek verilerde ters QRS kompleksleri veya hareket artefaktları nedeniyle uyarlanabilir eşikler gerekebilir. Pan–Tompkins algoritması; bant geçiren filtreleme, türev alma, karesini hesaplama ve hareketli pencere integrasyonu adımlarını birleştirerek daha dayanıklı R tepesi tespiti sunar.

## Aritmi kararı nasıl verilir?

Kural tabanlı sistem, BPM ve RR değişkenliğine eşikler uygulayabilir. Daha gelişmiş sistemlerde RR istatistikleri, QRS süresi, dalga morfolojisi ve frekans özellikleri bir özellik vektörüne dönüştürülür. Ardından SVM, rastgele orman veya sinir ağı kullanılarak normal ritim ile aritmi sınıflandırılır.

Yine de algoritmanın verdiği sonuç tıbbi tanı değildir. Model; farklı yaş grupları, cihazlar ve hasta kayıtları üzerinde doğrulanmalı, duyarlılık ve özgüllük birlikte değerlendirilmelidir. Kısacası bilgisayar kalbin ritmini dikkatle dinler, fakat son sözü klinik uzmanlık söyler.

![ekg-sinyal-isleme-60](/img/ekg-sinyal-isleme-60.svg)

