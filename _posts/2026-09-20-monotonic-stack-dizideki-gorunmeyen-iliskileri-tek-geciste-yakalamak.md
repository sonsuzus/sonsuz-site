---
layout: post
title: "Monotonic Stack: Dizideki Görünmeyen İlişkileri Tek Geçişte Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - monotonic-stack
  - algoritma
  - veri-yapıları
  - javascript
  - zaman-karmaşıklığı
toc: true
---

Bir dizide her elemanın sağındaki ilk büyük değeri bulmanız istendiğinde, akla hemen iç içe döngüler gelebilir. Ancak bu yaklaşım büyüyen girdilerde bilgisayarınızı küçük bir jet motoruna dönüştürür. Monotonic Stack, henüz cevabı bulunmamış elemanları düzenli biçimde saklayarak görünmeyen komşuluk ilişkilerini tek geçişte ortaya çıkarır.

``

## Monotonic Stack nedir?

Monotonic Stack, elemanları belirli bir sıralama kuralına göre tutan yığındır. Yığın artan veya azalan olabilir:

| Tür | Yığındaki düzen | Sık kullanılan amaç |
|---|---|---|
| Artan yığın | Alttan üste değerler artar | Önceki ya da sonraki küçük eleman |
| Azalan yığın | Alttan üste değerler azalır | Önceki ya da sonraki büyük eleman |

Buradaki “monotonic” sözcüğü, yığının her an sıralı kalmasını ifade eder. Yeni bir değer bu düzeni bozuyorsa tepeden elemanlar çıkarılır. İşin sihri de tam burada gerçekleşir: Çıkarılan elemanların aradığı ilişki, çoğu zaman yeni gelen eleman tarafından tamamlanır.

Örneğin `[2, 1, 5, 3, 4]` dizisinde her elemanın sağındaki ilk büyük değeri arayalım. `2` ve `1`, `5` gelene kadar cevaplarını bulamaz. `5` geldiğinde ikisi de yığından çıkar; çünkü sağlarında karşılaştıkları ilk büyük değer artık bellidir.

## Neden tek geçiş yeterli?

İç içe döngülü yöntemde her eleman, sağındaki birçok elemanla yeniden karşılaştırılır. Bu nedenle en kötü durumda zaman karmaşıklığı:

$$T(n) = O(n^2)$$

Monotonic Stack yaklaşımında ise her indis yığına en fazla bir kez eklenir ve yığından en fazla bir kez çıkarılır. Toplam yığın işlemi yaklaşık olarak $2n$ ile sınırlıdır:

$$T(n) = O(n), \qquad S(n) = O(n)$$

Bir eleman için `while` döngüsü uzun sürebilir; fakat bu durum algoritmanın tamamını karesel yapmaz. Çünkü çıkarılan bir eleman tekrar yığına dönmez. Bu analiz tekniğine amortize analiz denir.

| Yaklaşım | Zaman | Ek alan | Büyük dizilerde durum |
|---|---:|---:|---|
| İç içe döngü | $O(n^2)$ | $O(1)$ | Yavaş |
| Monotonic Stack | $O(n)$ | $O(n)$ | Verimli |

## JavaScript ile sonraki büyük eleman

Aşağıdaki fonksiyon, her konum için sağdaki ilk büyük değeri bulur. Böyle bir değer yoksa sonuçta `-1` bırakır. Yığında değerleri değil indisleri saklamak önemlidir; böylece sonuç dizisinde hangi konumun güncelleneceğini biliriz.

```javascript
function nextGreater(nums) {
  const result = new Array(nums.length).fill(-1);
  const stack = []; // Cevabı henüz bulunmamış indisler

  for (let i = 0; i < nums.length; i++) {
    while (
      stack.length > 0 &&
      nums[i] > nums[stack[stack.length - 1]]
    ) {
      const index = stack.pop();
      result[index] = nums[i];
    }

    stack.push(i);
  }

  return result;
}

console.log(nextGreater([2, 1, 5, 3, 4]));
// [5, 5, -1, 4, -1]
```

`5` işlenirken yığının tepesindeki `1` ve ardından `2` çıkarılır. Buna karşılık `3`, `4` geldiğinde çıkarılır. Yığında kalan `5` ve `4` için sağda daha büyük değer bulunmadığından sonuçları `-1` kalır.

## Kuralı probleme göre çevirmek

Monotonic Stack ezberlenecek tek bir kod şablonu değildir. Üç soruyu cevaplayarak doğru çeşidi kurabilirsiniz:

1. Aranan eleman büyük mü, küçük mü?
2. İlişki sağ tarafta mı, sol tarafta mı?
3. Eşit değerler ilişkiyi bozuyor mu?

Örneğin “sonraki büyük” probleminde küçük elemanları yığından çıkarırsınız. “Sonraki küçük” probleminde karşılaştırma yönünü ters çevirirsiniz. Önceki eleman aranıyorsa, yeni değer için cevap çoğunlukla yığının tepesinde hazırdır.

Bu yapı; günlük sıcaklıklar, histogramdaki en büyük dikdörtgen, borsa fiyat aralıkları ve yağmur suyu biriktirme gibi problemlerde karşınıza çıkar. Bir soruda “ilk büyük”, “ilk küçük”, “en yakın” veya “sınır” ifadelerini görüyorsanız zihinsel alarmınızı çalıştırın: Dizinin içinde görünmeyen bir Monotonic Stack ilişkisi saklanıyor olabilir.
