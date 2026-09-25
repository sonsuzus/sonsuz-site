---
layout: post
title: "Fenwick Ağacı ile Çok Boyutlu Aralık Sorgularında Bellek Tasarrufu"
math: true
categories: 
  - Bilgi
tags: 
  - fenwick ağacı
  - bit
  - veri yapıları
  - algoritma
  - aralık sorguları
  - bellek optimizasyonu
  - cpp
toc: true
image: /img/fenwick-agaci-ile-35.png
---

Bir oyun haritasındaki kaynak miktarlarını, elektronik tablodaki hücre değerlerini veya koordinat düzlemindeki hareketli puanları sürekli güncellediğimizi düşünelim. Her değişiklikten sonra dikdörtgen bir bölgenin toplamını hesaplamak, naif yöntemle pahalıdır. Fenwick Ağacı ya da kısa adıyla **BIT (Binary Indexed Tree)**, segment ağacına göre daha az kod ve yardımcı bellek kullanarak bu işi logaritmik sürede yapar.

``

## Fenwick Ağacının temel fikri

Tek boyutlu BIT, her indeksin belirli uzunluktaki bir aralığın toplamını saklamasına dayanır. Bir indeksin sorumlu olduğu aralık, ikili gösterimindeki en düşük anlamlı bit ile belirlenir:

$$lowbit(x)=x\ \&\ (-x)$$

Örneğin $12=(1100)_2$ için $lowbit(12)=4$ olur. Güncelleme sırasında indeksleri $lowbit(i)$ kadar artırır, önek toplamında ise aynı miktarı çıkarırız. Böylece her işlem en fazla $O(\log n)$ düğüme dokunur.

İki boyutta aynı düşünceyi satır ve sütun eksenlerine ayrı ayrı uygularız. $(x,y)$ noktasına eklenen değer, iki iç içe Fenwick yürüyüşüyle ilgili hücrelere taşınır. Bir dikdörtgen toplamı ise dahil etme–hariç tutma ilkesiyle bulunur:

$$R(x_1,y_1,x_2,y_2)=P(x_2,y_2)-P(x_1-1,y_2)-P(x_2,y_1-1)+P(x_1-1,y_1-1)$$

Burada $P(x,y)$, $(1,1)$ ile $(x,y)$ arasındaki önek toplamıdır.

## Segment ağacı mı, Fenwick mi?

| Özellik | 2B Fenwick Ağacı | 2B Segment Ağacı |
|---|---:|---:|
| Nokta güncelleme | $O(\log n\log m)$ | $O(\log n\log m)$ |
| Dikdörtgen toplamı | $O(\log n\log m)$ | $O(\log n\log m)$ |
| Tipik yardımcı bellek | Yaklaşık $nm$ | Yaklaşık $4n\cdot4m$ |
| Uygulama karmaşıklığı | Düşük | Yüksek |
| Min/maks gibi işlemler | Sınırlı | Daha esnek |

![fenwick-agaci-ile-35](/img/fenwick-agaci-ile-35.svg)


BIT’in önemli sınırlaması, işlemin tersinin bulunabilmesidir. Toplamada çıkarma sayesinde iki önekten aralık üretilebilir. Ancak genel minimum sorgusunda “önek minimumlarını çıkarma” diye bir işlem yoktur. Bu durumda segment ağacı daha doğru seçimdir.

## Bellek dostu 2B uygulama

Aşağıdaki C++ sınıfı matrisi satır satır tek bir `vector` içinde tutar. Ayrı ayrı vektörler oluşturmadığı için tahsis maliyetini azaltır ve önbellek yerelliğini iyileştirir.

```cpp
#include <bits/stdc++.h>
using namespace std;

class Fenwick2D {
    int n, m;
    vector<long long> bit;

    long long& at(int x, int y) {
        return bit[x * (m + 1) + y];
    }

public:
    Fenwick2D(int rows, int cols)
        : n(rows), m(cols), bit((rows + 1) * (cols + 1), 0) {}

    // (x, y) noktasına delta ekler.
    void add(int x, int y, long long delta) {
        for (int i = x; i <= n; i += i & -i)
            for (int j = y; j <= m; j += j & -j)
                at(i, j) += delta;
    }

    // (1,1) ile (x,y) arasındaki toplamı döndürür.
    long long prefix(int x, int y) {
        long long result = 0;
        for (int i = x; i > 0; i -= i & -i)
            for (int j = y; j > 0; j -= j & -j)
                result += at(i, j);
        return result;
    }

    long long rectangle(int x1, int y1, int x2, int y2) {
        return prefix(x2, y2) - prefix(x1 - 1, y2)
             - prefix(x2, y1 - 1) + prefix(x1 - 1, y1 - 1);
    }
};
```

İndekslerin **1’den başlaması** önemlidir; sıfır için `lowbit(0)` sıfırdır ve güncelleme döngüsü ilerlemez.

## Boyutlar devasa olduğunda

Koordinatlar milyarlara ulaşıyor fakat yalnızca birkaç bin nokta kullanılıyorsa tam matris ayırmak anlamsızdır. Güncelleme ve sorgulardaki koordinatları sıralayıp benzersizleştirerek **koordinat sıkıştırma** uygulanabilir. Her gerçek koordinat, sıralamadaki 1 tabanlı sırasına dönüştürülür.

$d$ boyutta güncelleme ve sorgu maliyeti yaklaşık $O(\log^d n)$ olur. Buna karşılık yoğun depolama $O(n^d)$ büyüdüğünden, pratikte üç ve üzeri boyutlarda yalnızca erişilen Fenwick hücrelerini karma tablo veya sıkıştırılmış iç vektörlerle saklamak gerekir. Kısacası toplam ve frekans sorgularında BIT, küçük kodu ve düşük sabit maliyetiyle güçlüdür; karmaşık birleştirme işlemlerinde ise segment ağacı hâlâ sahnededir.
