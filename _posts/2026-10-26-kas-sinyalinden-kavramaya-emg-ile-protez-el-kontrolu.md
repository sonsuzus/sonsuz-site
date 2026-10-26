---
layout: post
title: "Kas Sinyalinden Kavramaya: EMG ile Protez El Kontrolü"
math: true
categories: 
  - Bilgi
tags: 
  - emg
  - sinyal işleme
  - protez
  - makine öğrenmesi
  - biyomedikal
  - python
toc: true
image: /img/kas-sinyalinden-kavramaya-79.png
---

Bir bardağı kavramak bize son derece doğal görünür; fakat bu hareketin arkasında sinir sistemi, kaslar ve beynin birlikte yönettiği karmaşık bir iletişim ağı bulunur. EMG kontrollü protez eller, kaslarda oluşan elektriksel etkinliği dinleyerek kullanıcının hareket niyetini tahmin eder. Başka bir deyişle protez, kasların fısıltısını mekanik parmakların anlayabileceği komutlara çevirir.

``

## EMG sinyali nedir?

Elektromiyografi, kas lifleri etkinleştiğinde oluşan elektriksel potansiyellerin ölçülmesidir. Yüzey EMG sistemlerinde elektrotlar deri üzerine yerleştirilir. Kullanıcı elini kapatmayı düşündüğünde ön koldaki ilgili kaslar kasılır ve elektrotlarda mikrovolt ile milivolt seviyeleri arasında değişen bir sinyal oluşur.

Ham EMG genellikle düzensiz, çift yönlü ve gürültülüdür. Bu nedenle sinyal doğrudan motora gönderilemez. Ölçülen veri basitleştirilmiş biçimde

$$x(t)=s(t)+n(t)$$

olarak düşünülebilir. Burada $s(t)$ istenen kas etkinliği, $n(t)$ ise hareket artefaktı, elektronik gürültü ve şebeke paraziti gibi istenmeyen bileşenlerdir.

## Sinyal işleme hattı

Tipik bir protez kontrol sistemi aşağıdaki aşamalardan oluşur:

| Aşama | Amaç | Yaygın yöntem |
|---|---|---|
| Ölçüm | Kas etkinliğini toplamak | Yüzey elektrotları |
| Filtreleme | Gürültüyü azaltmak | Bant geçiren ve çentik filtre |
| Pencereleme | Veriyi kısa bölümlere ayırmak | 150–300 ms kayan pencere |
| Özellik çıkarımı | Sinyali sayısal olarak özetlemek | RMS, MAV, sıfır geçişi |
| Sınıflandırma | Hareket niyetini belirlemek | LDA, SVM, sinir ağı |
| Motor kontrolü | Kararı fiziksel harekete çevirmek | PWM ve geri besleme |

![kas-sinyalinden-kavramaya-79](/img/kas-sinyalinden-kavramaya-79.svg)


EMG enerjisinin önemli bölümü yaklaşık 20–450 Hz aralığındadır. Bant geçiren filtre bu aralığın dışındaki bileşenleri bastırırken, 50 Hz veya 60 Hz çentik filtresi elektrik şebekesinden gelen uğultuyu azaltır.

## Kasılmayı sayıya dönüştürmek

Filtrelenmiş sinyal kısa zaman pencerelerine ayrılır. Her pencere için hesaplanan RMS değeri kasılma şiddetini özetleyebilir:

$$RMS=\sqrt{\frac{1}{N}\sum_{i=1}^{N}x_i^2}$$

Benzer şekilde ortalama mutlak değer, yani MAV,

$$MAV=\frac{1}{N}\sum_{i=1}^{N}\vert x_i\vert $$

ile hesaplanır. RMS büyükse güçlü, küçükse zayıf kasılma olduğu yorumlanabilir. Ancak farklı hareketler benzer enerji üretebildiği için birden fazla elektrot kanalı ve özellik birlikte kullanılır.

Aşağıdaki Python örneği, örnek bir EMG dizisini filtreler ve pencerelerden RMS özellikleri çıkarır:

```python
import numpy as np
from scipy.signal import butter, filtfilt

def bandpass_emg(signal, fs=1000):
    # 20-450 Hz arasındaki kas etkinliğini korur.
    b, a = butter(4, [20, 450], btype="bandpass", fs=fs)
    return filtfilt(b, a, signal)

def rms_features(signal, window_size=200, step=100):
    features = []
    for start in range(0, len(signal) - window_size + 1, step):
        window = signal[start:start + window_size]
        features.append(np.sqrt(np.mean(window ** 2)))
    return np.array(features)

filtered = bandpass_emg(raw_emg)
rms_values = rms_features(filtered)
```

Buradaki 200 örneklik pencere, 1000 Hz örnekleme hızında 200 ms sürer. Pencerelerin örtüşmesi daha sık karar üretilmesini sağlar; ancak çok küçük pencereler kararsız tahminlere, çok büyük pencereler ise hissedilir gecikmeye yol açabilir.

## Karardan harekete

Basit bir sistem RMS eşiğini aşınca eli kapatabilir. Daha gelişmiş sistemlerde farklı hareketlerden toplanmış özelliklerle bir sınıflandırıcı eğitilir. Model; eli açma, kapatma, işaret etme veya bileği döndürme sınıflarından birini seçer. Tahmin güveni düşükse protezin hareket etmemesi güvenli bir seçenek olabilir.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Eşik tabanlı | Hızlı ve anlaşılır | Az sayıda hareket |
| Klasik makine öğrenmesi | Küçük veriyle çalışabilir | Özellik tasarımı gerekir |
| Derin öğrenme | Karmaşık örüntüleri öğrenir | Daha çok veri ve işlem gücü ister |

Son aşamada sınıf etiketi motor sürücüsüne gönderilir. Kuvvet sensörleri de bardağın ezilmesini veya elden kaymasını önleyen geri besleme sağlar. Böylece sistem yalnızca “kapat” demez; ne kadar hızlı ve güçlü kapanacağını da ayarlayabilir.

Başarılı bir protez kontrolünde doğruluk tek hedef değildir. Gecikme, enerji tüketimi, kullanıcı konforu ve elektrotların terleme nedeniyle değişen teması da önemlidir. En iyi sistem, laboratuvarda en yüksek skoru alan değil, günlük yaşamda kullanıcının niyetini hızlı, güvenli ve doğal biçimde harekete dönüştürendir.
