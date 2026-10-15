---
layout: post
title: "Robot Parmakları Kaymayı Nasıl Hisseder? Dokunsal Sensörlerin İnce Dünyası"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - dokunsal sensör
  - tactile sensor
  - nesne kayması
  - yapay zeka
  - kuvvet kontrolü
toc: true
image: /img/robot-parmaklari-kaymayi-43.png
---

![robot-parmaklari-kaymayi-43](/img/robot-parmaklari-kaymayi-43.svg)


Bir robotun bardağı ezmeden tutması kolay görünür; ta ki bardak parmaklarının arasından kaymaya başlayana kadar! İnsanlar bu küçük hareketi derideki mekanoreseptörlerle fark edip kavrama kuvvetini istemsizce artırır. Dokunsal sensörler de robotlara benzer bir refleks kazandırarak basınç, titreşim, kesme kuvveti ve temas geometrisi gibi ayrıntıları ölçer.

``

## Dokunmak yalnızca basınç ölçmek değildir

Basit bir temas anahtarı robota yalnızca nesneye değip değmediğini söyler. Gelişmiş bir tactile sensor ise temas yüzeyini küçük hücrelerden oluşan bir harita gibi algılar. Bu hücrelere çoğunlukla **taxel** adı verilir. Kameradaki piksel ışığı ölçerken taxel basınç veya deformasyon ölçer.

Bir kavrayıcı nesneye normal yönde $F_n$ kuvveti uygular. Nesneyi aşağı çeken veya yana kaydıran teğetsel kuvvet ise $F_t$ ile gösterilebilir. Coulomb sürtünme modeline göre kaymama koşulu yaklaşık olarak şöyledir:

$$\vert F_t\vert  \leq \mu F_n$$

Burada $\mu$, yüzeyler arasındaki sürtünme katsayısıdır. $F_t$ sınırı aşarsa nesne kayar. Ancak robot çoğu zaman $\mu$ değerini önceden bilmez; üstelik ıslak bardak, karton kutu ve metal anahtar aynı sürtünmeye sahip değildir. Bu nedenle kaymayı gerçekleştikten sonra görmek yerine, dokunsal sinyallerden **başlangıç aşamasında** tahmin etmek önemlidir.

## Kaymanın dokunsal imzası

Kayma genellikle bir anda tüm temas yüzeyinde başlamaz. Önce temas alanının kenarlarındaki taxeller yer değiştirir; buna kısmi kayma denir. Ardından basınç dağılımı hareket eder ve yüksek frekanslı küçük titreşimler ortaya çıkar. Robot bu değişimleri birkaç farklı yöntemle yakalayabilir:

| Sensör yaklaşımı | Ölçtüğü bilgi | Kayma belirtisi | Güçlü yönü |
|---|---|---|---|
| Piezorezistif | Basınca bağlı direnç | Basınç merkezinin hareketi | Basit ve ekonomik |
| Kapasitif | Elektrotlar arası değişim | Temas alanındaki deformasyon | Yüksek hassasiyet |
| Piezoelektrik | Dinamik kuvvet ve titreşim | Ani, yüksek frekanslı sinyal | Kayma başlangıcında hızlı |
| Optik dokunsal | Elastik yüzeyin görüntüsü | Doku ve hareket alanı | Zengin uzamsal veri |

Basınç merkezinin yatay konumu örneğin şu şekilde hesaplanabilir:

$$x_c = \frac{\sum_i p_i x_i}{\sum_i p_i}$$

Burada $p_i$, ilgili taxelin basıncı; $x_i$ ise konumudur. Ardışık ölçümlerde $x_c$ hızla değişiyorsa temas noktası hareket ediyor olabilir. Yalnızca bu değer yeterli değildir; robot titreşim enerjisini ve teğetsel kuvveti de birlikte değerlendirmelidir.

## Basit bir kayma algılayıcı

Aşağıdaki Python örneği, basınç merkezi hızı ile titreşim seviyesini birleştiren sade bir karar mekanizmasıdır:

```python
import numpy as np

def slip_score(previous, current, vibration, dt=0.01):
    positions = np.arange(len(current))

    old_center = np.sum(previous * positions) / (np.sum(previous) + 1e-9)
    new_center = np.sum(current * positions) / (np.sum(current) + 1e-9)

    center_speed = abs(new_center - old_center) / dt
    score = 0.7 * center_speed + 0.3 * vibration
    return score

score = slip_score(
    np.array([2.0, 4.0, 3.0]),
    np.array([1.0, 2.5, 5.5]),
    vibration=1.8
)

if score > 20:
    grip_force_increment = 0.2
```

Fonksiyon, basınç dağılımının ne kadar hızlı yer değiştirdiğini hesaplar ve bunu titreşim ölçümüyle birleştirir. Eşik aşılırsa kavrama kuvveti küçük bir miktar artırılır. Gerçek sistemlerde sabit eşikler yerine filtreler, destek vektör makineleri veya sinir ağları kullanılabilir.

## Refleks döngüsü neden hızlı olmalı?

Kayma algılamak tek başına yeterli değildir. Sensör okuma, sinyal işleme ve motor komutu arasındaki gecikme çok uzunsa robot durumu anlar ama nesne çoktan yere düşer. Kontrol döngüsü genellikle **algıla → sınıflandır → kuvveti ayarla → tekrar ölç** biçiminde çalışır.

Amaç maksimum kuvvet uygulamak değildir. Fazla kuvvet çileği ezer, yetersiz kuvvet ise bardağı düşürür. İyi bir dokunsal kontrolcü, gereken en düşük güvenli kuvveti bulur. Böylece robot parmakları yalnızca güçlü değil, aynı zamanda nazik ve çevik olur; kısacası robotun tutuşu bir mengene olmaktan çıkıp gerçek bir dokunuşa dönüşür.
