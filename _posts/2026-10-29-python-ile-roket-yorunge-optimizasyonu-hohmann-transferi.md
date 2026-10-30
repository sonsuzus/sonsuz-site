---
layout: post
title: "Python ile Roket Yörünge Optimizasyonu: Hohmann Transferi"
math: true
categories: 
  - Proje
tags: 
  - python
  - uzay
  - yörünge
  - optimizasyon
  - hohmann-transferi
  - fizik
toc: true
image: /img/python-ile-roket-78.png
---

Gezegenler arası yolculukta en kısa rota her zaman en ekonomik rota değildir. Uzay araçları, yakıt depolarını hızla tüketmek yerine Güneş’in kütleçekiminden yararlanarak uzun ve zarif elipsler çizer. Hohmann transfer yörüngesi, aynı düzlemde bulunan yaklaşık dairesel iki yörünge arasında geçiş yapmak için gereken toplam hız değişimini, yani $\Delta v$ değerini küçülten klasik yöntemlerden biridir.

``

## Hohmann transferinin temel fikri

İç yörüngenin yarıçapı $r_1$, dış yörüngenin yarıçapı $r_2$ olsun. Transfer yörüngesi, bir ucu ilk gezegenin yörüngesine, diğer ucu hedef gezegenin yörüngesine değen bir elipstir. Bu elipsin yarı büyük ekseni:

$$
a_t = \frac{r_1+r_2}{2}
$$

Bir gökcisminin merkezi etrafındaki herhangi bir noktada hız, vis-viva denklemiyle bulunabilir:

$$
v = \sqrt{\mu\left(\frac{2}{r}-\frac{1}{a}\right)}
$$

Burada $\mu=GM$, merkezdeki cismin standart kütleçekim parametresi; $r$ anlık uzaklık, $a$ ise yörüngenin yarı büyük eksenidir. Dairesel yörüngede $a=r$ olduğundan hız $v=\sqrt{\mu/r}$ biçimine iner.

Transfer iki motor ateşlemesi gerektirir. İlk ateşleme aracı başlangıçtaki dairesel yörüngeden elipse taşır. İkinci ateşleme ise hedef yörüngede eliptik hareketi daireselleştirir:

$$
\Delta v_1=\sqrt{\frac{\mu}{r_1}}\left(\sqrt{\frac{2r_2}{r_1+r_2}}-1\right)
$$

$$
\Delta v_2=\sqrt{\frac{\mu}{r_2}}\left(1-\sqrt{\frac{2r_1}{r_1+r_2}}\right)
$$

Toplam maliyet $\Delta v_{toplam}=\vert \Delta v_1\vert +\vert \Delta v_2\vert $ olur. Roket mühendisliğinde küçük bir $\Delta v$ farkı bile ciddi miktarda yakıt demektir; çünkü yakıt ihtiyacı roket denkleminde üstel davranır.

| Özellik | Doğrudan hızlı rota | Hohmann transferi |
|---|---:|---:|
| Yakıt ihtiyacı | Yüksek | Genellikle düşük |
| Seyahat süresi | Daha kısa olabilir | Daha uzundur |
| Motor ateşlemesi | Göreve bağlı | İdeal modelde iki |
| Hesaplama karmaşıklığı | Yüksek olabilir | Düşük |
| Gerçekçilik | Ayrıntılı modellerde iyi | İlk yaklaşım için iyi |

## Python ile Dünya–Mars hesabı

Aşağıdaki program, Dünya ve Mars yörüngelerini dairesel kabul ederek gerekli hız değişimlerini ve transfer süresini hesaplar. Birimler kilometre ve saniye olarak tutarlı seçilmiştir.

```python
from math import sqrt, pi

MU_SUN = 1.32712440018e11  # km^3/s^2
AU = 149_597_870.7         # km
DAY = 86_400               # saniye


def hohmann_transfer(r1, r2, mu):
    """İki dairesel yörünge arasındaki Hohmann transferini hesaplar."""
    transfer_a = (r1 + r2) / 2

    circular_v1 = sqrt(mu / r1)
    circular_v2 = sqrt(mu / r2)
    transfer_v1 = sqrt(mu * (2 / r1 - 1 / transfer_a))
    transfer_v2 = sqrt(mu * (2 / r2 - 1 / transfer_a))

    delta_v1 = transfer_v1 - circular_v1
    delta_v2 = circular_v2 - transfer_v2

    # Transfer, eliptik yörüngenin yarım periyodu kadar sürer.
    travel_time = pi * sqrt(transfer_a**3 / mu)
    return delta_v1, delta_v2, travel_time


dv1, dv2, duration = hohmann_transfer(AU, 1.524 * AU, MU_SUN)

print(f"İlk ateşleme: {dv1:.3f} km/s")
print(f"İkinci ateşleme: {dv2:.3f} km/s")
print(f"Toplam Δv: {abs(dv1) + abs(dv2):.3f} km/s")
print(f"Seyahat süresi: {duration / DAY:.1f} gün")
```

Sonuç yaklaşık 259 günlük bir seyahat verir. Buradaki hız değişimleri, gezegenlerin Güneş çevresindeki yörüngeleri arasındaki ideal geçişi temsil eder; Dünya’dan kalkış, atmosfer kayıpları, park yörüngesi ve Mars’a iniş hesaba katılmaz.

## Zamanlama neden önemlidir?

Mars’a doğru yola çıkmak için yalnızca doğru hız yetmez; Mars’ın varış anında elipsin diğer ucunda bulunması gerekir. Bu nedenle fırlatma penceresi, gezegenlerin açısal konumlarına göre belirlenir. Hedef gezegenin açısal hızı $n_2=\sqrt{\mu/r_2^3}$ ise yaklaşık başlangıç faz açısı:

$$
\phi=\pi-n_2t_H
$$

şeklinde hesaplanabilir. Gerçek görevlerde yörüngeler eliptik ve eğimli olduğundan Lambert çözücüleri, sayısal integrasyon ve kısıtlı optimizasyon algoritmaları kullanılır. Yine de Hohmann modeli, karmaşık uzay görevlerine geçmeden önce fiziksel sezgi geliştiren güçlü bir başlangıçtır: Uzayda sabır çoğu zaman yakıttan daha ucuzdur.

![python-ile-roket-78](/img/python-ile-roket-78.svg)

