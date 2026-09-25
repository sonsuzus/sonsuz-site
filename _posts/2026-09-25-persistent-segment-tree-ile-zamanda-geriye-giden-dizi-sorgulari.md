---
layout: post
title: "Persistent Segment Tree ile Zamanda Geriye Giden Dizi Sorguları"
math: true
categories: 
  - Bilgi
tags: 
  - persistent-segment-tree
  - veri-yapıları
  - algoritma
  - c++
  - segment-tree
  - zaman-yolculuğu
toc: true
image: /img/persistent-segment-tree-23.png
---

Bir diziyi güncelledikten sonra eski değerlerine yeniden ihtiyaç duyduğunuzu düşünün. Normal bir Segment Tree değişiklikleri doğrudan mevcut yapı üzerinde uygular; geçmiş ise sessizce kaybolur. Persistent Segment Tree, her güncellemede yeni bir sürüm oluşturarak bu sorunu çözer. Üstelik bütün ağacı kopyalamak yerine yalnızca değişen düğümleri üretir. Kısacası elimizde veri yapılarının zaman makinesi vardır!
``

## Kalıcılık fikri nedir?

Persistent, yani **kalıcı**, bir veri yapısında önceki sürümler değişmeden erişilebilir kalır. Dizinin başlangıç durumuna `versiyon 0`, ilk güncellemeden sonraki durumuna `versiyon 1` diyebiliriz. Her versiyonun Segment Tree kökünü ayrı bir dizide saklamak yeterlidir.

Bir Segment Tree güncellemesinde kökten yaprağa yalnızca tek yol değişir. Dizinin boyutu $n$ ise bu yolun uzunluğu $O(\log n)$ olur. Dolayısıyla yeni sürüm için tüm $O(n)$ düğümleri kopyalamak yerine yaklaşık $O(\log n)$ yeni düğüm oluştururuz. Değişmeyen alt ağaçlar eski ve yeni sürümler tarafından ortak kullanılır.

$u$ güncelleme sonrasında toplam bellek maliyeti yaklaşık olarak:

$$O(n + u \log n)$$

Bu tekniğe **path copying**, yani yol kopyalama adı verilir.

| Özellik | Normal Segment Tree | Persistent Segment Tree |
|---|---:|---:|
| Aralık sorgusu | $O(\log n)$ | $O(\log n)$ |
| Noktasal güncelleme | $O(\log n)$ | $O(\log n)$ |
| Geçmiş sürüme erişim | Yok | Var |
| Güncelleme başına bellek | Ek düğüm yok | $O(\log n)$ |
| Uygulama karmaşıklığı | Daha kolay | Biraz daha dikkat ister |

## Düğümler nasıl paylaşılır?

Her düğüm; tuttuğu toplamı, sol çocuk indeksini ve sağ çocuk indeksini saklar. Güncelleme başladığında eski düğüm kopyalanır. Değişiklik hangi taraftaysa yalnızca o çocuk yeniden oluşturulur; diğer çocuğun indeksi eski sürümden alınır. Böylece iki farklı zaman çizgisi aynı değişmemiş dalları paylaşabilir.

Aşağıdaki C++ örneği, noktasal değer atama ve geçmiş bir sürümde aralık toplamı sorgulama işlemlerini gerçekleştirir:

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Node {
    long long sum;
    int left, right;
};

vector<Node> tree;
vector<int> roots;

int build(const vector<int>& a, int l, int r) {
    int node = tree.size();
    tree.push_back({0, -1, -1});

    if (l == r) {
        tree[node].sum = a[l];
        return node;
    }

    int mid = (l + r) / 2;
    tree[node].left = build(a, l, mid);
    tree[node].right = build(a, mid + 1, r);
    tree[node].sum = tree[tree[node].left].sum
                   + tree[tree[node].right].sum;
    return node;
}

int update(int old, int l, int r, int pos, int value) {
    int node = tree.size();
    tree.push_back(tree[old]); // Eski düğümün kopyası

    if (l == r) {
        tree[node].sum = value;
        return node;
    }

    int mid = (l + r) / 2;
    if (pos <= mid)
        tree[node].left = update(tree[old].left, l, mid, pos, value);
    else
        tree[node].right = update(tree[old].right, mid + 1, r, pos, value);

    tree[node].sum = tree[tree[node].left].sum
                   + tree[tree[node].right].sum;
    return node;
}

long long query(int node, int l, int r, int ql, int qr) {
    if (qr < l || r < ql) return 0;
    if (ql <= l && r <= qr) return tree[node].sum;

    int mid = (l + r) / 2;
    return query(tree[node].left, l, mid, ql, qr)
         + query(tree[node].right, mid + 1, r, ql, qr);
}
```

İlk kök `roots.push_back(build(a, 0, n - 1))` ile kaydedilir. Yeni bir sürüm oluşturmak için `roots.push_back(update(roots.back(), 0, n - 1, konum, deger))` çağrılır. Örneğin üçüncü sürümde `[2, 6]` toplamı `query(roots[3], 0, n - 1, 2, 6)` ile bulunur.

## Nerelerde kullanılır?

Persistent Segment Tree; geçmiş durum sorgularında, geri alma sistemlerinde, çevrim dışı sorgularda ve bir aralıktaki $k$'ıncı küçük elemanı bulma problemlerinde oldukça etkilidir. Git’in commit geçmişini düşünmek iyi bir benzetmedir: Her sürüm tamamen bağımsız görünür, fakat değişmeyen içerik yeniden kullanılabilir.

En önemli ayrıntı, eski düğümleri asla değiştirmemektir. Yanlışlıkla eski bir çocuk üzerinde güncelleme yapmak bütün zaman çizgisini bozabilir. Doğru uygulandığında ise geçmiş, silinen bir kayıt değil; yalnızca doğru kökü seçerek ziyaret edebileceğiniz başka bir versiyondur.

![persistent-segment-tree-23](/img/persistent-segment-tree-23.svg)

