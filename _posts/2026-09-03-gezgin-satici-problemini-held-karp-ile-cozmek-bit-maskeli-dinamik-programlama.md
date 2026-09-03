---
layout: post
title: "Gezgin Satıcı Problemini Held-Karp ile Çözmek: Bit Maskeli Dinamik Programlama"
math: true
categories: 
  - Bilgi
tags: 
  - dinamik programlama
  - bit maskesi
  - held-karp
toc: true
---

Bir satıcının belirli şehirlerin tümünü tam bir kez ziyaret edip başladığı şehre dönmesi gerekiyor. Üstelik toplam yol mümkün olduğunca kısa olmalı! Gezgin Satıcı Problemi, yani TSP, tanımı basit fakat çözümü hesaplama açısından oldukça zorlu bir optimizasyon problemidir. Held-Karp algoritması ise gereksiz rota tekrarlarını ortadan kaldırarak faktöriyel aramayı dinamik programlama ve bit maskeleri yardımıyla daha yönetilebilir bir üstel çözüme dönüştürür.

``

## Neden bütün rotaları denemiyoruz?

Başlangıç şehrini sabitlersek geriye kalan $n-1$ şehir farklı sıralarla ziyaret edilebilir. Dolayısıyla kaba kuvvet yaklaşımı yaklaşık $(n-1)!$ rota inceler. Küçük sayılar masum görünse de 15 veya 20 şehir civarında işlem sayısı hızla kontrolden çıkar.

Held-Karp şu gözleme dayanır: Aynı şehir kümesini gezip aynı son şehirde duran iki kısmi rotadan yalnızca daha ucuz olanı gelecekteki çözüm için önemlidir. Pahalı rotayı saklamak gereksizdir.

| Yaklaşım | Zaman karmaşıklığı | Bellek | Temel fikir |
|---|---:|---:|---|
| Kaba kuvvet | $O(n!)$ | $O(n)$ | Tüm sıralamaları dene |
| Held-Karp | $O(n^2 2^n)$ | $O(n 2^n)$ | Alt kümelerin en iyi maliyetini sakla |
| Sezgisel yöntemler | Değişken | Değişken | Hızlı fakat optimal olmayabilir |

Held-Karp hâlâ üstel karmaşıklığa sahiptir; yani yüzlerce şehir için sihirli değnek değildir. Buna rağmen faktöriyel büyümeye kıyasla büyük bir ilerleme sağlar ve kesin sonuç üretir.

## Durumların bit maskesiyle gösterilmesi

Her şehir bir bit ile temsil edilir. Örneğin dört şehir için `0101` maskesi, 0 ve 2 numaralı şehirlerin ziyaret edildiğini anlatır. Bir şehrin kümede olup olmadığı şu işlemle kontrol edilir:

```python
if mask & (1 << city):
    print('Şehir ziyaret edilmiş')
```

Dinamik programlama durumunu $dp[S][j]$ olarak tanımlayalım. Bu değer, 0 numaralı şehirden başlayıp $S$ kümesindeki bütün şehirleri ziyaret ederek $j$ şehrinde biten en kısa yolun maliyetidir.

Başlangıç koşulu:

$$dp[\{0\}][0] = 0$$

Geçiş bağıntısı ise şöyledir:

$$dp[S][j] = \min_{k \in S, k \ne j}(dp[S-\{j\}][k] + d[k][j])$$

Burada $d[k][j]$, iki şehir arasındaki mesafedir. Son aşamada son şehirden başlangıca dönüş maliyeti eklenir.

## Python uygulaması

Aşağıdaki fonksiyon hem minimum maliyeti hem de optimal rotayı üretir. `parent` sözlüğü, çözüm tamamlandıktan sonra rotayı geriye doğru kurmak için kullanılır.

```python
def held_karp(distance):
    n = len(distance)
    dp = {(1, 0): 0}
    parent = {}

    for mask in range(1, 1 << n):
        if not (mask & 1):
            continue

        for last in range(1, n):
            if not (mask & (1 << last)):
                continue

            previous_mask = mask ^ (1 << last)
            candidates = []

            for previous in range(n):
                state = (previous_mask, previous)
                if previous_mask & (1 << previous) and state in dp:
                    cost = dp[state] + distance[previous][last]
                    candidates.append((cost, previous))

            if candidates:
                dp[(mask, last)], parent[(mask, last)] = min(candidates)

    full_mask = (1 << n) - 1
    total, last = min(
        (dp[(full_mask, city)] + distance[city][0], city)
        for city in range(1, n)
    )

    mask = full_mask
    reversed_route = [last]
    while last != 0:
        previous = parent[(mask, last)]
        mask ^= 1 << last
        last = previous
        reversed_route.append(last)

    route = list(reversed(reversed_route)) + [0]
    return total, route
```

Mesafe matrisi simetrik olmak zorunda değildir; bu nedenle algoritma yönlü maliyetlerle de çalışabilir. Ancak eksik bağlantılar varsa bu kenarların maliyeti sonsuz kabul edilmeli ve ulaşılamayan durumlar ayrıca ele alınmalıdır.

## Pratik sınırlar

Algoritmada yaklaşık $n2^n$ durum saklanır ve her durum için en fazla $n$ önceki şehir incelenir. Bellek genellikle zamandan önce sınıra ulaşabilir. Yalnızca minimum maliyet isteniyorsa katmanlı DP ile bellek azaltılabilir; fakat rotayı yeniden oluşturmak için ek bilgi gerekir.

Held-Karp, dinamik programlamanın özünü güzel biçimde gösterir: Aynı alt problemi tekrar çözmek yerine sonucunu sakla. Bit maskesi de kümeleri küçük ve hızlı tamsayılara dönüştürür. Böylece “bütün rotaları dene” yaklaşımı, sistematik ve matematiksel olarak optimal bir aramaya dönüşür.
