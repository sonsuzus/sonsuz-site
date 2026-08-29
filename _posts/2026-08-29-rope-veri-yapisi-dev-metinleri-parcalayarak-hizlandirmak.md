---
layout: post
title: "Rope Veri Yapısı: Dev Metinleri Parçalayarak Hızlandırmak"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - rope
  - metin düzenleme
---

Bir metin editöründe milyonlarca karakterlik bir günlük dosyasını açtığınızı düşünün. Ortasına tek bir cümle eklemek bile, klasik `string` yaklaşımında metnin geri kalanını kaydırmayı gerektirebilir. Rope (halat) veri yapısı tam bu noktada devreye girer: Metni tek ve dev bir karakter dizisi yerine, küçük parçalardan oluşan dengeli bir ağaç olarak saklar. Böylece ekleme, silme ve birleştirme işlemleri tüm metni taşımak yerine yalnızca ilgili dalları değiştirir.

``

## Neden sıradan dizeler zorlanır?

Klasik bir dizide metnin başına veya ortasına karakter eklemek, ekleme noktasından sonraki karakterlerin yer değiştirmesi anlamına gelir. Metin uzunluğu $n$ ise bu işlem çoğu durumda $O(n)$ maliyetlidir. Birkaç yüz karakter için önemsiz görünen bu maliyet; IDE'ler, belge editörleri, DNA dizisi analizleri veya devasa log görüntüleyicilerinde hissedilir hâle gelir.

Rope, metni yaprak düğümlerde kısa metin parçaları tutan ikili bir ağaç şeklinde temsil eder. İç düğümler ise genellikle sol alt ağacın karakter sayısını, yani **ağırlığını**, saklar. Aradığımız karakterin hangi dalda olduğunu bu ağırlıkla buluruz:

$$
\text{eğer } i < w(\text{sol}) \text{ ise sola git; aksi hâlde sağa git.}
$$

Ağaç dengeliyse yüksekliği yaklaşık $\log_2 n$ olur. Dolayısıyla karaktere erişim, bölme ve birleştirme işlemleri çoğunlukla $O(\log n)$ düzeyindedir.

| İşlem | Klasik String | Dengeli Rope |
|---|---:|---:|
| İndeksten karakter okuma | $O(1)$ | $O(\log n)$ |
| Ortaya ekleme | $O(n)$ | $O(\log n)$ |
| Aralık silme | $O(n)$ | $O(\log n)$ |
| İki metni birleştirme | $O(n+m)$ | $O(1)$ veya $O(\log n)$ |

Buradaki küçük sürpriz şudur: Rope her işte daha hızlı değildir. Rastgele karakter okumayı çok sık yapıyor, fakat nadiren düzenleme yapıyorsanız düz dizi önbellek dostu yapısıyla daha iyi sonuç verebilir.

## Böl, değiştir, yeniden bağla

Rope işlemlerinin kalbi `split` ve `concat` ikilisidir. Ekleme yapmak için metni istenen indiste ikiye böler, yeni parçayı araya koyar ve üç bölümü tekrar bağlarız. Silmede ise başlangıç ve bitiş noktalarından iki kez bölme yapıp ortadaki dalı atarız.

Aşağıdaki sade Python örneği fikri gösterir; gerçek kullanımda AVL veya Red-Black Tree ile dengeleme eklenmelidir:

```python
class Rope:
    def __init__(self, left=None, right=None, text=None):
        self.left, self.right, self.text = left, right, text
        self.weight = len(left.to_string()) if left else 0

    def to_string(self):
        if self.text is not None:
            return self.text
        return self.left.to_string() + self.right.to_string()

def concat(a, b):
    return Rope(left=a, right=b)

sol = Rope(text="Merhaba ")
sag = Rope(text="dünya!")
metin = concat(sol, sag)
print(metin.to_string())  # Merhaba dünya!
```

Bu kodda yapraklar gerçek metni, iç düğüm ise iki parçanın bağlantısını temsil eder. Ancak `to_string()` her çağrıda bütün ağacı dolaşır; bu nedenle üretim ortamında uzunluk, yükseklik ve ağırlık bilgileri düğümlerde önbelleklenir.

## Denge ve parça boyutu kritik

Rope'un performansı ağacın dengesine bağlıdır. Sürekli sona ekleme yapıp ağacı dengelemezseniz yapı zincire dönüşür ve karmaşıklık yeniden $O(n)$ olur. Ayrıca çok küçük parçalar fazla düğüm ve bellek tüketimi, aşırı büyük parçalar ise pahalı kopyalama demektir. Pratikte parçaları birkaç yüz veya birkaç bin karakter civarında tutmak sık kullanılan bir stratejidir.

| Senaryo | Rope tercihi |
|---|---|
| Küçük yapılandırma dosyası | Genellikle gereksiz |
| Büyük belge editörü | Çok uygun |
| Sık kopyala-yapıştır işlemi | Çok uygun |
| Karakter karakter yoğun erişim | Dikkatli ölçüm gerekli |

Özetle Rope, metni "tek parça nesne" olmaktan çıkarıp düzenlenebilir bir ağaç hâline getirir. Büyük metinlerde doğru dengeleme ve makul parça boyutuyla, kullanıcı yazarken görünmez ama etkili bir performans halatı olur.
