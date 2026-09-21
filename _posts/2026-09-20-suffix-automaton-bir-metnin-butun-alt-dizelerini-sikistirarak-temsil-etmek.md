---
layout: post
title: "Suffix Automaton: Bir Metnin Bütün Alt Dizelerini Sıkıştırarak Temsil Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - suffix-automaton
  - algoritma
  - string
  - otomata
  - dinamik-programlama
toc: true
image: /img/suffix-automaton-bir-13.png
---

Elimizde uzun bir metin olduğunu ve bu metindeki bütün **bitişik alt dizeleri** saklamak istediğimizi düşünelim. Uzunluğu $n$ olan bir metin, en fazla $n(n+1)/2$ farklı konum aralığı içerir. Hepsini ayrı ayrı depolamak karesel bir felakete dönüşebilir. Suffix Automaton, yani son ek otomatı, aynı bilgiyi yalnızca $O(n)$ durum ve geçişle temsil eden zarif bir veri yapısıdır.

![suffix-automaton-bir-13](/img/suffix-automaton-bir-13.svg)

``
## Temel fikir

Suffix Automaton, bir metnin bütün alt dizelerini kabul eden **deterministik sonlu otomatın sıkıştırılmış biçimidir**. Buradaki alt dize, karakterlerin metinde yan yana bulunduğu parçadır; subsequence gibi karakter atlamaya izin verilmez.

Her durum, metin içinde aynı bitiş konumları kümesine sahip alt dizeleri temsil eder. Bu kümeye `endpos` denir. Örneğin `ababa` içinde `ab` alt dizesi 2. ve 4. indekslerde bitiyorsa, bu konumlar onun `endpos` kümesini oluşturur. Aynı `endpos` kümesine sahip alt dizeler tek durumda birleşerek sıkıştırmayı sağlar.

Bir durum $v$ için iki önemli değer vardır:

- $len[v]$: Bu durumun temsil ettiği en uzun alt dizenin uzunluğu.
- $link[v]$: En uzun uygun son eki temsil eden duruma bağlantı.

Durumun temsil ettiği en kısa alt dizenin uzunluğu ise:

$$minlen(v) = len[link[v]] + 1$$

Dolayısıyla bir durumun temsil ettiği farklı uzunluk sayısı:

$$len[v] - len[link[v]]$$

Bu formül, farklı alt dizeleri saymanın anahtarıdır.

## Trie ile karşılaştırma

| Özellik | Suffix Trie | Suffix Automaton |
|---|---:|---:|
| Durum sayısı | $O(n^2)$ | En fazla $2n-1$ |
| Kurulum süresi | Genellikle $O(n^2)$ | $O(n)$ |
| Alt dize sorgusu | $O(m)$ | $O(m)$ |
| Bellek kullanımı | Yüksek | Düşük |
| Yapı karakteri | Ağaç | Yönlü döngüsüz grafik |

Otomatın grafiği `len` değerleri bakımından daima ileri gider. Bu nedenle durumları `len` sırasına koyarak dinamik programlama yapmak oldukça kolaydır.

## Çevrim içi kurulum ve klonlar

Metin soldan sağa işlenir. Her yeni karakter geldiğinde yeni bir `cur` durumu oluşturulur. Önceki durumlar üzerinden bu karaktere ait eksik geçişler eklenir. Bazen mevcut bir geçiş doğrudan bağlanamayacak kadar fazla bilgi taşır. İşte bu noktada bir **clone** oluşturulur.

Klon, hedef durumun geçişlerini ve suffix linkini kopyalar; ancak daha kısa bir `len` değeri alır. Böylece farklı `endpos` sınıfları doğru biçimde ayrılır. Biraz bilim kurgu gibi görünse de klonlama, otomatın minimal kalmasını sağlayan mekanizmadır.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct State {
    int len = 0, link = -1;
    map<char, int> next;
};

vector<State> st(1);
int last = 0;

void extendSAM(char c) {
    int cur = st.size();
    st.push_back({st[last].len + 1, 0, {}});
    int p = last;

    while (p != -1 && !st[p].next.count(c)) {
        st[p].next[c] = cur;
        p = st[p].link;
    }

    if (p == -1) {
        st[cur].link = 0;
    } else {
        int q = st[p].next[c];
        if (st[p].len + 1 == st[q].len) {
            st[cur].link = q;
        } else {
            int clone = st.size();
            st.push_back(st[q]);
            st[clone].len = st[p].len + 1;

            while (p != -1 && st[p].next[c] == q) {
                st[p].next[c] = clone;
                p = st[p].link;
            }
            st[q].link = st[cur].link = clone;
        }
    }
    last = cur;
}
```

Bu kod her karakteri otomata ekler. Alfabe sabitse `map` yerine dizi kullanmak geçişleri hızlandırabilir; `map` ise örneği daha genel tutar.

## Neler hesaplanabilir?

Farklı alt dize sayısı doğrudan şu toplamla bulunur:

$$\sum_{v \ne root} (len[v] - len[link[v]])$$

Bir desenin metinde bulunup bulunmadığını öğrenmek için kökten başlayıp karakter geçişlerini izlemek yeterlidir. Geçiş kaybolursa desen yoktur. Ayrıca durumların görülme sayılarını uzunluktan küçüğe doğru suffix linklere aktararak alt dizelerin kaç kez geçtiği bulunabilir.

Suffix Automaton; en uzun ortak alt dize, sözlük sırasındaki $k$'ıncı alt dize ve tekrar eden parçaların analizi gibi problemlerde de güçlüdür. İlk bakışta linkler ve klonlar ürkütücü olabilir; fakat özünde yaptığı şey basittir: Aynı geleceğe ve aynı bitiş davranışına sahip alt dizeleri tek bir durumda toplamak.
