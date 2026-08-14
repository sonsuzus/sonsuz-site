---
layout: post
title: "Ağ Akışı Problemleri: Ford-Fulkerson ile Maksimum Kapasiteyi Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - graf teorisi
  - python
---

Bir lojistik ağında kamyonların, internet omurgasında paketlerin veya bir üretim hattında ham maddelerin taşındığını düşünün. Her bağlantının bir kapasitesi vardır ve amaç, başlangıç noktasından hedefe toplamda ne kadar malzeme gönderebileceğimizi bulmaktır. İşte **maksimum akış (max flow)** problemi tam olarak bu soruyu matematiksel bir modele dönüştürür. Ford-Fulkerson yöntemi ise kapasite sınırlarına çarpmadan akışı adım adım büyüten klasik ve öğretici bir yaklaşımdır.
``

Bir akış ağı, yönlü bir grafik olarak tanımlanır: $G=(V,E)$. Burada $V$ düğümler kümesini, $E$ ise bağlantıları temsil eder. Ağda özel iki düğüm bulunur: akışın başladığı **kaynak** $s$ ve bittiği **hedef** $t$. Her kenarın kapasitesi $c(u,v)$ ile gösterilir. Bir kenardan geçen gerçek akış miktarı ise $f(u,v)$ olsun.

Geçerli bir çözüm iki temel kurala uymalıdır:

1. **Kapasite kısıtı:** Her kenar için $0 \leq f(u,v) \leq c(u,v)$ olmalıdır.
2. **Akış korunumu:** Kaynak ve hedef dışındaki her düğümde giren ve çıkan akış eşit olmalıdır.

$$\sum_{u} f(u,v) = \sum_{w} f(v,w)$$

Amaç fonksiyonu, kaynaktan çıkan net akışı mümkün olduğunca büyütmektir. Bu değer genellikle $ \vert f \vert $ ile yazılır. Önemli fikir şudur: En kısa yol her zaman en fazla akışı taşıyan yol değildir. Çünkü darboğazı belirleyen, bir yol üzerindeki **en küçük kapasitedir**.

| Kavram | Anlamı | Günlük hayattan karşılığı |
|---|---|---|
| Kaynak ($s$) | Akışın başladığı düğüm | Depo |
| Hedef ($t$) | Akışın ulaştığı düğüm | Mağaza |
| Kapasite ($c$) | Kenarın üst taşıma sınırı | Yolun şerit kapasitesi |
| Darboğaz | Yoldaki en küçük kapasite | En dar köprü |
| Artık kapasite | Hâlâ gönderilebilecek miktar | Kamyondaki boş yer |

Ford-Fulkerson, kaynak ile hedef arasında kullanılabilir kapasitesi olan bir yol, yani **artırıcı yol (augmenting path)** bulur. Ardından bu yolun darboğazı kadar akış ekler. Süreç, artık kaynak-hedef yolu kalmayana kadar devam eder. Algoritmanın sihri yalnızca ileri kenarlarda değil, gerektiğinde önceki kararları geri alabilmesini sağlayan **ters kenarlarda** gizlidir.

Örneğin $s \rightarrow A \rightarrow t$ yolundaki kapasite sırasıyla 10 ve 4 ise, bu yola en fazla $\min(10,4)=4$ birim akış gönderilebilir. Akış gönderildiğinde ileri kenarların artık kapasitesi azalır; buna karşılık ters yönde 4 birimlik kapasite oluşur. Böylece algoritma daha sonra daha iyi bir kombinasyon keşfederse önceki akışın bir kısmını geri yönlendirebilir.

Aşağıdaki Python örneği, artırıcı yolu genişlik öncelikli arama ile bulur. Bu özel uygulama **Edmonds-Karp** olarak adlandırılır; Ford-Fulkerson'un daha öngörülebilir bir varyantıdır.

```python
from collections import deque, defaultdict

def max_flow(graph, source, sink):
    residual = defaultdict(lambda: defaultdict(int))
    for u in graph:
        for v, capacity in graph[u].items():
            residual[u][v] += capacity
            residual[v]  # Ters düğümü de artık ağda oluşturur.

    total_flow = 0

    while True:
        parent = {source: None}
        queue = deque([source])

        while queue and sink not in parent:
            u = queue.popleft()
            for v, capacity in residual[u].items():
                if capacity > 0 and v not in parent:
                    parent[v] = u
                    queue.append(v)

        if sink not in parent:
            return total_flow

        bottleneck = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, residual[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
            v = u

        total_flow += bottleneck
```

Bu kodda `residual`, artık ağı tutar. İlk döngü hedefe ulaşan bir yol arar; ikinci döngü yolun darboğazını hesaplar; üçüncü döngü ise ileri ve ters kapasiteleri günceller. BFS kullanıldığı için Edmonds-Karp'ın zaman karmaşıklığı $O(VE^2)$'dir. Saf Ford-Fulkerson'da yol seçimi farklı yapılabildiğinden çalışma süresi seçilen artırıcı yollara bağlı olabilir.

| Yaklaşım | Yol seçimi | Karmaşıklık | Pratik avantaj |
|---|---|---:|---|
| Ford-Fulkerson | Serbestçe seçilir | Değişken | Kavramı öğretmek için ideal |
| Edmonds-Karp | BFS ile en az kenarlı yol | $O(VE^2)$ | Daha güvenilir sınır |
| Dinic | Seviye grafiği | Genellikle daha hızlı | Büyük ağlar için güçlü |

Maksimum akış, yalnızca taşıma problemi değildir: bipartite eşleştirme, görüntü bölütleme, görev atama ve ağ bant genişliği planlama gibi alanların da temelidir. Bir sonraki adımda minimum kesit teoremini inceleyin: Maksimum akış değeri, ağı kaynaktan hedefe ayıran en ucuz kesitin kapasitesine eşittir. Bu eşitlik, algoritmanın neden gerçekten optimum sonuca ulaştığını açıklar.
