---
layout: post
title: "Çarpışma Tespiti: İki Nesnenin Değdiğini Anlamanın Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - çarpışma tespiti
  - oyun geliştirme
  - matematik
  - algoritma
  - geometri
  - typescript
toc: true
image: /img/carpisma-tespiti-iki-81.png
---

![carpisma-tespiti-iki-81](/img/carpisma-tespiti-iki-81.svg)


Bir oyun karakteri duvarın içinden geçiyorsa, top zemine değmeden zıplıyorsa veya iki uzay gemisi birbirine çarpmasına rağmen yollarına devam ediyorsa suçlu çoğunlukla çarpışma tespitidir. Bilgisayarlar nesneleri gerçekten “görmez”; koordinatlar ve geometrik şekiller üzerinde yapılan matematiksel testlerle iki nesnenin temas edip etmediğine karar verir.
``
Çarpışma tespiti, iki geometrik bölgenin kesişip kesişmediğini bulma problemidir. En basit yaklaşım, nesneleri gerçek görünümleri yerine yaklaşık şekillerle temsil etmektir. Bu şekillere **çarpışma hacmi** veya *collider* denir. Karmaşık bir ejderhayı birkaç dikdörtgenle temsil etmek kulağa haksızlık gibi gelebilir; fakat işlemci ejderhanın duygularını değil, performansı önemser.

## Temel fikir: Bölgeler örtüşüyor mu?

İki boyutlu eksen hizalı dikdörtgenler, yani **AABB** (*Axis-Aligned Bounding Box*), minimum ve maksimum koordinatlarla tanımlanır. A ve B dikdörtgenleri şu koşulların tamamı doğruysa çarpışır:

$$
A_{minX} \le B_{maxX}, \quad A_{maxX} \ge B_{minX}
$$

$$
A_{minY} \le B_{maxY}, \quad A_{maxY} \ge B_{minY}
$$

Mantık aslında tersten daha kolaydır: Dikdörtgenlerden biri diğerinin tamamen sağında, solunda, üstünde veya altındaysa çarpışma yoktur. Bu ayrılma durumlarından hiçbiri bulunamıyorsa bölgeler örtüşmektedir.

```ts
type Rect = {
  x: number;
  y: number;
  width: number;
  height: number;
};

function intersectsAABB(a: Rect, b: Rect): boolean {
  return (
    a.x <= b.x + b.width &&
    a.x + a.width >= b.x &&
    a.y <= b.y + b.height &&
    a.y + a.height >= b.y
  );
}
```

Bu fonksiyon yalnızca birkaç karşılaştırma yaptığı için hızlıdır. Ancak döndürülmüş veya düzensiz nesnelerde gereğinden büyük alanları çarpışmış sayabilir.

## Daireler neden daha rahat?

Merkezleri $(x_1,y_1)$ ve $(x_2,y_2)$, yarıçapları $r_1$ ve $r_2$ olan iki daire, merkezleri arasındaki uzaklık yarıçaplar toplamından küçük veya eşitse temas eder:

$$
(x_2-x_1)^2 + (y_2-y_1)^2 \le (r_1+r_2)^2
$$

Burada karekök almamak bilinçli bir optimizasyondur. Uzaklığın karesiyle yarıçap toplamının karesini karşılaştırmak aynı sonucu daha az maliyetle verir.

```ts
function circlesCollide(
  x1: number, y1: number, r1: number,
  x2: number, y2: number, r2: number
): boolean {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const radiusSum = r1 + r2;

  return dx * dx + dy * dy <= radiusSum * radiusSum;
}
```

## Hangi yöntem ne zaman kullanılır?

| Yöntem | Güçlü yanı | Zayıf yanı | Uygun kullanım |
|---|---|---|---|
| AABB | Çok hızlı ve basit | Döndürülmüş şekillerde hatalı alan üretir | Platform oyunları, arayüzler |
| Daire | Dönüşten etkilenmez | Köşeli nesneleri kötü temsil eder | Toplar, parçacıklar |
| SAT | Döndürülmüş çokgenlerde hassastır | Daha fazla hesaplama ister | Fizik tabanlı 2D oyunlar |
| Piksel testi | Görsel olarak çok doğrudur | Yavaş ve bellek yoğundur | Özel durumlar |

**Ayıran Eksen Teoremi** veya SAT, iki dışbükey çokgen çarpışmıyorsa aralarında onları ayıran en az bir eksen bulunduğunu söyler. Çokgenlerin köşe izdüşümleri aday eksenlere yansıtılır. Herhangi bir eksende aralıklar örtüşmüyorsa çarpışma yoktur; bütün eksenlerde örtüşme varsa çarpışma vardır.

## Hızlı nesneler ve tünelleme

Çarpışmayı yalnızca her karede kontrol etmek bazen yetmez. Bir mermi bir karede duvarın solunda, sonraki karede sağında olabilir. Hiçbir ölçüm anında duvarın içinde olmadığı için sistem çarpışmayı kaçırır. Buna **tünelleme** denir.

Çözüm olarak hareket yolu boyunca ışın testi yapılabilir veya zaman sürekli ele alınabilir. Basit fikir, konumu yalnızca $t=0$ ve $t=1$ anlarında değil, hareket fonksiyonu üzerinden incelemektir:

$$
P(t)=P_0+tV, \quad 0 \le t \le 1
$$

Gerçek sistemlerde önce hızlı ve kaba bir **broad phase** testiyle olası çiftler bulunur, ardından hassas **narrow phase** algoritması çalıştırılır. Böylece yüzlerce nesnenin her biri diğerlerinin tamamıyla karşılaştırılmaz. Kısacası iyi çarpışma tespiti, en karmaşık şekli kullanmak değil; doğruluk, hız ve oyun hissi arasında doğru dengeyi kurmaktır.
