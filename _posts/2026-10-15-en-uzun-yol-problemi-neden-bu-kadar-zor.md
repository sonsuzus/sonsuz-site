---
layout: post
title: "En Uzun Yol Problemi Neden Bu Kadar Zor?"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - graf teorisi
  - np-zor
  - en uzun yol
  - dinamik programlama
toc: true
image: /img/en-uzun-yol-21.png
---

Bir şehirden diğerine giderken navigasyon uygulaması en kısa rotayı saniyeler içinde bulabilir. Peki uygulamadan hiçbir kavşağı iki kez ziyaret etmeden mümkün olan en uzun rotayı bulmasını istersek ne olur? Masum görünen bu değişiklik, problemi algoritmalar dünyasının en çetin sınıflarından birine taşır: En Uzun Yol Problemi genel graflarda NP-zordur.
``

## Önce “yol” kavramını netleştirelim

Bir graf $G=(V,E)$, düğümlerden oluşan $V$ kümesi ile bu düğümleri bağlayan $E$ kenar kümesidir. Ağırlıklı bir grafta her kenarın $w(u,v)$ maliyeti bulunur. Bir $P$ yolunun toplam ağırlığı şöyle hesaplanır:

$$
w(P)=\sum_{(u,v)\in P} w(u,v)
$$

Buradaki kritik ayrıntı, aradığımız yapının **basit yol** olmasıdır; yani hiçbir düğüm birden fazla ziyaret edilemez. Tekrara izin verilseydi pozitif ağırlıklı bir döngünün çevresinde sonsuza kadar dolaşarak yol uzunluğunu sınırsız büyütebilirdik. Dolayısıyla anlamlı optimizasyon problemi, tekrar içermeyen en uzun yolu arar.

| Özellik | En kısa yol | En uzun basit yol |
|---|---|---|
| Genel çözüm | Dijkstra, Bellman-Ford | Bilinen polinom zamanlı çözüm yok |
| Döngü etkisi | Pozitif döngüler sorun çıkarmaz | Düğüm tekrarı yoksa seçimleri zorlaştırır |
| Açgözlü yaklaşım | Bazı koşullarda çalışır | Genellikle yanlış sonuç verir |
| Karmaşıklık | Çoğunlukla polinom | Genel durumda NP-zor |

![en-uzun-yol-21](/img/en-uzun-yol-21.svg)


## En kısa yol kolayken en uzun yol neden zor?

En kısa yol algoritmaları **optimal alt yapıdan** yararlanır. Bir düğüme ulaşmanın en iyi maliyeti bulunduğunda, özellikle negatif ağırlık yoksa bu karar güvenle kullanılabilir. En uzun basit yolda ise erken seçilen bir kenar, ileride ihtiyaç duyulan önemli bir düğümü tüketebilir. Yerel olarak uzun görünen seçim, küresel olarak kısa bir çıkmaza dönüşebilir.

Örneğin en ağır komşuya gitmeyi seçen açgözlü algoritma, birkaç adım sonra kapanan bir kola sapabilir. Daha hafif başlayan başka bir kol ise grafın neredeyse tamamını dolaşabilir. Algoritmanın bütün olası düğüm sıralamalarını hesaba katması gerekebilir; bu olasılık sayısı üstel biçimde büyür.

## Hamilton Yolu bağlantısı

Zorluğu göstermenin klasik yolu, **Hamilton Yolu Problemi** ile ilişki kurmaktır. Hamilton yolu, graftaki her düğümü tam bir kez ziyaret eden basit bir yoldur ve bu karar problemi NP-tamdır.

Ağırlıksız bir grafta her kenara $1$ ağırlığını verelim. $\vert V\vert =n$ düğüm varsa Hamilton yolu tam olarak $n-1$ kenar içerir. Şu soruyu sorabiliriz:

$$
\text{Uzunluğu en az } n-1 \text{ olan basit bir yol var mı?}
$$

Bu soruya cevap verebilen bir en uzun yol algoritması, Hamilton yolu olup olmadığını da belirler. Dönüşüm polinom zamanda yapıldığı için en uzun yol problemi NP-zordur. Ayrıca verilen bir yolun basit olduğunu ve hedef uzunluğa ulaştığını hızlıca doğrulayabildiğimizden karar sürümü NP-tamdır.

## Her graf türünde umutsuz muyuz?

Hayır! Graf bir **DAG**, yani yönlendirilmiş döngüsüz graf ise topolojik sıralama sayesinde problem $O(\vert V\vert +\vert E\vert )$ zamanda çözülebilir. Döngü bulunmadığından geçmiş bir düğüme dönme ihtimali yoktur.

```python
def longest_path_dag(vertices, edges, order, source):
    dist = {v: float("-inf") for v in vertices}
    dist[source] = 0

    for u in order:
        if dist[u] == float("-inf"):
            continue
        for v, weight in edges[u]:
            dist[v] = max(dist[v], dist[u] + weight)

    return dist
```

Kod, düğümleri topolojik sırayla işler. `dist[v]`, kaynaktan `v` düğümüne bulunan en uzun mesafeyi saklar; her kenar yalnızca bir kez gevşetilir. Bu, en kısa yol gevşetmesine benzer, fakat `min` yerine `max` kullanılır.

Genel graflarda ise kesin çözüm için geri izleme, bitmask dinamik programlama veya dal-sınır yöntemleri kullanılabilir. Büyük örneklerde yaklaşım algoritmaları ve sezgiseller tercih edilir. Kısacası tek kelimelik “en” değişikliği, kolay bir rota probleminden kombinatoryal bir labirente geçmemize yeter!
