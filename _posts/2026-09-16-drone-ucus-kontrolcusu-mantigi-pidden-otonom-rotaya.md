---
layout: post
title: "Drone Uçuş Kontrolcüsü Mantığı: PID’den Otonom Rotaya"
math: true
categories: 
  - Bilgi
tags: 
  - drone
  - pid
  - otonom uçuş
  - uçuş kontrolü
  - sensör füzyonu
  - robotik
toc: true
image: /img/drone-ucus-kontrolcusu-11.png
---

![drone-ucus-kontrolcusu-11](/img/drone-ucus-kontrolcusu-11.svg)


Bir drone’u havada tutmak, dört motoru çalıştırıp şans dilemekten çok daha fazlasıdır. Uçuş kontrolcüsü; sensörleri okuyan, aracın mevcut durumunu tahmin eden ve motorlara saniyede yüzlerce kez düzeltme komutu gönderen gerçek zamanlı bir bilgisayardır. Manuel dengeden GPS destekli otonom rotaya kadar bütün uçuş yetenekleri, iç içe çalışan kontrol döngülerine dayanır.

``

## Önce drone neyi kontrol eder?

Bir quadcopter’ın hareketi dört temel eksen üzerinden açıklanır:

| Eksen | Anlamı | Motorların tepkisi |
|---|---|---|
| Roll | Sağa veya sola yatış | Bir taraftaki itki artırılır |
| Pitch | Öne veya arkaya yatış | Ön-arka motor dengesi değiştirilir |
| Yaw | Kendi ekseninde dönüş | Zıt yönde dönen motorlar ayarlanır |
| Throttle | Yükselme ve alçalma | Tüm motorların itkisi değiştirilir |

Kontrolcü, jiroskoptan açısal hızı, ivmeölçerden doğrusal ivmeyi, barometreden yüksekliği ve GPS’ten konumu alır. Ancak hiçbir sensör kusursuz değildir. Jiroskop zamanla sürüklenirken ivmeölçer titreşimlerden etkilenir. Bu nedenle tamamlayıcı filtre veya Kalman filtresi gibi **sensör füzyonu** yöntemleri kullanılır.

Basit bir açı tahmini şöyle düşünülebilir:

$$aci = α(aci + jiroskop \cdot Δt) + (1-α)ivmeolcerAcisi$$

Burada $α$, hızlı fakat sürüklenen jiroskop ile yavaş fakat referans sağlayan ivmeölçer arasındaki güven dengesidir.

## PID: Dengeyi sağlayan üçlü

PID kontrolcü, hedef değer ile ölçülen değer arasındaki $e(t)$ hatasını motor komutuna dönüştürür:

$$u(t)=K_p e(t)+K_i\int e(t)dt+K_d\frac{de(t)}{dt}$$

| Bileşen | Görevi | Fazla olduğunda |
|---|---|---|
| P | Mevcut hataya tepki verir | Drone salınım yapar |
| I | Birikmiş kalıcı hatayı giderir | Yavaş dalgalanma oluşur |
| D | Hatanın değişimini frenler | Gürültü ve motor ısınması artar |

Örneğin roll hedefi $0°$, ölçülen açı $8°$ ise PID, drone’u ters yönde yatıracak motor düzeltmesini üretir. Gerçek sistemlerde genellikle iç içe döngüler bulunur: dış döngü açı hedefini açısal hız hedefine, iç döngü ise açısal hız hatasını motor komutuna çevirir. İç döngü daha hızlı çalışır; çünkü önce gövde dengede kalmalıdır.

Aşağıdaki sade Python örneği tek eksenli PID hesabını gösterir:

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

        return (self.kp * error
                + self.ki * self.integral
                + self.kd * derivative)
```

Dönen değer doğrudan tek motora verilmez. Bir **mixer**, roll, pitch, yaw ve throttle çıktılarını drone geometrisine göre dört motora dağıtır. Komutlar ayrıca güvenli motor aralığında sınırlandırılır; integral teriminin kontrolden çıkmaması için anti-windup uygulanır.

## Denge kontrolünden otonom rotaya

Otonom uçuş, PID’yi ortadan kaldırmaz; onun üzerine yeni katmanlar ekler. Rota planlayıcı waypoint’leri belirler, konum kontrolcüsü istenen hız ve yatışı hesaplar, tutum kontrolcüsü de bu hedefleri motorlara uygular.

```text
Görev planı → Konum hedefi → Hız hedefi
           → Açı hedefi → Açısal hız → Motorlar
```

Drone hedef noktanın kuzeyinde kaldıysa konum döngüsü güneye doğru hız ister. Hız döngüsü bunu uygun pitch ve roll açılarına çevirir. En içteki PID döngüleri ise bu açıları fiziksel olarak gerçekleştirir. Engel algılama eklendiğinde kamera, lidar veya ultrasonik sensörlerden gelen veriler rota planlayıcıya aktarılır.

A* algoritması harita üzerinde düşük maliyetli bir yol bulabilirken RRT, karmaşık ve sürekli uzaylarda hızlı aday rotalar üretir. Fakat planlanan rota uçulabilir olmalıdır; keskin dönüşler, maksimum eğim, batarya ve rüzgâr hesaba katılmalıdır.

Sonuç olarak otonom drone, tek bir akıllı algoritmadan değil, farklı hızlarda çalışan güvenilir katmanlardan oluşur. PID refleksleri, sensör füzyonu denge hissini, rota planlama ise yön duygusunu sağlar. Gökyüzündeki zarif hareketin arkasında sürekli hata hesaplayan oldukça çalışkan bir matematik ekibi vardır.
