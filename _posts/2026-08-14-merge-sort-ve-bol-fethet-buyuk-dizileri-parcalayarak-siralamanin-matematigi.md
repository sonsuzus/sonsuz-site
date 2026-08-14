---
layout: post
title: "Merge Sort ve Böl-Fethet: Büyük Dizileri Parçalayarak Sıralamanın Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - merge sort
  - böl-fethet
  - karmaşıklık analizi
---

Merge Sort, karmaşık görünen bir sıralama işini şaşırtıcı derecede düzenli bir plana dönüştürür: Büyük diziyi sürekli ikiye böl, tek elemanlı parçalara ulaştığında bu parçaları sıralı biçimde geri birleştir. Bu yaklaşım, **böl-fethet** (divide and conquer) stratejisinin en tanınan örneklerinden biridir. Özellikle milyonlarca kayıt, log satırı veya zaman damgalı olay işlenirken öngörülebilir çalışma süresi sayesinde güven verir.
``

Böl-fethet stratejisi üç aşamadan oluşur: Problemi daha küçük alt problemlere **bölmek**, her alt problemi **çözmek** ve sonuçları **birleştirmek**. Merge Sort'ta bölme işlemi dizinin ortasını bulmaktır. Alt dizinin boyutu bir olduğunda sıralama zaten tamamdır; çünkü tek elemanlı bir dizi tanım gereği sıralıdır. Asıl sihir, iki sıralı diziyi doğrusal zamanda bir araya getiren `merge` adımında gerçekleşir.

Örneğin `[8, 3, 5, 1]` dizisi önce `[8, 3]` ve `[5, 1]` olarak ayrılır. Ardından `[8]`, `[3]`, `[5]`, `[1]` parçalarına inilir. Geri dönüşte `[3, 8]` ile `[1, 5]` elde edilir; son birleştirme ise `[1, 3, 5, 8]` sonucunu üretir. Her birleştirmede iki dizinin başındaki küçük eleman seçildiği için sıralı yapı hiç bozulmaz.

Karmaşıklık analizi için $n$ elemanlı bir diziyi düşünelim. Algoritma her çağrıda problemi iki eşit parçaya ayırır; yani iki adet $n/2$ boyutlu alt problem doğar. Birleştirme aşamasında ise tüm elemanlar en fazla bir kez gezilir ve maliyet $O(n)$ olur. Bu ilişkiyi şu yineleme ile yazarız:

$$T(n) = 2T(n/2) + O(n)$$

Özyineleme ağacının yüksekliği yaklaşık $\log_2 n$ seviyedir. Her seviyede yapılan toplam birleştirme işi $O(n)$ olduğundan toplam maliyet şöyledir:

$$T(n) = O(n \log n)$$

Dikkat çekici nokta, bu maliyetin dizinin başlangıç düzeninden etkilenmemesidir. Dizi zaten sıralı olsa da tamamen ters sıralı olsa da Merge Sort aynı asimptotik süreyi korur.

| Algoritma | En iyi durum | Ortalama durum | En kötü durum | Ek bellek |
|---|---:|---:|---:|---:|
| Merge Sort | $O(n\log n)$ | $O(n\log n)$ | $O(n\log n)$ | $O(n)$ |
| Quick Sort | $O(n\log n)$ | $O(n\log n)$ | $O(n^2)$ | $O(\log n)$ |
| Insertion Sort | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ |

Aşağıdaki Python örneği, bölme ve birleştirme görevlerini ayrı fonksiyonlarda tutar. `merge` fonksiyonu iki sıralı listeyi karşılaştırarak yeni ve sıralı bir liste üretir; ana fonksiyon ise özyinelemeli bölme akışını yönetir.

```python
def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result + left[i:] + right[j:]


def merge_sort(numbers):
    if len(numbers) <= 1:
        return numbers

    middle = len(numbers) // 2
    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])
    return merge(left, right)

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
```

Kodda `<=` kullanılması önemlidir: Eşit elemanlarda sol listedeki değer önce seçilir. Böylece Merge Sort **kararlı** (stable) olur; aynı anahtara sahip kayıtların ilk göreli sırası korunur. Örneğin öğrencileri nota göre sıralarken aynı notlu öğrencilerin kayıt sırası kaybolmaz.

Bu güvenilirliğin bir bedeli vardır: Standart uygulama birleştirme için $O(n)$ ek bellek kullanır. Belleğin çok kısıtlı olduğu durumlarda Quick Sort cazip olabilir. Buna karşılık bağlı listelerde, dış bellekteki dev dosyalarda ve kararlılığın kritik olduğu veri boru hatlarında Merge Sort güçlü bir tercihtir. Kısacası algoritma, “parçala, düzenle, birleştir” fikrinin hem teoride hem üretim sistemlerinde ne kadar etkili olabileceğini gösterir.
