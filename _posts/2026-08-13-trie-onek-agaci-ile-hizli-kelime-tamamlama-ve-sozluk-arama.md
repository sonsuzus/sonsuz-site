---
layout: post
title: "Trie (Önek Ağacı) ile Hızlı Kelime Tamamlama ve Sözlük Arama"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - trie
  - python
  - algoritmalar
  - otomatik tamamlama
---

Arama kutusuna birkaç harf yazdığınızda önerilerin anında belirmesi sihir değil; çoğu zaman arka planda çalışan akıllı bir veri yapısıdır: **Trie**. “Prefix Tree” yani önek ağacı olarak da bilinen Trie, kelimeleri karakter karakter dallandırarak saklar. Bu yaklaşım, özellikle sözlük araması, yazım denetimi, URL yönlendirme ve otomatik tamamlama gibi senaryolarda klasik liste taramasından çok daha verimli olabilir.
``

Trie’nin temel fikri oldukça sezgiseldir: Ortak başlangıca sahip kelimeler, ağacın aynı dallarını paylaşır. Örneğin `araba`, `arama` ve `armut` kelimeleri ilk iki karakter olan `ar` düğümlerini ortak kullanır. Her düğüm bir karakteri temsil eder; ayrıca o düğümde biten geçerli bir kelime olup olmadığını belirten bir işaret bulunur. Böylece `ara` bir kelimeyse, `a → r → a` yolunun son düğümünde `is_end = true` tutulur.

Bir Trie içindeki arama maliyeti, kelime sayısına değil sorgunun uzunluğuna bağlıdır. Uzunluğu $L$ olan bir kelime için ekleme ve arama karmaşıklığı genel olarak şöyledir:

$$T_{insert}(L) = T_{search}(L) = O(L)$$

Bu, binlerce hatta milyonlarca kelime olsa bile `merhaba` gibi 7 karakterli bir sorgunun yaklaşık 7 düğümlük yolunu izleyeceğimiz anlamına gelir. Elbette düğümlerdeki çocukları nasıl sakladığımız uygulamanın pratik performansını etkiler.

| Yapı | Kelime arama | Önek sorgusu | Ortak önek kullanımı | Bellek tüketimi |
|---|---:|---:|---|---|
| Liste | $O(N \cdot L)$ | $O(N \cdot L)$ | Yok | Düşük |
| Hash Set | Ortalama $O(L)$ | Doğrudan desteklemez | Yok | Orta |
| Trie | $O(L)$ | $O(P + K)$ | Var | Görece yüksek |

Tablodaki $N$ kelime sayısını, $L$ kelime uzunluğunu, $P$ yazılan önek uzunluğunu ve $K$ döndürülen öneri sayısını temsil eder. Trie’nin güçlü tarafı yalnızca “kelime var mı?” sorusu değildir; `pro` ile başlayan tüm kelimeleri de ağacın ilgili dalından yürüyerek bulabilir.

Aşağıdaki Python örneği, kelime ekleme, tam arama ve otomatik tamamlama işlevlerini içerir. Çocuk düğümleri `dict` ile tutulduğu için her karaktere erişim ortalama olarak hızlıdır.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word.lower():
            node = node.children.setdefault(char, TrieNode())
        node.is_end = True

    def search(self, word):
        node = self._find_node(word.lower())
        return node is not None and node.is_end

    def autocomplete(self, prefix, limit=5):
        node = self._find_node(prefix.lower())
        if node is None:
            return []

        results = []

        def dfs(current, suffix):
            if len(results) >= limit:
                return
            if current.is_end:
                results.append(prefix.lower() + suffix)
            for char, child in current.children.items():
                dfs(child, suffix + char)

        dfs(node, "")
        return results

    def _find_node(self, text):
        node = self.root
        for char in text:
            if char not in node.children:
                return None
            node = node.children[char]
        return node


trie = Trie()
for word in ["program", "programlama", "programcı", "proje", "python"]:
    trie.insert(word)

print(trie.search("proje"))          # True
print(trie.search("profil"))         # False
print(trie.autocomplete("prog"))     # ['program', 'programlama', 'programcı']
```

Buradaki `_find_node` yardımcı metodu, hem arama hem de önek tamamlama için ortak yolu izler. `autocomplete` ise önek düğümünden itibaren derinlik öncelikli arama (DFS) yapar. `limit` parametresi özellikle kullanıcı arayüzleri için önemlidir: Kullanıcıya yüzlerce öneri yerine ilk birkaç sonucu vermek hem daha anlaşılır hem de daha hızlıdır.

Trie’nin bedeli bellektir. Her karakter için nesne ve bağlantı oluşturmak, kısa kelimelerde maliyetli olabilir. Büyük sözlüklerde bu sorunu azaltmak için **radix tree** (sıkıştırılmış Trie), karakter dizisi tabanlı düğümler veya disk üzerinde indeksleme tercih edilir. Yine de önek araması uygulamanın merkezindeyse, Trie doğru problemi doğru araçla çözmenin en temiz örneklerinden biridir.
