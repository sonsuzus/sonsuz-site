---
layout: post
title: "Kosaraju-Sharir Algoritması: Yönlü Graflarda Güçlü Bağlı Bileşenleri Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - kosaraju
  - güçlü bağlı bileşen
  - dfs
  - algoritma
  - python
toc: true
image: /img/kosaraju-sharir-algoritmasi-37.png
---

![kosaraju-sharir-algoritmasi-37](/img/kosaraju-sharir-algoritmasi-37.svg)


Bir sosyal ağda Ayşe, Berk’in paylaşımlarına; Berk, Ceren’in paylaşımlarına; Ceren de Ayşe’nin paylaşımlarına ulaşabiliyorsa bu üçlü kapalı bir iletişim bölgesi oluşturur. Yönlü graflarda bu tür karşılıklı erişilebilir düğüm gruplarına **güçlü bağlı bileşen** denir. Kosaraju-Sharir algoritması, yalnızca iki derinlik öncelikli arama yaparak bu gizli toplulukları ortaya çıkarır.
``

## Güçlü bağlılık nedir?

Bir yönlü grafı $G=(V,E)$ ile gösterelim. $u$ düğümünden $v$ düğümüne yönlü bir yol varsa bunu $u \rightsquigarrow v$ biçiminde yazabiliriz. İki düğümün aynı güçlü bağlı bileşende bulunması için şu koşul sağlanmalıdır:

$$u \sim v \iff (u \rightsquigarrow v) \land (v \rightsquigarrow u)$$

Yani yalnızca ileri gitmek yetmez; geri dönebilmek de gerekir. Bu ilişki dönüşlü, simetrik ve geçişli olduğundan düğümleri birbirinden ayrık sınıflara böler.

| Kavram | Aranan erişim | Yönler önemli mi? |
|---|---|---|
| Bağlı bileşen | Düğümler arasında bir yol | Hayır |
| Zayıf bağlı bileşen | Kenar yönleri kaldırılınca yol | Kısmen |
| Güçlü bağlı bileşen | Her iki yönde de yol | Evet |

Her düğüm tek başına da güçlü bağlı sayılır. Ancak algoritmanın asıl eğlenceli kısmı, döngüler ve karmaşık bağlantılar arasındaki daha büyük bileşenleri bulmasıdır.

## Algoritmanın temel fikri

Kosaraju-Sharir üç aşamada çalışır:

1. Orijinal grafta DFS yap ve düğümleri **bitiş zamanlarına** göre kaydet.
2. Bütün kenarları ters çevirerek $G^T$ transpoz grafını oluştur.
3. Düğümleri azalan bitiş zamanı sırasıyla ele alıp $G^T$ üzerinde yeniden DFS yap.

İkinci turdaki her DFS ağacı tam olarak bir güçlü bağlı bileşen verir. İlk arama, hangi bileşenin önce ziyaret edilmesi gerektiğini belirleyen bir pusula gibidir.

Bir güçlü bağlı bileşeni tek bir süper düğüme sıkıştırırsak ortaya döngüsüz bir **yoğunlaşma grafı** çıkar. Bu graf bir DAG’dir. İlk DFS’nin bitiş sırası, ikinci geçişte başka bileşenlere yanlışlıkla taşmamızı önleyecek bir sıralama üretir. Kenarlar ters çevrilince bileşenlerin içindeki karşılıklı erişim korunur, bileşenler arasındaki geçiş yönleri ise değişir.

## Python ile uygulama

Aşağıdaki kod, komşuluk listesiyle verilen bir graftaki bileşenleri döndürür:

```python
def kosaraju(graph):
    visited = set()
    finish_order = []

    def first_dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                first_dfs(neighbor)
        finish_order.append(node)

    for node in graph:
        if node not in visited:
            first_dfs(node)

    transpose = {node: [] for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            transpose[neighbor].append(node)

    visited.clear()
    components = []

    def second_dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in transpose[node]:
            if neighbor not in visited:
                second_dfs(neighbor, component)

    while finish_order:
        node = finish_order.pop()
        if node not in visited:
            component = []
            second_dfs(node, component)
            components.append(component)

    return components
```

İlk `first_dfs`, bir düğümü ancak bütün komşuları tamamlandıktan sonra listeye ekler. Listenin sonundan eleman almak azalan bitiş sırasını sağlar. `second_dfs` ise transpoz grafta ulaşabildiği düğümleri aynı bileşende toplar.

## Karmaşıklık ve kullanım alanları

Her düğüm ve kenar sabit sayıda işlendiği için zaman karmaşıklığı

$$T(V,E)=O(\vert V\vert +\vert E\vert )$$

olur. Graf, transpoz yapı, ziyaret kümeleri ve DFS yığını için gereken bellek de $O(\vert V\vert +\vert E\vert )$ düzeyindedir.

Kosaraju-Sharir; sosyal ağ toplulukları, paket bağımlılık döngüleri, web bağlantıları, çağrı grafları ve durum makinelerinin analizinde kullanılabilir. İki DFS ile koskoca bir yönlü grafın içindeki karşılıklı ulaşılabilir adaları bulmak, algoritmanın hem zarif hem de pratik olmasının temel nedenidir.
