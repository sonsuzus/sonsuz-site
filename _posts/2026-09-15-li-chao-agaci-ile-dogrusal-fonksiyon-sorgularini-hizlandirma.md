---
layout: post
title: "Li Chao Ağacı ile Doğrusal Fonksiyon Sorgularını Hızlandırma"
math: true
categories: 
  - Bilgi
tags: 
  - li chao ağacı
  - veri yapıları
  - algoritma
  - dinamik programlama
  - c++
  - optimizasyon
toc: true
image: /img/li-chao-agaci-13.png
---

Elimizde sürekli yeni doğruların eklendiği ve belirli bir $x$ noktasında en küçük değeri veren doğrunun sorulduğu bir sistem düşünelim. Her sorguda bütün doğruları tek tek kontrol etmek kolaydır; fakat doğru ve sorgu sayısı yüz binlere ulaştığında bilgisayarımız küçük bir hesap makinesi gibi terlemeye başlar. Li Chao ağacı, bu doğrusal fonksiyon sorgularını logaritmik zamanda yanıtlayarak imdadımıza yetişir.


![li-chao-agaci-13](/img/li-chao-agaci-13.svg)

``

## Problem tam olarak nedir?

Her doğruyu

$$f(x)=mx+b$$

biçiminde ifade edebiliriz. Burada $m$ eğim, $b$ ise doğrunun $y$ eksenini kestiği noktadır. Veri yapımız iki temel işlemi destekler:

1. Sisteme yeni bir doğru eklemek.
2. Verilen $x$ için eklenmiş doğrular arasındaki minimum veya maksimum değeri bulmak.

Naif yöntemde bir sorgunun maliyeti $O(N)$ olur. Li Chao ağacında hem ekleme hem sorgulama, koordinat aralığının genişliğine bağlı olarak yaklaşık $O(\log X)$ zamanda çalışır.

| Yaklaşım | Doğru ekleme | Nokta sorgusu | Uygun kullanım |
|---|---:|---:|---|
| Tüm doğruları dolaşma | $O(1)$ | $O(N)$ | Küçük veri |
| Convex Hull Trick | Genellikle $O(1)$ veya $O(\log N)$ | $O(\log N)$ | Eğim ya da sorgular sıralıysa |
| Li Chao ağacı | $O(\log X)$ | $O(\log X)$ | Doğrular rastgele sırada geliyorsa |

## Ağacın arkasındaki fikir

Li Chao ağacı, $x$ koordinat aralığını bir segment ağacı gibi ikiye böler. Her düğüm, kendi aralığında avantajlı olan bir doğru saklar. Yeni bir doğru geldiğinde düğümdeki mevcut doğruyla aralığın orta noktasında karşılaştırılır.

Yeni doğru orta noktada daha iyiyse iki doğru yer değiştirir. Kaybeden doğru tamamen çöpe atılmaz; çünkü aralığın solunda veya sağında hâlâ daha iyi olabilir. Bu nedenle yalnızca üstünlük gösterebileceği alt aralığa gönderilir. İki farklı doğru en fazla bir noktada kesiştiği için hangi tarafa ilerlememiz gerektiğini güvenle belirleyebiliriz.

Örneğin minimum sorgusu yapıyorsak, orta noktada daha küçük sonuç üreten doğru düğümde kalır. Böylece her eklemede yalnızca tek bir kök-yaprak yolu ziyaret edilir.

## C++ uygulaması

Aşağıdaki yapı, $[L,R]$ tamsayı aralığında minimum değer sorgularını gerçekleştirir:

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = 4e18;

struct Line {
    ll m, b;
    Line(ll m = 0, ll b = INF) : m(m), b(b) {}
    ll get(ll x) const { return m * x + b; }
};

struct Node {
    Line line;
    Node *left = nullptr, *right = nullptr;
};

class LiChaoTree {
    ll L, R;
    Node* root = nullptr;

    void add(Node*& node, ll l, ll r, Line incoming) {
        if (!node) node = new Node();

        ll mid = l + (r - l) / 2;
        bool betterLeft = incoming.get(l) < node->line.get(l);
        bool betterMid = incoming.get(mid) < node->line.get(mid);

        if (betterMid) swap(incoming, node->line);
        if (l == r) return;

        if (betterLeft != betterMid)
            add(node->left, l, mid, incoming);
        else
            add(node->right, mid + 1, r, incoming);
    }

    ll query(Node* node, ll l, ll r, ll x) const {
        if (!node) return INF;
        ll answer = node->line.get(x);
        if (l == r) return answer;

        ll mid = l + (r - l) / 2;
        if (x <= mid)
            return min(answer, query(node->left, l, mid, x));
        return min(answer, query(node->right, mid + 1, r, x));
    }

public:
    LiChaoTree(ll leftBound, ll rightBound) : L(leftBound), R(rightBound) {}

    void addLine(ll m, ll b) { add(root, L, R, Line(m, b)); }
    ll getMin(ll x) const { return query(root, L, R, x); }
};
```

`addLine`, sisteme $mx+b$ doğrusunu ekler. `getMin` ise verilen koordinatta ulaşılabilen en küçük değeri döndürür. Dinamik düğüm oluşturma sayesinde tüm koordinatlar için baştan bellek ayırmak gerekmez.

## Nerelerde kullanılır?

Li Chao ağacı özellikle

$$dp[i]=\min_{j<i}(m_jx_i+b_j)$$

şeklindeki dinamik programlama geçişlerinde güçlüdür. Maliyet optimizasyonu, çizelgeleme ve geometrik sorgular sık karşılaşılan kullanım alanlarıdır. Maksimum sorgusu için karşılaştırmaları ters çevirmek veya katsayıları negatiflemek yeterlidir.

Son olarak çarpım taşmalarına dikkat edilmelidir. $m$, $x$ ve $b$ büyükse değerlendirme sırasında `__int128` tercih edilebilir. Koordinatlar önceden biliniyorsa sıkıştırma uygulanabilir; bilinmiyorsa dinamik Li Chao ağacı, doğruların kaotik dünyasında düzenli ve hızlı bir çözüm sunar.
