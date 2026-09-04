---
layout: post
title: "Sparse Table: Değişmeyen Verilerde Işık Hızında Aralık Sorguları"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - veri yapıları
  - sparse table
image: /img/sparse-table-degismeyen-15.png
---

Bir dizideki belirli aralıkların minimumunu, maksimumunu ya da EBOB'unu defalarca bulmanız gerektiğini düşünün. Veri hiç değişmiyorsa, her sorguda aralığı baştan taramak gereksiz bir maliyettir. **Sparse Table**, ön işlem süresini ve belleği göze alarak sorguları özellikle minimum/maksimum gibi işlemlerde $O(1)$ sürede cevaplayan etkileyici bir veri yapısıdır. Adındaki “sparse” kelimesi yanıltıcı olabilir: Bu yapı seyrek verilerden çok, $2$'nin kuvveti uzunluğundaki önceden hesaplanmış aralık bloklarından oluşur.
``

Temel fikir, diziyi farklı uzunluklardaki bloklara ayırmaktır. `st[k][i]`, dizinin `i` indeksinden başlayan ve uzunluğu $2^k$ olan parçanın sonucunu saklar. Örneğin `st[0][i]` doğrudan `a[i]` değeridir; çünkü $2^0 = 1$'dir. Bir sonraki seviye ise iki komşu küçük blok birleştirilerek elde edilir:

$$st[k][i] = f(st[k-1][i], st[k-1][i + 2^{k-1}])$$

Buradaki $f$, seçtiğiniz işlemdir: `min`, `max` veya `gcd` olabilir. Böylece her blok, kendisinden yarı boyuttaki iki bloğun özetinden inşa edilir. Bu yaklaşımın güzel tarafı, tüm tabloyu $O(n \log n)$ zamanda hazırlayabilmenizdir.

Bir $[L, R]$ aralığının uzunluğu $len = R-L+1$ olsun. Minimum sorgusunda $k = \lfloor\log_2(len)\rfloor$ seçilir. Aralığı tamamen kapsayan iki adet $2^k$ uzunluklu blok kullanılır. Bu bloklar çakışabilir; ancak `min` için bu sorun değildir. Çünkü aynı değeri iki kez minimuma dahil etmek sonucu değiştirmez:

$$\min(L,R) = \min(st[k][L],\ st[k][R-2^k+1])$$

Bu özellik, işlemin **idempotent** olmasıyla ilgilidir: $f(x,x)=x$. `min`, `max` ve `gcd` buna uygundur. Fakat toplama için uygun değildir; iki blok çakıştığında ortak elemanlar iki kez sayılır.

| Özellik | Sparse Table | Segment Tree | Prefix Sum |
|---|---:|---:|---:|
| Veri güncelleme | Uygun değil | $O(\log n)$ | Uygun değil |
| Minimum/maksimum sorgusu | $O(1)$ | $O(\log n)$ | Desteklemez |
| Toplam sorgusu | Genelde $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| Ön işlem | $O(n\log n)$ | $O(n)$ | $O(n)$ |
| Bellek | $O(n\log n)$ | $O(n)$ | $O(n)$ |

![sparse-table-degismeyen-15](/img/sparse-table-degismeyen-15.svg)


Aşağıdaki C++ örneği, statik bir dizide minimum sorgularını hazırlar. `lg` dizisi, sorgu uzunluğuna karşılık gelen en büyük $2$ kuvvetini hızlıca bulmak için kullanılır.

```cpp
#include <bits/stdc++.h>
using namespace std;

class SparseTable {
    vector<vector<int>> st;
    vector<int> lg;

public:
    SparseTable(const vector<int>& a) {
        int n = a.size();
        int K = __lg(n) + 1;
        st.assign(K, vector<int>(n));
        lg.assign(n + 1, 0);

        for (int i = 2; i <= n; ++i)
            lg[i] = lg[i / 2] + 1;

        st[0] = a;
        for (int k = 1; k < K; ++k) {
            for (int i = 0; i + (1 << k) <= n; ++i) {
                st[k][i] = min(st[k - 1][i],
                               st[k - 1][i + (1 << (k - 1))]);
            }
        }
    }

    int rangeMin(int left, int right) {
        int k = lg[right - left + 1];
        return min(st[k][left], st[k][right - (1 << k) + 1]);
    }
};
```

Örneğin `rangeMin(2, 7)`, üçüncü indexten sekizinci indexe kadar olan kapalı aralıktaki en küçük değeri döndürür. İndeksleme konusunda dikkatli olun: Kod sıfır tabanlı indeks kullanır. Ayrıca boş diziyle tablo kurmamak gerekir; `__lg(0)` geçersizdir.

Sparse Table'ın sınırı nettir: Bir eleman değişirse, onu içeren çok sayıda blok etkilenir ve yapı cazibesini kaybeder. Buna karşılık sıcaklık kayıtları, sabit oyun haritaları, önceden yüklenmiş yükseklik verileri veya değişmeyen log dizileri gibi statik senaryolarda harikadır. Çok sorgu, sıfır güncelleme: Sparse Table tam olarak bu denklemin yıldızıdır.
