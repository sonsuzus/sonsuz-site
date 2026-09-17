---
layout: post
title: "Link-Cut Tree ile Dinamik Ağaç Bağlantılarını Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - link-cut-tree
  - dinamik-ağaç
  - veri-yapıları
  - algoritma
  - splay-tree
  - cpp
toc: true
image: /img/link-cut-tree-39.png
---

Bir ağaçta kenarlar sürekli eklenip çıkarılıyorsa klasik DFS yaklaşımı kısa sürede nefes nefese kalır. Link-cut tree, düğümler arasındaki yolları sorgularken ağacın bağlantılarını dinamik biçimde değiştirmemizi sağlar. İsmi bir bahçıvanlık aracını çağrıştırsa da yaptığı iş oldukça bilgisayarcıdır: ağaçları bağlar, dalları keser ve yol bilgilerini verimli şekilde günceller.

``

## Problem neden zor?

Sabit bir ağaçta iki düğüm arasındaki yolu DFS, heavy-light decomposition veya binary lifting ile inceleyebiliriz. Ancak `link(u, v)` ile yeni kenar ekleniyor ve `cut(u, v)` ile mevcut kenar siliniyorsa önceden hazırlanan üst ata tabloları geçerliliğini kaybeder.

Link-cut tree, düğümleri doğrudan tek bir dengeli ağaçta tutmaz. Bunun yerine gerçek ormanı **tercih edilen yollar** adı verilen parçalara ayırır. Her tercih edilen yol, yardımcı bir splay tree ile temsil edilir. Splay işlemi sık erişilen düğümü yardımcı ağacın köküne taşıyarak sonraki işlemleri hızlandırır.

Amortize edilmiş işlem maliyeti:

$$T(n) = O(\log n)$$

Buradaki “amortize” sözcüğü önemlidir. Tek bir işlem bazen daha pahalı olabilir; fakat $m$ işlem için toplam maliyet $O(m\log n)$ sınırında kalır.

| Yaklaşım | Kenar güncelleme | Yol sorgusu | Uygun senaryo |
|---|---:|---:|---|
| DFS/BFS | $O(1)$ | $O(n)$ | Küçük ve seyrek sorgular |
| Heavy-light decomposition | Genellikle yeniden kurulum ister | $O(\log^2 n)$ | Sabit ağaçlar |
| Link-cut tree | $O(\log n)$ amortize | $O(\log n)$ amortize | Dinamik ormanlar |

## Temel mekanizma

Her düğümde iki yardımcı çocuk, bir ebeveyn, ters çevirme bayrağı ve yol toplamı gibi birleştirilmiş bilgiler saklanır. `access(x)`, kökten `x` düğümüne uzanan yolu tercih edilen yol hâline getirir. `makeroot(x)` ise yolu ters çevirerek `x` düğümünü temsil edilen ağacın kökü yapar.

Lazy propagation burada küçük ama kritik bir numaradır. Bir yolu anında fiziksel olarak ters çevirmek yerine `rev` bayrağı değiştirilir. Düğüme gerçekten ihtiyaç duyulduğunda çocuklar takas edilir ve bayrak aşağı aktarılır.

```cpp
struct Node {
    int ch[2] = {0, 0};
    int parent = 0;
    long long value = 0;
    long long sum = 0;
    bool rev = false;
};

bool isRoot(int x) {
    int p = tree[x].parent;
    return p == 0 ||
        (tree[p].ch[0] != x && tree[p].ch[1] != x);
}

void pull(int x) {
    int l = tree[x].ch[0], r = tree[x].ch[1];
    tree[x].sum = tree[l].sum + tree[x].value + tree[r].sum;
}
```

`isRoot`, düğümün temsil edilen ağacın değil, yardımcı splay ağacının kökü olup olmadığını denetler. Bu ayrım link-cut tree uygulamalarındaki en yaygın hata kaynaklarından biridir. `pull` ise çocukların toplamlarını birleştirerek yol toplamı sorgularını mümkün kılar.

## Bağlama, kesme ve sorgulama

İki farklı ağacı bağlamak için önce `u` kök yapılır. Ardından `u` düğümünün ebeveyni `v` olarak atanır. Döngü oluşmasını engellemek amacıyla iki düğümün zaten aynı ağaçta bulunmadığı doğrulanmalıdır.

```cpp
void link(int u, int v) {
    makeRoot(u);
    if (findRoot(v) != u)
        tree[u].parent = v;
}

void cut(int u, int v) {
    makeRoot(u);
    access(v);
    splay(v);

    if (tree[v].ch[0] == u && tree[u].ch[1] == 0) {
        tree[v].ch[0] = 0;
        tree[u].parent = 0;
        pull(v);
    }
}

long long pathSum(int u, int v) {
    makeRoot(u);
    access(v);
    splay(v);
    return tree[v].sum;
}
```

`pathSum` çağrısında `u` kök yapıldıktan sonra `v` düğümüne erişilir. Böylece yardımcı splay tree tam olarak $u \rightarrow v$ yolunu temsil eder ve `sum` sonucu hazır hâle gelir.

## Nerelerde kullanılır?

Link-cut tree; dinamik ağ bağlantıları, çevrim içi minimum yayılım ağacı problemleri, oyunlardaki değişken hiyerarşiler ve rekabetçi programlama sorularında karşımıza çıkar. Uygulaması kısa değildir; özellikle `rotate`, `splay`, `push` ve `access` fonksiyonlarında tek bir yanlış ebeveyn ataması bütün ormanı dijital odun yığınına çevirebilir. Buna rağmen bağlantıların sürekli değiştiği ve yol sorgularının yoğun olduğu problemlerde sunduğu $O(\log n)$ amortize performans, bu karmaşıklığa fazlasıyla değebilir.

![link-cut-tree-39](/img/link-cut-tree-39.svg)

