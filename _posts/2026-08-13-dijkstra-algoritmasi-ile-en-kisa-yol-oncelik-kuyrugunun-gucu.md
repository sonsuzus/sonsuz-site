---
layout: post
title: "Dijkstra Algoritması ile En Kısa Yol: Öncelik Kuyruğunun Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - graf teorisi
  - python
  - dijkstra
  - veri yapıları
image: /img/dijkstra-algoritmasi-ile-15.png
---

Bir harita uygulamasının sizi en kısa rotadan götürmesi, ağ paketlerinin hızlı yolu seçmesi veya bir oyundaki karakterin hedefe ulaşması çoğu zaman aynı soruya dayanır: Ağırlıklı bir graf üzerinde iki nokta arasındaki en düşük maliyetli yol nedir? Dijkstra algoritması, kenar ağırlıkları negatif olmadığı sürece bu soruyu sistematik ve oldukça verimli biçimde çözer.


![dijkstra-algoritmasi-ile-15](/img/dijkstra-algoritmasi-ile-15.svg)

``

## Graf ve maliyet fikri

Graf, düğümlerden (vertex) ve bu düğümleri bağlayan kenarlardan (edge) oluşur. Bir yolun maliyeti, geçtiği kenarların ağırlık toplamıdır. Başlangıç düğümü $s$, hedef düğüm $t$ ve yol üzerindeki kenar ağırlıkları $w(e)$ ise:

$$
\operatorname{cost}(P)=\sum_{e \in P} w(e)
$$

Dijkstra'nın amacı, her düğüm $v$ için başlangıçtan olan en küçük uzaklığı, yani $d(s,v)$ değerini hesaplamaktır. Algoritma önce tüm uzaklıkları sonsuz kabul eder; yalnızca başlangıç düğümünün uzaklığı sıfırdır. Ardından "şu anda en yakın görünen" düğümü seçer ve komşularına daha ucuz bir yol bulunup bulunmadığını kontrol eder. Bu güncelleme işlemine **relaxation (gevşetme)** denir:

$$
\text{eğer } d[u] + w(u,v) < d[v] \text{ ise } d[v] \leftarrow d[u] + w(u,v)
$$

| Kavram | Anlamı | Dijkstra'daki rolü |
|---|---|---|
| Düğüm | Konum, şehir veya sunucu | Yolun duraklarını temsil eder |
| Kenar | İki düğüm arasındaki bağlantı | Geçiş imkânını belirtir |
| Ağırlık | Mesafe, süre ya da ücret | Optimize edilen maliyettir |
| Uzaklık dizisi | Bilinen en iyi maliyetler | Algoritmanın sonuç tablosudur |

## Neden öncelik kuyruğu kullanılır?

Basit bir uygulamada her turda en küçük uzaklıklı düğümü bulmak için bütün düğümler taranabilir. Ancak bu yaklaşım büyük graflarda pahalıdır. Min-heap tabanlı bir **öncelik kuyruğu**, en küçük geçici uzaklığa sahip düğümü doğrudan üstte tutar.

Başlangıçta kuyrukta $(0,s)$ çifti bulunur. Kuyruktan çıkarılan $u$ düğümünün mesafesi, negatif ağırlık olmadığı için artık kesinleşir. Çünkü $u$ya daha kısa bir yol, henüz ziyaret edilmemiş ve daha pahalı bir düğüm üzerinden gelemez. Bu açgözlü seçim, algoritmanın temel doğruluk fikridir.

| Yaklaşım | En küçük düğümü seçme | Tipik zaman karmaşıklığı |
|---|---:|---:|
| Dizi ile tarama | $O(V)$ | $O(V^2)$ |
| Binary heap öncelik kuyruğu | $O(\log V)$ | $O((V+E)\log V)$ |
| BFS | Kuyruk sırası | Yalnızca eşit ağırlıklı kenarlar için $O(V+E)$ |

## Python ile uygulama

Aşağıdaki örnek, grafı komşuluk listesiyle tutar. Kuyrukta eski uzaklık kayıtları kalabileceğinden, çıkarılan kaydın güncel olup olmadığı ayrıca kontrol edilir. Bu yöntem Python'un `heapq` modülüyle pratik bir "decrease-key" alternatifi sunar.

```python
import heapq

def dijkstra(graf, baslangic):
    uzaklik = {dugum: float("inf") for dugum in graf}
    onceki = {dugum: None for dugum in graf}
    uzaklik[baslangic] = 0
    kuyruk = [(0, baslangic)]

    while kuyruk:
        maliyet, u = heapq.heappop(kuyruk)

        # Kuyruktaki eski kaydı atla.
        if maliyet != uzaklik[u]:
            continue

        for v, agirlik in graf[u]:
            yeni_maliyet = maliyet + agirlik
            if yeni_maliyet < uzaklik[v]:
                uzaklik[v] = yeni_maliyet
                onceki[v] = u
                heapq.heappush(kuyruk, (yeni_maliyet, v))

    return uzaklik, onceki
```

`onceki` sözlüğü, yalnızca mesafeyi değil yolun kendisini de üretmeye yarar. Hedeften başlayıp önceki düğümlere doğru ilerleyerek rota ters sırada bulunur; sonra liste ters çevrilir. Örneğin sonuçta `onceki["D"] = "B"` ise, en iyi bilinen rotada D'ye B üzerinden gelinmiştir.

## Kritik sınır: negatif kenarlar

Dijkstra, negatif ağırlıklı kenarlarda güvenilir değildir. Bir düğümün uzaklığını kesinleştirdikten sonra, ileride bulunan negatif bir kenar bu mesafeyi azaltabilir. Böyle bir durumda Bellman-Ford algoritması tercih edilmelidir. Negatif döngüler varsa ise "en kısa yol" kavramı bile bozulur: döngü tekrarlandıkça maliyet sınırsız biçimde düşebilir.

Özetle Dijkstra; teslimat rotaları, ağ yönlendirme ve oyun haritaları için güçlü bir araçtır. Doğru veri yapısı olan öncelik kuyruğu eklendiğinde, büyük ve seyrek graflarda bile hızlı sonuç üretir.
