---
layout: post
title: "Ramer-Douglas-Peucker Algoritması: Eğrileri Akıllıca Sadeleştirmek"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - geometri
  - python
  - veri-sadeleştirme
  - haritacılık
toc: true
image: /img/ramer-douglas-peucker-21.png
---

Bir GPS rotası, kıyı şeridi veya dijital çizim binlerce noktadan oluşabilir. Bu noktaların hepsini saklamak doğruluğu artırıyor gibi görünse de dosya boyutunu, çizim süresini ve işlem maliyetini büyütür. Ramer-Douglas-Peucker (RDP) algoritması, eğrinin görsel karakterini mümkün olduğunca korurken gereksiz noktaları kaldırır. Kısacası eğriye “Hangi noktalar gerçekten önem taşıyor?” diye sorar.
``

## Temel fikir

Algoritma, bir nokta dizisinin ilk ve son noktalarını düz bir doğruyla birleştirerek işe başlar. Ardından aradaki bütün noktaların bu doğruya olan dik uzaklıklarını hesaplar. Doğrudan en uzakta bulunan nokta, eğrinin en belirgin kırılma adayıdır.

Bu en büyük uzaklık belirlenen toleranstan, yani $\varepsilon$ değerinden büyükse nokta korunur. Eğri bu noktadan iki parçaya ayrılır ve aynı işlem her iki parça üzerinde özyinelemeli olarak tekrarlanır. Uzaklık toleransı aşmıyorsa aradaki noktalar silinebilir; çünkü söz konusu bölüm, yeterince iyi biçimde tek bir doğruyla temsil edilebilmektedir.

Bir $P$ noktasının, $A$ ve $B$ noktalarından geçen doğruya uzaklığı iki boyutta şöyle ifade edilebilir:

$$
d = \frac{\vert (B_y-A_y)P_x-(B_x-A_x)P_y+B_xA_y-B_yA_x\vert }{\sqrt{(B_y-A_y)^2+(B_x-A_x)^2}}
$$

Buradaki $d$, geometrik sapmayı; $\varepsilon$ ise kabul edilebilir hata sınırını temsil eder. Karar basittir: $d_{max} > \varepsilon$ ise böl, aksi hâlde sadeleştir.

## Tolerans neyi değiştirir?

| Tolerans | Korunan nokta | Görsel sonuç | Kullanım örneği |
|---|---:|---|---|
| Küçük $\varepsilon$ | Çok | Ayrıntılı ve aslına yakın | Hassas ölçüm |
| Orta $\varepsilon$ | Dengeli | Görsel bütünlük korunur | Web haritaları |
| Büyük $\varepsilon$ | Az | Köşeli ve kaba | Küçük önizlemeler |

Dolayısıyla “en iyi tolerans” diye evrensel bir sayı yoktur. Koordinatların birimi de önemlidir: enlem-boylam verisindeki $0.001$ ile piksel uzayındaki $0.001$ aynı fiziksel anlamı taşımaz.

## Python ile uygulama

Aşağıdaki orta düzey örnek, en uzak noktayı bulur ve tolerans aşılırsa listeyi özyinelemeli olarak parçalar:

```python
from math import hypot

def dogruya_uzaklik(p, a, b):
    x, y = p
    x1, y1 = a
    x2, y2 = b

    if a == b:
        return hypot(x - x1, y - y1)

    pay = abs((y2-y1)*x - (x2-x1)*y + x2*y1 - y2*x1)
    payda = hypot(y2-y1, x2-x1)
    return pay / payda


def rdp(noktalar, epsilon):
    if len(noktalar) < 3:
        return noktalar

    en_buyuk = 0
    indeks = 0
    for i in range(1, len(noktalar) - 1):
        uzaklik = dogruya_uzaklik(
            noktalar[i], noktalar[0], noktalar[-1]
        )
        if uzaklik > en_buyuk:
            en_buyuk = uzaklik
            indeks = i

    if en_buyuk > epsilon:
        sol = rdp(noktalar[:indeks + 1], epsilon)
        sag = rdp(noktalar[indeks:], epsilon)
        return sol[:-1] + sag

    return [noktalar[0], noktalar[-1]]
```

`sol[:-1] + sag` ifadesi, iki alt parçanın ortak kırılma noktasının iki kez eklenmesini engeller. En kötü durumda zaman karmaşıklığı $O(n^2)$ seviyesine çıkabilir; dengeli bölünmelerde davranış genellikle daha iyidir.

## Nerelerde kullanılır?

RDP; harita yollarının sadeleştirilmesinde, GPS izlerinin sıkıştırılmasında, çizim araçlarında ve sensör verilerinin azaltılmasında kullanılır. Bununla birlikte algoritma yalnızca geometrik uzaklığa bakar. Zaman, hız veya anlamsal önem taşıyan bir nokta küçük sapmaya sahipse yanlışlıkla elenebilir.

Sonuç olarak RDP, veri azaltma ile şekil sadakati arasında ayarlanabilir bir denge kurar. $\varepsilon$ düğmesini sağa çevirdikçe veri hafifler; fakat eğrinin kişiliği de yavaş yavaş minimalist sanata dönüşür.

![ramer-douglas-peucker-21](/img/ramer-douglas-peucker-21.svg)

