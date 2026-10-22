---
layout: post
title: "Robotlarda Kalman Filtresi: Gürültülü Sensörlerden Güvenilir Durum Tahmini"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - kalman-filtresi
  - sensör-füzyonu
  - durum-tahmini
  - python
  - kontrol-sistemleri
toc: true
image: /img/robotlarda-kalman-filtresi-50.png
---

![robotlarda-kalman-filtresi-50](/img/robotlarda-kalman-filtresi-50.svg)


Bir robotun sensörleri dünyayı kusursuz biçimde göremez. Tekerlek enkoderleri kayabilir, GPS ölçümleri sıçrayabilir ve ivmeölçer verileri titreşimden etkilenebilir. Kalman filtresi, gürültülü ölçümleri robotun hareket modeliyle birleştirerek konum, hız veya yönelim gibi doğrudan güvenemediğimiz durumları daha isabetli tahmin eder. Kısacası robota, “Sensöre inan ama her söylediğine de kanma” yaklaşımını kazandırır.
``

## Durum tahmini neden gereklidir?

Bir robotun gerçek durumunu $x_k$ ile gösterelim. Bu durum yalnızca konumdan oluşabileceği gibi konum ve hızı birlikte de içerebilir:

$$x_k = [p_k, v_k]^T$$

Robotun hareketi doğrusal bir modelle yaklaşık olarak şöyle ifade edilir:

$$x_k = A x_{k-1} + B u_k + w_k$$

Burada $A$ durum geçiş modelini, $u_k$ kontrol girdisini, $B$ kontrolün duruma etkisini ve $w_k$ süreç gürültüsünü temsil eder. Sensör ölçümü ise şöyledir:

$$z_k = H x_k + v_k$$

$H$, durumun hangi bölümünün ölçüldüğünü; $v_k$ ise sensör gürültüsünü belirtir. Kalman filtresi genellikle $w_k$ ve $v_k$ değerlerinin sıfır ortalamalı Gauss dağılımına sahip olduğunu varsayar.

| Kavram | Sembol | Robotik örneği |
|---|---:|---|
| Durum | $x$ | Konum ve hız |
| Ölçüm | $z$ | GPS veya enkoder verisi |
| Süreç kovaryansı | $Q$ | Hareket modelindeki belirsizlik |
| Ölçüm kovaryansı | $R$ | Sensörün gürültü seviyesi |
| Tahmin kovaryansı | $P$ | Durum tahminine duyulan güvensizlik |

## İki aşamalı çalışma mantığı

Kalman filtresi her zaman adımında **tahmin** ve **düzeltme** işlemlerini gerçekleştirir.

Tahmin aşamasında robotun önceki durumundan yeni durum hesaplanır:

$$\hat{x}_k^- = A\hat{x}_{k-1} + Bu_k$$

$$P_k^- = AP_{k-1}A^T + Q$$

Üstteki eksi işareti, ölçüm henüz kullanılmadan elde edilen ön tahmini gösterir. $Q$ büyüdükçe filtre hareket modeline daha az güvenir.

Düzeltme aşamasında sensör verisi devreye girer. Önce Kalman kazancı hesaplanır:

$$K_k = P_k^-H^T(HP_k^-H^T + R)^{-1}$$

Ardından durum ve belirsizlik güncellenir:

$$\hat{x}_k = \hat{x}_k^- + K_k(z_k-H\hat{x}_k^-)$$

$$P_k = (I-K_kH)P_k^-$$

Kalman kazancı model ile sensör arasındaki hakemdir. $R$ büyükse sensör gürültülü kabul edilir ve modele daha çok güvenilir. $P$ büyükse mevcut tahmin şüpheli görülür ve yeni ölçüm daha etkili olur.

| Durum | Filtrenin eğilimi | Olası sonuç |
|---|---|---|
| $R$ çok küçük | Sensöre aşırı güvenme | Gürültülü çıktı |
| $R$ çok büyük | Modele aşırı güvenme | Gerçek değişimleri kaçırma |
| $Q$ çok küçük | Hareketi fazla düzgün varsayma | Manevralara geç tepki |
| $Q$ dengeli | Model ve ölçümü uzlaştırma | Kararlı tahmin |

## Basit bir Python uygulaması

Aşağıdaki örnek, tek boyutta sabit hızlı hareket eden bir robotun konum ve hızını tahmin eder:

```python
import numpy as np

dt = 0.1
A = np.array([[1, dt],
              [0, 1]])
H = np.array([[1, 0]])
Q = np.diag([0.01, 0.05])
R = np.array([[0.8]])

x = np.array([[0.0], [0.0]])  # konum, hız
P = np.eye(2)

def kalman_adimi(olcum):
    global x, P

    # Tahmin: robotun hareket modelini uygula
    x = A @ x
    P = A @ P @ A.T + Q

    # Düzeltme: ölçüm ile tahmin arasındaki farkı kullan
    yenilik = np.array([[olcum]]) - H @ x
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)

    x = x + K @ yenilik
    P = (np.eye(2) - K @ H) @ P
    return x.flatten()
```

Buradaki `yenilik`, sensörün söylediği konum ile model tahmini arasındaki farktır. Filtre bu farkı doğrudan eklemek yerine Kalman kazancıyla ölçeklendirir. Böylece tek bir hatalı ölçüm robotu aniden başka bir konuma “ışınlamaz”.

## Doğru ayar, iyi tahmin

Kalman filtresinin başarısı büyük ölçüde $Q$ ve $R$ matrislerinin gerçekçi seçilmesine bağlıdır. $R$, sabit duran sensörden toplanan örneklerin varyansıyla yaklaşık belirlenebilir. $Q$ ise zemindeki kayma, beklenmeyen ivmelenme ve modellenmemiş dinamikler düşünülerek ayarlanır. Doğrusal olmayan robot modellerinde Genişletilmiş Kalman Filtresi veya Unscented Kalman Filtresi tercih edilebilir. Temel fikir değişmez: model geleceği tahmin eder, sensör tahmini sorgular ve belirsizlik ikisi arasında akıllı bir denge kurar.
