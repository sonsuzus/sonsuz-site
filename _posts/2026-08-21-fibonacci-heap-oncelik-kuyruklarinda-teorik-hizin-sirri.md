---
layout: post
title: "Fibonacci Heap: Öncelik Kuyruklarında Teorik Hızın Sırrı"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - algoritmalar
  - öncelik kuyruğu
  - fibonacci heap
---

Öncelik kuyruğu denince çoğumuzun aklına ikili yığın (binary heap) gelir: eleman ekle, en küçüğü al, işlem tamam. Ancak Dijkstra veya Prim gibi algoritmalarda bazı anahtarların değeri sürekli azaltılıyorsa, teorik olarak daha iddialı bir oyuncu sahneye çıkar: **Fibonacci Heap**. Bu veri yapısı, bazı pahalı işleri erteleyerek özellikle `decrease-key` operasyonunu amortismanlı olarak son derece ucuz hâle getirir.
``

Fibonacci Heap, tek bir ağaç yerine bir **kök listesi** tutar. Bu listedeki her düğüm, başka düğümlerin kökü olabilir; yani yapı bir orman gibidir. Ayrıca en küçük anahtara sahip düğüm için doğrudan bir işaretçi saklanır. Bu sayede minimum değeri bulmak için listenin tamamını gezmek gerekmez. Temel fikir şudur: Ekleme sırasında düzeni korumak için fazla çalışmayalım; asıl düzenlemeyi minimum çıkarılırken yapalım.

Bu yaklaşımı anlamak için amortismanlı analiz gerekir. Tek bir işlemin anlık maliyeti yüksek olabilir, fakat uzun bir işlem dizisindeki ortalama maliyet düşüktür. Fibonacci Heap için yaygın potansiyel fonksiyonu şöyledir:

$$\Phi(H) = t(H) + 2m(H)$$

Burada $t(H)$ kök sayısını, $m(H)$ ise işaretlenmiş düğüm sayısını ifade eder. Bir düğüm çocuklarından birini kaybettiğinde işaretlenebilir. İkinci çocuğunu da kaybederse ebeveyninden kesilerek kök listesine taşınır. Bu olaya **cascading cut** denir. Potansiyel fonksiyon, ertelenen düzenleme maliyetinin teorik muhasebesini tutar.

| İşlem | Binary Heap | Fibonacci Heap amortismanlı |
|---|---:|---:|
| `insert` | $O(\log n)$ | $O(1)$ |
| `find-min` | $O(1)$ | $O(1)$ |
| `extract-min` | $O(\log n)$ | $O(\log n)$ |
| `decrease-key` | $O(\log n)$ | $O(1)$ |
| `merge` | $O(n)$ veya $O(\log n)$ | $O(1)$ |

`insert` işlemi oldukça rahat davranır: Yeni düğüm kök listesine eklenir ve gerekiyorsa minimum işaretçisi güncellenir. Benzer şekilde iki Fibonacci Heap birleştirmek, iki kök listesini birbirine bağlamaktan ibarettir. Asıl hareket `extract-min` sırasında yaşanır. Minimum düğümün çocukları kök listesine alınır; ardından aynı dereceye sahip ağaçlar birleştirilerek **consolidation** yapılır. Derecesi küçük olan kök, derecesi büyük olanın çocuğu olur; anahtar karşılaştırması ise hangi kökün üstte kalacağını belirler.

Aşağıdaki sadeleştirilmiş Python örneği, ekleme mantığını gösterir. Gerçek bir uygulamada düğümlerin kardeş, ebeveyn, çocuk ve işaret durumları da yönetilmelidir.

```python
class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.child = None
        self.degree = 0
        self.mark = False

class FibonacciHeap:
    def __init__(self):
        self.roots = []
        self.minimum = None

    def insert(self, key):
        node = Node(key)
        self.roots.append(node)  # Düzenleme ertelenir.
        if self.minimum is None or key < self.minimum.key:
            self.minimum = node
        return node
```

Bu kodun kritik noktası, eklerken ağaçları yeniden dengelememesidir. Dolayısıyla işlem anlık olarak $O(1)$ sürer. Fakat kök listesi büyür; borç, ileride `extract-min` tarafından tahsil edilir. Veri yapılarında bazen temizlik işini sonraya bırakmak gerçekten stratejidir!

Fibonacci Heap özellikle teorik analizlerde ve çok sayıda `decrease-key` çağrısı içeren grafik algoritmalarında anlamlıdır. Örneğin Dijkstra algoritmasının klasik karmaşıklığı, uygun kullanımda $O(E + V\log V)$ seviyesine iner. Buna karşın pratikte Fibonacci Heap; karmaşık bağlantıları, hata yapmaya açık kesme işlemleri ve yüksek sabit maliyetleri nedeniyle çoğu zaman ikili heap kadar popüler değildir.

| Senaryo | Daha mantıklı tercih | Neden |
|---|---|---|
| Genel amaçlı uygulama | Binary Heap | Basit, önbellek dostu, uygulanması kolay |
| Teorik Dijkstra/Prim analizi | Fibonacci Heap | `decrease-key` için $O(1)$ amortismanlı maliyet |
| Birçok kuyruğun birleşmesi | Fibonacci Heap | `merge` işlemi $O(1)$ |

Özetle Fibonacci Heap, her durumda en hızlı pratik araç değil; fakat amortismanlı analizin gücünü gösteren olağanüstü bir veri yapısıdır. Onun mesajı nettir: Bazı işleri hemen yapmak zorunda değilsiniz; doğru zamanda yapılan toplu düzenleme, algoritmik olarak büyük kazanç sağlayabilir.
