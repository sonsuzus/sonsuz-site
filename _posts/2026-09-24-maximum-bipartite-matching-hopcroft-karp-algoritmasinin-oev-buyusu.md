---
layout: post
title: "Maximum Bipartite Matching: Hopcroft-Karp Algoritmasının O(E√V) Büyüsü"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - graf-teorisi
  - hopcroft-karp
  - maksimum-eşleşme
  - python
toc: true
image: /img/maximum-bipartite-matching-63.png
---

İşleri çalışanlara, öğrencileri projelere veya sürücüleri teslimatlara atamak istediğimizi düşünelim. Her aday yalnızca belirli seçeneklerle eşleşebiliyorsa problemimiz bir **iki parçalı graf eşleşmesi** problemine dönüşür. Tek tek eşleşme aramak kolay görünse de veri büyüdüğünde klasik yöntemler nefes nefese kalır. Hopcroft-Karp ise artırma yollarını toplu biçimde işleyerek sahneye çıkar ve karmaşıklığı $O(E\sqrt{V})$ seviyesine indirir.
``

## Önce problemi modelleyelim

İki parçalı bir grafın düğümleri, kendi içlerinde bağlantı bulunmayan iki ayrık kümeye bölünür: $U$ ve $V$. Her kenar, $U$ kümesindeki bir düğümü $V$ kümesindeki bir düğüme bağlar.

Bir **eşleşme**, ortak uç paylaşmayan kenarlar kümesidir. Amaç, seçilen kenar sayısını mümkün olduğunca artırmaktır. Örneğin bir geliştirici aynı anda yalnızca bir projeye, bir proje de yalnızca bir geliştiriciye atanabiliyorsa seçilen atamalar eşleşme oluşturur.

$$M^* = \arg\max_M \vert M\vert $$

Burada $M^*$ maksimum eşleşmeyi, $\vert M\vert $ ise eşleşmedeki kenar sayısını gösterir.

| Kavram | Anlamı | Günlük hayattaki karşılığı |
|---|---|---|
| Serbest düğüm | Henüz eşleşmemiş düğüm | Projesiz geliştirici |
| Eşleşmiş kenar | Mevcut atama | Geliştirici-proje bağlantısı |
| Artırma yolu | Kenar türleri dönüşümlü yol | Atamaları yeniden düzenleme planı |
| Maksimum eşleşme | Daha fazla büyütülemeyen en büyük sonuç | En çok kişiyi yerleştiren atama |

## Artırma yolunun sırrı

Bir **artırma yolu**, serbest bir düğümde başlayıp serbest bir düğümde biten; eşleşmemiş ve eşleşmiş kenarların dönüşümlü kullanıldığı yoldur. Bu yol üzerindeki kenarların durumunu tersine çevirirsek eşleşmenin boyutu tam olarak bir artar.

Basit yaklaşım, her turda DFS ile tek bir artırma yolu bulur. Bu yöntem en kötü durumda $O(VE)$ maliyetlidir. Hopcroft-Karp’ın numarası ise tek yol yerine aynı anda mümkün olduğunca çok sayıda, birbirinden bağımsız **en kısa artırma yolu** bulmasıdır.

| Yaklaşım | Bir turdaki davranış | Zaman karmaşıklığı |
|---|---|---|
| Klasik DFS | Tek artırma yolu bulur | $O(VE)$ |
| Hopcroft-Karp | En kısa yolları katmanlar hâlinde toplar | $O(E\sqrt{V})$ |

## BFS ve DFS takım oyunu

Algoritma iki aşamalı turlar çalıştırır:

1. **BFS**, serbest sol düğümlerden başlayarak katmanlı bir graf kurar ve en kısa artırma yollarının uzunluğunu belirler.
2. **DFS**, yalnızca bu katman düzenine uyan yolları izleyerek aynı turda birden fazla bağımsız artırma yolu çıkarır.
3. Yeni yol kalmayana kadar süreç tekrarlanır.

BFS gereksiz derin aramaları engellerken DFS bulunan yapıyı gerçek eşleşmelere dönüştürür. Bir fazın maliyeti $O(E)$, faz sayısı ise $O(\sqrt{V})$ ile sınırlıdır. Böylece:

$$O(E) \times O(\sqrt{V}) = O(E\sqrt{V})$$

## Python ile orta düzey uygulama

Aşağıdaki kod, sol küme için komşuluk listesi alır. `pair_u` ve `pair_v` mevcut eşleri, `dist` ise BFS katmanlarını saklar.

```python
from collections import deque

def hopcroft_karp(graph):
    pair_u = {u: None for u in graph}
    right = {v for neighbors in graph.values() for v in neighbors}
    pair_v = {v: None for v in right}
    dist = {}

    def bfs():
        queue = deque()
        path_exists = False
        for u in graph:
            if pair_u[u] is None:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = float('inf')

        while queue:
            u = queue.popleft()
            for v in graph[u]:
                partner = pair_v[v]
                if partner is None:
                    path_exists = True
                elif dist[partner] == float('inf'):
                    dist[partner] = dist[u] + 1
                    queue.append(partner)
        return path_exists

    def dfs(u):
        for v in graph[u]:
            partner = pair_v[v]
            if partner is None or (
                dist[partner] == dist[u] + 1 and dfs(partner)
            ):
                pair_u[u], pair_v[v] = v, u
                return True
        dist[u] = float('inf')
        return False

    matching = 0
    while bfs():
        for u in graph:
            if pair_u[u] is None and dfs(u):
                matching += 1

    return matching, pair_u
```

Örneğin `{'Ali': ['A', 'B'], 'Ece': ['B']}` girdisi, kişilerin yapabildiği işleri temsil eder. Fonksiyon hem maksimum eşleşme sayısını hem de atama sözlüğünü döndürür.

## Büyü değil, akıllı gruplama

Hopcroft-Karp’ın başarısı daha hızlı DFS yazmaktan değil, aramaları doğru katmanlarda **toplu yürütmekten** gelir. Büyük sosyal ağlarda, görev dağıtımında ve öneri sistemlerinde milyonlarca olası bağlantı bulunduğunda $O(VE)$ ile $O(E\sqrt{V})$ arasındaki fark, kahve molasıyla hafta sonu tatili arasındaki fark olabilir.

![maximum-bipartite-matching-63](/img/maximum-bipartite-matching-63.svg)

