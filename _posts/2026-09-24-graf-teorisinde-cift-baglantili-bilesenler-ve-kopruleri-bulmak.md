---
layout: post
title: "Graf Teorisinde Çift Bağlantılı Bileşenler ve Köprüleri Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - tarjan algoritması
  - çift bağlantılı bileşenler
  - köprüler
  - python
  - algoritmalar
toc: true
image: /img/graf-teorisinde-cift-15.png
---

Bir bilgisayar ağında tek bir kablonun kopması sistemi iki parçaya ayırabilir mi? Ya da bir sosyal ağdaki tek bir kullanıcının ayrılması topluluklar arasındaki iletişimi kesebilir mi? Graf teorisindeki **köprüler**, **eklem noktaları** ve **çift bağlantılı bileşenler**, ağların bu dramatik zayıflıklarını ortaya çıkarmamızı sağlar.

``

## Temel kavramlar

Yönsüz bir grafı $G=(V,E)$ olarak gösterelim. Bir kenar silindiğinde grafın bağlı bileşen sayısı artıyorsa bu kenara **köprü** denir. Benzer biçimde, bir düğüm ve ona bağlı kenarlar kaldırıldığında bileşen sayısı artıyorsa o düğüm bir **eklem noktasıdır**.

Çift bağlantılılık ise iki farklı anlamda kullanılabilir:

| Kavram | Dayanıklı olduğu arıza | Temel özellik |
|---|---|---|
| Kenar-çift-bağlantılı bileşen | Tek kenar kaybı | İçinde köprü bulunmaz |
| Düğüm-çift-bağlantılı bileşen | Tek düğüm kaybı | İçinde eklem noktasıyla ayrılma olmaz |
| Köprü | Kritik kenar kaybı | Silinince graf parçalanır |
| Eklem noktası | Kritik düğüm kaybı | Silinince graf parçalanır |

Örneğin bir üçgen içindeki herhangi bir kenar silinse bile kalan iki kenar düğümleri bağlı tutar. Buna karşılık üçgene yalnızca tek kenarla bağlanan bir sunucunun bağlantısı köprüdür. Başka bir deyişle, alternatif rota yoksa alarm zilleri çalmalıdır.

## DFS ve low-link fikri

Bu yapıları verimli biçimde bulmak için Tarjan yaklaşımından yararlanılır. Derinlik öncelikli arama sırasında her düğüm için iki değer saklanır:

- $disc[u]$: $u$ düğümünün keşfedilme zamanı,
- $low[u]$: $u$ veya DFS alt ağacından geri kenarlarla ulaşılabilen en eski düğümün keşif zamanı.

Bir DFS ağacı kenarı $(u,v)$ için

$$low[v] > disc[u]$$

ise $(u,v)$ bir köprüdür. Çünkü $v$ tarafındaki alt ağaç, $u$ veya onun atalarına alternatif bir yoldan dönememektedir.

Eklem noktası koşulu biraz farklıdır. Kök olmayan bir $u$ için herhangi bir çocuk $v$ üzerinde

$$low[v] \ge disc[u]$$

olması $u$'yu eklem noktası yapar. DFS kökü ise ancak en az iki bağımsız DFS çocuğuna sahipse eklem noktasıdır. `>` ile `>=` arasındaki küçücük fark, algoritmanın en sevdiği sınav tuzaklarından biridir.

## Python ile köprü ve eklem noktası bulma

Aşağıdaki kod, komşuluk listesiyle verilen yönsüz bir grafı tek DFS turunda inceler:

```python
def kritik_noktalar(graf):
    zaman = 0
    disc = {}
    low = {}
    parent = {}
    kopruler = []
    eklemler = set()

    def dfs(u):
        nonlocal zaman
        zaman += 1
        disc[u] = low[u] = zaman
        cocuk = 0

        for v in graf[u]:
            if v not in disc:
                parent[v] = u
                cocuk += 1
                dfs(v)
                low[u] = min(low[u], low[v])

                if low[v] > disc[u]:
                    kopruler.append((u, v))

                if u not in parent and cocuk > 1:
                    eklemler.add(u)
                elif u in parent and low[v] >= disc[u]:
                    eklemler.add(u)

            elif parent.get(u) != v:
                low[u] = min(low[u], disc[v])

    for dugum in graf:
        if dugum not in disc:
            dfs(dugum)

    return kopruler, eklemler
```

Kodun önemli noktası, ziyaret edilmiş bir komşunun ebeveyn olmaması hâlinde bunun bir geri kenar kabul edilmesidir. Böylece `low` değeri geçmişte keşfedilmiş bir düğüme doğru güncellenir. Graf bağlı değilse dıştaki döngü her bileşen için DFS başlatır.

## Bileşenler nasıl çıkarılır?

Düğüm-çift-bağlantılı bileşenleri doğrudan üretmek için DFS sırasında gezilen kenarlar bir yığında tutulur. Bir çocuk için $low[v] \ge disc[u]$ koşulu oluştuğunda, $(u,v)$ kenarına kadar yığından çıkarılan kenarlar bir bileşeni meydana getirir. Eklem noktaları birden fazla bileşende bulunabilir; bu bir hata değil, bileşenleri birbirine bağlayan menteşe görevlerinin sonucudur.

Algoritmanın zaman karmaşıklığı

$$O(\vert V\vert +\vert E\vert )$$

ve bellek karmaşıklığı $O(\vert V\vert )$ düzeyindedir. Dolayısıyla yönlendirici ağlarından bağımlılık grafiklerine kadar büyük sistemlerde uygulanabilir. Köprüler yedek bağlantı kurulması gereken hatları, eklem noktaları ise çoğaltılması gereken servisleri gösterir. Kısacası Tarjan algoritması yalnızca grafı dolaşmaz; sistemin nereden kırılabileceğini de fısıldar.

![graf-teorisinde-cift-15](/img/graf-teorisinde-cift-15.svg)

