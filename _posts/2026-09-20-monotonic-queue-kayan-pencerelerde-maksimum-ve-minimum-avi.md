---
layout: post
title: "Monotonic Queue: Kayan Pencerelerde Maksimum ve Minimum Avı"
math: true
categories: 
  - Bilgi
tags: 
  - monotonic-queue
  - kayan-pencere
  - algoritma
  - deque
  - veri-yapıları
  - python
toc: true
image: /img/monotonic-queue-kayan-74.png
---

Bir dizide belirli genişlikteki pencereyi soldan sağa kaydırıp her konumdaki maksimum veya minimum değeri bulmak, ilk bakışta zararsız görünen bir problemdir. Fakat pencere büyüdükçe her adımda tüm elemanları yeniden taramak, işlemciyi küçük bir maratona çıkarır. **Monotonic Queue**, yalnızca işe yarayabilecek adayları saklayarak bu avı doğrusal zamanda tamamlar.
``
## Önce problemimizi tanıyalım

Elimizde $n$ elemanlı bir dizi ve genişliği $k$ olan bir pencere bulunsun. Pencere toplam $n-k+1$ farklı konuma uğrar. Her konumda $k$ elemanı tararsak zaman karmaşıklığı

$$O((n-k+1)k) \approx O(nk)$$

olur. Özellikle $k$, $n$ değerine yaklaştığında bu yaklaşım $O(n^2)$ seviyesine kadar kötüleşebilir.

Monotonic Queue ise elemanları monoton, yani sürekli azalan veya artan bir düzende tutan özel bir çift uçlu kuyruk (**deque**) yaklaşımıdır. Buradaki önemli fikir şudur: Yeni gelen eleman, kuyruğun sonundaki bazı adayları sonsuza dek işe yaramaz hâle getirebilir.

| Hedef | Kuyruktaki düzen | Ön tarafta bulunan |
|---|---|---|
| Pencere maksimumu | Azalan | En büyük eleman |
| Pencere minimumu | Artan | En küçük eleman |

![monotonic-queue-kayan-74](/img/monotonic-queue-kayan-74.svg)


## Neden değer değil indeks saklıyoruz?

Kuyrukta doğrudan değer saklamak cazip görünür; ancak pencerenin dışına hangi elemanın çıktığını anlamamız gerekir. Bu nedenle indeksleri saklarız. Böylece hem `nums[index]` ile değeri karşılaştırabilir hem de `index <= i - k` koşuluyla eskimiş elemanları silebiliriz.

Maksimum ararken yeni değer, kuyruğun arkasındaki değerden büyük veya ona eşitse arkadaki indeks çıkarılır. Çünkü yeni eleman hem daha güçlüdür hem de pencerede daha uzun süre kalacaktır. Kuyruğun önündeyse o anki pencerenin şampiyonu bulunur.

```python
from collections import deque

def sliding_window_max(nums, k):
    q = deque()       # Değerleri azalan indeks kuyruğu
    result = []

    for i, value in enumerate(nums):
        # Artık pencerenin dışında kalan indeksi temizle
        while q and q[0] <= i - k:
            q.popleft()

        # Yeni değerden küçük veya eşit adaylar elenir
        while q and nums[q[-1]] <= value:
            q.pop()

        q.append(i)

        # İlk tam pencere oluştuğunda maksimumu kaydet
        if i >= k - 1:
            result.append(nums[q[0]])

    return result

print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
# [3, 3, 5, 5, 6, 7]
```

Kodda iki ayrı `while` döngüsü bulunmasına rağmen algoritma $O(n)$ zamanda çalışır. Çünkü her indeks kuyruğa yalnızca bir kez girer ve en fazla bir kez çıkar. Toplam kuyruk işlemi yaklaşık $2n$ ile sınırlıdır. Kuyrukta en fazla $k$ indeks tutulduğu için alan karmaşıklığı da $O(k)$ olur.

## Minimum avına çıkmak

Minimum değerleri bulmak için yapıyı baştan yazmaya gerek yoktur. Sadece ikinci döngüdeki karşılaştırmayı tersine çevirmek yeterlidir:

```python
# Artan kuyruk kurar; öndeki indeks minimumu gösterir.
while q and nums[q[-1]] >= value:
    q.pop()
```

| Yöntem | Zaman | Ek alan | Kullanım kolaylığı |
|---|---:|---:|---|
| Her pencereyi tarama | $O(nk)$ | $O(1)$ | Çok kolay |
| Dengeli ağaç / multiset | $O(n\log k)$ | $O(k)$ | Orta |
| Monotonic Queue | $O(n)$ | $O(k)$ | Biraz dikkat ister |

## Akılda kalacak tarif

Monotonic Queue kullanırken üç hareketi sırayla düşün: **eskileri önden at, güçsüzleri arkadan ele, yeniyi arkaya ekle**. Pencere tamamlandığında cevap daima öndedir. Bu teknik; sensör verilerindeki zirveleri bulma, trafik yoğunluğu analizi, zaman serileri, görüntü işleme ve çevrim içi ölçüm sistemleri gibi pek çok alanda kullanılır.

Kısacası kuyruk bütün pencereyi değil, gelecekte kazanma ihtimali bulunan adayları taşır. Gereksiz yarışmacıları erkenden elediği için de maksimum ve minimum avını $O(n)$ zamanda bitirir.
