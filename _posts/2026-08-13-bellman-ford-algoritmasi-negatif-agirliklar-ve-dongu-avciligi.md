---
layout: post
title: "Bellman-Ford Algoritması: Negatif Ağırlıklar ve Döngü Avcılığı"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - graf teorisi
  - bellman-ford
---

En kısa yol problemleri, haritalardaki rota bulmadan ağ paketlerinin yönlendirilmesine kadar pek çok sistemin kalbinde yer alır. Ancak her yolun maliyeti pozitif olmak zorunda değildir: indirimler, kazançlar veya enerji geri kazanımı gibi senaryolar negatif ağırlıklı kenarlar üretir. Dijkstra bu durumda güvenilirliğini kaybederken Bellman-Ford algoritması sahneye çıkar. Üstelik yalnızca en kısa mesafeleri bulmaz; maliyetin sonsuza kadar azaltılabildiği negatif döngüleri de yakalar.

``

Bir grafı $G=(V,E)$ ile gösterelim. Burada $V$ düğüm kümesi, $E$ ise yönlü kenar kümesidir. Her $(u,v)$ kenarının bir $w(u,v)$ ağırlığı vardır. Amaç, kaynak düğüm $s$ için diğer düğümlere ulaşmanın en düşük toplam maliyetini, yani $d[v]$ değerlerini hesaplamaktır. Başlangıçta $d[s]=0$, erişilemeyen tüm düğümler için ise $d[v]=\infty$ atanır.

Bellman-Ford'un temel fikri **gevşetme** (relaxation) işlemidir. Bir kenar üzerinden daha ucuz bir rota keşfedilirse hedef düğümün mesafesi güncellenir:

$$d[v] = \min(d[v],\ d[u] + w(u,v))$$

Bu formülün küçük ama güçlü bir anlamı vardır: Kaynağa giden en iyi yolun, bir önceki düğüme kadar olan en iyi yolun üzerine son kenarın maliyetinin eklenmesiyle kurulabileceğini söyler. Algoritma tüm kenarları $$\vert V \vert-1$$ kez dolaşır. Çünkü negatif döngü içermeyen basit bir yol en fazla $$ \vert V \vert -1$$ kenardan oluşabilir.

| Özellik | Dijkstra | Bellman-Ford |
|---|---|---|
| Negatif kenar ağırlığı | Desteklemez | Destekler |
| Negatif döngü tespiti | Yapamaz | Yapabilir |
| Zaman karmaşıklığı | Genellikle $O((V+E)\log V)$ | $O(VE)$ |
| Temel yaklaşım | En yakın düğümü kesinleştirir | Kenarları tekrar tekrar gevşetir |
| Uygun kullanım | Pozitif maliyetli büyük ağlar | Finans, kur dönüşümü, kısıt analizi |

Negatif ağırlığın neden sorun çıkardığını düşünelim. Dijkstra, en küçük geçici mesafeye sahip düğümü seçtiğinde onun maliyetinin artık değişmeyeceğini varsayar. Fakat ileride karşılaşılan negatif bir kenar bu maliyeti düşürebilir. Bellman-Ford ise acele etmez; bütün kenarları yineleyerek bu iyileştirmelerin graf boyunca yayılmasına izin verir.

Asıl dramatik durum negatif döngüdür. Örneğin $A \to B$ maliyeti $2$, $B \to C$ maliyeti $-5$ ve $C \to A$ maliyeti $1$ olsun. Döngünün toplamı $2-5+1=-2$ olur. Bu döngü her turda toplam maliyeti 2 azaltır. Dolayısıyla gerçek bir “en kısa” yol yoktur; döngü istenildiği kadar dönülerek maliyet $-\infty$ değerine yaklaştırılabilir.

Algoritma, $$|V|-1$$ tur bittikten sonra tüm kenarları bir kez daha kontrol eder. Hâlâ bir kenar gevşetilebiliyorsa kaynak düğümden erişilebilen negatif döngü vardır. Python ile temel uygulama şöyledir:

```python
def bellman_ford(vertex_count, edges, source):
    INF = float("inf")
    dist = [INF] * vertex_count
    dist[source] = 0

    # En fazla V-1 kenarlı basit yolların maliyetini yayar.
    for _ in range(vertex_count - 1):
        changed = False
        for u, v, weight in edges:
            if dist[u] != INF and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                changed = True
        if not changed:
            break  # Yeni iyileştirme yoksa erken çıkış güvenlidir.

    # Bir ek iyileştirme negatif döngü işaretidir.
    for u, v, weight in edges:
        if dist[u] != INF and dist[u] + weight < dist[v]:
            raise ValueError("Kaynak tarafından erişilen negatif döngü bulundu")

    return dist
```

Buradaki `changed` bayrağı pratik bir optimizasyondur: Bazı turlarda hiçbir mesafe değişmiyorsa sonraki turların da sonucu değiştirmeyeceği anlaşılır. Bununla birlikte en kötü durum karmaşıklığı hâlâ $O(VE)$'dir. Bu nedenle Bellman-Ford, çok yoğun ve devasa grafiklerde ilk tercih olmayabilir; fakat negatif maliyetlerin anlam taşıdığı problemlerde doğruluk, hızdan daha değerlidir.

Kısacası Bellman-Ford bir rota bulucudan fazlasıdır: Sistemde maliyeti sınırsız azaltan mantıksal bir açık olup olmadığını denetler. Özellikle döviz arbitrajı, bağımlılık kısıtları ve ağ protokollerinde bu “bir tur daha kontrol et” yaklaşımı, görünmeyen sorunları ortaya çıkaran güvenilir bir emniyet kemeridir.
