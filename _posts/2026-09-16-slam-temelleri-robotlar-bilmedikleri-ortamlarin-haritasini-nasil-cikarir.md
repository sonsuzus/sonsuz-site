---
layout: post
title: "SLAM Temelleri: Robotlar Bilmedikleri Ortamların Haritasını Nasıl Çıkarır?"
math: true
categories: 
  - Bilgi
tags: 
  - slam
  - robotik
  - haritalama
  - lokalizasyon
  - sensör füzyonu
  - otonom sistemler
toc: true
---

Bir robotu daha önce hiç görmediği bir odaya bıraktığımızı düşünelim. Elinde mimari plan, GPS veya duvarların nerede olduğunu söyleyen sihirli bir pusula yok. Buna rağmen hem nerede bulunduğunu anlaması hem de çevresinin haritasını çıkarması gerekiyor. İşte **SLAM** (Simultaneous Localization and Mapping), yani *Eş Zamanlı Konumlandırma ve Haritalama*, bu tavuk-yumurta problemini çözmeye çalışır.

``

## SLAM neden zor bir problem?

Harita oluşturmak için robotun konumunu bilmesi gerekir. Konumunu doğru hesaplamak içinse çevresindeki noktaların haritadaki yerlerini bilmelidir. SLAM, bu iki bilinmeyeni sensör ölçümlerini zaman içinde birleştirerek birlikte tahmin eder.

Robotun $t$ anındaki durumu kabaca şöyle gösterilebilir:

$$
\mathbf{x}_t = [x_t, y_t, \theta_t]^T
$$

Burada $x_t$ ve $y_t$ robotun düzlemdeki konumunu, $\theta_t$ ise baktığı yönü belirtir. Amaç; kontrol girdileri $u_{1:t}$ ve sensör ölçümleri $z_{1:t}$ verildiğinde robotun rotasıyla haritayı birlikte bulmaktır:

$$
p(\mathbf{x}_{1:t}, m \mid z_{1:t}, u_{1:t})
$$

Buradaki $m$, bilinmeyen ortam haritasıdır. Denklem ürkütücü görünse de fikir basittir: Robot hareket eder, çevresini ölçer, tahminini düzeltir ve bunu sürekli tekrarlar.

## Robot çevresini nasıl algılar?

SLAM sistemlerinde tek bir kusursuz sensör yoktur. Her sensör farklı bir ipucu sağlar ve farklı biçimde hata yapar.

| Sensör | Sağladığı bilgi | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| LiDAR | Nesnelere uzaklık | Hassas geometri | Maliyet ve yansıma sorunları |
| Kamera | Görsel özellikler | Zengin çevre bilgisi | Işık değişimlerinden etkilenir |
| IMU | İvme ve dönüş | Çok hızlı ölçüm | Hatası zamanla birikir |
| Teker enkoderi | Kat edilen mesafe | Basit ve ucuz | Kaygan zeminde şaşırır |
| GPS | Küresel konum | Açık alanda kullanışlı | Kapalı alanda çalışmaz |

Bu verilerin birleştirilmesine **sensör füzyonu** denir. Örneğin enkoder robotun bir metre ilerlediğini söylerken LiDAR, duvarın beklenenden yakın olduğunu gösterebilir. Algoritma her ölçümün belirsizliğini hesaba katarak daha güvenilir bir sonuç üretir.

## Tahmin, ölçüm ve düzeltme döngüsü

SLAM’in kalbinde sürekli çalışan üç aşama bulunur:

1. **Hareket tahmini:** Robotun motor komutlarına göre yeni konumu hesaplanır.
2. **Ölçüm eşleştirme:** Yeni sensör verileri, daha önce görülen özelliklerle karşılaştırılır.
3. **Düzeltme:** Tahmin ile ölçüm arasındaki fark azaltılır.

Basitleştirilmiş bir konum güncellemesi Python ile şöyle modellenebilir:

```python
import numpy as np

def hareket_modeli(durum, mesafe, donus):
    # Önce robotun yönünü güncelle
    x, y, aci = durum
    aci += donus

    # Yeni yöne göre düzlemde ilerle
    x += mesafe * np.cos(aci)
    y += mesafe * np.sin(aci)

    return np.array([x, y, aci])

durum = np.array([0.0, 0.0, 0.0])
durum = hareket_modeli(durum, 1.0, np.pi / 4)
```

Bu kod yalnızca hareket tahmini yapar. Gerçek bir SLAM sistemi, sensör ölçümlerini kullanarak bu sonucu düzeltir; çünkü tekerlek kayması veya motor hataları robotu matematiksel rotasından uzaklaştırabilir.

## Döngü kapatma: “Ben burayı görmüştüm!”

Robot uzun süre ilerledikten sonra başlangıç noktasına dönebilir. Sistem daha önce gördüğü bir koridoru veya köşeyi tanırsa buna **döngü kapatma** denir. Bu keşif, biriken konum hatalarının tüm rota boyunca dağıtılarak düzeltilmesini sağlar. Aksi hâlde kare biçimindeki bir oda, haritada yamuk bir çokgene dönüşebilir.

SLAM çözümleri genellikle EKF-SLAM, parçacık filtreleri, grafik tabanlı SLAM veya görsel SLAM gibi yaklaşımlara ayrılır. Günümüzde robot süpürgelerden otonom otomobillere, dronlardan artırılmış gerçeklik uygulamalarına kadar pek çok sistem bu fikirlerden yararlanır. Kısacası robot, kusursuz biçimde “bilmez”; hareket eder, ölçer, şüphe duyar ve tahminini tekrar tekrar iyileştirir.
