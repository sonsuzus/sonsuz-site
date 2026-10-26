---
layout: post
title: "Gökyüzünden Bitki Doktorluğu: Drone ile Multispektral Mahsul İzleme"
math: true
categories: 
  - Bilgi
tags: 
  - drone
  - multispektral
  - tarım teknolojileri
  - ndvi
  - görüntü işleme
  - hassas tarım
toc: true
image: /img/gokyuzunden-bitki-doktorlugu-49.png
---

![gokyuzunden-bitki-doktorlugu-49](/img/gokyuzunden-bitki-doktorlugu-49.svg)


Bir tarlaya yalnızca göz hizasından baktığınızda her şey yolunda görünebilir. Oysa bitkiler; susuzluk, hastalık veya besin eksikliği gibi sorunları gözle görülür hâle gelmeden önce ışığı yansıtma biçimleriyle belli eder. Multispektral kameralı drone’lar bu erken sinyalleri havadan yakalayarak çiftçiye adeta teknolojik bir stetoskop sunar.

``

## Multispektral görüntüleme nedir?

İnsan gözü elektromanyetik spektrumun yalnızca görünür bölümünü algılar. Multispektral kameralar ise mavi, yeşil ve kırmızı ışığa ek olarak kırmızı kenar ile yakın kızılötesi bantlarını kaydeder. Her piksel böylece yalnızca bir renk değil, farklı dalga boylarındaki yansıma değerlerinden oluşan küçük bir veri paketi hâline gelir.

Sağlıklı bitkiler fotosentez için kırmızı ışığı yoğun biçimde soğururken hücresel yapıları nedeniyle yakın kızılötesi ışığı güçlü şekilde yansıtır. Stresli bitkilerde bu düzen bozulur. Kamera yaprağın içini doğrudan görmez; fakat yansıma davranışındaki değişim üzerinden sağlık durumuna ilişkin güçlü ipuçları üretir.

| Spektral bant | Yaklaşık dalga boyu | Tarımsal kullanım |
|---|---:|---|
| Mavi | 450 nm | Su ve yüzey özelliklerinin incelenmesi |
| Yeşil | 560 nm | Yaprak canlılığı ve klorofil değerlendirmesi |
| Kırmızı | 668 nm | Klorofil soğurumu ve bitki ayrımı |
| Kırmızı kenar | 717 nm | Erken stres ve azot değişiminin belirlenmesi |
| Yakın kızılötesi | 840 nm | Hücre yapısı, biyokütle ve bitki yoğunluğu |

## NDVI: Tarlanın sağlık puanı

En yaygın bitki indeksi NDVI’dır. Yakın kızılötesi ile kırmızı bant arasındaki farkı, bu iki bandın toplamına oranlar:

$$
NDVI = \frac{NIR - Red}{NIR + Red}
$$

Sonuç teorik olarak $-1$ ile $1$ arasındadır. Yüksek pozitif değerler genellikle yoğun ve sağlıklı bitki örtüsünü, sıfıra yakın değerler çıplak toprağı, negatif değerler ise çoğunlukla suyu veya bitki olmayan yüzeyleri gösterir. Ancak NDVI kesin bir teşhis değildir. Düşük bir değer susuzluk, hastalık, seyrek ekim ya da gölge nedeniyle oluşabilir.

| NDVI aralığı | Genel yorum | Olası eylem |
|---|---|---|
| -1–0 | Su veya bitki dışı yüzey | Alanı sınıflandır |
| 0–0.2 | Çıplak ya da seyrek toprak | Çıkışı kontrol et |
| 0.2–0.5 | Orta yoğunluk veya stres | Yerinde inceleme yap |
| 0.5–1.0 | Yoğun bitki örtüsü | Gelişimi takip et |

## Görüntüden karara giden uçuş

Analiz kaliteli veriyle başlar. Drone uçuşu genellikle düzenli bir ızgara rotasında gerçekleştirilir ve fotoğraflar yüzde 70–80 oranında bindirmeli çekilir. Yazılım bu kareleri eşleştirerek coğrafi konumlu tek bir ortomozaik üretir.

Güneş açısının değişmesi sonuçları etkileyebileceği için uçuş öncesinde yansıtma kalibrasyon paneli görüntülenir. Işık sensörü, bulut geçişlerini kaydeder. Aynı tarlayı farklı tarihlerde karşılaştırmak için uçuş saati, yükseklik, kamera açısı ve hava koşulları mümkün olduğunca sabit tutulmalıdır.

Aşağıdaki Python örneği, hizalanmış kırmızı ve yakın kızılötesi bantlardan NDVI hesaplar:

```python
import numpy as np
import rasterio

with rasterio.open("red.tif") as src:
    red = src.read(1).astype("float32")
    profile = src.profile

with rasterio.open("nir.tif") as src:
    nir = src.read(1).astype("float32")

ndvi = (nir - red) / (nir + red + 1e-6)
ndvi = np.clip(ndvi, -1, 1)

profile.update(dtype="float32", count=1)
with rasterio.open("ndvi.tif", "w", **profile) as dst:
    dst.write(ndvi, 1)
```

Buradaki küçük $10^{-6}$ değeri, toplamın sıfır olduğu piksellerde bölme hatasını önler. `np.clip` ise ölçüm gürültüsünden doğabilecek uç değerleri geçerli aralığa sınırlar. Üretilen GeoTIFF, bir coğrafi bilgi sistemi üzerinde renklendirilerek düşük değerli bölgeleri görünür kılar.

## Harita tek başına reçete değildir

Multispektral analiz; sulama kaçaklarını, zararlı kümelerini, gübreleme farklılıklarını ve düzensiz çıkışı erken gösterebilir. Yine de sensör yalnızca belirtiyi algılar. Kesin neden için yaprak analizi, toprak ölçümü ve yerinde gözlem gerekir. En başarılı yaklaşım, drone haritasını çiftçinin saha deneyimiyle birleştirmektir. Böylece bütün tarlaya aynı işlemi uygulamak yerine yalnızca ihtiyaç duyan bölgelere müdahale edilir; maliyet azalırken verim ve sürdürülebilirlik artar.
