---
layout: post
title: "Möbius İnversiyonu ile Sayılar Teorisinde Kapsama-Dışlama"
math: true
categories: 
  - Bilgi
tags: 
  - möbius inversiyonu
  - sayılar teorisi
  - kapsama-dışlama
  - aralarında asallık
  - bölen toplamları
  - algoritma
toc: true
image: /img/mobius-inversiyonu-ile-53.png
---

Bazı sayılar teorisi problemleri, bölenlerin ve ortak çarpanların iç içe geçmesi yüzünden çözülmez bir düğüm gibi görünür. Möbius inversiyonu ise bu düğümü tek tek açmak yerine matematiksel olarak tersine çevirir. Aralarında asal çiftleri saymaktan bölen toplamlarından özgün bir fonksiyonu geri kazanmaya kadar pek çok işlem, böylece zarif bir kapsama-dışlama hesabına dönüşür.

![mobius-inversiyonu-ile-53](/img/mobius-inversiyonu-ile-53.svg)

``
## Möbius fonksiyonu nedir?

Möbius fonksiyonu $\mu(n)$, pozitif tam sayıları üç gruba ayırır:

$$
\mu(n)=
\begin{cases}
1, & n=1,\\
0, & n \text{ bir asalın karesine bölünüyorsa},\\
(-1)^k, & n \text{ farklı } k \text{ asalın çarpımıysa}.
\end{cases}
$$

Örneğin $\mu(6)=1$ olur; çünkü $6=2\cdot3$ ve iki farklı asal çarpanı vardır. Buna karşılık $12$, $2^2$ ile bölündüğü için $\mu(12)=0$ değerini alır.

| $n$ | Asal çarpan yapısı | $\mu(n)$ |
|---:|---|---:|
| 1 | Boş çarpım | 1 |
| 6 | $2\cdot3$ | 1 |
| 30 | $2\cdot3\cdot5$ | -1 |
| 12 | $2^2\cdot3$ | 0 |

Fonksiyonun sihirli özelliği şudur:

$$
\sum_{d\mid n}\mu(d)=
\begin{cases}
1, & n=1,\\
0, & n>1.
\end{cases}
$$

Bu eşitlik, istenmeyen ortak bölenleri artı ve eksi işaretlerle yok eden kapsama-dışlama ilkesinin aritmetik karşılığıdır.

## Möbius inversiyon formülü

Bir $f$ fonksiyonunun bölenler üzerindeki toplamıyla $g$ fonksiyonu tanımlansın:

$$g(n)=\sum_{d\mid n}f(d).$$

Möbius inversiyonu, toplamın içine saklanmış $f$ değerini geri çıkarır:

$$f(n)=\sum_{d\mid n}\mu(d)g\left(\frac{n}{d}\right).$$

| İleri işlem | Ters işlem |
|---|---|
| Bölenlerden bilgi toplar | Toplanan bilgiyi ayrıştırır |
| $g(n)=\sum_{d\mid n}f(d)$ | $f(n)=\sum_{d\mid n}\mu(d)g(n/d)$ |
| Birikimli görünüm üretir | Özgün katkıları bulur |

Bunun klasik örneği Euler’in totient fonksiyonudur. $n$ sayısının pozitif bölenlerinin totient değerleri toplamı $n$ eder:

$$n=\sum_{d\mid n}\varphi(d).$$

İnversiyon uygulandığında doğrudan şu formül elde edilir:

$$\varphi(n)=\sum_{d\mid n}\mu(d)\frac{n}{d}.$$

## Aralarında asal çiftleri saymak

$1\leq a,b\leq N$ koşulunu sağlayan ve $\gcd(a,b)=1$ olan sıralı çiftleri sayalım. Bir çiftin her iki elemanı da $d$ ile bölünüyorsa yaklaşık değil, tam olarak $\lfloor N/d\rfloor^2$ seçenek vardır. Möbius fonksiyonu ortak bölenleri kapsama-dışlama ile temizler:

$$
C(N)=\sum_{d=1}^{N}\mu(d)\left\lfloor\frac{N}{d}\right\rfloor^2.
$$

Burada $\mu(d)=0$ olan kare çarpanlı değerler otomatik olarak elenir. Tek sayıda farklı asal içerenler çıkarılır, çift sayıda asal içerenler yeniden eklenir. Kısacası Möbius fonksiyonu, kapsama-dışlamanın muhasebecisidir; üstelik hesap makinesini hiç düşürmez!

## Python ile doğrusal elek

Aşağıdaki kod, $1$ ile $N$ arasındaki Möbius değerlerini doğrusal zamanda üretir ve aralarında asal sıralı çiftlerin sayısını hesaplar:

```python
def mobius_sieve(n):
    mu = [0] * (n + 1)
    mu[1] = 1
    primes, composite = [], [False] * (n + 1)

    for i in range(2, n + 1):
        if not composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            composite[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return mu


def coprime_pairs(n):
    mu = mobius_sieve(n)
    return sum(mu[d] * (n // d) ** 2 for d in range(1, n + 1))

print(coprime_pairs(10))  # 63
```

Elek her bileşik sayıyı kontrollü biçimde işler; böylece karmaşıklık $O(N)$, toplam hesabı da $O(N)$ olur. Büyük sınırlar için $\lfloor N/d\rfloor$ değerlerinin yalnızca yaklaşık $2\sqrt N$ farklı değer aldığından yararlanılarak gruplama yapılabilir.

Möbius inversiyonunu gördüğünüzde temel soruyu sorun: “Elimdeki fonksiyon, bölenler üzerinden birikmiş başka bir bilginin toplamı mı?” Yanıt evetse, tersine çevirme formülü büyük olasılıkla problemi birkaç satırlık temiz bir toplama indirecektir.
