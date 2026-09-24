---
layout: post
title: "Dinamik Programlamada Hız Sihri: Knuth Optimizasyonunun Sırları"
math: true
categories: 
  - Bilgi
tags: 
  - dinamik programlama
  - knuth optimizasyonu
  - algoritma
  - cpp
  - zaman karmaşıklığı
  - interval dp
toc: true
image: /img/dinamik-programlamada-hiz-66.png
---

Dinamik programlama bazen doğru bağıntıyı bulduğumuz anda bizi sevindirir, ardından $O(N^3)$ zaman karmaşıklığıyla moralimizi bozar. Özellikle bir aralığı en uygun noktadan bölmeye dayanan problemlerde aynı geçişler tekrar tekrar incelenir. Knuth optimizasyonu, optimum bölme noktalarının düzenli hareket ettiğini matematiksel olarak kanıtlayabildiğimiz durumlarda bu kübik maliyeti $O(N^2)$ seviyesine indiren zarif bir tekniktir.

``

## Kübik karmaşıklık nereden geliyor?

Elimizde $[i,j]$ aralığının minimum maliyetini hesaplayan bir interval DP bulunduğunu düşünelim. Yaygın bağıntı şöyledir:

$$dp[i][j] = \min_{i \le k < j} \{dp[i][k] + dp[k+1][j] + C(i,j)\}$$

Burada $k$ bölme noktası, $C(i,j)$ ise mevcut aralığı birleştirmenin veya işlemenin maliyetidir. Toplam $O(N^2)$ farklı aralık vardır. Her aralık için $O(N)$ bölme noktası denendiğinde sonuç kaçınılmazdır:

$$O(N^2) \cdot O(N) = O(N^3)$$

Knuth'un temel fikri, her aralıkta bütün $k$ değerlerini denememektir. $opt[i][j]$, $dp[i][j]$ sonucunu veren en iyi bölme noktası olsun. Gerekli matematiksel koşullar sağlanıyorsa şu monotonluk ortaya çıkar:

$$opt[i][j-1] \le opt[i][j] \le opt[i+1][j]$$

Yani yeni optimum, komşu aralıkların optimumları arasında bulunur. Arama alanı dramatik biçimde küçülür.

## Hangi koşullarda kullanılabilir?

Knuth optimizasyonu her interval DP bağıntısına serpilebilen sihirli bir baharat değildir. Maliyet fonksiyonunun monotonluk ve dörtgen eşitsizliği olarak bilinen özellikleri sağlaması gerekir. $a \le b \le c \le d$ için yaygın yeterli koşullar şunlardır:

$$C(b,c) \le C(a,d)$$

$$C(a,c) + C(b,d) \le C(a,d) + C(b,c)$$

İkinci ifade, maliyet matrisinin Monge benzeri bir yapıya sahip olduğunu söyler. Başka bir deyişle, aralıklar genişledikçe optimum kararlar rastgele sağa sola sıçramaz.

| Özellik | Klasik Interval DP | Knuth Optimizasyonu |
|---|---:|---:|
| Durum sayısı | $O(N^2)$ | $O(N^2)$ |
| Geçiş aralığı | En fazla $O(N)$ | Komşu optimumlarla sınırlı |
| Toplam süre | $O(N^3)$ | $O(N^2)$ |
| Bellek | $O(N^2)$ | $O(N^2)$ |
| Ek gereksinim | Yok | Monoton optimum ve uygun maliyet |

## C++ ile uygulama

Aşağıdaki örnek, elemanları ardışık biçimde birleştirmenin minimum maliyetini hesaplar. $C(i,j)$, prefix sum kullanılarak aralık toplamı olarak alınır:

```cpp
#include <bits/stdc++.h>
using namespace std;

long long knuthMergeCost(const vector<int>& a) {
    int n = a.size();
    const long long INF = (1LL << 62);

    vector<long long> prefix(n + 1, 0);
    for (int i = 0; i < n; ++i)
        prefix[i + 1] = prefix[i] + a[i];

    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    vector<vector<int>> opt(n, vector<int>(n, 0));

    for (int i = 0; i < n; ++i)
        opt[i][i] = i;

    for (int len = 2; len <= n; ++len) {
        for (int i = 0; i + len <= n; ++i) {
            int j = i + len - 1;
            dp[i][j] = INF;

            int left = opt[i][j - 1];
            int right = min(j - 1, opt[i + 1][j]);
            long long cost = prefix[j + 1] - prefix[i];

            for (int k = left; k <= right; ++k) {
                long long candidate = dp[i][k] + dp[k + 1][j] + cost;
                if (candidate < dp[i][j]) {
                    dp[i][j] = candidate;
                    opt[i][j] = k;
                }
            }
        }
    }
    return dp[0][n - 1];
}
```

Kod aralıkları kısa uzunluktan başlayarak hesaplar; böylece ihtiyaç duyulan alt problemler ve komşu `opt` değerleri hazır olur. Prefix sum sayesinde $C(i,j)$ maliyeti $O(1)$ zamanda bulunur.

## En önemli tuzak

Optimum noktaların örnek testlerde monoton görünmesi bir kanıt değildir. Koşullar sağlanmadan arama aralığını daraltmak, hızlı fakat yanlış bir algoritma üretir. Önce bağıntıyı standart interval DP biçimine dönüştürün, ardından maliyet fonksiyonunu matematiksel olarak inceleyin. Uygunsa Knuth optimizasyonu yalnızca performans artışı değil, kübik bir çözümü uygulanabilir hâle getiren gerçek bir algoritmik süper güçtür.

![dinamik-programlamada-hiz-66](/img/dinamik-programlamada-hiz-66.svg)

