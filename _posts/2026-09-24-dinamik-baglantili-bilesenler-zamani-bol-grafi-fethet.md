---
layout: post
title: "Dinamik Bağlantılı Bileşenler: Zamanı Böl, Grafı Fethet"
math: true
categories: 
  - Bilgi
tags: 
  - graf
  - algoritma
  - böl-ve-fethet
  - dsu
  - çevrimdışı-sorgular
  - dinamik-bağlantılılık
toc: true
image: /img/dinamik-baglantili-bilesenler-37.png
---

Bir sosyal ağda arkadaşlıklar kuruluyor, bozuluyor ve arada “Ali ile Ayşe hâlâ dolaylı olarak bağlantılı mı?” soruları geliyor. Graf sürekli değişirken her sorguda baştan DFS çalıştırmak mümkündür; fakat performansınız kısa sürede dramatik bir vedaya hazırlanır. Çevrimdışı dinamik bağlantılılık, tüm işlemleri önceden bilmenin avantajını kullanarak zamanı parçalara ayırır ve bağlantıları geri alınabilir bir DSU ile takip eder.

``

## Problem neden zor?

Yalnızca kenar eklenen bir grafta Disjoint Set Union, yani DSU, mükemmel çalışır. `union(u, v)` bileşenleri birleştirir; `find(u) == find(v)` ise iki düğümün bağlı olup olmadığını söyler. Ancak standart DSU, silinen bir kenarı unutamaz. Çünkü birleşim sonrasında hangi değişikliklerin geri alınması gerektiğini saklamaz.

Elimizde zaman sırasına göre şu işlemler bulunsun:

- `add(u, v)`: Kenarı ekle.
- `remove(u, v)`: Kenarı sil.
- `query(u, v)`: Düğümler bağlı mı?

Her kenarın etkin olduğu aralığı $[L, R)$ şeklinde belirleyebiliriz. Burada kenar $L$ anında eklenmiş, $R$ anında kaldırılmıştır. Hiç kaldırılmayan kenarlar için $R = Q$ alınır; $Q$ toplam işlem sayısıdır.

## Zaman üzerinde bölümleme

İşlem zamanlarını kapsayan bir segment ağacı kurarız. Bir kenar hangi zaman aralığında etkinse onu, bu aralığı tamamen örten segment ağacı düğümlerine ekleriz. Böylece her kenar en fazla $O(log Q)$ düğümde tutulur.

| Yaklaşım | Kenar silme | Sorgu maliyeti | Temel fikir |
|---|---:|---:|---|
| Her sorguda DFS/BFS | Kolay | $O(N+M)$ | Grafı yeniden tara |
| Standart DSU | Desteklemez | Yaklaşık $O(1)$ | Yalnızca birleşim |
| Segment ağacı + rollback DSU | Destekler | Çevrimdışı verimli | Zamanı böl, durumu geri al |

![dinamik-baglantili-bilesenler-37](/img/dinamik-baglantili-bilesenler-37.svg)


Segment ağacında DFS yaparken bir düğüme ait bütün kenarları DSU’ya ekleriz. Yaprak noktası tek bir zamanı temsil eder; dolayısıyla o andaki sorguyu güncel DSU ile cevaplarız. Alt ağaçtan dönerken yapılan birleşimleri geri alırız. Algoritmanın küçük numarası tam olarak budur: zamanda ileri giderken birleştir, geriye çıkarken hafızayı temizle.

## Geri alınabilir DSU

Rollback yapılabilmesi için yol sıkıştırma kullanmamalıyız. Yol sıkıştırma çok sayıda ebeveyn değerini sessizce değiştirerek geri alma işlemini karmaşıklaştırır. Bunun yerine union-by-size kullanılır; böylece ağaç yüksekliği $O(log N)$ sınırında kalır.

```cpp
struct RollbackDSU {
    vector<int> parent, size;
    vector<pair<int, int>> history;

    RollbackDSU(int n) : parent(n), size(n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        while (x != parent[x]) x = parent[x];
        return x;
    }

    int snapshot() { return history.size(); }

    void unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) {
            history.push_back({-1, -1});
            return;
        }
        if (size[a] < size[b]) swap(a, b);
        history.push_back({b, size[a]});
        parent[b] = a;
        size[a] += size[b];
    }

    void rollback(int snap) {
        while ((int)history.size() > snap) {
            auto [b, oldSize] = history.back();
            history.pop_back();
            if (b == -1) continue;
            int a = parent[b];
            parent[b] = b;
            size[a] = oldSize;
        }
    }
};
```

`snapshot`, mevcut geçmiş uzunluğunu kaydeder. `rollback`, bu uzunluğa ulaşana kadar değişiklikleri tersine çevirir. Başarısız birleşimler için de işaret bırakılması, her çağrının geçmişte karşılığının bulunmasını sağlar.

## Karmaşıklık ve kullanım alanları

Her etkinlik aralığı segment ağacına $O(log Q)$ kez yerleştirilir. Union-by-size ile `find` maliyeti $O(log N)$ olduğundan toplam süre kabaca $O((M log Q + Q) log N)$, bellek tüketimi ise $O(M log Q + N)$ olur.

Bu yöntem ağ bağlantıları, oyuncu eşleştirme kümeleri, sürüm geçmişleri ve zaman damgalı sosyal ağ analizlerinde oldukça kullanışlıdır. Bedeli, cevapların çevrimiçi üretilememesidir: gelecekteki işlemleri önceden bilmek gerekir. Eğer bütün senaryo elinizdeyse zaman artık düşman değil, segmentlere ayrılmayı bekleyen yardımsever bir boyuttur.
