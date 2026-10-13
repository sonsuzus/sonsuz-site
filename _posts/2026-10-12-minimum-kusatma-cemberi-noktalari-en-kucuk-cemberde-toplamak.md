---
layout: post
title: "Minimum Kuşatma Çemberi: Noktaları En Küçük Çemberde Toplamak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - hesaplamalı-geometri
  - python
  - welzl-algoritması
  - matematik
toc: true
image: /img/minimum-kusatma-cemberi-56.png
---

Harita üzerindeki istasyonları tek bir kapsama alanına almak, bir grup nesnenin merkezini belirlemek veya geometrik veriyi sıkıştırmak istediğimizi düşünelim. Elimizde çok sayıda nokta var ve hepsini kapsayan mümkün olan en küçük çemberi arıyoruz. İşte **Minimum Kuşatma Çemberi** problemi tam olarak bunu çözer: Noktalardan hiçbirini dışarıda bırakmadan yarıçapı en aza indirir.
``

## Problemin matematiksel tanımı

Her nokta $p_i=(x_i,y_i)$ ve aradığımız çemberin merkezi $c=(a,b)$, yarıçapı ise $r$ olsun. Bütün noktaların çemberde kalması için şu koşul sağlanmalıdır:

$$
(x_i-a)^2+(y_i-b)^2 \leq r^2
$$

Ama yalnızca kapsayan bir çember bulmak yeterli değildir; $r$ değerini mümkün olduğunca küçültmeliyiz. İlginç nokta şudur: En küçük çember genellikle tüm noktalar tarafından değil, sınırında bulunan en fazla **üç nokta** tarafından belirlenir.

- Bir sınır noktası varsa çemberin yarıçapı sıfır olabilir.
- İki sınır noktası varsa bunlar çapın uçlarıdır.
- Üç sınır noktası varsa çember, üçgenin çevrel çemberidir.

Bu özellik, sonsuz sayıdaki olası merkezle uğraşmak yerine küçük bir sınır kümesini incelememizi sağlar.

| Yaklaşım | Zaman karmaşıklığı | Özellik |
|---|---:|---|
| Tüm ikili ve üçlü kombinasyonlar | Yaklaşık $O(n^4)$ | Basit fakat yavaş |
| Artımlı geometrik çözüm | $O(n^3)$ | Küçük veri için uygun |
| Welzl algoritması | Beklenen $O(n)$ | Rastgele ve oldukça hızlı |

## Welzl algoritmasının fikri

Welzl algoritması noktaları önce rastgele karıştırır. Ardından bir noktayı geçici olarak çıkarıp kalan noktaların minimum çemberini hesaplar. Çıkarılan nokta bulunan çemberin içindeyse sonuç değişmez. Dışındaysa bu noktanın nihai çemberin sınırında bulunması gerektiğini artık biliyoruz.

Rastgele sıralama önemlidir. Kötü bir nokta sırası çok sayıda yeniden hesaplamaya yol açabilirken karıştırma işlemi, algoritmanın beklenen çalışma süresini doğrusal seviyeye indirir.

```python
import math
import random


def inside(circle, p, eps=1e-9):
    x, y, r = circle
    return (p[0] - x) ** 2 + (p[1] - y) ** 2 <= r * r + eps


def diameter_circle(a, b):
    x = (a[0] + b[0]) / 2
    y = (a[1] + b[1]) / 2
    return x, y, math.dist(a, b) / 2


def boundary_circle(points):
    if not points:
        return 0.0, 0.0, 0.0
    if len(points) == 1:
        return points[0][0], points[0][1], 0.0
    if len(points) == 2:
        return diameter_circle(points[0], points[1])

    a, b, c = points
    d = 2 * (a[0] * (b[1] - c[1]) +
             b[0] * (c[1] - a[1]) +
             c[0] * (a[1] - b[1]))

    if abs(d) < 1e-12:  # Noktalar doğrusal olabilir.
        circles = [diameter_circle(a, b), diameter_circle(a, c),
                   diameter_circle(b, c)]
        return min((q for q in circles if all(inside(q, p) for p in points)),
                   key=lambda q: q[2])

    aa, bb, cc = a[0] ** 2 + a[1] ** 2, b[0] ** 2 + b[1] ** 2, c[0] ** 2 + c[1] ** 2
    ux = (aa * (b[1] - c[1]) + bb * (c[1] - a[1]) + cc * (a[1] - b[1])) / d
    uy = (aa * (c[0] - b[0]) + bb * (a[0] - c[0]) + cc * (b[0] - a[0])) / d
    return ux, uy, math.dist((ux, uy), a)


def welzl(points, boundary, n):
    if n == 0 or len(boundary) == 3:
        return boundary_circle(boundary)

    p = points[n - 1]
    circle = welzl(points, boundary, n - 1)
    if inside(circle, p):
        return circle
    return welzl(points, boundary + [p], n - 1)


def minimum_circle(points):
    points = list(points)
    random.shuffle(points)
    return welzl(points, [], len(points))
```

Kodda `boundary_circle`, en fazla üç sınır noktasından çember üretir. Determinantın sıfıra yakın olması üç noktanın doğrusal olduğunu gösterir; bu durumda uygun nokta çiftinin oluşturduğu çember seçilir. `eps` toleransı ise kayan noktalı sayı hatalarının, sınırdaki bir noktayı yanlışlıkla dışarıda göstermesini önler.

## Nerelerde kullanılır?

Minimum kuşatma çemberi; kablosuz ağ kapsaması, robotik, oyunlardaki çarpışma sınırları, coğrafi analiz ve küme görselleştirme gibi alanlarda kullanılır. Algoritmanın asıl güzelliği, karmaşık görünen küresel bir optimizasyonu en fazla üç kritik noktaya indirgemesidir. Bazen kalabalığın tamamını anlamak için yalnızca sınırdakilere bakmak yeterlidir!

![minimum-kusatma-cemberi-56](/img/minimum-kusatma-cemberi-56.svg)

