---
layout: post
title: "Biyolojik Gürültüden Anlamlı Veriye: EEG, EKG ve EMG Sinyalleri Nasıl Temizlenir?"
math: true
categories: 
  - Bilgi
tags: 
  - sinyal işleme
  - eeg
  - ekg
  - emg
  - python
  - biyomedikal
  - filtreleme
toc: true
image: /img/biyolojik-gurultuden-anlamli-50.png
---

Kalbin elektriksel ritmini, beynin düşünürken oluşturduğu dalgaları veya kasların çalışırken ürettiği gerilimleri bilgisayarda görebiliyoruz. Ne var ki elektrotlardan gelen ham EEG, EKG ve EMG kayıtları çoğu zaman tertemiz değildir; şebeke elektriği, hareket, terleme ve hatta göz kırpma bile ölçüme karışır. Tıbbi sinyal işleme, işte bu gürültülü elektrik çorbasından klinik açıdan anlamlı bilgiyi ayırma sanatıdır.

``

## Önce sinyalin matematiği

Bilgisayar, biyolojik sinyali belirli aralıklarla ölçülmüş sayılar dizisi olarak saklar. Sürekli zamanlı $x(t)$ sinyali, örnekleme sonrasında $x[n]$ biçimine dönüşür. Örnekleme frekansı $f_s$ ise iki ölçüm arasındaki süre $T_s = 1/f_s$ olur.

Nyquist ilkesine göre, frekansı $f_{max}$ olan bir bileşeni kaybetmeden yakalayabilmek için $f_s > 2f_{max}$ seçilmelidir. Örneğin 150 Hz'e kadar EMG bileşenleri incelenecekse 300 Hz teorik alt sınırdır; pratikte daha yüksek bir değer kullanılır.

Ham kayıt basitçe şöyle modellenebilir:

$$x[n] = s[n] + g[n] + a[n]$$

Burada $s[n]$ aradığımız biyolojik sinyal, $g[n]$ rastgele gürültü, $a[n]$ ise göz kırpması veya elektrot hareketi gibi artefaktlardır. Amaç her şeyi susturmak değil, $s[n]$ bileşenini bozmadan diğerlerini azaltmaktır.

## Üç sinyal, üç farklı karakter

| Sinyal | Kaynak | Yaklaşık anlamlı bant | Yaygın sorun |
|---|---|---:|---|
| EEG | Beyin etkinliği | 0.5–45 Hz | Göz kırpması, kas hareketi |
| EKG | Kalbin elektriksel etkinliği | 0.5–40 Hz | Baz çizgisi kayması, şebeke gürültüsü |
| EMG | Kas liflerinin etkinliği | 20–450 Hz | Hareket artefaktı, elektrot teması |

Bu farklılık önemlidir: EKG için uygun olan bir filtre, EMG'nin değerli yüksek frekanslarını silebilir. Yani tek bir “sihirli temizleme düğmesi” yoktur.

## Temizleme hattı nasıl kurulur?

İlk adım çoğunlukla **bant geçiren filtredir**. Yüksek geçiren bölüm yavaş baz çizgisi kaymasını, alçak geçiren bölüm ise gereksiz yüksek frekansları azaltır. Ardından 50 Hz veya 60 Hz elektrik şebekesi parazitine karşı dar bir **notch filtresi** uygulanabilir.

| Yöntem | Güçlü yanı | Dikkat edilmesi gereken |
|---|---|---|
| Bant geçiren filtre | İstenen frekansları ayırır | Kesim frekansları bilgi silebilir |
| Notch filtre | Şebeke parazitini bastırır | Yakındaki biyolojik bileşenleri etkileyebilir |
| Medyan filtre | Ani sıçramalara dayanıklıdır | Dalga biçimini değiştirebilir |
| ICA | Karışmış kaynakları ayırabilir | Uzman yorumu ve çok kanallı kayıt ister |
| Wavelet | Zamana göre değişen olaylarda etkilidir | Eşik ve dalgacık seçimi kritiktir |

Özellikle EEG'de göz kırpması birden fazla kanala yayılır. Bağımsız Bileşen Analizi, yani ICA, kayıtları istatistiksel olarak bağımsız kaynaklara ayırmaya çalışır. Göz hareketine benzeyen bileşen çıkarılıp kalanlar yeniden birleştirilebilir. Ancak yanlış bileşeni silmek, beynin gerçek etkinliğini de çöpe atabilir.

## Python ile örnek filtreleme

Aşağıdaki örnek, 250 Hz ile kaydedilmiş bir EKG sinyaline 0.5–40 Hz bant geçiren Butterworth filtresi uygular:

```python
import numpy as np
from scipy.signal import butter, sosfiltfilt

def ekg_temizle(sinyal, fs=250):
    # SOS gösterimi sayısal kararlılığı artırır.
    sos = butter(
        N=4,
        Wn=[0.5, 40],
        btype="bandpass",
        fs=fs,
        output="sos"
    )

    # İleri-geri filtreleme faz kaymasını önler.
    return sosfiltfilt(sos, np.asarray(sinyal))
```

`sosfiltfilt`, filtreyi iki yönde çalıştırarak dalgaların zamanını kaydırmaz. Bu, R tepesinin konumu gibi zamanlamaya bağlı EKG ölçümlerinde değerlidir. Bununla birlikte gerçek zamanlı sistemler gelecekteki örnekleri göremediği için aynı yöntemi doğrudan kullanamaz.

## Temiz sinyal her zaman doğru sinyal değildir

Filtreleme sonrasında ham ve temizlenmiş kayıt mutlaka birlikte karşılaştırılmalıdır. Güç spektrumu, sinyal-gürültü oranı ve klinik dalga biçimleri kontrol edilmelidir. Örneğin sinyal-gürültü oranı $SNR = 10\log_{10}(P_s/P_g)$ ile ifade edilebilir; yükselmesi olumlu görünse de tanısal bir tepenin silinmediğini garanti etmez.

Sonuç olarak başarılı tıbbi sinyal işleme; matematik, biyoloji ve dikkatli doğrulamanın birleşimidir. Amaç grafiği güzel göstermek değil, hastaya ait gerçek bilgiyi güvenilir biçimde korumaktır.

![biyolojik-gurultuden-anlamli-50](/img/biyolojik-gurultuden-anlamli-50.svg)

