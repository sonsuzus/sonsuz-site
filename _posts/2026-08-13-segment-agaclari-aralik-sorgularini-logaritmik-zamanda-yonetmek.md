---
layout: post
title: "Segment Ağaçları: Aralık Sorgularını Logaritmik Zamanda Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - algoritmalar
  - segment ağacı
---

Bir dizide belirli bir aralığın toplamını, minimumunu ya da maksimumunu sıkça hesaplamanız gerekiyorsa, düz bir yaklaşım hızla pahalılaşır. Örneğin her sorguda elemanları tek tek gezmek $O(n)$ sürer; dizi de güncelleniyorsa önceden hesaplanmış önek toplamları bile yetersiz kalır. Segment ağacı (segment tree), bu iki ihtiyacı dengeler: Hem aralık sorgularını hem de noktasal güncellemeleri $O(\log n)$ zamanda gerçekleştirir.
``

Temel fikir, diziyi sürekli iki parçaya ayıran ikili bir ağaç kurmaktır. Kök düğüm tüm diziyi, çocuklar ise onun sol ve sağ yarılarını temsil eder. Her düğüm kendi aralığı için bir özet değer saklar. Toplam sorgusunda bu değer toplam, minimum sorgusunda minimum, maksimum sorgusunda ise maksimumdur. Böylece `[l, r]` aralığı sorulduğunda ağaç yalnızca gerekli parçaları ziyaret eder.

Bir dizinin uzunluğu $n$ olsun. Ağacın yüksekliği yaklaşık $\log_2 n$ olur. Sorgu sırasında bir düğümün aralığı tamamen istenen aralığın dışındaysa atlanır; tamamen içindeyse sakladığı özet doğrudan kullanılır; kısmen kesişiyorsa çocuklarına inilerek sonuçlar birleştirilir. Toplam için birleştirme işlemi basitçe toplama işlemidir:

$$
S([l,r]) = S([l,m]) + S([m+1,r])
$$

Buradaki $m = \lfloor(l+r)/2\rfloor$ orta noktadır. Bu yapı yalnızca toplama için değildir. Birleştirme işlemi **birleşmeli** olduğu sürece segment ağacı kullanılabilir. Başka bir deyişle, $(a \circ b) \circ c = a \circ (b \circ c)$ koşulu sağlanmalıdır.

| Yaklaşım | Aralık toplamı | Noktasal güncelleme | En uygun kullanım |
|---|---:|---:|---|
| Doğrudan tarama | $O(n)$ | $O(1)$ | Çok az sorgu |
| Önek toplamı | $O(1)$ | $O(n)$ | Değişmeyen diziler |
| Fenwick ağacı | $O(\log n)$ | $O(\log n)$ | Özellikle toplamlar |
| Segment ağacı | $O(\log n)$ | $O(\log n)$ | Min, max, GCD ve esnek sorgular |

Aşağıdaki Python örneği, toplam sorgusu yapan ve tek bir indeksi güncelleyen bir segment ağacını gösterir. Dizi tabanlı temsil kullanıldığı için düğüm çocukları `2*node` ve `2*node+1` indislerinde tutulur.

```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, left, right):
        if left == right:
            self.tree[node] = data[left]
            return
        mid = (left + right) // 2
        self._build(data, node * 2, left, mid)
        self._build(data, node * 2 + 1, mid + 1, right)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def query(self, ql, qr, node=1, left=0, right=None):
        right = self.n - 1 if right is None else right
        if qr < left or right < ql:
            return 0
        if ql <= left and right <= qr:
            return self.tree[node]
        mid = (left + right) // 2
        return (self.query(ql, qr, node * 2, left, mid) +
                self.query(ql, qr, node * 2 + 1, mid + 1, right))

    def update(self, index, value, node=1, left=0, right=None):
        right = self.n - 1 if right is None else right
        if left == right:
            self.tree[node] = value
            return
        mid = (left + right) // 2
        if index <= mid:
            self.update(index, value, node * 2, left, mid)
        else:
            self.update(index, value, node * 2 + 1, mid + 1, right)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]
```

Örneğin `query(1, 3)` çağrısı, 1 ile 3 arasındaki elemanların toplamını verir; `update(2, 10)` ise üçüncü elemanı değiştirir ve yalnızca köke giden yolu yeniden hesaplar. Ağacı oluşturmak $O(n)$, bellek kullanmak ise yaklaşık $O(4n)$ maliyetindedir.

Daha ileri senaryolarda **lazy propagation** devreye girer. Bir aralıktaki tüm elemanlara değer eklemek gibi aralık güncellemelerinde, değişikliği her yaprağa anında indirmek yerine düğümde ertelersiniz. Bu teknik, aralık güncellemesini de $O(\log n)$ seviyesinde tutar. Segment ağacı başlangıçta biraz fazla mühendislik gibi görünse de dinamik istatistikler, oyun skorları ve zaman serileri için güçlü bir araçtır.
