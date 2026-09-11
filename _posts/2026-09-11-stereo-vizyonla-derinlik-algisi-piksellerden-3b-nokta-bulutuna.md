---
layout: post
title: "Stereo Vizyonla Derinlik Algısı: Piksellerden 3B Nokta Bulutuna"
math: true
categories: 
  - Bilgi
tags: 
  - stereo vizyon
  - derinlik algısı
  - otonom sistemler
toc: true
---

İnsanlar çevrelerini iki gözün sunduğu küçük açı farkı sayesinde üç boyutlu algılar. Stereo vizyon sistemleri de benzer bir numara yapar: Aynı sahneyi farklı konumlardaki iki kamerayla görüntüler, ortak pikselleri eşleştirir ve nesnelerin uzaklığını hesaplar. Böylece sıradan görüntüler; robotların, insansız araçların ve otonom makinelerin kullanabileceği geometrik bir çevre modeline dönüşür.

``

## İki Kamera Neden Derinlik Görür?

Yan yana duran kameralarda aynı nesne, görüntü düzlemlerinin farklı yatay konumlarında görünür. Bu konum farkına **disparite** denir. Kameralar arasındaki uzaklık $B$, odak uzaklığı $f$ ve ölçülen disparite $d$ biliniyorsa derinlik yaklaşık olarak şu eşitlikle bulunur:

$$Z = \frac{fB}{d}$$

Formül önemli bir davranışı ortaya çıkarır: Disparite büyüdükçe nesne kameraya yaklaşır; disparite küçüldükçe uzaklaşır. Çok uzaktaki nesnelerde piksel farkı son derece küçük olduğundan hata payı artar. Yani stereo kamera, ufuktaki tabeladan çok önündeki sandalyeyi ölçmekte başarılıdır.

Bir pikselin uzaydaki koordinatları ise kamera merkez noktası $(c_x,c_y)$ kullanılarak hesaplanabilir:

$$X = \frac{(u-c_x)Z}{f}, \qquad Y = \frac{(v-c_y)Z}{f}$$

Buradaki $(u,v)$ görüntü pikselini, $(X,Y,Z)$ ise karşılık gelen üç boyutlu noktayı temsil eder.

## Piksel Eşleştirme Süreci

Ham kamera görüntülerini doğrudan karşılaştırmak genellikle iyi sonuç vermez. Önce kameraların iç parametreleri, lens bozulmaları ve birbirlerine göre konumları **kalibrasyon** ile belirlenir. Ardından görüntüler **rektifikasyon** işleminden geçirilir. Böylece eşleşen noktalar aynı yatay satıra taşınır ve arama iki boyuttan tek boyuta iner.

Algoritma daha sonra sol görüntüdeki bir pikselin sağ görüntüdeki karşılığını arar. Klasik yöntemler küçük görüntü bloklarının benzerliğini ölçerken modern yaklaşımlar özellik çıkaran sinir ağlarından yararlanabilir.

| Yöntem | Güçlü yanı | Zayıf yanı | Uygun kullanım |
|---|---|---|---|
| Block Matching | Çok hızlı ve basit | Gürültülü sonuç üretir | Düşük güçlü robotlar |
| Semi-Global Matching | Dengeli doğruluk | Daha fazla hesaplama ister | Otonom araçlar |
| Derin öğrenme | Zorlu sahnelerde başarılı | GPU ve eğitim verisi ister | Gelişmiş algı sistemleri |

Tekrarlayan desenler, yansıyan yüzeyler, gölgeler ve dokusuz duvarlar eşleştirmeyi zorlaştırır. Örneğin bembeyaz bir duvardaki pikseller birbirine benzediği için algoritma “Bu piksel hangisiydi?” krizine girebilir.

## OpenCV ile Disparite Haritası

Aşağıdaki Python örneği, rektifiye edilmiş iki gri görüntüden Semi-Global Block Matching kullanarak disparite üretir:

```python
import cv2
import numpy as np

left = cv2.imread('left.png', cv2.IMREAD_GRAYSCALE)
right = cv2.imread('right.png', cv2.IMREAD_GRAYSCALE)

stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=128,
    blockSize=5,
    P1=8 * 5 ** 2,
    P2=32 * 5 ** 2,
    uniquenessRatio=10,
    speckleWindowSize=100
)

disparity = stereo.compute(left, right).astype(np.float32) / 16.0
disparity[disparity <= 0] = np.nan

depth = (700.0 * 0.12) / disparity
print('Geçerli derinlik sayısı:', np.isfinite(depth).sum())
```

Burada `700.0` piksel cinsinden odak uzaklığını, `0.12` ise metre cinsinden kamera taban mesafesini temsil eder. Gerçek projelerde bu değerler kalibrasyon sonucundan alınmalıdır. Geçersiz veya negatif disparitelerin temizlenmesi, hayalet noktaların nokta bulutuna karışmasını önler.

## Nokta Bulutundan Çevre Algısına

Her geçerli piksel uzay koordinatına dönüştürüldüğünde renkli veya renksiz bir **nokta bulutu** oluşur. Ancak otonom sistem için milyonlarca nokta tek başına yeterli değildir. Zemin düzlemi ayrılır, noktalar kümelenir ve kümeler araç, yaya ya da engel olarak sınıflandırılır.

| Temsil | Sağladığı bilgi | Tipik görev |
|---|---|---|
| Disparite haritası | Piksel kayması | Derinlik hesaplama |
| Derinlik haritası | Kameraya uzaklık | Çarpışma kontrolü |
| Nokta bulutu | 3B geometri | Haritalama ve planlama |
| İşgal ızgarası | Dolu ve boş alanlar | Güvenli rota üretme |

Otonom araç, nokta bulutundan yol sınırlarını ve yakın engelleri çıkarabilir; mobil robot ise geçebileceği boşlukları belirleyebilir. Stereo vizyon pasif çalıştığı için çevreye lazer göndermez ve maliyeti genellikle LiDAR’dan düşüktür. Buna karşılık karanlık, sis ve düşük dokulu yüzeyler performansı azaltır. Bu nedenle güvenilir sistemler stereo kamerayı LiDAR, radar ve IMU ile birleştirir. Kısacası iki görüntü arasındaki birkaç piksellik fark, doğru geometri ve iyi algoritmalarla robotun dünyayı üç boyutlu “görmesini” sağlar.
