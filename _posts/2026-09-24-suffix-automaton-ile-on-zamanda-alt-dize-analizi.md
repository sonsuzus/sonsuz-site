---
layout: post
title: "Suffix Automaton ile O(N) Zamanda Alt Dize Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - suffix-automaton
  - algoritma
  - string
  - c++
  - dinamik-programlama
  - metin-işleme
toc: true
image: /img/suffix-automaton-ile-87.png
---

![suffix-automaton-ile-87](/img/suffix-automaton-ile-87.svg)


Bir metindeki farklı alt dizgileri tek tek saklamaya kalkarsak, kısa sürede bellek canavarı üretiriz. Uzunluğu $N$ olan bir dizginin $O(N^2)$ adet alt dizgi aralığı bulunabilir. **Suffix Automaton** ya da kısaca **SAM**, bütün bu alt dizgileri en fazla $2N-1$ durum kullanarak temsil eder ve soldan sağa tek geçişte, yani $O(N)$ zamanda kurulabilir.

``

## Suffix Automaton neyi temsil eder?

Suffix Automaton, verilen metnin tüm alt dizgilerini kabul eden deterministik sonlu otomattır. Adındaki “suffix” biraz yanıltıcı olabilir: Yapı yalnızca son ekleri değil, **bütün alt dizgileri** temsil eder. Bunun nedeni, her alt dizginin metnin bir ön ekinin son eki olarak düşünülebilmesidir.

Her durum, aynı bitiş konumları kümesine sahip alt dizgilerin oluşturduğu bir sınıfı temsil eder. Bu kümeye `endpos` denir. Bir durumun temel bileşenleri şöyledir:

| Alan | Anlamı |
|---|---|
| `len` | Durumun temsil ettiği en uzun alt dizginin uzunluğu |
| `link` | Daha küçük bir `endpos` sınıfına giden suffix bağlantısı |
| `next` | Karakterlere göre geçişler |
| `occ` | İsteğe bağlı olarak görülme sayısı |

Bir `v` durumu tarafından temsil edilen alt dizgilerin uzunlukları şu aralıktadır:

$$len(link(v)) + 1 \le L \le len(v)$$

Dolayısıyla bu durumun farklı alt dizgi sayısına katkısı:

$$len(v) - len(link(v))$$

olur. Başlangıç durumu dışındaki tüm durumların katkılarını topladığımızda farklı alt dizgi sayısını elde ederiz.

## İnşa mantığı ve klon durumlar

Metni soldan sağa işlerken her yeni karakter için bir `cur` durumu oluşturulur. Önceki son durumdan suffix bağlantıları boyunca geriye gidilir ve eksik geçişler `cur` durumuna bağlanır.

Bazen mevcut bir `q` durumuna bağlanmak otomatonun uzunluk düzenini bozar. Eğer

$$len(p)+1 \ne len(q)$$

ise `q` kopyalanarak bir **clone** durumu oluşturulur. Clone aynı geçişlere ve suffix bağlantısına sahiptir; ancak `len` değeri gerekli sınıra çekilir. Ardından ilgili bağlantılar clone’a yönlendirilir. Clone, yeni bir metin oluşumunu değil, mevcut `endpos` sınıfının bölünmesini temsil eder.

| Yaklaşım | Kurulum | Durum/Bellek | Tipik kullanım |
|---|---:|---:|---|
| Tüm alt dizgileri kümede tutmak | $O(N^2)$ veya daha kötü | $O(N^2)$ | Küçük girdiler |
| Suffix Array | Genellikle $O(N \log N)$ | $O(N)$ | Sıralı suffix sorguları |
| Suffix Automaton | $O(N)$ | $O(N)$ | Alt dizgi ve tekrar analizi |

## C++ ile temel uygulama

Aşağıdaki kod otomatonu kurar ve farklı alt dizgi sayısını hesaplar:

```cpp
#include <bits/stdc++.h>
using namespace std;

struct State {
    int len = 0, link = -1;
    map<char, int> next;
};

vector<State> st(1);
int lastState = 0;

void extendSAM(char c) {
    int cur = st.size();
    st.push_back({st[lastState].len + 1, 0, {}});
    int p = lastState;

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
    lastState = cur;
}

long long distinctSubstrings() {
    long long answer = 0;
    for (int v = 1; v < (int)st.size(); ++v)
        answer += st[v].len - st[st[v].link].len;
    return answer;
}
```

`extendSAM`, yeni karakteri eklerken geçişleri ve suffix bağlantılarını günceller. `distinctSubstrings` ise her durumun temsil ettiği uzunluk aralığını toplar. `map` kullanımı nedeniyle pratik karmaşıklık alfabe erişimine bağlıdır; sabit boyutlu bir dizi veya `unordered_map` ile beklenen doğrusal çalışma elde edilebilir.

## Hangi problemleri çözer?

SAM ile bir desenin metinde bulunup bulunmadığı geçişler izlenerek $O(M)$ zamanda kontrol edilebilir. Ayrıca durumlara görülme sayıları eklenerek tekrar eden alt dizgiler, en uzun ortak alt dizgi ve belirli sayıda görülen parçalar bulunabilir.

Kısacası Suffix Automaton, karesel büyüyen alt dizgi evrenini doğrusal sayıda duruma sıkıştırır. İlk karşılaşmada clone mekanizması sihir gibi görünse de temel fikir nettir: Aynı bitiş davranışını paylaşan alt dizgileri tek durumda toplamak, davranış ayrıştığında ise sınıfı dikkatlice bölmek.
