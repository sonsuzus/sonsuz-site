---
layout: post
title: "Zamanı İleri Sar: Olay-Güdümlü Benzetimle Parçacık Çarpışmaları"
math: true
categories: 
  - Bilgi
tags: 
  - olay-güdümlü benzetim
  - simülasyon
  - algoritma
  - python
  - fizik
  - öncelik kuyruğu
toc: true
image: /img/zamani-ileri-sar-97.png
---

Bir bilardo masasındaki topları simüle ettiğimizi düşünelim. Zamanı milisaniyelik dilimlere ayırıp her adımda bütün topların konumunu güncelleyebiliriz. Ancak toplar çoğu zaman yalnızca düz bir çizgide ilerler; asıl ilginç değişimler çarpışma anlarında gerçekleşir. Olay-güdümlü benzetim, boş geçen zaman adımlarını hesaplamak yerine doğrudan bir sonraki önemli olaya sıçrayarak işlem yapar.


![zamani-ileri-sar-97](/img/zamani-ileri-sar-97.svg)

``

## Zaman adımlı ve olay-güdümlü yaklaşım

Geleneksel zaman adımlı benzetimde saat, sabit bir $\Delta t$ miktarıyla ilerletilir. Bir parçacığın yeni konumu yaklaşık olarak

$$
\vec{x}(t + \Delta t) = \vec{x}(t) + \vec{v}(t)\Delta t
$$

şeklinde hesaplanır. $\Delta t$ küçüldükçe sonuç genellikle daha hassas olur, fakat işlem sayısı artar. Üstelik hızlı parçacıklar büyük bir zaman adımında birbirlerinin içinden geçebilir. Buna tünelleme problemi denir.

Olay-güdümlü yaklaşımda ise sistemin gelecekteki çarpışma zamanları hesaplanır. Benzetim saati en yakın olaya taşınır, ilgili parçacıkların durumları değiştirilir ve bu değişiklikten etkilenen yeni olaylar planlanır.

| Özellik | Zaman adımlı benzetim | Olay-güdümlü benzetim |
|---|---|---|
| Zamanın ilerlemesi | Sabit $\Delta t$ | Bir sonraki olay zamanı |
| Boş hareket dönemleri | Tek tek hesaplanır | Doğrudan atlanır |
| Çarpışma hassasiyeti | Adım boyuna bağlıdır | Analitik zamana dayanır |
| Uygulama kolaylığı | Genellikle daha kolay | Olay yönetimi daha karmaşıktır |
| Uygun sistemler | Sürekli kuvvetler, akışkanlar | Sert küreler, kuyruklar, ağ paketleri |

## Çarpışma zamanı nasıl bulunur?

Yarıçapları $r_1$ ve $r_2$ olan iki parçacığın konum farkını $\Delta\vec{x}$, hız farkını da $\Delta\vec{v}$ olarak tanımlayalım. Çarpışma anında merkezler arasındaki uzaklık, yarıçapların toplamına eşittir:

$$
\left\vert \Delta\vec{x} + \Delta\vec{v}t\right\vert  = r_1 + r_2
$$

Denklemin karesi alındığında $at^2+bt+c=0$ biçiminde ikinci dereceden bir denklem elde edilir. Pozitif ve en küçük kök, gelecekteki ilk çarpışma zamanıdır. Diskler birbirinden uzaklaşıyorsa veya diskriminant negatifse çarpışma olayı oluşturulmaz.

Çarpışma gerçekleştiğinde hızlar momentum ve enerji korunumu kullanılarak güncellenir. Toplam momentum için

$$
m_1\vec{v}_1 + m_2\vec{v}_2 = m_1\vec{v}'_1 + m_2\vec{v}'_2
$$

olmalıdır. Esnek çarpışmada kinetik enerji de korunur. Böylece benzetim yalnızca görsel olarak değil, fiziksel olarak da tutarlı kalır.

## Öncelik kuyruğu: Benzetimin ajandası

Gelecekteki olaylar, olay zamanına göre sıralanan bir **öncelik kuyruğunda** tutulur. En yakın olay kuyruğun başından alınır. Python'daki `heapq`, bu iş için uygun bir min-heap sağlar.

```python
import heapq

queue = []
current_time = 0.0

def schedule(time, kind, particles):
    # Olayları gerçekleşme zamanına göre kuyruğa ekler.
    heapq.heappush(queue, (time, kind, particles))

schedule(1.25, "collision", (0, 3))
schedule(0.80, "wall", (2,))

while queue:
    event_time, kind, particles = heapq.heappop(queue)
    current_time = event_time

    if kind == "collision":
        resolve_collision(*particles)
    elif kind == "wall":
        reflect_from_wall(*particles)

    predict_new_events(particles, current_time)
```

Kod, zamanı küçük adımlarla artırmaz; saati doğrudan `event_time` değerine taşır. Olay işlendikten sonra yalnızca etkilenen parçacıklarla ilgili tahminlerin yenilenmesi önemli bir optimizasyondur.

## Geçersiz olaylar ve pratik zorluklar

Bir parçacık için önceden hesaplanan olay, araya başka bir çarpışma girdiğinde geçersiz olabilir. Her parçacıkta bir çarpışma sayacı tutularak olay oluşturulurken sayaç değerleri kaydedilebilir. Olay işlenmeden önce değerler karşılaştırılır; uyuşmuyorsa eski olay çöpe atılır.

Olay-güdümlü benzetim her problem için sihirli değnek değildir. Yerçekimi veya sürtünme gibi sürekli etkiler baskınsa olay zamanlarını analitik biçimde bulmak zorlaşır. Buna karşılık seyrek ve ani değişimlerin bulunduğu sistemlerde, zamanı adımlamak yerine olaydan olaya zıplamak hem daha hızlı hem de daha hassas bir dijital evren kurar.
