---
layout: post
title: "Minimum Yayılma Ağacı Yarışı: Kruskal, Prim ve Borůvka"
math: true
categories: 
  - Bilgi
tags: 
  - graf
  - algoritma
  - kruskal
  - prim
  - boruvka
  - minimum-yayılma-ağacı
toc: true
image: /img/minimum-yayilma-agaci-46.png
---

Bir şehirdeki tüm mahalleleri fiber kabloyla bağlamak istediğinizi düşünün. Her bağlantının farklı bir maliyeti var ve hedefiniz, hiçbir mahalleyi yalnız bırakmadan mümkün olan en az kabloyu kullanmak. İşte Minimum Yayılma Ağacı algoritmaları tam olarak bu problemi çözer. Kruskal kenarları sıraya dizer, Prim tek bir noktadan büyür, Borůvka ise bütün bileşenleri aynı anda harekete geçirir.


![minimum-yayilma-agaci-46](/img/minimum-yayilma-agaci-46.svg)

``

## Minimum Yayılma Ağacı nedir?

Bağlı, yönsüz ve ağırlıklı bir $G=(V,E)$ grafında **yayılma ağacı**, bütün düğümleri içeren, döngüsüz bir alt graftır. $\vert V\vert =n$ düğümlü her yayılma ağacında tam olarak $n-1$ kenar bulunur.

Minimum Yayılma Ağacı, kenar ağırlıkları toplamı en küçük olan yayılma ağacıdır:

$$
w(T)=Σ_{e \in T} w(e)
$$

Burada $T$, seçilen kenar kümesini; $w(e)$ ise bir kenarın maliyetini gösterir. Ağırlıklar farklıysa sonuç tektir. Eşit ağırlıklar varsa birden fazla doğru minimum ağaç bulunabilir.

Algoritmaların temelinde **kesim özelliği** vardır: Grafı iki parçaya ayıran herhangi bir kesimi geçen en hafif güvenli kenar, bir minimum yayılma ağacına eklenebilir. Ayrıca bir döngüdeki en ağır kenarı seçmemek güvenlidir. Üç yöntem aynı matematiksel gerçeği farklı stratejilerle kullanır.

## Yöntemlerin çalışma biçimi

| Algoritma | Temel strateji | Kullanılan yapı | Uygun olduğu durum |
|---|---|---|---|
| Kruskal | En ucuz kenarları sırayla seçer | Union-Find | Seyrek graflar |
| Prim | Tek ağaçtan en ucuz dış kenara ilerler | Öncelik kuyruğu | Yoğun veya bağlı graflar |
| Borůvka | Her bileşenin en ucuz kenarını aynı turda seçer | Union-Find | Paralel hesaplama |

### Kruskal: Ucuzdan pahalıya

Kruskal bütün kenarları ağırlıklarına göre sıralar. Bir kenar, uçları daha önce aynı bileşende değilse ağaca eklenir. Union-Find yapısı, döngü oluşup oluşmadığını hızlıca denetler.

```python
def kruskal(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree = []
    for cost, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:              # Eklenirse döngü oluşmaz
            parent[ru] = rv
            tree.append((u, v, cost))
    return tree
```

Sıralama baskın olduğu için karmaşıklığı $O(E \log E)$ düzeyindedir. Kenar sayısı azsa oldukça pratiktir.

### Prim: Ağacı adım adım büyüt

Prim herhangi bir düğümden başlar. Oluşan ağaç ile henüz ziyaret edilmemiş düğümler arasındaki en ucuz kenarı seçer. Öncelik kuyruğu kullanılan komşuluk listesi uygulamasının maliyeti $O(E \log V)$ olur.

```python
import heapq

def prim(graph, start=0):
    visited, tree = set(), []
    heap = [(0, start, -1)]

    while heap:
        cost, node, parent = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        if parent != -1:
            tree.append((parent, node, cost))
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(heap, (weight, neighbor, node))
    return tree
```

Prim, yalnızca ulaştığı bileşeni kapsar; bu nedenle başlangıç grafının bağlı olması gerekir.

### Borůvka: Herkes aynı anda seçim yapsın

Borůvka başlangıçta her düğümü ayrı bir bileşen kabul eder. Her turda her bileşen dışarıya giden en ucuz kenarını seçer ve bileşenler birleştirilir. Bileşen sayısı her turda en az yarıya yaklaşarak azaldığından yaklaşık $O(\log V)$ tur gerekir. Toplam karmaşıklık tipik olarak $O(E \log V)$ olur.

Borůvka’nın seçimleri bağımsız biçimde hesaplanabildiği için paralel sistemlerde güçlüdür. Hatta modern hibrit çözümler, önce Borůvka ile grafı küçültüp sonra Kruskal veya Prim çalıştırabilir.

## Hangisini seçmelisiniz?

Sıralanması kolay, seyrek bir kenar listeniz varsa **Kruskal**; komşuluk listesiyle temsil edilen bağlı bir grafınız varsa **Prim**; dağıtık veya paralel işlem hedefliyorsanız **Borůvka** iyi bir başlangıçtır. Graf bağlı değilse tek ağaç üretilemez; bunun yerine her bileşen için minimum ağaçlardan oluşan bir **minimum yayılma ormanı** elde edilir. Üç algoritmanın rotası farklı olsa da vardıkları ekonomik sonuç aynıdır: tüm düğümleri, döngü kurmadan ve toplam maliyeti mümkün olduğunca düşük tutarak bağlamak.
