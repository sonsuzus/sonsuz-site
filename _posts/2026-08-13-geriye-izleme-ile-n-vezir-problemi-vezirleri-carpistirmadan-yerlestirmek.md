---
layout: post
title: "Geriye İzleme ile N Vezir Problemi: Vezirleri Çarpıştırmadan Yerleştirmek"
math: true
categories: 
  - Proje
tags: 
  - python
  - algoritmalar
  - geriye izleme
  - n vezir problemi
toc: true
---

N Vezir Problemi, $N \times N$ boyutundaki bir satranç tahtasına $N$ adet veziri, hiçbir vezir diğerini tehdit etmeyecek biçimde yerleştirmeyi ister. Vezir yatay, dikey ve çapraz hareket edebildiği için mesele yalnızca boş bir kare bulmak değildir: Her yeni yerleşim, önceki tüm kararlarla uyumlu olmalıdır. Bu yüzden problem, kombinasyonel patlamayı yönetmeyi öğreten klasik bir geriye izleme laboratuvarıdır.
``

## Teorik temel: Neden geriye izleme?

Tahtadaki her kare için “vezir var” veya “vezir yok” kararı verdiğimizi düşünelim. Bu kaba yaklaşım yaklaşık $2^{N^2}$ olasılığı çağrıştırır; küçük tahtalarda bile oldukça pahalıdır. Daha akıllı bir gözlem yapalım: Her satıra tam bir vezir koyarsak, satır çakışmasını otomatik olarak engelleriz. Böylece her satırda yalnızca bir sütun seçeriz ve aday uzay en fazla $N^N$ seviyesine iner.

Geriye izleme, karar ağacını satır satır dolaşır. Bir satır için güvenli sütunları dener, seçim geçerliyse sonraki satıra geçer. Eğer bir noktada güvenli seçenek kalmazsa, son kararı geri alır ve başka bir sütun dener. Bu işlem “deneme-geri alma” gibi görünse de asıl gücü, imkânsız dalları erken budamasıdır.

Bir vezir $(r, c)$ konumundaysa, yeni aday $(i, j)$ için üç koşul kontrol edilir:

$$c \ne j$$
$$r-c \ne i-j$$
$$r+c \ne i+j$$

İlk ifade sütun çakışmasını, diğer ikisi iki farklı çaprazı temsil eder. Çaprazların neden toplama ve çıkarma ile tanımlandığı ilk anda sihir gibi gelebilir; ancak aynı `satır - sütun` değerine sahip kareler `\\` yönündeki, aynı `satır + sütun` değerine sahip kareler ise `/` yönündeki çaprazdadır.

| Yaklaşım | Aday üretimi | Çakışma kontrolü | Pratik sonuç |
|---|---:|---|---|
| Kaba kuvvet | $2^{N^2}$ | Sonradan | Gereksiz derecede büyük arama |
| Satır satır deneme | $N^N$ | Önceki vezirleri tarama | Öğretici, fakat yavaş |
| Kümeli geriye izleme | Budanmış arama ağacı | Ortalama $O(1)$ | Temiz ve hızlı çözüm |

## Python ile çözüm

Aşağıdaki uygulama sütunlar ve iki çapraz türü için `set` kullanır. Böylece her aday konumun güvenliği, tüm tahtayı gezmeden kontrol edilir. `positions` dizisinde indeks satırı, değer ise o satırdaki vezirin sütununu belirtir.

```python
def n_vezir_coz(n):
    cozumler = []
    sutunlar = set()
    capraz_eksi = set()  # satır - sütun
    capraz_arti = set()  # satır + sütun
    positions = [-1] * n

    def geri_izle(satir):
        if satir == n:
            cozumler.append(positions.copy())
            return

        for sutun in range(n):
            if (sutun in sutunlar or
                satir - sutun in capraz_eksi or
                satir + sutun in capraz_arti):
                continue

            positions[satir] = sutun
            sutunlar.add(sutun)
            capraz_eksi.add(satir - sutun)
            capraz_arti.add(satir + sutun)

            geri_izle(satir + 1)

            sutunlar.remove(sutun)
            capraz_eksi.remove(satir - sutun)
            capraz_arti.remove(satir + sutun)
            positions[satir] = -1

    geri_izle(0)
    return cozumler

print(n_vezir_coz(4))
```

`n_vezir_coz(4)` çağrısı iki çözüm döndürür. Örneğin `[1, 3, 0, 2]`, ilk satırda ikinci sütuna, ikinci satırda dördüncü sütuna vezir konulduğunu anlatır. İndeksler sıfırdan başladığı için bu gösterim Python dünyasında doğaldır.

| İşlem | Amaç | Geri alma adımı |
|---|---|---|
| Sütun seçmek | Yeni vezirin konumunu belirlemek | Başka sütunu denemek |
| Kümeye eklemek | Tehdit alanını işaretlemek | Kümeden silmek |
| Özyinelemeli çağrı | Sonraki satıra geçmek | Önceki satıra dönmek |

En kötü durumda süre karmaşıklığı kabaca $O(N!)$ olarak ifade edilir; her seviyede kullanılabilir sütunlar azalır. Buna karşılık bellek maliyeti, özyineleme derinliği ve kümeler nedeniyle yaklaşık $O(N)$'dir. N Vezir Problemi’nin güzel tarafı şudur: Çözüm yalnızca satrançla ilgili değildir. Çizelgeleme, Sudoku, rota arama ve kısıt tatmin problemlerinde aynı “seç, doğrula, ilerle, geri dön” ritmini tekrar tekrar görürsünüz.
