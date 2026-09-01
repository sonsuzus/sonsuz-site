---
layout: post
title: "Aho-Corasick Otomatı: Binlerce Kelimeyi Tek Geçişte Aramak"
math: true
categories: 
  - Bilgi
tags: 
  - aho-corasick
  - algoritma
  - metin-arama
toc: true
---

Bir metinde tek bir kelime aramak kolaydır; peki zararlı yazılım imzaları, yasaklı ifadeler veya DNA dizileri gibi binlerce deseni aynı anda bulmak istersek ne olur? Her kelime için metni baştan sona taramak çalışır, ancak performansı kısa sürede bir kaplumbağa yarışına dönüştürür. Aho-Corasick otomatı, bütün desenleri ortak bir sözlük ağacında birleştirerek metni yalnızca bir kez dolaşmamızı sağlar.

``

## Problemin matematiksel yüzü

Elimizde toplam uzunluğu $L$ olan desenler ve uzunluğu $N$ olan bir metin bulunsun. Her deseni bağımsız aradığımızda kaba yaklaşımın maliyeti, desen sayısı $K$ için yaklaşık $O(NK)$ olabilir. Aho-Corasick ise otomata hazırlama ve arama işlemlerini şu sınırda gerçekleştirir:

$$O(L + N + Z)$$

Buradaki $Z$, bulunan eşleşmelerin sayısıdır. Sonuçları yazdırmak bile zaman aldığı için $Z$ teriminden kaçmak mümkün değildir. Algoritmanın başarısı, binlerce ayrı aramayı metin üzerinde tek bir yürüyüşe çevirmesidir.

| Yaklaşım | Ön hazırlık | Arama maliyeti | Çoklu desen desteği |
|---|---:|---:|---|
| Saf karşılaştırma | Yok | $O(NK)$ | Zayıf |
| KMP | Her desen için | $O(NK)$ | Dolaylı |
| Aho-Corasick | $O(L)$ | $O(N + Z)$ | Doğrudan |

## Üç parçalı mekanizma

Algoritmanın ilk parçası **Trie**, yani sözlük ağacıdır. `elma`, `elmas` ve `elbise` sözcükleri `el` önekini paylaşır. Böylece aynı karakterler tekrar tekrar saklanmaz.

İkinci parça **failure link** bağlantılarıdır. Otomat mevcut karakterle ilerleyemediğinde aramayı sıfırlamak yerine, eşleşmiş bölümün kullanılabilecek en uzun son ekine geçer. Bu davranış KMP algoritmasındaki geri dönüş tablosuna benzer. Örneğin `hers` işlenirken bir yol tıkanırsa otomat uygun durum üzerinden `ers`, `rs` veya `s` olasılıklarını değerlendirebilir.

Üçüncü parça ise **çıktı listesidir**. Bir durum birden fazla deseni tamamlayabilir. Örneğin `she` okununca hem `she` hem de failure bağlantısı üzerinden `he` bulunmuş olabilir.

| Bileşen | Görevi | Kazancı |
|---|---|---|
| Trie geçişi | Ortak önekleri birleştirir | Bellek ve tekrar tasarrufu |
| Failure link | Hata sonrası uygun son eke döner | Metinde geri gitmeme |
| Çıktı listesi | Tamamlanan desenleri tutar | İç içe eşleşmeleri bulma |

## Python ile orta düzey bir uygulama

Aşağıdaki sınıf önce desenleri Trie yapısına ekler, ardından genişlik öncelikli aramayla failure bağlantılarını kurar. `search` metodu metni tek geçişte tarayarak bulunan kelimeleri ve başlangıç konumlarını döndürür.

```python
from collections import deque

class AhoCorasick:
    def __init__(self):
        self.next = [{}]
        self.fail = [0]
        self.output = [[]]

    def add(self, word):
        state = 0
        for char in word:
            if char not in self.next[state]:
                self.next[state][char] = len(self.next)
                self.next.append({})
                self.fail.append(0)
                self.output.append([])
            state = self.next[state][char]
        self.output[state].append(word)

    def build(self):
        queue = deque(self.next[0].values())
        while queue:
            state = queue.popleft()
            for char, child in self.next[state].items():
                queue.append(child)
                fallback = self.fail[state]
                while fallback and char not in self.next[fallback]:
                    fallback = self.fail[fallback]
                self.fail[child] = self.next[fallback].get(char, 0)
                self.output[child] += self.output[self.fail[child]]

    def search(self, text):
        state, matches = 0, []
        for index, char in enumerate(text):
            while state and char not in self.next[state]:
                state = self.fail[state]
            state = self.next[state].get(char, 0)
            for word in self.output[state]:
                matches.append((index - len(word) + 1, word))
        return matches
```

Kullanım oldukça sadedir:

```python
ac = AhoCorasick()
for word in ["he", "she", "his", "hers"]:
    ac.add(word)

ac.build()
print(ac.search("ushers"))
# [(1, 'she'), (2, 'he'), (2, 'hers')]
```

## Nerelerde kullanılır?

Aho-Corasick; antivirüs imza taramasında, içerik filtrelemede, arama motorlarında, log analizinde, ağ saldırısı tespitinde ve biyoinformatikte sıkça kullanılır. Desen kümesi sabitse hazırlama maliyeti bir kez ödenir ve milyonlarca metin hızla taranabilir.

Elbette ücretsiz öğle yemeği yoktur: Otomat, özellikle büyük alfabelerde önemli miktarda bellek tüketebilir. Seyrek geçişleri sözlüklerle saklamak belleği azaltırken dizi tabanlı geçişler daha hızlı olabilir. Yine de konu “çok desen, tek metin geçişi” olduğunda Aho-Corasick, algoritma çantasındaki en güçlü araçlardan biridir.
