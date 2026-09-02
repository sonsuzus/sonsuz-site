---
layout: post
title: "Çapraz Çarpımla İki Doğru Parçasının Kesişimini Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - vektörler
  - hesaplamalı geometri
  - algoritma
toc: true
---

Harita uygulamalarından oyun motorlarına kadar birçok sistem, iki doğru parçasının kesişip kesişmediğini hızlıca bilmek ister. İlk akla gelen yöntem eğimleri hesaplamak ve doğruların denklemlerini çözmek olabilir. Fakat bu yaklaşım dik doğrularda özel durumlar, bölme işlemleri ve kayan nokta hataları üretir. Neyse ki vektörel çapraz çarpım sayesinde sinüs, kosinüs ya da açı hesaplamadan yalnızca çıkarma ve çarpma işlemleriyle sağlam bir kesişim testi yapabiliriz.

``

## Temel fikir: Nokta hangi tarafta?

İki boyutlu $A=(a_x,a_y)$ ve $B=(b_x,b_y)$ vektörlerinin çapraz çarpımı, üç boyutlu sonucun yalnızca $z$ bileşeni düşünülerek şöyle hesaplanır:

$$A \times B = a_xb_y-a_yb_x$$

Sonucun işareti bize yön bilgisi verir. Bir $AB$ doğru parçasına göre $C$ noktasının konumunu anlamak için şu yönelim fonksiyonunu kullanırız:

$$\operatorname{orient}(A,B,C)=(B-A)\times(C-A)$$

| Sonuç | Geometrik anlam |
|---|---|
| $>0$ | $C$, $A \rightarrow B$ yönünün solundadır |
| $<0$ | $C$, $A \rightarrow B$ yönünün sağındadır |
| $=0$ | $A$, $B$ ve $C$ aynı doğru üzerindedir |

Buradaki güzellik şudur: Açının kaç derece olduğunu bilmeyiz, fakat hangi tarafa dönüldüğünü biliriz. Kesişim testi için ihtiyacımız olan da tam olarak budur.

## Karşılıklı taraf testi

İlk parçamız $AB$, ikinci parçamız $CD$ olsun. Genel durumda parçaların kesişmesi için $C$ ile $D$, $AB$ doğrusunun farklı taraflarında bulunmalıdır. Aynı şekilde $A$ ile $B$ de $CD$ doğrusunun farklı taraflarında olmalıdır.

Dört yönelim hesaplarız:

$$o_1=\operatorname{orient}(A,B,C), \quad o_2=\operatorname{orient}(A,B,D)$$

$$o_3=\operatorname{orient}(C,D,A), \quad o_4=\operatorname{orient}(C,D,B)$$

Sıfır olmayan genel durumda kesişim koşulu şöyledir:

$$o_1o_2<0 \quad \text{ve} \quad o_3o_4<0$$

| Yaklaşım | Avantaj | Sorun |
|---|---|---|
| Eğim hesabı | Tanıdık cebirsel yöntem | Dikey doğruda sıfıra bölme riski |
| Trigonometri | Açıları açıkça verir | Gereksiz derecede maliyetli |
| Çapraz çarpım | Hızlı, sade ve yön tabanlı | Eşdoğrusal durum ayrıca incelenmeli |

## Eşdoğrusal noktalar: Küçük ama önemli ayrıntı

Yönelimlerden biri sıfırsa ilgili nokta doğrunun üzerindedir; ancak doğru parçasının üzerinde olmak zorunda değildir. Örneğin $(20,0)$ noktası, $(0,0)$ ve $(10,0)$ ile aynı doğrudadır ama parçanın dışındadır. Bu nedenle koordinatların sınırlayıcı kutu içinde olup olmadığını kontrol ederiz:

$$\min(a_x,b_x)\leq p_x\leq\max(a_x,b_x)$$

Aynı koşul $y$ koordinatı için de sağlanmalıdır.

```javascript
function orientation(a, b, c) {
  // Pozitif: sol dönüş, negatif: sağ dönüş, sıfır: eşdoğrusal
  return (b.x - a.x) * (c.y - a.y) -
         (b.y - a.y) * (c.x - a.x);
}

function onSegment(a, b, p) {
  // Eşdoğrusal p noktasının AB sınırları içinde olduğunu doğrular.
  return p.x >= Math.min(a.x, b.x) &&
         p.x <= Math.max(a.x, b.x) &&
         p.y >= Math.min(a.y, b.y) &&
         p.y <= Math.max(a.y, b.y);
}

function intersects(a, b, c, d) {
  const o1 = orientation(a, b, c);
  const o2 = orientation(a, b, d);
  const o3 = orientation(c, d, a);
  const o4 = orientation(c, d, b);

  if (o1 * o2 < 0 && o3 * o4 < 0) return true;

  if (o1 === 0 && onSegment(a, b, c)) return true;
  if (o2 === 0 && onSegment(a, b, d)) return true;
  if (o3 === 0 && onSegment(c, d, a)) return true;
  if (o4 === 0 && onSegment(c, d, b)) return true;

  return false;
}
```

Algoritma sabit sayıda işlem yaptığı için zaman karmaşıklığı $O(1)$, bellek karmaşıklığı da $O(1)$ olur. Tamsayı koordinatlarında oldukça güvenilirdir; ancak çok büyük değerlerde taşma, ondalıklı koordinatlarda ise hassasiyet sorunları düşünülmelidir. Kayan noktalı verilerde `o === 0` yerine $\vert o\vert <\varepsilon$ biçiminde küçük bir tolerans kullanmak daha güvenlidir. Böylece çapraz çarpım, geometrinin İsviçre çakısı gibi çalışır: küçük, hızlı ve şaşırtıcı derecede kullanışlıdır.
