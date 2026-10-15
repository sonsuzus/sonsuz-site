---
layout: post
title: "İHA Uçuş Kontrolcüleri Rüzgâra Nasıl Meydan Okur?"
math: true
categories: 
  - Bilgi
tags: 
  - iha
  - drone
  - uçuş kontrolü
  - pid
  - robotik
  - rüzgar dayanıklılığı
toc: true
image: /img/iha-ucus-kontrolculeri-78.png
---

Bir drone sakin havada uslu bir robot gibi davranabilir; ancak rüzgâr başladığında işler hızla değişir. Ani yön değişimleri, pervane itkisindeki dengesizlikler ve gövde üzerindeki aerodinamik kuvvetler, İHA’yı hedeflenen konumdan uzaklaştırır. Uçuş kontrolcüsünün görevi bu bozucu etkileri algılamak, uygun motor komutlarını hesaplamak ve araç daha ne olduğunu anlamadan dengeyi yeniden kurmaktır.
``

## Rüzgâr neden bir bozucudur?

Bir İHA’nın hareketi basitleştirilmiş biçimde Newton’un ikinci yasasıyla açıklanabilir:

$$m\vec{a}=\vec{F}_{itki}+\vec{F}_{yerçekimi}+\vec{F}_{rüzgar}$$

Burada $\vec{F}_{rüzgar}$ kontrolcünün doğrudan yönetemediği dış kuvvettir. Rüzgârın sürükleme kuvveti yaklaşık olarak

$$F_d=\frac{1}{2}\rho C_d A v_r^2$$

ile modellenir. $\rho$ hava yoğunluğu, $C_d$ sürükleme katsayısı, $A$ rüzgâra maruz kalan alan ve $v_r$ bağıl hava hızıdır. Hızın karesi özellikle önemlidir: Rüzgâr iki katına çıktığında sürükleme yaklaşık dört katına çıkabilir. Küçük drone’un neden sert rüzgârda alışveriş poşeti gibi savrulduğu böylece anlaşılır.

## Kontrol döngüleri nasıl çalışır?

Modern uçuş kontrolcüleri genellikle iç içe geçmiş kontrol döngüleri kullanır. En içte açısal hız, onun dışında tutum, daha dışta hız ve konum kontrolü bulunur. İç döngüler yüzlerce veya binlerce hertz hızında çalışırken GPS tabanlı konum döngüsü daha yavaştır.

| Kontrol katmanı | Ölçülen büyüklük | Tipik sensör | Rüzgâra karşı görevi |
|---|---|---|---|
| Açısal hız | Roll, pitch, yaw hızı | Jiroskop | Ani dönmeleri bastırır |
| Tutum | Gövde açıları | IMU | Aracı istenen eğimde tutar |
| Hız | Yatay ve düşey hız | GPS, optik akış | Sürüklenmeyi azaltır |
| Konum | Dünya koordinatları | GPS, GNSS-RTK | Aracı hedef noktaya döndürür |

![iha-ucus-kontrolculeri-78](/img/iha-ucus-kontrolculeri-78.svg)


Rüzgâr drone’u sağa sürüklediğinde konum kontrolcüsü sola doğru hız talep eder. Hız kontrolcüsü bu talebi bir eğim açısına dönüştürür; tutum kontrolcüsü de motorların devirlerini değiştirir. Sonuçta drone, rüzgâra doğru hafifçe yatıp konumunu korur.

## PID kontrolünün rolü

Yaygın PID kontrol yasası şöyledir:

$$u(t)=K_p e(t)+K_i\int e(t)dt+K_d\frac{de(t)}{dt}$$

$K_p$ mevcut hataya tepki verir, $K_i$ sürekli rüzgârın oluşturduğu kalıcı kaymayı giderir, $K_d$ ise hızlı değişimleri sönümler. Fazla yüksek kazançlar titreşime, düşük kazançlar ise ağır ve yetersiz tepkiye yol açar.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| PID | Basit, hızlı ve ucuz | Değişen koşullara uyumu sınırlı |
| LQR | Çok değişkenli sistemi birlikte yönetir | Doğru model gerektirir |
| MPC | Kısıtları ve geleceği hesaba katar | Yüksek işlem yükü oluşturur |
| Adaptif kontrol | Rüzgâra göre kendini ayarlayabilir | Tasarımı ve doğrulaması zordur |

Aşağıdaki örnek, yatay hız hatasından pitch komutu üreten sade bir PID döngüsüdür:

```python
class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0.0
        self.previous_error = 0.0

    def update(self, target, measured, dt):
        error = target - measured
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        self.previous_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

pid = PID(0.8, 0.15, 0.05)
pitch_command = pid.update(target=0.0, measured=1.2, dt=0.01)
```

Burada hedef hız sıfırdır; ölçülen pozitif hız rüzgâr kaynaklı sürüklenmeyi temsil eder. Üretilen pitch komutu, drone’un ters yönde kuvvet oluşturmasını sağlar. Gerçek sistemlerde integral taşmasını önleyen sınırlar, çıkış doyumu ve türev filtresi de eklenmelidir.

## Dayanıklılığı artıran unsurlar

Başarılı rüzgâr dayanıklılığı yalnızca kontrol algoritmasına bağlı değildir. Düşük gürültülü IMU, doğru sensör füzyonu, rijit gövde, yeterli motor rezervi ve dengeli pervaneler birlikte çalışmalıdır. Kalman filtresi; jiroskop, ivmeölçer, barometre ve GPS verilerini birleştirerek daha güvenilir durum tahmini üretir.

Kontrolcü ayrıca motorların maksimum itki sınırını bilmelidir. Rüzgârı yenmek için gereken kuvvet fiziksel kapasiteyi aşarsa dünyanın en akıllı algoritması bile mucize yaratamaz. Bu nedenle dayanıklı bir İHA; iyi modellenmiş, doğru ayarlanmış, simülasyonda sınanmış ve kontrollü saha testleriyle doğrulanmış sistemdir. Kısacası rüzgârla kavga etmek yerine onu ölçer, tahmin eder ve motorlara doğru karşı hamleyi yaptırır.
