---
layout: post
title: "Robotik Hasat Sistemlerinde Nesne Tanıma ve Meyve Olgunluğu Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - görüntü işleme
  - nesne tanıma
  - yapay zeka
  - tarım teknolojileri
  - python
toc: true
image: /img/robotik-hasat-sistemlerinde-46.png
---

Bir meyve toplama robotu için ağaca bakmak, insanın manav tezgâhına bakmasından çok daha karmaşıktır. Robot; yaprakların arkasındaki meyveleri bulmalı, hangilerinin olgun olduğunu anlamalı ve ezmeden toplayabileceği bir hareket planlamalıdır. Bu süreçte kameralar robotun gözü, görüntü işleme algoritmaları ise deneyimli bir çiftçinin sezgileri gibi çalışır.


![robotik-hasat-sistemlerinde-46](/img/robotik-hasat-sistemlerinde-46.svg)

``

## Robot meyveyi nasıl görür?

Sistem genellikle RGB, derinlik veya multispektral kamera kullanır. RGB kamera renk ve doku bilgisi sağlarken derinlik kamerası meyvenin robota uzaklığını ölçer. Multispektral kameralar ise insan gözünün göremediği yakın kızılötesi bantları inceleyerek meyvenin kimyasal yapısı hakkında ipuçları yakalayabilir.

İlk aşama **nesne tespiti**dir. Görüntü içindeki elma, domates veya çilek gibi hedefler sınırlayıcı kutu ya da piksel maskesiyle belirlenir. YOLO gibi tek aşamalı modeller hızlı çalıştıkları için hareketli robotlarda sık kullanılır. Mask R-CNN gibi bölütleme modelleri ise meyvenin sınırlarını daha hassas çıkarır; ancak daha fazla hesaplama gücü ister.

| Yöntem | Avantajı | Dezavantajı | Uygun kullanım |
|---|---|---|---|
| Renk eşikleme | Hızlı ve ucuzdur | Işıktan kolay etkilenir | Kontrollü seralar |
| YOLO | Gerçek zamanlı tespit yapar | Eğitim verisi gerektirir | Hareketli hasat robotları |
| Mask R-CNN | Hassas meyve maskesi üretir | Hesaplama maliyeti yüksektir | Karmaşık ve örtüşen sahneler |
| Multispektral analiz | İç kaliteyi tahmin edebilir | Kamera maliyeti yüksektir | Hassas olgunluk ölçümü |

## Olgunluk yalnızca renk değildir

Kırmızı bir elmanın olgun olduğu düşünülebilir; fakat güneş ışığı, kamera pozlaması ve meyvenin çeşidi bu varsayımı bozabilir. Bu nedenle sistemler renk, doku, boyut ve spektral yansıma gibi birden fazla özelliği birlikte değerlendirir.

RGB yerine HSV renk uzayı kullanıldığında renk tonu, parlaklıktan kısmen ayrılır. Burada **H** renk tonunu, **S** doygunluğu, **V** ise parlaklığı temsil eder. Basit bir olgunluk skoru şöyle tanımlanabilir:

$$M = w_h H + w_s S + w_t T + w_d D$$

Bu denklemde $T$ doku özelliğini, $D$ tahmin edilen çapı, $w$ değerleri ise her özelliğin önem katsayısını gösterir. Makine öğrenmesi kullanıldığında bu ağırlıklar elle seçilmek yerine veriden öğrenilir. İkili sınıflandırmada modelin olgunluk olasılığı lojistik fonksiyonla hesaplanabilir:

$$P(olgun) = \frac{1}{1 + e^{-z}}$$

Olasılık belirlenen eşiği, örneğin $0.80$ değerini aşarsa robot toplama kararı verir.

## Basit bir renk analizi

Aşağıdaki Python kodu, görüntüdeki kırmızı bölgeleri HSV eşikleme ile ayırır. Bu yaklaşım tek başına endüstriyel çözüm değildir; ancak olgun domates adaylarını hızlıca belirleyen faydalı bir ön işleme adımıdır.

```python
import cv2
import numpy as np

image = cv2.imread('domatesler.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Kırmızı, HSV çemberinin iki ucunda bulunduğu için iki aralık kullanılır.
mask1 = cv2.inRange(hsv, np.array([0, 90, 70]), np.array([10, 255, 255]))
mask2 = cv2.inRange(hsv, np.array([170, 90, 70]), np.array([180, 255, 255]))
mask = cv2.bitwise_or(mask1, mask2)

# Küçük gürültüleri temizleyerek daha kararlı bölgeler oluştururuz.
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

ratio = cv2.countNonZero(mask) / mask.size
print(f'Kırmızı piksel oranı: {ratio:.2%}')
```

Kod, kırmızı piksel oranını verir; fakat yaprak, gölge veya kırmızı bir ekipman yanlış pozitif üretebilir. Bu nedenle pratik sistemlerde sonuç, eğitilmiş bir sinir ağı ve derinlik ölçümüyle doğrulanır.

## Tarladaki gerçek zorluklar

Değişken güneş ışığı, üst üste gelen meyveler, rüzgârla sallanan dallar ve kamera üzerindeki toz model başarımını düşürür. Eğitim veri kümesinde farklı saatler, hava koşulları, çeşitler ve olgunluk seviyeleri bulunmalıdır. Döndürme, parlaklık değiştirme ve yapay gölge ekleme gibi veri artırma teknikleri de modeli dayanıklı hâle getirir.

Son aşamada meyvenin 3B konumu robot koluna aktarılır. Kol, yaklaşma açısını hesaplar; kuvvet sensörüyle sıkma basıncını sınırlar ve meyveyi nazikçe koparır. Böylece nesne tanıma yalnızca “Bu bir meyve mi?” sorusunu değil, “Olgun mu, nerede ve güvenle toplanabilir mi?” sorularını da yanıtlayan bütüncül bir karar mekanizmasına dönüşür.
