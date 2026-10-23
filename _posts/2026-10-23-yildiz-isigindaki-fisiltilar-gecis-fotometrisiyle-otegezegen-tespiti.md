---
layout: post
title: "Yıldız Işığındaki Fısıltılar: Geçiş Fotometrisiyle Ötegezegen Tespiti"
math: true
categories: 
  - Bilgi
tags: 
  - ötegezegen
  - astronomi
  - veri analizi
  - python
  - geçiş fotometrisi
  - ışık eğrisi
  - algoritma
toc: true
image: /img/yildiz-isigindaki-fisiltilar-35.png
---

![yildiz-isigindaki-fisiltilar-35](/img/yildiz-isigindaki-fisiltilar-35.svg)


Bir yıldızın önünden geçen gezegen, yıldız ışığının çok küçük bir bölümünü engeller. Teleskop açısından bu olay, parlaklıkta düzenli aralıklarla tekrarlanan sığ düşüşler olarak görünür. Ancak yıldız lekeleri, cihaz gürültüsü ve veri boşlukları da benzer izler bırakabilir. Geçiş fotometrisinin asıl heyecanı, bu kozmik saklambaç oyununu istatistik ve algoritmalar yardımıyla çözmektir.

``

## Geçiş sinyalinin fiziği

Bir gezegen yıldız diskinin önünden geçtiğinde ölçülen göreli parlaklık azalmasına **geçiş derinliği** denir. Basitçe yıldız ve gezegen disklerini düzgün daireler kabul edersek:

$$
delta \approx \left(\frac{R_p}{R_*}\right)^2
$$

Burada $R_p$ gezegenin, $R_*$ yıldızın yarıçapıdır. Örneğin yarıçapı yıldızın onda biri olan bir gezegen yaklaşık $0.01$, yani yüzde bir parlaklık düşüşü oluşturur. Dünya büyüklüğündeki gezegenlerde bu oran çok daha küçüktür; dolayısıyla hassas ölçüm gerekir.

Algoritma yalnızca düşüşün derinliğini değil, süresini ve tekrar aralığını da inceler. Ardışık geçişlerin arasındaki zaman gezegenin yörünge periyodu $P$ hakkında bilgi verir.

| Özellik | Gezegen geçişi | Gürültü veya yıldız etkinliği |
|---|---|---|
| Tekrarlanma | Yaklaşık periyodik | Genellikle düzensiz |
| Şekil | Simetrik, kutuya benzer | Değişken veya sivri |
| Derinlik | Geçişler arasında benzer | Sıkça değişken |
| Süre | Yörüngeyle uyumlu | Rastlantısal olabilir |

## Ham veriden temiz ışık eğrisine

Analiz; zaman ve akı, yani parlaklık ölçümleriyle başlar. Önce eksik veya geçersiz değerler kaldırılır. Ardından akı medyana bölünerek yıldızın normal parlaklığı yaklaşık 1 yapılır. Teleskobun sıcaklık değişimi ya da yıldızın uzun dönemli etkinliği gibi yavaş eğilimler de çıkarılmalıdır. Bu adıma **detrending** denir.

```python
import numpy as np
from scipy.signal import savgol_filter

# time ve flux teleskoptan alınmış NumPy dizileridir.
valid = np.isfinite(time) & np.isfinite(flux)
time_clean = time[valid]
flux_clean = flux[valid]

normalized = flux_clean / np.median(flux_clean)
trend = savgol_filter(normalized, 301, 2)
flat_flux = normalized / trend
```

Bu kod geçersiz ölçümleri temizler, ışık eğrisini normalize eder ve Savitzky–Golay filtresiyle yavaş değişen eğilimi tahmin eder. Pencere boyutu yanlış seçilirse gerçek geçişler de silinebileceği için beklenen geçiş süresinden belirgin biçimde büyük olmalıdır.

## Periyodik düşüşleri BLS ile aramak

Geçişler sinüs dalgasına benzemez; daha çok kısa süreli kutu biçimli çukurlardır. Bu nedenle yaygın çözüm **Box Least Squares (BLS)** algoritmasıdır. BLS, çok sayıda aday periyodu dener, veriyi o periyoda göre katlar ve hangi kutu modelinin gözlemleri en iyi açıkladığını hesaplar.

Sinyalin güvenilirliği kabaca şu oranla değerlendirilebilir:

$$
SNR = \frac{\delta}{\sigma}\sqrt{N_{in}}
$$

Burada $\sigma$ ölçüm saçılımı, $N_{in}$ ise geçiş içinde kalan veri noktalarının sayısıdır.

```python
from astropy.timeseries import BoxLeastSquares

model = BoxLeastSquares(time_clean, flat_flux)
periods = np.linspace(0.5, 30, 10000)
durations = np.linspace(0.05, 0.3, 10)
result = model.power(periods, durations)

best = np.argmax(result.power)
print('Aday periyot:', result.period[best])
print('Geçiş derinliği:', result.depth[best])
```

Kod, 0,5 ile 30 gün arasındaki periyotları tarar ve en güçlü kutu biçimli sinyali seçer. Bulunan zirve doğrudan gezegen kanıtı değildir; yalnızca incelenmeye değer bir adaydır.

## Yanlış pozitifleri elemek

Tutulmalı çift yıldızlar gezegen geçişlerini taklit edebilir. Bu nedenle tek ve çift numaralı geçişlerin derinlikleri karşılaştırılır. Belirgin fark varsa iki yıldızın karşılıklı tutulması söz konusu olabilir. Geçiş sırasında yıldız görüntüsünün merkezinin kayması da sinyalin yakındaki başka bir yıldızdan geldiğini gösterebilir.

Son aşamada aday periyotla katlanmış ışık eğrisi görselleştirilir, farklı gözlemlerle doğrulanır ve gerekirse tayfsal hız ölçümleri yapılır. Böylece birkaç yüz milyonda birlik parlaklık değişimleri, uzak bir dünyanın yarıçapı ve yörüngesi hakkında bilgi veren güçlü bir astronomik kanıta dönüşür.
