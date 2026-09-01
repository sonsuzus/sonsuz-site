---
layout: post
title: "Fenwick Ağacı Varyasyonları: 2B Matrislerde Güncelleme ve Alan Sorgusu"
math: true
categories: 
  - Bilgi
tags: 
  - fenwick ağacı
  - veri yapıları
  - algoritmalar
toc: true
---

Bir matris üzerinde sürekli hücre güncelleyip dikdörtgen alanların toplamını sorgulamak, ilk bakışta iç içe döngülerle çözülebilecek masum bir problem gibi görünür. Ancak matris büyüdükçe bu yaklaşım bilgisayarınıza küçük çaplı bir sabır testi uygular. İki boyutlu Fenwick Ağacı, diğer adıyla 2D Binary Indexed Tree, nokta güncellemelerini ve alan toplamı sorgularını logaritmik maliyetle bir araya getirerek bu sorunu zarifçe çözer.

``

## Tek Boyuttan İki Boyuta Geçiş

Klasik Fenwick Ağacı, bir dizideki önek toplamlarını saklar. Temel fikir, her düğümün indeksinin son anlamlı bitine göre belirlenen bir aralığı temsil etmesidir. Bu bit şu ifadeyle bulunur:

$$
\operatorname{lowbit}(x) = x \mathbin{\&} (-x)
$$

Örneğin $12$ sayısının ikilik gösterimi $1100$ olduğundan, $\operatorname{lowbit}(12)=4$ olur. Güncelleme sırasında indekse `lowbit` eklenerek üst sorumluluk bölgelerine çıkılır; sorguda ise çıkarılarak köke doğru ilerlenir.

İki boyutlu sürümde aynı işlem hem satır hem sütun için uygulanır. `tree[i][j]` hücresi, belirli bir satır aralığı ile sütun aralığının Kartezyen çarpımından oluşan dikdörtgenin toplamını taşır.

| İşlem | Naif matris | 2B Fenwick Ağacı |
|---|---:|---:|
| Nokta güncelleme | $O(1)$ | $O(\log n\log m)$ |
| Dikdörtgen toplamı | $O(nm)$ | $O(\log n\log m)$ |
| Bellek | $O(nm)$ | $O(nm)$ |

Naif yapı güncellemede hızlıdır fakat sorguda tüm alanı gezer. 2B Fenwick ise iki işlemi dengeler; özellikle çok sayıda güncelleme ve sorgunun karışık geldiği senaryolarda parlar.

## Önek Toplamından Alan Sorgusuna

Fenwick ağacının doğrudan hesapladığı değer, $(1,1)$ ile $(x,y)$ arasındaki önek dikdörtgeninin toplamıdır. Herhangi bir $(x_1,y_1)$–$(x_2,y_2)$ alanı için dahil etme-çıkarma ilkesi kullanılır:

$$
S = P(x_2,y_2)-P(x_1-1,y_2)-P(x_2,y_1-1)+P(x_1-1,y_1-1)
$$

Son terimin yeniden eklenmesinin nedeni, sol üstteki ortak bölgenin iki kez çıkarılmış olmasıdır. Bu formül, iki boyutlu önek toplamlarının Fenwick üzerindeki karşılığıdır.

## C++ ile Uygulama

Aşağıdaki sınıf, tek bir hücreye fark değeri ekler ve istenen dikdörtgenin toplamını döndürür:

```cpp
class Fenwick2D {
    int n, m;
    vector<vector<long long>> tree;

public:
    Fenwick2D(int rows, int cols)
        : n(rows), m(cols),
          tree(rows + 1, vector<long long>(cols + 1)) {}

    void add(int x, int y, long long delta) {
        for (int i = x; i <= n; i += i & -i)
            for (int j = y; j <= m; j += j & -j)
                tree[i][j] += delta;
    }

    long long prefixSum(int x, int y) const {
        long long result = 0;
        for (int i = x; i > 0; i -= i & -i)
            for (int j = y; j > 0; j -= j & -j)
                result += tree[i][j];
        return result;
    }

    long long areaSum(int x1, int y1, int x2, int y2) const {
        return prefixSum(x2, y2)
             - prefixSum(x1 - 1, y2)
             - prefixSum(x2, y1 - 1)
             + prefixSum(x1 - 1, y1 - 1);
    }
};
```

Kod 1 tabanlı indeksleme kullanır; çünkü sıfır için `lowbit(0)` değeri ilerleme sağlamaz ve döngüyü sonsuzlaştırabilir. Mevcut bir hücrenin değerini doğrudan değiştirmek istiyorsak eski değeri saklayıp `delta = yeni - eski` hesaplamalıyız.

```cpp
long long delta = newValue - matrix[x][y];
matrix[x][y] = newValue;
fenwick.add(x, y, delta);
```

## Nerelerde Kullanılır?

Bu yapı; çevrim içi görüntü yoğunluğu sorguları, oyun haritalarındaki kaynak değişimleri, coğrafi ızgara analizleri ve yarışma programlamasındaki dinamik matris problemleri için uygundur. Matris seyrek ve koordinatlar çok büyükse, standart dizi yerine koordinat sıkıştırma veya sözlük tabanlı düğümler düşünülebilir.

Sonuç olarak 2B Fenwick Ağacı, basit bit işlemlerini güçlü bir geometrik sorgu mekanizmasına dönüştürür. Segment ağacına göre daha az esnek olsa da toplam sorgularında daha kısa kod, düşük sabit maliyet ve oldukça tatmin edici bir performans sunar.
