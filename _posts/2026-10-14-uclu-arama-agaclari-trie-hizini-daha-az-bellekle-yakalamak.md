---
layout: post
title: "Üçlü Arama Ağaçları: Trie Hızını Daha Az Bellekle Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - tst
  - trie
  - veri yapıları
  - algoritmalar
  - dizgi arama
  - bellek yönetimi
toc: true
image: /img/uclu-arama-agaclari-53.png
---

Bir sözlük uygulamasında binlerce kelimeyi saklamak, otomatik tamamlama yapmak veya belirli bir önekle başlayan kayıtları bulmak istediğinizi düşünün. Trie bu işler için oldukça hızlıdır; ancak her düğümde alfabenin tamamı kadar bağlantı tutması belleği adeta açık büfeye çevirebilir. Üçlü Arama Ağacı, yani Ternary Search Tree (TST), Trie’ın karakter tabanlı yaklaşımını ikili arama ağacının ekonomik bağlantı modeliyle birleştirir.

``

## TST’nin temel fikri

TST’de her düğüm tek bir karakter ve üç bağlantı saklar:

- **Sol bağlantı:** Aranan karakter düğümün karakterinden küçükse izlenir.
- **Orta bağlantı:** Karakterler eşitse bir sonraki karaktere geçilir.
- **Sağ bağlantı:** Aranan karakter düğümün karakterinden büyükse izlenir.

Örneğin `kedi` kelimesini ararken kökteki karakter `k` ise orta dala geçilir ve `e` karşılaştırılır. Karşılaşılan düğüm `f` olsaydı `e < f` olduğundan sol dal izlenirdi. Bir düğüm ayrıca o noktada geçerli bir kelimenin bitip bitmediğini belirten işaret taşır. Böylece `el` ve `elma` aynı yapı içinde sorunsuzca saklanabilir.

TST’yi zihinde canlandırmanın pratik yolu şudur: **Orta bağlantılar kelimenin içinde ilerler, sol ve sağ bağlantılar aynı konumdaki alternatif karakterleri arar.**

## Trie ile karşılaştırma

| Özellik | Trie | TST |
|---|---|---|
| Düğüm başına bağlantı | Alfabe büyüklüğüne kadar | Her zaman 3 |
| Bellek kullanımı | Seyrek alfabelerde yüksek | Genellikle daha düşük |
| Arama yaklaşımı | Doğrudan karakter geçişi | Karakter karşılaştırması |
| Önek sorguları | Çok başarılı | Çok başarılı |
| Uygulama karmaşıklığı | Görece basit | Biraz daha dikkat ister |

![uclu-arama-agaclari-53](/img/uclu-arama-agaclari-53.svg)


Alfabe büyüklüğünü $R$, en uzun kelime uzunluğunu $L$ kabul edelim. Klasik Trie düğümü potansiyel olarak $R$ bağlantı taşırken TST düğümü yalnızca üç bağlantı taşır. Kabaca bağlantı alanı karşılaştırması şu şekilde düşünülebilir:

$$M_{Trie} \approx N \times R, \qquad M_{TST} \approx N \times 3$$

Buradaki $N$ düğüm sayısıdır. Bu ifade gerçek byte miktarını birebir vermez; fakat alfabe büyüdükçe Trie üzerindeki boş bağlantı maliyetinin neden can sıkıcı olduğunu gösterir.

## Python ile TST uygulaması

Aşağıdaki örnek kelime ekleme ve tam eşleşme arama işlemlerini gerçekleştirir:

```python
class Node:
    def __init__(self, char):
        self.char = char
        self.left = None
        self.middle = None
        self.right = None
        self.is_end = False


class TernarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, word):
        if not word:
            return
        self.root = self._insert(self.root, word, 0)

    def _insert(self, node, word, index):
        char = word[index]

        if node is None:
            node = Node(char)

        if char < node.char:
            node.left = self._insert(node.left, word, index)
        elif char > node.char:
            node.right = self._insert(node.right, word, index)
        elif index < len(word) - 1:
            node.middle = self._insert(node.middle, word, index + 1)
        else:
            node.is_end = True

        return node

    def contains(self, word):
        node = self.root
        index = 0

        while node and word:
            if word[index] < node.char:
                node = node.left
            elif word[index] > node.char:
                node = node.right
            elif index < len(word) - 1:
                index += 1
                node = node.middle
            else:
                return node.is_end

        return False
```

`insert`, karakter küçük veya büyük olduğunda aynı indisle yatay arama yapar. Eşleşme gerçekleştiğinde ise orta bağlantıya geçerek kelimenin sonraki karakterini işler. `contains` aynı mantığı döngüyle uygular ve son karakterde `is_end` değerini denetler.

## Zaman karmaşıklığı ve denge konusu

Dengeli bir TST’de arama maliyeti pratikte kelime uzunluğuna yakın davranır. Genel gösterimle ortalama maliyet $O(L + \log N)$ biçiminde yorumlanabilir. Ancak karakterler sıralı biçimde eklenirse sol ve sağ dallar dengesizleşebilir; en kötü durumda arama maliyeti $O(N)$ seviyesine yaklaşabilir.

Bu nedenle büyük veri kümelerinde kelimeleri karışık sırayla eklemek veya dengeli kurulum stratejileri kullanmak yararlıdır. TST; otomatik tamamlama, yazım denetimi, yönlendirme tabloları ve metin indeksleme gibi önek işlemlerinin önemli olduğu projelerde güçlü bir seçenektir. Kısacası Trie bir spor araba kadar doğrudan, TST ise aynı yolculuğu daha küçük bir yakıt deposuyla tamamlayan akıllı bir hibrittir.
