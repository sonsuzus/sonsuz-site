---
layout: post
title: "Aho-Corasick: Binlerce Kelimeyi Tek Geçişte Aramak"
math: true
categories: 
  - Bilgi
tags: 
  - aho-corasick
  - algoritma
  - metin-arama
  - trie
  - python
  - veri-yapıları
toc: true
---

Bir metinde tek kelime aramak kolaydır; fakat yasaklı sözcükler, virüs imzaları veya anahtar kelimelerden oluşan dev bir listeyi aramak istediğimizde işler değişir. Her kelime için metni baştan sona taramak, aynı yolu binlerce kez yürümeye benzer. Aho-Corasick algoritması ise kelimeleri ortak bir veri yapısında birleştirerek metni yalnızca bir kez tarar.

``

## Problem neden zorlaşıyor?

Metnin uzunluğu $n$, aranacak desenlerin sayısı $k$ ve desenlerin ortalama uzunluğu $m$ olsun. Her deseni ayrı ayrı, basit yöntemle ararsak yaklaşık maliyet:

$$O(n \cdot k \cdot m)$$

olabilir. Aho-Corasick, ön işleme sonrasında arama maliyetini şu seviyeye indirir:

$$O(n + z)$$

Buradaki $z$, bulunan eşleşmelerin sayısıdır. Otomatı kurma maliyeti ise desenlerin toplam karakter sayısı $L$ için yaklaşık $O(L \cdot \vert \Sigma\vert )$ ya da geçişlerin saklanma biçimine göre $O(L)$ kabul edilir. $\Sigma$, kullanılan karakter alfabesidir.

| Yaklaşım | Ön işleme | Arama yaklaşımı | Çok sayıda desen için durum |
|---|---:|---:|---|
| Basit arama | Yok | Her kelime metinde ayrı aranır | Yavaş |
| KMP | Her desen için | Tek desende verimli | Binlerce desen için tekrarlı |
| Aho-Corasick | Trie ve hata bağlantıları | Tüm desenler aynı anda aranır | Çok verimli |

## Üç temel parça

Algoritmanın kalbinde bir **Trie** bulunur. Kelimeler karakter karakter ağaca eklenir ve ortak önekler aynı yolu paylaşır. Örneğin `elma` ile `elmas`, ilk dört karakter boyunca aynı düğümleri kullanır.

İkinci parça **failure link**, yani hata bağlantısıdır. Okunan karakter için mevcut düğümden geçiş yoksa algoritma başlangıca dönüp her şeyi unutmaz. Bunun yerine, şimdiye kadar okunan parçanın anlamlı en uzun son ekine gider. Bu fikir, KMP algoritmasındaki başarısızlık fonksiyonunun çok desenli kuzeni gibidir.

Üçüncü parça **çıktı listeleridir**. Bir düğüme ulaşıldığında yalnızca o düğümde biten kelime değil, hata bağlantıları üzerinden biten daha kısa kelimeler de eşleşmiş olabilir. Örneğin `biber` aranırken desen listesinde `ber` varsa iki desen aynı konumda raporlanabilir.

## Python ile orta düzey bir uygulama

Aşağıdaki sınıf Trie oluşturur, genişlik öncelikli aramayla hata bağlantılarını hesaplar ve metindeki eşleşmeleri döndürür:

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
        state = 0
        for index, char in enumerate(text):
            while state and char not in self.next[state]:
                state = self.fail[state]

            state = self.next[state].get(char, 0)
            for word in self.output[state]:
                yield index - len(word) + 1, word
```

Kullanımı oldukça doğrudandır:

```python
matcher = AhoCorasick()
for word in ["elma", "armut", "mat", "umut"]:
    matcher.add(word)

matcher.build()
print(list(matcher.search("elmalı armut umut verir")))
```

`add` kelimeleri Trie'a yerleştirir, `build` hata bağlantılarını hazırlar, `search` ise metni soldan sağa tek geçişte işler. Aynı konumda birden fazla sonuç çıkması tamamen normaldir.

## Nerelerde kullanılır?

Aho-Corasick; içerik moderasyonu, spam filtreleme, ağ saldırısı imzaları, DNA dizisi analizi, log tarama ve arama motorlarında kullanılır. En büyük avantajı, desen sayısı arttıkça metni tekrar tekrar dolaşmamasıdır. Bunun karşılığında Trie düğümleri ve bağlantılar ek bellek tüketir.

Kısacası algoritma, “Her kelime için yeniden ara” yaklaşımını “Bütün kelimeleri bir otomatta topla” fikrine dönüştürür. Büyük desen listelerinde bu küçük zihniyet değişikliği, dramatik bir performans kazancı sağlar.
