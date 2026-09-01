---
layout: post
title: "Palindromik Ağaç (Eertree): Metinlerdeki Simetrileri Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - eertree
  - palindrom
  - veri-yapıları
toc: true
---

Bir kelimeyi tersten okuduğumuzda yine aynı kelimeyle karşılaşıyorsak elimizde bir palindrom vardır: `kazak`, `ada` veya `kabak` gibi. Peki milyonlarca karakter içeren bir metindeki bütün farklı palindromik alt metinleri bulmak istersek ne olur? Her aralığı tek tek denemek yerine Eertree, diğer adıyla Palindromik Ağaç, bu simetrik parçaları oldukça zarif biçimde saklar.
``
## Önce küçük bir terminoloji düzeltmesi

Eertree, tüm palindromik **alt metinleri** yani ardışık karakterlerden oluşan parçaları bulur. Alt dizi kavramında karakterlerin bitişik olması gerekmez; dolayısıyla klasik Eertree doğrudan palindromik alt dizileri çözmez.

Uzunluğu $n$ olan bir metinde yaklaşık

$$\frac{n(n+1)}{2}$$

farklı aralık bulunur. Her aralığın palindrom olup olmadığını karakterleri karşılaştırarak kontrol etmek kaba kuvvette $O(n^3)$ zamana kadar çıkabilir. Merkezden genişletme yaklaşımı bunu $O(n^2)$ seviyesine indirir. Eertree ise bütün **farklı** palindromik alt metinleri $O(n \cdot \vert \Sigma\vert )$ veya geçişler sözlükle tutulduğunda beklenen $O(n)$ zamanda oluşturabilir.

| Yöntem | Zaman | Bellek | Farklı palindromları saklar mı? |
|---|---:|---:|---|
| Kaba kuvvet | $O(n^3)$ | $O(1)$ | Hayır |
| Merkezden genişletme | $O(n^2)$ | $O(1)$ | Ek yapı gerekir |
| Manacher algoritması | $O(n)$ | $O(n)$ | Doğrudan saklamaz |
| Eertree | $O(n)$ beklenen | $O(n)$ | Evet |

## Ağacın düğümleri neyi temsil eder?

Eertree'deki her normal düğüm, metinde bulunan farklı bir palindromu temsil eder. Bir palindroma iki taraftan aynı karakter eklenebiliyorsa yeni bir düğüme geçilir. Örneğin `a` palindromunun iki yanına `b` eklenmesi `bab` sonucunu üretir.

Yapı iki özel kök düğümle başlar:

- Uzunluğu `-1` olan hayali kök, tek uzunluklu palindromların kurulmasını kolaylaştırır.
- Uzunluğu `0` olan kök, çift uzunluklu palindromların temelidir.

Her düğüm ayrıca bir **suffix link** taşır. Bu bağlantı, ilgili palindromun kendisinden kısa olan en uzun palindromik son ekini gösterir. Örneğin `ababa` düğümünün suffix link'i `aba` düğümüne gider. Bu fikir, KMP algoritmasındaki başarısızlık bağlantılarını biraz andırır.

Bir metnin en fazla $n$ farklı palindromik alt metni olabilir. İki özel kökle birlikte düğüm sayısı en fazla $n+2$ olur. Eertree'nin şaşırtıcı derecede az bellek tüketmesinin sırrı budur.

## Orta düzey bir C++ uygulaması

Aşağıdaki yapı, karakterler geldikçe uygun palindromik son eki bulur ve daha önce görülmemişse yeni bir düğüm oluşturur:

```cpp
struct Node {
    int len, link, count;
    unordered_map<char, int> next;
    Node(int length) : len(length), link(0), count(0) {}
};

struct Eertree {
    string text;
    vector<Node> tree;
    int suffix;

    Eertree() : tree{Node(-1), Node(0)}, suffix(1) {
        tree[0].link = 0;
        tree[1].link = 0;
    }

    void add(char c) {
        text += c;
        int pos = static_cast<int>(text.size()) - 1;
        int current = suffix;

        while (pos - 1 - tree[current].len < 0 ||
               text[pos - 1 - tree[current].len] != c)
            current = tree[current].link;

        if (tree[current].next.count(c)) {
            suffix = tree[current].next[c];
            tree[suffix].count++;
            return;
        }

        tree.emplace_back(tree[current].len + 2);
        int created = static_cast<int>(tree.size()) - 1;
        tree[current].next[c] = created;
        tree[created].count = 1;

        if (tree[created].len == 1) {
            tree[created].link = 1;
        } else {
            int candidate = tree[current].link;
            while (pos - 1 - tree[candidate].len < 0 ||
                   text[pos - 1 - tree[candidate].len] != c)
                candidate = tree[candidate].link;
            tree[created].link = tree[candidate].next[c];
        }
        suffix = created;
    }
};
```

`add` fonksiyonu önce yeni karakterle genişletilebilecek en uzun palindromik son eki arar. Geçiş zaten varsa yalnızca kullanım sayısını artırır; yoksa uzunluğu iki fazla olan yeni palindromu ekler. `count` değerleri suffix link'ler üzerinden uzun düğümlerden kısalara aktarılırsa her palindromun toplam görülme sayısı da hesaplanabilir.

## Ne zaman kullanılmalı?

Eertree; farklı palindromları sayma, en uzun palindromik son eki izleme, çevrim içi karakter ekleme ve palindrom görülme sıklıklarını hesaplama problemlerinde parıldar. Yalnızca her merkezdeki palindrom yarıçapı gerekiyorsa Manacher daha sade olabilir. Fakat palindromların kendileri arasında bağlantılar kurmak istiyorsanız Eertree, metnin simetri arşivini tutan küçük ama güçlü bir kütüphaneci gibidir.
