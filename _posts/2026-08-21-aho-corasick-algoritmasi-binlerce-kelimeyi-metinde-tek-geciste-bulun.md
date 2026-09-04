---
layout: post
title: "Aho-Corasick Algoritması: Binlerce Kelimeyi Metinde Tek Geçişte Bulun"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - metin işleme
  - aho-corasick
image: /img/aho-corasick-algoritmasi-67.png
---

Bir metinde tek bir kelime aramak kolaydır; `indexOf`, regex veya KMP çoğu zaman yeterlidir. Peki bir log akışında binlerce zararlı imzayı, bir sözlükte binlerce anahtar sözcüğü ya da bir DNA dizisinde çok sayıda motifi aynı anda bulmak gerekirse? Her kelime için metni yeniden taramak, büyüyen veriyle birlikte pahalılaşır. Aho-Corasick, bu problemi bir trie ve akıllı geri dönüş bağlantılarıyla tek geçişte çözen klasik çoklu örüntü arama algoritmasıdır.

![aho-corasick-algoritmasi-67](/img/aho-corasick-algoritmasi-67.svg)

``

Algoritmanın teorik kalbinde **trie** bulunur. Trie, ortak ön ekleri paylaşan kelimeleri ağaç biçiminde saklar. Örneğin `he`, `she`, `his` ve `hers` kelimeleri aynı yapıdaki bazı düğümleri kullanır. Ancak trie tek başına yeterli değildir: Metinde bir karakter uyuşmadığında köke dönmek, daha önce elde edilen bilgiyi çöpe atar. Aho-Corasick bu kaybı **failure (başarısızlık)** bağlantılarıyla önler.

Her düğümün failure bağlantısı, o düğümün temsil ettiği metnin en uzun uygun son ekini temsil eden düğümü gösterir. Başka deyişle, bir eşleşme yolu bozulduğunda algoritma “Şimdiye kadarki karakterlerin sonu, hangi başka kelimenin başlangıcı olabilir?” diye sorar. Bu fikir KMP'nin prefix tablosuna benzer, fakat burada tek desen yerine bütün bir trie vardır.

| Yapı / kavram | Görevi | Neden önemlidir? |
|---|---|---|
| Trie | Desenlerin ön eklerini saklar | Ortak karakterleri tekrar etmez |
| Failure link | Uyuşmazlıkta alternatif duruma geçer | Metni geri sarmayı engeller |
| Output listesi | Bir düğümde biten desenleri tutar | İç içe eşleşmeleri yakalar |
| BFS | Failure linklerini kurar | Bağlantıları doğru sırada üretir |

Çalışma maliyeti etkileyici derecede dengelidir. Desenlerin toplam uzunluğu $P$, metin uzunluğu $N$ ve bulunan eşleşme sayısı $Z$ olsun. Otomatın kurulması yaklaşık $O(P)$, arama ise $O(N + Z)$ maliyetindedir. `Z` terimi kaçınılmazdır; sonuç olarak on bin eşleşme döndürüyorsanız, bunları raporlamanın da bir bedeli vardır.

$$T_{toplam} = O(P + N + Z)$$

Aşağıdaki Python örneği, eğitim amacıyla sadeleştirilmiş bir Aho-Corasick otomatonu kurar. `fail` dizisi geri dönüşleri, `out` ise eşleşen kelimeleri taşır. Gerçek üretim sistemlerinde büyük alfabeler için geçiş tablosu, bellek optimizasyonu veya hazır bir kütüphane tercih edilebilir.

```python
from collections import deque, defaultdict

patterns = ["he", "she", "his", "hers"]
next_node = [defaultdict(lambda: -1)]
fail = [0]
out = [[]]

# Trie oluşturma
for word in patterns:
    state = 0
    for ch in word:
        if next_node[state][ch] == -1:
            next_node[state][ch] = len(next_node)
            next_node.append(defaultdict(lambda: -1))
            fail.append(0)
            out.append([])
        state = next_node[state][ch]
    out[state].append(word)

# Failure bağlantılarını BFS ile kurma
queue = deque()
for ch, child in next_node[0].items():
    queue.append(child)

while queue:
    state = queue.popleft()
    for ch, child in next_node[state].items():
        queue.append(child)
        fallback = fail[state]
        while fallback and next_node[fallback][ch] == -1:
            fallback = fail[fallback]
        fail[child] = max(next_node[fallback][ch], 0)
        out[child] += out[fail[child]]

# Metni tek geçişte tarama
text, state = "ushers", 0
for i, ch in enumerate(text):
    while state and next_node[state][ch] == -1:
        state = fail[state]
    state = max(next_node[state][ch], 0)
    for word in out[state]:
        print(word, "başlangıç:", i - len(word) + 1)
```

`ushers` üzerinde çıktı, `she`, `he` ve `hers` eşleşmelerini verir. Özellikle `she` bulunurken onun son ekindeki `he` de kaçmaz; output listelerinin failure bağlantısından miras almasının sebebi budur.

| Yaklaşım | Çok sayıda desen için durum |
|---|---|
| Her desenle ayrı arama | Yaklaşık $O(N \times desen\ sayısı)$ |
| Büyük regex alternatifi | Pratik ama motor davranışına bağımlı |
| Aho-Corasick | Deterministik, tek geçişte $O(N + Z)$ |

Spam filtresi, içerik moderasyonu, ağ paketi inceleme, genom analizi ve IDE'lerde çoklu arama gibi alanlarda Aho-Corasick güçlü bir araçtır. Desen sayısı arttıkça sihri daha görünür olur: Metni yeniden okutmak yerine, otomatonun durumunu ilerletirsiniz. Binlerce kelime, tek yürüyüş; algoritmaların en tatlı kestirmelerinden biri budur.
