---
layout: post
title: "PID Kontrolörü: Bir Robotun Dengede Kalma Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - pid
  - robotik
  - kontrol-sistemleri
  - arduino
  - matematik
  - denge-robotu
toc: true
image: /img/pid-kontroloru-bir-97.png
---

İki tekerlek üzerinde duran bir robotu, parmağınızın ucunda dik tutmaya çalıştığınız süpürgeye benzetebilirsiniz. Robot biraz öne eğildiğinde tekerleklerini öne sürmeli, fazla hızlandığında ise geri çekmelidir. Bu kararların hızlı, ölçülü ve sürekli alınmasını sağlayan matematiksel kahraman PID kontrolörüdür.


![pid-kontroloru-bir-97](/img/pid-kontroloru-bir-97.svg)

``

## Temel problem: Hata ne kadar büyük?

Denge robotunda sensörler, gövdenin düşey eksene göre açısını ölçer. İstenen açıya **referans**, ölçülen açıya ise **geri bildirim** denir. İkisi arasındaki fark hata sinyalidir:

$$e(t)=r(t)-y(t)$$

Burada $r(t)$ hedef açıyı, $y(t)$ ölçülen açıyı temsil eder. Örneğin hedef $0^\circ$, ölçüm $5^\circ$ ise hata $-5^\circ$ olur. Kontrolör bu hatayı motorların hızına veya torkuna dönüştürür.

PID adı, üç farklı davranışın baş harflerinden gelir: **Oransal**, **İntegral** ve **Türevsel**. Denetim sinyali şu denklemle hesaplanır:

$$u(t)=K_p e(t)+K_i\int_0^t e(\tau)d\tau+K_d\frac{de(t)}{dt}$$

| Bileşen | Neye bakar? | Robottaki etkisi | Fazlası ne yapar? |
|---|---|---|---|
| P | Anlık hata | Eğilmeye hemen karşı koyar | Robot sertçe salınabilir |
| I | Birikmiş hata | Kalıcı açı sapmasını düzeltir | Yığılma ve taşma oluşturabilir |
| D | Hatanın değişim hızı | Düşüşü önceden sezip frenler | Sensör gürültüsünü büyütebilir |

## Üç karakterli bir ekip

**P bileşeni**, robot ne kadar eğilmişse o kadar güçlü tepki verir. $K_p$ küçükse robot uyuşuk davranır; büyükse panikleyen bir garson gibi ileri geri koşturur.

**I bileşeni**, geçmiş hataları toplar. Robot ağırlık merkezi nedeniyle sürekli iki derece öne yatıyorsa P kontrolü küçük bir hatayı kabullenebilir. İntegral terimi bu hatayı biriktirerek sonunda ortadan kaldırır. Ancak robot devrilmiş ve motorlar sınırda çalışıyorsa integral büyümeye devam edebilir. Buna **integral windup** denir.

**D bileşeni**, hatanın yönünü ve değişim hızını izler. Robot hızla öne düşüyorsa henüz açı çok büyümeden güçlü karşılık verir. Böylece sisteme matematiksel bir amortisör eklenmiş olur.

## Bilgisayarda ayrık PID hesabı

Mikrodenetleyici sürekli zamanı değil, örneğin her $10$ milisaniyede bir alınan örnekleri işler. Bu durumda integral ve türev yaklaşık olarak hesaplanır:

$$I_k=I_{k-1}+e_k\Delta t$$

$$D_k=\frac{e_k-e_{k-1}}{\Delta t}$$

Aşağıdaki Arduino tarzı fonksiyon, açı hatasından motor komutu üretir. `constrain` kullanımı integral yığılmasını ve motor sınırlarının aşılmasını azaltır:

```cpp
float updatePID(float target, float angle, float dt) {
    static float integral = 0.0;
    static float previousError = 0.0;

    const float kp = 28.0;
    const float ki = 1.2;
    const float kd = 0.8;

    float error = target - angle;
    integral += error * dt;
    integral = constrain(integral, -20.0, 20.0);

    float derivative = (error - previousError) / dt;
    float output = kp * error + ki * integral + kd * derivative;

    previousError = error;
    return constrain(output, -255.0, 255.0);
}
```

Fonksiyon sabit aralıklarla çağrılmalıdır; değişken `dt`, özellikle türev hesabını bozabilir. Motor komutunun işareti de bağlantı yönüne göre test edilmelidir. Robot öne düşerken motorlar geriye gidiyorsa kontrol sistemi dengelemek yerine düşüşü alkışlıyor demektir.

## PID katsayıları nasıl ayarlanır?

Pratik başlangıç yöntemi, önce $K_i$ ve $K_d$ değerlerini sıfırlamaktır. $K_p$, robot hızlı salınmaya başlayana kadar yavaşça artırılır; ardından biraz azaltılır. Sonra salınımı sönümlemek için $K_d$ eklenir. En son küçük bir $K_i$ değeriyle kalıcı eğim giderilir.

| Belirti | Muhtemel çözüm |
|---|---|
| Robot geç tepki veriyor | $K_p$ artırılabilir |
| Hızlı ileri geri sallanıyor | $K_p$ azaltılabilir veya $K_d$ artırılabilir |
| Sürekli hafif eğik duruyor | $K_i$ artırılabilir |
| Motor komutu doygun kalıyor | İntegral sınırlandırılmalıdır |
| Çıkış titriyor | Türev filtresi ve sensör filtresi kullanılmalıdır |

Başarılı bir denge sistemi yalnızca PID denkleminden ibaret değildir. IMU sensöründeki ivmeölçer ve jiroskop verileri tamamlayıcı ya da Kalman filtresiyle birleştirilmeli, kontrol döngüsü düzenli çalışmalı ve mekanik ağırlık merkezi doğru seçilmelidir. PID sihir değildir; fakat doğru ölçüm ve ayarla robota sürekli şu soruyu sorduran etkili bir refleks mekanizmasıdır: “Ne kadar eğildim, ne zamandır eğik durumdayım ve ne kadar hızlı düşüyorum?”
