---
layout: post
title: "İki Bacaklı Robotlarda Ters Sarkaç ile Denge Kontrolü"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - denge kontrolü
  - ters sarkaç
  - biped robot
  - lqr
  - zmp
toc: true
image: /img/iki-bacakli-robotlarda-52.png
---

![iki-bacakli-robotlarda-52](/img/iki-bacakli-robotlarda-52.svg)


İki bacak üzerinde yürümek insanlar için sıradan, robotlar için ise sürekli çözülmesi gereken bir denge problemidir. Robotun kütle merkezi destek alanının dışına çıktığında yer çekimi hemen devreye girer ve pahalı metal kahramanımız yere doğru dramatik bir yolculuğa başlar. Ters sarkaç modeli, bu karmaşık gövde ve eklem sistemini daha anlaşılır bir fizik problemine dönüştürerek denge denetleyicilerinin tasarlanmasını kolaylaştırır.

``

## Robot neden ters sarkaç olarak modellenir?

Klasik sarkaçta kütle aşağıdadır ve sistem doğal olarak kararlı durumuna dönmek ister. Ters sarkaçta ise kütle dönme noktasının üzerindedir. Küçük bir eğim bile kütlenin daha fazla uzaklaşmasına yol açar. İki bacaklı robot da ayakları üzerinde dururken benzer biçimde **doğal olarak kararsızdır**.

Basitleştirilmiş modelde robotun toplam kütlesi, kütle merkezinde bulunan noktasal bir $m$ kütlesi olarak kabul edilir. Bacak ise uzunluğu $l$ olan, kütlesiz bir çubuk gibi düşünülür. Robotun dikey eksene göre açısı $\theta$ ise temel dinamik yaklaşık olarak şöyledir:

$$ml^2\ddot{\theta}=mgl\sin(\theta)+\tau$$

Burada $g$ yer çekimi ivmesini, $\tau$ ise ayak bileği veya eş değer eklem torkunu gösterir. Denge çevresindeki küçük açılarda $\sin(\theta)\approx\theta$ kabulü yapılabilir:

$$\ddot{\theta}\approx\frac{g}{l}\theta+\frac{1}{ml^2}\tau$$

$\theta$ katsayısının pozitif olması kritik ayrıntıdır: kontrol uygulanmazsa eğim kendiliğinden büyür.

## Basitleştirme seçenekleri

| Model | Varsayım | Avantaj | Sınırlama |
|---|---|---|---|
| Ters sarkaç | Tek dönme noktası ve sabit bacak | Basit kontrol tasarımı | Yürüyüş ayrıntılarını az temsil eder |
| Doğrusal ters sarkaç | Kütle merkezi yüksekliği sabittir | ZMP ve adım planlamada hızlıdır | Dikey hareketleri ihmal eder |
| Çok bağlantılı model | Gövde ve eklemler ayrıdır | Daha gerçekçi sonuç verir | Hesaplama maliyeti yüksektir |

Özellikle **Doğrusal Ters Sarkaç Modeli** (LIPM), kütle merkezinin yatay hareketini incelemek için kullanılır. Sabit $z_c$ yüksekliğinde yatay dinamik:

$$\ddot{x}=\frac{g}{z_c}(x-p)$$

şeklindedir. Buradaki $x$ kütle merkezinin yatay konumu, $p$ ise basınç merkezi veya ideal koşullarda Zero Moment Point (ZMP) konumudur. Dengeyi korumak için $p$ değerinin ayağın oluşturduğu destek çokgeni içinde kalması gerekir.

## Denetleyici nasıl müdahale eder?

Robot; IMU, eklem enkoderleri ve ayak tabanı kuvvet sensörlerinden veri toplar. Bu ölçümlerle açı, açısal hız ve kütle merkezi durumu tahmin edilir. Ardından PID, durum geri besleme veya LQR gibi bir denetleyici düzeltici tork üretir.

Durum vektörü $X=[\theta,\dot{\theta}]^T$ seçildiğinde LQR yaklaşımı

$$u=-KX$$

kontrol yasasını kullanır. $K$ kazancı, açı hatası ile enerji tüketimi arasında sistematik bir denge kurar. Aşağıdaki Python örneği, basitleştirilmiş bir geri besleme döngüsünü simüle eder:

```python
import numpy as np

m, l, g = 20.0, 0.8, 9.81
dt = 0.002
K = np.array([450.0, 90.0])
state = np.array([0.12, 0.0])  # açı ve açısal hız

for _ in range(3000):
    theta, omega = state
    torque = -K @ state
    acceleration = (g / l) * theta + torque / (m * l**2)

    omega += acceleration * dt
    theta += omega * dt
    state = np.array([theta, omega])

print(f"Son açı: {np.degrees(state[0]):.4f} derece")
```

Kod, robot öne eğildiğinde ters yönde tork uygulayarak açıyı sıfıra yaklaştırır. Gerçek robotta tork sınırları, sensör gürültüsü, gecikme ve ayağın kayması da modele eklenmelidir.

## Ayakta durmaktan yürümeye

Yürüme sırasında destek noktası sürekli değişir. Denetleyici yalnızca mevcut düşüşü engellemez; bir sonraki ayağın nereye basacağını da planlar. Küçük bozucular ayak bileği torkuyla, daha büyük bozucular kalça hareketiyle, çok güçlü itmeler ise yeni bir adımla karşılanır. Böylece ters sarkaç modeli, kusursuz bir robot kopyası olmaktan ziyade, karmaşık denge problemini gerçek zamanlı çözülebilen kullanışlı bir haritaya dönüştürür.
