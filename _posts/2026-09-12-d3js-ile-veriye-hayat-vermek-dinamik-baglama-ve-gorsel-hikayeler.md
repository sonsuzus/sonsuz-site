---
layout: post
title: "D3.js ile Veriye Hayat Vermek: Dinamik Bağlama ve Görsel Hikâyeler"
math: true
categories: 
  - Bilgi
tags: 
  - d3.js
  - veri görselleştirme
  - javascript
toc: true
---

Bir veri tablosuna baktığınızda yalnızca satırlar ve sütunlar görebilirsiniz; D3.js ise aynı veride hareket eden çubuklar, renk değiştiren noktalar ve kullanıcıyla konuşan hikâyeler görür. Açılımı **Data-Driven Documents** olan D3.js, hazır grafikler sunmaktan çok daha temel bir fikir üzerine kuruludur: Veriyi HTML, SVG ve CSS gibi web standartlarına bağlamak. Böylece görselleştirme, ekrana çizilip unutulan bir resim değil; veriye tepki veren canlı bir arayüz hâline gelir.

``

## D3.js bir grafik kütüphanesi midir?

Evet, ama alışılmış anlamda değil. Çoğu grafik kütüphanesinde veri verilir, grafik türü seçilir ve sonuç alınır. D3.js ise geliştiriciye cetvel, boya ve tuval verir. Bu yaklaşım biraz daha fazla kod gerektirir; karşılığında görselin hemen her ayrıntısı kontrol edilebilir.

| Yaklaşım | Hazır grafik kütüphanesi | D3.js |
|---|---|---|
| Başlangıç hızı | Yüksek | Orta |
| Özelleştirme | Sınırlı veya orta | Çok yüksek |
| Web standartlarıyla ilişki | Soyutlanmış olabilir | Doğrudan |
| Animasyon kontrolü | Hazır seçenekler | Ayrıntılı kontrol |
| Öğrenme eğrisi | Daha yumuşak | Daha dik |

D3’ün temel felsefesi şu cümleyle özetlenebilir: **Önce DOM elemanlarını seç, sonra veriyi bu elemanlara bağla.** DOM, tarayıcının sayfadaki öğeleri temsil ettiği ağaç yapısıdır. D3 bu ağacı veriyle senkronize eder.

## Dinamik bağlama: Verinin DOM ile dansı

Elimizde $n$ veri öğesi ve $m$ görsel eleman bulunduğunu düşünelim. D3, eşleşen öğeleri **update**, henüz görsel karşılığı bulunmayan verileri **enter**, artık veride karşılığı kalmayan elemanları ise **exit** kümesine ayırır.

$$
DOM_{yeni} = Update + Enter - Exit
$$

Bu denklem matematiksel bir D3 komutu değildir; veri bağlamanın zihinsel modelidir. Modern D3 sürümlerindeki `join` metodu bu üç aşamayı daha okunabilir biçimde yönetir.

```js
const data = [12, 35, 22, 48];

const bars = d3.select('#chart')
  .selectAll('div')
  .data(data)
  .join('div')
  .attr('class', 'bar')
  .style('width', d => `${d * 6}px`)
  .style('background', 'steelblue')
  .text(d => d);
```

Burada `selectAll`, mevcut çubukları seçer; `data`, sayıları bu seçime bağlar; `join` ise eksik DOM elemanlarını üretir veya gereksiz olanları kaldırır. `d => ...` biçimindeki fonksiyonlarda `d`, ilgili elemana bağlanan veri değeridir. Veri değiştiğinde aynı işlem yeniden çalıştırılarak görsel güncellenebilir.

## Ölçekler neden gereklidir?

Ham veriler doğrudan piksel değildir. Örneğin 80.000 değerini ekranda 80.000 piksel olarak göstermek pek akıllıca olmaz. Ölçekler, veri uzayını görsel uzaya dönüştürür:

$$
x_{ekran} = a \cdot x_{veri} + b
$$

```js
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

console.log(scale(40)); // 200
```

`domain` verinin aralığını, `range` ise ekrandaki karşılığını belirtir. Doğrusal ölçeğin yanında logaritmik, zamansal, kategorik ve renk ölçekleri de bulunur.

| Ölçek | Uygun veri | Örnek kullanım |
|---|---|---|
| `scaleLinear` | Sürekli sayılar | Satış miktarı |
| `scaleBand` | Kategoriler | Şehir isimleri |
| `scaleTime` | Tarihler | Zaman serisi |
| `scaleLog` | Büyük oran farkları | Nüfus dağılımı |

## Etkileşim ve animasyon

D3, kullanıcı olaylarını veriye bağlı fonksiyonlarla işler. Böylece bir sütunun üzerine gelindiğinde ayrıntı gösterilebilir veya tıklamayla veri filtrelenebilir.

```js
d3.selectAll('.bar')
  .on('mouseenter', function (event, d) {
    d3.select(this).style('background', 'tomato');
  })
  .on('mouseleave', function () {
    d3.select(this).style('background', 'steelblue');
  })
  .transition()
  .duration(700)
  .style('opacity', 1);
```

Animasyon yalnızca süs değildir. Doğru kullanıldığında kullanıcının “hangi değer nereye taşındı?” sorusunu cevaplar ve değişimin sürekliliğini korur. Ancak aşırı hareket, görsel hikâyeyi lunaparka çevirebilir; amaç veriyi açıklamak, onu dans yarışmasına sokmak değildir.

Sonuç olarak D3.js, ham veriyi hazır bir kalıba dökmek yerine veri ile belge arasında sürdürülebilir bir bağ kurar. Seçimler, bağlama, ölçekler, geçişler ve olaylar birlikte kullanıldığında kullanıcı yalnızca grafiğe bakmaz; veriyi keşfeder, değiştirir ve hikâyenin parçası olur.
