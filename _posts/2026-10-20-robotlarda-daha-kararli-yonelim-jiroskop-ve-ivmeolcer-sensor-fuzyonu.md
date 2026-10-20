---
layout: post
title: "Robotlarda Daha Kararlı Yönelim: Jiroskop ve İvmeölçer Sensör Füzyonu"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - sensör füzyonu
  - jiroskop
  - ivmeölçer
  - yönelim tahmini
  - tamamlayıcı filtre
toc: true
image: /img/robotlarda-daha-kararli-13.png
---

Bir robotun dengesini koruması, doğru yöne dönmesi veya eğimli bir zeminde hareket etmesi için uzaydaki yönelimini bilmesi gerekir. Fakat tek bir sensöre güvenmek çoğu zaman yeterli değildir: Jiroskop zamanla sürüklenirken ivmeölçer titreşimlerden etkilenir. Sensör füzyonu, bu iki huysuz sensörü birlikte çalıştırarak daha güvenilir bir yönelim tahmini üretir.

``

## Sensörler neyi ölçer?

Jiroskop, robotun eksenler çevresindeki açısal hızını ölçer. Örneğin $x$ eksenindeki ölçüm $\omega_x$ ise kısa bir zaman aralığındaki açı değişimi yaklaşık olarak şöyledir:

$$
\theta_t = \theta_{t-1} + \omega_t \Delta t
$$

Bu entegrasyon kısa vadede oldukça başarılıdır. Ancak sensördeki küçücük bir ofset sürekli toplandığı için tahmin zamanla gerçek açıdan uzaklaşır. Buna **drift**, yani sürüklenme denir.

İvmeölçer ise doğrusal ivmeyi ve yerçekimi etkisini ölçer. Robot hareketsizken ölçümün baskın bileşeni yerçekimidir. Böylece roll ve pitch açıları hesaplanabilir:

$$
roll = \operatorname{atan2}(a_y, a_z)
$$

$$
pitch = \operatorname{atan2}(-a_x, \sqrt{a_y^2 + a_z^2})
$$

Ne var ki robot aniden hızlandığında sensör yalnızca yerçekimini değil, hareketten doğan ivmeyi de görür. Motor titreşimleri de ölçümü gürültülü hâle getirir.

| Özellik | Jiroskop | İvmeölçer |
|---|---|---|
| Ölçtüğü büyüklük | Açısal hız | Doğrusal ivme |
| Kısa vadeli davranış | Hızlı ve düzgün | Gürültülü olabilir |
| Uzun vadeli davranış | Sürüklenir | Yerçekimine göre kararlıdır |
| Güçlü yönü | Ani dönüşleri izlemek | Mutlak eğim referansı vermek |
| Zayıf yönü | Ofset birikmesi | Hareket ve titreşim etkisi |

## Tamamlayıcı filtre mantığı

Tamamlayıcı filtre, jiroskobun kısa vadeli çevikliğini ivmeölçerin uzun vadeli kararlılığıyla birleştirir. Temel denklem şöyledir:

$$
\theta = \alpha(\theta_{eski} + \omega \Delta t) + (1-\alpha)\theta_{acc}
$$

Burada $\alpha$ genellikle 0,90 ile 0,99 arasında seçilir. Büyük bir değer jiroskoba daha fazla güvenilmesi anlamına gelir. Filtrenin fiziksel zaman sabiti biliniyorsa katsayı şu şekilde belirlenebilir:

$$
\alpha = \frac{\tau}{\tau + \Delta t}
$$

$\tau$ büyüdükçe filtre ivmeölçer düzeltmelerine daha yavaş tepki verir. Böylece titreşimler bastırılır; ancak gerçek eğim değişikliklerinin düzeltilmesi de gecikir.

## Python ile örnek uygulama

Aşağıdaki sınıf, roll açısı için basit bir tamamlayıcı filtre uygular. `gyro_rate` radyan/saniye, ivmeölçer değerleri ise aynı ölçek biriminde kabul edilir.

```python
import math

class ComplementaryFilter:
    def __init__(self, tau=0.5):
        self.tau = tau
        self.roll = 0.0

    def update(self, gyro_rate, ay, az, dt):
        # İvmeölçerden yerçekimine dayalı roll tahmini
        accel_roll = math.atan2(ay, az)

        # Örnekleme süresine göre filtre katsayısı
        alpha = self.tau / (self.tau + dt)

        # Jiroskop entegrasyonu ve ivmeölçer düzeltmesi
        gyro_roll = self.roll + gyro_rate * dt
        self.roll = alpha * gyro_roll + (1 - alpha) * accel_roll

        return self.roll
```

Örneğin döngü 100 Hz hızında çalışıyorsa $\Delta t$ yaklaşık 0,01 saniyedir. Yine de sabit bir değer varsaymak yerine iki ölçüm arasındaki gerçek süreyi hesaplamak daha doğrudur. Zamanlama hataları doğrudan entegrasyon hatasına dönüşür.

## Kalibrasyon ve pratik ayrıntılar

Robot hareketsizken birkaç yüz jiroskop örneğinin ortalaması alınarak ofset belirlenmeli ve sonraki ölçümlerden çıkarılmalıdır. Sensör eksenlerinin robot koordinat sistemiyle uyumlu olduğu da doğrulanmalıdır; aksi hâlde robot öne eğilirken algoritma bunu yana eğilme sanabilir.

Titreşimli platformlarda ivmeölçer verisine alçak geçiren filtre uygulanabilir. Çok dinamik sistemlerde ise tamamlayıcı filtre yerine Kalman veya genişletilmiş Kalman filtresi tercih edilebilir. Bu yöntemler sensör belirsizliklerini matematiksel olarak modeller, fakat daha fazla işlem gücü ve dikkatli ayar ister.

Son olarak, ivmeölçer yerçekimi sayesinde roll ve pitch açılarını düzeltebilir; ancak yerçekimi yaw açısı hakkında bilgi vermez. Uzun süreli yaw kararlılığı gerekiyorsa manyetometre, kamera ya da başka bir harici referans sisteme eklenmelidir.

![robotlarda-daha-kararli-13](/img/robotlarda-daha-kararli-13.svg)

