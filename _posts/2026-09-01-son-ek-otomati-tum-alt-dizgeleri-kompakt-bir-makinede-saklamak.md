---
layout: post
title: "Son Ek Otomatı: Tüm Alt Dizgeleri Kompakt Bir Makinede Saklamak"
math: true
categories: 
  - Bilgi
tags: 
  - suffix-automaton
  - string-algorithms
  - competitive-programming
toc: true
---

Bir metnin bütün **ardışık alt dizgelerini** saklamak istediğimizi düşünelim. İlk fikir, her alt dizgeyi ayrı ayrı üretmek olabilir; ancak uzunluğu $n$ olan bir dizgenin $O(n^2)$ farklı konumu vardır. Son Ek Otomatı, diğer adıyla **Suffix Automaton (SAM)**, bu devasa koleksiyonu en fazla $2n-1$ durum kullanarak temsil eden deterministik ve yönsüz döngüsüz bir otomattır. Kısacası bütün alt dizgeleri cebine koyar, ama valiz parası ödemez.
``
## Temel fikir: Durumlar neyi temsil eder?

SAM içindeki her yol, kaynak metinde geçen bir alt dizgeye karşılık gelir. Başlangıç durumundan karakter geçişlerini takip ederek bir kelimeyi okuyabiliyorsak o kelime metnin içinde bulunur.

Fakat her alt dizge için ayrı durum oluşturulmaz. Aynı bitiş konumları kümesine sahip alt dizgeler tek bir durumda gruplanır. Bu kümeye **endpos** denir. Örneğin iki farklı alt dizge metinde daima aynı konumlarda bitiyorsa otomata açısından eşdeğerdir.

Her durum için iki kritik bilgi tutulur:

- `len[v]`: Durumun temsil ettiği en uzun alt dizgenin uzunluğu.
- `link[v]`: Bu alt dizgenin farklı bir endpos sınıfına ait en uzun son ekini gösteren bağlantı.

Bir durumun temsil ettiği alt dizge uzunlukları şu aralıktadır:

$$len[link[v]] + 1 \leq L \leq len[v]$$

Dolayısıyla durum `v`, tam olarak $len[v]-len[link[v]]$ adet farklı alt dizgeyi temsil eder.

| Yapı | Durum sayısı | Kurulum | Tipik kullanım |
|---|---:|---:|---|
| Trie | $O(n^2)$ | $O(n^2)$ | Açık biçimde kelime saklama |
| Suffix Array | $O(n)$ | $O(n \log n)$ veya $O(n)$ | Sıralı son ek sorguları |
| Suffix Automaton | En fazla $2n-1$ | $O(n)$ | Alt dizge arama ve sayma |

## Otomat nasıl büyütülür?

Metin soldan sağa işlenir. Yeni karakter geldiğinde önce `cur` adlı yeni bir durum açılır. Önceki son durumdan başlayarak bu karaktere geçişi bulunmayan durumlara geçiş eklenir.

Bazen mevcut bir geçiş, uzunluk koşulunu bozacak bir duruma çıkar. İşte sahneye **clone** girer: Hedef durumun geçişleri ve suffix link’i kopyalanır, fakat uzunluğu uygun değere indirilir. İlgili geçişler clone’a yönlendirilir. Clone yeni bir metin parçası eklemez; yalnızca endpos sınıflarını doğru biçimde ayırır.

```cpp
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

Kod, her karakteri amortize $O(1)$ zamanda işler; `map` kullanıldığında alfabe erişimi nedeniyle pratik karmaşıklık $O(n \log \vert \Sigma\vert )$ olur. Sabit alfabelerde dizi kullanarak doğrusal süre elde edilebilir.

## Yarışmalarda hangi işleri çözer?

Bir desenin metinde bulunup bulunmadığını anlamak için başlangıçtan itibaren karakter geçişleri takip edilir. Bir geçiş eksikse desen yoktur; tüm karakterler okunursa vardır. Sorgu maliyeti desen uzunluğu $m$ için $O(m)$ olur.

Farklı alt dizge sayısı ise doğrudan hesaplanabilir:

$$\sum_{v \neq root} (len[v]-len[link[v]])$$

Durumlara oluşma sırasına göre katkı aktarılarak alt dizgelerin kaç kez geçtiği de bulunabilir. Ayrıca en uzun ortak alt dizge, sözlük sırasındaki $k$’ıncı alt dizge ve minimum döndürme gibi problemler SAM üzerinde çözülebilir.

Özetle Son Ek Otomatı; trie’ın ifade gücünü, güçlü suffix bağlantılarını ve doğrusal boyutu bir araya getirir. Clone mekanizması ilk bakışta ürkütse de temel soru hep aynıdır: “Bu alt dizgeler aynı bitiş konumlarını mı paylaşıyor?” Bu fikir oturduğunda SAM, yarışma çantanızdaki en etkili metin araçlarından birine dönüşür.
