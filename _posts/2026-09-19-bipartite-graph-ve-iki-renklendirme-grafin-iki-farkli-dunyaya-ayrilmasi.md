---
layout: post
title: "Bipartite Graph ve İki-Renklendirme: Grafın İki Farklı Dünyaya Ayrılması"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - bipartite graph
  - iki renklendirme
  - algoritma
  - python
  - bfs
toc: true
---

Bir partide herkesin iki gruptan yalnızca karşı gruptakilerle iletişim kurduğunu düşünün. Aynı gruptaki hiç kimse birbiriyle konuşmuyor! Kulağa biraz tuhaf gelse de bu düzen, graf teorisindeki **bipartite graph**, yani **iki parçalı graf** kavramını mükemmel biçimde anlatır. Üstelik bu graflar; eşleştirme, görev dağıtımı ve sosyal ağ analizi gibi birçok gerçek problemde karşımıza çıkar.

``

## İki parçalı graf nedir?

Bir grafın düğüm kümesi, kendi içinde bağlantı bulunmayan iki ayrı kümeye bölünebiliyorsa bu graf iki parçalıdır. Başka bir ifadeyle $G=(V,E)$ grafında düğümler $A$ ve $B$ kümelerine ayrılabiliyorsa şu koşullar sağlanır:

$$V=A ∪ B, \quad A ∩ B=∅$$

Her $(u,v) ∈ E$ kenarı için düğümlerden biri $A$, diğeri $B$ kümesinde bulunmalıdır. Dolayısıyla aynı kümedeki iki düğüm arasında kenar olamaz.

Örneğin öğrenciler ile projeleri modelleyen bir graf düşünelim. Öğrenciler bir tarafta, projeler diğer tarafta yer alır. Bir öğrencinin ilgilendiği projeye kenar çizilir. İki öğrenci veya iki proje doğrudan bağlanmadığı için ortaya doğal bir bipartite graph çıkar.

## İki-renklendirme bağlantısı

Bir grafın iki parçalı olup olmadığını anlamanın en kullanışlı yolu **iki-renklendirme** yapmaktır. Her düğüme kırmızı veya mavi renk veririz. Bir kenarın iki ucunun aynı renkte olmaması gerekir.

Bunu matematiksel olarak $c:V→\{0,1\}$ fonksiyonuyla gösterebiliriz. Her $(u,v) ∈ E$ kenarı için:

$$c(u) ≠ c(v)$$

koşulu sağlanıyorsa graf iki parçalıdır. Buradaki renklerin gerçek bir anlamı yoktur; yalnızca düğümlerin hangi dünyaya ait olduğunu gösteren etiketlerdir.

| Özellik | Bipartite graf | Bipartite olmayan graf |
|---|---|---|
| İki renkle boyanabilir mi? | Evet | Hayır |
| Aynı grupta kenar olabilir mi? | Hayır | Olabilir |
| Tek uzunluklu döngü içerir mi? | Hayır | En az bir tane içerir |
| Tipik örnek | Öğrenci–proje ağı | Üçgen graf |

Buradaki en önemli teorik sonuç şudur: **Bir graf ancak ve ancak tek sayıda kenardan oluşan bir döngü içermiyorsa iki parçalıdır.** Örneğin üç düğümlü bir üçgende ilk düğümü kırmızı, ikincisini mavi yaparız. Üçüncü düğüm hem kırmızıya hem maviye bağlı olduğundan uygun renk kalmaz. Algoritma adeta “Renkler bitti!” diye alarm verir.

## BFS ile kontrol algoritması

Kontrol işlemi için genişlik öncelikli arama, yani BFS kullanılabilir. Başlangıç düğümünü bir renge boyar, komşularına ters rengi veririz. Daha önce boyanmış bir komşunun rengi mevcut düğümle aynıysa graf iki parçalı değildir.

Graf bağlantısız olabileceği için yalnızca tek düğümden BFS başlatmak yeterli değildir. Henüz boyanmamış her düğüm için işlem tekrarlanmalıdır.

```python
from collections import deque

def is_bipartite(graph):
    colors = {}

    for start in graph:
        if start in colors:
            continue

        colors[start] = 0
        queue = deque([start])

        while queue:
            node = queue.popleft()

            for neighbor in graph[node]:
                if neighbor not in colors:
                    # Komşuyu karşı gruba yerleştir.
                    colors[neighbor] = 1 - colors[node]
                    queue.append(neighbor)
                elif colors[neighbor] == colors[node]:
                    # Aynı renkte komşular varsa ayrım mümkün değildir.
                    return False, {}

    return True, colors

network = {
    "Ayşe": ["Proje A", "Proje B"],
    "Mehmet": ["Proje B"],
    "Proje A": ["Ayşe"],
    "Proje B": ["Ayşe", "Mehmet"]
}

print(is_bipartite(network))
```

BFS her düğümü ve kenarı en fazla sabit sayıda inceler. Bu nedenle zaman karmaşıklığı $O(\vert V\vert +\vert E\vert )$, renk tablosu ve kuyruk nedeniyle alan karmaşıklığı ise $O(\vert V\vert )$ olur.

## Nerelerde kullanılır?

İki parçalı graflar çalışan–görev, kullanıcı–ürün, doktor–vardiya ve aday–iş eşleştirmelerinde kullanılır. Ayrıca maksimum eşleştirme algoritmalarının teorik temelini oluştururlar. Kısacası iki-renklendirme yalnızca düğümleri boyayan sevimli bir işlem değildir; karmaşık ilişkileri iki tutarlı dünyaya ayıran güçlü ve verimli bir modelleme aracıdır.
