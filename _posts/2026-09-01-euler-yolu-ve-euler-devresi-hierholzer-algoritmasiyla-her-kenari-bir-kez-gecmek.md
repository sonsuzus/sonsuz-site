---
layout: post
title: "Euler Yolu ve Euler Devresi: Hierholzer Algoritmasıyla Her Kenarı Bir Kez Geçmek"
math: true
categories: 
  - Program
tags: 
  - çizge teorisi
  - hierholzer algoritması
  - python
toc: true
---

Bir şehrin bütün köprülerinden yalnızca bir kez geçebilir miyiz? Königsberg köprüleri problemiyle ünlenen bu soru, çizge teorisindeki **Euler yolu** ve **Euler devresi** kavramlarının temelini oluşturur. Bu yazıda, bir çizgenin her kenarını tam olarak bir kez kullanan rotaları tanıyacak ve böyle bir rotayı verimli biçimde bulan Hierholzer algoritmasını Python ile kodlayacağız.
``

## Euler Yolu ile Euler Devresi Arasındaki Fark

Bir çizgeyi $G=(V,E)$ olarak gösterelim. Burada $V$ düğümleri, $E$ ise düğümler arasındaki kenarları temsil eder. Euler rotalarında amaç bütün düğümleri değil, **bütün kenarları** tam bir kez kullanmaktır.

| Kavram | Başlangıç ve bitiş | Kenar kullanımı |
|---|---|---|
| Euler yolu | Farklı olabilir | Her kenar tam bir kez |
| Euler devresi | Aynı düğümdür | Her kenar tam bir kez |
| Hamilton yolu | Farklı olabilir | Her düğüm tam bir kez |

Euler ve Hamilton problemleri sıkça karıştırılır. Euler problemi kenarlara, Hamilton problemi düğümlere odaklanır. Üstelik Euler rotası doğrusal zamanda bulunabilirken Hamilton yolu genel durumda çok daha zorlu bir problemdir.

## Euler Rotasının Var Olma Koşulları

Yönsüz ve bağlantılı bir çizgede bir düğümün derecesi, o düğüme bağlı kenarların sayısıdır. Dereceyi $deg(v)$ ile gösterirsek el sıkışma lemması şunu söyler:

$$
Σ_{v∈V} deg(v) = 2\vert E\vert 
$$

Her kenar toplam dereceye iki katkı yaptığı için tek dereceli düğümlerin sayısı daima çifttir. Euler rotasının koşulları şöyledir:

| Tek dereceli düğüm sayısı | Sonuç |
|---:|---|
| 0 | Euler devresi vardır |
| 2 | Euler yolu vardır |
| 2'den fazla | Euler rotası yoktur |

İki tek dereceli düğüm varsa yol bunlardan birinde başlayıp diğerinde biter. Hiç yoksa kenarı bulunan herhangi bir düğüm başlangıç olabilir. Ayrıca sıfır dereceli düğümler görmezden gelindiğinde çizgenin bağlantılı olması gerekir.

## Hierholzer Algoritmasının Mantığı

Algoritma, kullanılmamış bir kenarı takip ederek ilerler. Çıkış kalmadığında ulaşılan düğümü sonuca ekler ve bir önceki düğüme geri döner. Böylece geçici çevrimler iç içe birleştirilir. Sonuç tersten oluştuğu için en sonunda liste ters çevrilir.

1. Uygun başlangıç düğümünü seç.
2. Düğümü yığına ekle.
3. Kullanılmamış kenar varsa bu kenarı silip komşuya ilerle.
4. Kenar kalmadıysa düğümü rotaya aktar.
5. Yığın boşalınca rotayı ters çevir.

## Python ile Uygulama

Aşağıdaki kod yönsüz bir çizgeyi komşuluk listesiyle işler. Kenarlar iki yönde kaydedildiğinden, bir kenar seçildiğinde karşı düğümün listesinden de kaldırılır.

```python
from collections import defaultdict

def hierholzer(edges):
    graph = defaultdict(list)

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    odd = [v for v in graph if len(graph[v]) % 2 == 1]
    if len(odd) not in (0, 2):
        raise ValueError('Euler yolu veya devresi yok.')

    start = odd[0] if odd else edges[0][0]
    stack = [start]
    route = []

    while stack:
        current = stack[-1]

        if graph[current]:
            neighbor = graph[current].pop()
            graph[neighbor].remove(current)
            stack.append(neighbor)
        else:
            route.append(stack.pop())

    route.reverse()

    if len(route) != len(edges) + 1:
        raise ValueError('Çizge bağlantılı değil.')

    return route

edges = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 2)]
print(hierholzer(edges))
```

`len(route) == |E| + 1` kontrolü önemlidir: Ayrık bir bileşende kullanılmamış kenar kalmışsa algoritmanın ürettiği rota kısa olur. Böylece bağlantılılık ayrıca bir arama yazmadan doğrulanır.

## Karmaşıklık ve Küçük Bir İyileştirme

Algoritmanın ideal zaman karmaşıklığı $O(\vert V\vert +\vert E\vert )$, bellek karmaşıklığı ise $O(\vert V\vert +\vert E\vert )$ olur. Ancak Python listesindeki `remove` işlemi doğrusal maliyetlidir; bu örnek öğretici sadelik uğruna kullanılmıştır. Büyük çizgelerde her kenara benzersiz bir kimlik verip `kullanildi[kenar_id]` dizisi tutmak, gerçek doğrusal performansı korur.

Hierholzer algoritmasının güzelliği burada yatar: Karmaşık görünen bütün kenarları bir kez kullanma problemi, bir yığın, kontrollü geri dönüş ve doğru derece koşullarıyla zarif bir yürüyüşe dönüşür.
