---
layout: post
title: "İkili Arama Varyasyonları: Diziden Cevap Uzayına Akıllı Arama"
math: true
categories: 
  - Bilgi
tags: 
  - ikili arama
  - algoritmalar
  - binary search
  - optimizasyon
  - python
---

İkili arama denince çoğu kişinin aklına sıralı bir dizide hedef sayıyı bulmak gelir. Oysa bu algoritmanın asıl süper gücü, yalnızca elemanları değil, **monotonik kararları** aramasıdır. Bir problemde “Bu cevap mümkün mü?” sorusuna verilen yanıt, belirli bir eşikten sonra sürekli evet ya da sürekli hayır oluyorsa, cevap uzayında ikili arama yapabiliriz. Böylece devasa olasılıkları logaritmik sayıda denemeyle küçültürüz.
``

## Temel fikir: Monotonluk nedir?

Klasik ikili aramada sıralı dizi zaten monotoniktir: değerler soldan sağa artar. Cevap uzayı aramasında ise sıralı olan şey değerler değil, karar fonksiyonudur. Örneğin bir paketi en fazla $C$ ağırlıkla taşıyabiliyor muyuz? Kapasite arttıkça iş zorlaşmaz; yani `mümkün(C)` fonksiyonu şu yapıya sahiptir:

$$
false, false, false, \dots, true, true, true
$$

Aradığımız değer, ilk `true` olan kapasitedir. Genel maliyet ise yaklaşık olarak şöyledir:

$$
T = O(\log(R) \cdot F)
$$

Burada $R$, cevap aralığının büyüklüğü; $F$ ise tek bir “mümkün mü?” kontrolünün maliyetidir. Örneğin $F=O(n)$ ise toplam maliyet $O(n\log R)$ olur.

| Varyasyon | Aranan şey | Karar deseni | Tipik kullanım |
|---|---|---|---|
| Klasik arama | Hedef eleman | Karşılaştırma | Dizide sayı bulma |
| Lower bound | İlk uygun indeks | `false → true` | İlk büyük/eşit eleman |
| Upper bound | İlk büyük indeks | `false → true` | Tekrar edenleri sayma |
| Cevap uzayı | En küçük/en büyük geçerli değer | Fizibilite | Kapasite, süre, mesafe |

## Lower bound ve upper bound: Tekrarların efendisi

Bir dizide `x` değerinin yalnızca var olup olmadığını bilmek bazen yetmez. İlk ve son konumlarını bulmak, tekrar sayısını hesaplamak veya ekleme noktasını belirlemek gerekir. `lower_bound`, `x`'ten küçük olmayan ilk indeksi; `upper_bound` ise `x`'ten büyük ilk indeksi verir.

Bu iki sonuçla tekrar sayısı doğrudan hesaplanır:

$$
count(x) = upper\_bound(x) - lower\_bound(x)
$$

Python'da standart kütüphane bu işi oldukça zarif yapar:

```python
from bisect import bisect_left, bisect_right

sayilar = [1, 2, 2, 2, 5, 8]
hedef = 2

sol = bisect_left(sayilar, hedef)   # 1: ilk 2'nin konumu
sag = bisect_right(sayilar, hedef)  # 4: 2'den büyük ilk konum
print(sag - sol)                    # 3
```

Burada `bisect_left`, hedefi düzeni bozmadan ekleyebileceğiniz en sol noktayı döndürür. Bu yaklaşım, sıralı olay kayıtları, puan tabloları ve zaman damgalı verilerde özellikle kullanışlıdır.

## Cevap uzayında arama: Minimum kapasite problemi

Diyelim ki paketleri sırayı bozmadan en fazla `gun` günde göndermek istiyoruz. Bir geminin kapasitesi kaç olmalı? Her olası kapasiteyi denemek pahalıdır; fakat belirli bir kapasiteyle sevkiyat mümkünse daha büyük kapasitelerle de mümkündür. İşte monotonluk yakalandı!

```python
def minimum_kapasite(paketler, gun):
    def mumkun_mu(kapasite):
        kullanilan_gun, yuk = 1, 0
        for paket in paketler:
            if yuk + paket > kapasite:
                kullanilan_gun += 1
                yuk = 0
            yuk += paket
        return kullanilan_gun <= gun

    sol, sag = max(paketler), sum(paketler)
    while sol < sag:
        orta = (sol + sag) // 2
        if mumkun_mu(orta):
            sag = orta       # Daha küçük kapasiteyi zorla
        else:
            sol = orta + 1   # Kapasite yetersiz
    return sol
```

Alt sınır `max(paketler)` olmalıdır; tek bir paketten küçük kapasite anlamsızdır. Üst sınır ise tüm paketlerin toplamıdır: Hepsi tek günde taşınabilir. Kod, her adımda aralığı yarıya indirerek ilk geçerli kapasiteyi bulur.

## Uygulama kontrol listesi

Cevap uzayında ikili arama yazmadan önce şu soruları sorun: Cevap için sayısal bir alt ve üst sınır var mı? `mümkün mü?` fonksiyonu gerçekten monoton mu? İlk geçerli değeri mi, son geçerli değeri mi arıyorum? Son olarak taşma riskine karşı orta noktayı `sol + (sag - sol) // 2` biçiminde hesaplamak, özellikle C++ ve Java gibi dillerde güvenli bir alışkanlıktır. İkili arama, doğru monoton soruyu bulduğunuzda basit bir arama değil, güçlü bir optimizasyon aracıdır.
