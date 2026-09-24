---
layout: post
title: "Ağaçlarda Euler Turu Tekniği: Alt Ağaçları Tek Boyutlu Dizide Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - euler-turu
  - ağaçlar
  - segment-ağacı
  - veri-yapıları
  - rekabetçi-programlama
toc: true
image: /img/agaclarda-euler-turu-67.png
---

![agaclarda-euler-turu-67](/img/agaclarda-euler-turu-67.svg)


Bir şirket hiyerarşisindeki yöneticileri, dosya sistemindeki klasörleri veya bir oyundaki yetenek ağacını düşünün. Bu yapılarda “X düğümünün altındaki bütün değerlerin toplamı nedir?” gibi sorgular sıkça karşımıza çıkar. Ağacı her sorguda yeniden dolaşmak pahalıdır; Euler Turu Tekniği (ETT), alt ağaçları tek boyutlu ve kesintisiz dizi aralıklarına dönüştürerek segment ağacının süper güçlerinden yararlanmamızı sağlar.

``

## Temel fikir: Ağacı ütülemek

Köklü bir ağaçta DFS dolaşması yaparken her düğüme giriş zamanını `tin[v]` olarak kaydedelim. Düğümün bütün çocuklarını ziyaret ettikten sonra da alt ağacının bittiği konumu `tout[v]` ile işaretleyelim.

DFS, bir düğüme girdikten sonra başka bir dala geçmeden önce o düğümün tüm torunlarını ziyaret eder. Dolayısıyla `v` düğümünün alt ağacındaki düğümler, oluşturduğumuz dizide şu kesintisiz aralığa yerleşir:

$$
subtree(v) \longleftrightarrow [tin[v],\ tout[v]]
$$

Düğüm değerlerini giriş sırasına göre `flat` dizisine yazarsak alt ağaç toplamı artık ağaç üzerinde değil, sıradan bir aralık üzerinde hesaplanır:

$$
S(v)=\sum_{i=tin[v]}^{tout[v]} flat[i]
$$

Örneğin DFS sırası `A, B, D, E, C, F` olsun. `B` düğümünün altında `B, D, E` bulunuyorsa bunlar dizide yan yana durur. Ağaç karmaşık görünse bile sorgu yalnızca `[1, 3]` aralığıdır. Kısacası ağaç ütülenmiş, kırışıklıklar kaybolmuştur!

| İşlem | Doğrudan DFS | ETT + Segment Ağacı |
|---|---:|---:|
| Ön işleme | Yok | $O(n)$ |
| Alt ağaç toplamı | $O(k)$ | $O(\log n)$ |
| Tek düğüm güncelleme | $O(1)$ | $O(\log n)$ |
| Bellek | $O(n)$ | $O(n)$ |

Buradaki $k$, sorgulanan alt ağaçtaki düğüm sayısıdır. Ağaç zincir şeklindeyse $k$, $n$ kadar büyüyebilir.

## Euler dizisini oluşturmak

Aşağıdaki Python kodu, her düğümü yalnızca giriş anında diziye ekleyen yaygın ETT çeşidini uygular:

```python
def build_euler(graph, values, root=0):
    n = len(graph)
    tin = [0] * n
    tout = [0] * n
    flat = []

    def dfs(node, parent):
        tin[node] = len(flat)
        flat.append(values[node])

        for child in graph[node]:
            if child != parent:
                dfs(child, node)

        tout[node] = len(flat) - 1

    dfs(root, -1)
    return tin, tout, flat
```

`tin[node]`, düğümün değerinin `flat` içindeki konumudur. `tout[node]` ise son torunun konumunu gösterir. Böylece alt ağaç aralığı iki indeksle temsil edilir.

## Segment ağacıyla sorgulamak

Aşağıdaki sınıf noktasal güncelleme ve aralık toplamı işlemlerini $O(\log n)$ zamanda gerçekleştirir:

```python
class SegmentTree:
    def __init__(self, data):
        size = 1
        while size < len(data):
            size *= 2
        self.size = size
        self.tree = [0] * (2 * size)

        for i, value in enumerate(data):
            self.tree[size + i] = value
        for i in range(size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index, value):
        i = self.size + index
        self.tree[i] = value
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def query(self, left, right):
        left += self.size
        right += self.size
        total = 0
        while left <= right:
            if left % 2 == 1:
                total += self.tree[left]
                left += 1
            if right % 2 == 0:
                total += self.tree[right]
                right -= 1
            left //= 2
            right //= 2
        return total
```

Kullanımı oldukça nettir:

```python
tin, tout, flat = build_euler(graph, values)
segment = SegmentTree(flat)

subtree_sum = segment.query(tin[v], tout[v])
segment.update(tin[v], new_value)
```

## İnce noktalar

ETT’nin farklı tanımları vardır. Bazı sürümlerde düğüm hem girişte hem çıkışta kaydedilir. Alt ağaç sorgularında genellikle her düğümü bir kez yazan sürüm daha pratiktir. Aralıkların kapalı mı `[l, r]`, yoksa yarı açık mı `[l, r)` olduğunu da baştan belirlemek önemlidir; indeks hatalarının doğal yaşam alanı tam olarak burasıdır.

Ağaç değişmiyor fakat değerler güncelleniyorsa ETT mükemmel bir seçimdir. Yalnızca toplam gerekiyorsa Fenwick ağacı da kullanılabilir. Minimum, maksimum veya daha gelişmiş birleştirme işlemlerinde ise segment ağacı daha esnektir. Sonuç olarak ETT tek başına sorguları cevaplamaz; ağacın geometrisini, güçlü dizi veri yapılarına uygun bir forma dönüştüren zekice bir köprüdür.
