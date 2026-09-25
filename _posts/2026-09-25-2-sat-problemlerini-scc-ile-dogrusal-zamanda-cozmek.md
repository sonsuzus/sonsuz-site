---
layout: post
title: "2-SAT Problemlerini SCC ile Doğrusal Zamanda Çözmek"
math: true
categories: 
  - Bilgi
tags: 
  - 2-sat
  - graf teorisi
  - güçlü bağlı bileşenler
  - algoritma
  - kosaraju
  - mantıksal kısıtlamalar
toc: true
image: /img/2-sat-problemlerini-73.png
---

Bir festivalde her etkinlik için “yapılsın” veya “yapılmasın” kararı verdiğimizi düşünelim. Kurallar ise “Konser yapılacaksa güvenlik ekibi gelsin” ya da “Ya konser ya tiyatro seçilsin” biçiminde olsun. Binlerce ikili karar birbirine bağlandığında deneme-yanılma yaklaşımı hızla çöker. 2-SAT, tam da bu tür sistemlerin çözülebilirliğini yönlü grafikler ve güçlü bağlı bileşenler sayesinde zarifçe belirler.

``

## 2-SAT nedir?

2-SAT formülleri, her parantezinde en fazla iki literal bulunan ve bağlaçlarla birleştirilen ifadelerdir:

$$
(x_1 \lor \neg x_2) \land (x_2 \lor x_3) \land (\neg x_1 \lor \neg x_3)
$$

Literal, bir değişkenin kendisi ($x$) veya değili ($\neg x$) olabilir. Genel bir madde $(a \lor b)$ biçimindedir. Bu ifade yalnızca $a$ ve $b$ birlikte yanlış olduğunda bozulur. Dolayısıyla şu iki zorunluluğu türetebiliriz:

$$
(a \lor b) \equiv (\neg a \Rightarrow b) \land (\neg b \Rightarrow a)
$$

Her zorunluluğu yönlü bir kenara dönüştürürsek **implikasyon grafiği** ortaya çıkar.

| Mantıksal kısıt | Grafiğe eklenen kenarlar |
|---|---|
| $a \lor b$ | $\neg a \to b$, $\neg b \to a$ |
| $a \Rightarrow b$ | $a \to b$, $\neg b \to \neg a$ |
| $a$ doğru olmalı | $\neg a \to a$ |
| $a$ ve $b$ eşit | $a \to b$, $b \to a$, $\neg a \to \neg b$, $\neg b \to \neg a$ |

## SCC neden çözümü belirliyor?

Bir güçlü bağlı bileşende, her düğümden diğer bütün düğümlere ulaşılabilir. Eğer $x$ ile $\neg x$ aynı SCC içindeyse hem $x \Rightarrow \neg x$ hem de $\neg x \Rightarrow x$ geçerlidir. Hangi doğruluk değerini seçersek seçelim sistem tersini de zorlar; formül çözülemez.

Böylece temel ölçüt şudur:

$$
\text{Formül çözülebilir} \iff \forall x_i,\ SCC(x_i) \ne SCC(\neg x_i)
$$

Bu, yönlü döngülerin mantıksal çelişkiyi görünür hâle getirmesidir. SCC’ler Tarjan veya Kosaraju algoritmasıyla $O(V+E)$ zamanda bulunur. $n$ değişken ve $m$ madde için grafikte $2n$ düğüm, $2m$ kenar bulunduğundan toplam karmaşıklık $O(n+m)$ olur.

| Yaklaşım | Zaman | Büyük girdilerde durum |
|---|---:|---|
| Tüm atamaları denemek | $O(2^n)$ | Hızla kullanılamaz |
| SCC tabanlı 2-SAT | $O(n+m)$ | Milyonlarca kısıta uygundur |

## Kosaraju ile uygulama

Aşağıdaki C++ kodu, pozitif literali `2*x`, negatifini `2*x+1` ile temsil eder. `p^1` işlemi bir literalden karşıtına geçer. İlk DFS bitiş sırasını, ikinci DFS ise ters grafikte bileşenleri üretir.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TwoSAT {
    int n;
    vector<vector<int>> g, rg;
    vector<int> order, comp, used;

    TwoSAT(int n) : n(n), g(2*n), rg(2*n),
                    comp(2*n, -1), used(2*n) {}

    // (a OR b) maddesini implikasyon grafiğine ekler.
    void addClause(int a, int b) {
        g[a ^ 1].push_back(b);
        rg[b].push_back(a ^ 1);
        g[b ^ 1].push_back(a);
        rg[a].push_back(b ^ 1);
    }

    void dfs1(int v) {
        used[v] = 1;
        for (int u : g[v]) if (!used[u]) dfs1(u);
        order.push_back(v);
    }

    void dfs2(int v, int id) {
        comp[v] = id;
        for (int u : rg[v]) if (comp[u] == -1) dfs2(u, id);
    }

    bool solve(vector<bool>& value) {
        for (int v = 0; v < 2*n; ++v)
            if (!used[v]) dfs1(v);

        reverse(order.begin(), order.end());
        int id = 0;
        for (int v : order)
            if (comp[v] == -1) dfs2(v, id++);

        value.resize(n);
        for (int x = 0; x < n; ++x) {
            if (comp[2*x] == comp[2*x+1]) return false;
            value[x] = comp[2*x] > comp[2*x+1];
        }
        return true;
    }
};
```

`solve`, çelişki yoksa örnek bir doğruluk ataması da üretir. Bileşen numaralarına göre yapılan karşılaştırma, SCC’lerin yoğunlaştırılmış grafiğindeki ters topolojik sıradan yararlanır.

Sonuç olarak 2-SAT’ın gücü, mantığı kaba kuvvetle çözmek yerine onu erişilebilirlik problemine dönüştürmesinden gelir. Bir değişken kendi değiliyle aynı yönlü döngünün içine hapsolmuşsa çelişki kaçınılmazdır; aksi durumda bileşen sırası tutarlı bir atamayı doğrudan verir.

![2-sat-problemlerini-73](/img/2-sat-problemlerini-73.svg)

