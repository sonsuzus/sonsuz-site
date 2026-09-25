---
layout: post
title: "Min-Cost Max-Flow: Kapasite ve Maliyeti Aynı Anda Optimize Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - graf
  - ağ-akışı
  - optimizasyon
  - python
  - min-cost-max-flow
toc: true
image: /img/min-cost-max-80.png
---

Bir lojistik ağında mümkün olan en fazla ürünü taşımak yetmez; bunu hangi maliyetle yaptığınız da önemlidir. **Min-Cost Max-Flow (MCMF)**, kaynaktan hedefe maksimum akışı gönderirken toplam taşıma maliyetini en aza indiren algoritma ailesidir. Kısacası maksimum performans ile minimum fatura arasında matematiksel bir barış anlaşması imzalar.


![min-cost-max-80](/img/min-cost-max-80.svg)

``

## Problemin matematiksel modeli

Yönlü bir ağdaki her $(u,v)$ kenarı iki değere sahiptir: kapasite $c(u,v)$ ve birim akış maliyeti $w(u,v)$. Kenardan geçirilen akış $f(u,v)$ ise şu koşulu sağlamalıdır:

$$0 \leq f(u,v) \leq c(u,v)$$

Kaynak $s$ ve hedef $t$ dışındaki her düğümde akış korunur:

$$\sum_u f(u,v)=\sum_x f(v,x)$$

Önce toplam akış miktarı $F$ maksimize edilir, ardından bu akışın maliyeti minimize edilir:

$$C=\sum_{(u,v)\in E} f(u,v)\cdot w(u,v)$$

Bu öncelik önemlidir. Sadece en ucuz yolu seçmek maksimum akışa ulaşmayı engelleyebilir; sadece maksimum akış bulmak ise gereksiz derecede pahalı bir sonuç üretebilir.

| Problem | Amaç | Kenar bilgisi |
|---|---|---|
| En kısa yol | En ucuz tek rota | Maliyet |
| Maximum Flow | En yüksek akış | Kapasite |
| Min-Cost Flow | Belirli akışı ucuza taşıma | Kapasite ve maliyet |
| Min-Cost Max-Flow | Maksimum akışı en ucuza taşıma | Kapasite ve maliyet |

## Artık ağ neden gereklidir?

Algoritma her seçimden sonra bir **artık ağ (residual graph)** tutar. Kapasitesi kullanılan ileri kenarın artık kapasitesi azalır; ters yönde ise maliyeti $-w(u,v)$ olan bir kenar oluşur. Bu ters kenar, algoritmanın önceki kararından vazgeçebilmesini sağlar. Yani sistem yalnızca ilerlemez; gerektiğinde “Bu rota pek iyi olmadı” diyerek akışı geri alıp daha ucuz biçimde düzenler.

Yaygın yaklaşım, artık ağda maliyeti en düşük artırma yolunu bulup mümkün olan akışı bu yoldan göndermektir. Negatif kenarlar nedeniyle Bellman-Ford kullanılabilir. Daha hızlı uygulamalarda ise düğüm potansiyelleriyle maliyetler yeniden ağırlıklandırılır ve Dijkstra çalıştırılır.

İndirgenmiş maliyet şu şekilde hesaplanır:

$$w'(u,v)=w(u,v)+p(u)-p(v)$$

Doğru potansiyeller altında $w'(u,v)\geq 0$ olur; böylece Dijkstra güvenle kullanılabilir.

## Python ile temel uygulama

Aşağıdaki sürüm, anlaşılır olması için SPFA ile en ucuz artırma yolunu bulur:

```python
from collections import deque

class Edge:
    def __init__(self, to, rev, cap, cost):
        self.to, self.rev = to, rev
        self.cap, self.cost = cap, cost

def add_edge(g, u, v, cap, cost):
    g[u].append(Edge(v, len(g[v]), cap, cost))
    g[v].append(Edge(u, len(g[u]) - 1, 0, -cost))

def min_cost_max_flow(g, source, target):
    n = len(g)
    flow = cost = 0

    while True:
        dist = [float('inf')] * n
        parent = [None] * n
        in_queue = [False] * n
        dist[source] = 0
        q = deque([source])

        while q:
            u = q.popleft()
            in_queue[u] = False
            for i, e in enumerate(g[u]):
                if e.cap > 0 and dist[e.to] > dist[u] + e.cost:
                    dist[e.to] = dist[u] + e.cost
                    parent[e.to] = (u, i)
                    if not in_queue[e.to]:
                        q.append(e.to)
                        in_queue[e.to] = True

        if parent[target] is None:
            break

        pushed = float('inf')
        v = target
        while v != source:
            u, i = parent[v]
            pushed = min(pushed, g[u][i].cap)
            v = u

        v = target
        while v != source:
            u, i = parent[v]
            e = g[u][i]
            e.cap -= pushed
            g[v][e.rev].cap += pushed
            cost += pushed * e.cost
            v = u

        flow += pushed

    return flow, cost
```

`add_edge`, ileri kenarla birlikte ters kenarı da oluşturur. Ana döngü en ucuz yolu bulur, yol üzerindeki darboğaz kapasiteyi hesaplar ve artık ağı günceller. Sonuç `(maksimum_akış, minimum_maliyet)` biçimindedir.

## Karmaşıklık ve kullanım alanları

SPFA tabanlı yaklaşım pratikte kullanışlı olsa da en kötü durumda yavaşlayabilir. Bellman-Ford ile yaklaşık $O(FVE)$, potansiyel ve Dijkstra ile $O(FE\log V)$ davranışı beklenir; burada $F$ artırma sayısıyla ilişkilidir.

MCMF; kargo dağıtımı, çalışan-görev eşleştirmesi, üretim planlama, ağ paketlerinin yönlendirilmesi ve kaynak tahsisi gibi alanlarda kullanılır. Özetle soru “Ne kadar taşıyabilirim?” ile bitmiyor, “Bunu en akıllıca kaça taşırım?” diye devam ediyorsa sahne Min-Cost Max-Flow’undur.
