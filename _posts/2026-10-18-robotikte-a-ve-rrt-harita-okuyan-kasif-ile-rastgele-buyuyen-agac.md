---
layout: post
title: "Robotikte A* ve RRT: Harita Okuyan Kâşif ile Rastgele Büyüyen Ağaç"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - yol-planlama
  - a-star
  - rrt
  - algoritma
  - otonom-robotlar
toc: true
image: /img/robotikte-a-ve-74.png
---

Bir robotun başlangıç noktasından hedefe gitmesi, düz bir çizgi çizmekten çok daha karmaşıktır. Duvarlar, hareket kısıtları, robotun boyutları ve bilinmeyen bölgeler devreye girdiğinde bir **yol planlama algoritmasına** ihtiyaç duyulur. A* ve RRT aynı soruya cevap arasa da bunu tamamen farklı biçimlerde yapar: A* düzenli bir haritada en umut verici hücreleri incelerken RRT, uzaya rastgele dallar uzatan meraklı bir ağaç gibi davranır.

![robotikte-a-ve-74](/img/robotikte-a-ve-74.svg)

``

## Önce problem uzayını tanıyalım

Yol planlamada robotun bulunabileceği tüm durumlar **konfigürasyon uzayı**, yani $C$-space ile temsil edilir. İki boyutlu hareket eden noktasal bir robot için durum $(x,y)$ olabilir. Robotun yönü de önemliyse durum $(x,y,\theta)$ hâline gelir. Eklemli bir robot kolunda ise her eklem açısı yeni bir boyut ekler.

Engellerin kapladığı durumlar $C_{obs}$, güvenli durumlar ise $C_{free}$ olarak gösterilir. Amaç, başlangıç $q_{start}$ ile hedef $q_{goal}$ arasında tamamen $C_{free}$ içinde kalan bir yol bulmaktır.

A* çoğunlukla ayrıklaştırılmış grafiklerde çalışır. RRT ise sürekli ve yüksek boyutlu uzayları örnekleyerek grafik oluşturur. Temel ayrım burada başlar.

## A*: Maliyeti ve hedefi birlikte düşünmek

A*, incelenecek düğümleri şu puana göre seçer:

$$f(n)=g(n)+h(n)$$

Burada $g(n)$ başlangıçtan $n$ düğümüne kadar ödenen gerçek maliyet, $h(n)$ ise hedeften ne kadar uzakta olunduğunu tahmin eden sezgisel fonksiyondur. Izgara haritalarda Öklid uzaklığı $h(n)=\sqrt{(x_g-x_n)^2+(y_g-y_n)^2}$ olarak kullanılabilir.

Eğer $h(n)$ gerçek kalan maliyeti abartmıyorsa A*, en düşük maliyetli yolu bulmayı garanti eder. Ancak büyük veya çok boyutlu haritalarda bellekte tuttuğu açık ve kapalı düğüm kümeleri hızla büyüyebilir.

```python
from heapq import heappush, heappop

def astar(start, goal, neighbors, heuristic):
    queue = [(0, start)]
    cost = {start: 0}
    parent = {start: None}

    while queue:
        _, current = heappop(queue)
        if current == goal:
            return parent

        for nxt, step_cost in neighbors(current):
            new_cost = cost[current] + step_cost
            if nxt not in cost or new_cost < cost[nxt]:
                cost[nxt] = new_cost
                priority = new_cost + heuristic(nxt, goal)
                heappush(queue, (priority, nxt))
                parent[nxt] = current
```

Bu sade uygulama, komşuları değerlendirerek en umut verici düğümü öncelik kuyruğundan seçer. Dönen `parent` sözlüğü geriye doğru izlenerek yol oluşturulur.

## RRT: Boşluğa rastgele dallar uzatmak

RRT başlangıç durumunu ağacın kökü yapar. Ardından uzaydan rastgele bir $q_{rand}$ noktası seçer, ağaçtaki en yakın $q_{near}$ düğümünü bulur ve ona doğru sınırlı bir adım atarak $q_{new}$ üretir. Bağlantı engelle çakışmıyorsa yeni düğüm ağaca eklenir.

```python
def rrt(start, goal, sample, nearest, steer, collision_free):
    tree = [start]
    parent = {start: None}

    for _ in range(5000):
        random_state = sample(goal)
        near = nearest(tree, random_state)
        new = steer(near, random_state)

        if collision_free(near, new):
            tree.append(new)
            parent[new] = near
            if collision_free(new, goal):
                parent[goal] = new
                return parent
```

`sample(goal)` zaman zaman doğrudan hedefi seçerse **goal bias** uygulanır ve arama hızlanabilir. RRT bir çözümü çabuk bulabilir; fakat bulunan yol genellikle zikzaklıdır ve en kısa yol garantisi yoktur. Bu nedenle sonradan yol yumuşatma yapılır veya asimptotik olarak optimum çözüme yaklaşan RRT* kullanılır.

## Hızlı karşılaştırma

| Özellik | A* | RRT |
|---|---|---|
| Arama biçimi | Sistematik ve sezgisel | Rastgele örnekleme |
| Uzay | Ayrık grafik/ızgara | Sürekli konfigürasyon uzayı |
| Optimumluk | Uygun sezgiselle garantili | Temel sürümde garantisiz |
| Yüksek boyutlar | Maliyetli | Genellikle daha uygun |
| Sonuç yolu | Düzenli, maliyeti düşük | Zikzaklı, yumuşatma gerektirebilir |
| Tekrarlanabilirlik | Genellikle aynı sonuç | Rastgeleliğe bağlı |

## Hangisini seçmeli?

Depo robotu gibi iki boyutlu, bilinen bir maliyet haritasında çalışan sistemlerde A* güçlü ve öngörülebilir bir tercihtir. Robot kolu, insansız hava aracı veya karmaşık hareket kısıtları bulunan bir araç söz konusuysa RRT daha doğal olabilir. Pratik sistemler ikisini birleştirebilir: RRT ile uygulanabilir bir koridor bulunup A* veya optimizasyon yöntemleriyle yol iyileştirilebilir. Kısacası A* haritayı dikkatle okuyan bir kâşif, RRT ise hızla farklı yönlere dal uzatan bir öncüdür.
