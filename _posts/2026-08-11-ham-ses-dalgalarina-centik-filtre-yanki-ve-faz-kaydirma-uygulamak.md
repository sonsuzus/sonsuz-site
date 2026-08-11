---
layout: post
title: "Ham Ses Dalgalarına Çentik Filtre, Yankı ve Faz Kaydırma Uygulamak"
math: true
categories: 
  - Bilgi
tags: 
  - sinyal işleme
  - dijital ses
  - python
---

Ham bir ses kaydı, zaman içinde ölçülmüş örneklerden oluşan bir dizidir: $x[n]$. Bu diziyi yalnızca dinlemek yerine matematiksel olarak dönüştürmek; örneğin elektrik şebekesi uğultusunu temizlemek, mekânsal yankı eklemek veya stereo algısını değiştirmek mümkündür. Çentik filtre, yankı ve faz kaydırma; sinyal işlemenin frekans, zaman ve faz eksenlerinde nasıl çalıştığını gösteren üç güçlü efekttir.

``

Dijital ses, sürekli zamanlı $x(t)$ dalgasının örneklenmiş hâlidir. Örnekleme frekansı $f_s$ ise, Nyquist kuralına göre temsil edilebilecek en yüksek frekans $f_s/2$ olur. Örneğin 44.100 Hz ile kaydedilen bir sesin teorik üst sınırı 22.050 Hz'dir. Efekt tasarlarken gecikme sürelerini örnek sayısına, hedef frekansları ise normalize açısal frekansa çevirmek gerekir:

$$\omega_0 = 2\pi\frac{f_0}{f_s}$$

| Efekt | Müdahale alanı | Temel hedef | Duyulabilir sonuç |
|---|---|---|---|
| Çentik filtre | Frekans | Çok dar bir bandı bastırmak | Uğultu azalır |
| Yankı | Zaman | Gecikmiş kopya eklemek | Mekân/derinlik hissi |
| Faz kaydırma | Faz ve frekans | Frekansa bağlı faz döndürmek | Hareketli, dalgalı karakter |

## Çentik filtre: İstenmeyen tonu avlamak

Çentik (notch) filtre, belirli bir frekansı mümkün olduğunca azaltırken çevresindeki sesleri korumaya çalışır. En klasik örnek, 50 Hz veya 60 Hz şebeke uğultusudur. İkinci dereceden IIR çentik filtrenin pay kısmı şu yapıdadır:

$$H(z) = \frac{1 - 2\cos(\omega_0)z^{-1} + z^{-2}}{1 - 2r\cos(\omega_0)z^{-1} + r^2z^{-2}}$$

Burada $\omega_0$ hedef frekanstır. Sıfırlar birim çember üzerinde hedef tonu söndürür; kutupları belirleyen $r$ değeri ise çentiğin genişliğini kontrol eder. $r$ değeri 1'e yaklaştıkça filtre daha dar ve seçici olur, fakat sayısal kararlılık ile geçici davranış daha hassas hâle gelir.

## Yankı: Gecikmiş bir kopyayla alan yaratmak

En basit yankı modeli, giriş sinyaline geciktirilmiş ve zayıflatılmış bir sürümünü ekler:

$$y[n] = x[n] + g\,x[n-D]$$

$D$, gecikmenin örnek sayısıdır. 250 ms gecikme için $D = 0.25f_s$ seçilir. $g$ kazancı genellikle $0 < g < 1$ aralığındadır. Tekrar eden yankı için geri besleme kullanılır:

$$y[n] = x[n] + g\,y[n-D]$$

Bu modelde $|g|<1$ şartı önemlidir; aksi takdirde yankı sönmek yerine büyüyebilir. Çıkışın genliği yükseldiğinden, son aşamada kırpılmayı önlemek için normalizasyon yapılmalıdır.

## Faz kaydırma: Genlik aynı, algı farklı

Faz kaydırma, frekans bileşenlerinin zaman hizasını değiştirir. Saf bir sinüs için $x(t)=A\sin(2\pi ft)$ iken fazı $\phi$ kadar kaydırılmış sürüm şöyledir:

$$y(t)=A\sin(2\pi ft+\phi)$$

Tek başına faz değişimi çoğu zaman aynı genlik spektrumunu korur. Ancak özgün sinyalle karıştırıldığında bazı frekanslarda yapıcı, bazılarında yıkıcı girişim oluşur. Phaser efektinin karakteristik taramalı sesi, frekansa bağlı faz kaydıran all-pass filtrelerin karışımından gelir.

| Parametre | Küçük değer | Büyük değer | Pratik not |
|---|---|---|---|
| $r$ | Geniş çentik | Dar çentik | Uğultu için dar ayar tercih edilir |
| $D$ | Kısa ambiyans | Belirgin tekrar | Milisaniyeden örneğe çevrilir |
| $g$ | Hızlı sönüm | Uzun kuyruk | $|g|<1$ korunmalıdır |
| $\phi$ | Hafif fark | Belirgin girişim | Kuru sinyalle karıştırınca etkili |

Aşağıdaki Python örneği, WAV verisine 50 Hz çentik filtre ve basit geri beslemeli yankı uygular. `scipy.signal.iirnotch` katsayıları üretir; `lfilter` ise fark denklemini örnek örnek çalıştırır.

```python
import numpy as np
from scipy.signal import iirnotch, lfilter

fs = 44100
f0, Q = 50.0, 30.0          # Hedef uğultu ve seçicilik
b, a = iirnotch(f0, Q, fs)
temiz = lfilter(b, a, ses)  # ses: -1 ile 1 arası mono NumPy dizisi

delay = int(0.25 * fs)
gain = 0.45
yanki = np.zeros_like(temiz)
for n in range(len(temiz)):
    yankı_gecmisi = yanki[n - delay] if n >= delay else 0.0
    yanki[n] = temiz[n] + gain * yankı_gecmisi

cikis = yanki / max(1.0, np.max(np.abs(yanki)))
```

Faz kaydırma için üretim ortamında all-pass filtre zinciri veya FFT tabanlı faz manipülasyonu tercih edilir. En kritik test ise matematiktir ama son karar kulaktır: Kulaklıkla dinleyin, spektrumu inceleyin ve her parametreyi küçük adımlarla değiştirerek sinyalin neden değiştiğini keşfedin.
