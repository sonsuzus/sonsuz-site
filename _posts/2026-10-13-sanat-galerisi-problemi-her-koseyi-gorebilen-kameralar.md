---
layout: post
title: "Sanat Galerisi Problemi: Her Köşeyi Görebilen Kameralar"
math: true
categories: 
  - Bilgi
tags: 
  - hesaplamalı geometri
  - sanat galerisi problemi
  - algoritma
  - kamera yerleşimi
  - üçgenleme
  - graf teorisi
toc: true
image: /img/sanat-galerisi-problemi-98.png
---

Bir sanat galerisinde geceleri dolaşan tek şey güvenlik görevlisi değil, geometridir! Duvarlarla çevrili çokgen biçimindeki bir mekânın tamamını kameralarla gözetlemek istediğimizi düşünelim. Kameraları nereye koymalı ve kaç tane kullanmalıyız? İlk bakışta basit görünen bu soru, hesaplamalı geometrinin en ünlü problemlerinden biri olan **Sanat Galerisi Problemi**ni ortaya çıkarır.

``

## Problemin geometrik modeli

Galeri, kendi kenarlarıyla kesişmeyen basit bir çokgen olarak modellenir. Çokgenin $n$ adet köşesi vardır ve kameraların genellikle bu köşelere yerleştirilebildiği kabul edilir. Bir kamera, bulunduğu noktayla galeri içindeki hedef nokta arasındaki doğru parçası tamamen çokgenin içinde kalıyorsa o noktayı görebilir.

Burada iki farklı soru birbirinden ayrılmalıdır:

| Soru | Amaç | Zorluk |
|---|---|---|
| En kötü durumda kaç kamera yeterlidir? | Her $n$ köşeli galeriyi koruyacak üst sınırı bulmak | Klasik teoremle çözülür |
| Belirli bir galeri için gerçek minimum nedir? | O galeriye özel en küçük kamera kümesini bulmak | Hesaplama açısından zordur |

![sanat-galerisi-problemi-98](/img/sanat-galerisi-problemi-98.svg)


Chvátal’ın Sanat Galerisi Teoremi, $n$ köşeli basit bir çokgen için her zaman

$$
\left\lfloor \frac{n}{3} \right\rfloor
$$

kameranın yeterli olduğunu söyler. Üstelik bazı özel galeriler gerçekten bu kadar kameraya ihtiyaç duyar. Örneğin 12 köşeli en kötü durum galerisi için garanti edilen sayı $\lfloor 12/3 \rfloor=4$ olur.

## Üçgenleme neden işe yarıyor?

İspatın merkezinde **üçgenleme** bulunur. Çokgenin içine, kesişmeyen köşegenler eklenerek galeri üçgenlere ayrılır. $n$ köşeli basit bir çokgenin üçgenlenmesi sonucunda:

- $n-2$ üçgen oluşur.
- $n-3$ köşegen kullanılır.
- Hiçbir yeni köşe eklenmez.

Ardından köşeler üç renkle boyanır. Üçgenlemeden doğan yapıda her üçgenin köşeleri üç farklı renge sahip olacak biçimde bir renklendirme yapılabilir. Her renk sınıfındaki köşe sayıları $c_1$, $c_2$ ve $c_3$ olsun:

$$
c_1+c_2+c_3=n
$$

Güvercin yuvası ilkesine göre en küçük renk sınıfı en fazla $\lfloor n/3 \rfloor$ köşe içerir. Kameralar bu sınıftaki köşelere konulduğunda her üçgende seçilen renkten bir köşe bulunur. Böylece bütün üçgenler, dolayısıyla tüm galeri görülür.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Her köşeye kamera | Son derece kolay | Gereksiz derecede pahalı |
| Üç renk teoremi | Güçlü bir garanti verir | Her galeri için gerçek minimumu vermez |
| Galeriye özel optimizasyon | En az kamerayı bulabilir | NP-zor bir probleme dönüşebilir |

## Küçük bir kod örneği

Aşağıdaki Python fonksiyonu, üçgenleme sonrasında köşelerin geçerli biçimde üç renge boyandığını varsayar. En az kullanılan rengi seçerek kameraların yerleştirileceği köşeleri döndürür:

```python
from collections import Counter

def kamera_koseleri(renkler):
    """Köşe indeksi -> renk eşlemesinden kamera noktalarını seçer."""
    sayilar = Counter(renkler.values())
    secilen_renk = min(sayilar, key=sayilar.get)

    return [
        kose for kose, renk in renkler.items()
        if renk == secilen_renk
    ]

renkler = {
    0: "kirmizi", 1: "mavi", 2: "yesil",
    3: "kirmizi", 4: "mavi", 5: "yesil",
    6: "kirmizi", 7: "mavi"
}

print(kamera_koseleri(renkler))
```

Bu kod üçgenleme veya renklendirme işlemini kendisi yapmaz; teorinin son seçim adımını gösterir. Gerçek bir uygulamada önce çokgen doğrulanmalı, ardından kulak kesme gibi bir algoritmayla üçgenlenmeli ve oluşan yapı üç renge boyanmalıdır.

## Teoremden gerçek dünyaya

Klasik model; sütunları, kameraların görüş açısını, menzilini ve hareketli engelleri hesaba katmaz. Gerçek güvenlik sistemlerinde problem; görünürlük çokgenleri, kapsama optimizasyonu ve maliyet gibi ek koşullarla genişletilir. Yine de temel fikir şaşırtıcı derecede güçlüdür: Duvarları üçgenlere ayır, köşeleri renklendir ve en küçük renk grubunu seç. Bazen bir galeriyi korumanın yolu, sanat eserlerinden önce matematiğe bakmaktır!
