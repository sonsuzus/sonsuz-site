---
layout: post
title: "Ağır-Hafif Ayrıştırma: Ağaç Yollarını Logaritmik Hızda Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - heavy-light-decomposition
  - ağaç-algoritmaları
  - segment-tree
toc: true
---

Bir ağaçta iki düğüm arasındaki yolu bulmak kolaydır; ancak yüz binlerce düğüm ve sorgu devreye girdiğinde masum bir yürüyüş performans canavarına dönüşür. Ağır-Hafif Ayrıştırma, yani Heavy-Light Decomposition (HLD), uzun yolları birkaç doğrusal parçaya bölerek sorgu ve güncellemeleri Segment Tree gibi veri yapılarıyla hızlandırır.
``

## Temel fikir: Her çocuk aynı ağırlıkta değildir

Köklenmiş bir ağaçta her düğüm için alt ağaç boyutunu hesaplayalım. Bir $v$ düğümünün çocukları arasında alt ağacı en büyük olan çocuk **ağır çocuk**, diğerleri ise **hafif çocuk** kabul edilir.

$$size(v)=1+\sum_{u \in children(v)} size(u)$$

Ağır çocukla kurulan kenara ağır, diğer kenarlara hafif kenar denir. Ağır kenarlar birleşerek **ağır zincirleri** oluşturur. Her düğüm tam olarak bir zincire aittir.

Asıl sihir hafif kenarlardadır. Bir düğümden hafif bir çocuğa geçtiğimizde alt ağaç boyutu en az yarıya iner. Bu nedenle kökten herhangi bir düğüme giden yolda en fazla $O(\log n)$ hafif kenar bulunabilir. Dolayısıyla iki düğüm arasındaki yol da en fazla $O(\log n)$ ağır zincir parçasına ayrılır.

| Yaklaşım | Yol sorgusu | Yol güncellemesi | Ek bellek |
|---|---:|---:|---:|
| Düğümleri tek tek dolaşma | $O(n)$ | $O(n)$ | $O(n)$ |
| HLD + Segment Tree | $O(\log^2 n)$ | $O(\log^2 n)$ | $O(n)$ |
| Sadece LCA | LCA için $O(\log n)$ | Uygun değil | $O(n\log n)$ |

Burada küçük ama önemli bir ayrıntı vardır: HLD yolu $O(\log n)$ parçaya böler; her parçadaki Segment Tree işlemi de $O(\log n)$ sürdüğü için genel karmaşıklık çoğunlukla $O(\log^2 n)$ olur.

## Ağacı doğrusal diziye dönüştürmek

Önce bir DFS ile alt ağaç boyutları, ebeveynler, derinlikler ve ağır çocuklar hesaplanır. İkinci DFS ise aynı ağır zincirdeki düğümleri dizide art arda yerleştirir. Böylece ağaç üzerindeki bir zincir, Segment Tree üzerinde kesintisiz bir aralığa dönüşür.

Her düğüm için şu bilgiler tutulur:

- `parent[v]`: Ebeveyni
- `depth[v]`: Derinliği
- `heavy[v]`: Ağır çocuğu
- `head[v]`: Bulunduğu zincirin başı
- `pos[v]`: Doğrusal dizideki konumu

```cpp
vector<vector<int>> g;
vector<int> parent, depth, sz, heavy, head, pos;
int timer = 0;

int dfs(int v, int p) {
    parent[v] = p;
    sz[v] = 1;
    int bestSize = 0;

    for (int u : g[v]) {
        if (u == p) continue;
        depth[u] = depth[v] + 1;
        int childSize = dfs(u, v);
        sz[v] += childSize;

        if (childSize > bestSize) {
            bestSize = childSize;
            heavy[v] = u;
        }
    }
    return sz[v];
}

void decompose(int v, int chainHead) {
    head[v] = chainHead;
    pos[v] = timer++;

    if (heavy[v] != -1)
        decompose(heavy[v], chainHead);

    for (int u : g[v]) {
        if (u == parent[v] || u == heavy[v]) continue;
        decompose(u, u);
    }
}
```

İlk fonksiyon ağır çocukları belirler. İkinci fonksiyon ağır çocuğu önce ziyaret ederek zincirdeki düğümlerin dizide yan yana kalmasını sağlar.

## Yol sorgusu ve güncellemesi

İki düğüm farklı zincirlerdeyken daha derindeki zincirin başından yukarı sıçrarız. Her sıçrayışta ilgili doğrusal aralığı Segment Tree üzerinden işleriz.

```cpp
long long queryPath(int a, int b) {
    long long answer = 0;

    while (head[a] != head[b]) {
        if (depth[head[a]] < depth[head[b]]) swap(a, b);
        answer += st.query(pos[head[a]], pos[a]);
        a = parent[head[a]];
    }

    if (depth[a] > depth[b]) swap(a, b);
    answer += st.query(pos[a], pos[b]);
    return answer;
}

void addPath(int a, int b, int value) {
    while (head[a] != head[b]) {
        if (depth[head[a]] < depth[head[b]]) swap(a, b);
        st.add(pos[head[a]], pos[a], value);
        a = parent[head[a]];
    }

    if (depth[a] > depth[b]) swap(a, b);
    st.add(pos[a], pos[b], value);
}
```

Buradaki `st.query` aralık toplamını, `st.add` ise lazy propagation kullanan aralık güncellemesini temsil eder. Düğüm değerleri yerine kenar değerleri tutuluyorsa son zincirde LCA düğümünün konumu hariç bırakılmalıdır.

HLD; yol toplamı, maksimum değer, renk değiştirme ve kenar ağırlığı güncelleme gibi dinamik problemlerde güçlüdür. Biraz DFS, biraz Segment Tree ve doğru zincir yönetimiyle devasa ağaçlar artık korkutucu bir orman değil, düzenli birkaç otoyoldur.
