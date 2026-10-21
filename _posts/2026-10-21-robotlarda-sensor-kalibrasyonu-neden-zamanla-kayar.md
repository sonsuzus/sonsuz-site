---
layout: post
title: "Robotlarda Sensör Kalibrasyonu Neden Zamanla Kayar?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - sensör füzyonu
  - kalibrasyon
  - drift
  - python
  - otonom sistemler
toc: true
image: /img/robotlarda-sensor-kalibrasyonu-26.png
---

![robotlarda-sensor-kalibrasyonu-26](/img/robotlarda-sensor-kalibrasyonu-26.svg)


Bir robot fabrikadan kusursuz kalibre edilmiş biçimde çıksa bile bu durum sonsuza kadar sürmez. Kamera, LiDAR, IMU, enkoder ve GPS gibi sensörlerin ölçümleri; sıcaklık, titreşim, mekanik aşınma ve elektronik yaşlanma nedeniyle zamanla birbirinden uzaklaşır. Robot hâlâ veri topluyor gibi görünür, ancak artık dünyayı hafifçe “yamuk” algılıyordur. İşte bu yavaş bozulmaya kalibrasyon kayması, yani **drift** denir.

``

## Çoklu sensör kalibrasyonu nedir?

Çoklu sensörlü bir sistemde yalnızca her sensörün kendi doğruluğu değil, sensörlerin birbirleriyle olan geometrik ve zamansal ilişkileri de önemlidir. Örneğin kamera ile LiDAR arasındaki dönüşüm genellikle şu katı cisim dönüşümüyle gösterilir:

$$
\mathbf{p}_{kamera} = \mathbf{R}\mathbf{p}_{lidar} + \mathbf{t}
$$

Burada $\mathbf{R}$ dönme matrisini, $\mathbf{t}$ ise öteleme vektörünü temsil eder. Sensör yuvasının bir vida kadar oynaması bile bu dış parametreleri değiştirir. Benzer şekilde kameranın odak uzaklığı veya mercek bozulması gibi iç parametreler de sıcaklık ve darbe etkisiyle sapabilir.

Zamansal kalibrasyon da en az geometrik kalibrasyon kadar kritiktir. Kamera görüntüsü ile IMU ölçümü arasında $\Delta t$ gecikmesi varsa hızlı hareket sırasında aynı fiziksel an karşılaştırılmaz. Açısal hız $\omega$ olduğunda yaklaşık yönelim hatası şöyle büyür:

$$
\Delta \theta \approx \omega \Delta t
$$

Robot hızlandıkça küçücük bir saat farkının büyük konum hatasına dönüşmesinin nedeni budur.

## Drift neden oluşur?

| Drift kaynağı | Etkilenen bileşen | Olası belirti |
|---|---|---|
| Sıcaklık değişimi | IMU biası, kamera odağı | Konumun yavaşça sürüklenmesi |
| Titreşim ve darbe | Sensörün dış dönüşümü | Nokta bulutunun görüntüyle örtüşmemesi |
| Mekanik aşınma | Enkoder, mafsal geometrisi | Tekrarlanan hareketlerde farklı sonuç |
| Saat kayması | Sensör zaman damgaları | Hızlı dönüşlerde çift kenarlar |
| Elektronik yaşlanma | Kazanç ve ofset | Sistematik ölçüm sapması |
| Yazılım güncellemesi | Sürücü ve koordinat sistemi | Güncelleme sonrası ani uyumsuzluk |

Drift her zaman doğrusal ilerlemez. Robot soğukken farklı, çalışma sıcaklığına ulaştığında farklı davranabilir. Bu nedenle yalnızca “ayda bir kalibre et” yaklaşımı her sistem için yeterli değildir.

## Yeniden kalibrasyon zamanı nasıl anlaşılır?

Kalibrasyon sağlığı, sensörlerin ortak gözlemleri arasındaki **residual**, yani artık hata üzerinden izlenebilir. Ölçülen değer $z_i$, modelin tahmini $h_i(\mathbf{x})$ ise toplam hata:

$$
J(\mathbf{x}) = \sum_i \left\\vert z_i-h_i(\mathbf{x})\right\\vert _{\Sigma_i^{-1}}^2
$$

şeklinde tanımlanabilir. $J$ değerinin sürekli yükselmesi, sensör ilişkisinin bozulduğuna işaret eder. Ancak hareketli nesneler, yağmur veya kirli mercek de residual değerini artırabileceğinden tek ölçümle karar verilmemelidir.

Aşağıdaki Python örneği, hata serisinin hareketli ortalamasını izleyerek basit bir yeniden kalibrasyon uyarısı üretir:

```python
from collections import deque

class CalibrationMonitor:
    def __init__(self, window=30, threshold=1.5):
        self.errors = deque(maxlen=window)
        self.threshold = threshold

    def update(self, residual):
        self.errors.append(residual)
        if len(self.errors) < self.errors.maxlen:
            return False

        mean_error = sum(self.errors) / len(self.errors)
        return mean_error > self.threshold

monitor = CalibrationMonitor(window=30, threshold=1.5)

for error in [0.8] * 20 + [1.9] * 30:
    if monitor.update(error):
        print("Yeniden kalibrasyon öneriliyor!")
        break
```

Bu kod ani bir sıçrama yerine son 30 ölçümün ortalamasını kullanır. Gerçek sistemlerde sıcaklık, robot hızı ve titreşim seviyesi de karara eklenerek yanlış alarmlar azaltılabilir.

## Takvim mi, koşul bazlı bakım mı?

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Periyodik kalibrasyon | Planlaması kolaydır | Gereksiz bakım yapılabilir |
| Koşul bazlı kalibrasyon | Gerçek bozulmaya tepki verir | İzleme altyapısı gerektirir |
| Sürekli çevrim içi kalibrasyon | Drift hareket sırasında düzeltilir | Gözlemlenebilirlik ve hesaplama zordur |
| Hibrit yaklaşım | Güvenlik ile verimliliği dengeler | Tasarımı daha karmaşıktır |

Güvenlik kritik robotlarda en sağlam çözüm genellikle hibrittir: residual değerleri sürekli izlenir, eşik aşılırsa erken bakım yapılır ve buna rağmen belirli aralıklarla doğrulama kalibrasyonu uygulanır. Ayrıca kalibrasyon parametreleri sıcaklıkla birlikte kaydedilmeli, sensör montajları işaretlenmeli ve her bakım sonrası referans veri setiyle test edilmelidir.

Sonuç olarak kalibrasyon tek seferlik bir kurulum adımı değil, robotun yaşam döngüsü boyunca yönetilmesi gereken bir sağlık göstergesidir. Robotun dünyayı doğru görmesini istiyorsak yalnızca sensörlerin çalışıp çalışmadığını değil, hâlâ aynı dünyaya bakıp bakmadıklarını da sorgulamalıyız.
