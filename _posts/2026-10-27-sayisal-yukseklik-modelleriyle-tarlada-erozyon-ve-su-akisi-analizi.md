---
layout: post
title: "Sayısal Yükseklik Modelleriyle Tarlada Erozyon ve Su Akışı Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - sayısal yükseklik modeli
  - dem
  - arazi analizi
  - erozyon
  - su akışı
  - coğrafi bilgi sistemleri
  - python
toc: true
image: /img/sayisal-yukseklik-modelleriyle-30.png
---

![sayisal-yukseklik-modelleriyle-30](/img/sayisal-yukseklik-modelleriyle-30.svg)


Bir tarla uzaktan bakıldığında dümdüz görünebilir; ancak birkaç santimetrelik yükselti farkları bile yağmur suyunun yönünü, birikeceği noktaları ve toprağı nerede aşındıracağını değiştirebilir. Sayısal Yükseklik Modeli, yani DEM, bu görünmez topografik ayrıntıları hücrelerden oluşan sayısal bir yüzeye dönüştürerek çiftçilere ve arazi uzmanlarına adeta tarlanın su haritasını sunar.

``

## Sayısal Yükseklik Modeli nedir?

DEM, arazinin belirli aralıklarla ölçülmüş yükseklik değerlerini içeren bir raster veri kümesidir. Raster üzerindeki her hücre bir konumu, hücre değeri ise o konumun deniz seviyesine göre yüksekliğini temsil eder. Veriler uydu radarından, LiDAR ölçümlerinden, dron fotogrametrisinden veya arazi ölçümlerinden üretilebilir.

Tarım uygulamalarında yalnızca yükseklik değerlerine bakılmaz. DEM işlenerek eğim, bakı, akış yönü, akış birikimi ve havza sınırları gibi yeni katmanlar oluşturulur.

| Türetilen veri | Cevapladığı soru | Tarımsal kullanım |
|---|---|---|
| Eğim | Arazi ne kadar dik? | Erozyon riskini belirleme |
| Bakı | Yamaç hangi yöne bakıyor? | Nem ve güneşlenme analizi |
| Akış yönü | Su hangi komşu hücreye gider? | Drenaj hattı çıkarma |
| Akış birikimi | Bir noktaya ne kadar alan su taşır? | Su yollarını bulma |
| Çukurluklar | Su nerede hapsolur? | Su baskını ve göllenme tahmini |

## Eğim ve su hareketinin matematiği

Bir yüzeyin eğimi, yüksekliğin yatay yöndeki değişiminden hesaplanır. Hücre boyutu $d$, doğu-batı yönündeki yükseklik değişimi $\Delta z_x$ ve kuzey-güney değişimi $\Delta z_y$ ise eğim yaklaşık olarak şöyle ifade edilir:

$$S = \sqrt{\left(\frac{\Delta z_x}{d}\right)^2 + \left(\frac{\Delta z_y}{d}\right)^2}$$

$S$ büyüdükçe suyun akış hızı ve toprağı taşıma potansiyeli genellikle artar. Ancak toprak türü, bitki örtüsü ve yüzey pürüzlülüğü de sonucu etkiler. Killi bir zemin ile yoğun bitki örtüsüne sahip bir yüzey aynı eğimde farklı davranabilir.

Akış yönü için yaygın D8 yöntemi, her hücredeki suyu çevresindeki sekiz komşudan en dik aşağı eğime sahip olana gönderir. Akış birikimi ise hücreye yukarı havzadan ulaşan hücrelerin sayısını toplar. Böylece yüksek birikim değerleri doğal drenaj kanallarını ortaya çıkarır.

## Erozyon riski nasıl tahmin edilir?

Yaygın RUSLE yaklaşımı yıllık toprak kaybını şu denklemle kestirir:

$$A = R \times K \times LS \times C \times P$$

Burada $R$ yağış aşındırıcılığı, $K$ toprağın erozyona duyarlılığı, $LS$ eğim uzunluğu ve dikliği, $C$ bitki örtüsü, $P$ ise koruyucu uygulama faktörüdür. DEM özellikle $LS$ faktörünün hesaplanmasında kullanılır. Dik ve uzun yamaçlar daha yüksek risk puanı alırken teraslama veya şeritvari ekim gibi uygulamalar $P$ değerini azaltabilir.

## Python ile temel eğim hesabı

Aşağıdaki örnek, bir DEM dosyasını okuyarak yükseklik yüzeyinin gradyanını ve yüzde eğimini hesaplar:

```python
import rasterio
import numpy as np

with rasterio.open('tarla_dem.tif') as src:
    dem = src.read(1).astype(float)
    profile = src.profile
    cell_size = src.res[0]

# İki eksendeki yükseklik değişimini hesaplar
dz_dy, dz_dx = np.gradient(dem, cell_size)

# Gradyandan yüzde eğim üretir
slope_percent = np.sqrt(dz_dx**2 + dz_dy**2) * 100

profile.update(dtype='float32', count=1)
with rasterio.open('egim_yuzde.tif', 'w', **profile) as dst:
    dst.write(slope_percent.astype('float32'), 1)
```

Üretilen raster, yüksek eğimli bölgeleri harita üzerinde göstermek için sınıflandırılabilir. Örneğin yüzde 0–2 düşük, 2–6 orta, 6 üzeri ise arazi koşullarına bağlı olarak yüksek risk kabul edilebilir.

## Sonuçları tarlada kullanmak

Analiz sonunda suyun yoğunlaştığı hatlara çimenli su yolları kurulabilir, göllenme alanlarına drenaj planlanabilir ve yüksek erozyonlu yamaçlarda toprak işleme yönü değiştirilebilir. Bununla birlikte DEM çözünürlüğü kritik önemdedir: 30 metrelik uydu verisi bölgesel inceleme için yeterliyken küçük bir tarla için dronla üretilmiş santimetre veya desimetre çözünürlüklü model daha anlamlıdır.

DEM tek başına geleceği söyleyen sihirli bir küre değildir; fakat yağış, toprak ve bitki örtüsü verileriyle birleştiğinde suyun tarlada çıkacağı yolculuğu güçlü biçimde tahmin eder. Böylece müdahale, toprak kaybolduktan sonra değil, ilk damla düşmeden önce planlanabilir.
