---
layout: post
title: "Merkezcil Ayrıştırma ile Ağaç Mesafe Sorgularını Hızlandırma"
math: true
categories: 
  - Bilgi
tags: 
  - centroid-decomposition
  - ağaç-algoritmaları
  - böl-ve-fethet
toc: true
---

Bir ağaçta “işaretli en yakın düğüm hangisi?” veya “uzaklığı tam $K$ olan kaç düğüm çifti var?” gibi sorular ilk bakışta masum görünür. Fakat her sorguda bütün ağacı dolaşmak, $N$ düğüm ve $Q$ sorgu için $O(NQ)$ maliyet doğurabilir. Merkezcil ayrıştırma, ağacı dengeli parçalara bölerek her düğümün yalnızca logaritmik sayıda temsilciyle ilişki kurmasını sağlar. Kısacası ağacı keser, fakat mesafe bilgisini kaybetmez.

``

## Merkezcil düğüm nedir?

Bir ağacın **merkezi (centroid)**, kaldırıldığında geriye kalan bağlı bileşenlerin hiçbirinin toplam düğüm sayısının yarısından büyük olmadığı düğümdür. $N$ düğümlü bir ağaçta merkez $c$ ise her bileşen için

$$
\vert C_i\vert  \leq \frac{N}{2}
$$

koşulu sağlanır. Her ağacın en az bir, en fazla iki merkezi vardır. Ayrıştırmada bunlardan herhangi biri seçilebilir.

Merkez kaldırılır, oluşan alt ağaçların her birinde aynı işlem tekrarlanır. Böylece özgün ağaçtan farklı bir **centroid ağacı** meydana gelir. Her seviyede problem boyutu en fazla yarıya indiğinden bu yeni ağacın yüksekliği

$$
H \leq \lceil \log_2 N \rceil
$$

olur. “Üstel düşüş” ifadesinin kaynağı da budur: Alt problem boyutu her adımda $N, N/2, N/4, \ldots$ biçiminde küçülür.

| Yaklaşım | Ön işleme | Tek sorgu | Temel fikir |
|---|---:|---:|---|
| Her sorguda DFS/BFS | $O(1)$ | $O(N)$ | Tüm düğümleri tara |
| Her çiftin mesafesini saklama | $O(N^2)$ | $O(1)$ | Çok fazla bellek kullan |
| Centroid decomposition | $O(N\log N)$ | Genellikle $O(\log N)$ | Yalnızca merkez atalarını incele |

## Mesafeler neden korunuyor?

Ağaçta iki düğüm arasında yalnızca tek bir basit yol vardır. Bir sorgu düğümü $u$ ile hedef $v$ arasındaki yol, centroid hiyerarşisindeki uygun bir merkez $c$ üzerinden temsil edilebilir. Mesafe şu şekilde birleştirilir:

$$
d(u,v)=d(u,c)+d(c,v)
$$

Bu eşitlik yalnızca $c$ gerçek yol üzerindeyse doğrudan geçerlidir. Dinamik en yakın işaretli düğüm probleminde ise her centroid için işaretli düğümlere ait en küçük uzaklık tutulur; üçgen eşitsizliği ve ortak centroid ataları sayesinde doğru minimum bulunur.

## Temel kurulum

Aşağıdaki C++ kodu alt ağaç boyutlarını hesaplar, merkezi bulur ve centroid ağacını kurar:

```cpp
vector<vector<int>> graph;
vector<int> subtree, centroidParent;
vector<bool> removed;

int calculateSize(int node, int parent) {
    subtree[node] = 1;
    for (int next : graph[node]) {
        if (next != parent && !removed[next])
            subtree[node] += calculateSize(next, node);
    }
    return subtree[node];
}

int findCentroid(int node, int parent, int total) {
    for (int next : graph[node]) {
        if (next != parent && !removed[next] &&
            subtree[next] > total / 2)
            return findCentroid(next, node, total);
    }
    return node;
}

void decompose(int entry, int parent) {
    int total = calculateSize(entry, -1);
    int centroid = findCentroid(entry, -1, total);

    centroidParent[centroid] = parent;
    removed[centroid] = true;

    for (int next : graph[centroid]) {
        if (!removed[next])
            decompose(next, centroid);
    }
}
```

`calculateSize` etkin bileşenin büyüklüklerini çıkarır. `findCentroid`, yarıdan büyük bir alt ağaç gördükçe o yöne ilerler. `decompose` ise bulunan merkezi geçici olarak kaldırıp kalan bileşenleri bağımsız problemlere dönüştürür. Her seviyede toplam çalışma $O(N)$, seviye sayısı $O(\log N)$ olduğundan kurulum $O(N\log N)$ sürer.

## Sorgu modeli

En yakın işaretli düğüm örneğinde her centroid için `best[c]`, o merkezin bildiği en yakın işaretli düğüm mesafesidir. Bir düğüm işaretlenirken centroid ataları dolaşılıp değerler güncellenir. Sorguda da

$$
\min_c \bigl(best[c] + d(u,c)\bigr)
$$

hesaplanır. Ataların sayısı logaritmik olduğu için güncelleme ve sorgu çoğunlukla $O(\log N)$ zamanda tamamlanır; mesafeler ayrıca hesaplanıyorsa LCA kullanımı maliyeti $O(\log^2 N)$ yapabilir.

Centroid decomposition özellikle dinamik mesafe sorguları, belirli uzunluktaki yolların sayılması ve renkli düğüm problemlerinde parlar. Uygulaması biraz dikkat ister: kaldırılmış düğümleri atlamak, mesafeleri doğru seviyede saklamak ve çift sayımı engellemek şarttır. Ancak doğru kurulduğunda dev bir ağacı, yalnızca birkaç logaritmik adımdan oluşan düzenli bir sorgu makinesine dönüştürür.
