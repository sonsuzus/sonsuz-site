---
layout: post
title: "Çinlilerin Kalan Teoremi: Parçalı Bilgiden Tek Bir Sayıya"
math: true
categories: 
  - Bilgi
tags: 
  - çinlilerin kalan teoremi
  - modüler aritmetik
  - sayı teorisi
  - matematik
  - python
  - algoritma
toc: true
image: /img/cinlilerin-kalan-teoremi-86.png
---

Bir sayıyı doğrudan bilmiyor, fakat farklı sayılara bölündüğünde bıraktığı kalanları biliyor olabilirsiniz. İlk bakışta bu bilgiler ayrı yapboz parçaları gibi görünür. Çinlilerin Kalan Teoremi, modüller uygun olduğunda bütün parçaları birleştirerek tek ve tutarlı bir çözüm üretir. Üstelik bu çözüm yalnızca teorik bir merak değildir; kriptografi, takvim hesapları, paralel işlem ve bilgisayar aritmetiğinde karşımıza çıkar.

``

## Temel fikir: Aynı sayı, farklı saatler

Modüler aritmetiği farklı büyüklüklerde çalışan saatlere benzetebiliriz. Örneğin

$$x \equiv 2 \pmod{3}$$

ifadesi, $x$ sayısının 3'e bölündüğünde 2 kalanını verdiğini söyler. Benzer biçimde şu sistemi ele alalım:

$$
x \equiv 2 \pmod{3}, \qquad
x \equiv 3 \pmod{5}, \qquad
x \equiv 2 \pmod{7}
$$

Burada aynı $x$, üç farklı modüler saatte belirli konumlara gelmektedir. Modüller olan 3, 5 ve 7 ikişer ikişer aralarında asaldır. Yani her farklı çift için $\gcd(m_i,m_j)=1$ koşulu sağlanır.

Çinlilerin Kalan Teoremi şunu garanti eder: Modüller ikişer ikişer aralarında asalsa sistemin, modüllerin çarpımına göre tek bir çözüm sınıfı vardır.

$$M=m_1m_2\cdots m_k$$

Başka bir deyişle çözüm $M$ aralığında benzersizdir; fakat tam sayılarda sonsuz kez tekrar eder.

| Kavram | Anlamı | Örnekteki değeri |
|---|---|---:|
| $a_i$ | İstenen kalan | 2, 3, 2 |
| $m_i$ | Modül | 3, 5, 7 |
| $M$ | Tüm modüllerin çarpımı | 105 |
| Çözüm sınıfı | Eşdeğer bütün sayılar | $23+105k$ |

## Çözüm nasıl inşa edilir?

Her denklem için toplam çarpımdan ilgili modülü çıkaran bir parça oluşturulur:

$$M_i=\frac{M}{m_i}$$

Ardından $M_i$ sayısının $m_i$ modülündeki çarpımsal tersi bulunur. Bu ters $y_i$ ile gösterilirse

$$M_i y_i \equiv 1 \pmod{m_i}$$

olmalıdır. Son çözüm şu formülle birleştirilir:

$$x \equiv \sum_{i=1}^{k} a_iM_iy_i \pmod{M}$$

Örneğimizde $M=105$ olur. Parçalar sırasıyla 35, 21 ve 15'tir. Bunların ilgili modüllerdeki tersleri 2, 1 ve 1 olarak bulunur. Dolayısıyla

$$x \equiv 2\cdot35\cdot2+3\cdot21\cdot1+2\cdot15\cdot1=233 \pmod{105}$$

elde edilir. $233$ sayısının 105'e göre kalanı 23 olduğundan en küçük pozitif çözüm $x=23$'tür. Gerçekten de 23; 3'e bölününce 2, 5'e bölününce 3 ve 7'ye bölününce 2 kalanını verir.

## Python ile genel çözüm

Aşağıdaki fonksiyon, modüllerin bağımsızlığını kontrol eder ve yapıcı formülü uygular. `pow(Mi, -1, mi)` ifadesi Python'da modüler tersi hesaplar.

```python
from math import gcd, prod

def crt(kalanlar, moduller):
    # Modüllerin ikişer ikişer aralarında asal olduğunu doğrula.
    for i in range(len(moduller)):
        for j in range(i + 1, len(moduller)):
            if gcd(moduller[i], moduller[j]) != 1:
                raise ValueError('Modüller aralarında asal değil')

    M = prod(moduller)
    toplam = 0

    for ai, mi in zip(kalanlar, moduller):
        Mi = M // mi
        ters = pow(Mi, -1, mi)
        toplam += ai * Mi * ters

    return toplam % M, M

cozum, periyot = crt([2, 3, 2], [3, 5, 7])
print(cozum, periyot)  # 23 105
```

Fonksiyon `(23, 105)` döndürür. Bu sonuç yalnızca 23'ü değil, $x=23+105k$ biçimindeki bütün çözümleri temsil eder.

## Modüller aralarında asal değilse

Teoremin klasik biçimi doğrudan uygulanamaz; ancak sistem mutlaka çözümsüz değildir. İki denklem için kalanların $\gcd(m_1,m_2)$ modülünde uyumlu olması gerekir. Örneğin $x\equiv1\pmod4$ ve $x\equiv3\pmod6$ sistemi uyumludur; fakat $x\equiv1\pmod4$ ve $x\equiv2\pmod6$ değildir. Kısacası CRT, farklı modüler dünyaların aynı sayıda buluşabilmesi için güçlü ve zarif bir köprü kurar.

![cinlilerin-kalan-teoremi-86](/img/cinlilerin-kalan-teoremi-86.svg)

