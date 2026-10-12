---
layout: post
title: "Sürekli Kesirlerle Rasyonel Sayı Gösterimi ve En İyi Yaklaşımlar"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - sürekli kesirler
  - rasyonel sayılar
  - python
  - algoritma
  - sayı teorisi
toc: true
image: /img/surekli-kesirlerle-rasyonel-28.png
---

Bir ondalık sayıyı kesre dönüştürmek bazen basit, bazen de şaşırtıcı derecede zordur. Örneğin $0{,}5=1/2$ hemen görülürken, $3{,}1415926$ için hangi kesrin “iyi” olduğu pek açık değildir. Sürekli kesirler, bir sayıyı iç içe geçmiş tam sayıların yardımıyla temsil eder ve küçük paydalı, son derece başarılı yaklaşık kesirleri sistematik biçimde üretir.
``
Sürekli kesir açılımı genel olarak şu biçimdedir:

$$
x=a_0+\cfrac{1}{a_1+\cfrac{1}{a_2+\cfrac{1}{a_3+\ddots}}}
$$

Bu gösterim kısaca $[a_0;a_1,a_2,a_3,\ldots]$ şeklinde yazılır. Burada $a_0$ bir tam sayı, sonraki $a_i$ değerleri ise pozitif tam sayılardır. İşlemin temel fikri basittir: Sayının tam kısmını ayır, kalan kesirli kısmın tersini al ve aynı adımları tekrarla.

Örneğin $43/19$ sayısını inceleyelim. Öklid algoritmasına benzeyen bölmeler yaparız:

$$
43=2\cdot19+5
$$

$$
19=3\cdot5+4,\qquad 5=1\cdot4+1,\qquad 4=4\cdot1
$$

Bölümlerdeki sayılar bize doğrudan açılımı verir:

$$
\frac{43}{19}=[2;3,1,4]
$$

Rasyonel sayıların sürekli kesir açılımı her zaman sonludur. İrrasyonel sayılarda ise süreç sonsuza kadar devam eder. Özellikle ikinci dereceden irrasyonel sayıların açılımları periyodiktir; meşhur altın oran bunun en zarif örneklerinden biridir:

$$
\varphi=\frac{1+\sqrt5}{2}=[1;1,1,1,\ldots]
$$

## Yakınsaklar nasıl üretilir?

Açılımı belirli bir noktada keserek elde ettiğimiz kesirlere **yakınsak** denir. $[a_0;a_1,\ldots,a_n]$ yakınsağının pay ve paydası şu bağıntılarla hesaplanabilir:

$$
p_n=a_np_{n-1}+p_{n-2},\qquad q_n=a_nq_{n-1}+q_{n-2}
$$

Başlangıç değerleri $p_{-2}=0$, $p_{-1}=1$, $q_{-2}=1$ ve $q_{-1}=0$ olarak alınır. Bu formüller, iç içe kesri her seferinde baştan çözmek yerine sonuçları adım adım oluşturmamızı sağlar.

$\pi=[3;7,15,1,292,\ldots]$ için ilk yakınsaklar şöyledir:

| Yakınsak | Ondalık değer | $\pi$ ile farkı | Yorum |
|---|---:|---:|---|
| $3/1$ | 3,000000 | 0,141593 | Çok kaba |
| $22/7$ | 3,142857 | 0,001264 | Küçük payda, iyi sonuç |
| $333/106$ | 3,141509 | 0,000083 | Daha hassas |
| $355/113$ | 3,141593 | Yaklaşık $2{,}67\times10^{-7}$ | Olağanüstü yaklaşım |

![surekli-kesirlerle-rasyonel-28](/img/surekli-kesirlerle-rasyonel-28.svg)


Buradaki sihir, yakınsakların yalnızca rastgele tahminler olmamasıdır. Bir yakınsak $p_n/q_n$, benzer büyüklükte paydaya sahip kesirler arasında çoğunlukla mümkün olan en iyi yaklaşımlardan biridir. Hata için de güçlü bir sınır vardır:

$$
\left\vert x-\frac{p_n}{q_n}\right\vert <\frac{1}{q_nq_{n+1}}<\frac{1}{q_n^2}
$$

Payda büyüdükçe hatanın karesel hızla küçülebilmesi, yöntemi sayısal hesaplamalarda değerli kılar.

## Python ile açılım ve yakınsak üretmek

Aşağıdaki kod, kayan noktalı bir sayının sınırlı uzunlukta sürekli kesir açılımını çıkarır; ardından her adımda oluşan yaklaşık kesri gösterir:

```python
from fractions import Fraction
from math import floor

def continued_fraction(x, steps=10):
    terms = []
    for _ in range(steps):
        a = floor(x)
        terms.append(a)
        remainder = x - a
        if abs(remainder) < 1e-15:
            break
        x = 1 / remainder
    return terms

def convergents(terms):
    p_old, p = 0, 1
    q_old, q = 1, 0

    for a in terms:
        p_old, p = p, a * p + p_old
        q_old, q = q, a * q + q_old
        yield Fraction(p, q)

terms = continued_fraction(3.141592653589793, 5)
print(terms)
print(list(convergents(terms)))
```

Kod yaklaşık olarak `[3, 7, 15, 1, 292]` ve buna karşılık gelen $3$, $22/7$, $333/106$, $355/113$ yakınsaklarını üretir. Ancak kayan nokta yuvarlama hataları uzun açılımlarda sonucu bozabilir; kesin rasyonel girdiler için `Fraction` ile pay ve payda üzerinden ilerlemek daha güvenlidir.

Sürekli kesirler; ölçüm değerlerini sade oranlarla ifade etme, müzik aralıklarını karşılaştırma, dişli oranı tasarlama ve irrasyonel sayılara yaklaşma gibi alanlarda kullanılır. Kısacası yöntem, “Bu sayıya en yakın basit kesir hangisi?” sorusunu deneme-yanılmadan çıkarıp güçlü bir algoritmaya dönüştürür.
