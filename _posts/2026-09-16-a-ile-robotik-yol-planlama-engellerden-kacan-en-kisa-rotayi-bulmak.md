---
layout: post
title: "A* ile Robotik Yol Planlama: Engellerden Kaçan En Kısa Rotayı Bulmak"
math: true
categories: 
  - Proje
tags: 
  - a-star
  - robotik
  - yol-planlama
  - algoritma
  - python
  - yapay-zeka
toc: true
image: /img/a-ile-robotik-59.png
---

Bir robotun başlangıç noktasından hedefe gitmesi kolay görünebilir; ta ki odanın ortasına sandalye, kutu ve duvarlar yerleştirene kadar! Robotik yol planlamanın amacı, hareketli sistemi engellere çarptırmadan hedefe ulaştıracak mümkün olan en düşük maliyetli rotayı bulmaktır. A* algoritması, gerçek maliyet ile hedefe yönelik tahmini birleştirerek bu işi hem verimli hem de anlaşılır biçimde yapar.

``

## A* algoritmasının temel fikri

A*, harita üzerindeki her aday düğüm için üç değer kullanır:

$$f(n) = g(n) + h(n)$$

Burada $g(n)$, başlangıçtan mevcut düğüme kadar ödenen gerçek maliyettir. $h(n)$ ise düğümden hedefe kalan mesafeye ilişkin sezgisel tahmindir. Algoritma, toplam tahmini maliyeti $f(n)$ en küçük olan düğümü önce inceler.

Bunu bir navigasyon uygulaması gibi düşünebiliriz: $g(n)$ şimdiye kadar kullandığımız yakıtı, $h(n)$ ise hedefe ulaşmak için harcayacağımız tahmini yakıtı temsil eder. Yalnızca geçmişe bakmak aramayı yavaşlatır; yalnızca tahmine güvenmek ise kötü rotalara yol açabilir. A*, ikisini dengeler.

| Algoritma | Gerçek maliyet | Sezgisel tahmin | Tipik davranış |
|---|---:|---:|---|
| Dijkstra | Var | Yok | Garantili fakat geniş arama yapar |
| Greedy Best-First | Yok | Var | Hızlı olabilir, en kısa yolu garanti etmez |
| A* | Var | Var | Doğru sezgiyle hızlı ve optimaldir |

![a-ile-robotik-59](/img/a-ile-robotik-59.svg)


## Izgara haritası ve sezgisel fonksiyon

Robotun çevresi çoğunlukla hücrelerden oluşan bir maliyet haritasına dönüştürülür. Boş hücreler geçilebilir, dolu hücreler engeldir. Robot yalnızca yatay ve dikey hareket ediyorsa Manhattan uzaklığı uygundur:

$$h(n) = \vert x_n-x_g\vert  + \vert y_n-y_g\vert $$

Çapraz hareket serbestse Öklid uzaklığı kullanılabilir:

$$h(n) = \sqrt{(x_n-x_g)^2 + (y_n-y_g)^2}$$

En kısa yol garantisi için sezgisel fonksiyon gerçek kalan maliyeti abartmamalıdır. Bu özelliğe **kabul edilebilirlik** denir.

## Python ile basit A* uygulaması

Aşağıdaki kod, sıfırların boş alanı ve birlerin engelleri gösterdiği bir ızgarada dört yönlü rota üretir:

```python
import heapq

def astar(grid, start, goal):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    open_set = [(0, start)]
    came_from = {}
    g_cost = {start: 0}

    def heuristic(node):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            x, y = neighbor

            if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
                continue
            if grid[x][y] == 1:
                continue

            candidate_cost = g_cost[current] + 1
            if candidate_cost < g_cost.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_cost[neighbor] = candidate_cost
                f_cost = candidate_cost + heuristic(neighbor)
                heapq.heappush(open_set, (f_cost, neighbor))

    return None
```

`open_set`, henüz değerlendirilecek hücreleri öncelik sırasıyla tutar. `came_from` ise hedef bulunduğunda geriye doğru ilerleyerek rotayı yeniden oluşturur. Engel veya harita sınırı kontrolü sayesinde robot geçersiz hücrelere girmez.

## Gerçek robotlarda dikkat edilmesi gerekenler

Izgara üzerindeki robot tek bir nokta değildir; fiziksel genişliği vardır. Bu nedenle engeller, robot yarıçapı ve güvenlik payı kadar şişirilmelidir. Aksi hâlde hesaplanan rota matematiksel olarak geçerli olsa bile robot duvara sürtebilir.

| Sorun | Pratik çözüm |
|---|---|
| Robotun fiziksel boyutu | Engel şişirme |
| Keskin dönüşler | Rota yumuşatma |
| Hareketli engeller | Haritayı yenileyip tekrar planlama |
| Dar alanlarda risk | Hücrelere ek maliyet verme |

A* statik haritalarda güçlü bir başlangıçtır. Sensörlerden gelen güncel veriler, maliyet haritası ve hareket denetleyicisiyle birleştirildiğinde robot yalnızca kısa değil, güvenli ve uygulanabilir bir rota da izleyebilir. Böylece “duvara çarpmadan hedefe ulaşma” problemi, düzenli bir maliyet hesabına dönüşür.
