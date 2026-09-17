---
layout: post
title: "Konveks Zarf Hilesi ile Dinamik Programlamayı Jet Hızına Çıkarma"
math: true
categories: 
  - Bilgi
tags: 
  - dinamik programlama
  - konveks zarf hilesi
  - cht
  - algoritma
  - c++
  - optimizasyon
toc: true
image: /img/konveks-zarf-hilesi-21.png
---

![konveks-zarf-hilesi-21](/img/konveks-zarf-hilesi-21.svg)


Dinamik programlama bazen doğru bağıntıyı bulduğumuz hâlde bizi $O(n^2)$ karmaşıklığıyla baş başa bırakır. Konveks Zarf Hilesi, İngilizce adıyla **Convex Hull Trick (CHT)**, belirli biçimdeki geçişleri doğru parçaları olarak yorumlayarak bu maliyeti $O(n\log n)$, hatta uygun koşullarda $O(n)$ seviyesine indirebilir. Yani iç içe döngüleri geometrinin küçük ama etkili bir numarasıyla değiştiririz.
``

## CHT hangi bağıntılarda kullanılabilir?

Şu klasik DP geçişini ele alalım:

$$
dp[i] = \min_{j<i}\{dp[j] + a[j]\cdot x[i] + b[j]\}
$$

Sabit bir $i$ için $x[i]$ bellidir. Her $j$ seçeneği ise

$$
y = m_jx + c_j
$$

biçiminde bir doğru oluşturur. Burada $m_j=a[j]$ eğim, $c_j=dp[j]+b[j]$ sabit terimdir. Dolayısıyla $dp[i]$, bütün doğruların $x[i]$ noktasındaki minimum değeridir.

Naif çözüm her $i$ için tüm eski doğruları dener. CHT ise yalnızca gelecekte gerçekten en iyi olabilecek doğruları saklar. Bir doğru hiçbir $x$ değerinde minimum olamıyorsa zarftan çıkarılır; geometrik olarak alt konveks zarf korunur.

| Özellik | Naif DP | CHT ile DP |
|---|---:|---:|
| Her durumdaki aday sayısı | $O(n)$ | Amortize $O(1)$ veya $O(\log n)$ |
| Toplam karmaşıklık | $O(n^2)$ | $O(n)$ ya da $O(n\log n)$ |
| Gerekli yapı | İç içe döngü | Doğrular ve sorgular |
| Temel koşul | Yok | Geçişin doğrusal biçime dönüşmesi |

## Bir doğru ne zaman gereksizdir?

Eğimleri sıralı üç doğru düşünelim: $L_1$, $L_2$ ve $L_3$. Eğer $L_1$ ile $L_2$ kesişimi, $L_2$ ile $L_3$ kesişiminin sağında kalıyorsa $L_2$ hiçbir zaman en iyi seçenek olamaz. Bölme işlemi ve kayan nokta hatalarından kaçınmak için kesişimleri çapraz çarparak karşılaştırabiliriz.

Doğruların eğimleri monoton ekleniyor ve sorgu değerleri $x$ de monoton geliyorsa bir `deque` yeterlidir. Ön taraftaki doğru, sıradaki doğrudan kötü olduğunda silinir. Böylece her doğru en fazla bir kez eklenir ve bir kez çıkarılır.

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Line {
    ll m, b;
    ll value(ll x) const { return m * x + b; }
};

// Orta doğru, alt zarf üzerinde gereksiz mi?
bool redundant(const Line& a, const Line& b, const Line& c) {
    return (__int128)(b.b - a.b) * (b.m - c.m)
         >= (__int128)(c.b - b.b) * (a.m - b.m);
}

struct MonotoneCHT {
    deque<Line> hull;

    // Eğimlerin azalan sırada geldiği varsayılıyor.
    void add(ll m, ll b) {
        Line line{m, b};
        while (hull.size() >= 2 &&
               redundant(hull[hull.size() - 2], hull.back(), line))
            hull.pop_back();
        hull.push_back(line);
    }

    // x değerlerinin artan sırada sorgulandığı varsayılıyor.
    ll query(ll x) {
        while (hull.size() >= 2 &&
               hull[0].value(x) >= hull[1].value(x))
            hull.pop_front();
        return hull.front().value(x);
    }
};
```

`__int128`, çarpımların `long long` sınırını aşma riskini azaltır. Ancak doğru değerlerinin kendisi de taşabilecekse `value` fonksiyonunda aynı tür kullanılmalıdır.

## Monotonluk yoksa ne olacak?

Eğimler veya sorgular sıralı değilse deque sürümü güvenli değildir. Bu durumda iki yaygın seçenek vardır:

| Yöntem | Kullanım durumu | Karmaşıklık |
|---|---|---:|
| Kesişim noktalarıyla CHT | Eğimler sıralı, sorgular karışık | $O(\log n)$ sorgu |
| Li Chao ağacı | Eğimler ve sorgular tamamen karışık | $O(\log X)$ |

Li Chao ağacı, belirli bir $x$ aralığında doğruları segment ağacına benzer biçimde tutar. Biraz daha fazla bellek kullanır ama monotonluk şartlarını ortadan kaldırır.

CHT uygularken önce bağıntıdaki $j$ kaynaklı ifadeleri eğim ve sabit terime, $i$ kaynaklı ifadeyi ise sorgu koordinatına ayır. Ardından minimum mu maksimum mu aradığını, eşit eğimlerin nasıl yönetileceğini ve sayı taşmalarını kontrol et. Doğru cebir yapıldığında konveks zarf hilesi, ürkütücü görünen karesel DP’leri oldukça zarif algoritmalara dönüştürür.
