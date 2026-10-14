---
layout: post
title: "A* Arama Algoritması: Sezgilerle En Kısa Yolu Bulmak"
math: true
categories: 
  - Program
tags: 
  - a-star
  - arama-algoritmaları
  - python
  - yapay-zeka
  - graf-teorisi
  - algoritma
toc: true
image: /img/a-arama-algoritmasi-25.png
---

Bir labirentte çıkışı aradığınızı düşünün. Dijkstra algoritması, hedefin hangi yönde olduğunu önemsemeden çevresindeki yolları sabırla inceler. A* ise aynı işi yaparken hedefe doğru ne kadar yaklaştığını tahmin eden bir pusula kullanır. Bu sezgisel yaklaşım, doğru koşullarda en kısa yolu korurken gereksiz düğümleri ziyaret etmeyi azaltabilir.

``

## A* algoritmasının temel fikri

A*, ağırlıklı bir graf üzerinde başlangıç düğümünden hedef düğüme giden en düşük maliyetli yolu arar. Her düğüm için üç önemli değer kullanır:

$$f(n) = g(n) + h(n)$$

- $g(n)$: Başlangıçtan $n$ düğümüne kadar ödenen gerçek maliyettir.
- $h(n)$: $n$ düğümünden hedefe kalan maliyetin tahminidir.
- $f(n)$: Düğüm üzerinden geçen yolun tahmini toplam maliyetidir.

Algoritma, sıradaki adım olarak $f(n)$ değeri en küçük olan düğümü seçer. Başka bir deyişle geçmişte ödediği maliyet ile gelecekte ödeyeceğini düşündüğü maliyeti birlikte değerlendirir.

| Algoritma | Kullanılan değer | Hedef bilgisi | Genel davranış |
|---|---:|---|---|
| Dijkstra | $g(n)$ | Kullanmaz | Her yöne dengeli yayılır |
| Greedy Best-First | $h(n)$ | Kullanır | Hedefe koşar, en kısa yolu garanti etmeyebilir |
| A* | $g(n)+h(n)$ | Kullanır | Maliyet ile yön tahminini dengeler |

![a-arama-algoritmasi-25](/img/a-arama-algoritmasi-25.svg)


Aslında $h(n)=0$ seçilirse A*, Dijkstra algoritmasına dönüşür. Dolayısıyla A* için Dijkstra'nın hedef bilgisiyle güçlendirilmiş hâli denebilir.

## Sezgisel fonksiyon nasıl seçilir?

Kareli ve dört yönde hareket edilen bir haritada Manhattan uzaklığı kullanılabilir:

$$h(n)=\vert x_n-x_h\vert +\vert y_n-y_h\vert $$

Çapraz hareket mümkünse Öklid uzaklığı daha uygun olabilir. A*'ın en kısa yolu garanti etmesi için sezgisel fonksiyonun gerçek kalan maliyeti aşmaması gerekir. Bu özelliğe **kabul edilebilirlik** denir. Ayrıca tutarlı bir sezgi için her kenarda şu koşul sağlanır:

$$h(n) \leq c(n,m)+h(m)$$

Tahmin çok küçükse algoritma güvenli fakat Dijkstra'ya yakın çalışır. Tahmin gereğinden büyükse daha hızlı görünebilir, ancak en kısa yol garantisi kaybolabilir.

## Python ile A* uygulaması

Aşağıdaki kod, sözlük biçiminde tanımlanmış ağırlıklı bir graf üzerinde çalışır. Öncelik kuyruğu, tahmini toplam maliyeti en düşük düğümü verimli biçimde seçer.

```python
from heapq import heappush, heappop

def a_star(graph, start, goal, heuristic):
    # Kuyruk elemanları: (f maliyeti, düğüm)
    open_set = [(heuristic(start, goal), start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, current = heappop(open_set)

        if current in visited:
            continue
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1], g_score[goal]

        visited.add(current)

        for neighbor, edge_cost in graph[current]:
            tentative = g_score[current] + edge_cost

            if tentative < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                f_score = tentative + heuristic(neighbor, goal)
                heappush(open_set, (f_score, neighbor))

    return None, float("inf")
```

Örnek olarak düğümlerin koordinatlarını ve bağlantılarını tanımlayabiliriz:

```python
graph = {
    "A": [("B", 2), ("C", 4)],
    "B": [("A", 2), ("D", 3)],
    "C": [("A", 4), ("D", 1)],
    "D": [("B", 3), ("C", 1), ("E", 2)],
    "E": []
}

coords = {
    "A": (0, 0), "B": (1, 0), "C": (0, 1),
    "D": (1, 1), "E": (2, 1)
}

def manhattan(a, b):
    x1, y1 = coords[a]
    x2, y2 = coords[b]
    return abs(x1 - x2) + abs(y1 - y2)

path, cost = a_star(graph, "A", "E", manhattan)
print(path, cost)
```

Bu uygulama yolu `A, B, D, E` veya aynı maliyetli uygun bir alternatif olarak döndürebilir. A* özellikle oyun haritaları, robot navigasyonu ve rota planlama sistemlerinde güçlüdür. Yine de hız avantajı otomatik değildir: kötü bir sezgisel fonksiyon, büyük bellek tüketimi veya düzensiz graf yapısı performansı azaltabilir. İyi bir $h(n)$ seçimi ise A*'ın gerçek süper gücüdür.
