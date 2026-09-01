---
layout: post
title: "FFT ile Polinom ve Büyük Sayı Çarpımı: O(n log n) Hızına Yolculuk"
math: true
categories: 
  - Bilgi
tags: 
  - fft
  - algoritmalar
  - polinom çarpımı
toc: true
---

Binlerce basamaklı iki sayıyı klasik yöntemle çarpmak, her basamağı diğer sayının bütün basamaklarıyla eşleştirmeyi gerektirir. Bu yaklaşım küçük sayılarda sorunsuzdur; ancak veri büyüdükçe işlem sayısı hızla artar. Hızlı Fourier Dönüşümü, yani FFT, sayıları polinom gibi yorumlayarak çarpımı frekans uzayına taşır ve yaklaşık $O(n \log n)$ zamanda tamamlar. Kısacası FFT, devasa çarpma işlemini akıllıca organize edilmiş küçük işlemlere dönüştürür.

``

## Büyük sayı nasıl polinoma dönüşür?

Örneğin $1234$ sayısını basamaklarına ayıralım:

$$1234 = 4 + 3x + 2x^2 + x^3, \quad x=10$$

Benzer biçimde ikinci sayı da katsayıları basamaklardan oluşan bir polinom olarak yazılır. İki sayıyı çarpmak, bu polinomları çarpıp sonucu tekrar $x=10$ için değerlendirmekle aynıdır. Polinom çarpımında sonuç katsayıları şu evrişim formülüyle bulunur:

$$c_k = \sum_{i=0}^{k} a_i b_{k-i}$$

Doğrudan hesaplamada her katsayı, pek çok katsayıyla eşleştirilir. $n$ terimli iki polinom için bu yöntem $O(n^2)$ işlem gerektirir. FFT ise katsayı gösterimini, polinom değerlerinin belirli karmaşık noktalardaki gösterimine çevirir.

| Yöntem | Temel işlem | Karmaşıklık | Uygun kullanım |
|---|---|---:|---|
| Klasik çarpım | Tüm katsayı çiftlerini çarpar | $O(n^2)$ | Küçük girdiler |
| Karatsuba | Çarpımı üç alt probleme böler | Yaklaşık $O(n^{1.585})$ | Orta büyüklükte sayılar |
| FFT | Evrişimi noktasal çarpıma dönüştürür | $O(n \log n)$ | Çok büyük sayılar ve veri kümeleri |

## FFT neden hızlıdır?

FFT, Ayrık Fourier Dönüşümü'nü böl ve yönet yaklaşımıyla hesaplar. Kullanılan noktalar, $n$'inci birim kökleridir:

$$\omega_n = e^{2\pi i/n}$$

Polinomun çift ve tek dereceli katsayıları ayrılır. Böylece $n$ boyutlu problem, iki adet $n/2$ boyutlu probleme dönüşür. Bu bölünme $\log n$ seviye sürer ve her seviyede toplam $O(n)$ iş yapılır. Sonuç olarak:

$$T(n)=2T(n/2)+O(n)=O(n\log n)$$

Çarpım üç aşamada gerçekleşir: iki katsayı dizisine FFT uygulanır, karşılık gelen değerler noktasal olarak çarpılır ve ters FFT ile sonuç katsayılarına dönülür. Frekans uzayında evrişimin yalnızca noktasal çarpım olması, işin sihirli kısmıdır.

## Python ile örnek uygulama

Aşağıdaki kod, onluk basamakları katsayı kabul ederek iki pozitif tam sayıyı çarpar:

```python
import cmath
from math import pi

def fft(a, inverse=False):
    n = len(a)
    if n == 1:
        return a

    even = fft(a[0::2], inverse)
    odd = fft(a[1::2], inverse)
    sign = 1 if inverse else -1
    root = cmath.exp(sign * 2j * pi / n)
    w = 1
    result = [0] * n

    for i in range(n // 2):
        value = w * odd[i]
        result[i] = even[i] + value
        result[i + n // 2] = even[i] - value
        w *= root

    if inverse:
        result = [x / 2 for x in result]
    return result

def multiply(x, y):
    a = list(map(int, str(x)[::-1]))
    b = list(map(int, str(y)[::-1]))
    n = 1
    while n < len(a) + len(b):
        n *= 2

    a += [0] * (n - len(a))
    b += [0] * (n - len(b))
    fa, fb = fft(a), fft(b)
    values = fft([fa[i] * fb[i] for i in range(n)], True)
    digits = [round(v.real) for v in values]

    carry = 0
    for i in range(len(digits)):
        total = digits[i] + carry
        digits[i] = total % 10
        carry = total // 10
    while carry:
        digits.append(carry % 10)
        carry //= 10
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return int(''.join(map(str, digits[::-1])))
```

Kod önce dizi uzunluğunu ikinin kuvvetine tamamlar; çünkü FFT'nin bölünmesi böyle kolaylaşır. Ters dönüşümden sonra kayan nokta hataları `round` ile düzeltilir ve elde taşıma işlemi uygulanır.

Pratikte karmaşık sayılı FFT hassasiyet sorunları oluşturabilir. Çok büyük girdilerde daha geniş tabanlar, Number Theoretic Transform veya birden fazla modül kullanılabilir. Yine de temel fikir değişmez: pahalı evrişimi frekans uzayında ucuz noktasal çarpıma dönüştürmek.
