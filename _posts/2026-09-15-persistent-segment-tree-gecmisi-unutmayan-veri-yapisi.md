---
layout: post
title: "Persistent Segment Tree: Geçmişi Unutmayan Veri Yapısı"
math: true
categories: 
  - Bilgi
tags: 
  - persistent-segment-tree
  - veri-yapıları
  - algoritma
  - c++
  - segment-tree
  - kalıcılık
toc: true
---

Bir segment tree düşünün: aralık toplamlarını hızla hesaplıyor, güncellemeleri şıp diye uyguluyor ama her değişiklikte eski hâlini unutuyor. Persistent segment tree ise biraz nostaljiktir; yapılan her güncellemeden sonra geçmiş sürümleri saklar. Böylece yalnızca güncel veriye değil, dizinin herhangi bir zamandaki hâline de erişebiliriz.
``
## Önce normal segment tree

$n$ elemanlı bir dizi üzerinde aralık toplamı, minimum veya maksimum gibi sorguları hızlandırmak için segment tree kullanılır. Her düğüm bir aralığı temsil eder; yapraklar tek elemanlara, kök ise tüm diziye karşılık gelir.

Dengeli ağacın yüksekliği yaklaşık olarak

$$h = \lceil \log_2 n \rceil$$

olduğundan noktasal güncelleme ve aralık sorgusu $O(\log n)$ zamanda gerçekleştirilir. Fakat klasik yapıda bir değer güncellendiğinde ilgili düğümlerin üzerine yazılır. Eski bilgi artık yoktur.

| Özellik | Klasik Segment Tree | Persistent Segment Tree |
|---|---|---|
| Sorgu süresi | $O(\log n)$ | $O(\log n)$ |
| Güncelleme süresi | $O(\log n)$ | $O(\log n)$ |
| Eski sürümlere erişim | Yok | Var |
| Güncelleme başına ek bellek | Genellikle yok | $O(\log n)$ |
| Temel yaklaşım | Düğümleri değiştir | Değişen yolu kopyala |

## Kalıcılığın sırrı: Path Copying

Bir elemanı güncellediğimizde kökten ilgili yaprağa kadar yalnızca $O(\log n)$ düğüm etkilenir. Persistent yapı bütün ağacı kopyalamak yerine sadece bu yolu kopyalar. Değişmeyen alt ağaçlar eski ve yeni sürümler arasında paylaşılır.

Örneğin `version[0]` ilk ağacın kökü olsun. Bir güncelleme yapıldığında yeni bir kök üretilir ve `version[1]` içine konur. Eski kök yerinde durduğu için iki sürüm de sorgulanabilir. $q$ güncellemeden sonraki yaklaşık bellek maliyeti şöyledir:

$$O(n + q\log n)$$

Bu paylaşım mekanizması, yapının sanıldığı kadar bellek canavarı olmasını engeller. Yine de her güncellemede yeni düğümler üretildiği için dikkatli kapasite planlaması gerekir.

## C++ ile temel uygulama

Aşağıdaki örnek noktasal güncelleme ve aralık toplamı işlemlerini destekler. `update`, eski düğümleri değiştirmek yerine yeni düğümler oluşturarak yeni sürümün kökünü döndürür.

```cpp
#include <iostream>
#include <vector>
using namespace std;

struct Node {
    long long sum;
    Node *left, *right;
    Node(long long s = 0, Node* l = nullptr, Node* r = nullptr)
        : sum(s), left(l), right(r) {}
};

Node* build(const vector<int>& a, int l, int r) {
    if (l == r) return new Node(a[l]);
    int m = (l + r) / 2;
    Node* left = build(a, l, m);
    Node* right = build(a, m + 1, r);
    return new Node(left->sum + right->sum, left, right);
}

Node* update(Node* old, int l, int r, int pos, int value) {
    if (l == r) return new Node(value);

    int m = (l + r) / 2;
    Node *left = old->left, *right = old->right;

    if (pos <= m)
        left = update(old->left, l, m, pos, value);
    else
        right = update(old->right, m + 1, r, pos, value);

    return new Node(left->sum + right->sum, left, right);
}

long long query(Node* node, int l, int r, int ql, int qr) {
    if (qr < l || r < ql) return 0;
    if (ql <= l && r <= qr) return node->sum;
    int m = (l + r) / 2;
    return query(node->left, l, m, ql, qr)
         + query(node->right, m + 1, r, ql, qr);
}
```

Kullanım sırasında kökler bir vektörde tutulabilir:

```cpp
vector<Node*> versions;
versions.push_back(build(a, 0, n - 1));
versions.push_back(update(versions[0], 0, n - 1, 2, 10));

cout << query(versions[0], 0, n - 1, 0, 3) << '\n';
cout << query(versions[1], 0, n - 1, 0, 3) << '\n';
```

İlk sorgu güncelleme öncesini, ikincisi sonrasını gösterir. Adeta veri yapısının zaman makinesine iki farklı bilet almış oluruz.

## Nerelerde kullanılır?

Persistent segment tree; geçmiş kayıtları inceleyen sistemlerde, geri alma mekanizmalarında, rekabetçi programlamadaki $k$'ıncı küçük eleman sorgularında ve zaman içindeki istatistikleri karşılaştırmada kullanılır. Özellikle farklı sürümler değiştirilmeyecekse bu yaklaşım **partial persistence** olarak adlandırılır.

Özetle fikir oldukça zariftir: Geçmişi tamamen kopyalama, yalnızca değişen yolu yeniden oluştur. Böylece hızlı sorgular korunurken her sürüm erişilebilir kalır. Normal segment tree bugünü yönetiyorsa persistent segment tree hem bugünü hem de dünün hesabını tutar.
