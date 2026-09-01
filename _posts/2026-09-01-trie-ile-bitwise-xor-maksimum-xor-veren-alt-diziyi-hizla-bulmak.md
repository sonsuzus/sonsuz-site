---
layout: post
title: "Trie ile Bitwise XOR: Maksimum XOR Veren Alt Diziyi Hızla Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - trie
  - bitwise xor
  - algoritmalar
toc: true
---

Bir sayı dizisindeki tüm alt dizileri deneyerek maksimum XOR sonucunu aramak kolaydır; ne var ki bu yöntem büyük verilerde bilgisayarı küçük çaplı bir varoluş krizine sürükler. Önek XOR değerlerini bit düzeyinde saklayan bir **Trie**, aynı problemi çok daha verimli biçimde çözmemizi sağlar. Üstelik yalnızca maksimum değeri değil, bu değeri oluşturan alt dizinin sınırlarını da bulabiliriz.

``

## Temel fikir: Önek XOR

Dizimiz $a_0,a_1,\ldots,a_{n-1}$ olsun. İlk $i$ elemanın XOR sonucunu önek değeri olarak tanımlayalım:

$$P_i=a_0\oplus a_1\oplus\cdots\oplus a_i$$

XOR işleminin önemli özelliği, aynı sayının kendisiyle XOR sonucunun sıfır olmasıdır: $x\oplus x=0$. Bu nedenle $l$ ile $r$ arasındaki alt dizinin XOR değeri şöyle hesaplanır:

$$a_l\oplus\cdots\oplus a_r=P_r\oplus P_{l-1}$$

Burada $l=0$ durumu için hayali bir $P_{-1}=0$ öneki kullanılır. Böylece problem, her yeni $P_r$ için daha önce görülen ve $P_r\oplus P_j$ değerini maksimum yapan $P_j$ önek değerini bulmaya dönüşür.

| Yaklaşım | Alt dizi sorgusu | Toplam süre | Ek bellek |
|---|---:|---:|---:|
| Tüm alt dizileri doğrudan hesaplama | $O(n)$ | $O(n^3)$ | $O(1)$ |
| Önek XOR ile çiftleri deneme | $O(1)$ | $O(n^2)$ | $O(n)$ |
| Bitwise Trie kullanma | $O(W)$ | $O(nW)$ | $O(nW)$ |

$W$, sayıların incelenen bit sayısıdır. 32 bitlik pozitif tamsayılarda sabit kabul edildiğinden Trie yaklaşımı pratikte yaklaşık $O(n)$ çalışır.

## Trie neden maksimumu bulur?

Her önek XOR değeri, en anlamlı bitten en az anlamlı bite doğru Trie'a eklenir. Her düğümün `0` ve `1` olmak üzere en fazla iki çocuğu vardır.

Bir $x$ değeriyle maksimum XOR üretmek istediğimizi düşünelim. $x$'in mevcut biti `0` ise sonuç bitini `1` yapmak için Trie'da `1` dalını seçmek isteriz. Bit `1` ise bu kez `0` dalı tercih edilir. Karşıt dal yoksa aynı bitli dala mecburen geçilir. En anlamlı bitler sayısal değere daha fazla katkı verdiği için bu açgözlü seçim doğrudur.

Örneğin 5 sayısı ikilik sistemde `0101` ise öncelikli olarak `1, 0, 1, 0` yönleri aranır. Trie adeta “zıt kutuplar birbirini çeker” ilkesini bitlere uygular.

## Python uygulaması

Aşağıdaki kod, maksimum XOR değerini ve bunu veren kapsayıcı alt dizi sınırlarını döndürür:

```python
class BitwiseTrie:
    def __init__(self, width=31):
        self.width = width
        self.root = {}

    def insert(self, value, index):
        node = self.root
        for bit_pos in range(self.width, -1, -1):
            bit = (value >> bit_pos) & 1
            node = node.setdefault(bit, {})
        node['index'] = index

    def best_match(self, value):
        node = self.root
        result = 0

        for bit_pos in range(self.width, -1, -1):
            bit = (value >> bit_pos) & 1
            opposite = 1 - bit

            if opposite in node:
                result |= 1 << bit_pos
                node = node[opposite]
            else:
                node = node[bit]

        return result, node['index']


def maximum_xor_subarray(numbers):
    trie = BitwiseTrie()
    trie.insert(0, -1)  # P[-1]: sıfır öneki

    prefix = 0
    best_value = -1
    best_range = None

    for right, number in enumerate(numbers):
        prefix ^= number
        value, prefix_index = trie.best_match(prefix)

        if value > best_value:
            best_value = value
            best_range = (prefix_index + 1, right)

        trie.insert(prefix, right)

    return best_value, best_range
```

Sıfır önekinin `-1` indeksiyle baştan eklenmesi, dizinin ilk elemanından başlayan alt dizileri özel koşul yazmadan kapsar. Ayrıca sorgunun eklemeden önce yapılması, yalnızca önceki öneklerle eşleşme kurulmasını sağlar.

## Dikkat edilmesi gerekenler

Python tamsayıları sınırsız hassasiyetlidir; negatif sayılarda sağa kaydırma işaret bitini korur. Negatif girdiler desteklenecekse sabit bir bit genişliği seçilip değerler maske ile dönüştürülmelidir:

$$x'=x\ \&\ (2^W-1)$$

Eşit maksimum sonuçlar için kod ilk bulunan aralığı saklar. En kısa veya sözlük sırasına göre ilk aralık isteniyorsa eşitlik durumuna ek karşılaştırma eklenebilir. Sonuç olarak önek XOR cebiri ve Bitwise Trie birleşimi, karesel aramayı bit başına birkaç karara indirerek büyük dizilerde güçlü ve öğretici bir çözüm sunar.
