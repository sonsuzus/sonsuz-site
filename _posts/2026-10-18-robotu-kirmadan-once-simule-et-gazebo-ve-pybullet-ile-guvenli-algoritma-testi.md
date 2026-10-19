---
layout: post
title: "Robotu Kırmadan Önce Simüle Et: Gazebo ve PyBullet ile Güvenli Algoritma Testi"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - simülasyon
  - gazebo
  - pybullet
  - sim2real
  - ros
toc: true
image: /img/robotu-kirmadan-once-59.png
---

Bir robot algoritmasını doğrudan gerçek donanımda denemek, paraşütü uçaktan atladıktan sonra dikmeye benzer: öğreticidir ama pahalı sonuçlar doğurabilir! Gazebo ve PyBullet gibi robotik simülasyon ortamları; hareket, sensör ve kontrol algoritmalarını fiziksel motora, pahalı kameraya veya hassas robot koluna zarar vermeden sınamamızı sağlar.

``

## Robotik simülasyon neyi taklit eder?

Bir simülatör, robotun yalnızca üç boyutlu modelini ekranda hareket ettirmez. Yer çekimi, sürtünme, çarpışma, eklem sınırları ve sensör gürültüsü gibi fiziksel olayları sayısal olarak hesaplar. Böylece kontrol yazılımı, sanal robotu gerçek bir donanım gibi algılayabilir.

Basit bir eklemin dinamiği şu denklemle özetlenebilir:

$$
I\ddot{\theta} + b\dot{\theta} + g(\theta) = \tau
$$

Burada $I$ eylemsizlik momentini, $b$ sürtünmeyi, $g(\theta)$ yer çekimi etkisini ve $\tau$ motora uygulanan torku temsil eder. Simülasyon motoru, küçük zaman adımlarında bu denklemleri çözerek robotun bir sonraki konumunu tahmin eder. Zaman adımı küçüldükçe sonuç genellikle daha kararlı olur; ancak işlem yükü artar.

## Gazebo ve PyBullet karşılaştırması

Her iki araç da fizik tabanlı test sağlar fakat kullanım alışkanlıkları farklıdır.

| Özellik | Gazebo | PyBullet |
|---|---|---|
| Temel yaklaşım | Kapsamlı robotik dünya simülasyonu | Python odaklı fizik simülasyonu |
| ROS entegrasyonu | Çok güçlü | Ek geliştirme gerektirebilir |
| Sensör seçenekleri | Kamera, LiDAR, IMU ve eklentiler | Daha sade, kodla özelleştirilebilir |
| Öğrenme eğrisi | Orta veya yüksek | Başlangıç için daha kolay |
| Uygun senaryo | Mobil robotlar ve karmaşık ROS projeleri | Kontrol, robot kolu ve pekiştirmeli öğrenme |

![robotu-kirmadan-once-59](/img/robotu-kirmadan-once-59.svg)


Gazebo, bir depo robotunun LiDAR verisini ve ROS mesajlarını gerçek sisteme yakın biçimde denemek için güçlüdür. PyBullet ise hızlı prototipleme, ters kinematik ve binlerce öğrenme bölümünün otomatik çalıştırılması gereken deneylerde oldukça pratiktir.

## PyBullet ile küçük bir deney

Aşağıdaki kod, yer çekimi bulunan sanal bir dünya oluşturur ve hazır bir robot modelini yükler:

```python
import time
import pybullet as p
import pybullet_data

client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

plane_id = p.loadURDF("plane.urdf")
robot_id = p.loadURDF(
    "r2d2.urdf",
    basePosition=[0, 0, 0.5]
)

for _ in range(2400):
    p.stepSimulation()
    time.sleep(1 / 240)

p.disconnect(client)
```

`setGravity`, Dünya koşullarını tanımlar; `loadURDF` robotun gövde ve eklem modelini yükler. `stepSimulation` ise fizik dünyasını bir adım ilerletir. Bu döngüye motor komutları, sensör okumaları ve kontrolcü hesapları eklenerek gerçek algoritma sınanabilir.

## Simülasyondan gerçeğe geçiş sorunu

Simülasyon kusursuz değildir. Model ile gerçek dünya arasındaki fark, **sim-to-real gap** olarak adlandırılır. Gerçek lastiğin sürtünmesi, motor gecikmesi veya kameradaki ışık değişimi modelde tam karşılık bulmayabilir.

| Simülasyonda ideal durum | Gerçek dünyadaki karşılığı |
|---|---|
| Sabit sürtünme katsayısı | Zemine ve sıcaklığa göre değişim |
| Gürültüsüz sensör | Sapma, gecikme ve ölçüm hatası |
| Kesin motor komutu | Boşluk, doygunluk ve aşınma |
| Kusursuz model | Üretim toleransları |

Bu farkı azaltmak için sensörlere rastgele gürültü eklenebilir, kütle ve sürtünme değerleri çeşitlendirilebilir. Bu tekniğe **domain randomization** denir. Örneğin sürtünme katsayısı her deneyde $\mu \sim U(0.5, 0.9)$ dağılımından seçilirse algoritma tek bir ideal zemine ezber yapmaz.

## Güvenli geliştirme sırası

Sağlıklı süreç; algoritmayı önce birim testlerde, ardından simülasyonda, donanım döngülü testlerde ve son olarak düşük hızdaki gerçek robotta çalıştırmaktır. Acil durdurma mekanizması da unutulmamalıdır. Simülasyon gerçek donanımın yerini tamamen almaz; fakat hataları ucuz, tekrarlanabilir ve çoğu zaman eğlenceli hâle getirir. Kısacası önce sanal robot duvara çarpsın, gerçek robot değil!
