---
layout: post
title: "OpenStreetMap, uMap ve Leaflet ile Harita ve Konum Sistemleri"
math: true
categories: 
  - Program
tags: 
  - openstreetmap
  - umap
  - leaflet
  - javascript
  - harita
  - konum
toc: true
image: /img/openstreetmap-umap-ve-88.png
---

Dijital haritalar yalnızca “buradan şuraya nasıl giderim?” sorusunu yanıtlamaz. Mağaza buluculardan afet koordinasyonuna, gezi rotalarından sensör takibine kadar pek çok uygulamanın görünmez kahramanıdır. OpenStreetMap, uMap ve Leaflet üçlüsü sayesinde lisans engellerine takılmadan etkileşimli bir konum sistemi geliştirebiliriz. Üstelik bunun için harita mühendisi şapkası takmamız gerekmiyor!
``
## Üç araç, üç farklı görev

Bu teknolojiler aynı ekosistemde çalışabilse de birbirlerinin alternatifi değildir. **OpenStreetMap (OSM)** topluluk tarafından üretilen coğrafi verileri sağlar. Yollar, binalar, parklar ve ilgi noktaları bu veri tabanında tutulur. **uMap**, OSM tabanlı kişisel haritaları kod yazmadan hazırlamaya yarar. **Leaflet** ise web sayfasında etkileşimli harita oluşturabileceğimiz hafif bir JavaScript kütüphanesidir.

| Araç | Temel görevi | Kod gereksinimi | Uygun kullanım |
|---|---|---:|---|
| OpenStreetMap | Coğrafi veri üretmek ve paylaşmak | Yok / isteğe bağlı | Açık harita verisi |
| uMap | Özel haritayı görsel arayüzle hazırlamak | Yok | Rotalar, etkinlikler, sunumlar |
| Leaflet | Programlanabilir web haritası oluşturmak | JavaScript | Dinamik web uygulamaları |

![openstreetmap-umap-ve-88](/img/openstreetmap-umap-ve-88.svg)


Kısacası OSM mutfaktaki malzemeler, uMap hazır yemek tezgâhı, Leaflet ise tarif üzerinde istediğimiz değişikliği yapabildiğimiz şef bıçağıdır.

## Konum bilgisinin matematiği

Dünya üzerindeki bir nokta genellikle enlem ve boylam çiftiyle ifade edilir:

$$P = (\varphi, \lambda)$$

Burada $\varphi$ enlemi, $\lambda$ ise boylamı temsil eder. Enlem kuzey-güney, boylam doğu-batı konumunu belirtir. Leaflet koordinatları çoğunlukla `[enlem, boylam]` sırasıyla bekler. GeoJSON standardında ise sıra `[boylam, enlem]` biçimindedir. Bu küçük fark, işaretçinizin İstanbul yerine okyanusta yüzmesine neden olabilecek kadar önemlidir.

İki konum arasındaki kuş uçuşu mesafe, küresel Dünya yaklaşımında Haversine formülüyle hesaplanabilir:

$$a=\sin^2(\Delta\varphi/2)+\cos(\varphi_1)\cos(\varphi_2)\sin^2(\Delta\lambda/2)$$

$$d=2R\arcsin(\sqrt{a})$$

$R$ yaklaşık $6371$ kilometredir. Yol mesafesi içinse yolların bağlantılarını içeren bir rota motoruna ihtiyaç duyulur; düz çizgi her zaman kullanılabilir bir cadde değildir.

## Leaflet ile ilk etkileşimli harita

Önce sayfaya Leaflet CSS ve JavaScript dosyaları eklenmeli, ardından haritanın yerleşeceği elemana yükseklik verilmelidir. Aşağıdaki örnek İstanbul merkezli bir harita oluşturur:

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css">
<div id="map" style="height: 420px"></div>
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
  const map = L.map('map').setView([41.0082, 28.9784], 12);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap katkıda bulunanlar'
  }).addTo(map);

  const marker = L.marker([41.0082, 28.9784]).addTo(map);
  marker.bindPopup('<strong>İstanbul</strong><br>Harita burada başlıyor!');

  map.on('click', event => {
    L.popup()
      .setLatLng(event.latlng)
      .setContent(`Konum: ${event.latlng.lat.toFixed(5)}, ${event.latlng.lng.toFixed(5)}`)
      .openOn(map);
  });
</script>
```

`setView` başlangıç merkezini ve yakınlaştırma seviyesini belirler. `tileLayer`, OSM karo görüntülerini haritaya taşır. Tıklama olayı ise kullanıcının seçtiği koordinatı gösterir. Gerçek projelerde herkese açık karo sunucularının kullanım politikasını incelemek, yoğun trafik için uygun bir sağlayıcı seçmek gerekir.

## uMap ve veri paylaşımı

Kod yazmadan başlamak isteyenler uMap üzerinde işaretçiler, çizgiler ve bölgeler ekleyebilir. Hazırlanan katmanlar GeoJSON olarak dışa aktarılıp Leaflet uygulamasına alınabilir:

```javascript
fetch('noktalar.geojson')
  .then(response => response.json())
  .then(data => L.geoJSON(data, {
    onEachFeature: (feature, layer) => {
      layer.bindPopup(feature.properties.name ?? 'İsimsiz nokta');
    }
  }).addTo(map));
```

Bu yaklaşımda içerik ekibi uMap ile veriyi düzenlerken geliştirici Leaflet arayüzünü yönetir. OSM veriyi, uMap kolay düzenlemeyi, Leaflet ise özgür programlamayı sağlar. Böylece küçük bir gezi rehberinden kapsamlı bir konum platformuna kadar büyüyebilen, açık ve esnek bir mimari kurulur.
