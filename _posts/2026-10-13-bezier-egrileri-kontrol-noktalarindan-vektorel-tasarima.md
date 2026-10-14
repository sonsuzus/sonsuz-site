---
layout: post
title: "Bézier Eğrileri: Kontrol Noktalarından Vektörel Tasarıma"
math: true
categories: 
  - Bilgi
tags: 
  - bezier
  - vektörel-tasarım
  - bilgisayar-grafikleri
  - matematik
  - javascript
  - svg
toc: true
image: /img/bezier-egrileri-kontrol-15.png
---

![bezier-egrileri-kontrol-15](/img/bezier-egrileri-kontrol-15.svg)

Bir logodaki kusursuz kıvrımın veya bir yazı karakterindeki zarif yayın arkasında çoğu zaman Bézier eğrileri vardır. Bu eğriler, yüzlerce pikseli tek tek yerleştirmek yerine birkaç kontrol noktasıyla akıcı şekiller oluşturmamızı sağlar. Üstelik yalnızca Illustrator, Figma ve Inkscape gibi tasarım araçlarında değil; animasyonlardan fontlara, oyunlardan robot hareketlerine kadar geniş bir alanda kullanılır.

``

## Eğriyi oluşturan temel fikir

Bézier eğrisi, Fransız mühendis Pierre Bézier tarafından otomobil gövdelerinin modellenmesinde yaygınlaştırıldı. Temel yaklaşım şaşırtıcı derecede basittir: Eğrinin başlangıç ve bitiş noktalarını belirler, araya da eğriyi kendilerine doğru çeken kontrol noktaları koyarız.

En basit tür olan doğrusal Bézier eğrisinde iki nokta bulunur:

$$B(t)=(1-t)P_0+tP_1, \quad 0 \leq t \leq 1$$

Burada $t$, başlangıçtan sona doğru ilerlemeyi temsil eder. $t=0$ olduğunda $P_0$, $t=1$ olduğunda ise $P_1$ noktasındayız. Aslında bu, iki nokta arasında yapılan doğrusal enterpolasyondur.

Grafik yazılımlarında sık karşılaştığımız kübik Bézier eğrisi ise dört nokta kullanır:

$$B(t)=(1-t)^3P_0+3(1-t)^2tP_1+3(1-t)t^2P_2+t^3P_3$$

$P_0$ ve $P_3$ eğrinin uçlarıdır. $P_1$ ve $P_2$ ise çoğu tasarım aracında tutamaç olarak gördüğümüz kontrol noktalarıdır. Eğri genellikle bu kontrol noktalarının üzerinden geçmez; yalnızca onların etkisiyle yön değiştirir. Kontrol noktasını çektiğinizde eğrinin lastik gibi uzaması bundandır.

| Eğri türü | Nokta sayısı | Kullanım alanı | Esneklik |
|---|---:|---|---|
| Doğrusal | 2 | Düz çizgiler | Düşük |
| Kuadratik | 3 | Basit kıvrımlar, fontlar | Orta |
| Kübik | 4 | İllüstrasyon, SVG, animasyon | Yüksek |

## Yumuşaklık nasıl sağlanır?

Birden fazla Bézier parçası uç uca eklenerek karmaşık yollar oluşturulur. Ancak parçaların yalnızca aynı noktada buluşması yeterli değildir. Keskin bir köşe istemiyorsak, birleşim noktasındaki kontrol kollarının aynı doğrultuda olması gerekir. Böylece eğrilerin teğetleri uyumlu olur ve gözümüz geçişi pürüzsüz algılar.

| Süreklilik | Anlamı | Görsel sonuç |
|---|---|---|
| $C^0$ | Parçalar aynı noktada buluşur | Kopukluk yoktur, köşe olabilir |
| $C^1$ | Birinci türevler eşittir | Yön ve hız yumuşaktır |
| $C^2$ | İkinci türevler de eşittir | Eğrilik daha doğal değişir |

Tasarım programlarındaki simetrik tutamaçlar, iki kolu aynı doğrultuda ve çoğunlukla eşit uzunlukta tutar. Köşe noktası seçildiğinde ise kollar bağımsız hareket eder; böylece sivri dönüşler üretilebilir.

## Canvas üzerinde bir Bézier eğrisi

Aşağıdaki JavaScript kodu, HTML Canvas üzerinde kübik bir eğri çizer. Kırmızı noktalar başlangıç ve bitişi, mavi noktalar ise eğrinin yönünü belirleyen kontrol noktalarını gösterir.

```javascript
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');

const points = [
  { x: 40,  y: 180 },  // başlangıç
  { x: 100, y: 20 },   // kontrol 1
  { x: 240, y: 260 },  // kontrol 2
  { x: 320, y: 80 }    // bitiş
];

ctx.beginPath();
ctx.moveTo(points[0].x, points[0].y);
ctx.bezierCurveTo(
  points[1].x, points[1].y,
  points[2].x, points[2].y,
  points[3].x, points[3].y
);
ctx.strokeStyle = '#222';
ctx.lineWidth = 4;
ctx.stroke();

points.forEach((p, index) => {
  ctx.beginPath();
  ctx.arc(p.x, p.y, 6, 0, Math.PI * 2);
  ctx.fillStyle = index === 0 || index === 3 ? 'red' : 'blue';
  ctx.fill();
});
```

Kodda `bezierCurveTo`, iki kontrol noktasıyla bitiş noktasını alır. Noktaları fareyle sürüklenebilir hâle getirerek küçük bir vektörel çizim aracı bile geliştirebilirsiniz.

## Neden vektörel tasarımın yıldızıdır?

Bézier eğrileri çözünürlükten bağımsızdır. Bir logo kartvizit boyutundan bina cephesine büyütülse bile matematiksel tanımı değişmez; eğri yeni ölçekte tekrar hesaplanır. Raster görsellerdeki pikselleşmenin görülmemesi bu yüzdendir.

SVG dosyalarındaki `C` komutu, fontların dış hatları ve CSS animasyonlarındaki zamanlama fonksiyonları aynı düşünceden yararlanır. Kısacası kontrol noktaları yalnızca çizgileri bükmez; dijital tasarımın ölçeklenebilir, düzenlenebilir ve şaşırtıcı derecede zarif olmasını sağlar.
