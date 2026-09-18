---
layout: post
title: "Ters Kinematik: Robot Koluna Hedefi Göster, Açıları O Bulsun"
math: true
categories: 
  - Bilgi
tags: 
  - ters kinematik
  - robotik
  - matematik
  - python
  - simülasyon
  - kinematik
toc: true
image: /img/ters-kinematik-robot-91.png
---

Bir robot koluna “şu noktaya uzan” demek kolaydır; asıl mesele, motorların bunu gerçekleştirmek için kaç derece dönmesi gerektiğini bulmaktır. Ters kinematik, hedef konumdan yola çıkarak eklem açılarını hesaplayan yöntemlerin genel adıdır. Endüstriyel robotlardan oyun karakterlerine kadar uzanan bu konu, geometri ile programlamanın keyifli bir buluşmasıdır.

![ters-kinematik-robot-91](/img/ters-kinematik-robot-91.svg)

``
## İleri ve ters kinematik farkı

Robot kolunun eklem açıları biliniyorsa uç noktanın konumunu hesaplamaya **ileri kinematik** denir. Ters kinematikte ise sonuç bilinir, bilinmeyenler aranır: Robot elinin ulaşması gereken hedef verilir ve uygun eklem açıları çözülür.

| Özellik | İleri kinematik | Ters kinematik |
|---|---|---|
| Girdi | Eklem açıları | Hedef konum ve yönelim |
| Çıktı | Uç nokta konumu | Eklem açıları |
| Çözüm yapısı | Genellikle doğrudan | Sıfır, bir veya birden fazla çözüm |
| Zorluk | Görece kolay | Geometrik ve sayısal olarak zor |
| Kullanım | Simülasyon, konum bulma | Hareket planlama, animasyon |

## İki eklemli düzlemsel kol

Mantığı görmek için uzunlukları $L_1$ ve $L_2$ olan, düzlemde hareket eden iki parçalı bir kol düşünelim. Eklem açıları $\theta_1$ ve $\theta_2$ olsun. İleri kinematik denklemleri şöyledir:

$$
x=L_1\cos(\theta_1)+L_2\cos(\theta_1+\theta_2)
$$

$$
y=L_1\sin(\theta_1)+L_2\sin(\theta_1+\theta_2)
$$

Ters problemde $x$ ve $y$ hedefini bilir, açıları ararız. Önce kosinüs teoreminden ikinci eklemi hesaplarız:

$$
\cos(\theta_2)=\frac{x^2+y^2-L_1^2-L_2^2}{2L_1L_2}
$$

Ardından iki olası dirsek duruşundan biri seçilir:

$$
\theta_2=\operatorname{atan2}(\pm\sqrt{1-\cos^2(\theta_2)},\cos(\theta_2))
$$

Birinci eklem açısı ise şu ifadeyle bulunur:

$$
\theta_1=\operatorname{atan2}(y,x)-\operatorname{atan2}(L_2\sin\theta_2,L_1+L_2\cos\theta_2)
$$

$\pm$ işareti önemlidir: Aynı hedefe “dirsek yukarıda” veya “dirsek aşağıda” olmak üzere iki farklı duruşla ulaşılabilir. Yani robot bazen hedefe giderken küçük bir stil seçimi yapar!

## Python ile geometrik çözüm

Aşağıdaki fonksiyon, iki eklemli kol için iki muhtemel açı çiftini derece cinsinden döndürür. Hedef çalışma alanının dışındaysa hata üretir.

```python
import math

def ters_kinematik(x, y, L1, L2):
    c2 = (x*x + y*y - L1*L1 - L2*L2) / (2 * L1 * L2)

    if not -1 <= c2 <= 1:
        raise ValueError('Hedefe ulaşılamıyor')

    cozumler = []
    for isaret in (1, -1):
        s2 = isaret * math.sqrt(max(0, 1 - c2*c2))
        t2 = math.atan2(s2, c2)
        t1 = math.atan2(y, x) - math.atan2(
            L2 * s2, L1 + L2 * c2
        )
        cozumler.append((math.degrees(t1), math.degrees(t2)))

    return cozumler

print(ters_kinematik(1.2, 0.8, 1.0, 1.0))
```

`atan2`, sıradan arktanjanttan farklı olarak noktanın hangi bölgede bulunduğunu dikkate alır. `max` kullanımıysa kayan nokta hataları nedeniyle karekök içine çok küçük negatif bir değer girmesini önler.

## Ulaşılabilirlik ve tekillikler

Hedef uzaklığı $r=\sqrt{x^2+y^2}$ ile gösterilirse hedef ancak şu koşulda erişilebilirdir:

$$
\vert L_1-L_2\vert \le r\le L_1+L_2
$$

Kol tamamen açıldığında veya kendi üzerine katlandığında **tekillik** oluşabilir. Bu durumlarda küçük bir hedef hareketi, eklemlerde çok büyük hızlar gerektirebilir.

Gerçek robotlarda üç boyut, eklem sınırları ve engeller devreye girdiği için analitik formüller her zaman yeterli olmaz. Jacobian tabanlı yöntemler, gradyan inişi ve CCD gibi sayısal algoritmalar hedefe adım adım yaklaşır. Başarılı bir ters kinematik sistemi yalnızca hedefe ulaşmamalı; güvenli, kararlı ve doğal görünen çözümü de seçmelidir.
