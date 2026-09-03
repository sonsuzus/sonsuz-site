---
layout: post
title: "Fast Inverse Square Root: Bir Sihirli Sayıyla 3B Grafikleri Hızlandırmak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - kayan nokta
  - grafik programlama
toc: true
---

1990'ların oyun motorlarında her işlemci döngüsü değerliydi. Bir vektörü normalize etmek için gereken $1/\sqrt{x}$ hesabı bile performansı ciddi biçimde etkileyebiliyordu. Fast Inverse Square Root algoritması, kayan noktalı sayının bitlerini bir tamsayı gibi yorumlayıp yaklaşık sonucu şaşırtıcı derecede hızlı üretmesiyle ünlendi. Üstelik bunu yalnızca matematikle değil, sayıların bellekteki temsilini yaratıcı biçimde manipüle ederek yapıyordu.
``

## Neden ters karekök gerekiyor?

Üç boyutlu grafiklerde yön, yüzey normali ve ışık vektörleri çoğunlukla birim uzunluğa getirilir. $\vec{v}=(x,y,z)$ vektörünün uzunluğu

$$
\\vert \vec{v}\\vert =\sqrt{x^2+y^2+z^2}
$$

şeklindedir. Normalize edilmiş vektör ise

$$
\hat{v}=\vec{v}\cdot\frac{1}{\sqrt{x^2+y^2+z^2}}
$$

olarak hesaplanır. Eski işlemcilerde karekök ve bölme pahalı olduğundan, milyonlarca normal için bu işlemleri yapmak ekran kartının ve CPU'nun sabrını sınardı. Algoritmanın hedefi, $x^{-1/2}$ değerini doğrudan ve yaklaşık biçimde bulmaktır.

## IEEE 754 temsilindeki açık kapı

32 bitlik bir `float`; işaret, üs ve mantis alanlarından oluşur.

| Alan | Bit sayısı | Görevi |
|---|---:|---|
| İşaret | 1 | Sayının pozitif veya negatif olması |
| Üs | 8 | Sayının yaklaşık büyüklüğü |
| Mantis | 23 | Sayının hassasiyeti |

Pozitif ve normal bir kayan noktalı sayı kabaca $x=2^e\cdot m$ biçiminde düşünülebilir. Logaritma alınırsa çarpma ve üs alma işlemleri doğrusal ilişkilere dönüşür:

$$
\log_2(x^{-1/2})=-\frac{1}{2}\log_2(x)
$$

Float'ın bit deseni bir tamsayı olarak yorumlandığında, bu desen $\log_2(x)$ ile yaklaşık doğrusal davranır. Dolayısıyla bit desenini ikiye bölmek, logaritmayı yaklaşık yarıya indirmek gibidir. Ünlü `0x5f3759df` sabitinden bu yarım değer çıkarıldığında, ters karekök için oldukça iyi bir ilk tahmin elde edilir.

## Newton yöntemiyle tahmini parlatmak

Bit hilesi tek başına kusursuz değildir. Sonuç, Newton–Raphson yöntemiyle düzeltilir. $y=1/\sqrt{x}$ ilişkisi için kullanılan yineleme şöyledir:

$$
y_{n+1}=y_n\left(\frac{3}{2}-\frac{x}{2}y_n^2\right)
$$

Bir yineleme çoğu grafik hesabı için yeterli doğruluk sağlar. İkinci yineleme hatayı daha da azaltır; ancak hız avantajının bir kısmını tüketir.

| Yaklaşım | Hız | Doğruluk | Taşınabilirlik |
|---|---|---|---|
| `1.0f / sqrtf(x)` | Modern donanımda iyi | Yüksek | Yüksek |
| Bit hilesi | Eski işlemcilerde çok hızlı | Yaklaşık | Dikkat gerektirir |
| Donanım `rsqrt` komutu | Çok hızlı | Donanıma bağlı | Mimariye bağlı |

## Daha güvenli bir C uygulaması

Klasik Quake III kodu pointer tür dönüşümü kullanıyordu. Bu yaklaşım modern C kurallarında tanımsız davranış doğurabilir. `memcpy` ile aynı fikir daha güvenli uygulanabilir:

```c
#include <stdint.h>
#include <string.h>

float fast_inverse_sqrt(float x) {
    const float half_x = 0.5f * x;
    float y = x;
    uint32_t bits;

    // Float bitlerini tür ihlali yapmadan kopyala.
    memcpy(&bits, &y, sizeof(bits));
    bits = 0x5f3759dfu - (bits >> 1);
    memcpy(&y, &bits, sizeof(y));

    // İlk Newton-Raphson düzeltmesi.
    y = y * (1.5f - half_x * y * y);
    return y;
}
```

Fonksiyonun yalnızca pozitif ve sonlu girdiler için tasarlandığı unutulmamalıdır. Sıfır, negatif sayılar, sonsuzluk ve `NaN` değerleri ayrıca ele alınmalıdır.

## Bugün hâlâ kullanmalı mıyız?

Modern CPU ve GPU'lar karekök, SIMD ve yaklaşık ters karekök komutları sunar. Derleyiciler de optimizasyon konusunda 1999'daki atalarından çok daha yeteneklidir. Bu nedenle sihirli sabit günümüzde otomatik olarak en hızlı seçenek değildir; ölçüm yapmadan kullanmak nostaljik ama riskli olabilir.

Yine de algoritma, veri temsilini anlamanın neden önemli olduğunu gösteren eşsiz bir örnektir. Fast Inverse Square Root yalnızca bir performans numarası değil; logaritmaların, IEEE 754 bit düzeninin ve sayısal yöntemlerin aynı kazanda kaynatıldığı gerçek bir programlama efsanesidir.
