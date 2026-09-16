---
layout: post
title: "Kalman Filtresiyle Sensör Füzyonu: Gürültüden Güvenilir Konuma"
math: true
categories: 
  - Bilgi
tags: 
  - kalman filtresi
  - sensör füzyonu
  - konum kestirimi
  - python
  - imu
  - gps
toc: true
---

Bir robotun GPS verisi bir sağa bir sola sıçrarken ivmeölçeri en küçük titreşimi bile hareket sanabilir. Peki telefonlar, dronlar ve otonom araçlar bu karmaşadan nasıl düzgün bir konum çıkarır? Cevap çoğu zaman Kalman filtresidir: Ölçümlere körü körüne inanmak yerine model ile sensörler arasında matematiksel bir güven pazarlığı yapan akıllı bir tahmin mekanizması.

``

## Temel fikir: Tahmin et, ölç, düzelt

Kalman filtresi, sistemin durumunu doğrudan bilmediğimizi kabul eder. Bunun yerine konum ve hız gibi değişkenleri bir **durum vektöründe** toplar. Tek boyutlu hareket için şöyle bir vektör kullanabiliriz:

$$x_k = [p_k, v_k]^T$$

Burada $p_k$ konumu, $v_k$ hızı, $k$ ise zaman adımını gösterir. Sabit hızlı hareket varsayımında yeni durumun modeli şöyledir:

$$x_k = F x_{k-1} + w_k$$

$F$ durum geçiş matrisi, $w_k$ ise modelin açıklayamadığı süreç gürültüsüdür. Zaman aralığı $dt$ olduğunda geçiş matrisi $F = [[1, dt], [0, 1]]$ biçimindedir. Yani yeni konum, eski konuma hız çarpı zaman eklenerek bulunur.

Sensör ölçümü ise şu modelle ifade edilir:

$$z_k = H x_k + v_k$$

Buradaki $H$, durumun hangi bölümünün ölçüldüğünü; $v_k$ ise sensör gürültüsünü temsil eder. Örneğin GPS yalnızca konum veriyorsa $H = [1, 0]$ olur.

## Sensörler neden birleştirilir?

Her sensörün farklı bir süper gücü ve zayıflığı vardır:

| Sensör | Güçlü yanı | Zayıf yanı | Füzyondaki rolü |
|---|---|---|---|
| GPS | Uzun vadede mutlak konum verir | Gürültülü ve yavaştır | Biriken hatayı düzeltir |
| İvmeölçer | Hızlı tepki verir | Sapma zamanla büyür | Kısa süreli hareketi izler |
| Jiroskop | Dönüşleri hassas ölçer | Drift üretir | Yönelim değişimini yakalar |
| Enkoder | Tekerlek hareketini ölçer | Kaymada yanılır | Yerel hareket tahmini sağlar |

Kalman filtresi hızlı sensörlerle sık tahmin yapıp GPS gibi mutlak ölçümler geldiğinde sonucu düzeltir. Böylece GPS’in sıçramaları yumuşatılırken yalnızca IMU kullanmanın oluşturacağı sürüklenme de sınırlandırılır.

## Belirsizlik işin merkezinde

Filtre yalnızca konumu değil, tahminine ne kadar güvendiğini de taşır. Bu güven, $P$ hata kovaryans matrisiyle temsil edilir. Süreç gürültüsü kovaryansı $Q$, hareket modelinin; ölçüm gürültüsü kovaryansı $R$ ise sensörün belirsizliğini anlatır.

Tahmin aşaması:

$$x_k^- = F x_{k-1}$$

$$P_k^- = F P_{k-1} F^T + Q$$

Düzeltme aşamasında önce Kalman kazancı hesaplanır:

$$K_k = P_k^- H^T (H P_k^- H^T + R)^{-1}$$

$R$ büyükse filtre sensöre daha az, modele daha çok güvenir. $P$ büyüdüğünde ise yeni ölçüm daha etkili olur. Ardından ölçüm ile tahmin arasındaki fark kullanılır:

$$x_k = x_k^- + K_k(z_k - Hx_k^-)$$

## Python ile basit konum filtresi

Aşağıdaki sınıf, sabit hızlı tek boyutlu hareketi izler ve gürültülü konum ölçümlerini süzer:

```python
import numpy as np

class PositionKalman:
    def __init__(self, dt, process_noise=0.1, measurement_noise=4.0):
        self.x = np.array([[0.0], [0.0]])  # konum, hız
        self.F = np.array([[1.0, dt], [0.0, 1.0]])
        self.H = np.array([[1.0, 0.0]])
        self.P = np.eye(2) * 10.0
        self.Q = np.eye(2) * process_noise
        self.R = np.array([[measurement_noise]])
        self.I = np.eye(2)

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x[0, 0]

    def update(self, measured_position):
        z = np.array([[measured_position]])
        innovation = z - self.H @ self.x
        innovation_cov = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(innovation_cov)

        self.x = self.x + K @ innovation
        self.P = (self.I - K @ self.H) @ self.P
        return self.x[0, 0]
```

`predict()` hareket modeline göre ara konumu üretir. `update()` ise GPS benzeri bir ölçüm geldiğinde yenilik değerini hesaplayıp tahmini düzeltir. Gerçek uygulamalarda $Q$ ve $R$ değerleri sensör kayıtları incelenerek ayarlanmalıdır; yanlış ayar, filtrenin ya aşırı titrek ya da tembel olmasına neden olur.

Kalman filtresi sihirli bir gürültü silgisi değildir. Doğru hareket modeli, gerçekçi belirsizlikler ve sensörlerin zaman eşlemesi şarttır. Ancak bu parçalar yerli yerine oturduğunda, birbirinden şüpheli sensörler birlikte oldukça güvenilir bir konum anlatmaya başlar.
