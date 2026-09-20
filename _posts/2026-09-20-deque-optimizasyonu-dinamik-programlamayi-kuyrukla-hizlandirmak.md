---
layout: post
title: "Deque Optimizasyonu: Dinamik Programlamayı Kuyrukla Hızlandırmak"
math: true
categories: 
  - Bilgi
tags: 
  - dinamik programlama
  - deque
  - monoton kuyruk
  - algoritma
  - optimizasyon
  - cplusplus
toc: true
---

Dinamik programlama bazen doğru bağıntıyı bulduğumuz anda bitmiş gibi görünür. Sonra zaman karmaşıklığını hesaplarız ve karşımıza tatsız bir $O(nk)$ çıkar! Neyse ki geçişler belirli bir pencere içindeki minimum veya maksimum değere dayanıyorsa, çift uçlu kuyruk yani `deque` yardımımıza yetişebilir.
``
## Temel problem nerede?

Şöyle bir DP bağıntısı düşünelim:

$$
dp[i] = cost[i] + \min_{i-k \leq j < i} dp[j]
$$

Burada `dp[i]`, önceki en fazla $k$ durumdan birine geçilerek hesaplanıyor. Her `i` için geriye dönüp $k$ elemanı tek tek incelersek toplam karmaşıklık:

$$
O(n \cdot k)
$$

olur. $n$ ve $k$ yüz binler seviyesindeyse programımız kahvesini içip dönmemizi beklemeden zaman aşımına uğrar.

Aslında her adımda ihtiyacımız olan şey bütün pencere değil, yalnızca pencerenin minimum elemanıdır. Ayrıca pencere ilerledikçe bazı eski indeksler geçersiz hâle gelir. Deque, bu iki gereksinimi aynı anda yönetir.

## Monoton deque mantığı

Deque içinde DP değerleri artan sırada olacak biçimde indeksler saklarız. Böylece kuyruğun önündeki indeks her zaman geçerli pencerenin minimum değerini temsil eder.

Her yeni `i` için üç işlem yapılır:

1. Pencerenin dışında kalan indeksleri önden çıkar.
2. Öndeki indeksle `dp[i]` değerini hesapla.
3. Arkadan, `dp[i]` değerinden büyük veya eşit değerleri çıkar ve `i` indeksini ekle.

Neden büyük değerleri siliyoruz? Yeni değer hem daha küçük hem de daha yeni olduğundan, büyük olan eski değer gelecekte hiçbir zaman minimum seçilemez. Kısacası onu kuyrukta tutmak yalnızca kalabalık yapar.

| Yaklaşım | Bir durumun maliyeti | Toplam karmaşıklık | Ek yapı |
|---|---:|---:|---|
| İç içe döngü | $O(k)$ | $O(nk)$ | Yok |
| Dengeli ağaç | $O(\log k)$ | $O(n\log k)$ | Multiset |
| Monoton deque | Amortize $O(1)$ | $O(n)$ | Deque |

## C++ uygulaması

Aşağıdaki kod, her konuma ulaşma maliyetini hesaplar. Bir konuma yalnızca önceki $k$ konumdan geçilebildiğini varsayıyoruz:

```cpp
#include <iostream>
#include <vector>
#include <deque>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;

    vector<long long> cost(n), dp(n);
    for (long long &x : cost) cin >> x;

    deque<int> dq;
    dp[0] = cost[0];
    dq.push_back(0);

    for (int i = 1; i < n; ++i) {
        // Artık pencereye ait olmayan indeksleri temizle.
        while (!dq.empty() && dq.front() < i - k)
            dq.pop_front();

        // Öndeki indeks, penceredeki minimum DP değeridir.
        dp[i] = cost[i] + dp[dq.front()];

        // Artan monotonluğu bozan değerleri kaldır.
        while (!dq.empty() && dp[dq.back()] >= dp[i])
            dq.pop_back();

        dq.push_back(i);
    }

    cout << dp[n - 1] << '\n';
}
```

Kodda her indeks deque'e yalnızca bir kez girer ve en fazla bir kez çıkar. Bazı iterasyonlarda çok sayıda `pop_back` görülse bile toplam çıkarma sayısı $n$ değerini aşmaz. Bu nedenle işlem maliyeti amortize olarak $O(1)$ kabul edilir.

## Ne zaman kullanılabilir?

Deque optimizasyonu her DP bağıntısına sihirli değnek sallamaz. Geçiş kümesi kayan bir aralık olmalı ve bu aralıktan minimum ya da maksimum gibi monoton biçimde yönetilebilen bir sonuç aranmalıdır.

| Uygun durum | Uygun olmayan durum |
|---|---|
| Kayan aralık minimumu | Keyfî indekslerden geçiş |
| Kayan aralık maksimumu | Tüm elemanların medyanı |
| Sabit veya düzenli pencere | Karmaşık, değişken bağlantılar |

Maksimum arıyorsak yalnızca karşılaştırmaları tersine çevirerek deque'i azalan sırada tutarız. Özetle fikir basittir: Gelecekte kazanma ihtimali kalmayan adayları erkenden ele. Dinamik programlama böylece gereksiz geçmişi taşımayı bırakır ve $O(nk)$ çözüm, zarif bir $O(n)$ algoritmaya dönüşür.
