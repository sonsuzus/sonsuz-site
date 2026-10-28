---
layout: post
title: "Mikroskobik Görüntülerde Otomatik Hücre Sayımı ve Segmentasyon"
math: true
categories: 
  - Proje
tags: 
  - görüntü işleme
  - hücre sayımı
  - segmentasyon
  - opencv
  - python
  - bilgisayarlı görü
toc: true
image: /img/mikroskobik-goruntulerde-otomatik-13.png
---

Mikroskop altında kan hücrelerini tek tek saymak, sabır isteyen ve insan hatasına açık bir işlemdir. Neyse ki görüntü işleme algoritmaları; eritrosit, lökosit ve trombosit gibi hücreleri arka plandan ayırabilir, sınırlarını belirleyebilir ve saniyeler içinde sayabilir. Bu süreç yalnızca “resimdeki daireleri bulmak” değildir; aydınlatma farklılıkları, üst üste binen hücreler ve boyama artefaktlarıyla mücadele eden çok aşamalı bir analiz problemidir.

``

## Segmentasyon neden gereklidir?

Segmentasyon, görüntüdeki her pikselin hücreye mi yoksa arka plana mı ait olduğuna karar verme işlemidir. Gri tonlu bir görüntü matematiksel olarak $I(x,y)$ yoğunluk fonksiyonuyla temsil edilebilir. En basit yaklaşımda bir eşik değeri $T$ seçilir:

$$
M(x,y)=\begin{cases}
1, & I(x,y) < T \\
0, & I(x,y) \geq T
\end{cases}
$$

Burada $M$, ikili hücre maskesidir. Kan hücreleri arka plandan daha koyu görünüyorsa eşikten küçük pikseller hücre kabul edilir. Ancak sabit eşik, düzensiz aydınlatmada başarısız olabilir. Otsu yöntemi, sınıf içi varyansı küçülten eşiği otomatik seçer; adaptif eşikleme ise görüntünün farklı bölgeleri için farklı eşikler hesaplar.

| Yöntem | Güçlü yanı | Zayıf yanı | Uygun senaryo |
|---|---|---|---|
| Sabit eşik | Çok hızlıdır | Işığa duyarlıdır | Kontrollü çekimler |
| Otsu | Otomatik eşik seçer | Histogram örtüşürse zorlanır | Homojen arka plan |
| Adaptif eşik | Yerel ışık değişimini yönetir | Gürültüyü büyütebilir | Düzensiz aydınlatma |
| Derin öğrenme | Karmaşık hücreleri tanır | Etiketli veri ve GPU ister | Klinik ölçekli sistemler |

![mikroskobik-goruntulerde-otomatik-13](/img/mikroskobik-goruntulerde-otomatik-13.svg)


## İşlem hattı nasıl çalışır?

Tipik bir hücre sayım sistemi şu adımları izler:

1. **Ön işleme:** Görüntü yeniden boyutlandırılır, gri tona çevrilir ve Gauss filtresiyle gürültü azaltılır.
2. **Segmentasyon:** Otsu, adaptif eşikleme veya renk uzayı analiziyle hücre maskesi üretilir.
3. **Morfolojik düzeltme:** Açma işlemi küçük lekeleri temizler; kapama işlemi hücre içindeki boşlukları doldurur.
4. **Hücreleri ayırma:** Birbirine temas eden hücreler distance transform ve watershed algoritmasıyla ayrılır.
5. **Sayım:** Bağlı bileşenler veya konturlar bulunur; alanı makul aralıkta olan nesneler hücre kabul edilir.

İkili maskede hücre alanı, hücreye ait piksellerin toplamıdır:

$$A=\sum_{x,y}M(x,y)$$

Bir konturun alanı $A$, çevresi $P$ ise dairesellik $C=\frac{4\pi A}{P^2}$ ile ölçülebilir. Kusursuz çemberde $C=1$ olur. Böylece uzun çizikler veya boya kalıntıları hücrelerden ayrılabilir.

## Python ve OpenCV ile örnek sayım

Aşağıdaki kod, hücreleri koyu nesneler olarak kabul eder. Gürültüyü temizler, dış konturları bulur ve çok küçük parçaları sayım dışında bırakır:

```python
import cv2
import numpy as np

image = cv2.imread("kan_ornegi.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Koyu hücreleri beyaz maskeye dönüştürür.
_, mask = cv2.threshold(
    blurred, 0, 255,
    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)

# Küçük gürültüleri morfolojik açma ile temizler.
kernel = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

contours, _ = cv2.findContours(
    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

cells = []
for contour in contours:
    area = cv2.contourArea(contour)
    if 150 < area < 5000:
        cells.append(contour)
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

print(f"Tahmini hücre sayısı: {len(cells)}")
cv2.imwrite("sonuc.jpg", image)
```

Alan sınırları mikroskobun büyütmesine ve görüntü çözünürlüğüne göre kalibre edilmelidir. Sabit `150` değeri her laboratuvar görüntüsünde sihirli biçimde çalışmaz; ne yazık ki algoritmaların da mikroskop ayarı vardır!

## Üst üste binen hücreler ve doğrulama

Basit kontur sayımı, temas eden üç hücreyi tek nesne sanabilir. Watershed yaklaşımı, distance transform üzerindeki yerel tepeleri hücre merkezleri olarak kullanıp birleşik bölgeleri ayırır. Daha karmaşık örneklerde U-Net veya Mask R-CNN gibi modeller, piksel düzeyinde segmentasyon sağlayabilir.

Sistemin başarısı yalnızca tahmini sayıya bakılarak ölçülmemelidir. Uzman tarafından hazırlanmış gerçek maske ile karşılaştırma yapılabilir. Kesişim-birleşim oranı

$$IoU=\frac{\vert M_{tahmin}\cap M_{gerçek}\vert }{\vert M_{tahmin}\cup M_{gerçek}\vert }$$

şeklindedir. Ayrıca sayım hatası için $MAE=\frac{1}{n}\sum \vert y_i-\hat{y}_i\vert $ kullanılabilir. Yüksek IoU doğru sınırları, düşük MAE ise doğru hücre sayısını gösterir. Böylece sistem sadece hızlı değil, ölçülebilir biçimde güvenilir hâle gelir.
