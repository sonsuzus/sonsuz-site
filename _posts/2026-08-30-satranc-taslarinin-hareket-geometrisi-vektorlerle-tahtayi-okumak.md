---
layout: post
title: "Satranç Taşlarının Hareket Geometrisi: Vektörlerle Tahtayı Okumak"
math: true
categories: 
  - Bilgi
tags: 
  - satranç
  - doğrusal cebir
  - vektör
  - python
  - algoritma
---

Satranç tahtası yalnızca 64 karelik bir oyun alanı değil, ayrık koordinat düzleminde çalışan küçük ama etkileyici bir geometri laboratuvarıdır. Her taşı bir başlangıç noktası, her hamleyi ise bir yer değiştirme vektörü olarak düşünürsek kurallar daha programlanabilir hâle gelir. Bu yaklaşım; hamle doğrulayıcıları, satranç motorları ve görselleştirme projeleri geliştirirken özellikle faydalıdır.

``

Tahtadaki sütunları `a`–`h` yerine 0–7, satırları da 0–7 ile temsil edelim. Böylece `e4` karesi örneğin $(4, 3)$ koordinatına dönüşür. Bir taş $(x, y)$ konumundan $(x', y')$ konumuna giderken hareket vektörü şöyledir:

$$\Delta = (\Delta x, \Delta y) = (x' - x, y' - y)$$

Bu fark vektörü, taşın hareketinin türünü belirler. Vezir, kale ve fil gibi taşlar doğrusal alt uzaylara benzer çizgiler üzerinde ilerler. At ise bu düzeni sevimli bir biçimde bozan, sıçramalı bir vektör kümesine sahiptir.

| Taş | Geometrik koşul | Vektörel yorum | Engel kontrolü |
|---|---|---|---|
| Kale | $\Delta x = 0$ veya $\Delta y = 0$ | Yatay/dikey doğru | Gerekli |
| Fil | $\vert \Delta x\vert  = \vert \Delta y\vert $ | Çapraz doğru | Gerekli |
| Vezir | Kale veya fil koşulu | Doğrusal birleşim | Gerekli |
| At | $(\vert \Delta x\vert , \vert \Delta y\vert ) \in \{(1,2),(2,1)\}$ | Ayrık sıçrama vektörleri | Gerekmez |
| Şah | $\max(\vert \Delta x\vert ,\vert \Delta y\vert )=1$ | Komşuluk hareketi | Gerekli |

Filin kuralı, iki koordinattaki mutlak değişimin eşit olmasıdır. Örneğin $(2,1)$ noktasından $(5,4)$ noktasına giderken $\Delta=(3,3)$ elde edilir; dolayısıyla bu hamle çaprazdır. Aynı taşın $(2,1)$ konumundan $(6,3)$ konumuna gitmesi ise $(4,2)$ üretir ve eşitlik bozulduğu için geçersizdir. Dahası, fil her zaman aynı renkli karelerde kalır. Bunun cebirsel açıklaması, $x+y$ toplamının çapraz hamlelerde çift sayıda değişmesidir; parite korunur.

Atın meşhur L hareketi için tek bir doğru denklemi yazamayız. Bunun yerine izinli vektörlerden oluşan bir küme tanımlarız:

$$K = \{(\pm1,\pm2), (\pm2,\pm1)\}$$

Bu tanım, atın neden aradaki taşların üzerinden atlayabildiğini de açıklar: Hareket bir ışın boyunca ilerlemez, başlangıçtan hedefe doğrudan bir ayrık geçiştir. Aşağıdaki Python kodu, iki kare arasındaki hamlenin at için geçerli olup olmadığını kontrol eder:

```python
def at_hamlesi_mi(baslangic, hedef):
    x1, y1 = baslangic
    x2, y2 = hedef

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return (dx, dy) in {(1, 2), (2, 1)}

print(at_hamlesi_mi((1, 0), (2, 2)))  # True
print(at_hamlesi_mi((1, 0), (4, 1)))  # False
```

Kale, fil ve vezir için yalnızca yön kontrolü yetmez; yolun açık olması gerekir. Burada hareket vektörünü birim adıma indirgeriz. Örneğin $\Delta=(6,-3)$ için en büyük ortak bölen $\gcd(6,3)=3$ olduğundan adım vektörü $(2,-1)$ olur. Ancak bu vektör filin veya kalenin yönü değildir; dolayısıyla önce taşın yön kuralı doğrulanmalıdır. Geçerli bir fil hamlesinde $(4,4)$ vektörü, $(1,1)$ birim yönüne ayrılır.

```python
from math import copysign

def fil_hamlesi_mi(baslangic, hedef):
    dx = hedef[0] - baslangic[0]
    dy = hedef[1] - baslangic[1]
    return dx != 0 and abs(dx) == abs(dy)

def birim_yon(dx, dy):
    return (int(copysign(1, dx)), int(copysign(1, dy)))
```

Gerçek bir uygulamada `birim_yon` ile başlangıç ve hedef arasındaki kareleri sırayla üretip tahtadaki doluluk durumunu kontrol edersiniz. Sonuçta satranç hamleleri, karmaşık görünen kurallardan çok koordinat farkları, mutlak değerler, parite ve yön vektörleriyle ifade edilen düzenli bir sistemdir. Tahtaya bu gözle bakınca atın L’si bir ezber değil, sekiz olası vektörden ibaret olur.
