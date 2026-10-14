---
layout: post
title: "DAG’larda En Kısa Yol: Döngüler Olmadan Daha Hızlı Rotalar"
math: true
categories: 
  - Bilgi
tags: 
  - dag
  - graf teorisi
  - en kısa yol
  - topolojik sıralama
  - algoritmalar
  - python
toc: true
image: /img/daglarda-en-kisa-47.png
---

Bir şehir haritasında sürekli aynı kavşağa dönebiliyorsanız rota bulmak biraz baş ağrıtabilir. Yönlendirilmiş Asiklik Graf (Directed Acyclic Graph veya DAG) ise bu karmaşayı ortadan kaldırır: Okları takip ederek başladığınız düğüme geri dönemezsiniz. Bu döngüsüz yapı sayesinde en kısa yolları, Dijkstra’nın öncelik kuyruğuna bile ihtiyaç duymadan oldukça zarif biçimde hesaplayabiliriz.


![daglarda-en-kisa-47](/img/daglarda-en-kisa-47.svg)

``

## Önce DAG nedir?

Yönlendirilmiş bir grafta kenarlar belirli bir yöne sahiptir. Örneğin $u \rightarrow v$ kenarı, yalnızca $u$ düğümünden $v$ düğümüne geçişi temsil eder. Grafın içinde yönlendirilmiş hiçbir döngü bulunmuyorsa bu yapı bir DAG’dır.

DAG’lar; görev planlama, ders ön koşulları, bağımlılık yönetimi, veri işleme hatları ve sürüm geçmişleri gibi doğal bir ilerleme sırası bulunan problemlerde sıkça görülür.

Döngünün bulunmaması, düğümleri **topolojik olarak sıralayabilmemizi** sağlar. Böyle bir sıralamada her $u \rightarrow v$ kenarı için $u$, listede $v$’den önce gelir. En kısa yol algoritmasının asıl süper gücü de budur.

## Neden topolojik sıralama yeterli?

Başlangıç düğümünün uzaklığını $0$, diğer bütün uzaklıkları $∞$ kabul edelim. Düğümleri topolojik sırayla işlerken her kenar için gevşetme yaparız:

$$d[v] = \min(d[v],\ d[u] + w(u,v))$$

Burada $d[u]$, başlangıçtan $u$ düğümüne bilinen en kısa uzaklık; $w(u,v)$ ise kenarın ağırlığıdır. Bir düğüm işlendiğinde ona gelebilecek bütün önceki düğümler zaten değerlendirilmiştir. Dolayısıyla geriye dönüp uzaklığı tekrar tekrar düzeltmeye gerek kalmaz.

| Algoritma | Negatif kenar | Döngü desteği | Zaman karmaşıklığı |
|---|---:|---:|---:|
| DAG en kısa yol | Evet | Hayır | $O(V+E)$ |
| Dijkstra | Hayır | Evet | Genellikle $O((V+E)\log V)$ |
| Bellman-Ford | Evet | Evet | $O(VE)$ |

DAG algoritması negatif ağırlıklı kenarlarla da çalışır. Çünkü negatif bir kenarın uzaklıkları sonradan beklenmedik biçimde değiştireceği döngüsel bir geri dönüş yoktur. Negatif döngü zaten DAG tanımı gereği oluşamaz.

## Python ile uygulama

Aşağıdaki fonksiyon önce DFS kullanarak topolojik sıralamayı oluşturur, ardından düğümleri bu sırada işleyerek kenarları gevşetir:

```python
def dag_shortest_path(graph, start):
    visited = set()
    order = []

    def dfs(node):
        visited.add(node)
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        order.append(node)

    # Bağlantısız parçalar için tüm düğümleri dolaşır.
    for node in graph:
        if node not in visited:
            dfs(node)

    order.reverse()
    distance = {node: float('inf') for node in graph}
    distance[start] = 0

    for node in order:
        if distance[node] == float('inf'):
            continue

        for neighbor, weight in graph.get(node, []):
            candidate = distance[node] + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate

    return distance


graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('D', 3)],
    'C': [('B', -1), ('D', 5)],
    'D': []
}

print(dag_shortest_path(graph, 'A'))
```

Bu örnekte `C → B` kenarının ağırlığı negatiftir. Buna rağmen sonuç güvenle hesaplanır: `A → C → B → D` rotasının toplam maliyeti $2 + (-1) + 3 = 4$ olur. Doğrudan görünen yollar her zaman en hesaplı yollar değildir!

## Karmaşıklık ve önemli ayrıntılar

Topolojik sıralama $O(V+E)$, bütün kenarların gevşetilmesi de $O(V+E)$ sürer. Böylece toplam zaman karmaşıklığı $O(V+E)$, ek alan gereksinimi ise $O(V)$ olur. Bu, grafın tamamını en azından bir kez incelemek zorunda olduğumuz düşünüldüğünde oldukça verimlidir.

Ancak algoritmayı kullanmadan önce grafın gerçekten asiklik olduğu doğrulanmalıdır. Döngü varsa topolojik sıralama üretilemez. Kahn algoritması sonunda işlenen düğüm sayısını kontrol etmek veya DFS sırasında renk tabanlı döngü tespiti yapmak bu doğrulama için uygundur.

Özetle DAG yapısı, “ilerideki bir düğüm geçmişi etkileyemez” garantisi verir. Bu garanti en kısa yol problemini tek yönlü, doğrusal ve hızlı bir hesaplamaya dönüştürür; bazen döngülerin yokluğu gerçekten de hayatı kolaylaştırır.
