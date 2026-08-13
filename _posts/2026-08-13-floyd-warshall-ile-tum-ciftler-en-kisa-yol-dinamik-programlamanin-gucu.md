---
layout: post
title: "Floyd-Warshall ile Tüm Çiftler En Kısa Yol: Dinamik Programlamanın Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - dinamik programlama
  - graf
  - floyd-warshall
---

Bir şehir haritasında her kavşaktan diğer tüm kavşaklara en kısa yolu aynı anda bulmak istediğinizi düşünün. Floyd-Warshall algoritması tam olarak bu işi yapar: ağırlıklı bir graftaki **tüm düğüm çiftleri** arasındaki en kısa mesafeleri hesaplar. Tek kaynaklı Dijkstra'nın aksine, başlangıç düğümünü tekrar tekrar değiştirmek zorunda kalmazsınız. Negatif ağırlıklı kenarları da desteklemesi, onu özellikle maliyet farkları, kur dönüşümleri ve bağımlılık analizleri gibi senaryolarda değerli kılar.
``

Algoritmanın kalbi dinamik programlamadır. Düğümleri `0` ile `n-1` arasında numaralandıralım. `D[k][i][j]`, yalnızca ilk `k` düğümün ara durak olarak kullanılmasına izin verildiğinde `i` düğümünden `j` düğümüne olan en kısa mesafeyi temsil etsin. Her yeni ara düğüm, mevcut en iyi yol ile bu düğümden geçen alternatif arasında bir yarış başlatır:

$$
d_k(i,j) = \min\big(d_{k-1}(i,j),\; d_{k-1}(i,k) + d_{k-1}(k,j)\big)
$$

Bu formülün sezgisi oldukça nettir: `i`den `j`ye giderken ya `k` düğümüne hiç uğramazsınız ya da rota `i → k → j` biçiminde iki parçaya ayrılır. Üç boyutlu tablo tutmak teorik olarak mümkündür; ancak her adım yalnızca bir önceki değerleri kullandığından, tek bir `dist` matrisi yerinde güncellenebilir.

Başlangıç koşulları da önemlidir. Bir düğümün kendisine uzaklığı `0`dır. Doğrudan kenar varsa ağırlığı matrise yazılır; kenar yoksa ulaşılmazlığı temsil etmek için $\infty$ kullanılır. Paralel kenarlarda ise en küçük ağırlık korunmalıdır.

| Durum | `dist[i][j]` başlangıç değeri |
|---|---:|
| `i = j` | `0` |
| `i → j` doğrudan kenarı var | Kenarın ağırlığı |
| Doğrudan bağlantı yok | $\infty$ |

Python ile temel uygulama aşağıdaki gibidir. Kritik ayrıntı, en dış döngünün ara düğüm `k` olmasıdır; döngü sırası değiştirilirse dinamik programlama varsayımı bozulabilir.

```python
INF = float("inf")

def floyd_warshall(n, edges):
    dist = [[INF] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, v, weight in edges:
        dist[u][v] = min(dist[u][v], weight)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                via_k = dist[i][k] + dist[k][j]
                if via_k < dist[i][j]:
                    dist[i][j] = via_k

    return dist
```

Kod, her `k` için bütün başlangıç-bitiş çiftlerini dener. `via_k` değeri, `i`den önce `k`ya sonra `j`ye gitmenin maliyetidir. Python'da `inf + sayı` yine `inf` olduğundan, ulaşılamayan yollar için ek bir kontrol yazmadan güvenli karşılaştırma yapılabilir.

Floyd-Warshall'ın zaman karmaşıklığı $O(V^3)$, bellek tüketimi ise $O(V^2)$dir. Bu nedenle binlerce düğümlü seyrek graflarda her kaynak için Dijkstra çalıştırmak daha iyi olabilir. Buna karşılık, düğüm sayısı orta seviyedeyse ve çok sayıda mesafe sorgusu yapılacaksa tek seferlik matris hesabı son derece pratiktir.

| Özellik | Floyd-Warshall | Dijkstra |
|---|---|---|
| Problem türü | Tüm çiftler | Tek kaynak |
| Negatif kenar | Destekler | Desteklemez |
| Zaman | $O(V^3)$ | Tipik olarak $O((V+E)\log V)$ |
| Negatif döngü tespiti | Evet | Hayır |

Negatif döngüler özel bir tuzaktır: Bir döngünün toplam ağırlığı negatifse, o döngü etrafında tekrar tekrar dolaşarak maliyeti sınırsız azaltabilirsiniz; dolayısıyla anlamlı bir “en kısa” yol yoktur. Algoritma sonunda herhangi bir `dist[i][i] < 0` ise graf negatif döngü içerir. Böylece Floyd-Warshall yalnızca rota hesaplayan değil, veri modelinizdeki maliyet tutarsızlıklarını da ortaya çıkaran güçlü bir analiz aracına dönüşür.
