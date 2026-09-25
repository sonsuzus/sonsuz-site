---
layout: post
title: "Ağaç İçi Mesafelerin Gizli Silahı: Centroid Decomposition"
math: true
categories: 
  - Bilgi
tags: 
  - centroid decomposition
  - ağaç algoritmaları
  - graf teorisi
  - mesafe sorguları
  - c++
  - rekabetçi programlama
toc: true
image: /img/agac-ici-mesafelerin-68.png
---

Bir ağaçta iki düğüm arasındaki mesafeyi hesaplamak kolaydır; fakat binlerce güncelleme ve sorgu geldiğinde işler hızla dallanıp budaklanır. Centroid Decomposition, ağacı dengeli biçimde parçalara ayırarak mesafe problemlerini yaklaşık $O(\log n)$ katman üzerinden çözmemizi sağlar. Kısacası ağacın fiziksel yapısını değiştirmeden, onun üzerinde ikinci ve dengeli bir “centroid ağacı” kurarız.


![agac-ici-mesafelerin-68](/img/agac-ici-mesafelerin-68.svg)

``

## Centroid nedir?

Bir ağacın centroid’i, kaldırıldığında geriye kalan bağlı bileşenlerin hiçbirinin toplam düğüm sayısının yarısından büyük olmadığı düğümdür. $n$ düğümlü bir ağaçta centroid $c$ ise her bileşen için şu koşul geçerlidir:

$$
\text{bileşenBoyutu} \leq \frac{n}{2}
$$

Her ağacın en az bir, en fazla iki centroid’i vardır. Algoritmada bunlardan herhangi birini seçebiliriz. Centroid’i kaldırır, oluşan alt ağaçların her birine aynı işlemi özyineli uygularız. Her seviyede parça boyutu en az yarıya indiğinden decomposition yüksekliği $O(\log n)$ olur.

| Yaklaşım | Güncelleme | Mesafe sorgusu | Ön işleme |
|---|---:|---:|---:|
| Her sorguda DFS/BFS | $O(1)$ | $O(n)$ | $O(1)$ |
| LCA ile sabit düğümler | Yok | $O(\log n)$ | $O(n\log n)$ |
| Centroid Decomposition | $O(\log n)$ | $O(\log n)$ | $O(n\log n)$ |

LCA iki belirli düğümün mesafesinde harikadır. Centroid Decomposition ise “işaretli en yakın düğüm”, “$k$ mesafedeki düğüm sayısı” veya dinamik renk güncellemeleri gibi toplu problemlerde parlar.

## Centroid nasıl bulunur?

Önce alt ağaç boyutlarını hesaplarız. Ardından boyutu toplamın yarısından büyük olan bir çocuk varsa o yöne ilerleriz. Böyle bir çocuk kalmadığında centroid’i bulmuş oluruz.

```cpp
int calcSize(int u, int p) {
    sub[u] = 1;
    for (int v : graph[u])
        if (v != p && !removed[v])
            sub[u] += calcSize(v, u);
    return sub[u];
}

int findCentroid(int u, int p, int total) {
    for (int v : graph[u])
        if (v != p && !removed[v] && sub[v] > total / 2)
            return findCentroid(v, u, total);
    return u;
}

void decompose(int entry, int parent) {
    int total = calcSize(entry, -1);
    int c = findCentroid(entry, -1, total);
    centroidParent[c] = parent;
    removed[c] = true;

    for (int v : graph[c])
        if (!removed[v]) decompose(v, c);
}
```

`removed` dizisi centroid olarak ayrılmış düğümlerin sonraki hesaplamalara katılmasını engeller. `centroidParent` ise yeni centroid ağacındaki ebeveyn ilişkisini saklar.

## En yakın işaretli düğüm uygulaması

Başlangıçta bazı düğümlerin kırmızı olduğunu düşünelim. Bir düğümü kırmızıya boyamak ve verilen $u$ düğümüne en yakın kırmızının mesafesini bulmak istiyoruz. Her centroid için kendisine en yakın kırmızı düğümün mesafesini `best` dizisinde tutarız.

```cpp
void paint(int u) {
    int x = u;
    while (x != -1) {
        best[x] = min(best[x], distance(u, x));
        x = centroidParent[x];
    }
}

int query(int u) {
    int answer = INF;
    int x = u;
    while (x != -1) {
        answer = min(answer, best[x] + distance(u, x));
        x = centroidParent[x];
    }
    return answer;
}
```

Buradaki `distance(a, b)` değeri LCA ile $O(\log n)$ sürede veya centroid atalarına ait önceden saklanmış mesafelerle $O(1)$ sürede alınabilir. İkinci seçenek kullanıldığında güncelleme ve sorgu doğrudan $O(\log n)$ olur.

Temel fikir şudur: Her düğüm yalnızca $O(\log n)$ centroid atasına sahiptir. Olası cevapları bu dengeli ata zinciri üzerinden birleştiririz. Böylece kocaman ağacı her sorguda dolaşmak yerine birkaç stratejik ağırlık merkezine uğrarız; algoritmik anlamda tam bir “merkeze çekilme” hareketi!
