---
layout: post
title: "Kalbin Kodunu Çözmek: EKG Sinyallerinden Ritim Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - ekg
  - sinyal işleme
  - yapay zeka
  - python
  - sağlık teknolojileri
toc: true
image: /img/kalbin-kodunu-cozmek-60.png
---

Kalp, elektriksel uyarılarla çalışan biyolojik bir pompadır. Elektrokardiyografi, yani EKG, bu uyarıların vücut yüzeyindeki küçük gerilim değişimlerini kaydeder. Bilgisayar ise dalgalı görünen bu sinyali temizleyip ölçerek normal ritim, taşikardi veya ritim düzensizliği gibi örüntüler arasında ayrım yapmaya çalışır. Kısacası mesele, kalbin çıkardığı elektriksel “müziğin” temposunu ve notalarını analiz etmektir.

``

## EKG sinyalinde ne görüyoruz?

Tipik bir kalp atımı P dalgası, QRS kompleksi ve T dalgasından oluşur. P dalgası kulakçıkların, QRS kompleksi karıncıkların elektriksel aktivasyonunu temsil eder. T dalgası ise karıncıkların elektriksel olarak toparlanmasıyla ilişkilidir.

| Bileşen | Temel anlamı | Analizdeki önemi |
|---|---|---|
| P dalgası | Kulakçık aktivasyonu | Atriyal ritimlerin değerlendirilmesi |
| QRS kompleksi | Karıncık aktivasyonu | Atımın bulunması ve iletim bozuklukları |
| T dalgası | Karıncıkların toparlanması | Repolarizasyon değişikliklerinin incelenmesi |
| R-R aralığı | İki R tepesi arasındaki süre | Nabız ve ritim düzenliliği |

R tepeleri tespit edildiğinde yaklaşık kalp hızı şöyle hesaplanabilir:

$$HR = 60 / RR$$

Burada $RR$ saniye cinsinden iki atım arasındaki süredir. Örneğin $RR = 0.8$ saniyeyse kalp hızı yaklaşık $75$ atım/dakikadır.

## Ham sinyal neden doğrudan kullanılamaz?

EKG kayıtları kusursuz değildir. Solunum, kas hareketleri, elektrot temassızlığı ve elektrik şebekesi sinyale gürültü ekler. Bu nedenle ilk aşama genellikle ön işlemedir.

| Sorun | Sinyaldeki etkisi | Yaygın çözüm |
|---|---|---|
| Bazal çizgi kayması | Sinyalin yavaşça yukarı-aşağı gezinmesi | Yüksek geçiren filtre |
| Şebeke gürültüsü | 50 veya 60 Hz titreşim | Çentik filtresi |
| Kas gürültüsü | Düzensiz, hızlı değişimler | Alçak geçiren filtre |
| Hareket artefaktı | Büyük ve sahte tepeler | Artefakt tespiti, kayıt eleme |

Filtreleme dengeli yapılmalıdır. Çok zayıf filtre gürültüyü bırakırken aşırı güçlü filtre tıbbi açıdan önemli dalgaları bozabilir.

## Bilgisayar atımları nasıl buluyor?

Klasik yöntemler QRS kompleksinin keskinliğinden yararlanır. Sinyalin türevi alınarak hızlı değişimler belirginleştirilir, değerler karesel dönüşümden geçirilir ve hareketli pencereyle enerji hesaplanır. Ardından uyarlanabilir bir eşik, gerçek R tepelerini gürültüden ayırır.

Aşağıdaki Python örneği, filtrelenmiş bir EKG sinyalinde olası R tepelerini bulur:

```python
from scipy.signal import find_peaks
import numpy as np

# ecg: filtrelenmiş EKG dizisi
# fs: saniyedeki örnek sayısı
minimum_distance = int(0.3 * fs)
threshold = np.mean(ecg) + 0.8 * np.std(ecg)

peaks, properties = find_peaks(
    ecg,
    distance=minimum_distance,
    height=threshold
)

rr_intervals = np.diff(peaks) / fs
heart_rates = 60 / rr_intervals
```

`distance` parametresi birbirine fizyolojik olarak fazla yakın tepelerin iki ayrı atım sayılmasını engeller. Eşik ise sinyalin ortalaması ve standart sapmasına göre belirlenir. Gerçek klinik sistemlerde ters QRS kompleksleri, farklı derivasyonlar ve değişken sinyal kalitesi de hesaba katılır.

## Anormallik kararı nasıl veriliyor?

R tepeleri bulunduktan sonra R-R aralıkları, QRS genişliği, dalga şekli ve kalp hızı değişkenliği gibi özellikler çıkarılır. Örneğin R-R sürelerinin belirgin biçimde düzensiz olması bazı ritim bozukluklarıyla ilişkili olabilir. Ancak tek başına düzensizlik kesin tanı anlamına gelmez.

Modern sistemler özellik tabanlı makine öğrenmesi veya ham sinyali işleyen evrişimsel sinir ağları kullanabilir. Model, uzmanlar tarafından etiketlenmiş çok sayıda kayıt üzerinden normal ve anormal örüntüleri öğrenir. Başarı yalnızca doğrulukla değil; duyarlılık, özgüllük ve yanlış alarm oranıyla da ölçülür.

EKG analizi güçlü bir karar destek aracıdır, fakat kayıt kalitesi, hastanın yaşı, ilaçları ve klinik durumu sonucu etkiler. Bu nedenle bilgisayarın çıktısı tanı değil, uzman değerlendirmesine yardımcı olan bir uyarı olarak görülmelidir.

![kalbin-kodunu-cozmek-60](/img/kalbin-kodunu-cozmek-60.svg)

