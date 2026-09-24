---
layout: post
title: "Heavy-Light Decomposition: Ağaç Yollarını Segment Ağacına Taşımak"
math: true
categories: 
  - Bilgi
tags: 
  - heavy-light decomposition
  - segment ağacı
  - ağaç algoritmaları
  - veri yapıları
  - rekabetçi programlama
toc: true
image: /img/heavy-light-decomposition-19.png
---

Bir ağaçta “$u$ ile $v$ arasındaki düğümlerin toplamı nedir?” veya “bu yol üzerindeki bütün değerleri artır” gibi işlemler ilk bakışta masum görünür. Ancak her sorguda yolu adım adım yürümek, çarpık bir ağaçta $O(n)$ zaman harcatabilir. Heavy-Light Decomposition, kısaca HLD, ağacı değiştirmek yerine yolları akıllıca numaralandırır ve zor görünen yol işlemlerini segment ağacının sevdiği dizi aralıklarına dönüştürür.
``
## Temel fikir: Ağır çocuk kimdir?

Önce her düğüm için alt ağaç boyutu hesaplanır. Bir düğümün çocukları arasından alt ağacı en büyük olan çocuk **ağır çocuk**, diğerleri ise **hafif çocuk** kabul edilir. Ağır çocukla kurulan kenar ağır, kalan kenarlar hafiftir.

Buradaki kritik gözlem şudur: Hafif bir kenardan aşağı indiğimizde ulaşılan alt ağacın boyutu en fazla mevcut alt ağacın yarısıdır. Aksi durumda o çocuk ağır çocuk olurdu. Dolayısıyla kökten herhangi bir düğüme giderken en fazla

$$O(\log n)$$

adet hafif kenar geçilebilir. Ağır kenarlar art arda birleştirilerek **zincirler** oluşturulur. Böylece herhangi iki düğüm arasındaki yol en fazla $O(\log n)$ zincir parçasına ayrılır.

| Yaklaşım | Yol sorgusu | Nokta güncelleme | Ek yapı |
|---|---:|---:|---|
| Yolu doğrudan yürümek | $O(n)$ | $O(1)$ | Yok |
| HLD + segment ağacı | $O(\log^2 n)$ | $O(\log n)$ | Segment ağacı |
| HLD + Fenwick ağacı | $O(\log^2 n)$ | $O(\log n)$ | Fenwick ağacı |

## Ağacı diziye dönüştürmek

Her ağır zincirin düğümleri dizide ardışık konumlara yerleştirilir. `head[u]`, düğümün bulunduğu zincirin başını; `pos[u]`, segment ağacındaki konumunu; `parent[u]` ve `depth[u]` ise ebeveyn ile derinliği saklar.

İlk DFS alt ağaç boyutlarını ve ağır çocukları bulur:

```cpp
void dfs(int u, int p) {
    parent[u] = p;
    size[u] = 1;
    heavy[u] = -1;

    for (int v : graph[u]) {
        if (v == p) continue;
        depth[v] = depth[u] + 1;
        dfs(v, u);
        size[u] += size[v];

        if (heavy[u] == -1 || size[v] > size[heavy[u]])
            heavy[u] = v;
    }
}
```

İkinci DFS, ağır çocuğu aynı zincirde tutarak düğümlere doğrusal konum verir:

```cpp
void decompose(int u, int h) {
    head[u] = h;
    pos[u] = currentPos++;

    if (heavy[u] != -1)
        decompose(heavy[u], h);

    for (int v : graph[u]) {
        if (v == parent[u] || v == heavy[u]) continue;
        decompose(v, v);
    }
}
```

Bu sıralama sayesinde aynı zincirdeki iki düğüm arasındaki yol, segment ağacında tek bir `[l, r]` aralığıdır.

## İki düğüm arasındaki sorgu

`u` ve `v` farklı zincirlerdeyse, zincir başı daha derinde olan taraf yukarı taşınır. Taşınmadan önce ilgili zincir parçası sorgulanır. İki düğüm aynı zincire geldiğinde kalan son aralık işlenir.

```cpp
long long queryPath(int u, int v) {
    long long answer = 0;

    while (head[u] != head[v]) {
        if (depth[head[u]] < depth[head[v]]) swap(u, v);

        answer += segmentTree.query(pos[head[u]], pos[u]);
        u = parent[head[u]];
    }

    if (depth[u] > depth[v]) swap(u, v);
    answer += segmentTree.query(pos[u], pos[v]);
    return answer;
}
```

Her zincir geçişi en fazla $O(\log n)$ kez gerçekleşir. Her parça için segment ağacı sorgusu da $O(\log n)$ olduğundan toplam karmaşıklık

$$O(\log n) \times O(\log n) = O(\log^2 n)$$

olur. Toplam yerine minimum, maksimum veya XOR kullanılabilir. Yol güncellemelerinde ise lazy propagation destekli segment ağacı tercih edilir.

HLD’nin küçük tuzağı, işlemin düğümlerde mi yoksa kenarlarda mı tutulduğudur. Kenar değerleri genellikle daha derindeki düğümün konumuna yazılır; son aynı-zincir sorgusunda ortak atanın konumu dışarıda bırakılır. Bu ayrıntı doğru yönetildiğinde HLD, ağacı adeta fermuarlı bir diziye çevirir: yolu aç, logaritmik parçaları işle ve tekrar kapat!

![heavy-light-decomposition-19](/img/heavy-light-decomposition-19.svg)

