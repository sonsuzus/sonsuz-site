---
layout: post
title: "Quick Sort ve Pivot Seçimi: En Kötü Durumun Anahtarı"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - quick sort
  - pivot
  - python
image: /img/quick-sort-ve-81.png
---

![quick-sort-ve-81](/img/quick-sort-ve-81.svg)


Quick Sort, pratikte son derece hızlı çalışan ancak kaderi büyük ölçüde pivot seçimine bağlı olan klasik bir sıralama algoritmasıdır. Temel fikir basittir: Diziden bir **pivot** seçilir, küçük elemanlar sol tarafa, büyük elemanlar sağ tarafa bölünür ve aynı işlem alt dizilerde tekrarlanır. Fakat kötü seçilmiş bir pivot, zarif görünen bu yaklaşımı beklenmedik biçimde yavaşlatabilir.
``

Quick Sort'un maliyeti, her bölmedeki dizinin ne kadar dengeli parçalandığıyla belirlenir. Bölme işlemi her çağrıda yaklaşık $n$ karşılaştırma gerektirir. Pivot diziyi iki eşit parçaya ayırabiliyorsa çalışma süresi şu bağıntıyla ifade edilir:

$$T(n) = 2T(n/2) + O(n)$$

Bu denklem, Master Teoremi ile $O(n \log n)$ sonucunu verir. Ancak pivot sürekli olarak en küçük ya da en büyük eleman seçilirse bir tarafta boş, diğer tarafta $n-1$ eleman kalır:

$$T(n) = T(n-1) + O(n) = O(n^2)$$

Yani Quick Sort'un en kötü durumu teorik bir dipnot değil; giriş verisinin yapısı ve pivot politikasıyla doğrudan ilişkili bir risktir.

| Pivot stratejisi | Tipik seçim | Sıralı dizide risk | En kötü durum |
|---|---|---:|---:|
| İlk eleman | `dizi[low]` | Çok yüksek | $O(n^2)$ |
| Son eleman | `dizi[high]` | Çok yüksek | $O(n^2)$ |
| Rastgele eleman | Rastgele indeks | Düşük olasılık | $O(n^2)$ |
| Ortanca-üçlü | İlk, orta, sonun ortancası | Düşük | $O(n^2)$ |
| Medyanın medyanı | Yaklaşık gerçek medyan | Çok düşük | $O(n \log n)$ |

İlk veya son elemanı pivot almak kodu sadeleştirir; fakat sıralı ya da ters sıralı veri bu stratejinin kriptonitidir. Örneğin artan `[1, 2, 3, 4, 5]` dizisinde ilk eleman seçildiğinde sol parça her zaman boş kalır. Çağrı ağacı dengeli bir çam yerine tek yöne uzayan bir bambuya dönüşür. Ayrıca çok sayıda eşit değer içeren dizilerde iki yönlü klasik bölümleme de verimsizleşebilir.

Rastgele pivot, düşmanca veya düzenli girdilerin etkisini azaltan popüler bir çözümdür. En kötü durum hâlâ matematiksel olarak mümkündür; ancak her seferinde kötü pivot seçme olasılığı küçüktür. Bu nedenle beklenen çalışma süresi $O(n \log n)$ olarak değerlendirilir. Ortanca-üçlü yöntemi ise ilk, orta ve son eleman arasındaki ortanca değeri seçer; rastgelelik üretmeden birçok gerçek hayat verisinde daha dengeli bölmeler sağlar.

Aşağıdaki Python örneği, ortanca-üçlü seçimi ve eşit elemanları ayrı tutan üç yönlü bölümlemeyi birleştirir:

```python
def median_of_three(a, b, c):
    return sorted((a, b, c))[1]

def quick_sort(values):
    if len(values) <= 1:
        return values

    pivot = median_of_three(values[0], values[len(values)//2], values[-1])
    less = [x for x in values if x < pivot]
    equal = [x for x in values if x == pivot]
    greater = [x for x in values if x > pivot]

    return quick_sort(less) + equal + quick_sort(greater)
```

Burada `equal` listesi kritik bir iyileştirmedir: Pivotla aynı değerler tekrar tekrar özyinelemeye gönderilmez. Örneğin tüm elemanları `7` olan büyük bir dizide algoritma tek bölmeden sonra tamamlanır. Üretim ortamında bu yaklaşım ek bellek kullanır; yerinde (in-place) partition ise daha az bellekle çalışır fakat uygulanması daha karmaşıktır.

| Öncelik | Uygun yaklaşım | Neden |
|---|---|---|
| Basit eğitim örneği | İlk/son pivot | Mantığı görünür kılar |
| Genel amaçlı kullanım | Rastgele pivot | Beklenen dengeli performans |
| Kısmen sıralı veri | Ortanca-üçlü | Kötü bölmeleri azaltır |
| Garantili sınır | Medyanın medyanı | En kötü durumda bile denge sağlar |

Sonuç olarak pivot seçimi, Quick Sort'un küçük bir ayrıntısı değil performans karakterini belirleyen tasarım kararıdır. Pratikte rastgele veya ortanca-üçlü pivot çoğu zaman doğru dengedir; mutlak en kötü durum garantisi gerektiğinde ise daha maliyetli seçme algoritmaları ya da Heap Sort tabanlı hibritler düşünülmelidir.
