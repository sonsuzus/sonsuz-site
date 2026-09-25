---
layout: post
title: "FFT ile Dev Sayıları O(N log N) Sürede Çarpmak"
math: true
categories: 
  - Bilgi
tags: 
  - fft
  - algoritma
  - matematik
  - python
  - büyük sayılar
  - polinomlar
toc: true
image: /img/fft-ile-dev-80.png
---

İlkokulda öğrendiğimiz uzun çarpma yöntemi küçük sayılarda harikadır; ancak milyonlarca basamak söz konusu olduğunda işler dramatik biçimde yavaşlar. Neyse ki sinyal işlemenin yıldızı Hızlı Fourier Dönüşümü, yani FFT, basamakları birer polinom katsayısı gibi ele alarak çarpma işlemini yaklaşık $O(N \log N)$ sürede gerçekleştirebilir.

``

## Uzun çarpma neden yavaş?

İki sayının da $N$ basamaklı olduğunu düşünelim. Geleneksel yöntemde birinci sayının her basamağı, ikinci sayının her basamağıyla çarpılır. Dolayısıyla yaklaşık $N^2$ işlem gerekir:

$$T(N)=O(N^2)$$

Basamak sayısı iki katına çıktığında çalışma miktarı yaklaşık dört katına çıkar. FFT tabanlı yaklaşımda ise büyüme çok daha sakindir:

$$T(N)=O(N\log N)$$

| Yöntem | Zaman karmaşıklığı | Temel fikir |
|---|---:|---|
| Uzun çarpma | $O(N^2)$ | Tüm basamak çiftlerini çarp |
| Karatsuba | $O(N^{1.585})$ | Çarpımları parçalayarak azalt |
| FFT | $O(N\log N)$ | Konvolüsyonu frekans uzayında hesapla |

## Sayıları polinoma dönüştürmek

Örneğin $1234$ sayısını şu polinomla temsil edebiliriz:

$$A(x)=4+3x+2x^2+x^3$$

Burada $x=10$ seçildiğinde yeniden 1234 elde edilir. İki sayıyı çarpmak, bunlara karşılık gelen polinomları çarpmaya eşdeğerdir. Polinom çarpımındaki katsayılar ise ayrık konvolüsyonla bulunur:

$$c_k=\sum_{i=0}^{k}a_i b_{k-i}$$

Bu formül doğrudan uygulanırsa yine $O(N^2)$ zaman harcar. FFT’nin sihri, konvolüsyonu noktasal çarpıma dönüştürmesidir:

$$\operatorname{FFT}(a*b)=\operatorname{FFT}(a)\cdot\operatorname{FFT}(b)$$

Yani önce katsayıları frekans uzayına taşır, karşılık gelen değerleri tek tek çarpar ve ters FFT ile geri döneriz.

## Birim kökler ve böl-parçala-yönet

Ayrık Fourier Dönüşümü şu şekilde tanımlanır:

$$X_k=\sum_{j=0}^{N-1}x_j e^{-2\pi i jk/N}$$

Üstel ifadeler, karmaşık düzlemde eşit aralıklarla yerleşmiş $N$’inci birim köklerdir. FFT, çift ve tek indeksli katsayıları ayırarak aynı hesaplamaları tekrar yapmaktan kurtulur. Her seviyede toplam $O(N)$ iş yapılır ve yaklaşık $\log_2N$ seviye bulunur.

| Alan | İşlem | Maliyet |
|---|---|---:|
| Katsayı uzayı | Konvolüsyon | $O(N^2)$ |
| Frekans uzayı | Noktasal çarpım | $O(N)$ |
| FFT ve ters FFT | Dönüşüm | $O(N\log N)$ |

## Python ile sade bir uygulama

Aşağıdaki örnek, sayıları onluk basamaklarına ayırır. NumPy FFT hesaplamasını yapar; son döngü ise yuvarlama ve elde taşıma işlemlerini düzeltir.

```python
import numpy as np

def fft_multiply(x: str, y: str) -> str:
    a = np.array([int(d) for d in x[::-1]], dtype=float)
    b = np.array([int(d) for d in y[::-1]], dtype=float)

    size = 1
    while size < len(a) + len(b):
        size *= 2

    fa = np.fft.fft(a, size)
    fb = np.fft.fft(b, size)
    coefficients = np.rint(np.fft.ifft(fa * fb).real).astype(np.int64)

    carry = 0
    digits = []
    for value in coefficients:
        total = int(value) + carry
        digits.append(total % 10)
        carry = total // 10

    while carry:
        digits.append(carry % 10)
        carry //= 10

    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()

    return ''.join(map(str, digits[::-1]))

print(fft_multiply("123456789012345", "987654321098765"))
```

Bu uygulama öğreticidir; kayan nokta hataları nedeniyle gerçekten milyonlarca basamakta güvenilir olmayabilir. Pratik sistemler basamakları daha büyük bloklara ayırır veya modüler aritmetik kullanan Sayı Teorik Dönüşümü’nü (NTT) tercih eder. Birden fazla asal modülle yapılan sonuçlar Çin Kalan Teoremi aracılığıyla birleştirilebilir.

Sonuçta FFT yalnızca ses ve görüntü analizi yapan bir araç değildir. Büyük sayı çarpımını polinom çarpımına, polinom çarpımını konvolüsyona ve konvolüsyonu ucuz noktasal çarpımlara dönüştüren güçlü bir algoritmik köprüdür.

![fft-ile-dev-80](/img/fft-ile-dev-80.svg)

