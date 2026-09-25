---
layout: post
title: "Tarama Çizgisi ile Dikdörtgenlerin Kesişim Alanını Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - sweep-line
  - hesaplamalı-geometri
  - python
  - dikdörtgen
  - koordinat-sıkıştırma
toc: true
image: /img/tarama-cizgisi-ile-31.png
---

Düzlemde yüzlerce dikdörtgen bulunduğunu ve en az iki dikdörtgen tarafından kaplanan toplam alanı hesaplamamız gerektiğini düşünelim. Her dikdörtgen çiftini ayrı ayrı incelemek cazip görünür; ancak üçlü kesişimler aynı alanı defalarca saydırabilir. Tarama çizgisi, iki boyutlu bu karmaşayı dikey bir çizgiyi soldan sağa kaydırarak tek boyutlu aralık problemlerine dönüştürür.

``

## Temel fikir

Kenarları eksenlere paralel bir dikdörtgeni $(x_1,y_1,x_2,y_2)$ ile gösterelim. Dikey tarama çizgisi yalnızca bir dikdörtgenin sol veya sağ kenarına ulaştığında aktif dikdörtgen kümesi değişir. Bu nedenle her dikdörtgenden iki olay üretiriz:

- $x_1$ konumunda dikdörtgenin $[y_1,y_2)$ aralığını ekle.
- $x_2$ konumunda aynı aralığı kaldır.

Ardışık olay koordinatları $x_i$ ve $x_{i+1}$ arasında aktif küme sabittir. Bu şeritte en az iki kez kaplanan toplam dikey uzunluk $L_i$ ise alana katkı

$$A_i=(x_{i+1}-x_i)L_i$$

olur. Sonuç, bütün şeritlerin toplamıdır:

$$A=\sum_i (x_{i+1}-x_i)L_i.$$

Böylece alan hesabı, aktif $y$ aralıklarında en az iki kat örtülen uzunluğu bulma problemine indirgenir.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Dikdörtgen çiftlerini karşılaştırma | Uygulaması kolaydır | Üçlü kesişimleri tekrar sayabilir |
| Hücre veya piksel tarama | Sezgiseldir | Büyük koordinatlarda aşırı maliyetlidir |
| Sweep line | Koordinat büyüklüğünden az etkilenir | Olay yönetimi dikkat ister |
| Sweep line + segment tree | Büyük veri için hızlıdır | Uygulaması daha karmaşıktır |

![tarama-cizgisi-ile-31](/img/tarama-cizgisi-ile-31.svg)


## Orta ölçekli bir Python çözümü

Aşağıdaki uygulama, her $x$ şeridinde aktif aralıkların uç noktalarını tarar. En az iki aralığın örttüğü dikey uzunluğu hesapladığı için üç veya daha fazla dikdörtgenin ortak bölgesi yalnızca bir kez alana eklenir.

```python
def overlap_y_length(intervals):
    """En az iki aktif aralık tarafından kaplanan y uzunluğunu döndürür."""
    points = []
    for y1, y2 in intervals:
        points.append((y1, 1))
        points.append((y2, -1))

    points.sort()
    covered = 0
    count = 0
    previous_y = None

    for y, delta in points:
        if previous_y is not None and count >= 2:
            covered += y - previous_y
        count += delta
        previous_y = y

    return covered


def rectangle_overlap_area(rectangles):
    """En az iki dikdörtgenin kapladığı birleşik kesişim alanını bulur."""
    events = []
    for rect_id, (x1, y1, x2, y2) in enumerate(rectangles):
        events.append((x1, 1, rect_id, y1, y2))   # ekle
        events.append((x2, -1, rect_id, y1, y2))  # kaldır

    events.sort()
    active = {}
    area = 0
    previous_x = events[0][0] if events else 0
    index = 0

    while index < len(events):
        x = events[index][0]
        width = x - previous_x
        area += width * overlap_y_length(active.values())

        # Aynı x koordinatındaki olayları birlikte uygula.
        while index < len(events) and events[index][0] == x:
            _, event_type, rect_id, y1, y2 = events[index]
            if event_type == 1:
                active[rect_id] = (y1, y2)
            else:
                active.pop(rect_id)
            index += 1

        previous_x = x

    return area

rectangles = [(0, 0, 4, 3), (2, 1, 6, 5), (3, 2, 5, 4)]
print(rectangle_overlap_area(rectangles))
```

## Karmaşıklık ve geliştirme

Her şeritte aktif aralıklar yeniden sıralandığından bu öğretici sürümün en kötü durum maliyeti yaklaşık $O(n^2\log n)$ olabilir. Büyük veri kümelerinde $y$ koordinatları sıkıştırılır ve bir segment tree üzerinde kapsama sayıları tutulur. Böylece güncellemeler $O(\log n)$ sürer ve toplam karmaşıklık $O(n\log n)$ düzeyine yaklaşır.

Sweep line’ın asıl güzelliği burada saklıdır: Alanı doğrudan hesaplamaya çalışmak yerine, yalnızca değişimin gerçekleştiği koordinatlara bakarız. Geometri bir anda olaylar, aralıklar ve küçük şeritlerin toplamı hâline gelir.
