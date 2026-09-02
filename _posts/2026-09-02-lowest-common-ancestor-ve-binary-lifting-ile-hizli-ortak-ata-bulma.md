---
layout: post
title: "Lowest Common Ancestor ve Binary Lifting ile Hızlı Ortak Ata Bulma"
math: true
categories: 
  - Bilgi
tags: 
  - lca
  - binary lifting
  - ağaç algoritmaları
toc: true
---

Bir soy ağacında iki kişinin ortak atasını aramak kolay görünebilir; ancak yüz binlerce düğümlü bir ağaçta binlerce sorgu sorulduğunda işler hızla karışır. **Lowest Common Ancestor (LCA)**, iki düğümün ikisine de ata olan en derin düğümü bulur. Binary Lifting ise ön işleme yaparak bu sorguyu oldukça hızlı cevaplamamızı sağlar.
``
## LCA tam olarak nedir?

Köklü bir ağaçta $u$ ve $v$ düğümlerinin LCA'sı, her iki düğümün de atası olan ve kökten en uzakta bulunan düğümdür. İki farklı yaprak düşünelim. Bu yapraklardan köke doğru yürüdüğümüzde yollarının ilk birleştiği düğüm, aradığımız en yakın ortak atadır.

Basit yaklaşımda derin olan düğümü yukarı çıkarır, ardından iki düğümü birlikte ebeveynlerine taşırız. Ağacın yüksekliği $H$ ise tek sorgunun maliyeti $O(H)$ olur. Dengesiz bir ağaçta $H=N$ olabileceğinden çok sayıda sorgu pahalıdır.

| Yöntem | Ön işleme | Sorgu | Bellek |
|---|---:|---:|---:|
| Ebeveynlere tek tek çıkma | $O(N)$ | $O(N)$ | $O(N)$ |
| Binary Lifting | $O(N\log N)$ | $O(\log N)$ | $O(N\log N)$ |

## Binary Lifting fikri

Her düğüm için yalnızca doğrudan ebeveyni değil, ikinin kuvvetleri kadar yukarıdaki ataları saklarız:

$$up[v][j] = v \text{ düğümünün } 2^j \text{ adım yukarıdaki atası}$$

İlk sütun doğrudan ebeveyndir:

$$up[v][0] = parent(v)$$

Daha uzun sıçramalar önceki sonuçlardan üretilir:

$$up[v][j] = up[up[v][j-1]][j-1]$$

Örneğin $up[v][3]$, düğümün $2^3=8$ seviye yukarısındaki atasıdır. Sekiz adım tek tek yürümek yerine tek tablo erişimi yapılır. Bir uzaklık, ikilik gösterimindeki kuvvetlere ayrılarak en fazla $O(\log N)$ sıçramayla tamamlanır.

## Sorgu stratejisi

Önce iki düğümün derinliklerini eşitleriz. $u$ daha derindeyse aradaki

$$d = depth[u]-depth[v]$$

farkını Binary Lifting ile kapatırız. Düğümler eşitlenince aynı düğüme geldilerse LCA bulunmuştur. Aksi durumda en büyük sıçramadan küçüğe doğru ilerleriz. İki düğümün $2^j$ yukarıdaki ataları farklıysa ikisini de oraya taşırız. İşlem bittiğinde düğümler LCA'nın hemen altında kalır; dolayısıyla doğrudan ebeveyn cevap olur.

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
const int LOG = 20;
vector<int> tree[MAXN];
int up[MAXN][LOG], depthNode[MAXN];

// DFS, derinlikleri ve 2^j uzaklıktaki ataları hazırlar.
void dfs(int node, int parent) {
    up[node][0] = parent;

    for (int j = 1; j < LOG; ++j)
        up[node][j] = up[up[node][j - 1]][j - 1];

    for (int next : tree[node]) {
        if (next == parent) continue;
        depthNode[next] = depthNode[node] + 1;
        dfs(next, node);
    }
}

int lca(int u, int v) {
    if (depthNode[u] < depthNode[v]) swap(u, v);

    int difference = depthNode[u] - depthNode[v];
    for (int j = LOG - 1; j >= 0; --j)
        if (difference & (1 << j))
            u = up[u][j];

    if (u == v) return u;

    for (int j = LOG - 1; j >= 0; --j) {
        if (up[u][j] != up[v][j]) {
            u = up[u][j];
            v = up[v][j];
        }
    }

    return up[u][0];
}
```

`LOG` değeri, $\lceil\log_2 N\rceil+1$ seviyeyi kapsamalıdır. Kök düğüm için ebeveyn olarak yine kökü vermek, tablo erişimlerini güvenli tutar. Çok derin ağaçlarda özyinelemeli DFS yığın taşmasına yol açabileceği için iteratif DFS tercih edilebilir.

## Neden ön işleme kazandırır?

Binary Lifting, başlangıçta daha fazla zaman ve bellek harcayıp sonraki sorguları hızlandıran klasik bir takastır. $Q$ sorgu için toplam maliyet

$$O(N\log N + Q\log N)$$

olur. Bu nedenle yöntem; yol uzunluğu hesaplama, sanal ağaç oluşturma ve çevrim içi ata sorguları gibi problemlerde güçlüdür. Kısacası ağaçta merdivenleri tek tek çıkmak yerine asansör duraklarını önceden kaydederiz!
