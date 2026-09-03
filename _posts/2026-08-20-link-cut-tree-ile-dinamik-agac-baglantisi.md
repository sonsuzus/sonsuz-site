---
layout: post
title: "Link-Cut Tree ile Dinamik Ağaç Bağlantısı"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - link-cut tree
  - dinamik ağaçlar
toc: true
image: /img/link-cut-tree-25.png
---

Sabit bir ağaç üzerinde yol sorguları yapmak görece kolaydır; ancak kenarlar sürekli eklenip siliniyorsa klasik DFS, Euler turu veya ağır-hafif ayrıştırması kısa sürede zorlanır. Link-Cut Tree (LCT), tam bu hareketli dünyada devreye girer: Ormanı dinamik biçimde yönetir, iki düğümün bağlı olup olmadığını sorar, kenar koparır ve yeni bağlantılar kurar. Üstelik doğru kullanımda her işlem amortize olarak logaritmiktir.
``

## Problem: Ağaç Yerinde Durmuyorsa?

Elimizde başlangıçta bir **orman** olduğunu düşünelim. Her bileşen çevrimsizdir, fakat zaman içinde şu olaylar yaşanabilir:

- `link(u, v)`: Farklı iki ağacın köklerini bir kenarla bağlamak,
- `cut(u, v)`: Var olan bir kenarı kaldırmak,
- `connected(u, v)`: İki düğümün aynı bileşende olup olmadığını öğrenmek,
- `query(u, v)`: $u$ ile $v$ arasındaki yolda maksimum, toplam veya minimum değeri bulmak.

| Yaklaşım | Bağlantı ekleme/silme | Yol sorgusu | Dinamik yapıya uygunluk |
|---|---:|---:|---|
| DFS/BFS | $O(n)$ | $O(n)$ | Düşük |
| Heavy-Light Decomposition | Yeniden kurulum gerekebilir | $O(\log^2 n)$ | Sınırlı |
| Link-Cut Tree | Amortize $O(\log n)$ | Amortize $O(\log n)$ | Çok yüksek |

![link-cut-tree-25](/img/link-cut-tree-25.svg)


Buradaki kritik kelime **amortize**dir. Tek bir işlem bazen pahalı görünebilir; fakat uzun bir işlem dizisinde ortalama maliyet $O(\log n)$ seviyesinde kalır. Bu garanti, splay tree tabanlı yeniden düzenleme mekanizmasından gelir.

## Temel Fikir: Preferred Path ve Splay Tree

LCT, gerçek ağacı doğrudan tek bir ağaç olarak saklamaz. Bunun yerine kökten düğümlere uzanan bazı tercihli yolları (*preferred paths*) splay tree içinde temsil eder. Bir düğüme sık erişildiğinde, o düğüme giden yolun veri yapısı içinde öne çıkarılması sezgisel olarak önbellek benzeri bir avantaj yaratır.

En önemli işlem `access(x)`tir. Bu işlem, kökten $x$ düğümüne giden yolu düzenleyerek $x$'i kendi yardımcı ağacının sağ ucuna taşır. Ardından `makeRoot(x)` uygulanırsa yol ters çevrilir ve $x$, temsil edilen ağacın mantıksal kökü olur.

Yol sorgusunun özeti şöyledir:

$$
\text{query}(u,v) = \text{aggregate after } makeRoot(u),\ access(v)
$$

Örneğin her düğümde bir değer varsa, `access(v)` sonrasında `v`'nin splay alt ağacı $u \to v$ yolunu temsil eder. Bu alt ağacın sakladığı `sum`, `max` veya `min` alanı doğrudan cevaptır.

## Operasyonların Mantığı

| İşlem | Ön koşul | Yapılan iş |
|---|---|---|
| `makeRoot(x)` | Yok | $x$'i mantıksal kök yapar |
| `link(x,y)` | Farklı bileşenler | $x$ kök yapılır, $y$'ye bağlanır |
| `cut(x,y)` | Kenar mevcut | İki uç arasındaki doğrudan bağı kaldırır |
| `connected(x,y)` | Yok | Kök/temsilci karşılaştırması yapar |

Aşağıdaki iskelet, kenar değerleri yerine düğüm değerleri üzerinde toplam sorgusu yapan tipik bir LCT tasarımını gösterir. `push` ters çevirme bayrağını çocuklara iletir, `pull` ise alt ağaç özetini günceller.

```cpp
void makeRoot(int x) {
    access(x);
    splay(x);
    rev[x] ^= 1;       // Yolun yönünü ters çevir
}

void link(int x, int y) {
    makeRoot(x);
    if (findRoot(y) != x) parent[x] = y;
}

void cut(int x, int y) {
    makeRoot(x);
    access(y);
    splay(y);
    // x-y doğrudan kenarsa x, y'nin sol çocuğudur
    if (left[y] == x && right[x] == 0) {
        left[y] = parent[x] = 0;
        pull(y);
    }
}

long long pathSum(int x, int y) {
    makeRoot(x);
    access(y);
    splay(y);
    return sum[y];
}
```

Bu kodun görünmeyen ama hayati parçaları `rotate`, `splay`, `access`, `push` ve `pull` fonksiyonlarıdır. Özellikle lazy `rev` bayrağını splay işleminden önce aşağı itmemek, yol yönlerini bozarak son derece sinsi hatalara yol açar.

## Ne Zaman Kullanılmalı?

LCT; çevrimiçi sorgular, değişken ağ topolojileri, dinamik minimum kapsayan ağaç benzeri senaryolar ve yarışma programlamadaki “kes, bağla, yolda sor” problemleri için güçlüdür. Buna karşılık yalnızca sabit bir ağaç varsa HLD daha okunabilir olabilir. Link-Cut Tree biraz huysuz bir İsviçre çakısıdır: kurulumu zahmetlidir, fakat doğru problemde elinize aldığınız anda pek çok pahalı işlemi $O(\log n)$ hızına indirir.
