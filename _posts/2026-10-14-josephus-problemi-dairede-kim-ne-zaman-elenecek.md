---
layout: post
title: "Josephus Problemi: Dairede Kim, Ne Zaman Elenecek?"
math: true
categories: 
  - Program
tags: 
  - josephus problemi
  - python
  - algoritma
  - veri yapıları
  - matematik
  - simülasyon
toc: true
image: /img/josephus-problemi-dairede-42.png
---

Bir grup insanın daire şeklinde dizildiğini, belirli aralıklarla bir kişinin elendiğini ve bu işlemin yalnızca tek kişi kalana kadar sürdüğünü düşünün. Kulağa biraz acımasız bir sandalye kapmaca oyunu gibi gelen **Josephus Problemi**, döngüsel yapıları, indeks hesaplarını ve algoritmik düşünmeyi öğrenmek için kullanılan klasik bir bilgisayar bilimi problemidir.


![josephus-problemi-dairede-42](/img/josephus-problemi-dairede-42.svg)

``

## Problemin kuralları

Dairede $n$ kişi bulunsun. Saymaya birinci kişiden başlayalım ve her $k$ adımda ulaşılan kişiyi eleyelim. Elenen kişinin hemen yanındaki kişiyle saymaya yeniden devam edelim. Amaç iki farklı sonucu hesaplamak olabilir:

1. Kişilerin elenme sırası,
2. Oyunda hayatta kalan son kişi.

Örneğin $n=7$ ve $k=3$ olsun. Kişiler `1, 2, 3, 4, 5, 6, 7` biçiminde numaralandırılır. İlk elenen kişi 3, sonraki kişi 6 olur. Dairenin sonuna gelindiğinde sayma başa döner.

| Tur | Dairede kalanlar | Elenen kişi |
|---:|---|---:|
| 1 | 1, 2, 4, 5, 6, 7 | 3 |
| 2 | 1, 2, 4, 5, 7 | 6 |
| 3 | 1, 2, 4, 5 | 2 |
| 4 | 1, 4, 5 | 7 |
| 5 | 1, 4 | 5 |
| 6 | 4 | 1 |

Böylece elenme sırası $[3,6,2,7,5,1]$, kazanan ise 4 olur.

## Matematiksel düşünce

Yalnızca kazananı arıyorsak problemi daha küçük problemlere indirebiliriz. Sıfır tabanlı indeks kullanan Josephus bağıntısı şöyledir:

$$
J(1,k)=0
$$

$$
J(n,k)=(J(n-1,k)+k) \bmod n
$$

Buradaki mod işlemi, dairenin sonundan sonra tekrar başa dönmemizi sağlar. İnsanları 1'den başlayarak numaralandırmak istediğimiz için nihai sonuca 1 ekleriz:

$$
\text{kazanan}=J(n,k)+1
$$

Bu yaklaşım $O(n)$ zamanda ve $O(1)$ ek bellekte çalışır. Ancak yalnızca kazananı verir; bütün elenme sırasını öğrenmek için daireyi ayrıca simüle etmeliyiz.

| Yaklaşım | Ürettiği sonuç | Zaman | Ek bellek |
|---|---|---:|---:|
| Matematiksel bağıntı | Son kalan kişi | $O(n)$ | $O(1)$ |
| Kuyruk simülasyonu | Tüm elenme sırası | Uygulamaya bağlı | $O(n)$ |

## Python ile daireyi simüle etmek

Python'daki `deque`, iki uçtan hızlı ekleme ve çıkarma yapabilen bir kuyruktur. `rotate` metodu sayesinde sıradaki kişiyi kuyruğun başına taşıyabiliriz.

```python
from collections import deque


def josephus_sirasi(kisi_sayisi, adim):
    if kisi_sayisi < 1 or adim < 1:
        raise ValueError("Kişi sayısı ve adım pozitif olmalıdır.")

    daire = deque(range(1, kisi_sayisi + 1))
    elenenler = []

    while len(daire) > 1:
        # İlk kişi zaten birinci sayıldığı için k-1 konum ilerliyoruz.
        daire.rotate(-(adim - 1))
        elenenler.append(daire.popleft())

    return elenenler, daire[0]


elenenler, kazanan = josephus_sirasi(7, 3)
print("Elenenler:", elenenler)
print("Kazanan:", kazanan)
```

Programın çıktısı şöyledir:

```text
Elenenler: [3, 6, 2, 7, 5, 1]
Kazanan: 4
```

`rotate(-(adim - 1))` işlemi kuyruğu sola döndürür. Böylece elenecek kişi başa gelir; `popleft()` da onu daireden çıkarır. Negatif döndürme miktarı büyük olsa bile `deque`, döngüsel davranışı korur.

## Yalnızca kazananı bulmak

Büyük girişlerde elenme listesini saklamak istemiyorsak bağıntıyı döngüyle uygulayabiliriz:

```python
def josephus_kazanan(n, k):
    konum = 0
    for mevcut_boyut in range(2, n + 1):
        konum = (konum + k) % mevcut_boyut
    return konum + 1
```

Josephus Problemi küçük bir oyun gibi görünse de modüler aritmetik, kuyruklar, yinelemeli bağıntılar ve performans karşılaştırmaları için güçlü bir örnektir. Adım değerini veya başlangıç kişisini değiştirerek farklı senaryolar üretmek, algoritmanın döngüsel mantığını iyice pekiştirir.
