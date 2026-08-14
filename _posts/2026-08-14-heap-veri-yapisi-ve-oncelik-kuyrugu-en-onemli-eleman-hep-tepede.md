---
layout: post
title: "Heap Veri Yapısı ve Öncelik Kuyruğu: En Önemli Eleman Hep Tepede"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - heap
  - öncelik kuyruğu
  - python
---

Bir iş kuyruğunda herkes sırayla beklemek zorunda değildir: acil bir hata kaydı, normal bir rapordan önce işlenmelidir. İşte **öncelik kuyruğu** bu ihtiyacı çözer; **heap (ikili yığın)** ise en yüksek ya da en düşük öncelikli elemana son derece hızlı ulaşmanın pratik yoludur. Heap, "tam sıralı dizi" kadar katı davranmaz; yalnızca her ebeveynin çocuklarıyla olan ilişkisini düzenler. Bu küçük kural, büyük performans kazancı sağlar.
``

## Heap mantığı: Kısmi sıralama yeterlidir

İkili heap, genellikle dizi içinde tutulan **tam ikili ağaçtır**. Tam ikili ağaçta düğümler seviyeler halinde soldan sağa doldurulur. Dizide indeksler `0` ile başlıyorsa bir düğümün ilişkileri şöyledir:

$$sol(i)=2i+1, \qquad sağ(i)=2i+2, \qquad ebeveyn(i)=\lfloor(i-1)/2\rfloor$$

**Min-heap** kuralında her ebeveyn, çocuklarından küçük veya eşittir. Böylece kökte, yani `heap[0]` konumunda, daima en küçük eleman bulunur. **Max-heap** bunun tersidir: kökte en büyük değer yer alır. Dikkat edilmesi gereken nokta, kardeş düğümlerin kendi aralarında sıralı olmak zorunda olmamasıdır.

| Özellik | Min-Heap | Max-Heap |
|---|---|---|
| Kök eleman | En küçük değer | En büyük değer |
| Öncelik yorumu | Küçük sayı daha acil | Büyük sayı daha acil |
| Tipik kullanım | Zamanlanmış işler, Dijkstra | Skor tablosu, en büyük `k` değer |
| `peek` maliyeti | $O(1)$ | $O(1)$ |

Bir heap'in yüksekliği yaklaşık olarak $\log_2 n$ olduğundan, kökten yaprağa ya da yapraktan köke ilerleyen işlemler logaritmik sürede biter. Bu, neden ekleme ve silmenin hızlı olduğunu açıklar.

## Ekleme ve çıkarma sırasında ne olur?

Yeni eleman önce dizinin sonuna eklenir. Ardından ebeveyniyle karşılaştırılır; heap kuralını bozuyorsa yukarı doğru yer değiştirir. Bu adıma **sift-up** veya *bubble-up* denir. En öncelikli elemanı çıkarmak için kök alınır, son eleman köke taşınır ve uygun konuma inene kadar küçük çocukla değiştirilir. Bu da **sift-down** işlemidir.

| İşlem | Heap | Sıralı dizi | Sırasız dizi |
|---|---:|---:|---:|
| En öncelikliyi görme | $O(1)$ | $O(1)$ | $O(n)$ |
| Ekleme | $O(\log n)$ | $O(n)$ | $O(1)$ |
| En öncelikliyi çıkarma | $O(\log n)$ | $O(n)$ | $O(n)$ |

Aşağıdaki Python örneği, min-heap kullanan küçük ama işlevsel bir öncelik kuyruğu tanımlar. Python'ın yerleşik `heapq` modülü üretim kodunda tercih edilir; burada ise mekanizmayı görünür kılmak için temel algoritmayı kendimiz yazıyoruz.

```python
class MinPriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        i = len(self.heap) - 1
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[parent] <= self.heap[i]:
                break
            self.heap[parent], self.heap[i] = self.heap[i], self.heap[parent]
            i = parent

    def pop(self):
        if not self.heap:
            raise IndexError("Kuyruk boş")
        minimum = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return minimum

    def _sift_down(self, i):
        while 2 * i + 1 < len(self.heap):
            left, right = 2 * i + 1, 2 * i + 2
            child = left
            if right < len(self.heap) and self.heap[right] < self.heap[left]:
                child = right
            if self.heap[i] <= self.heap[child]:
                break
            self.heap[i], self.heap[child] = self.heap[child], self.heap[i]
            i = child
```

Bu sınıfta `push`, yeni işi doğru konuma taşır; `pop` ise en küçük öncelik değerini verir. Örneğin `(öncelik, görev)` ikilileri saklayarak görev sıralaması oluşturabilirsiniz. Eşit önceliklerde kararlı sıralama gerekiyorsa ikiliye artan bir sayaç eklemek akıllıca olur.

Heap, her şeyi sıralamak için değil, **bir sonraki en önemli şeyi** hızla bulmak için tasarlanmıştır. Zamanlayıcılar, grafik algoritmaları, olay sistemleri ve iş planlayıcılarında bu nedenle vazgeçilmezdir.
