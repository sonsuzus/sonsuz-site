---
layout: post
title: "Amortized Analysis: Tek Bir İşlem Pahalıyken Dizi Nasıl Hâlâ Hızlı Kalır?"
math: true
categories: 
  - Bilgi
tags: 
  - amortized analysis
  - algoritmalar
  - veri yapıları
  - zaman karmaşıklığı
  - dinamik dizi
  - big-o
toc: true
image: /img/amortized-analysis-tek-72.png
---

Bir algoritmanın bazı işlemleri aniden pahalılaşabilir. Dinamik bir dizi büyürken bütün elemanların kopyalanması veya bir sayaç artırılırken art arda birçok bitin değişmesi buna örnektir. Ancak tek bir kötü ana bakıp algoritmayı yavaş ilan etmek, ayda bir gelen yüklü market fişine bakarak her gün aynı harcamayı yaptığımızı sanmaya benzer. **Amortized analysis**, işlemleri tek tek değil, uzun bir işlem dizisi boyunca değerlendirir.
``
## En kötü durumdan farkı nedir?

Klasik worst-case analiz, her işlemin karşılaşabileceği en yüksek maliyeti sorar. Amortized analiz ise belirli bir işlem dizisinin toplam maliyetini hesaplayıp bunu işlem sayısına böler. Burada olasılık kullanılmaz; kötü işlemlerin gerçekten gerçekleşebileceği kabul edilir, fakat ne sıklıkta gerçekleşebilecekleri hesaba katılır.

$n$ işlemin gerçek toplam maliyeti $T(n)$ ise işlem başına amortized maliyet:

$$
\frac{T(n)}{n}
$$

şeklindedir. Örneğin toplam maliyet $T(n)=O(n)$ ise bazı işlemler $O(n)$ sürse bile işlem başına amortized maliyet $O(1)$ olabilir.

| Analiz türü | Temel soru | Olasılık kullanır mı? | Bakış açısı |
|---|---|---:|---|
| En kötü durum | Tek işlem en fazla kaça mal olur? | Hayır | En pahalı işlem |
| Ortalama durum | Beklenen maliyet nedir? | Genellikle evet | Girdi dağılımı |
| Amortized analiz | Bir işlem dizisinin ortalama maliyeti nedir? | Hayır | Toplam maliyet |

## Dinamik dizi örneği

Kapasitesi dolan bir dinamik dizi, kapasitesini iki katına çıkarıp eski elemanları yeni alana kopyalayabilir. Normal ekleme $O(1)$ iken yeniden boyutlandırma sırasında yapılan tek bir ekleme $O(n)$ maliyetlidir.

```python
class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.data = [None] * self.capacity

    def append(self, value):
        if self.size == self.capacity:
            self.capacity *= 2
            new_data = [None] * self.capacity

            for i in range(self.size):
                new_data[i] = self.data[i]

            self.data = new_data

        self.data[self.size] = value
        self.size += 1
```

Kodda `append`, yer varsa değeri doğrudan ekler. Yer yoksa kapasiteyi iki katına çıkarır ve mevcut elemanları kopyalar. Pahalı kopyalamalar kapasite $1,2,4,8,\ldots$ olduğunda gerçekleşir.

$n$ ekleme boyunca yapılan kopyaların toplamı yaklaşık olarak şöyledir:

$$
1+2+4+\cdots+\frac{n}{2}<n
$$

Doğrudan eklemelerin maliyeti de $n$ olduğundan toplam maliyet $O(n)$ olur. Böylece işlem başına maliyet:

$$
\frac{O(n)}{n}=O(1)
$$

çıkar. Buradaki $O(1)$, her eklemenin sabit zamanda tamamlandığını değil, **amortized olarak** sabit maliyetli olduğunu söyler.

## Üç temel analiz yöntemi

Amortized analiz genellikle üç farklı teknikle yapılır:

1. **Aggregate yöntemi:** Bütün işlemlerin gerçek maliyeti toplanır ve işlem sayısına bölünür. Dinamik dizi hesabı bunun tipik örneğidir.
2. **Accounting yöntemi:** Ucuz işlemlere gerçek maliyetlerinden biraz daha yüksek ücret atanır. Aradaki kredi biriktirilerek gelecekteki pahalı işlemler ödenir.
3. **Potential yöntemi:** Veri yapısında saklanan geleceğe yönelik iş, bir potansiyel fonksiyonuyla ölçülür.

Potential yönteminde amortized maliyet şu şekilde tanımlanır:

$$
\hat{c_i}=c_i+\Phi(D_i)-\Phi(D_{i-1})
$$

Burada $c_i$ gerçek maliyet, $\Phi(D_i)$ ise işlem sonrasındaki potansiyeldir. Potansiyel arttığında gelecekte kullanılmak üzere enerji depolanmış gibi düşünülür; azaldığında bu enerji pahalı işlemi karşılar.

## Sık yapılan yanlış yorum

Amortized analiz, average-case analiz değildir. Average-case belirli girdilerin görülme olasılığına dayanabilir. Amortized analizde ise rastgelelik gerekmez ve kötü niyetli bir işlem sırası bile incelenebilir. Garanti şudur: Kurallara uygun herhangi bir $n$ işlemlik dizinin toplam maliyeti belirlenen üst sınırı aşmaz.

Bu yaklaşım dinamik dizilerde, hash table yeniden boyutlandırmalarında, yığınlarda, union-find yapılarında ve garbage collector tasarımlarında sıkça kullanılır. Kısacası tek bir işlemin dramatik performansına değil, bütün sezonun puan tablosuna bakar.

![amortized-analysis-tek-72](/img/amortized-analysis-tek-72.svg)

