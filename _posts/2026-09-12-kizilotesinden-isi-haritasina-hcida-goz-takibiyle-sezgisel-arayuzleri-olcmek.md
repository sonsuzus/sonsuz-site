---
layout: post
title: "Kızılötesinden Isı Haritasına: HCI’da Göz Takibiyle Sezgisel Arayüzleri Ölçmek"
math: true
categories: 
  - Bilgi
tags: 
  - hcı
  - göz takibi
  - kullanıcı deneyimi
toc: true
---

Bir kullanıcı arayüzündeki parlak “Satın Al” düğmesine bakmıyorsa sorun kullanıcıda mı, tasarımcıda mı? İnsan-Bilgisayar Etkileşimi (HCI) araştırmalarında göz takibi, bu tartışmayı tahminlerden çıkarıp ölçülebilir verilere dönüştürür. Kızılötesi tabanlı cihazlar, kullanıcının ekranda nereye ve ne kadar süre baktığını belirleyerek dikkat dağılımını ısı haritaları üzerinde görünür hâle getirir.

``

## Kızılötesi göz takibi nasıl çalışır?

Göz takip cihazı, göze insanın göremediği yakın kızılötesi ışık gönderir. Kamera, korneadaki ışık yansımasını ve göz bebeğinin merkezini algılar. Göz bebeği ile kornea yansıması arasındaki geometrik ilişki, bakış yönünün hesaplanmasını sağlar. Kullanıcıdan ekran üzerindeki belirli noktalara bakmasının istendiği **kalibrasyon**, bu yönü ekran koordinatlarına dönüştüren modeli kişiselleştirir.

Basitleştirilmiş bakış tahmini şöyle ifade edilebilir:

$$
(x_s, y_s) = f(x_p, y_p, x_c, y_c)
$$

Burada $(x_p,y_p)$ göz bebeği merkezini, $(x_c,y_c)$ kornea yansımasını, $(x_s,y_s)$ ise ekrandaki tahmini bakış noktasını temsil eder. $f$ fonksiyonu kalibrasyon sırasında öğrenilen geometrik veya makine öğrenmesi tabanlı dönüşümdür.

Ham bakış noktaları tek başına yeterli değildir. HCI araştırmacıları bunları iki temel göz hareketine ayırır:

| Kavram | Özellik | Arayüz açısından anlamı |
|---|---|---|
| Fiksasyon | Gözün kısa süreyle bir bölgede kalması | Bilginin işlendiğini veya kullanıcının zorlandığını gösterebilir |
| Sakkad | İki fiksasyon arasındaki hızlı hareket | Dikkatin öğeler arasında nasıl taşındığını gösterir |
| Göz kırpma | Geçici veri kaybı | Yorgunlukla ilişkili olabilir; dikkatle filtrelenmelidir |

## Isı haritası nasıl oluşur?

Her bakış örneği ekran üzerinde bir koordinattır. Bu noktalara genellikle Gauss çekirdeği uygulanır; yakın noktaların etkileri birleşerek yoğunluk alanı oluşturur:

$$
H(x,y)=\sum_{i=1}^{n} w_i\exp\left(-\frac{(x-x_i)^2+(y-y_i)^2}{2\sigma^2}\right)
$$

$w_i$ fiksasyon süresini, $\sigma$ ise yayılma genişliğini belirler. Kırmızı alanlar yüksek, mavi alanlar düşük görsel dikkati temsil eder. Ancak kırmızı her zaman “iyi” değildir: Kullanıcı hata mesajına uzun süre bakıyorsa mesaj dikkat çekmiş olabilir, fakat anlaşılmamış da olabilir.

Aşağıdaki Python örneği, fiksasyonları sürelerine göre ağırlıklandırarak basit bir ısı haritası üretir:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# x, y ve milisaniye cinsinden fiksasyon süresi
fixations = [(220, 140, 180), (225, 145, 420),
             (700, 500, 250), (710, 505, 300)]

heatmap = np.zeros((600, 800), dtype=float)

for x, y, duration in fixations:
    heatmap[y, x] += duration

# Ayrık noktaları okunabilir yoğunluk bölgelerine dönüştürür.
heatmap = gaussian_filter(heatmap, sigma=25)

plt.imshow(heatmap, cmap="jet", origin="upper")
plt.colorbar(label="Ağırlıklı dikkat yoğunluğu")
plt.axis("off")
plt.show()
```

## Sezgisellik bilimsel olarak nasıl sınanır?

Sadece renkli bir haritaya bakıp karar vermek bilimsel değildir. Önceden hipotez kurulmalı, görevler tanımlanmalı ve **ilgi alanları** (AOI) belirlenmelidir. Örneğin “Kullanıcılar ödeme düğmesini beş saniye içinde fark eder” hipotezi şu metriklerle değerlendirilebilir:

| Metrik | Daha sezgisel tasarım beklentisi |
|---|---|
| İlk fiksasyona kadar geçen süre | Daha kısa |
| Görevi tamamlama süresi | Daha kısa |
| Hatalı tıklama sayısı | Daha az |
| AOI üzerindeki fiksasyon oranı | Kritik öğelerde daha yüksek |
| Geri dönüş sayısı | Genellikle daha az |

Mevcut ve yeni tasarım, benzer kullanıcı gruplarına dengeli sırayla gösterilebilir. Sonuçlar eşleştirilmiş t-testi, Wilcoxon testi veya karma etkili modellerle karşılaştırılabilir. Etki büyüklüğü ve güven aralığı da raporlanmalıdır; yalnızca $p<0.05$ görmek tasarım zaferi ilan etmek için yeterli değildir.

Göz takibi zihni doğrudan okumaz; bakılan öğenin sevildiğini ya da anlaşıldığını tek başına kanıtlayamaz. Kalibrasyon hataları, gözlükler, ekran boyutu ve kullanıcı deneyimi sonuçları etkileyebilir. Bu nedenle göz verileri; görev başarısı, tıklama kayıtları, görüşmeler ve kullanılabilirlik ölçekleriyle birlikte yorumlandığında güçlü bilimsel kanıta dönüşür. Böylece “Bence sezgisel” cümlesinin yerini, ölçülmüş davranış ve tekrarlanabilir deney alır.
