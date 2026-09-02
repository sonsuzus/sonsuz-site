---
layout: post
title: "2-SAT Problemlerini Çizgelerle Çözmek: Mantıktan Güçlü Bileşenlere"
math: true
categories: 
  - Bilgi
tags: 
  - 2-sat
  - çizge teorisi
  - algoritmalar
toc: true
---

Bazı problemlerde seçenekler yalnızca doğru veya yanlış olabilir; fakat seçenekler arasındaki koşullar işleri hızla karıştırır. “Ali gelirse Ayşe gelmesin” ya da “Sunucu A çalışmıyorsa B mutlaka çalışsın” gibi kuralların tümünü aynı anda sağlayan bir durum arıyorsak karşımızda büyük olasılıkla bir **2-SAT** problemi vardır. Güzel haber şu: Bu mantık bulmacası, çizgeler sayesinde doğrusal zamanda çözülebilir.
``
2-SAT, Boolean değişkenlerinden oluşan ve her koşulunda en fazla iki ifade bulunan bir sağlanabilirlik problemidir. Genel biçimi şöyledir:

$$(a \lor b) \land (\neg c \lor d) \land (\neg a \lor \neg d)$$

Burada her parantez bir **clause**, yani koşuldur. $a \lor b$ koşulu, “a veya b ifadelerinden en az biri doğru olmalı” demektir. İfadelerden biri diğerini dışlayabilir, zorunlu kılabilir veya ikisi aynı anda seçilemez olabilir.

## Mantıksal koşuldan çıkarıma

Çözümün temelindeki numara, bir OR koşulunu iki çıkarıma dönüştürmektir:

$$a \lor b \equiv (\neg a \Rightarrow b) \land (\neg b \Rightarrow a)$$

Yani $a$ yanlışsa $b$ doğru olmak zorundadır; $b$ yanlışsa da $a$ doğru olmalıdır. Her literal için bir düğüm oluşturup bu çıkarımları yönlü kenarlar hâlinde eklediğimiz yapıya **çıkarım çizgesi** denir.

| Mantıksal koşul | Anlamı | Çizgeye eklenecek kenarlar |
|---|---|---|
| $a \lor b$ | En az biri doğru | $\neg a \to b$, $\neg b \to a$ |
| $\neg a \lor b$ | a doğruysa b doğru | $a \to b$, $\neg b \to \neg a$ |
| $\neg a \lor \neg b$ | İkisi birlikte doğru olamaz | $a \to \neg b$, $b \to \neg a$ |
| $a \lor a$ | a zorunlu | $\neg a \to a$ |

## Güçlü bağlı bileşenler neden önemli?

Yönlü bir çizgede iki düğüm birbirine karşılıklı ulaşabiliyorsa aynı **güçlü bağlı bileşen** içindedir. Bir değişken $x$ ile karşıtı $\neg x$ aynı bileşende bulunursa şu çelişki oluşur:

$$x \Rightarrow \neg x \quad \text{ve} \quad \neg x \Rightarrow x$$

Başka bir deyişle, $x$ seçildiğinde yanlış olması; yanlış seçildiğinde ise doğru olması zorunludur. Böyle bir durumda bütün koşulları sağlayan bir atama yoktur. Aksi hâlde formül çözülebilir.

Tarjan veya Kosaraju algoritmasıyla güçlü bağlı bileşenler $O(V+E)$ zamanda bulunabilir. 2-SAT çizgesinde her değişken için iki düğüm ve her clause için iki kenar bulunduğundan toplam karmaşıklık $O(n+m)$ olur.

## Python ile uygulama

Aşağıdaki kod Kosaraju algoritmasını kullanır. Literal’ler tam sayı olarak gösterilir: `1`, birinci değişkeni; `-1` ise onun değillemesini temsil eder.

```python
def two_sat(n, clauses):
    size = 2 * n
    graph = [[] for _ in range(size)]
    reverse = [[] for _ in range(size)]

    def node(x):
        v = abs(x) - 1
        return 2 * v + (x < 0)

    def add_edge(a, b):
        graph[a].append(b)
        reverse[b].append(a)

    for a, b in clauses:
        add_edge(node(-a), node(b))
        add_edge(node(-b), node(a))

    visited, order = [False] * size, []

    def dfs(v):
        visited[v] = True
        for u in graph[v]:
            if not visited[u]:
                dfs(u)
        order.append(v)

    for v in range(size):
        if not visited[v]:
            dfs(v)

    component = [-1] * size

    def assign(v, label):
        component[v] = label
        for u in reverse[v]:
            if component[u] == -1:
                assign(u, label)

    for v in reversed(order):
        if component[v] == -1:
            assign(v, v)

    for i in range(n):
        if component[2 * i] == component[2 * i + 1]:
            return False
    return True
```

Örneğin `two_sat(2, [(1, 2), (-1, 2), (-2, 1)])` çağrısı, koşulların birlikte sağlanabildiğini bildirir. Kod önce çıkarım çizgesini kurar, ardından bileşenleri hesaplar ve her değişkeni karşıtıyla karşılaştırır.

2-SAT; ders programı hazırlama, özellik seçimi, kaynak yerleştirme ve karşılıklı dışlayan yapılandırmaları denetleme gibi alanlarda kullanılır. Özetle yöntem şudur: Koşulları çıkarımlara çevir, çizgeyi kur, güçlü bağlı bileşenleri bul ve hiçbir değişkenin kendi değiliyle aynı bileşende olmadığını kontrol et. Mantık karmaşık görünse de çizge doğru hikâyeyi anlatır.
