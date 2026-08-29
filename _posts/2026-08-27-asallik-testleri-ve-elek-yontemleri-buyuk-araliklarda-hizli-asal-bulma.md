---
layout: post
title: "Asallık Testleri ve Elek Yöntemleri: Büyük Aralıklarda Hızlı Asal Bulma"
math: true
categories: 
  - Bilgi
tags: 
  - asal sayılar
  - eratosthenes eleği
  - algoritmalar
  - python
  - segmentli elek
toc: true
---

Asal sayılar, yalnızca 1’e ve kendilerine bölünebilen 1’den büyük tam sayılardır; fakat bu kısa tanım, büyük veri aralıklarında hesaplama yaparken ciddi bir algoritma problemine dönüşür. Tek tek sayıları denemek küçük örneklerde işe yarasa da, örneğin $10^{12}$ civarındaki milyonlarca sayıyı taramak istediğimizde akıllı eleme stratejilerine ihtiyaç duyarız. Bu noktada Eratosthenes Eleği ve onun büyük aralıklara uyarlanmış hâli olan segmentli elek devreye girer.

``

## Asallık testi neden tek başına yeterli değildir?

Bir $n$ sayısının asal olup olmadığını anlamanın temel yolu, onu olası bölenlere bölmektir. Ancak tüm sayılara bölmeye gerek yoktur: Eğer $n = a \cdot b$ ise çarpanlardan en az biri $\sqrt{n}$ değerinden küçük veya eşittir. Bu nedenle deneme bölmesi yaklaşımı en fazla $\sqrt{n}$ değerine kadar ilerler.

$$
\text{Bir sayı için maliyet} \approx O(\sqrt{n})
$$

Bu yöntem tek bir büyük sayı için makuldür. Fakat $[L, R]$ aralığındaki her sayıyı ayrı ayrı test edersek maliyet kabaca $O((R-L+1)\sqrt{R})$ olur. Aralık büyüdükçe bilgisayarınız asal aramak yerine fan sesi üretmeye başlayabilir.

| Yaklaşım | En uygun kullanım | Yaklaşık maliyet | Temel sorun |
|---|---|---:|---|
| Deneme bölmesi | Tek sayı testi | $O(\sqrt{n})$ | Çok sayıda adayda yavaştır |
| Eratosthenes Eleği | $2$ ile $N$ arası | $O(N\log\log N)$ | Çok büyük $N$ için bellek ister |
| Segmentli elek | Büyük bir $[L,R]$ aralığı | $O((R-L+1)\log\log R)$ | Başlangıç asallarını üretmek gerekir |

## Eratosthenes Eleği: Çarpanları sistematik biçimde silmek

Eratosthenes Eleği’nin fikri basittir: Önce tüm sayıları potansiyel asal kabul ederiz. Ardından 2’den başlayarak her asalın katlarını eleriz. Örneğin 2’nin katları, sonra 3’ün katları silinir. Bir sayının ilk kez silinmesi, onun en küçük asal çarpanıyla karşılaşması demektir.

Önemli optimizasyon şudur: Bir $p$ asalı için eleme işlemine $p^2$ değerinden başlanır. Çünkü $p$ ile $p^2$ arasındaki $p$ katları daha önce daha küçük asal çarpanlar tarafından zaten işaretlenmiştir.

```python
def eratosthenes(n: int) -> list[int]:
    is_prime = [True] * (n + 1)
    is_prime[0:2] = [False, False]

    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    return [i for i, prime in enumerate(is_prime) if prime]
```

Bu kod, $N$ sınırına kadar tüm asalları üretir. `is_prime` dizisi her sayı için bir durum sakladığından bellek maliyeti $O(N)$’dir. İşte $N$ çok büyük olduğunda segmentli yaklaşımın sahneye çıkma zamanı gelir.

## Segmentli elek ile dev aralıkları taramak

Segmentli elekte tüm $[2,R]$ aralığını belleğe almak yerine yalnızca hedef $[L,R]$ parçasını tutarız. Önce $\sqrt{R}$ değerine kadar olan asal sayıları klasik elekle üretiriz. Ardından bu asalların hedef aralıktaki katlarını işaretleriz.

Bir $p$ asalı için aralıktaki ilk silinecek kat şudur:

$$
\max(p^2, \lceil L/p \rceil \cdot p)
$$

```python
from math import isqrt

def segmented_sieve(left: int, right: int) -> list[int]:
    base_primes = eratosthenes(isqrt(right))
    segment = [True] * (right - left + 1)

    for p in base_primes:
        start = max(p * p, ((left + p - 1) // p) * p)
        for value in range(start, right + 1, p):
            segment[value - left] = False

    if left == 1:
        segment[0] = False

    return [left + i for i, prime in enumerate(segment) if prime]
```

Burada `value - left` ifadesi, gerçek sayı değerini segment dizisindeki indekse çevirir. Ayrıca 1’in asal olmadığını özellikle elemek gerekir. Bu teknik, örneğin $[10^{12}, 10^{12}+10^6]$ gibi aralıklarda son derece kullanışlıdır: Bellek tüketimi $R$ yerine aralık genişliğine, yani $O(R-L+1)$ seviyesine iner.

Pratikte çok geniş aralıkları daha küçük bloklara bölmek, `bytearray` kullanmak ve yalnızca tek sayıları işlemek performansı artırır. Özetle: Tek bir sayıyı sınarken $\sqrt{n}$ mantığı yeterli olabilir; ama çok sayıda asal ararken kazanan strateji, adayları tek tek sorgulamak değil, bileşikleri topluca elemek olur.
