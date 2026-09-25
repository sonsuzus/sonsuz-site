---
layout: post
title: "Karp’ın Minimum Ortalama Döngü Algoritmasıyla Graflarda Darboğaz Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - graf algoritmaları
  - karp algoritması
  - dinamik programlama
  - darboğaz analizi
  - python
  - optimizasyon
toc: true
image: /img/karpin-minimum-ortalama-45.png
---

Bir üretim hattı, işlemci görev zinciri veya ağ yönlendirme sistemi düşünün: İşler belirli durumlar arasında sürekli dolaşıyor ve her geçişin bir maliyeti var. Sistemin uzun vadeli sınırını çoğu zaman tek bir pahalı kenar değil, tekrar tekrar kullanılan bir döngünün ortalama maliyeti belirler. Richard Karp’ın minimum ortalama döngü algoritması, tam olarak bu gizli darboğazı polinom zamanda ortaya çıkarır.


![karpin-minimum-ortalama-45](/img/karpin-minimum-ortalama-45.svg)

``

## Minimum ortalama döngü nedir?

Yönlü ve ağırlıklı bir grafı $G=(V,E)$ olarak tanımlayalım. Bir $C$ döngüsünün ortalama ağırlığı, döngüdeki toplam maliyetin kenar sayısına bölünmesidir:

$$
μ(C)=\frac{\sum_{e \in C} w(e)}{\vert C\vert }
$$

Amaç, bütün yönlü döngüler arasında $μ(C)$ değerini en aza indirmektir. Burada aranan şey toplam ağırlığı en düşük döngü değildir. Örneğin iki kenarlı ve toplam ağırlığı 8 olan bir döngünün ortalaması 4; beş kenarlı ve toplam ağırlığı 10 olan başka bir döngünün ortalaması 2’dir. Toplam maliyeti daha yüksek olan ikinci döngü, uzun vadede daha avantajlıdır.

| Ölçüt | Sorduğu soru | Tipik kullanım |
|---|---|---|
| En kısa yol | İki nokta arasında en ucuz rota hangisi? | Navigasyon |
| Minimum toplam döngü | Toplam maliyeti en küçük döngü hangisi? | Yerel optimizasyon |
| Minimum ortalama döngü | Her tekrar başına en ucuz döngü hangisi? | Performans sınırı |
| Maksimum akış | Ağdan ne kadar veri geçirilebilir? | Kapasite analizi |

## Karp’ın dinamik programlama fikri

Grafın $n=\vert V\vert $ düğümü olduğunu varsayalım. Bir başlangıç düğümü $s$ seçilir ve $d_k(v)$, tam olarak $k$ kenar kullanarak $s$ düğümünden $v$ düğümüne ulaşmanın minimum maliyeti olarak tanımlanır:

$$
d_k(v)=\min_{(u,v)\in E}\left(d_{k-1}(u)+w(u,v)\right)
$$

Başlangıçta $d_0(s)=0$, diğer değerler sonsuzdur. Karp’ın önemli sonucu, güçlü bağlı bir graf için minimum döngü ortalamasını şu formülle verir:

$$
μ^*=\min_{v\in V}\max_{0\leq k<n}\frac{d_n(v)-d_k(v)}{n-k}
$$

Neden $n$ adım? Çünkü $n$ düğümlü bir graf üzerinde $n$ kenarlık bir yürüyüş mutlaka en az bir düğümü tekrar ziyaret eder; yani içinde bir döngü bulunur. Farklı $k$ noktalarından kalan parçaların ortalamaları karşılaştırıldığında, tekrarın sürdürülebilir en düşük maliyeti görünür hâle gelir.

## Python ile uygulama

Aşağıdaki kod, düğümleri `0` ile `n-1` arasında numaralanmış bir graf için minimum ortalama değeri hesaplar:

```python
def karp_minimum_cycle_mean(n, edges, source=0):
    inf = float("inf")
    dp = [[inf] * n for _ in range(n + 1)]
    dp[0][source] = 0

    # Tam olarak k kenarlı en ucuz yürüyüşleri hesapla.
    for k in range(1, n + 1):
        for u, v, weight in edges:
            if dp[k - 1][u] != inf:
                candidate = dp[k - 1][u] + weight
                dp[k][v] = min(dp[k][v], candidate)

    answer = inf
    for v in range(n):
        if dp[n][v] == inf:
            continue

        worst_ratio = -inf
        for k in range(n):
            if dp[k][v] != inf:
                ratio = (dp[n][v] - dp[k][v]) / (n - k)
                worst_ratio = max(worst_ratio, ratio)

        answer = min(answer, worst_ratio)

    return answer
```

Dinamik programlama tablosu $n+1$ satır ve $n$ sütun içerir. Her satırda bütün kenarlar gevşetildiği için zaman karmaşıklığı $O(nm)$, bellek karmaşıklığı ise $O(n^2)$ olur. Burada $m=\vert E\vert $ değeridir.

## Darboğaz analizindeki anlamı

Ağırlıklar gecikmeyi temsil ediyorsa minimum ortalama döngü, sistemde tekrar başına erişilebilecek en düşük maliyeti gösterir. Ağırlıklar kazanç veya kapasite olarak yorumlanıyorsa işaretleri değiştirerek maksimum ortalama döngü de bulunabilir. Böylece zamanlanmış devrelerde çevrim süresi, üretim ağlarında tekrar maliyeti ve olay sistemlerinde uzun dönem verimi analiz edilebilir.

Algoritmanın verdiği temel sonuç sayısal ortalamadır; döngünün kenarlarını doğrudan döndürmez. Gerçek döngüyü çıkarmak için öncül düğümler saklanmalı ve tekrar eden düğümler geriye doğru izlenmelidir. Ayrıca graf güçlü bağlı değilse her güçlü bağlı bileşeni ayrı incelemek, ulaşılamayan bölgelerin sonucu bozmasını engeller. Kısacası Karp’ın yaklaşımı, “Sistem sonsuza dek çalışırsa hangi tekrar performansı belirler?” sorusuna matematiksel ve uygulanabilir bir cevap verir.
