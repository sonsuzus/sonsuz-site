---
layout: post
title: "Möbius Dönüşümü: Bölen Toplamlarını Tersine Çevirmenin Matematiksel Anahtarı"
math: true
categories: 
  - Bilgi
tags: 
  - sayı teorisi
  - möbius fonksiyonu
  - matematiksel algoritmalar
toc: true
---

Sayı teorisinde bazı fonksiyonlar kendilerini doğrudan göstermek yerine bölenleri üzerinden ipucu verir. Elimizde bir sayının tüm bölenlerine ait değerlerin toplamı bulunur; fakat asıl fonksiyonu keşfetmemiz gerekir. Möbius dönüşümü, tam da bu matematiksel bilmeceyi çözen güçlü bir tersine çevirme tekniğidir.
``

## Temel problem nedir?

İki aritmetik fonksiyon arasında

$$
g(n)=\sum_{d\mid n} f(d)
$$

ilişkisi bulunduğunu düşünelim. Buradaki $d\mid n$ gösterimi, $d$ sayısının $n$'yi böldüğünü ifade eder. Yani $g(n)$, $n$'nin bütün pozitif bölenleri için hesaplanan $f(d)$ değerlerinin toplamıdır.

Örneğin $n=6$ için:

$$
g(6)=f(1)+f(2)+f(3)+f(6)
$$

Peki yalnızca $g$ biliniyorsa $f$ nasıl bulunur? Cevap Möbius tersine çevirme formülüdür:

$$
f(n)=\sum_{d\mid n}\mu(d)g\left(\frac{n}{d}\right)
$$

Buradaki $\mu$, Möbius fonksiyonudur ve adeta gereksiz bölen katkılarını artı ve eksi işaretlerle temizleyen matematiksel bir filtre gibi çalışır.

## Möbius fonksiyonu

Bir pozitif tam sayının asal çarpanlarına ayrılması, $\mu(n)$ değerini belirler:

$$
\mu(n)=
\begin{cases}
1, & n=1\\
0, & n \text{ bir asalın karesine bölünüyorsa}\\
(-1)^k, & n \text{ farklı } k \text{ asalın çarpımıysa}
\end{cases}
$$

| Sayı | Asal çarpan yapısı | $\mu(n)$ |
|---:|---|---:|
| 1 | Özel durum | 1 |
| 6 | $2\cdot3$ | 1 |
| 10 | $2\cdot5$ | 1 |
| 12 | $2^2\cdot3$ | 0 |
| 30 | $2\cdot3\cdot5$ | -1 |

Kare içeren sayılara sıfır verilmesi tesadüf değildir. Tersine çevirme sırasında yinelenen asal faktörlerden gelen katkılar böylece tamamen elenir.

## Dirichlet konvolüsyonu açısından

Möbius dönüşümü, Dirichlet konvolüsyonu adı verilen işlemle daha kısa anlatılabilir:

$$
(f*h)(n)=\sum_{d\mid n}f(d)h\left(\frac{n}{d}\right)
$$

Sabit $1(n)=1$ fonksiyonunu kullanırsak başlangıç ilişkisi $g=f*1$ olur. Möbius fonksiyonu, sabit bir fonksiyonunun konvolüsyon tersidir:

$$
\mu*1=\varepsilon
$$

Burada $\varepsilon(1)=1$, diğer pozitif tam sayılarda ise $0$ değerini alır. Dolayısıyla her iki tarafı $\mu$ ile konvolüsyona sokmak, $f$ fonksiyonunu yalnız bırakır.

| Yaklaşım | İfade | Amaç |
|---|---|---|
| İleri dönüşüm | $g(n)=\sum_{d\mid n}f(d)$ | Bölen katkılarını birleştirmek |
| Ters dönüşüm | $f(n)=\sum_{d\mid n}\mu(d)g(n/d)$ | Özgün değerleri geri kazanmak |
| Konvolüsyon | $g=f*1$ | İlişkiyi cebirsel göstermek |

## Klasik örnek: Euler phi fonksiyonu

Euler'in totient fonksiyonu $\varphi(n)$, $1$ ile $n$ arasında $n$ ile aralarında asal olan sayıların adedidir. Şu önemli özdeşlik geçerlidir:

$$
\sum_{d\mid n}\varphi(d)=n
$$

Burada $g(n)=n$ kabul edilip Möbius dönüşümü uygulanırsa:

$$
\varphi(n)=\sum_{d\mid n}\mu(d)\frac{n}{d}
=n\sum_{d\mid n}\frac{\mu(d)}{d}
$$

elde edilir. Böylece bir bölen toplamının içindeki $\varphi$ fonksiyonu başarıyla çekilip çıkarılır.

## Python ile hesaplama

Aşağıdaki kod, doğrusal eleğe benzer bir yöntemle $1$ ile $N$ arasındaki Möbius değerlerini hesaplar:

```python
def mobius_sieve(n):
    mu = [1] * (n + 1)
    is_prime = [True] * (n + 1)

    for p in range(2, n + 1):
        if is_prime[p]:
            for multiple in range(p, n + 1, p):
                is_prime[multiple] = False
                mu[multiple] *= -1

            square = p * p
            for multiple in range(square, n + 1, square):
                mu[multiple] = 0

    return mu

print(mobius_sieve(10)[1:])
```

İlk döngü her farklı asal çarpan için işareti değiştirir. İkinci döngü ise asal karelerine bölünen sayıların değerini sıfırlar. Yaklaşık $O(N\log\log N)$ ile $O(N\log N)$ arasında pratik bir çalışma maliyetine sahiptir.

Möbius dönüşümü; aralarında asal çiftleri sayma, bölünebilirlik kısıtlarını çözme, kombinatorik sayımlar ve hızlı bölen toplamı algoritmalarında sıkça kullanılır. Bir problemde “bütün bölenler üzerinden toplam” görülüyorsa, matematiksel alet çantasından Möbius anahtarını çıkarmanın zamanı gelmiş olabilir.
