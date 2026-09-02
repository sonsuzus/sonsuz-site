---
layout: post
title: "Minimum Kapsayan Ağaçlarda Borůvka Algoritması: Paralelliğe Açılan Yol"
math: true
categories: 
  - Bilgi
tags: 
  - boruvka algoritması
  - minimum kapsayan ağaç
  - paralel programlama
toc: true
---

Bir şehirdeki tüm veri merkezlerini mümkün olan en düşük kablo maliyetiyle bağlamak istediğinizi düşünün. Her merkez diğer merkezlerle bağlantı kurabilir, ancak bütçe sınırlıdır. İşte Minimum Kapsayan Ağaç (Minimum Spanning Tree, MST) problemi tam olarak bu tür senaryoları çözer. Borůvka algoritması ise MST ailesinin özellikle paralel çalışmaya hevesli, aynı anda birçok işe el atan üyesidir.

``

## Önce MST Mantığını Hatırlayalım

Bağlı, yönsüz ve ağırlıklı bir grafik $G=(V,E)$ için kapsayan ağaç, bütün düğümleri birbirine bağlayan ve döngü içermeyen bir kenar kümesidir. $\vert V\vert $ düğümlü her kapsayan ağaçta tam olarak $\vert V\vert -1$ kenar bulunur.

Amaç, seçilen kenarların toplam ağırlığını en aza indirmektir:

$$
T^* = \underset{T}{\operatorname{argmin}} \sum_{e \in T} w(e)
$$

Burada $w(e)$, ilgili kenarın maliyetidir. Borůvka algoritmasının temel fikri şaşırtıcı derecede doğaldır: **Her bileşen, dış dünyaya açılan en ucuz kenarı aynı anda seçer.**

## Borůvka Nasıl Çalışır?

Başlangıçta her düğüm tek başına bir bileşen kabul edilir. Ardından aşağıdaki tur tekrarlanır:

1. Her bağlı bileşen için başka bir bileşene giden en ucuz kenar bulunur.
2. Bulunan kenarlar MST adayına eklenir.
3. Bu kenarların bağladığı bileşenler birleştirilir.
4. Tek bir bileşen kalıncaya kadar devam edilir.

Bir turda bileşen sayısı en azından yaklaşık yarıya düşer. Bu nedenle tur sayısı $O(\log \vert V\vert )$ olur. Her turda bütün kenarlar incelenirse toplam zaman karmaşıklığı:

$$
O(\vert E\vert \log \vert V\vert )
$$

Bu yaklaşımın güvenli olmasını **kesme özelliği** açıklar: Bir bileşeni grafiğin geri kalanından ayıran kesitteki en hafif kenar, bir MST içerisinde bulunabilir.

## Diğer MST Algoritmalarıyla Karşılaştırma

| Özellik | Borůvka | Kruskal | Prim |
|---|---|---|---|
| Temel hareket | Her bileşenin en ucuz kenarı | Küresel olarak en ucuz kenar | Ağacı en ucuz kenarla büyütme |
| Paralelleştirme | Çok uygun | Sıralama nedeniyle sınırlı | Genellikle daha zor |
| Kullanılan yapı | Union-Find | Union-Find | Öncelik kuyruğu |
| Tipik karmaşıklık | $O(E\log V)$ | $O(E\log E)$ | $O(E\log V)$ |
| Dağıtık sistem uyumu | Yüksek | Orta | Düşük/orta |

Borůvka’nın yıldızının parladığı nokta, bileşenlerin en ucuz kenarlarını birbirinden büyük ölçüde bağımsız arayabilmesidir. Kenarlar işlemcilere, sunuculara veya GPU iş parçacıklarına dağıtılabilir; her çalışan yerel adayını bulur ve sonuçlar indirgeme işlemiyle birleştirilir.

## Python ile Orta Düzey Bir Uygulama

Aşağıdaki kod, bileşenleri verimli biçimde yönetmek için Union-Find kullanır:

```python
def boruvka(n, edges):
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        a, b = find(a), find(b)
        if a == b:
            return False
        if rank[a] < rank[b]:
            a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]:
            rank[a] += 1
        return True

    mst, total = [], 0
    components = n

    while components > 1:
        cheapest = {}

        for u, v, weight in edges:
            ru, rv = find(u), find(v)
            if ru == rv:
                continue
            if ru not in cheapest or weight < cheapest[ru][2]:
                cheapest[ru] = (u, v, weight)
            if rv not in cheapest or weight < cheapest[rv][2]:
                cheapest[rv] = (u, v, weight)

        if not cheapest:
            raise ValueError("Grafik bağlı değil")

        for u, v, weight in cheapest.values():
            if union(u, v):
                mst.append((u, v, weight))
                total += weight
                components -= 1

    return mst, total
```

`cheapest` sözlüğü her bileşenin en ucuz dış kenarını tutar. Aynı kenar iki bileşen tarafından seçilebildiği için `union` işlemi, kenarın yalnızca gerektiğinde eklenmesini ve döngü oluşmamasını sağlar.

## Paralel Dünyadaki Yeri

Borůvka; büyük ölçekli ağ analizi, coğrafi bilgi sistemleri, kümeleme ve dağıtık grafik motorlarında kullanışlıdır. Hibrit çözümlerde önce Borůvka ile grafik hızla küçültülür, sonra Kruskal veya Prim uygulanır. Kısacası Borůvka yalnızca bir MST algoritması değil, büyük grafikleri işlemcilere paylaştırmanın son derece zarif bir yoludur.
