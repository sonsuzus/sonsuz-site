---
layout: post
title: "YOLO Mimarisi: Bilgisayar Görüşünün Tek Bakışta Nesne Avcısı"
math: true
categories: 
  - Bilgi
tags: 
  - yolo
  - bilgisayar görüşü
  - nesne tespiti
toc: true
---

Bir fotoğraftaki kediyi bulmak kolay görünebilir; fakat bilgisayarın aynı anda kediyi, koltuğu ve masayı tanıyıp konumlarını milisaniyeler içinde işaretlemesi ciddi bir problemdir. YOLO, yani *You Only Look Once*, bu problemi görüntüye yalnızca bir kez bakarak çözen hızlı bir nesne tespiti ailesidir. Klasik yöntemlerin aksine önce bölge arayıp sonra sınıflandırma yapmak yerine bütün işlemi tek bir sinir ağı geçişinde tamamlar.

``

## Sınıflandırma Değil, Nesne Tespiti

Görüntü sınıflandırma, resimde baskın olarak ne bulunduğunu söyler. Nesne tespiti ise hem **ne** olduğunu hem de **nerede** bulunduğunu belirler. Dolayısıyla modelin her nesne için bir sınıf etiketi ve sınırlayıcı kutu üretmesi gerekir.

Bir kutu genellikle şu değerlerle temsil edilir:

$$
b = (x, y, w, h, c)
$$

Burada $x$ ve $y$ kutunun merkezini, $w$ genişliğini, $h$ yüksekliğini, $c$ ise güven skorunu ifade eder. YOLO bu değerleri doğrudan görüntü piksellerinden öğrenir; arada elle tasarlanmış bir bölge önerme aşaması yoktur.

| Yaklaşım | İşleyiş | Hız | Tipik özellik |
|---|---|---:|---|
| İki aşamalı modeller | Bölge öner, sonra sınıflandır | Daha düşük | Genellikle yüksek doğruluk |
| YOLO | Kutuları ve sınıfları birlikte tahmin et | Çok yüksek | Gerçek zamanlı çalışmaya uygun |
| Görüntü sınıflandırma | Tek etiket üret | Çok yüksek | Nesnenin yerini göstermez |

## Izgara Mantığı Nasıl Çalışır?

YOLO’nun temel fikrinde görüntü $S \times S$ hücreden oluşan sanal bir ızgaraya ayrılır. Bir nesnenin merkezi hangi hücreye düşüyorsa o hücre nesneyi tahmin etmekten sorumlu olur. Örneğin görüntü $7 \times 7$ ızgaraya bölündüğünde toplam 49 hücre bulunur. Her hücre birden fazla aday kutu, nesne bulunma olasılığı ve sınıf skorları üretebilir.

Bir sınıfa ait yaklaşık güven değeri şöyle düşünülebilir:

$$
P(\text{sınıf}) \times P(\text{nesne}) \times IoU
$$

Buradaki **IoU**, tahmin edilen kutu ile gerçek kutunun ne kadar örtüştüğünü ölçer:

$$
IoU = \frac{\vert B_{tahmin} \cap B_{gerçek}\vert }{\vert B_{tahmin} \cup B_{gerçek}\vert }
$$

IoU değeri 1’e yaklaştıkça kutular daha iyi örtüşür. Aynı nesne için çok sayıda kutu üretildiğinde **Non-Maximum Suppression** işlemi en güçlü kutuyu korur, onunla fazla örtüşen zayıf kutuları eler. Böylece bir köpek ekranda beş farklı dikdörtgenle dolaşmaz.

## Tek Geçiş Neden Hızlıdır?

YOLO, nesne tespitini bir regresyon problemi gibi ele alır. Omurga ağı görüntüden kenar, doku ve şekil özellikleri çıkarır; boyun bölümü farklı ölçeklerdeki özellikleri birleştirir; tespit başlığı ise kutu ve sınıf tahminlerini üretir. Tüm bileşenler birlikte, uçtan uca eğitilir.

Basitleştirilmiş kullanım aşağıdaki gibi olabilir:

```python
from ultralytics import YOLO

# Önceden eğitilmiş modeli yükler.
model = YOLO("yolo11n.pt")

# Görüntüdeki nesneleri tek çağrıyla tespit eder.
results = model("sokak.jpg", conf=0.40)

# Kutuları, sınıfları ve güven skorlarını gösterir.
for result in results:
    result.show()
```

Buradaki `conf=0.40`, güven skoru yüzde 40’ın altında kalan tahminleri filtreler. Eşik yükseltilirse yanlış alarmlar azalabilir; ancak bazı gerçek nesneler de kaçırılabilir.

## Güçlü ve Zayıf Yönler

| Güçlü yön | Sınırlama |
|---|---|
| Kamera akışında gerçek zamanlı tespit | Küçük nesnelerde ayrıntı kaybı yaşanabilir |
| Tek ağ sayesinde sade işlem hattı | Yoğun ve üst üste nesneler zorlayıcıdır |
| GPU, mobil cihaz ve uç sistemlere uyarlanabilir | Hız-doğruluk dengesi model boyutuna bağlıdır |

YOLO; otonom araçlar, güvenlik kameraları, üretim hattı denetimi, tarım ve robotik gibi alanlarda kullanılır. Başarısının sırrı kusursuz bir sihir değil, problemi akıllıca sadeleştirmesidir: görüntüyü tekrar tekrar incelemek yerine tek bakışta kutuları ve sınıfları birlikte tahmin etmek. Kısacası YOLO, bilgisayar görüşünün hızlı çalışan ama kahvesini soğutmayan dedektifidir.
