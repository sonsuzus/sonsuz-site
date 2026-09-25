---
layout: post
title: "Trie Üzerinde XOR Maksimizasyonu: Bitwise Aramanın Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - trie
  - xor
  - bitwise
  - python
  - veri yapıları
toc: true
image: /img/trie-uzerinde-xor-11.png
---

![trie-uzerinde-xor-11](/img/trie-uzerinde-xor-11.svg)


Bir sayı dizisindeki iki elemanın XOR sonucunu en büyük yapmak, ilk bakışta bütün çiftleri denemeyi gerektiren yorucu bir problem gibi görünür. Ancak sayıları bit dizileri olarak ele alıp bir **ikili Trie** içine yerleştirdiğimizde, her sayı için en iyi eşleşmeyi bit bit seçebiliriz. Böylece kaba kuvvetin karesel maliyetinden kurtulup oldukça hızlı ve eğlenceli bir çözüme ulaşırız.

``

## XOR neden maksimize edilebilir?

XOR işlemi, aynı bitler için `0`, farklı bitler için `1` üretir. Örneğin:

```text
10 = 1010
 5 = 0101
---------- XOR
15 = 1111
```

Matematiksel olarak iki sayının XOR değeri şöyle düşünülebilir:

$$x \oplus y = \sum_{i=0}^{B-1} d_i 2^i$$

Burada $d_i$, ilgili bitler farklıysa `1`, aynıysa `0` olur. Yüksek basamaklı bir bitin değeri, kendisinden düşük bütün bitlerin toplamından daha büyüktür. Bu nedenle aramaya **en anlamlı bitten** başlamak gerekir. Mevcut bit `0` ise karşı tarafta `1`, mevcut bit `1` ise karşı tarafta `0` bulmayı tercih ederiz.

| Yaklaşım | Zaman karmaşıklığı | Ek bellek | Temel fikir |
|---|---:|---:|---|
| Kaba kuvvet | $O(n^2)$ | $O(1)$ | Her sayı çiftini dene |
| Sıralama | Doğrudan yeterli değil | Değişken | Sayısal yakınlık XOR yakınlığı değildir |
| İkili Trie | $O(nB)$ | $O(nB)$ | Her bitte zıt dalı seç |

Buradaki $B$, sayıların bit uzunluğudur. Standart 32 bit tamsayılarda sabit kabul edildiğinde algoritma pratikte $O(n)$ gibi davranır.

## İkili Trie nasıl çalışır?

Trie düğümlerinin en fazla iki çocuğu vardır: `0` ve `1`. Bir sayı eklenirken bitleri soldan sağa doğru uygun dallara yerleştirilir. Bir sayı sorgulanırken ise XOR değerini büyütmek için öncelikle mevcut bitin tersi aranır. Ters dal yoksa mecburen aynı bitin bulunduğu dala gidilir.

Sayıları sırayla sorgulayıp ardından Trie'a eklemek önemli bir ayrıntıdır. Böylece sorgulanan sayı yalnızca daha önce eklenmiş sayılarla eşleşir; aynı elemanın kendisiyle çift oluşturması engellenir.

## Python uygulaması

Aşağıdaki kod hem en büyük XOR değerini hem de bu değeri üreten sayı çiftini döndürür:

```python
class BinaryTrie:
    def __init__(self, bit_count):
        self.root = {}
        self.bit_count = bit_count

    def insert(self, number):
        node = self.root
        for bit_index in range(self.bit_count - 1, -1, -1):
            bit = (number >> bit_index) & 1
            node = node.setdefault(bit, {})
        node['value'] = number

    def best_partner(self, number):
        node = self.root
        for bit_index in range(self.bit_count - 1, -1, -1):
            bit = (number >> bit_index) & 1
            opposite = 1 - bit

            # Farklı bit, XOR sonucunda bu basamağı 1 yapar.
            if opposite in node:
                node = node[opposite]
            else:
                node = node[bit]

        return node['value']


def maximum_xor_pair(numbers):
    if len(numbers) < 2:
        raise ValueError('En az iki sayı gereklidir.')

    bit_count = max(1, max(numbers).bit_length())
    trie = BinaryTrie(bit_count)
    trie.insert(numbers[0])

    best_xor = -1
    best_pair = None

    for number in numbers[1:]:
        partner = trie.best_partner(number)
        current_xor = number ^ partner

        if current_xor > best_xor:
            best_xor = current_xor
            best_pair = (partner, number)

        trie.insert(number)

    return best_pair, best_xor


values = [3, 10, 5, 25, 2, 8]
print(maximum_xor_pair(values))  # ((5, 25), 28)
```

Örnekte $5 \oplus 25 = 28$ olur. İkili gösterimde `00101 XOR 11001 = 11100` elde edilir. En yüksek bitlerde farklılık yakalandığı için sonuç büyüktür.

## Dikkat edilmesi gerekenler

Bu uygulama negatif olmayan tamsayıları hedefler. Negatif sayılarda Python'ın işaret uzatmalı bit gösterimi devreye girdiğinden sabit bir bit genişliği belirlemek gerekir. Ayrıca Trie bellek tüketimini azaltmak için sözlükler yerine iki elemanlı düğüm dizileri kullanılabilir. Özetle ikili Trie, XOR problemini sayılar dünyasından çıkarıp yönlendirilmiş bir bit yolculuğuna dönüştürür: Her kavşakta zıt yolu seç, mümkün olan en büyük sonuca ilerle!
