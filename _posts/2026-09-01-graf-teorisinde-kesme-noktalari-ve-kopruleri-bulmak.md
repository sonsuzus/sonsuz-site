---
layout: post
title: "Graf Teorisinde Kesme Noktaları ve Köprüleri Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - tarjan algoritması
  - derinlik öncelikli arama
toc: true
---

İnternet omurgası, elektrik şebekesi veya şehirler arası yol ağı düşünelim. Bazı istasyonların kapanması yalnızca küçük bir aksaklık yaratırken bazıları bütün ağı iki parçaya ayırabilir. Graf teorisi, ağın bu kritik düğüm ve bağlantılarını **kesme noktaları** ve **köprüler** kavramlarıyla belirler. Üstelik bunu her elemanı tek tek kaldırıp ağı tekrar sınamadan, verimli bir DFS algoritmasıyla gerçekleştirebiliriz.

``

## Matematiksel model

Yönsüz bir grafı $G=(V,E)$ biçiminde tanımlayalım. Burada $V$ düğümleri, $E$ ise düğümler arasındaki kenarları temsil eder.

Bir $v \in V$ düğümü ve ona bağlı kenarlar silindiğinde grafın bağlı bileşen sayısı artıyorsa $v$, **kesme noktası**dır. Benzer şekilde bir $e \in E$ kenarı silindiğinde bağlı bileşen sayısı artıyorsa bu kenara **köprü** denir.

| Kavram | Silinen eleman | Kritik olma koşulu | Gerçek hayat örneği |
|---|---|---|---|
| Kesme noktası | Düğüm | Bağlı bileşen sayısı artar | Merkezi ağ yönlendiricisi |
| Köprü | Kenar | Bağlı bileşen sayısı artar | İki şehir arasındaki tek yol |
| Normal eleman | Düğüm veya kenar | Alternatif rota bulunur | Yedekli bağlantı |

Saf yaklaşımda her düğüm ve kenarı sırayla kaldırıp BFS veya DFS çalıştırabiliriz. Bu yöntem yaklaşık $O(V(V+E))$ veya $O(E(V+E))$ maliyetine ulaşabilir. Tarjan yaklaşımı ise bütün kritik elemanları yalnızca $O(V+E)$ zamanda bulur.

## DFS zamanları ve low değeri

Algoritma, derinlik öncelikli arama sırasında her düğüm için iki değer tutar:

- $disc[u]$: $u$ düğümünün ilk ziyaret edilme zamanı.
- $low[u]$: $u$ veya DFS alt ağacındaki düğümlerden geri kenarlarla ulaşılabilen en eski düğümün zamanı.

Bir düğümün low değeri sezgisel olarak “Bu alt ağaç, atasına farklı bir kapıdan dönebiliyor mu?” sorusunu yanıtlar:

$$low[u] = min(disc[u],\ disc[w],\ low[v])$$

Burada $w$, bir geri kenarla erişilen ata; $v$ ise DFS ağacındaki çocuktur.

DFS ağacında $u$ düğümünden $v$ çocuğuna giden kenarı inceleyelim:

- Eğer $low[v] > disc[u]$ ise $(u,v)$ bir **köprüdür**. Çünkü $v$ alt ağacının $u$ veya daha eski bir düğüme alternatif dönüşü yoktur.
- Eğer $u$ kök değilse ve $low[v] \ge disc[u]$ ise $u$ bir **kesme noktasıdır**.
- DFS kökü, en az iki bağımsız DFS çocuğuna sahipse kesme noktasıdır.

## Python ile Tarjan uygulaması

Aşağıdaki kod, komşuluk listesiyle verilen yönsüz bir grafın kesme noktalarını ve köprülerini aynı DFS geçişinde bulur:

```python
def kritik_elemanlar(graf):
    zaman = 0
    disc = {}
    low = {}
    parent = {}
    kesme = set()
    kopruler = []

    def dfs(u):
        nonlocal zaman
        zaman += 1
        disc[u] = low[u] = zaman
        cocuk_sayisi = 0

        for v in graf[u]:
            if v not in disc:
                parent[v] = u
                cocuk_sayisi += 1
                dfs(v)
                low[u] = min(low[u], low[v])

                if low[v] > disc[u]:
                    kopruler.append((u, v))

                if u not in parent and cocuk_sayisi > 1:
                    kesme.add(u)
                elif u in parent and low[v] >= disc[u]:
                    kesme.add(u)

            elif parent.get(u) != v:
                low[u] = min(low[u], disc[v])

    for dugum in graf:
        if dugum not in disc:
            dfs(dugum)

    return kesme, kopruler
```

Dış döngü önemlidir; çünkü başlangıçtaki ağ zaten birden fazla bağlı bileşenden oluşabilir. DFS, keşfedilmemiş her düğümden yeniden başlatılarak grafın tamamını kapsar.

## Neden işe yarıyor?

Bir DFS çocuğunun low değeri atasının keşif zamanına ulaşamıyorsa alt ağaçta alternatif rota bulunmuyor demektir. İlgili kenarı veya ebeveyn düğümü kaldırmak, bu bölgeyi ağdan koparır. Böylece algoritma fiziksel silme denemeleri yapmak yerine bağlantı yedekliliğini matematiksel zaman damgalarıyla ölçer.

Bu yöntem ağ güvenliği, yol planlama, sosyal ağ analizi ve mikroservis mimarilerinde tek hata noktalarını keşfetmek için kullanılabilir. Kısacası Tarjan algoritması, ağın “Buraya bir şey olursa ne olur?” sorusuna doğrusal zamanda oldukça net bir cevap verir.
