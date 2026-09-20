---
layout: post
title: "Sweep Line Algoritması: Düzlemdeki Olayları Tek Boyuta İndirerek Çözmek"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - sweep-line
  - geometri
  - python
  - veri-yapıları
toc: true
image: /img/sweep-line-algoritmasi-54.png
---

Bilgisayarsal geometri problemleri ilk bakışta ürkütücüdür: Doğrular kesişir, dikdörtgenler üst üste biner ve noktalar düzleme dağılır. Sweep Line, yani **tarama doğrusu algoritması**, bu iki boyutlu karmaşayı hareket eden hayali bir doğru ve sıralanmış olaylar yardımıyla yönetilebilir hâle getirir. Kısacası bütün düzleme aynı anda bakmak yerine, önemli değişiklikleri sırayla işleriz.
``

## Temel fikir: Düzlemi süpürmek

Genellikle soldan sağa hareket eden dikey bir doğru düşünülür. Bu doğru $x=-\infty$ konumundan başlayıp $x=+\infty$ yönüne ilerler. Algoritmanın durumu yalnızca belirli koordinatlarda değişir. Bu koordinatlara **olay**, olayların sıralandığı yapıya ise **olay kuyruğu** denir.

Bir doğru parçası problemi için tipik olaylar şunlardır:

- Bir parçanın başladığı nokta
- Bir parçanın bittiği nokta
- Başka parçaların sorgulandığı bir koordinat
- Bazı algoritmalarda iki parçanın kesişmesi

Tarama doğrusunun o anda kestiği nesneler ayrıca **aktif küme** içinde tutulur. Böylece her yeni nesneyi düzlemdeki tüm nesnelerle karşılaştırmak yerine yalnızca ilgili komşularla karşılaştırabiliriz.

| Yaklaşım | İncelenen ilişkiler | Tipik karmaşıklık | Temel sorun |
|---|---:|---:|---|
| Kaba kuvvet | Tüm nesne çiftleri | $O(n^2)$ | Gereksiz karşılaştırmalar |
| Sweep Line | Sıralı olaylar ve aktif nesneler | $O((n+k)\log n)$ | Olay sırası dikkat ister |

Burada $n$ nesne sayısını, $k$ ise raporlanan kesişim sayısını gösterir. Başlangıçta olayları sıralamak genellikle $O(n\log n)$ sürer. Aktif kümeye ekleme, silme ve arama dengeli bir ağaçla $O(\log n)$ zamanda gerçekleştirilebilir.

## Örnek: Yatay ve dikey parçaların kesişmesi

Yatay bir parça $(x_1,y)$ ile $(x_2,y)$ arasında olsun. Tarama doğrusu $x_1$ noktasına geldiğinde parçayı aktif kümeye ekler, $x_2$ noktasında çıkarır. Dikey bir parça $x=c$ ve $[y_1,y_2]$ aralığındaysa, olay anında aktif kümede

$$y_1 \leq y \leq y_2$$

koşulunu sağlayan yatay parçalar aranır. Bulunan her parça bir kesişimdir.

Aşağıdaki Python kodu bu mantığın öğretici bir uygulamasıdır:

```python
from bisect import bisect_left, bisect_right, insort

def kesismeleri_bul(yataylar, dikeyler):
    olaylar = []

    for x1, x2, y in yataylar:
        x1, x2 = sorted((x1, x2))
        olaylar.append((x1, 0, y))       # Aktif kümeye ekle
        olaylar.append((x2, 2, y))       # Aktif kümeden çıkar

    for x, y1, y2 in dikeyler:
        y1, y2 = sorted((y1, y2))
        olaylar.append((x, 1, y1, y2))   # Aralık sorgusu

    olaylar.sort()
    aktif_y = []
    sonuclar = []

    for olay in olaylar:
        x, tur = olay[0], olay[1]

        if tur == 0:
            insort(aktif_y, olay[2])
        elif tur == 2:
            i = bisect_left(aktif_y, olay[2])
            aktif_y.pop(i)
        else:
            y1, y2 = olay[2], olay[3]
            sol = bisect_left(aktif_y, y1)
            sag = bisect_right(aktif_y, y2)
            sonuclar.extend((x, y) for y in aktif_y[sol:sag])

    return sonuclar
```

Olay türlerinin `ekle < sorgula < çıkar` sırasıyla numaralandırılması tesadüf değildir. Aynı $x$ koordinatındaki uç noktaların kesişim kabul edilmesini sağlar. Olay sırası yanlış seçilirse geometrik olarak mevcut bir kesişim görünmez olabilir.

Python listesindeki silme işlemi $O(n)$ olduğundan bu kod eğitim amaçlıdır. Üretim düzeyinde dengeli arama ağacı, Fenwick ağacı veya koordinat sıkıştırmalı segment ağacı kullanılabilir.

## Nerelerde kullanılır?

Sweep Line; doğru parçası kesişimleri, dikdörtgenlerin birleşim alanı, takvim çakışmaları, en fazla eşzamanlı kullanıcı sayısı ve en yakın nokta çifti gibi problemlerde karşımıza çıkar. Hepsindeki ortak numara aynıdır: **Uzayı gezmek yerine değişimin gerçekleştiği olayları gezmek.** Böylece iki boyutlu görünen problem, sıralı bir zaman çizelgesi ve güncel bir aktif durum problemine dönüşür.

![sweep-line-algoritmasi-54](/img/sweep-line-algoritmasi-54.svg)

