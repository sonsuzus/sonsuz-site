---
layout: post
title: "Ray Tracing Temelleri: Işığın Peşinden Gerçekçiliğe"
math: true
categories: 
  - Bilgi
tags: 
  - ray tracing
  - bilgisayar grafikleri
  - ışık simülasyonu
  - render
  - 3d programlama
  - vektör matematiği
toc: true
image: /img/ray-tracing-temelleri-92.png
---

Bir sahneyi gerçekçi göstermek istiyorsanız yalnızca nesneleri çizmek yetmez; ışığın dünyada nasıl davrandığını da düşünmeniz gerekir. Ray tracing, yani ışın izleme, tam olarak bunu yapar: Kameradan hayali ışınlar gönderir, bu ışınların nesnelerle karşılaşmasını hesaplar ve her pikselin rengini belirler. Kısacası yöntem, dijital bir sahnede ışığa dedektif şapkası takar.

``

## Temel fikir: Pikselden sahneye yolculuk

Gerçek dünyada ışık, kaynaktan çıkarak nesnelere çarpar ve gözümüze ulaşır. Ancak bir ışık kaynağından yayılan milyarlarca ışının çoğu kameraya hiç gelmez. Bunların tamamını simüle etmek pahalıdır. Bu nedenle klasik ray tracing süreci ters yönde çalışır: Her piksel için kameradan sahneye bir ışın gönderilir.

Bir ışın matematiksel olarak şöyle tanımlanır:

$$
R(t) = O + tD
$$

Burada $O$ ışının başlangıç noktası, $D$ normalize edilmiş yön vektörü ve $t \geq 0$ ışın boyunca alınan mesafedir. $t$ büyüdükçe ışın, başlangıç noktasından daha uzağa gider.

## Işın ve nesne kesişimi

Gönderilen ışının sahnedeki hangi nesneye önce çarptığını bulmamız gerekir. Örneğin merkezi $C$, yarıçapı $r$ olan bir kürenin yüzeyindeki her $P$ noktası şu koşulu sağlar:

$$
\lVert P-C \rVert^2 = r^2
$$

$P$ yerine ışın denklemi yerleştirildiğinde ikinci dereceden bir denklem elde edilir. Denklemin diskriminantı kesişimin durumunu anlatır:

| Diskriminant | Sonuç | Görsel anlamı |
|---|---|---|
| $\Delta < 0$ | Kesişim yok | Işın küreyi ıskalar |
| $\Delta = 0$ | Tek kesişim | Işın küreye teğettir |
| $\Delta > 0$ | İki kesişim | Işın kürenin içinden geçer |

![ray-tracing-temelleri-92](/img/ray-tracing-temelleri-92.svg)


Pozitif olan en küçük $t$ değeri, kameraya en yakın görünür yüzeyi verir. Böylece arkadaki nesnenin yanlışlıkla öndeymiş gibi çizilmesi engellenir.

## Yüzey neden aydınlık görünür?

Kesişim noktasını bulmak yalnızca başlangıçtır. Şimdi yüzey normalini, ışık yönünü ve malzeme özelliklerini kullanarak renk hesaplanır. Basit Lambert aydınlatmasında dağınık ışık şiddeti şöyledir:

$$
I_d = k_d I_L \max(0, N \cdot L)
$$

$N$ yüzey normali, $L$ ışığa doğru yön, $k_d$ malzemenin dağınık yansıma katsayısıdır. İki vektör aynı yöne yaklaştıkça noktasal çarpım büyür ve yüzey daha aydınlık görünür.

```python
def lambert(normal, light_dir, base_color, intensity):
    brightness = max(0.0, dot(normal, light_dir))
    return base_color * brightness * intensity
```

Bu fonksiyon, normal ile ışık yönünün noktasal çarpımını kullanarak yüzey rengini ölçekler. Sonuç negatifse ışık yüzeyin arkasındadır ve katkı sıfırlanır.

## Gölge, yansıma ve kırılma

Bir noktanın gölgede olup olmadığını anlamak için kesişim noktasından ışık kaynağına doğru yeni bir **gölge ışını** gönderilir. Arada başka bir nesne varsa doğrudan ışık engellenmiştir.

Yansıtıcı yüzeylerde gelen $D$ yönü, normal $N$ üzerinden şu şekilde yansıtılır:

$$
R = D - 2(D \cdot N)N
$$

Ardından yansıma yönünde yeni bir ışın oluşturulur. Saydam malzemelerde ise Snell yasasına dayalı kırılma hesabı yapılır. Her yeni ışın başka ışınlar üretebildiğinden işlem küçük bir soy ağacına dönüşebilir.

| Özellik | Ek ışın | Maliyet |
|---|---|---|
| Doğrudan renk | Birincil ışın | Düşük |
| Gölge | Işığa doğru ışın | Orta |
| Yansıma | Sekonder ışın | Yüksek |
| Kırılma | Malzeme içi ışın | Yüksek |

## Performans neden zorlayıcıdır?

Milyonlarca piksel, çok sayıda nesne ve tekrarlanan yansımalar ciddi hesaplama yükü oluşturur. Bu yüzden BVH gibi hızlandırma yapıları, ışının her nesneyle tek tek test edilmesini önler. Ayrıca maksimum yansıma derinliği belirlenir; örneğin beş sekmeden sonra süreç durdurulur.

Ray tracing’in özü şaşırtıcı derecede sadedir: ışın gönder, en yakın kesişimi bul, ışığı hesapla ve gerekiyorsa yeni ışınlar üret. Gerçekçilik ise bu basit döngünün gölge, malzeme, örnekleme ve performans teknikleriyle sabırla zenginleştirilmesinden doğar.
