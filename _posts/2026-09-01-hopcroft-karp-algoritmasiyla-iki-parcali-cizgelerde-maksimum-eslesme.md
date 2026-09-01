---
layout: post
title: "Hopcroft-Karp Algoritmasıyla İki Parçalı Çizgelerde Maksimum Eşleşme"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - hopcroft-karp
  - maksimum eşleşme
toc: true
---

Bir şirkette çalışanları görevlere, öğrencileri projelere veya gönüllüleri etkinliklere dağıttığımızı düşünelim. Herkes her işe uygun olmayabilir; üstelik bir kişi yalnızca bir göreve atanabilir. Bütün olası dağılımları denemek kısa sürede kombinasyon cehennemine dönüşür. Hopcroft-Karp algoritması, bu karmaşayı iki parçalı çizge modeliyle düzenler ve mümkün olan en fazla sayıda eşleşmeyi verimli biçimde bulur.

``

## Problemi çizgeye dönüştürmek

İki parçalı bir çizge, düğümleri kesişmeyen iki kümeye ayrılabilen bir yapıdır:

$$G=(U,V,E)$$

Burada $U$ çalışanları veya öğrencileri, $V$ ise işleri veya projeleri temsil eder. Bir $(u,v)$ kenarı, $u$ kişisinin $v$ seçeneğine uygun olduğunu gösterir. Aynı kümedeki düğümler arasında kenar bulunmaz.

Bir **eşleşme**, ortak uç noktası bulunmayan kenarlar kümesidir. Başka bir ifadeyle hiçbir öğrenci iki projeye, hiçbir proje de iki öğrenciye atanamaz. Amaç, eşleşmedeki kenar sayısını en büyük yapmaktır:

$$M^*=\operatorname*{arg\,max}_{M \subseteq E}\vert M\vert $$

Buradaki “maksimum”, eşleşmeye artık rastgele bir kenar eklenememesi anlamındaki **maksimal** kavramıyla karıştırılmamalıdır.

| Kavram | Anlamı | Sonuç garantisi |
|---|---|---|
| Maksimal eşleşme | Yeni kenar eklenemeyen eşleşme | En büyük olmak zorunda değil |
| Maksimum eşleşme | En fazla kenarı içeren eşleşme | Optimum çözüm |
| Tam eşleşme | Bir taraftaki tüm düğümleri kapsar | Her zaman mevcut olmayabilir |

## Artırıcı yol fikri

Hopcroft-Karp’ın kalbinde **artırıcı yol** bulunur. Bu yol, eşleşmemiş bir düğümden başlar; eşleşmede olmayan ve olan kenarlar arasında sırayla ilerler; başka bir boş düğümde sona erer. Yol üzerindeki kenarların durumunu ters çevirdiğimizde eşleşmenin büyüklüğü tam olarak bir artar.

Basit algoritmalar her turda tek artırıcı yol arar. Hopcroft-Karp ise “bir yol bulmuşken neden mahalledeki diğerlerini de toplamıyoruz?” diyerek aynı anda birden fazla, birbirinden bağımsız en kısa artırıcı yolu işler.

Algoritma iki aşamayı tekrarlar:

1. **BFS**, serbest düğümlerden başlayarak katmanlı bir çizge oluşturur ve en kısa artırıcı yolların uzunluğunu belirler.
2. **DFS**, yalnızca bu katman düzenine uyan yolları izleyerek mümkün olduğunca çok artırıcı yol bulur.

Zaman karmaşıklığı

$$O(\vert E\vert \sqrt{\vert V\vert })$$

olduğundan, özellikle büyük ve seyrek çizgelerde tek tek yol arayan $O(\vert U\Vert E\vert )$ yaklaşımlarına göre ciddi avantaj sağlar.

## Python ile uygulama

Aşağıdaki kodda `graph`, sol taraftaki her düğümün bağlanabileceği sağ düğümleri tutar. BFS mesafeleri kurar; DFS ise bu mesafelere uygun eşleşmeleri gerçekleştirir.

```python
from collections import deque


def hopcroft_karp(graph):
    left_match = {u: None for u in graph}
    right_nodes = {v for edges in graph.values() for v in edges}
    right_match = {v: None for v in right_nodes}
    distance = {}

    def bfs():
        queue = deque()
        path_exists = False

        for u in graph:
            if left_match[u] is None:
                distance[u] = 0
                queue.append(u)
            else:
                distance[u] = float("inf")

        while queue:
            u = queue.popleft()
            for v in graph[u]:
                paired = right_match[v]
                if paired is None:
                    path_exists = True
                elif distance[paired] == float("inf"):
                    distance[paired] = distance[u] + 1
                    queue.append(paired)
        return path_exists

    def dfs(u):
        for v in graph[u]:
            paired = right_match[v]
            if paired is None or (
                distance[paired] == distance[u] + 1 and dfs(paired)
            ):
                left_match[u] = v
                right_match[v] = u
                return True
        distance[u] = float("inf")
        return False

    while bfs():
        for u in graph:
            if left_match[u] is None:
                dfs(u)

    return {u: v for u, v in left_match.items() if v is not None}
```

Örneğin `{"Ada": ["Web", "Mobil"], "Ece": ["Mobil"], "Can": ["Web", "Veri"]}` girdisi, öğrencilerin seçebileceği projeleri temsil eder. Algoritma uygun bir maksimum eşleşme döndürür; ancak birden fazla optimum dağılım varsa bunlardan yalnızca birini seçebilir.

Hopcroft-Karp kapasitesi bir olan atamalarda harikadır. Projelerin kontenjanı, öncelikler veya maliyetler varsa problem; akış ağları, minimum maliyetli maksimum akış ya da ağırlıklı eşleşme modellerine genişletilmelidir. Yani bu algoritma güçlü bir çekiçtir, fakat her atama problemi de çivi değildir!
