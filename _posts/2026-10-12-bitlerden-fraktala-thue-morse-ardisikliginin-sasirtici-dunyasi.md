---
layout: post
title: "Bitlerden Fraktala: Thue-Morse Ardışıklığının Şaşırtıcı Dünyası"
math: true
categories: 
  - Bilgi
tags: 
  - thue-morse
  - algoritma
  - matematik
  - fraktal
  - python
  - bit işlemleri
toc: true
image: /img/bitlerden-fraktala-thue-22.png
---

Bir bilgisayara yalnızca “elindeki bitleri kopyala ve terslerini yanına ekle” deseydik, ortaya ne kadar karmaşık bir yapı çıkabilirdi? Thue-Morse ardışıklığı, son derece basit bu talimattan doğmasına rağmen öz-benzerlik, düzen ve kaos arasında gidip gelen büyüleyici bir dizidir. Üstelik matematikten müziğe, kombinatorikten algoritma tasarımına kadar pek çok alanda karşımıza çıkar.

![bitlerden-fraktala-thue-22](/img/bitlerden-fraktala-thue-22.svg)

``
Diziyi oluşturmaya tek bir `0` ile başlayalım. Her adımda mevcut bölümün bitlerini ters çevirip sonuna ekleyelim:

```text
0
01
0110
01101001
0110100110010110
```

Burada ters çevirme işlemi `0 → 1` ve `1 → 0` biçimindedir. Örneğin `0110` kelimesinin tümleyeni `1001` olur; ikisini birleştirince `01101001` elde edilir. Bu üretim kuralı matematiksel olarak

$$T_{k+1} = T_k\,\overline{T_k}$$

şeklinde yazılabilir. $\overline{T_k}$, $T_k$ içindeki bütün bitlerin tümleyenini temsil eder. Her turda uzunluk iki katına çıktığı için $k$ adımından sonra $2^k$ eleman bulunur.

## Sayıların ikili gösterimiyle bağlantısı

Thue-Morse dizisinin yalnızca önceki parçayı kopyalayarak tanımlanması gerekmez. Sıfırdan başlayan $n$ indeksli terim, $n$ sayısının ikili gösterimindeki `1` sayısının tek veya çift olmasına göre hesaplanabilir.

$n$ içindeki `1` bitlerinin sayısına $s_2(n)$ dersek:

$$t_n = s_2(n) \bmod 2$$

Yani `1` sayısı çiftse sonuç `0`, tekse `1` olur.

| $n$ | İkili gösterim | `1` sayısı | $t_n$ |
|---:|:---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 10 | 1 | 1 |
| 3 | 11 | 2 | 0 |
| 4 | 100 | 1 | 1 |
| 5 | 101 | 2 | 0 |
| 6 | 110 | 2 | 0 |
| 7 | 111 | 3 | 1 |

Bu tanımdan kullanışlı iki bağıntı çıkar:

$$t_{2n}=t_n, \qquad t_{2n+1}=1-t_n$$

Çift indeksler önceki değerleri tekrar ederken tek indeksler onların tersini taşır. Dizinin fraktal karakterinin cebirsel özeti tam olarak budur.

## Neden fraktala benziyor?

Fraktallarda bütünün daha küçük ölçekli kopyalarını görürüz. Thue-Morse dizisinde de her blok, daha önce oluşmuş bir bloğu ve onun renkleri değiştirilmiş hâlini içerir. Bitleri siyah ve beyaz kareler olarak çizersek farklı ölçeklerde yinelenen desenler ortaya çıkar. Ancak bu tekrar tam anlamıyla periyodik değildir.

| Özellik | Periyodik dizi | Thue-Morse dizisi |
|---|---|---|
| Üretim | Sabit blok tekrarı | Blok ve tümleyenini birleştirme |
| Tahmin edilebilirlik | Kısa dönem yeterlidir | İndeksin bit yapısı gerekir |
| Öz-benzerlik | Genellikle sınırlı | Her iki kat ölçekte görünür |
| Periyot | Sonlu olabilir | Sonsuz dizide yoktur |

Dizi deterministiktir; yani rastgele değildir. Buna karşın sonsuza kadar tekrar eden sabit bir periyoda da sahip değildir. Dahası, belirli türde aşırı tekrarları engelleyen **overlap-free** özelliğiyle kelime kombinatoriğinde önemli bir yere sahiptir.

## Python ile üretelim

Aşağıdaki fonksiyon, her turun sonuna mevcut bitlerin tümleyenini ekler:

```python
def thue_morse(iterations: int) -> str:
    sequence = "0"

    for _ in range(iterations):
        complement = "".join(
            "1" if bit == "0" else "0"
            for bit in sequence
        )
        sequence += complement

    return sequence

print(thue_morse(4))
# 0110100110010110
```

Tek bir terime ihtiyaç duyulduğunda bütün diziyi üretmek gereksizdir. Python’daki `bit_count()` yöntemi daha doğrudan bir çözüm sunar:

```python
def thue_morse_term(n: int) -> int:
    # İkili gösterimdeki 1 sayısının paritesini döndürür.
    return n.bit_count() % 2

print([thue_morse_term(n) for n in range(16)])
```

İlk yöntem görsel deseni ve öz-benzerliği incelemek için, ikinci yöntemse büyük indekslerde hızlı sorgulama yapmak için uygundur.

Thue-Morse ardışıklığı, karmaşıklığın mutlaka karmaşık kurallardan doğmadığını gösteren zarif bir örnektir. Bir bit, bir tümleyen işlemi ve tekrar: Dijital dünyanın bu küçük tarifi, sonsuz ve periyotsuz bir matematik manzarası üretmeye yeter.
