---
layout: post
title: "Kendi Kendine Dengelenen Robot: Ters Sarkacı İki Teker Üzerinde Ehlileştirmek"
math: true
categories: 
  - Proje
tags: 
  - robotik
  - ters sarkaç
  - pid
  - arduino
  - imu
  - kontrol sistemleri
toc: true
---

İki tekerlek üzerinde duran bir robot, fizik kurallarına meydan okuyor gibi görünür. Oysa yaptığı şey düşmeyi engellemek değil, düşüşünü sürekli ölçüp tekerleklerini doğru yöne sürerek gövdesini yeniden dengelemektir. Bu proje; mekanik, elektronik, sensör füzyonu ve kontrol teorisini eğlenceli biçimde bir araya getirir.

``

## Ters sarkaç neden kararsızdır?

Normal bir sarkaç aşağı doğru durduğunda kararlıdır; küçük bir itmeden sonra tekrar denge noktasına döner. Ters sarkaçta ise ağırlık merkezi dönme ekseninin üzerindedir. Çok küçük bir açı hatası bile yerçekimi torku oluşturarak sapmayı büyütür.

Basitleştirilmiş yerçekimi torku şöyle yazılabilir:

$$\tau_g = m g l \sin(\theta)$$

Burada $m$ gövde kütlesi, $g$ yerçekimi ivmesi, $l$ ağırlık merkezinin tekerlek eksenine uzaklığı ve $\theta$ eğim açısıdır. Küçük açılarda $\sin(\theta) \approx \theta$ kabul edilir. Böylece sistem yaklaşık doğrusal modellenebilir; fakat kendi hâline bırakıldığında hâlâ kararsızdır.

Robotun görevi, motorların ürettiği karşı torkla bu sapmayı bastırmaktır. Başka bir ifadeyle robot öne düşüyorsa tekerlekler öne kaçmalı, arkaya düşüyorsa arkaya gitmelidir.

## Gerekli bileşenler

| Bileşen | Görevi | Seçim notu |
|---|---|---|
| Mikrodenetleyici | Kontrol döngüsünü çalıştırır | Arduino Nano, ESP32 veya STM32 kullanılabilir |
| IMU | Açısal hız ve ivme ölçer | MPU6050 ekonomik bir başlangıçtır |
| DC motor ve enkoder | Hareket ve konum geri bildirimi sağlar | Boşluksuz redüktör tercih edilmelidir |
| Motor sürücü | Motor akımını kontrol eder | TB6612FNG, L298N'den daha verimlidir |
| Batarya | Sistemi besler | Ani motor akımını karşılayabilmelidir |
| Şasi ve tekerlekler | Mekanik yapıyı oluşturur | Ağırlık merkezi eksenin üzerinde olmalıdır |

## Açıyı doğru ölçmek

İvmeölçer uzun vadede güvenilir açı verir, ancak titreşimden etkilenir. Jiroskop kısa vadede pürüzsüzdür, fakat zamanla sürüklenir. Tam bir “biri iyi biri kötü” hikâyesi değil; ikisi birlikte daha güçlüdür.

| Sensör | Avantaj | Dezavantaj |
|---|---|---|
| İvmeölçer | Mutlak eğim referansı sağlar | Motor titreşimlerine duyarlıdır |
| Jiroskop | Hızlı değişimleri iyi izler | Entegrasyon hatası birikir |
| Birleşik sonuç | Kararlı ve hızlıdır | Filtre ve ayar gerektirir |

Tamamlayıcı filtre şu şekilde kurulabilir:

$$\theta_k = \alpha(\theta_{k-1} + \omega\Delta t) + (1-\alpha)\theta_{acc}$$

Genellikle $\alpha$ değeri 0,95–0,99 arasında seçilir. Kontrol döngüsünün sabit zaman aralığında çalışması kritik önemdedir.

## PID ile denge kontrolü

PID denetleyici, hedef açı ile ölçülen açı arasındaki $e(t)$ hatasını motor komutuna dönüştürür:

$$u(t)=K_p e(t)+K_i\int e(t)dt+K_d\frac{de(t)}{dt}$$

$K_p$ robotu dik konuma iter, $K_d$ salınımı frenler, $K_i$ ise kalıcı küçük hataları giderir. Denge robotlarında integral terimi çoğunlukla çok düşük tutulur; aksi hâlde robot geçmiş hataları fazla ciddiye alıp dramatik bir kaçış gerçekleştirebilir.

```cpp
float error = targetAngle - angle;
integral += error * dt;
float derivative = (error - previousError) / dt;

float output = kp * error
             + ki * integral
             + kd * derivative;

output = constrain(output, -255, 255);
setMotorPower(output);
previousError = error;
```

Bu kod her kontrol çevriminde açı hatasını hesaplar ve iki motora uygulanacak PWM değerini üretir. Robot çok hızlı titreşiyorsa $K_p$ veya $K_d$ yüksek olabilir. Yavaşça devriliyorsa $K_p$ yetersizdir. Sürekli bir tarafa gidiyorsa hedef açıya küçük bir ofset eklenebilir.

## Sağlam bir geliştirme sırası

Önce motor yönlerini ve IMU eksenlerini doğrula. Ardından robotu kaldırarak açı ölçümünü seri portta izle. $K_i=0$ iken düşük $K_p$ ile başla, robot tepki verene kadar artır ve salınımı $K_d$ ile azalt. Enkoderlerden gelen hız bilgisini ikinci bir kontrol döngüsünde kullanmak, robotun dengede dururken odanın öbür ucuna kaçmasını önler.

İlk denemelerde robotu bir askı düzeneğinde çalıştırmak, motor çıkışını sınırlamak ve acil durdurma düğmesi eklemek iyi fikirdir. Başarılı sonuç yalnızca iyi PID ayarına değil; rijit şasiye, düşük mekanik boşluğa, temiz güç hattına ve hızlı örneklemeye bağlıdır. Ters sarkaç tam anlamıyla takım oyunudur.
