---
layout: post
title: "Link-Cut Tree Nedir? Dinamik Ağaçların Gizli İsviçre Çakısı"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - algoritmalar
  - link-cut tree
toc: true
---

Bir ağacın kenarlarını çalışma anında ekleyip silmek, ardından iki düğüm arasındaki yolun toplamını saniyeler içinde sormak ilk bakışta masum görünür. Ancak klasik DFS, BFS veya sabit köklenmiş ağır-hafif ayrıştırması bu dünyada zorlanır. Link-Cut Tree (LCT), dinamik ormanlar üzerinde bağlantı, yol sorgusu ve kök değiştirme işlemlerini amortize olarak $O(\log n)$ sürede gerçekleştiren gelişmiş bir veri yapısıdır.
``

## Problem: Ağaç Sabit Değilse Ne Olur?

Bir orman düşünelim: Başlangıçta düğümler birbirinden kopuk olabilir, zamanla iki ağacı bir kenarla bağlayabilir veya var olan bir kenarı kaldırabiliriz. Bu sırada şu sorular gelir:

- `u` ve `v` aynı ağaçta mı?
- `u-v` yolundaki düğüm değerlerinin toplamı, minimumu ya da maksimumu nedir?
- `u` düğümünü ağacın kökü kabul edersek `v` nerede konumlanır?
- Bir kenarı silince hangi iki bileşen oluşur?

Sabit bir ağaçta Euler turu, segment tree ve Heavy-Light Decomposition (HLD) harika çözümlerdir. Fakat HLD’nin kurduğu zincirler ağacın yapısı değiştiğinde geçerliliğini kaybedebilir. LCT tam burada sahneye çıkar: Ağacı sürekli yeniden inşa etmek yerine, yalnızca sorgu için gerekli tercih edilen yolları yeniden düzenler.

| Özellik | HLD | Link-Cut Tree |
|---|---:|---:|
| Statik yol sorgusu | $O(\log^2 n)$ | $O(\log n)$ amortize |
| Kenar ekleme/silme | Doğal olarak desteklemez | $O(\log n)$ amortize |
| Alt ağaç sorgusu | Görece kolay | Ek teknik gerektirir |
| Uygulama zorluğu | Orta | Yüksek |

## Temel Fikir: Preferred Path ve Splay Tree

LCT, orijinal ağacı doğrudan tek bir ikili arama ağacında tutmaz. Bunun yerine bazı kök-yaprak yollarını **preferred path** olarak seçer. Her tercih edilen yol bir **splay tree** ile temsil edilir. Splay tree, yakın zamanda erişilen düğümleri köke yaklaştıran kendini dengeleyen bir ikili ağaçtır.

Bir düğüm için iki ayrı ebeveyn kavramı bulunur: splay ağacındaki ebeveyn ve asıl ormandaki bağlantıyı temsil eden `path-parent`. Bu ayrım, LCT kodunun ilk okuyuşta büyülü görünmesinin ana nedenidir. Ancak sonuç nettir: `access(x)` işlemi, kökten `x`e uzanan yolu parçalara ayırıp yeniden düzenler. Böylece istenen yol tek bir yardımcı ağaçta görünür hâle gelir.

Amortize maliyet, splay işlemlerinin analizinden gelir. Tek bir adım pahalılaşabilir; fakat çok sayıda işlemde ortalama maliyet:

$$T(m)=O(m\log n)$$

olur. Dolayısıyla işlem başına maliyet $O(\log n)$ amortizedir.

## Dört Kritik Operasyon

LCT’nin pratikte en önemli operasyonları aşağıdaki gibidir:

| Operasyon | Görev |
|---|---|
| `makeroot(x)` | Ağacı mantıksal olarak `x` köklü yapar |
| `access(x)` | Kökten `x`e giden yolu erişilebilir kılar |
| `findroot(x)` | `x`in bileşen kökünü bulur |
| `link(x, y)` / `cut(x, y)` | Kenar ekler veya kaldırır |

`makeroot(x)` genellikle `access(x)` sonrası splay ağacındaki çocukları ters çeviren bir `rev` bayrağıyla uygulanır. Bu bayrak lazy propagation mantığıyla aşağı doğru yayılır. Yol toplamı için her düğümde örneğin `sum` tutulursa:

$$sum(x)=sum(left(x))+value(x)+sum(right(x))$$

eşitliği her rotasyondan sonra güncellenir.

## Yol Toplamı Sorgusu

Aşağıdaki iskelet, `u-v` yolunu tek bir splay ağacında toplama fikrini gösterir. `sum[v]`, gerekli `pull` güncellemelerinden sonra yolun toplamını verir.

```cpp
long long pathSum(int u, int v) {
    makeRoot(u);   // u'yu temsil edilen ağacın kökü yap
    access(v);     // u-v yolu v'nin yardımcı ağacında görünür olur
    return sum[v]; // yol üzerindeki düğüm değerlerinin toplamı
}

void link(int u, int v) {
    makeRoot(u);
    if (findRoot(v) != u) parent[u] = v; // döngü oluşturma
}

void cut(int u, int v) {
    makeRoot(u);
    access(v);
    // u, v'nin sol çocuğuysa ve arada başka düğüm yoksa kenarı kopar
    if (left[v] == u && right[u] == 0) {
        left[v] = parent[u] = 0;
        pull(v);
    }
}
```

Bu kodun güvenli çalışması için `rotate`, `splay`, `push` ve `pull` fonksiyonlarının kusursuz yazılması gerekir. Özellikle tersleme bayrağını rotasyon öncesinde üstten alta doğru itmemek, nadir görünen ama yıkıcı hatalara yol açar.

## Ne Zaman Kullanılmalı?

Çevrim içi kenar ekleme-silme ve yol sorguları birlikte isteniyorsa LCT çok güçlüdür: dinamik minimum yayılım ağacı yaklaşımları, sürüm kontrolündeki hiyerarşiler, ağ topolojileri ve yarışma programlama problemleri buna örnektir. Buna karşılık yalnızca statik bir ağaçta alt ağaç sorgusu yapıyorsanız Euler turu ile segment tree daha okunabilir ve daha az hatalı bir tercihtir. LCT bir çekiç değil; karmaşık dinamik ağaç problemleri için özel tasarlanmış, dikkatle kullanılacak bir cerrahi alettir.
