---
layout: post
title: "Bileğinizdeki Laboratuvar: Giyilebilir Sağlık Teknolojileri Nasıl Ölçüm Yapıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - giyilebilir teknoloji
  - sağlık teknolojileri
  - sensörler
  - akıllı saat
  - veri analizi
  - biyometri
toc: true
image: /img/bileginizdeki-laboratuvar-giyilebilir-43.png
---

Akıllı saatler yalnızca adımlarımızı sayan dijital aksesuarlar değil; ışık, elektrik, hareket ve sıcaklık gibi fiziksel sinyalleri biyolojik verilere dönüştüren küçük laboratuvarlardır. Ancak ekranda gördüğümüz “72 BPM” veya “%98 SpO₂” değerleri doğrudan ölçülmez. Sensörlerden gelen gürültülü sinyaller, algoritmalar ve istatistiksel modeller yardımıyla tahmin edilir.
``

## Işıkla nabız ölçmek: PPG

Saatlerin arkasındaki yanıp sönen yeşil LED’ler, **fotopletismografi (PPG)** yönteminin parçasıdır. LED cilde ışık gönderir; fotodiyot ise geri yansıyan ışığı ölçer. Kalp her attığında damarlardaki kan hacmi değişir. Hemoglobin yeşil ışığı emdiği için yansıma miktarındaki periyodik değişim nabzı ortaya çıkarır.

İki tepe arasındaki süre $\Delta t$ saniye ise kalp atış hızı yaklaşık olarak şöyle hesaplanır:

$$BPM = \frac{60}{\Delta t}$$

Örneğin tepeler arasında $0.8$ saniye varsa sonuç $75$ BPM olur. Ne var ki kol hareketi, ter, dövme, gevşek kayış ve ortam ışığı sinyali bozabilir. Saat bu nedenle ivmeölçer verisini kullanarak hareket kaynaklı parazitleri ayıklamaya çalışır.

## Oksijen, elektrik ve sıcaklık

Kandaki oksijen doygunluğu için kırmızı ve kızılötesi ışık kullanılır. Oksijenli ve oksijensiz hemoglobin bu dalga boylarını farklı oranlarda emer. Cihaz, emilim oranını kalibrasyon modeliyle karşılaştırarak **SpO₂ tahmini** üretir.

Elektrokardiyografi özellikli saatlerdeyse kullanıcı elektrotlara dokunarak elektrik devresini tamamlar. Elde edilen tek derivasyonlu EKG, kalbin elektriksel aktivitesini gösterir. Hastanedeki 12 derivasyonlu cihaz kadar kapsamlı değildir; yine de düzensiz ritim belirtilerinin yakalanmasına yardımcı olabilir.

| Sensör | Ham veri | Tahmin edilen bilgi | Yaygın hata kaynağı |
|---|---|---|---|
| PPG | Yansıyan ışık | Nabız, SpO₂ | Hareket, gevşek temas |
| İvmeölçer | Üç eksenli ivme | Adım, aktivite, uyku | Araç yolculuğu, el hareketi |
| Jiroskop | Açısal hız | Egzersiz biçimi | Yanlış bilek konumu |
| Elektrot | Elektrik potansiyeli | EKG, ritim | Kuru cilt, temas kaybı |
| Termistör | Cilt sıcaklığı | Sıcaklık eğilimi | Oda sıcaklığı, terleme |

## Hareketten adıma, adımdan uykuya

İvmeölçer genellikle $x$, $y$ ve $z$ eksenlerinde örnek toplar. Yön etkisini azaltmak için toplam hareket büyüklüğü hesaplanabilir:

$$a = \sqrt{x^2 + y^2 + z^2}$$

Yerçekimi ve gürültü filtrelendikten sonra belirli eşikleri aşan ritmik tepeler adım olarak yorumlanır. Uyku takibi ise çoğunlukla hareketsizlik, kalp hızı, solunum eğilimi ve kalp hızı değişkenliğini birleştirir. Saat beynin elektriksel aktivitesini ölçmediği için uyku evreleri kesin teşhis değil, algoritmik tahmindir.

Aşağıdaki Python örneği, basitleştirilmiş ivme verisindeki tepeleri sayar:

```python
import numpy as np
from scipy.signal import find_peaks

# Üç eksenli ivmeden hareket büyüklüğünü hesapla
x, y, z = np.loadtxt("ivme.csv", delimiter=",", unpack=True)
magnitude = np.sqrt(x**2 + y**2 + z**2)

# Yerçekimi çevresindeki sapmaları belirginleştir
movement = magnitude - np.mean(magnitude)

# Birbirine çok yakın titreşimleri adım saymamak için mesafe uygula
peaks, _ = find_peaks(movement, height=0.25, distance=20)
print(f"Tahmini adım: {len(peaks)}")
```

Gerçek cihazlar sabit bir eşikten fazlasını kullanır: filtreleme, kişisel kalibrasyon ve makine öğrenmesi modelleri farklı yürüyüş biçimlerini ayırır.

## Ölçüm mü, tahmin mi?

| Tıbbi cihaz | Tüketici tipi giyilebilir cihaz |
|---|---|
| Kontrollü koşullarda doğrulanır | Günlük yaşam kolaylığına odaklanır |
| Klinik yorumla birlikte kullanılır | Eğilim ve farkındalık sağlar |
| Çoklu elektrot veya profesyonel sensör içerir | Boyut ve pil tüketimi sınırlıdır |

Giyilebilir cihazların asıl gücü tek bir ölçümden ziyade **zaman içindeki değişimi** göstermeleridir. Dinlenik nabzın günlerce yükselmesi veya sıcaklık eğiliminin değişmesi anlamlı olabilir. Yine de sensör hatası ile sağlık sorununu ayırmak her zaman kolay değildir. Bu nedenle saat bildirimleri tanı kabul edilmemeli; devam eden veya ciddi belirtilerde sağlık uzmanına başvurulmalıdır. Bileğinizdeki teknoloji iyi bir gözlemci olabilir, fakat henüz doktor önlüğü giymiyor.

![bileginizdeki-laboratuvar-giyilebilir-43](/img/bileginizdeki-laboratuvar-giyilebilir-43.svg)

