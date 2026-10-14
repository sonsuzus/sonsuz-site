---
layout: post
title: "Ağırlıklı Hızlı-Birleşme: Union-Find Ağaçlarını Dengede Tutmak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - union-find
  - veri-yapıları
  - java
  - weighted-quick-union
toc: true
image: /img/agirlikli-hizli-birlesme-21.png
---

Union-Find, elemanların hangi gruba ait olduğunu hızlıca belirlemek ve iki grubu birleştirmek için kullanılan klasik bir veri yapısıdır. Ancak grupları düşünmeden birleştirirsek ortaya uzun, ince ve performans düşmanı ağaçlar çıkabilir. Ağırlıklı Hızlı-Birleşme (Weighted Quick-Union), küçük ağacı büyük ağacın altına bağlayarak bu sorunu oldukça zarif biçimde çözer.

``

## Union-Find hangi problemi çözer?

Elimizde başlangıçta birbirinden bağımsız $N$ eleman bulunduğunu düşünelim. Union-Find iki temel işlemi destekler:

- `find(p)`: `p` elemanının bağlı olduğu kümenin kökünü bulur.
- `union(p, q)`: `p` ve `q` elemanlarının kümelerini birleştirir.

Bu yapı; sosyal ağ bağlantıları, bilgisayar ağları, görüntü işleme, labirent üretimi ve Kruskal’ın minimum kapsayan ağaç algoritması gibi birçok alanda kullanılır.

Quick-Union yaklaşımında her eleman, ebeveyninin indeksini saklar. Bir kökte `parent[i] == i` olur. `find`, ebeveyn bağlantılarını köke ulaşıncaya kadar takip eder. Ne var ki birleşimler kötü sırayla yapılırsa ağaç bir zincire dönüşebilir.

| Yaklaşım | Birleştirme stratejisi | Olası ağaç yüksekliği | En kötü `find` |
|---|---|---:|---:|
| Quick-Union | Bir kökü diğerine rastgele bağlar | $N-1$ | $O(N)$ |
| Weighted Quick-Union | Küçük ağacı büyük ağaca bağlar | $log_2 N$ | $O(log N)$ |
| Yol sıkıştırmalı ağırlıklı sürüm | Düğümleri köke yaklaştırır | Çok düşük | Yaklaşık $O(α(N))$ |

Buradaki $α(N)$, ters Ackermann fonksiyonudur ve pratik veri boyutlarında neredeyse sabit kabul edilir.

## Ağırlık neden işe yarar?

Her kök için ağacındaki eleman sayısını tutan bir `size` dizisi kullanılır. İki küme birleştirilirken küçük ağacın kökü, büyük ağacın köküne bağlanır. Böylece büyük ağaçtaki düğümlerin derinliği hiç değişmez; yalnızca küçük ağaçtaki düğümlerin derinliği bir artabilir.

Bir düğümün derinliği her arttığında, içinde bulunduğu ağacın büyüklüğü en az iki katına çıkar. Derinlik $h$ ise ağacın en az $2^h$ elemanı olmalıdır:

$$2^h ≤ N \Rightarrow h ≤ log_2 N$$

İşte performans garantisinin kalbi budur. Örneğin $N=1.000.000$ olduğunda zincir biçimli ağaç yaklaşık bir milyon adım gerektirebilirken ağırlıklı ağacın yüksekliği yaklaşık 20 ile sınırlıdır. Algoritmik diyet işe yarıyor: küçük ağaç, büyük ağacın sırtına biniyor!

## Java ile uygulama

Aşağıdaki sınıf, ebeveynleri `parent`, ağaç büyüklüklerini ise `size` dizisinde saklar:

```java
public class WeightedQuickUnion {
    private final int[] parent;
    private final int[] size;

    public WeightedQuickUnion(int n) {
        parent = new int[n];
        size = new int[n];

        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
    }

    public int find(int p) {
        validate(p);
        while (p != parent[p]) {
            p = parent[p];
        }
        return p;
    }

    public boolean connected(int p, int q) {
        return find(p) == find(q);
    }

    public void union(int p, int q) {
        int rootP = find(p);
        int rootQ = find(q);

        if (rootP == rootQ) return;

        if (size[rootP] < size[rootQ]) {
            parent[rootP] = rootQ;
            size[rootQ] += size[rootP];
        } else {
            parent[rootQ] = rootP;
            size[rootP] += size[rootQ];
        }
    }

    private void validate(int p) {
        if (p < 0 || p >= parent.length) {
            throw new IllegalArgumentException();
        }
    }
}
```

`find` yalnızca köke yürür. `union` önce iki kökü bulur, ardından `size` değerlerini karşılaştırarak küçük ağacı büyük ağaca bağlar. Boyut bilgisinin yalnızca köklerde anlamlı olduğuna dikkat edilmelidir.

## Bir adım daha: yol sıkıştırma

Performansı daha da artırmak için `find` döngüsüne şu satır eklenebilir:

```java
parent[p] = parent[parent[p]];
```

Bu işlem, ziyaret edilen düğümü büyük ebeveynine bağlayarak yolu kısaltır. Ağırlıklandırma ağacın baştan fazla uzamasını önlerken yol sıkıştırma mevcut yolları düzleştirir. Birlikte kullanıldıklarında Union-Find işlemleri pratikte sabit zamana yakın çalışır. Sonuç olarak Weighted Quick-Union, küçük bir ek bellek maliyeti karşılığında kontrolsüz ağaç büyümesini engelleyen, basit ama son derece güçlü bir optimizasyondur.

![agirlikli-hizli-birlesme-21](/img/agirlikli-hizli-birlesme-21.svg)

