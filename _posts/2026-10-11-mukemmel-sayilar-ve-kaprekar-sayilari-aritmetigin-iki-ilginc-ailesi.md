---
layout: post
title: "Mükemmel Sayılar ve Kaprekar Sayıları: Aritmetiğin İki İlginç Ailesi"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - python
  - sayılar teorisi
  - algoritma
  - kaprekar sayıları
  - mükemmel sayılar
toc: true
image: /img/mukemmel-sayilar-ve-44.png
---

Bazı sayılar yalnızca miktar belirtmekle yetinmez; bölenleriyle veya kareleriyle şaşırtıcı ilişkiler kurar. Mükemmel sayılar, kendileri hariç pozitif bölenlerinin toplamına eşit olurken Kaprekar sayıları, kareleri uygun biçimde parçalandığında yeniden kendilerini üretir. Gelin bu iki sayı ailesinin kurallarını, örneklerini ve Python ile nasıl bulunabileceklerini inceleyelim.
``
## Mükemmel sayı nedir?

Bir $n$ pozitif tam sayısının kendisi dışındaki pozitif bölenlerine **öz bölenler** denir. Bu bölenlerin toplamı yeniden $n$ ediyorsa sayı mükemmeldir:

$$
n = \sum_{d \mid n,\ d<n} d
$$

En bilinen örnek $6$ sayısıdır. Öz bölenleri $1$, $2$ ve $3$ olduğundan:

$$1+2+3=6$$

Benzer şekilde $28$ sayısının öz bölenleri $1,2,4,7,14$ biçimindedir ve toplamları $28$ eder. Sayının bölen toplamı kendisinden küçükse **eksik**, büyükse **aşkın** sayı olarak adlandırılır.

| Sayı | Öz bölenleri | Toplam | Sınıf |
|---:|---|---:|---|
| 8 | 1, 2, 4 | 7 | Eksik |
| 12 | 1, 2, 3, 4, 6 | 16 | Aşkın |
| 28 | 1, 2, 4, 7, 14 | 28 | Mükemmel |

Çift mükemmel sayıların üretiminde Öklid–Euler teoremi kullanılır. Eğer $2^p-1$ asal ise aşağıdaki sayı mükemmeldir:

$$
N=2^{p-1}(2^p-1)
$$

Örneğin $p=3$ için $2^3-1=7$ asaldır ve $2^2\cdot7=28$ elde edilir. $2^p-1$ biçimindeki asallara **Mersenne asalları** denir. İlginç bir bilgi: Bugüne kadar herhangi bir tek mükemmel sayı bulunamamıştır; böyle bir sayının var olup olmadığı hâlâ açık bir problemdir.

## Kaprekar sayısı nedir?

Kaprekar sayılarında sahneye bölenler değil, sayının karesi çıkar. $n$ sayısı $k$ basamaklı olsun. $n^2$, sağdan $k$ basamak ayrılarak iki parçaya bölünür. Soldaki ve sağdaki parçaların toplamı $n$ ise sayı Kaprekar sayısıdır. Sağ parçada baştaki sıfırlara izin verilir ancak bu parçanın sıfır olmaması beklenir.

Örneğin $45$ iki basamaklıdır:

$$45^2=2025 \Rightarrow 20+25=45$$

$297$ için ise üç basamak ayrılır:

$$297^2=88209 \Rightarrow 88+209=297$$

| Sayı | Karesi | Parçalama | Sonuç |
|---:|---:|---|---:|
| 9 | 81 | 8 + 1 | 9 |
| 55 | 3025 | 30 + 25 | 55 |
| 99 | 9801 | 98 + 01 | 99 |
| 100 | 10000 | 10 + 000 | 10 |

Bu tabloda $100$ koşulu sağlayamaz. Ayrıca bazı kaynakların farklı parçalama tanımları kullandığını unutmamak gerekir; burada standart basamak sayısı yaklaşımını kullanıyoruz.

## Python ile sayıları avlamak

Aşağıdaki program iki özelliği ayrı fonksiyonlarla test eder. Mükemmel sayı kontrolünde tüm sayıları denemek yerine bölen çiftlerinden yararlanarak yalnızca $\sqrt{n}$ değerine kadar ilerler. Bu yaklaşım yaklaşık $O(\sqrt{n})$ zaman karmaşıklığına sahiptir.

```python
from math import isqrt

def is_perfect(n):
    if n < 2:
        return False

    divisor_sum = 1
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            divisor_sum += d
            pair = n // d
            if pair != d:
                divisor_sum += pair

    return divisor_sum == n


def is_kaprekar(n):
    if n < 1:
        return False

    digits = len(str(n))
    power = 10 ** digits
    square = n * n
    left, right = divmod(square, power)
    return right > 0 and left + right == n


perfect_numbers = [n for n in range(1, 10000) if is_perfect(n)]
kaprekar_numbers = [n for n in range(1, 1000) if is_kaprekar(n)]

print(perfect_numbers)
print(kaprekar_numbers)
```

`divmod`, kareyi $10^k$ ile bölerek sol bölüm ile sağ kalanı tek adımda üretir. Program ilk listede $6, 28, 496, 8128$ değerlerini bulacaktır. Kaprekar listesinde ise $1, 9, 45, 55, 99, 297$ gibi örnekler görülebilir.

Mükemmel sayılar bölen yapısındaki dengeyi, Kaprekar sayıları ise basamaklarla cebir arasındaki eğlenceli uyumu gösterir. İkisi de basit kurallardan doğmasına rağmen sayı teorisinin keşif, algoritma ve hâlâ çözülememiş sorularla dolu olduğunu kanıtlar.

![mukemmel-sayilar-ve-44](/img/mukemmel-sayilar-ve-44.svg)

