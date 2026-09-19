---
layout: post
title: "Kosaraju Algoritması: Yönlü Grafların Gizli Topluluklarını Keşfetmek"
math: true
categories: 
  - Bilgi
tags: 
  - kosaraju
  - graf teorisi
  - algoritma
  - python
  - derinlik öncelikli arama
  - bağlı bileşenler
toc: true
---

Bir sosyal ağda herkes birbirini takip etmeyebilir; Ayşe, Berk’i takip ederken Berk Ayşe’yi takip etmiyor olabilir. Buna rağmen bazı kullanıcı gruplarında herkes diğerlerine dolaylı yollardan ulaşabilir. Yönlü grafların içindeki bu gizli ve sıkı topluluklara **güçlü bağlı bileşenler** denir. Kosaraju algoritması, grafı iki kez dolaşarak bu toplulukları şaşırtıcı derecede zarif biçimde ortaya çıkarır.

``

## Güçlü bağlı bileşen nedir?

Yönlü bir grafı $G=(V,E)$ olarak gösterelim. Burada $V$ düğüm, $E$ ise yönlü kenar kümesidir. İki düğüm $u$ ve $v$ aynı güçlü bağlı bileşendeyse hem $u$’dan $v$’ye hem de $v$’den $u$’ya bir yol bulunmalıdır:

$$u \leadsto v \quad \text{ve} \quad v \leadsto u$$

Örneğin $A \rightarrow B$, $B \rightarrow C$ ve $C \rightarrow A$ kenarları bir döngü meydana getirir. Bu üç düğüm karşılıklı erişilebilir olduğu için tek bir güçlü bağlı bileşendir. Ancak yalnızca $C \rightarrow D$ varsa, $D$ geri dönemediğinden aynı topluluğa katılamaz.

| Kavram | Yönsüz graf | Yönlü graf |
|---|---|---|
| Bağlantı koşulu | Arada bir yol bulunması yeterlidir | İki yönde de yol bulunmalıdır |
| Bileşen türü | Bağlı bileşen | Güçlü bağlı bileşen |
| Tipik yöntem | DFS veya BFS | Kosaraju, Tarjan |

## Kosaraju’nun iki perdelik oyunu

Algoritmanın temel fikri, önce bileşenlerin bitiş sırasını öğrenmek, ardından tüm yolların yönünü ters çevirerek bileşenleri tek tek toplamaktır:

1. Orijinal grafta DFS çalıştırılır. Her düğüm, keşfi bittiğinde bir yığına eklenir.
2. Bütün kenarlar ters çevrilerek transpoz graf $G^T$ oluşturulur.
3. Düğümler yığından sırayla alınır ve $G^T$ üzerinde yeniden DFS yapılır.
4. Her yeni DFS ağacı, ayrı bir güçlü bağlı bileşen verir.

Peki grafı neden ters çeviriyoruz? Güçlü bağlı bir bileşenin içindeki karşılıklı erişilebilirlik, kenarlar ters dönünce korunur. Buna karşılık bileşenler arasındaki tek yönlü geçişler tersine döner. İlk DFS’nin bitiş sırası sayesinde ikinci tur, başka bir bileşene yanlışlıkla taşmadan doğru topluluğu yakalar. Bir bakıma ilk tur haritayı okur, ikinci tur gizli mahallelerin sınırlarını çizer.

## Python uygulaması

Aşağıdaki uygulama, grafı komşuluk listesiyle tutar. İlk `dfs` bitiş sırasını üretir; `collect` ise ters graftaki bileşenleri toplar.

```python
def kosaraju(graph):
    visited = set()
    order = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        order.append(node)  # Düğüm tamamlanınca kaydet

    for node in graph:
        if node not in visited:
            dfs(node)

    reversed_graph = {node: [] for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reversed_graph[neighbor].append(node)

    visited.clear()
    components = []

    def collect(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in reversed_graph[node]:
            if neighbor not in visited:
                collect(neighbor, component)

    while order:
        node = order.pop()
        if node not in visited:
            component = []
            collect(node, component)
            components.append(component)

    return components

 graph = {
    "A": ["B"],
    "B": ["C"],
    "C": ["A", "D"],
    "D": ["E"],
    "E": ["D"]
}

print(kosaraju(graph))
```

Bu örnekte sonuç, sıralaması değişebilmekle birlikte, `['A', 'B', 'C']` ve `['D', 'E']` topluluklarını içerir.

## Karmaşıklık ve kullanım alanları

Her düğüm ve kenar yalnızca sabit sayıda ziyaret edilir. Bu nedenle zaman karmaşıklığı

$$O(\vert V\vert +\vert E\vert )$$

olur. Graf, ters graf, ziyaret kümeleri ve yığın için gereken bellek de $O(\vert V\vert +\vert E\vert )$ düzeyindedir.

| Kullanım alanı | Güçlü bileşenin anlamı |
|---|---|
| Sosyal ağ | Karşılıklı erişebilen kullanıcı topluluğu |
| Yazılım bağımlılıkları | Döngüsel bağımlı modüller |
| Web analizi | Birbirine bağlantılarla dönebilen sayfalar |
| Oyun haritası | Karşılıklı geçiş yapılabilen bölgeler |

Kosaraju, iki DFS ve bir kenar tersine çevirme işlemiyle karmaşık görünen yönlü ağları anlaşılır parçalara böler. Özellikle uygulama kolaylığı ve doğrusal çalışma süresi sayesinde graf teorisi araç çantasının hem öğretici hem de güçlü üyelerinden biridir.
