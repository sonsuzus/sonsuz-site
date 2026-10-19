---
layout: post
title: "İki Teker Üstünde Dans: Ters Sarkaçla Kendi Kendini Dengeleyen Robot"
math: true
categories: 
  - Proje
tags: 
  - robotik
  - ters sarkaç
  - pid kontrol
  - arduino
  - imu
  - kontrol sistemleri
toc: true
image: /img/iki-teker-ustunde-21.png
---

![iki-teker-ustunde-21](/img/iki-teker-ustunde-21.svg)


İki tekerlekli bir robotun devrilmeden ayakta kalması ilk bakışta sihir gibi görünür. Oysa robotun yaptığı şey, düşmeye başladığı yönü sürekli ölçmek ve tekerleklerini aynı yöne sürerek gövdesini yeniden ağırlık merkezinin altına taşımaktır. Bu hızlı geri besleme döngüsü; mekanik, sensör füzyonu ve kontrol teorisinin eğlenceli bir birleşimidir.
``
## Ters sarkaç mantığı

Normal bir sarkaç aşağı doğru asılıyken kararlıdır. Ters sarkaçta ise kütle, dönme noktasının üzerinde bulunur. Robotun gövdesi dik konumdan çok az uzaklaştığında yer çekimi onu daha da fazla yatırır. Bu nedenle sistem **doğal olarak kararsızdır**.

Robotun eğim açısını $theta$, dik konumu da $theta = 0$ kabul edelim. Basitleştirilmiş açısal hareket yaklaşık olarak şöyle düşünülebilir:

$$I theta'' = m g l sin(theta) - u$$

Burada $I$ eylemsizlik momenti, $m$ gövde kütlesi, $g$ yer çekimi ivmesi, $l$ ağırlık merkezinin tekerlek eksenine uzaklığı ve $u$ motorların oluşturduğu düzeltici etkidir. Küçük açılarda $sin(theta) yaklaşık theta$ olduğundan model doğrusal hâle getirilebilir. Kontrolcünün görevi, uygun $u$ değerini üreterek açıyı sıfıra yaklaştırmaktır.

## Robot eğildiğini nasıl anlar?

MPU6050 gibi bir IMU, ivmeölçer ve jiroskop içerir. İvmeölçer uzun vadede güvenilir bir açı tahmini sunar fakat titreşimlerden etkilenir. Jiroskop hızlı hareketleri iyi ölçer ancak zamanla sürüklenir. İki ölçüm tamamlayıcı filtreyle birleştirilebilir:

$$theta = alpha(theta_{eski} + omega Delta t) + (1-alpha)theta_{ivme}$$

| Sensör | Güçlü yanı | Zayıf yanı |
|---|---|---|
| İvmeölçer | Mutlak eğimi tahmin eder | Motor titreşimlerine duyarlıdır |
| Jiroskop | Hızlı değişimleri yakalar | Zamanla sürüklenir |
| Birleşik tahmin | Daha kararlı sonuç verir | Doğru örnekleme süresi ister |

$alpha$ çoğunlukla 0,95 ile 0,99 arasında seçilir. Böylece kısa vadede jiroskopa, uzun vadede ivmeölçere güvenilir.

## PID kontrolü

En yaygın yaklaşım PID kontrolcüdür. Hata, hedef açı ile ölçülen açı arasındaki farktır:

$$e(t) = theta_{hedef} - theta(t)$$

Kontrol çıkışı ise üç davranışı birleştirir:

$$u(t) = K_p e(t) + K_i integral(e(t)) + K_d de(t)/dt$$

| Terim | Görevi | Fazla olursa |
|---|---|---|
| P | Eğime anında karşı koyar | Robot sallanır |
| I | Kalıcı açı hatasını giderir | Yavaş salınım ve taşma oluşur |
| D | Hızlı değişimi frenler | Gürültü büyütülür |

Aşağıdaki Arduino tarzı örnek, filtrelenmiş açı üzerinden temel kontrol çıkışını hesaplar:

```cpp
float kp = 28.0, ki = 0.8, kd = 1.4;
float integral = 0, previousError = 0;

float updateController(float angle, float dt) {
  float targetAngle = 0.0;
  float error = targetAngle - angle;

  integral += error * dt;
  integral = constrain(integral, -20.0, 20.0);

  float derivative = (error - previousError) / dt;
  previousError = error;

  float output = kp * error + ki * integral + kd * derivative;
  return constrain(output, -255.0, 255.0);
}
```

Fonksiyon, motor sürücüsüne gönderilecek yönlü PWM değerini üretir. İntegral sınırı, motorlar doygundayken hatanın kontrolsüz birikmesini önleyen **anti-windup** yöntemidir. Robot güvenlik açısını, örneğin 35 dereceyi aşarsa motorlar kapatılmalıdır.

## Ayar yaparken izlenecek yol

Önce $K_i$ ve $K_d$ sıfırlanır. $K_p$, robot tepki verene kadar artırılır. Sürekli sallanma başladığında biraz azaltılır. Ardından $K_d$ eklenerek hareket sönümlenir. Son olarak küçük bir $K_i$, ağırlık dağılımından kaynaklanan kalıcı hatayı temizler.

Kontrol döngüsünün sabit aralıklarla, tercihen 200–500 Hz civarında çalışması önemlidir. Gevşek şasi, boşluklu dişliler, düşük torklu motorlar veya gecikmeli yazılım en iyi PID ayarını bile bozabilir. Başarılı bir dengeleme robotu yalnızca iyi kod değil; sağlam mekanik, temiz sensör verisi ve düzenli zamanlama ister. Kısacası robot düşmeyi engellemez; düşüşü saniyede yüzlerce kez ustaca yakalar.
