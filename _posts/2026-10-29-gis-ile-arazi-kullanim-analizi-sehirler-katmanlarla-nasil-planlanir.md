---
layout: post
title: "GIS ile Arazi Kullanım Analizi: Şehirler Katmanlarla Nasıl Planlanır?"
math: true
categories: 
  - Bilgi
tags: 
  - gis
  - arazi kullanımı
  - şehir planlama
  - mekânsal analiz
  - python
  - geopandas
toc: true
image: /img/gis-ile-arazi-88.png
---

Bir şehrin nereye doğru büyümesi gerektiğine karar vermek, boş görünen bir araziyi işaretlemekten çok daha karmaşıktır. Zeminin eğimi, ulaşım ağı, nüfus yoğunluğu, tarım alanları, su kaynakları ve afet riskleri aynı anda değerlendirilmelidir. Coğrafi Bilgi Sistemleri (GIS), tüm bu verileri katmanlar hâlinde bir araya getirerek yapılaşma kararlarını ölçülebilir, karşılaştırılabilir ve görsel olarak anlaşılır hâle getirir.
``

## Katman mantığı nedir?

GIS ortamında gerçek dünyanın farklı özellikleri ayrı veri katmanlarında tutulur. Yol ağı bir çizgi katmanı, binalar poligon katmanı, hastaneler nokta katmanı olabilir. Uydu görüntüsü ve yükseklik modeli gibi kesintisiz veriler ise genellikle raster biçimindedir.

| Veri katmanı | Tipik veri modeli | Planlamadaki rolü |
|---|---|---|
| Mevcut binalar | Vektör-poligon | Yapı yoğunluğunu gösterir |
| Ulaşım ağı | Vektör-çizgi | Erişilebilirliği ölçer |
| Sayısal yükseklik modeli | Raster | Eğim ve bakı üretir |
| Taşkın alanları | Raster veya poligon | Riskli bölgeleri dışlar |
| Tarım ve orman alanları | Poligon | Korunacak bölgeleri belirler |
| Nüfus yoğunluğu | Raster veya bölgesel tablo | Hizmet talebini açıklar |

![gis-ile-arazi-88](/img/gis-ile-arazi-88.svg)


Bu katmanların birlikte kullanılabilmesi için aynı koordinat referans sistemine dönüştürülmesi gerekir. Örneğin mesafe ve alan hesabı yapılacaksa derece kullanan coğrafi koordinatlar yerine metre tabanlı uygun bir projeksiyon tercih edilmelidir. Aksi hâlde harita güzel görünürken hesaplar sessizce hatalı sonuç verebilir.

## Uygunluk modeli nasıl kurulur?

Yeni bir konut bölgesi aradığımızı düşünelim. Düz araziler, ana yollara yakın bölgeler ve mevcut altyapıya erişebilen alanlar avantajlıdır. Taşkın riski yüksek, orman niteliğindeki veya aşırı eğimli bölgeler ise elenmelidir.

Her ölçüt ortak bir ölçeğe, örneğin 0 ile 1 arasına normalize edilebilir. Ardından ağırlıklı doğrusal birleşim uygulanır:

$$S = \sum_{i=1}^{n} w_i x_i$$

Burada $S$ toplam uygunluk puanı, $x_i$ normalize edilmiş ölçüt değeri ve $w_i$ karar vericinin belirlediği ağırlıktır. Ağırlıkların toplamı genellikle $\sum w_i = 1$ olacak şekilde düzenlenir. Örnek olarak eğim için 0,30; ulaşım için 0,25; altyapı için 0,25 ve nüfus talebi için 0,20 kullanılabilir.

Ancak yüksek puan, alanın otomatik olarak imara açılması gerektiği anlamına gelmez. Yasal koruma sınırları gibi kesin kısıtlar ayrı bir maske ile uygulanır:

$$S_{son} = S \times M$$

$M$ değeri yasak bölgelerde 0, değerlendirilebilir bölgelerde 1 olur. Böylece çok erişilebilir olsa bile bir sulak alan sonuç listesinden çıkarılır.

## Python ile basit bir mekânsal eleme

Aşağıdaki GeoPandas örneği, aday parsellerden taşkın alanlarıyla kesişenleri çıkarır ve yollara yakın olanları seçer:

```python
import geopandas as gpd

parseller = gpd.read_file("aday_parseller.geojson")
yollar = gpd.read_file("ana_yollar.geojson")
taskin = gpd.read_file("taskin_alani.geojson")

# Tüm katmanları metre tabanlı aynı koordinat sistemine getirir.
hedef_crs = "EPSG:32636"
parseller = parseller.to_crs(hedef_crs)
yollar = yollar.to_crs(hedef_crs)
taskin = taskin.to_crs(hedef_crs)

# Ana yolların çevresinde 1000 metrelik erişim bölgesi oluşturur.
yol_tamponu = yollar.buffer(1000).union_all()

# Yola yakın ve taşkın alanıyla kesişmeyen parselleri belirler.
uygun = parseller[
    parseller.intersects(yol_tamponu)
    & ~parseller.intersects(taskin.union_all())
].copy()

uygun.to_file("uygun_parseller.geojson", driver="GeoJSON")
```

Bu işlem yalnızca ilk elemedir. Sonraki aşamada parsel alanı, eğim ortalaması, toplu taşımaya mesafe ve altyapı maliyeti gibi nitelikler puanlanabilir.

## Harita kararın kendisi değildir

GIS güçlü bir karar destek aracıdır; fakat verinin güncelliği, çözünürlüğü ve kaynağı sonucu doğrudan etkiler. Ayrıca ağırlıklar teknik uzmanlar, yerel yönetimler ve bölge halkıyla birlikte belirlenmelidir. Farklı ağırlık senaryolarını karşılaştıran duyarlılık analizi, hangi kararların sağlam kaldığını gösterir.

Sonuç olarak katmanlı analiz, şehir planlamasını sezgisel bir çizim çalışmasından şeffaf bir değerlendirme sürecine taşır. En iyi harita yalnızca nerede yapılaşılabileceğini değil, neden orada yapılaşmanın daha dengeli olduğunu da açıklayabilen haritadır.
