---
layout: post
title: "Palindromic Tree: Bütün Palindromları Tek Yapıda Toplamak"
math: true
categories: 
  - Bilgi
tags: 
  - palindrom
  - eertree
  - veri yapıları
  - algoritma
  - c++
  - metin işleme
toc: true
---

Bir metindeki bütün palindromları bulmak ilk bakışta kolay görünür: Her merkezi seç, iki yana doğru genişle ve eşleşmeler bitene kadar devam et. Fakat metin uzadığında ve aynı palindromlar tekrar tekrar karşımıza çıktığında işler karışır. **Palindromic Tree**, diğer adıyla **Eertree**, farklı palindromları tek bir yapıda saklayarak bu karmaşayı oldukça zarif biçimde çözer.

``

## Eertree nedir?

Eertree, bir metinde bulunan her **farklı palindromik alt dizeyi** bir düğüm olarak temsil eden veri yapısıdır. İsmi ağaç olsa da teknik olarak bağlantıları bulunan yönlü bir grafiğe daha yakındır. Yapı, metnin karakterleri soldan sağa eklenirken çevrim içi olarak oluşturulabilir.

Her düğümde genellikle şu bilgiler tutulur:

- Palindromun uzunluğu,
- En uzun uygun palindromik son ekine giden bağlantı,
- Yeni karakterlerle oluşabilecek palindromlara giden kenarlar,
- Palindromun metinde kaç defa görüldüğü.

Eertree iki özel kök düğümle başlar. Birinin uzunluğu $0$, diğerinin uzunluğu $-1$ kabul edilir. Sıfır uzunluklu kök çift uzunluklu, eksi bir uzunluklu hayali kök ise tek uzunluklu palindromların kurulmasını kolaylaştırır. $-1$ ilk bakışta matematik öğretmenini kızdırabilir, ama sınır kontrollerini sadeleştiren kullanışlı bir numaradır.

## Temel çalışma mantığı

Yeni bir $c$ karakteri eklendiğinde, önce önceki konumda biten en uzun palindromik son eke bakılır. Bu palindromun solundaki karakter de $c$ ise iki uca $c$ eklenerek daha uzun bir palindrom elde edilir:

$$P_{yeni} = c + P_{eski} + c$$

Eşleşme yoksa düğümün **suffix link** bağlantısı takip edilir. Uygun palindrom bulunana kadar bu işlem sürer. Oluşan palindrom daha önce eklenmişse yalnızca görülme sayısı artırılır; yeni ise yeni bir düğüm oluşturulur.

Örneğin `ababa` metninde düğümler `a`, `b`, `aba`, `bab` ve `ababa` palindromlarını temsil eder. Aynı `a` üç kez geçse bile üç ayrı düğüm oluşturulmaz.

| Yaklaşım | Süre | Bellek | Farklı palindromları saklama |
|---|---:|---:|---|
| Merkezden genişleme | $O(n^2)$ | $O(1)$ | Ek yapı gerekir |
| Manacher algoritması | $O(n)$ | $O(n)$ | Doğrudan sağlamaz |
| Palindromic Tree | $O(n)$ | $O(n\sigma)$ veya seyrek kenarlar | Doğrudan sağlar |

Buradaki $\sigma$, alfabenin büyüklüğüdür. Harita kullanılırsa yalnızca mevcut kenarlar saklanabilir.

## Orta düzey bir C++ uygulaması

Aşağıdaki uygulama küçük İngiliz alfabesi için farklı palindromları oluşturur. `addChar`, yeni karakterin tamamladığı en uzun palindromu bulur ve gerekiyorsa düğüm ekler.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Node {
    int len, link, count;
    array<int, 26> next{};
    Node(int length = 0) : len(length), link(0), count(0) {}
};

class Eertree {
    vector<Node> tree;
    string text;
    int last;

public:
    Eertree() {
        tree.emplace_back(-1); // Hayali tek uzunluklu kök
        tree.emplace_back(0);  // Boş palindrom kökü
        tree[0].link = 0;
        tree[1].link = 0;
        text = "#";
        last = 1;
    }

    void addChar(char ch) {
        text += ch;
        int pos = (int)text.size() - 1;
        int current = last;

        while (text[pos - tree[current].len - 1] != ch)
            current = tree[current].link;

        int edge = ch - 'a';
        if (tree[current].next[edge]) {
            last = tree[current].next[edge];
            tree[last].count++;
            return;
        }

        tree.emplace_back(tree[current].len + 2);
        int created = (int)tree.size() - 1;
        tree[current].next[edge] = created;
        tree[created].count = 1;

        if (tree[created].len == 1) {
            tree[created].link = 1;
        } else {
            int candidate = tree[current].link;
            while (text[pos - tree[candidate].len - 1] != ch)
                candidate = tree[candidate].link;
            tree[created].link = tree[candidate].next[edge];
        }

        last = created;
    }

    int distinctCount() const {
        return (int)tree.size() - 2;
    }
};
```

Her ekleme sırasında suffix link zincirinde geriye gidilebilir; ancak toplam ilerleme amortize edildiğinde yapının oluşturulması $O(n)$ zamanda tamamlanır. Bir metnin en fazla $n$ farklı palindromik alt dizesi olabileceği için düğüm sayısı da $O(n)$ olur.

Eertree; palindrom sayma, en uzun palindromik son eki bulma, tekrar sıklıklarını hesaplama ve dinamik metin sorguları gibi problemlerde parıldar. Manacher yalnızca uzunluklarla ilgilenirken Eertree palindromların kimliklerini ve aralarındaki ilişkileri korur. Kısacası, palindrom koleksiyonunuzu çekmecelere ayırmak istiyorsanız Eertree oldukça düzenli bir dolaptır.
