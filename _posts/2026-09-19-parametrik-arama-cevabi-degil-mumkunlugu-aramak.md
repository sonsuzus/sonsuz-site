---
layout: post
title: "Parametrik Arama: Cevabı Değil, Mümkünlüğü Aramak"
math: true
categories: 
  - Bilgi
tags: 
  - parametrik arama
  - ikili arama
  - algoritma
  - python
  - karmaşıklık
  - problem çözme
toc: true
---

Bazı algoritma soruları bizden doğrudan “en iyi cevap nedir?” diye sorar; fakat cevabı tek hamlede hesaplamak neredeyse imkânsızdır. Parametrik arama bu soruyu daha kolay bir soruya dönüştürür: “Verilen bir cevap mümkün mü?” Böylece karanlıkta cevabı tahmin etmek yerine, mümkün ve imkânsız bölgeler arasındaki sınırı sistematik biçimde buluruz.

``

## Temel fikir: Optimizasyondan karar problemine

Elimizde en küçük veya en büyük değeri bulmayı amaçlayan bir optimizasyon problemi olduğunu düşünelim. Her aday cevap $x$ için çalışan bir uygunluk fonksiyonu tanımlarız:

$$
P(x) = \begin{cases}
1, & x \text{ mümkünse} \\
0, & x \text{ mümkün değilse}
\end{cases}
$$

Parametrik aramanın çalışması için $P(x)$ fonksiyonunun **monoton** olması gerekir. Örneğin bir işi $10$ günde bitirmek mümkünse, genellikle $11$, $12$ veya daha fazla günde bitirmek de mümkündür. Sonuçlar şu biçimlerden birini oluşturmalıdır:

- `False, False, False, True, True, True`
- `True, True, True, False, False, False`

Aradığımız şey tek tek bütün cevapları denemek değil, iki bölge arasındaki sınırdır.

| Yaklaşım | Aranan şey | Tipik maliyet | Kullanım durumu |
|---|---|---:|---|
| Doğrusal tarama | Her aday cevap | $O(R)$ | Aralık küçükse |
| Klasik ikili arama | Dizide belirli eleman | $O(\log R)$ | Sıralı veri varsa |
| Parametrik arama | İlk/son mümkün cevap | $O(T \log R)$ | Monoton uygunluk varsa |

Burada $R$ cevap aralığının büyüklüğü, $T$ ise bir adayın mümkün olup olmadığını sınama maliyetidir.

## Örnek: Kargolar kaç günde taşınır?

Sırayla taşınması gereken paketlerin ağırlıkları ve günlük kapasitesi sabit bir gemimiz olsun. Tüm paketleri en fazla $D$ günde taşımak için gereken **en küçük kapasiteyi** arıyoruz.

Bir kapasite tahmin ettiğimizde sonucu doğrudan bulmak yerine şunu sorabiliriz: “Bu kapasiteyle taşıma $D$ gün içinde tamamlanabilir mi?” Kapasite arttıkça gereken gün sayısı azalır veya aynı kalır. Dolayısıyla uygunluk monoton davranır.

Alt sınır en ağır paket olmalıdır; çünkü paketler bölünemez. Üst sınır ise bütün paketlerin ağırlıkları toplamıdır; bu kapasiteyle her şey bir günde taşınabilir.

```python
def minimum_capacity(weights, max_days):
    def is_possible(capacity):
        days = 1
        current_load = 0

        for weight in weights:
            if current_load + weight > capacity:
                days += 1
                current_load = 0
            current_load += weight

        return days <= max_days

    left = max(weights)
    right = sum(weights)

    while left < right:
        middle = (left + right) // 2

        if is_possible(middle):
            right = middle
        else:
            left = middle + 1

    return left

print(minimum_capacity([3, 2, 2, 4, 1, 4], 3))  # 6
```

`is_possible`, verilen kapasiteyle kaç güne ihtiyaç duyulduğunu hesaplar. Tahmin mümkünse daha küçük kapasiteleri araştırmak için sağ sınırı daraltırız. Mümkün değilse kapasiteyi artırırız. Döngü bittiğinde `left`, ilk mümkün kapasitedir.

## Sınırları doğru yönetmek

Parametrik aramada en sık hata, orta noktadan çok sınırların anlamını karıştırmaktır.

| Hedef | Mümkün sonuçta yapılacak işlem | Sonuç |
|---|---|---|
| En küçük mümkün değer | `right = middle` | İlk `True` |
| En büyük mümkün değer | `left = middle` veya uygun yuvarlama | Son `True` |

Özellikle en büyük mümkün değeri ararken orta noktanın yukarı yuvarlanması gerekebilir:

$$
mid = \left\lfloor \frac{left + right + 1}{2} \right\rfloor
$$

Aksi hâlde iki elemanlı aralıkta sonsuz döngü oluşabilir. Ayrıca uygunluk fonksiyonunun gerçekten monoton olduğunu kanıtlamak gerekir; “öyle görünüyor” algoritmik kanıt sayılmaz.

## Ne zaman akla gelmeli?

Soruda “minimum hız”, “maksimum mesafe”, “en az kapasite”, “en büyük eşit pay” veya “belirli sürede tamamlanabilir mi?” gibi ifadeler varsa parametrik arama güçlü bir adaydır. Önce cevap aralığını belirleyin, sonra bir aday cevabın mümkünlüğünü test edin ve monotonluğu doğrulayın. Kısacası bazen cevaba ulaşmanın en iyi yolu, cevabı aramayı bırakıp onun mümkün olup olmadığını sormaktır.
