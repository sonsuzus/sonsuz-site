---
layout: post
title: "Çizgeler Dans Ederken: Kuvvet Yönelimli Graph Drawing Algoritmaları"
math: true
categories: 
  - Bilgi
tags: 
  - graph-drawing
  - veri-görselleştirme
  - force-directed
toc: true
---

Bir sosyal ağdaki arkadaşlıkları, şehirler arasındaki yolları veya yazılım modüllerinin bağımlılıklarını dümdüz bir listeyle incelemek pek heyecan verici değildir. Çizge görselleştirme, düğümlerden ve bağlantılardan oluşan bu karmaşık yapıları anlaşılır bir haritaya dönüştürür. Kuvvet yönelimli algoritmalar ise düğümleri küçük fiziksel cisimler gibi ele alarak onları ekranda adeta dans ettirir.
``
## Önce çizgenin dilini öğrenelim

Bir çizge matematiksel olarak $G=(V,E)$ biçiminde gösterilir. Burada $V$ düğümler kümesini, $E$ ise düğümler arasındaki kenarları temsil eder. Örneğin bir sosyal ağda insanlar düğüm, arkadaşlıklar kenardır.

Çizge çizimindeki temel problem, her $v_i$ düğümüne iki boyutlu bir konum $(x_i,y_i)$ atamaktır. Ama rastgele konumlar genellikle kenarların üst üste binmesine, düğümlerin kümelenmesine ve görüntünün çözülmesi zor bir kablo yığınına dönüşmesine neden olur. İyi bir yerleşim; ilişkili düğümleri yakın tutmalı, ilgisiz olanları ayırmalı ve mümkünse kenar kesişimlerini azaltmalıdır.

| Yaklaşım | Güçlü yönü | Zayıf yönü |
|---|---|---|
| Rastgele yerleşim | Çok hızlıdır | Genellikle okunaksızdır |
| Dairesel yerleşim | Düzenli ve öngörülebilirdir | Kümeleri iyi göstermez |
| Hiyerarşik yerleşim | Akış ve bağımlılıklar için uygundur | Döngülü ağlarda zorlanır |
| Kuvvet yönelimli yerleşim | Organik kümeler üretir | Büyük ağlarda maliyetlidir |

## Düğümler neden birbirini itiyor?

Kuvvet yönelimli modellerde düğümler aynı elektrik yüküne sahip parçacıklar gibi birbirini iter. Bir kenarla bağlı düğümler ise aralarında yay varmış gibi birbirini çeker. Böylece sistem, toplam enerjinin düşük olduğu dengeli bir konuma ulaşmaya çalışır.

Basitleştirilmiş itme kuvveti şu şekilde modellenebilir:

$$F_r(d)=-\frac{k_r}{d^2}$$

Burada $d$ iki düğüm arasındaki mesafe, $k_r$ ise itmenin gücüdür. Negatif işaret kuvvetin uzaklaştırıcı olduğunu belirtir. Yay benzeri çekim için Hooke yasasından esinlenebiliriz:

$$F_a(d)=k_a(d-L)$$

$L$ ideal kenar uzunluğudur. Düğümler fazla uzaksa çekilir, fazla yakınsa yay sıkışmış gibi ters yönde zorlanır. Her turda bütün kuvvetler toplanır ve düğümün konumu yaklaşık olarak güncellenir:

$$p_{t+1}=p_t+\alpha F_t$$

Buradaki $\alpha$, simülasyonun sıcaklığı veya adım büyüklüğüdür. Başlangıçta büyük olan bu değer zamanla azaltılır. Bu işleme **soğutma** denir; aksi hâlde düğümler sonsuza kadar zıplayabilir.

## D3.js ile hareketi görelim

Aşağıdaki örnek, D3.js kullanarak düğümleri iter, bağlı olanları bir arada tutar ve tüm ağı ekranın merkezine çeker:

```javascript
const nodes = [
  { id: "Ada" }, { id: "Bora" },
  { id: "Cem" }, { id: "Deniz" }
];

const links = [
  { source: "Ada", target: "Bora" },
  { source: "Ada", target: "Cem" },
  { source: "Cem", target: "Deniz" }
];

const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links)
    .id(d => d.id)
    .distance(90))
  .force("charge", d3.forceManyBody().strength(-250))
  .force("center", d3.forceCenter(400, 250))
  .force("collision", d3.forceCollide(24));

simulation.on("tick", () => {
  circles
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);

  lines
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);
});
```

`forceManyBody` elektriksel itmeyi, `forceLink` yay etkisini, `forceCenter` merkezlemeyi sağlar. `forceCollide` ise düğümlerin görsel olarak birbirinin içine girmesini engeller. `tick` olayı her fizik adımında SVG elemanlarının koordinatlarını yeniler.

## Büyük çizgelerde performans

Doğrudan hesaplamada her düğüm diğer tüm düğümlerle karşılaştırılır. Bu nedenle itme hesabının karmaşıklığı yaklaşık $O(\vert V\vert ^2)$ olur. Barnes–Hut yaklaşımı, uzaktaki düğümleri tek bir kütle gibi gruplayarak bunu yaklaşık $O(\vert V\vert \log\vert V\vert )$ seviyesine indirebilir.

Binlerce düğüm söz konusuysa Canvas veya WebGL, SVG’den daha uygun olabilir. Ayrıca zayıf kenarları filtrelemek, kümeleri önce toplulaştırmak ve simülasyonu belirli bir turdan sonra durdurmak ciddi hız kazandırır. Sonuçta güzel bir çizge yalnızca estetik değildir; verinin sakladığı toplulukları, merkezî aktörleri ve beklenmedik köprüleri görünür kılan güçlü bir keşif aracıdır.
