---
layout: post
title: "Trie ile Otomatik Tamamlama: Arama Kutularına Akıl Katmak"
math: true
categories: 
  - Proje
tags: 
  - trie
  - veri yapıları
  - javascript
toc: true
image: /img/trie-ile-otomatik-43.png
---

Bir arama kutusuna `pro` yazdığınızda saniyeler değil, milisaniyeler içinde `programlama`, `proje` ve `profil` önerilerinin belirmesi sihir değildir: sahnenin arkasında çoğu zaman Trie veri yapısı çalışır. Prefix tree olarak da bilinen Trie, kelimeleri karakter karakter dallandırarak saklar. Böylece tüm kelime listesini her tuş vuruşunda baştan sona dolaşmak yerine, yalnızca yazılan öneke karşılık gelen dalı takip ederiz.
``
## Trie mantığı: Kelimeler bir ağacın dallarıdır

Trie içinde her düğüm bir karakteri temsil eder; kök düğüm ise boş başlangıç noktasıdır. `cat`, `car` ve `card` kelimelerini eklediğimizi düşünelim. İlk iki karakter olan `c` ve `a`, kelimeler arasında ortak olduğundan tek kez saklanır. Ardından `t` ve `r` için dallanma gerçekleşir. Bir düğümdeki `isWord` işareti, o noktaya kadar gelinen karakter dizisinin geçerli bir kelime olup olmadığını belirtir.

Bir kelimenin uzunluğu $L$ ise ekleme ve arama işlemlerinin zaman maliyeti genellikle $O(L)$ olur. Önemli nokta şudur: Bu maliyet, sözlükteki toplam kelime sayısı $N$ ile doğrudan büyümez. Elbette öneri listesini üretirken bulunan sonuç sayısı $K$ da maliyete eklenir: $O(P + K)$; burada $P$, kullanıcının yazdığı prefix uzunluğudur.

| Yaklaşım | Prefix arama maliyeti | Güçlü yanı | Zayıf yanı |
|---|---:|---|---|
| Dizi + filtre | $O(N \times P)$ | Uygulaması çok kolay | Büyük sözlüklerde yavaşlar |
| Sıralı dizi + ikili arama | $O(\log N + K)$ | Bellek açısından verimli | Ekleme maliyetlidir |
| Trie | $O(P + K)$ | Anlık öneriler için idealdir | Düğüm sayısı bellek tüketebilir |

![trie-ile-otomatik-43](/img/trie-ile-otomatik-43.svg)


## JavaScript ile çalışan bir Trie

Aşağıdaki sınıf, kelime ekler; girilen prefix için sınırlı sayıda öneri döndürür. Çocuk düğümlerini `Map` ile tutmak, karakter erişimini okunaklı ve ortalama durumda hızlı hale getirir.

```javascript
class TrieNode {
  constructor() {
    this.children = new Map();
    this.isWord = false;
  }
}

class Trie {
  constructor() {
    this.root = new TrieNode();
  }

  insert(word) {
    let node = this.root;
    for (const char of word.toLocaleLowerCase('tr-TR')) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char);
    }
    node.isWord = true;
  }

  suggest(prefix, limit = 5) {
    const normalized = prefix.toLocaleLowerCase('tr-TR');
    let node = this.root;

    for (const char of normalized) {
      node = node.children.get(char);
      if (!node) return [];
    }

    const results = [];
    const walk = (current, text) => {
      if (results.length >= limit) return;
      if (current.isWord) results.push(text);
      for (const [char, child] of current.children) {
        walk(child, text + char);
      }
    };

    walk(node, normalized);
    return results;
  }
}

const trie = new Trie();
['program', 'programlama', 'proje', 'profil', 'python'].forEach(w => trie.insert(w));
console.log(trie.suggest('pro')); // ["program", "programlama", "proje", "profil"]
```

`walk` fonksiyonu, prefix düğümünden itibaren derinlik öncelikli dolaşım yapar. `limit` kontrolü kritik bir ayrıntıdır: Çok geniş bir dalda binlerce sonucu tek seferde arayüze taşımak hem gereksiz hem de kullanıcı deneyimi açısından yorucudur.

## Arama kutusuna bağlamak

Gerçek bir arayüzde `input` olayını dinleyip her değişimde `suggest` çağırabilirsiniz. Boş sorguda öneri göstermemek ve kullanıcı hızlı yazarken aramayı küçük bir `debounce` ile geciktirmek iyi fikirdir. Ayrıca Türkçe karakterler için `toLocaleLowerCase('tr-TR')` kullanılması, özellikle `I/ı` ve `İ/i` dönüşümlerinde beklenmedik eşleşmeleri önler.

Trie temel sürümde sonuçları eklenme sırasına göre döndürür. Popülerlik tabanlı öneriler istiyorsanız düğümlere arama sayacı ekleyebilir, sonuçları bu puana göre sıralayabilirsiniz. Yazım toleransı, çok kelimeli arama ve kişiselleştirme eklendiğinde Trie tek başına yeterli olmayabilir; fakat hızlı prefix eşleştirme için hâlâ sağlam, öğretici ve etkileyici bir başlangıçtır.
