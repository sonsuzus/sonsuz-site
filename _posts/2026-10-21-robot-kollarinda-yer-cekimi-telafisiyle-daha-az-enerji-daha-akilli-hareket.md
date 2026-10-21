---
layout: post
title: "Robot Kollarında Yer Çekimi Telafisiyle Daha Az Enerji, Daha Akıllı Hareket"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - yer çekimi telafisi
  - enerji verimliliği
  - kontrol sistemleri
  - robot kolları
  - mekatronik
toc: true
image: /img/robot-kollarinda-yer-30.png
---

Bir robot kolu hareketsiz görünürken bile motorları pek dinlenmez. Eklemler, kolun ve taşıdığı yükün aşağı düşmesini önlemek için sürekli tork üretir. Yer çekimi telafisi, bu zorunlu yükü yazılımsal kontrol, yaylar, karşı ağırlıklar veya başka mekanik düzeneklerle dengeleyerek enerji tüketimini azaltmayı amaçlar. Kısacası robot, kendi kolunu taşımak yerine asıl görevine odaklanır.

``

## Yer çekimi robot kolunu nasıl etkiler?

Robot kolunun her bağlantısının bir kütlesi ve kütle merkezi vardır. Yer çekimi bu merkezlerde kuvvet oluşturur; eklem motorları da ters yönde tork üretmek zorunda kalır. Basit, tek eklemli bir kol için gerekli dengeleme torku yaklaşık olarak şöyledir:

$$\tau_g = m g l_c \cos(\theta)$$

Burada $m$ bağlantının kütlesi, $g$ yer çekimi ivmesi, $l_c$ eklem ile kütle merkezi arasındaki mesafe, $\theta$ ise kolun açısıdır. Çok eklemli robotlarda tüm bağlantılar birbirini etkiler ve denklem vektörel hâle gelir:

$$M(q)\ddot{q} + C(q,\dot{q})\dot{q} + G(q) + F(\dot{q}) = \tau$$

$G(q)$ terimi, eklemlerin yer çekimine karşı üretmesi gereken torkları temsil eder. Telafinin temel fikri, denetleyiciye önceden hesaplanmış $G(q)$ değerini eklemektir:

$$\tau_{motor} = \tau_{kontrol} + G(q)$$

Böylece geri besleme denetleyicisi büyük konum hataları oluşmasını beklemeden doğru torku uygular.

## Yazılımsal ve mekanik telafi aynı şey mi?

Hayır. Yazılımsal telafi hareket kalitesini artırır ancak motorun fiziksel olarak tork üretme zorunluluğunu ortadan kaldırmaz. Mekanik telafi ise yükün bir kısmını gerçekten yaylara veya karşı ağırlıklara aktarabilir.

| Yaklaşım | Avantaj | Dezavantaj | Enerji etkisi |
|---|---|---|---|
| Model tabanlı yazılım | Hassas ve ayarlanabilir | Doğru model gerektirir | Gereksiz düzeltmeleri azaltır |
| Yay veya gazlı amortisör | Elektrik harcamadan tork sağlar | Çalışma aralığı sınırlı olabilir | Statik tüketimi ciddi azaltabilir |
| Karşı ağırlık | Basit ve güvenilir | Kütleyi ve ataleti artırır | Tutma enerjisini azaltır |
| Rejeneratif sürücü | İnişte enerjiyi geri kazanır | Uyumlu donanım gerekir | Enerjiyi sisteme geri besler |

En iyi sonuç çoğu zaman hibrit çözümdür: mekanik sistem yükün büyük bölümünü taşırken yazılım kalan hatayı düzeltir.

## Enerji tasarrufu nasıl hesaplanır?

Bir eklemde elektriksel tüketimi kabaca tork ve açısal hızla ilişkilendirebiliriz:

$$P_{mekanik} = \tau \omega$$

Kol sabitken $\omega=0$ olduğundan mekanik güç sıfır görünür. Fakat motor sargılarından akım geçtiği için $P_{bakır}=I^2R$ kaybı devam eder. Bu önemli ayrıntı, “hareket etmeyen robot enerji harcamaz” düşüncesini bozar.

Aşağıdaki Python kodu, telafi öncesi ve sonrası bakır kaybını yaklaşık olarak karşılaştırır:

```python
import math

mass = 8.0          # kg
length = 0.45       # metre
angle = math.radians(30)
torque_constant = 0.8  # Nm/A
resistance = 1.2       # ohm
compensation = 0.70    # mekanik olarak karşılanan oran

gravity_torque = mass * 9.81 * length * math.cos(angle)
current_before = gravity_torque / torque_constant
current_after = gravity_torque * (1 - compensation) / torque_constant

loss_before = current_before**2 * resistance
loss_after = current_after**2 * resistance
saving = 100 * (1 - loss_after / loss_before)

print(f"Yer çekimi torku: {gravity_torque:.2f} Nm")
print(f"Tahmini bakır kaybı azalması: %{saving:.1f}")
```

Akım azaldığında kayıp karesel olarak düştüğü için yüzde 70 tork telafisi, ideal koşullarda yüzde 91 civarında bakır kaybı azalması sağlayabilir. Gerçek sistemlerde sürücü kayıpları, sürtünme ve değişken yük nedeniyle sonuç daha düşük olur.

## Tasarımda dikkat edilmesi gerekenler

Yanlış kütle veya kütle merkezi tahmini robotun titremesine, sürüklenmesine ya da gereğinden fazla tork üretmesine yol açabilir. Ayrıca karşı ağırlık enerji kazandırırken robotun ataletini yükseltip hızlı hareketleri pahalılaştırabilir. Bu nedenle başarı yalnızca “daha büyük yay” seçmekten değil; görev çevrimi, yük değişimi, güvenlik ve hareket hızını birlikte değerlendirmekten geçer.

Doğru tasarlanan yer çekimi telafisi daha küçük motorlar, daha düşük sıcaklık, uzun batarya ömrü ve daha güvenli insan-robot etkileşimi sağlar. Robot koluna görünmez bir destek eli vermek, enerji verimliliğinin en etkili yollarından biridir.

![robot-kollarinda-yer-30](/img/robot-kollarinda-yer-30.svg)

