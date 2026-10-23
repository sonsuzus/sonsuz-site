---
layout: post
title: "Black-Scholes Modeli: Opsiyon Fiyatlamasının Matematiksel ve Algoritmik Temelleri"
math: true
categories: 
  - Bilgi
tags: 
  - black-scholes
  - opsiyon
  - finansal matematik
  - python
  - algoritma
  - türev ürünler
toc: true
image: /img/black-scholes-modeli-65.png
---

Bir opsiyonun “adil” fiyatı nasıl belirlenir? Black-Scholes modeli, bu soruyu rastgele fiyat hareketlerini matematiksel bir çerçeveye oturtarak yanıtlar. Model kusursuz bir piyasa kristal küresi değildir; ancak risk, zaman ve belirsizlik arasındaki ilişkiyi anlamak için finansal matematiğin en güçlü başlangıç noktalarından biridir.
``

## Opsiyon nedir?

Opsiyon, sahibine belirli bir varlığı gelecekte belirli bir kullanım fiyatından alma veya satma hakkı verir. **Call opsiyonu** alma, **put opsiyonu** ise satma hakkıdır. Buradaki kritik kelime “hak”tır: Opsiyon sahibi işlemi gerçekleştirmek zorunda değildir.

| Özellik | Call opsiyonu | Put opsiyonu |
|---|---|---|
| Sağladığı hak | Varlığı satın alma | Varlığı satma |
| Değer kazandığı durum | Fiyat yükseldiğinde | Fiyat düştüğünde |
| Vade sonu getirisi | $\max(S_T-K,0)$ | $\max(K-S_T,0)$ |
| Temel beklenti | Yükseliş | Düşüş |

![black-scholes-modeli-65](/img/black-scholes-modeli-65.svg)


Burada $S_T$ vade sonundaki varlık fiyatını, $K$ ise kullanım fiyatını gösterir.

## Modelin teorik zemini

Black-Scholes, varlık fiyatının geometrik Brown hareketi izlediğini varsayar:

$$dS_t = \mu S_t\,dt + \sigma S_t\,dW_t$$

Bu denklemde $\mu$ beklenen getiri oranı, $\sigma$ volatilite ve $dW_t$ rastgele şoku temsil eder. Geometrik yapı sayesinde fiyatın negatif olması engellenir. Model ayrıca işlem maliyeti bulunmadığını, risksiz faiz oranının sabit olduğunu, varlığın sürekli alınıp satılabildiğini ve piyasanın arbitraja izin vermediğini kabul eder.

Asıl matematiksel sihir, opsiyon ile temel varlıktan oluşturulan **delta-nötr portföyde** gerçekleşir. Portföy çok kısa bir süre için fiyat hareketlerine karşı dengelenirse rastgelelik ortadan kaldırılabilir. Risksiz hale gelen portföy, arbitraj olmaması nedeniyle risksiz faiz oranıyla büyümelidir. Bu fikir şu kısmi diferansiyel denklemi doğurur:

$$\frac{\partial V}{\partial t}+\frac{1}{2}\sigma^2S^2\frac{\partial^2V}{\partial S^2}+rS\frac{\partial V}{\partial S}-rV=0$$

Avrupa tipi, temettüsüz bir call opsiyonunun kapalı form çözümü şöyledir:

$$C=S_0N(d_1)-Ke^{-rT}N(d_2)$$

$$d_1=\frac{\ln(S_0/K)+(r+\sigma^2/2)T}{\sigma\sqrt{T}}, \qquad d_2=d_1-\sigma\sqrt{T}$$

$N(x)$ standart normal dağılımın kümülatif dağılım fonksiyonudur. $S_0$ bugünkü fiyatı, $T$ vadeye kalan süreyi ve $r$ sürekli bileşik risksiz faiz oranını belirtir.

## Algoritmik uygulama

Formülü Python ile doğrudan hesaplayabiliriz:

```python
from math import log, sqrt, exp, erf

def normal_cdf(x):
    # Standart normal dağılımın kümülatif olasılığını hesaplar.
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def black_scholes_call(S, K, T, r, sigma):
    if T <= 0:
        return max(S - K, 0.0)
    if sigma <= 0:
        return max(S - K * exp(-r * T), 0.0)

    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * normal_cdf(d1) - K * exp(-r * T) * normal_cdf(d2)

fiyat = black_scholes_call(100, 105, 1, 0.04, 0.25)
print(f"Call fiyatı: {fiyat:.2f}")
```

Fonksiyon önce vade ve volatilite gibi sınır durumlarını denetler; ardından $d_1$ ve $d_2$ değerlerini hesaplayarak teorik call fiyatını üretir. Gerçek uygulamalarda temettü, piyasa spread’i ve veri kalitesi de hesaba katılmalıdır.

## Parametreler fiyatı nasıl etkiler?

| Değişim | Call üzerindeki genel etki | Gerekçe |
|---|---:|---|
| $S_0$ artar | Artar | Satın alma hakkı değerlenir |
| $K$ artar | Azalır | Kullanım pahalılaşır |
| $\sigma$ artar | Artar | Büyük kazanç olasılığı yükselir |
| $T$ artar | Genellikle artar | Olumlu hareket için süre çoğalır |
| $r$ artar | Genellikle artar | Kullanım fiyatının bugünkü değeri düşer |

Modelin en tartışmalı girdisi volatilitedir. Piyasa fiyatından tersine hesaplanan **örtük volatilite**, yatırımcıların gelecekteki belirsizlik beklentisini yansıtır. Gerçekte volatilite sabit değildir; ayrıca fiyatlarda sıçramalar ve kalın kuyruklar görülebilir. Bu yüzden Black-Scholes nihai gerçek değil, güçlü bir referans modelidir: Mantığı öğrenildiğinde binom ağaçları, Monte Carlo simülasyonu ve stokastik volatilite modelleri çok daha anlaşılır hale gelir.
