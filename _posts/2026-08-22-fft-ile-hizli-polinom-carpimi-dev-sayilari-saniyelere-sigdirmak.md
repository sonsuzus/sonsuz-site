---
layout: post
title: "FFT ile Hızlı Polinom Çarpımı: Dev Sayıları Saniyelere Sığdırmak"
math: true
categories: 
  - Bilgi
tags: 
  - FFT
  - Polinom Çarpımı
  - Algoritmalar
---

İki uzun polinomu klasik yöntemle çarpmak, her katsayının diğer tüm katsayılarla buluştuğu pahalı bir danstır. Derecesi milyonlara yaklaşan polinomlarda veya binlerce basamaklı tamsayılarda bu dans hızla kabusa dönüşür. Hızlı Fourier Dönüşümü (FFT), çarpma işlemini farklı bir uzaya taşıyarak problemi akıllıca küçültür: çarpmak yerine değerlendirir, noktasal çarpar ve geri dönüştürür.

``

## Neden klasik çarpım yavaş kalır?

İki polinomumuz olsun:

$$A(x)=\sum_{i=0}^{n-1}a_i x^i, \qquad B(x)=\sum_{j=0}^{m-1}b_j x^j$$

Çarpımın $k$. katsayısı evrişim (convolution) ile bulunur:

$$c_k=\sum_{i=0}^{k} a_i b_{k-i}$$

Bu formül basit görünür; ancak her katsayı için çok sayıda çarpım gerekir. Boyutlar benzerken klasik yaklaşımın maliyeti $O(n^2)$ olur. FFT tabanlı yaklaşım ise işlemi $O(n\log n)$ seviyesine indirir. Aradaki fark, veri büyüdükçe roket ile bisiklet arasındaki fark kadar dramatiktir.

| Yaklaşım | Temel fikir | Zaman karmaşıklığı | En uygun kullanım |
|---|---|---:|---|
| Klasik çarpım | Her katsayı çiftini çarp | $O(n^2)$ | Küçük diziler, basit kod |
| Karatsuba | Çarpımları böl-parçala ile azalt | Yaklaşık $O(n^{1.585})$ | Orta büyüklükte sayılar |
| FFT | Değerlendir, noktasal çarp, ters dönüştür | $O(n\log n)$ | Büyük polinomlar ve dev tamsayılar |

## Dönüşümün arkasındaki fikir

Bir polinom, katsayı listesiyle tanımlanabildiği gibi yeterli sayıda noktadaki değerleriyle de tanımlanabilir. FFT, polinomu özel karmaşık sayılarda, yani birliğin köklerinde değerlendirmenin hızlı yoludur. $N$ bir ikinin kuvveti olmak üzere kökler şudur:

$$\omega_N=e^{2\pi i/N}$$

Önce katsayıları en az $n+m-1$ uzunluğa kadar sıfırlarla doldururuz. Ardından $A$ ve $B$ için FFT uygularız. Elde edilen değerleri aynı indekslerde çarparız ve ters FFT (IFFT) ile katsayılara döneriz:

$$C=\operatorname{IFFT}(\operatorname{FFT}(A)\odot\operatorname{FFT}(B))$$

Buradaki $\odot$, eleman bazlı çarpımdır. FFT'nin hız sırrı, çift ve tek indeksli terimleri ayırmasıdır. Böylece $N$ noktalı dönüşüm, iki adet $N/2$ noktalı dönüşüme bölünür. Bu özyinelemeli yapı toplam maliyeti logaritmik katmanlara dağıtır.

## Python ile pratik uygulama

Aşağıdaki örnek, `numpy` kullanarak iki katsayı dizisini çarpar. Gerçek sayılı FFT kullandığımız için sonuçta oluşabilecek çok küçük kayan nokta hatalarını `round` ile temizliyoruz.

```python
import numpy as np

def hizli_polinom_carp(a, b):
    # Sonucun en az bu kadar katsayısı vardır.
    sonuc_uzunlugu = len(a) + len(b) - 1

    # FFT için uygun, ikinin kuvveti bir tampon boyutu seçilir.
    n = 1
    while n < sonuc_uzunlugu:
        n *= 2

    fa = np.fft.rfft(a, n)
    fb = np.fft.rfft(b, n)
    katsayilar = np.fft.irfft(fa * fb, n)

    return np.rint(katsayilar[:sonuc_uzunlugu]).astype(int).tolist()

print(hizli_polinom_carp([1, 2, 3], [4, 5]))
# [4, 13, 22, 15]
```

Örnekte ilk polinom $1+2x+3x^2$, ikincisi ise $4+5x$'tir. Sonuç $4+13x+22x^2+15x^3$ olarak gelir. `rfft`, giriş verisi gerçek sayılardan oluştuğunda simetrik karmaşık bileşenleri gereksiz hesaplamadan sakladığı için bellek ve süre avantajı sağlar.

## Büyük tamsayılarla bağlantısı

Dev bir tamsayıyı taban $10^k$ basamaklarından oluşan bir polinom gibi düşünebilirsiniz. Örneğin basamak blokları katsayı, taban ise $x$ olur. FFT ile katsayıları çarptıktan sonra elde taşımalarını normalleştirmek yeterlidir. Ancak kayan nokta FFT'sinde çok büyük girdiler yuvarlama hatası üretebilir. Kesin sonuç gerektiren kriptografik veya cebirsel uygulamalarda, modüler aritmetik kullanan NTT (Number Theoretic Transform) daha güvenli bir alternatiftir.

FFT, yalnızca hızlı bir numara değil; doğru temsili seçmenin performansı nasıl dönüştürdüğünün güçlü bir örneğidir. Problemi katsayı uzayından değer uzayına taşıdığınızda, zor evrişim sıradan bir noktasal çarpıma dönüşür.
