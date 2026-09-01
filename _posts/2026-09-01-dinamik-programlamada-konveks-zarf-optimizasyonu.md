---
layout: post
title: "Dinamik Programlamada Konveks Zarf Optimizasyonu"
math: true
categories: 
  - Bilgi
tags: 
  - dinamik programlama
  - konveks zarf
  - algoritma optimizasyonu
toc: true
---

Dinamik programlama bazen doğru bağıntıyı bulduğumuz hâlde bizi $O(n^2)$ karmaşıklığıyla baş başa bırakır. Her durum için önceki bütün durumları denemek, küçük girdilerde masum görünürken yüz bin elemanda bilgisayarı düşünsel bir inzivaya sokabilir. Eğer geçiş maliyeti belirli biçimde doğrusal fonksiyonlara ayrılabiliyorsa **Konveks Zarf Optimizasyonu** veya yaygın adıyla **Convex Hull Trick (CHT)**, bu aramayı geometrik bir probleme dönüştürerek ciddi biçimde hızlandırır.
``
## DP bağıntısından doğruya giden yol

Aşağıdaki klasik geçişi ele alalım:

$$dp[i] = min_{j<i} \{dp[j] + (S_i-S_j)^2 + C\}$$

Kareyi açtığımızda bağıntı şu hâle gelir:

$$dp[i] = S_i^2 + C + min_{j<i} \{(-2S_j)S_i + dp[j] + S_j^2\}$$

Buradaki sihirli gözlem şudur: $i$ sabitken $S_i$ bir sorgu noktasıdır. Her $j$ ise

$$y = m_jx + b_j$$

biçiminde bir doğru üretir. Eşleştirme yaparsak $x=S_i$, $m_j=-2S_j$ ve $b_j=dp[j]+S_j^2$ olur. Dolayısıyla her adımda yeni bir doğru ekler, mevcut doğrular arasından verilen $x$ noktasında en küçük değeri üreteni sorarız.

| DP kavramı | Geometrik karşılığı |
|---|---|
| Önceki durum $j$ | Bir doğru |
| $S_i$ | Sorgulanan $x$ koordinatı |
| Geçiş maliyeti | Doğrunun $y$ değeri |
| Minimum geçiş | Alt zarftaki en iyi doğru |

## Konveks zarf neden işe yarar?

Bütün doğruları saklamak yeterli değildir; aksi hâlde her sorguda yine hepsini dolaşırız. CHT, hiçbir sorguda en iyi olamayacak doğruları siler. Kalan doğruların minimum değerleri geometrik olarak bir **alt konveks zarf** oluşturur.

Eğer eğimler monoton sırayla ekleniyor ve sorgu noktaları da monoton ilerliyorsa doğruları bir `deque` içinde tutabiliriz. Yeni doğru eklenirken ortadaki bir doğru gereksiz hâle gelmişse arkadan çıkarılır. Sorgu sırasında ikinci doğru birinciden daha iyiyse öndeki doğru silinir. Her doğru en fazla bir kez eklenip bir kez çıkarıldığı için toplam çalışma süresi $O(n)$ olur.

| Yaklaşım | Ekleme | Sorgu | Toplam DP maliyeti |
|---|---:|---:|---:|
| Bütün geçişleri deneme | $O(1)$ | $O(n)$ | $O(n^2)$ |
| Monoton CHT | Amortize $O(1)$ | Amortize $O(1)$ | $O(n)$ |
| Li Chao ağacı | $O(log X)$ | $O(log X)$ | $O(n log X)$ |

## C++ ile monoton CHT

Aşağıdaki yapı minimum sorgusu yapar. Eğimlerin azalan, sorgu değerlerinin ise artan sırada geldiği varsayılır:

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Line {
    long long m, b;
    long long value(long long x) const {
        return m * x + b;
    }
};

struct ConvexHullTrick {
    deque<Line> hull;

    bool unnecessary(const Line& a, const Line& b,
                     const Line& c) {
        return (__int128)(b.b - a.b) * (b.m - c.m) >=
               (__int128)(c.b - b.b) * (a.m - b.m);
    }

    void add(long long m, long long b) {
        Line current{m, b};
        while (hull.size() >= 2 &&
               unnecessary(hull[hull.size() - 2], hull.back(), current))
            hull.pop_back();
        hull.push_back(current);
    }

    long long query(long long x) {
        while (hull.size() >= 2 &&
               hull[0].value(x) >= hull[1].value(x))
            hull.pop_front();
        return hull.front().value(x);
    }
};
```

`unnecessary` fonksiyonu kesişim noktalarını bölme yapmadan karşılaştırır. `__int128` kullanılması, çarpımlar sırasında `long long` taşması riskini azaltır. Başlangıçta $S_0=0$ ve $dp[0]=0$ doğrusu eklenerek her $i$ için `query(S[i])` çağrılabilir; ardından o duruma ait yeni doğru zarfa eklenir.

## Ne zaman kullanmalıyız?

CHT için geçişin $m_jx_i+b_j$ biçimine ayrılabilmesi gerekir. Eğimler veya sorgular monoton değilse basit `deque` sürümü güvenli değildir; Li Chao ağacı ya da ikili aramalı dinamik zarf tercih edilmelidir. Kısacası önce cebiri düzenleyin, sonra geometrinin bedava hızlandırmasını alın. Bazen hızlı DP yazmanın yolu daha fazla DP değil, birkaç doğru çizmektir!
