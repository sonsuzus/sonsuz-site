---
layout: post
title: "Dinamik Programlamada Profil Maskeleme ile Fayans Kaplama"
math: true
categories: 
  - Bilgi
tags: 
  - dinamik programlama
  - bit maskesi
  - profil dp
toc: true
---

Bir tahtayı domino taşlarıyla kaplamak ilk bakışta basit bir yapboz gibi görünür. Ancak tahta büyüdükçe olası yerleşimleri tek tek denemek, bilgisayarı kısa sürede matematiksel bir bataklığa sürükler. Profil maskeleme, satır satır veya sütun sütun ilerleyerek yalnızca sınırdaki doluluk bilgisini saklar; böylece devasa bir arama ağacını küçük ve tekrar kullanılabilir durumlara dönüştürür.
``

## Temel fikir: Geçmişin tamamı değil, sınırı önemlidir

Elimizde $N \times M$ boyutunda bir tahta ve her biri iki komşu hücreyi kaplayan $1 \times 2$ domino taşları olsun. Amaç, tahtanın kaç farklı biçimde tamamen kaplanabileceğini bulmaktır.

Hücreleri soldan sağa, satır bitince bir alt satıra geçerek işlediğimizi düşünelim. Önceki satırlardaki taşların tam yerleşimini bilmemize gerek yoktur. Yalnızca dikey yerleştirilen taşların mevcut satırdaki hangi hücreleri önceden doldurduğunu bilmek yeterlidir.

Bu bilgi bir bit maskesiyle tutulabilir:

- Bit `1`: Hücre önceki yerleştirmeden dolayı dolu.
- Bit `0`: Hücre henüz boş.
- $M$ sütun için toplam durum sayısı en fazla $2^M$ olur.

Örneğin $M=4$ ve maske `0101` ise birinci ve üçüncü hücreler doludur. Bitlerin hangi yönde okunduğu uygulamaya bağlıdır; önemli olan tutarlı olmaktır.

| Yaklaşım | Saklanan bilgi | Yaklaşık durum uzayı | Sonuç |
|---|---|---:|---|
| Kaba kuvvet | Tüm taş yerleşimleri | Üstel ve çok büyük | Küçük tahtalarda çalışır |
| Klasik DP | İşlenen hücre ve ayrıntılı geçmiş | Gereğinden büyük olabilir | Tasarlaması zorlaşır |
| Profil DP | Yalnızca sınır maskesi | $O(NM2^M)$ | Dar tahtalarda etkilidir |

## Durum ve geçişler

Bir hücreyi işlerken iki temel durum vardır. Hücre maskede doluysa onu atlar, ilgili biti temizler ve sonraki hücreye geçeriz. Hücre boşsa dominoyu yatay ya da dikey yerleştirmeyi deneriz.

Yatay yerleştirme için sağdaki hücre bulunmalı ve boş olmalıdır. Dikey yerleştirme için alt satır bulunmalıdır; bu taşın alt yarısını gelecekte hatırlamak amacıyla maskeye uygun bit eklenir.

DP durumu kabaca şöyle tanımlanabilir:

$$dp[pos][mask] = \text{pos konumuna kadar gelip mask durumunu üretme sayısı}$$

Her durumda en fazla iki yerleştirme denendiğinden karmaşıklık genellikle

$$O(N \cdot M \cdot 2^M)$$

seviyesindedir. Bu nedenle gerekirse tahtayı döndürüp $M=\min(N,M)$ seçmek ciddi hız kazandırır.

## C++ ile uygulama

Aşağıdaki özyinelemeli DP, hücreleri doğrusal sırada gezer. `mask` değişkeninin en düşük biti mevcut hücrenin doluluk bilgisini temsil eder.

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, m;
map<pair<int, int>, long long> memo;

long long solve(int pos, int mask) {
    if (pos == n * m)
        return mask == 0;

    auto key = make_pair(pos, mask);
    if (memo.count(key)) return memo[key];

    int row = pos / m;
    int col = pos % m;
    long long ways = 0;

    if (mask & 1) {
        // Mevcut hücre önceden doldurulmuş; profile ilerle.
        ways = solve(pos + 1, mask >> 1);
    } else {
        // Yatay domino: sağdaki hücre boş ve aynı satırda olmalı.
        if (col + 1 < m && !(mask & 2))
            ways += solve(pos + 2, mask >> 2);

        // Dikey domino: alt hücreyi gelecekte dolu gösterecek biti ekle.
        if (row + 1 < n)
            ways += solve(pos + 1, (mask >> 1) | (1 << (m - 1)));
    }

    return memo[key] = ways;
}
```

Buradaki bit kaydırmalar, profil penceresini hücrelerle birlikte ilerletir. Yatay taş iki mevcut hücreyi tükettiği için iki konum atlanır. Dikey taşta ise alt hücre henüz ziyaret edilmediğinden, bilgi maskenin en yüksek bitine yazılır.

## Ne zaman kullanılır?

Profil DP yalnızca domino kaplama için değildir. Izgarada bağımsız hücre seçimi, engelli yollar, eşleştirme ve bağlantı kısıtları gibi problemlerde de kullanılabilir. Ana soru şudur: “İşlenmiş bölgenin geleceği etkileyen en küçük özeti nedir?” Cevap dar bir sınırsa, bit maskesi büyük ihtimalle doğru araçtır.

Kısacası profil maskeleme, geçmişi unutma sanatıdır: Tahtanın tamamını değil, yalnızca geleceğin gerçekten ihtiyaç duyduğu izleri hatırlar.
