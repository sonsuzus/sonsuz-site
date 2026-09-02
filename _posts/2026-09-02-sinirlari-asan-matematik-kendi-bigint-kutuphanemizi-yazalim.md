---
layout: post
title: "Sınırları Aşan Matematik: Kendi BigInt Kütüphanemizi Yazalım"
math: true
categories: 
  - Proje
tags: 
  - bigınt
  - uzun sayı aritmetiği
  - algoritmalar
toc: true
---

Bir tam sayının milyonlarca basamağı olsaydı onu nasıl toplardınız? Standart veri türleri işlemcinin belirlediği sınırlar içinde yaşarken BigInt yaklaşımı, sayıları küçük parçalara ayırarak bu duvarı aşar. Bu projede veri kaybına uğramadan dev sayıları saklayan, toplayan ve çarpan küçük bir kütüphanenin temelini kuracağız.
``

## Standart tam sayılar neden yetmez?

Birçok dilde 64 bit işaretli tam sayıların aralığı şöyledir:

$$
-2^{63} \leq n \leq 2^{63}-1
$$

Bu sınır yaklaşık 19 ondalık basamağa karşılık gelir. Daha büyük bir değer taşmaya uğrayabilir veya dile bağlı olarak farklı bir türe dönüştürülebilir. Kayan noktalı sayılar geniş bir aralık sunsa da bütün basamakları kesin biçimde korumaz. Örneğin JavaScript'in klasik `Number` türünde güvenli tam sayı üst sınırı $2^{53}-1$ değeridir.

| Yaklaşım | Kapasite | Kesinlik | Temel maliyet |
|---|---:|---|---|
| 64 bit tamsayı | Sabit | Tam | Çok düşük |
| Kayan nokta | Çok geniş aralık | Büyük sayılarda kayıplı | Düşük |
| BigInt | Bellekle sınırlı | Tam | Basamak sayısıyla artar |

BigInt'in sırrı aslında şaşırtıcı derecede tanıdıktır: İlkokuldaki sütun işlemleri! Sayıyı tek parça yerine bir dizi içinde saklarız. Her hücre bir basamak taşıyabilir; fakat işlemciyi daha verimli kullanmak için tabanı 10 değil, örneğin $10^9$ seçebiliriz.

$$
N = a_0B^0+a_1B^1+\cdots+a_kB^k, \qquad B=10^9
$$

Burada $a_0$ en düşük anlamlı parçadır. Böylece `12345678901234567890` sayısı küçükten büyüğe `[234567890, 345678901, 12]` olarak tutulur.

## Python ile çekirdek sınıf

Python zaten sınırsız büyüklükte tamsayı destekler; onu burada algoritmayı rahatça göstermek için kullanıyoruz. Aşağıdaki eğitim sürümü negatif olmayan sayıları destekliyor:

```python
class BigUInt:
    BASE = 10**9

    def __init__(self, value='0'):
        value = value.lstrip('0') or '0'
        self.parts = []
        for end in range(len(value), 0, -9):
            start = max(0, end - 9)
            self.parts.append(int(value[start:end]))
        self._trim()

    def _trim(self):
        while len(self.parts) > 1 and self.parts[-1] == 0:
            self.parts.pop()

    def __str__(self):
        head = str(self.parts[-1])
        tail = ''.join(f'{x:09d}' for x in reversed(self.parts[:-1]))
        return head + tail

    def __add__(self, other):
        result, carry = [], 0
        size = max(len(self.parts), len(other.parts))
        for i in range(size):
            a = self.parts[i] if i < len(self.parts) else 0
            b = other.parts[i] if i < len(other.parts) else 0
            total = a + b + carry
            result.append(total % self.BASE)
            carry = total // self.BASE
        if carry:
            result.append(carry)
        answer = BigUInt()
        answer.parts = result
        return answer
```

`carry`, yani elde, bir hücrenin tabanı aşan bölümünü sonraki hücreye aktarır. Toplama her parçayı yalnızca bir kez ziyaret ettiği için zaman karmaşıklığı $O(n)$ olur.

## Uzun çarpma

Çarpma işleminde her parçayı karşı tarafın tüm parçalarıyla eşleştiririz:

```python
def multiply(a, b):
    out = [0] * (len(a.parts) + len(b.parts))
    for i, x in enumerate(a.parts):
        carry = 0
        for j, y in enumerate(b.parts):
            total = out[i + j] + x * y + carry
            out[i + j] = total % a.BASE
            carry = total // a.BASE
        out[i + len(b.parts)] += carry

    result = BigUInt()
    result.parts = out
    result._trim()
    return result
```

Bu klasik algoritma $O(nm)$ karmaşıklığındadır. Binlerce parçada Karatsuba ile yaklaşık $O(n^{1.585})$, daha büyük girdilerde FFT tabanlı yöntemlerle daha iyi sonuç alınabilir.

## Sıradaki geliştirmeler

Gerçek bir kütüphane için işaret yönetimi, çıkarma, karşılaştırma, bölme ve sıfıra bölme denetimi eklenmelidir. Rastgele üretilen sayılarla sonuçları dilin yerleşik BigInt özelliğine karşı sınamak da güçlü bir test stratejisidir. Böylece dev sayıların sihir değil; doğru temsil, elde aktarımı ve dikkatli algoritma seçiminden ibaret olduğunu görebilirsiniz.
