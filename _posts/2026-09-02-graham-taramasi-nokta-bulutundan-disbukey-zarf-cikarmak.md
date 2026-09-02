---
layout: post
title: "Graham Taraması: Nokta Bulutundan Dışbükey Zarf Çıkarmak"
math: true
categories: 
  - Bilgi
tags: 
  - graham taraması
  - dışbükey zarf
  - hesaplamalı geometri
toc: true
---

Bir kâğıda rastgele noktalar çizdiğinizi ve hepsini çevreleyecek biçimde bir lastik bant geçirdiğinizi düşünün. Bandı bıraktığınızda yalnızca en dıştaki noktalara tutunur ve dışbükey bir çokgen oluşturur. **Dışbükey zarf** adı verilen bu sınır; harita uygulamalarından görüntü işlemeye, robot hareket planlamasından oyun geliştirmeye kadar pek çok alanda kullanılır. Graham Taraması ise zarfı, noktaları kutupsal açılarına göre düzenleyip sistematik biçimde eleyerek bulur.
``
## Dışbükey zarf nedir?

Bir $P$ nokta kümesinin dışbükey zarfı, $P$ içindeki bütün noktaları kapsayan en küçük dışbükey bölgedir. Bir çokgen, içindeki herhangi iki nokta arasına çizilen doğru parçasının tamamı yine çokgenin içinde kalıyorsa dışbükeydir.

Graham Taraması üç temel adımdan oluşur:

1. Başlangıç, yani pivot noktayı seçmek.
2. Diğer noktaları pivot çevresindeki kutupsal açılarına göre sıralamak.
3. Sıralı noktaları gezerken sağa dönüş oluşturanları elemek.

## Pivot ve kutupsal açı

Pivot olarak genellikle $y$ koordinatı en küçük nokta seçilir. Eşitlik varsa $x$ koordinatı daha küçük olan tercih edilir. Böylece diğer bütün noktalar pivotun üstünde veya sağında kalır ve açısal tarama düzenli ilerler.

Pivot $p_0=(x_0,y_0)$ ve başka bir nokta $p=(x,y)$ için kutupsal açı teorik olarak

$$
\theta=\operatorname{atan2}(y-y_0, x-x_0)
$$

ile hesaplanabilir. Ancak gerçek uygulamalarda trigonometrik hesap yapmak şart değildir. Sıralama sırasında yön ve uzaklık bilgilerini kullanmak, kayan nokta maliyetlerinden kaçınabilir.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| `atan2` ile açı | Anlaşılması ve uygulanması kolaydır | Trigonometrik hesap görece maliyetlidir |
| Çapraz çarpım | Hızlı ve sayısal olarak daha güvenlidir | Özel bir karşılaştırıcı gerektirir |
| Uzaklığa göre bağ kırma | Aynı açıdaki noktaları düzenler | Yanlış sıra iç noktayı zarfa katabilir |

## Dönüş yönünü çapraz çarpımla bulmak

Algoritmanın kalbi, art arda gelen üç noktanın sola mı yoksa sağa mı döndüğünü belirlemektir. $A$, $B$ ve $C$ noktaları için yön değeri şöyledir:

$$
(B_x-A_x)(C_y-A_y)-(B_y-A_y)(C_x-A_x)
$$

Sonuç pozitifse sola dönüş, negatifse sağa dönüş, sıfırsa doğrusal hizalanma vardır.

| Sonuç | Geometrik anlam | Algoritmanın davranışı |
|---:|---|---|
| $>0$ | Sola dönüş | Noktayı zarfta tutar |
| $<0$ | Sağa dönüş | Ortadaki noktayı çıkarır |
| $=0$ | Doğrusal noktalar | Genellikle en uzaktakini tutar |

Tarama sırasında zarf adayları bir yığında saklanır. Yeni nokta sağa dönüş oluşturuyorsa yığının tepesindeki nokta çıkarılır. Bu işlem sola dönüş elde edilene veya yığında ikiden az nokta kalana kadar sürer. Kısacası algoritma, “yanlış sokağa girdim” dediği her köşeyi geri alır.

## Python ile uygulama

Aşağıdaki kod, noktaları sıralar ve dışbükey zarfın köşelerini saat yönünün tersine döndürür:

```python
from math import atan2

def graham_scan(points):
    points = sorted(set(points))
    if len(points) <= 2:
        return points

    pivot = min(points, key=lambda p: (p[1], p[0]))

    def distance_sq(p):
        return (p[0] - pivot[0]) ** 2 + (p[1] - pivot[1]) ** 2

    ordered = sorted(
        (p for p in points if p != pivot),
        key=lambda p: (atan2(p[1] - pivot[1], p[0] - pivot[0]),
                       distance_sq(p))
    )

    def cross(a, b, c):
        return ((b[0] - a[0]) * (c[1] - a[1])
                - (b[1] - a[1]) * (c[0] - a[0]))

    hull = [pivot]
    for point in ordered:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)

    return hull
```

`set` yinelenen noktaları kaldırır. `distance_sq`, aynı açıda bulunan noktaları yakından uzağa sıralar; tarama sırasında yakın olanlar elenir. `cross` fonksiyonu dönüş yönünü bulurken `hull` listesi yığın görevi görür.

## Karmaşıklık ve püf noktaları

Pivot seçimi $O(n)$, tarama $O(n)$ zaman alır. Baskın işlem sıralama olduğu için toplam karmaşıklık

$$
O(n\log n)
$$

olur. Ek bellek ihtiyacı ise zarf ve sıralanmış noktalar nedeniyle $O(n)$ düzeyindedir.

Tüm noktalar aynı doğru üzerindeyse sonuç yalnızca iki uç nokta olmalıdır. Ayrıca `<= 0` kullanımı doğrusal ara noktaları çıkarır; sınır üzerindeki bütün doğrusal noktaların korunması isteniyorsa koşul `< 0` yapılabilir. Böylece Graham Taraması, basit bir sıralama ve küçük bir yön testiyle karmaşık görünen nokta bulutunun dış kabuğunu zarifçe ortaya çıkarır.
