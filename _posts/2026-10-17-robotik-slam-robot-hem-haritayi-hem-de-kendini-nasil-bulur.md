---
layout: post
title: "Robotik SLAM: Robot Hem Haritayı Hem de Kendini Nasıl Bulur?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - slam
  - haritalama
  - lokalizasyon
  - sensör füzyonu
  - otonom robotlar
toc: true
image: /img/robotik-slam-robot-76.png
---

Bir robotu daha önce görmediği bir binaya bıraktığımızı düşünelim. Elinde kat planı yok, GPS içeride çalışmıyor ve robot başlangıçta yalnızca kendi sensörlerine güvenebiliyor. Buna rağmen duvarlara çarpmadan ilerlemesi, çevrenin haritasını oluşturması ve bu haritada nerede bulunduğunu anlaması gerekiyor. SLAM, yani *Simultaneous Localization and Mapping*, tam olarak bu tavuk-yumurta problemini çözer.
``

## SLAM problemi neden zordur?

Harita oluşturmak için robotun ölçümlerin nereden alındığını bilmesi gerekir. Konumunu bulmak içinse güvenilir bir haritaya ihtiyacı vardır. SLAM bu iki bilinmeyeni birlikte tahmin eder: robotun zamana bağlı pozu $x_t$ ve çevrenin haritası $m$.

Amaç, sensör ölçümleri $z_{1:t}$ ve kontrol girdileri $u_{1:t}$ verildiğinde şu olasılığı hesaplamaktır:

$$
p(x_t, m \mid z_{1:t}, u_{1:t})
$$

Buradaki **poz**, yalnızca konumu değil yönelimi de kapsar. İki boyutlu bir robot için genellikle $x_t = (x, y, \theta)$ biçimindedir. Tekerleklerin dönüşünden elde edilen odometri robotun hareketini tahmin eder; LiDAR, kamera veya sonar ise çevre hakkında gözlem üretir.

| Bilgi kaynağı | Avantajı | Temel problemi |
|---|---|---|
| Tekerlek odometrisi | Hızlı ve ucuzdur | Kayma nedeniyle hata birikir |
| LiDAR | Hassas mesafe ölçer | Maliyetli olabilir |
| Kamera | Zengin görsel bilgi sağlar | Işık değişimlerinden etkilenir |
| IMU | Hızlı hareket ölçümü sunar | Uzun vadede sürüklenir |

![robotik-slam-robot-76](/img/robotik-slam-robot-76.svg)


SLAM’in sihri, bu kusurlu kaynakları **sensör füzyonu** ile bir araya getirmesidir.

## Tahmin ve düzeltme döngüsü

Çoğu SLAM sistemi iki aşamalı bir döngü kullanır. **Tahmin aşamasında** hareket modeli uygulanır:

$$
x_t = f(x_{t-1}, u_t) + w_t
$$

Burada $w_t$ hareket belirsizliğidir. Robot bir metre ilerlediğini düşünse bile gerçekte 98 santimetre gitmiş olabilir. **Düzeltme aşamasında** sensör gözlemleri beklenen harita ölçümleriyle karşılaştırılır:

$$
z_t = h(x_t, m) + v_t
$$

$v_t$ sensör gürültüsünü temsil eder. Beklenen ve gerçek ölçüm arasındaki fark, konum ile haritanın düzeltilmesinde kullanılır.

## Başlıca SLAM yaklaşımları

| Yaklaşım | Temel fikir | Uygun senaryo |
|---|---|---|
| EKF-SLAM | Durumu Gauss dağılımıyla izler | Küçük ve düzenli ortamlar |
| FastSLAM | Parçacık filtresi kullanır | Çoklu konum olasılıkları |
| Graph SLAM | Pozları düğüm, ilişkileri kenar yapar | Büyük ölçekli haritalar |
| Visual SLAM | Kamera özelliklerini takip eder | Drone ve mobil cihazlar |

Modern sistemlerde Graph SLAM oldukça yaygındır. Robotun farklı zamanlardaki pozları bir grafik oluşturur. Odometri ve sensör eşleşmeleri bu pozlar arasına kısıt ekler. Optimizasyon, toplam hatayı küçülten pozları arar:

$$
x^* = \operatorname{argmin}_x \sum_i e_i(x)^T \Omega_i e_i(x)
$$

Burada $e_i$ ölçüm hatası, $\Omega_i$ ise ölçümün ne kadar güvenilir olduğunu belirten ağırlıktır.

## Basitleştirilmiş bir SLAM döngüsü

Aşağıdaki Python benzeri örnek, gerçek bir SLAM kütüphanesi değildir; tahmin, ölçüm eşleştirme ve düzeltme akışını gösterir:

```python
pose = Pose(x=0.0, y=0.0, angle=0.0)
world_map = Map()

for control, scan in sensor_stream:
    # Odometriyle robotun yeni pozunu tahmin eder.
    predicted_pose = motion_model(pose, control)

    # LiDAR taramasını mevcut haritayla eşleştirir.
    match = scan_match(scan, world_map, predicted_pose)

    # Eşleşme sonucuyla poz tahminini düzeltir.
    pose = correct_pose(predicted_pose, match)

    # Düzeltilmiş poz üzerinden haritayı günceller.
    world_map.integrate(scan, pose)
```

`scan_match` fonksiyonu yeni taramadaki şekilleri haritadaki duvar veya köşelerle eşleştirir. Bu sayede odometri hatası azaltılır.

## Döngü kapatma: Eski bir dostu tanımak

Robot daha önce ziyaret ettiği bir yere döndüğünde bunu fark ederse **loop closure** gerçekleşir. Örneğin uzun bir koridorda biriken hata, başlangıç noktası yeniden tanındığında tüm rota boyunca dağıtılarak düzeltilebilir. Yanlış döngü kapatma ise haritayı dramatik biçimde bozabileceğinden benzerlik kontrolü kritik önemdedir.

Kısacası SLAM, tek bir algoritmadan çok hareket modelleme, olasılıksal çıkarım, veri ilişkilendirme ve optimizasyon tekniklerinin birleşimidir. Robot haritayı çizerken kendini, kendini bulurken de haritayı sürekli iyileştirir; yani bilinmeyen ortamla adım adım tanışır.
