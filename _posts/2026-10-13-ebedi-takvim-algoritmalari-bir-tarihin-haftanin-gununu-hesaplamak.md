---
layout: post
title: "Ebedi Takvim Algoritmaları: Bir Tarihin Haftanın Gününü Hesaplamak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - matematik
  - takvim
  - python
  - zeller
  - tarih-hesaplama
toc: true
image: /img/ebedi-takvim-algoritmalari-99.png
---

Takvim uygulamasına bakmadan 29 Ekim 1923’ün hangi güne denk geldiğini bulabilir misiniz? Ebedi takvim algoritmaları, geçmişteki veya gelecekteki bir tarihin haftanın gününü yalnızca aritmetik işlemlerle hesaplar. İşin içinde artık yıllar, ayların farklı uzunlukları ve modüler aritmetik olsa da temel fikir şaşırtıcı derecede düzenlidir.

![ebedi-takvim-algoritmalari-99](/img/ebedi-takvim-algoritmalari-99.svg)

``

## Takvim neden matematikle hesaplanabilir?

Hafta, yedi günde bir kendini tekrar eden döngüdür. Bu nedenle hesaplamaların kalbinde **modüler aritmetik** bulunur. Bir günün sayısal değerini $d$ kabul edersek sonraki gün şu şekilde yazılabilir:

$$
yeni\_gun = (d + 1) \bmod 7
$$

Örneğin pazartesiye 0 değerini verirsek 10 gün sonrası $(0+10) \bmod 7=3$, yani perşembe olur. Takvim algoritmaları da belirli bir başlangıçtan itibaren geçen günleri hesaplayıp sonucu 7’ye böler.

Ancak yıl uzunluğu tam olarak 365 gün değildir. Gregoryen takviminde artık yıl kuralları şöyledir:

- 4’e bölünen yıllar artık yıldır.
- 100’e bölünen yıllar artık yıl değildir.
- 400’e bölünen yıllar yeniden artık yıldır.

Buna göre 2000 artık yılken 1900 değildir. Bu düzeltme, takvimin mevsimlerden uzaklaşmasını önler.

| Yıl | 4’e bölünür | 100’e bölünür | 400’e bölünür | Sonuç |
|---:|:---:|:---:|:---:|---|
| 2024 | Evet | Hayır | Hayır | Artık yıl |
| 1900 | Evet | Evet | Hayır | Normal yıl |
| 2000 | Evet | Evet | Evet | Artık yıl |
| 2023 | Hayır | Hayır | Hayır | Normal yıl |

## Zeller bağıntısı

En tanınmış ebedi takvim yöntemlerinden biri **Zeller bağıntısıdır**. Gregoryen takvimi için formül şöyledir:

$$
h=\left(q+\left\lfloor\frac{13(m+1)}{5}\right\rfloor+K+\left\lfloor\frac{K}{4}\right\rfloor+\left\lfloor\frac{J}{4}\right\rfloor+5J\right)\bmod 7
$$

Buradaki değişkenler:

| Sembol | Anlamı |
|---|---|
| $q$ | Ayın günü |
| $m$ | Ay numarası; mart 3, ..., aralık 12, ocak 13, şubat 14 |
| $K$ | Yılın yüzyıl içindeki kısmı: $y \bmod 100$ |
| $J$ | Sıfır tabanlı yüzyıl: $\lfloor y/100 \rfloor$ |
| $h$ | Haftanın günü; 0 cumartesi, 1 pazar, ..., 6 cuma |

Buradaki küçük numara hilesi önemlidir: Ocak ve şubat, önceki yılın 13. ve 14. ayı sayılır. Böylece artık gün düzeltmesi formüle daha doğal biçimde katılır. Örneğin Şubat 2024 hesaplanırken yıl 2023 kabul edilir.

## Python ile uygulama

Aşağıdaki fonksiyon formülü doğrudan uygular ve sayısal sonucu okunabilir bir gün adına dönüştürür:

```python
def haftanin_gunu(gun, ay, yil):
    # Zeller'de ocak ve şubat önceki yılın aylarıdır.
    if ay < 3:
        ay += 12
        yil -= 1

    K = yil % 100
    J = yil // 100

    h = (
        gun
        + (13 * (ay + 1)) // 5
        + K
        + K // 4
        + J // 4
        + 5 * J
    ) % 7

    gunler = [
        "Cumartesi", "Pazar", "Pazartesi", "Salı",
        "Çarşamba", "Perşembe", "Cuma"
    ]
    return gunler[h]

print(haftanin_gunu(29, 10, 1923))  # Pazartesi
print(haftanin_gunu(1, 1, 2000))    # Cumartesi
```

Tam sayı bölmesi için `//` kullanılması kritiktir; formüldeki taban fonksiyonu $\lfloor x \rfloor$, ondalık kısmın atılmasını ister. `% 7` işlemi ise büyük toplamı haftanın yedi olası gününden birine indirger.

## Hangi yaklaşım ne zaman kullanılmalı?

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Zeller bağıntısı | Hızlı, sabit zamanlı ve öğretici | Ay numaralandırması alışılmadık |
| Günleri tek tek saymak | Mantığı kolay anlaşılır | Uzak tarihlerde verimsiz |
| Dilin tarih kütüphanesi | Güvenilir ve pratiktir | Matematiksel süreci gizler |

Algoritmanın çalışma süresi $O(1)$’dir; tarih ne kadar uzak olursa olsun yalnızca birkaç aritmetik işlem yapılır. Yine de tarihsel tarihlerde dikkat gerekir: Bu formül **ileriye ve geriye uzatılmış Gregoryen takvimi** varsayar. Gregoryen takvimine geçilmeden önce kullanılan Jülyen takvimi veya ülkelerin farklı geçiş tarihleri hesaba katılacaksa ayrıca dönüşüm kuralları uygulanmalıdır. Kısacası ebedi takvim, matematiğin zamanı küçük bir mod 7 döngüsüne nasıl sığdırabildiğinin zarif bir örneğidir.
