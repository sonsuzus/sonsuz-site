---
layout: post
title: "Fazladan Eklem, Fazladan Kaçış: Redundant Robot Kollarda Engel Atlama"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - redundant manipülatör
  - engel kaçınma
  - ters kinematik
  - jacobian
  - optimizasyon
toc: true
image: /img/fazladan-eklem-fazladan-66.png
---

Bir robot kolunun görevi yalnızca hedefe ulaşmak değildir; bunu masaya, duvara veya merakla yaklaşan başka bir robota çarpmadan yapması gerekir. Redundant, yani artıklıklı çok eklemli kollar tam bu noktada avantaj sağlar. Uç efektörün konumu değişmeden dirseklerini ve diğer eklemlerini hareket ettirebilen bu robotlar, engeller karşısında adeta “hedefe bakarken belini büken” mekanik akrobatlara dönüşür.
``
## Artıklılık ne anlama gelir?

Bir manipülatörün eklem değişkenlerini $q \in R^n$, uç efektör görevini ise $x \in R^m$ ile gösterelim. İleri kinematik ilişki

$$x = f(q)$$

şeklindedir. Eğer eklem sayısı görev uzayının boyutundan büyükse, yani $n > m$ ise sistem redundant kabul edilir. Örneğin üç boyutlu uzayda yalnızca uç noktanın konumunu kontrol etmek için üç bağımsız değişken yeterliyken yedi eklemli bir kol dört adet fazladan serbestlik derecesine sahiptir.

Bu fazlalık gereksiz değildir. Aynı uç efektör konumunu üreten birden fazla eklem yapılandırması bulunabilir. Robot böylece ana görevi bozmadan dirseğini bir engelden uzaklaştırabilir, eklem sınırlarından kaçabilir veya daha rahat bir duruş seçebilir.

| Özellik | Minimum serbestlikli kol | Redundant kol |
|---|---|---|
| Aynı hedef için çözüm | Genellikle sınırlı | Çok sayıda |
| Engel çevresinde hareket | Kısıtlı | Esnek |
| Eklem sınırlarından kaçış | Zor | İkincil görevle mümkün |
| Hesaplama maliyeti | Daha düşük | Daha yüksek |
| Arıza toleransı | Düşük | Görece yüksek |

![fazladan-eklem-fazladan-66](/img/fazladan-eklem-fazladan-66.svg)


## Jacobian ve sıfır uzayı

Eklem hızları ile uç efektör hızı arasındaki ilişki Jacobian matrisiyle kurulur:

$$\dot{x} = J(q)\dot{q}$$

Redundant bir sistemde ters çözüm tek değildir. Yaygın hız çözümü şöyledir:

$$\dot{q} = J^+\dot{x} + (I-J^+J)z$$

Burada $J^+$ Jacobian'ın sözde tersidir. İlk terim uç efektörü hedeflenen yönde hareket ettirir. İkinci terim ise Jacobian'ın sıfır uzayında kalır; başka bir deyişle uç efektör hareketini değiştirmeden eklemleri oynatır. Engel kaçınma sihrinin büyük bölümü bu ikinci terimdedir.

$z$ vektörü, robotu engelden uzaklaştıran bir maliyet fonksiyonunun negatif gradyanı olarak seçilebilir:

$$z = -k \nabla H(q)$$

$H(q)$ robot ile engel arasındaki mesafe azaldıkça büyüyen bir ceza fonksiyonu olabilir. Böylece robot bir eliyle hedefe ilerlerken “dirseğini içeri çekebilir.”

## Basit bir hesaplama örneği

Aşağıdaki Python kodu, ana uç efektör hızına sıfır uzayı üzerinden ikincil bir kaçınma hareketi ekler:

```python
import numpy as np

def redundant_velocity(J, target_velocity, avoidance_gradient, gain=0.4):
    J_pinv = np.linalg.pinv(J)
    identity = np.eye(J.shape[1])

    primary = J_pinv @ target_velocity
    null_space = identity - J_pinv @ J
    secondary = null_space @ (-gain * avoidance_gradient)

    return primary + secondary
```

`primary` hedefe ulaşma görevini gerçekleştirir. `secondary` ise engel maliyetini azaltmaya çalışır. `null_space` izdüşümü sayesinde ikincil hareket, ideal matematiksel koşullarda uç efektörün istenen hızını bozmaz.

## Potansiyel alan yaklaşımı

Engeller çoğu zaman itici potansiyel alanlarla modellenir. Engel ile robot noktası arasındaki mesafe $d$, etkinin başladığı güvenli mesafe $d_0$ olsun:

$$U(d) = \frac{1}{2}\eta\left(\frac{1}{d}-\frac{1}{d_0}\right)^2, \quad d < d_0$$

Robot engelden uzaktaysa ceza sıfırdır; yaklaştıkça hızla büyür. Bu yöntem sezgiseldir fakat yerel minimumlara takılabilir. Ayrıca yalnızca uç efektörü değil, dirsek ve bağlantılar üzerindeki örnek noktaları da kontrol etmek gerekir.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Potansiyel alan | Hızlı ve sezgisel | Yerel minimum oluşturabilir |
| Sıfır uzayı kontrolü | Ana görevi korur | Tekilliklere duyarlıdır |
| Optimizasyon tabanlı kontrol | Kısıtları birlikte işler | Daha fazla hesaplama ister |

Sonuç olarak fazladan serbestlik derecesi, robota yalnızca daha fazla hareket değil, aynı hedefe giderken daha iyi hareket seçme özgürlüğü verir. Doğru kontrol algoritmasıyla redundant kol; engellerden kaçınabilir, eklem sınırlarını koruyabilir ve çalışma alanında çok daha güvenli davranabilir.
