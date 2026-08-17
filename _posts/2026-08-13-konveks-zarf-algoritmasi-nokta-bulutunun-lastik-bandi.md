---
layout: post
title: "Konveks Zarf Algoritması: Nokta Bulutunun Lastik Bandı"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - hesaplamalı geometri
  - python
  - convex hull
image: /img/konveks-zarf-algoritmasi-73.png
---

Bir harita üzerindeki sensörleri, bir oyundaki çarpışma sınırlarını veya bir görseldeki nesnenin dış konturunu düşünün. Konveks zarf (convex hull), verilen nokta kümesini içine alan en küçük dışbükey çokgendir. Sezgisel olarak noktaların etrafına lastik bir bant geçirirsek, bant gevşediğinde oluşan şekil konveks zarftır. İçeride kalan noktalar bantla temas etmez; yalnızca sınırdaki kritik noktalar sonuçta yer alır.

``

## Dışbükeylik neden önemlidir?

Bir şekil, içindeki herhangi iki noktayı bir doğru parçasıyla birleştirdiğimizde bu parçanın tamamı şeklin içinde kalıyorsa **dışbükeydir**. Konveks zarf da bir kümenin tüm dışbükey kapsayıcıları arasında alanı en küçük olanıdır. Matematiksel olarak, $P$ nokta kümesinin zarfı $\operatorname{conv}(P)$ ile gösterilir. Bir $x$ noktası şu biçimde yazılabiliyorsa zarftadır:

$$x = \sum_{i=1}^{n}\lambda_i p_i, \qquad \lambda_i \geq 0, \qquad \sum_{i=1}^{n}\lambda_i = 1$$

Buradaki $\lambda_i$ değerleri ağırlıklardır. Bu ifade, zarf içindeki her noktanın başlangıç noktalarının ağırlıklı ortalaması olduğunu söyler.

Algoritmanın kalbindeki fikir ise üç noktanın dönüş yönünü bulmaktır. $O$, $A$ ve $B$ için çapraz çarpım işareti aşağıdaki değerden gelir:

$$\operatorname{cross}(O,A,B)=(A_x-O_x)(B_y-O_y)-(A_y-O_y)(B_x-O_x)$$

Sonuç pozitifse sola dönüş, negatifse sağa dönüş, sıfırsa noktalar aynı doğru üzerindedir. Konveks zarf oluştururken yanlış yöndeki dönüşleri sileriz.

| Çapraz çarpım sonucu | Geometrik anlamı | Monotonic Chain kararı |
|---|---|---|
| $>0$ | Sola dönüş | Köşe korunur |
| $<0$ | Sağa dönüş | Son eklenen köşe çıkarılır |
| $=0$ | Doğrusal hizalanma | Politikanıza göre ara nokta çıkarılabilir |

## Andrew’s Monotonic Chain yaklaşımı

En pratik klasik yöntemlerden biri Andrew’s Monotonic Chain algoritmasıdır. Önce noktalar $x$, eşitlik durumunda $y$ koordinatına göre sıralanır. Ardından soldan sağa ilerleyerek alt zarf, ters yönde ilerleyerek üst zarf üretilir. İki zincir birleştirildiğinde çokgen tamamlanır.

Sıralama maliyeti baskın olduğu için zaman karmaşıklığı $O(n \log n)$, ek bellek maliyeti ise $O(n)$ düzeyindedir. Bu, binlerce hatta milyonlarca nokta için oldukça iyi bir sonuçtur.

```python
from typing import List, Tuple

Point = Tuple[int, int]

def cross(o: Point, a: Point, b: Point) -> int:
    # O->A ile O->B vektörlerinin 2B çapraz çarpımı
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points: List[Point]) -> List[Point]:
    points = sorted(set(points))  # Yinelenenleri kaldır, sırala
    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()  # Sağa dönüş veya doğrusal ara nokta
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]
```

Kodda `<= 0` kullanılması, aynı doğru üzerindeki ara noktaları sonuçtan çıkarır ve yalnızca uç köşeleri bırakır. Eğer sınır üzerindeki tüm doğrusal noktaları korumak istiyorsanız koşulu `< 0` olarak değiştirebilirsiniz. Bu küçük ayrıntı; örneğin tel çit uzunluğu hesaplamak ile sınırdaki bütün sensörleri raporlamak arasında önemli fark yaratır.

| Algoritma | Ortalama karmaşıklık | Güçlü yanı | Dikkat edilmesi gereken |
|---|---:|---|---|
| Monotonic Chain | $O(n \log n)$ | Basit ve güvenilir | Ön sıralama gerekir |
| Graham Scan | $O(n \log n)$ | Klasik öğretim örneği | Açı sıralaması hassastır |
| Jarvis March | $O(nh)$ | Az köşeli kümelerde iyi | Çok köşede yavaşlar |

Konveks zarf, daha gelişmiş geometri araçlarının da temelidir: en uzak iki nokta, minimum alanlı sınırlayıcı dikdörtgen ve çarpışma tespiti gibi problemler çoğu zaman önce bu “lastik bant” sınırını çıkararak sadeleşir.

![konveks-zarf-algoritmasi-73](/img/konveks-zarf-algoritmasi-73.svg)

