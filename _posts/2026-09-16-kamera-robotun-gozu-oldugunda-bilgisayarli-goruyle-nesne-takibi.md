---
layout: post
title: "Kamera Robotun Gözü Olduğunda: Bilgisayarlı Görüyle Nesne Takibi"
math: true
categories: 
  - Bilgi
tags: 
  - bilgisayarlı görü
  - robotik
  - nesne takibi
  - opencv
  - python
  - pid kontrol
toc: true
image: /img/kamera-robotun-gozu-18.png
---

Bir robotun hareket eden topu izlemesi, raftaki kutuya yönelmesi veya sahibini takip etmesi dışarıdan sihirli görünebilir. Oysa perde arkasında kamera görüntülerini sayılara dönüştüren bilgisayarlı görü, hedefin konumunu tahmin eden algoritmalar ve motorlara komut veren kontrol mekanizmaları birlikte çalışır. Kamera robotun gözü ise nesne takip sistemi de dikkatini nereye yönelteceğine karar veren beynidir.


![kamera-robotun-gozu-18](/img/kamera-robotun-gozu-18.svg)

``

## Görüntüden harekete uzanan zincir

Kamera gerçekte nesneleri değil, piksellerden oluşan kareleri görür. Her karede hedef nesne bulunur, önceki karedeki konumuyla ilişkilendirilir ve robotun nasıl hareket edeceği hesaplanır. Temel işlem hattı şöyledir:

1. Kameradan yeni bir görüntü karesi alınır.
2. Hedef nesne algılanır veya takip edilir.
3. Nesnenin merkez koordinatı hesaplanır.
4. Görüntü merkeziyle hedef merkezi arasındaki hata bulunur.
5. Hata, motor hızına ya da direksiyon açısına dönüştürülür.

Görüntünün genişliği $W$, hedef merkezinin yatay koordinatı $x_t$ olsun. Robotun yönelme hatası:

$$e_x = x_t - \frac{W}{2}$$

şeklinde hesaplanabilir. $e_x < 0$ ise hedef solda, $e_x > 0$ ise sağdadır. Hata sıfıra yaklaştıkça robot hedefe bakıyor demektir. Perspektif kamera modelinde bir noktanın görüntü koordinatı yaklaşık olarak

$$x = f\frac{X}{Z}, \qquad y = f\frac{Y}{Z}$$

ile ifade edilir. Burada $f$ odak uzaklığı, $Z$ ise nesnenin kameraya olan derinliğidir. Bu nedenle nesne yaklaştıkça görüntüde büyür; yalnızca kutu boyutuna bakarak yaklaşık mesafe tahmini yapılabilir.

## Algılama mı, takip mi?

Bu iki kavram sıkça aynı sanılır, ancak görevleri farklıdır.

| Yaklaşım | Ne yapar? | Avantajı | Dezavantajı |
|---|---|---|---|
| Nesne algılama | Her karede hedefi yeniden bulur | Kaybolan hedefi tekrar yakalayabilir | Daha fazla işlem gücü ister |
| Nesne takibi | Önceden seçilen hedefin hareketini izler | Hızlıdır | Örtülme durumunda hedefi kaybedebilir |
| Hibrit sistem | Algılama ve takibi birlikte kullanır | Daha dayanıklıdır | Tasarımı daha karmaşıktır |

YOLO gibi sinir ağı tabanlı algılayıcılar hedefi sınıfıyla birlikte bulabilir. KCF, CSRT ve optik akış gibi takip yöntemleri ise ardışık karelerdeki değişimden yararlanır. Pratik bir robot, hedefi belirli aralıklarla algılayıp aradaki karelerde daha hızlı bir takipçi kullanabilir.

## OpenCV ile basit renk takibi

Aşağıdaki örnek, turuncu bir nesneyi HSV renk uzayında ayırır ve yatay hataya göre robotun yönünü belirler:

```python
import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    ok, frame = camera.read()
    if not ok:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([5, 120, 120])
    upper = np.array([20, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        target = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(target)
        center_x = x + w // 2
        error = center_x - frame.shape[1] // 2

        command = 'sola dön' if error < -30 else 'sağa dön' if error > 30 else 'ileri'
        print(command, 'hata:', error)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Robot Gözü', frame)
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()
```

Kod, en büyük renk bölgesini hedef kabul eder. Gerçek robotta `command` değişkeni seri port, ROS mesajı veya motor sürücü kartı üzerinden fiziksel harekete çevrilir.

## Robot neden titrer?

Ham hata doğrudan motorlara gönderilirse robot sürekli sağa sola oynayabilir. Bunun çözümü PID kontrolüdür:

$$u(t)=K_p e(t)+K_i\int e(t)dt+K_d\frac{de(t)}{dt}$$

$K_p$ anlık hataya tepki verir, $K_i$ kalıcı sapmayı azaltır, $K_d$ ise ani değişimleri yumuşatır. Ayrıca küçük hataların yok sayıldığı bir ölü bölge, görüntü filtreleme ve maksimum hız sınırı sistemi sakinleştirir.

Işık değişimi, hareket bulanıklığı ve nesnenin başka bir cismin arkasına geçmesi gerçek dünyanın sürprizleridir. Kalman filtresiyle konum tahmini, iyi kamera kalibrasyonu ve algılama-takip hibriti kullanıldığında robot yalnızca bakmaz; gördüğünü anlamlandırıp güvenli biçimde peşinden gider.
