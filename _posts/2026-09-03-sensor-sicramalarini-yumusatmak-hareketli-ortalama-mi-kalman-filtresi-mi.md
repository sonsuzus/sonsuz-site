---
layout: post
title: "Sensör Sıçramalarını Yumuşatmak: Hareketli Ortalama mı, Kalman Filtresi mi?"
math: true
categories: 
  - Bilgi
tags: 
  - zaman serileri
  - kalman filtresi
  - sensör verisi
toc: true
---

Bir sıcaklık sensörünün 22,1 °C gösterirken aniden 47 °C’ye çıkıp sonraki ölçümde normale döndüğünü düşünün. Ortam bir saniyede tropik adaya dönüşmediğine göre karşımızda büyük olasılıkla elektriksel parazit, haberleşme hatası veya ölçüm gürültüsü vardır. Bu sıçramaları azaltmanın iki popüler yolu hareketli ortalama ve Kalman filtresidir.
``
## Gürültü ve gerçek sinyal ayrımı

Bir sensör ölçümünü basitçe şöyle modelleyebiliriz:

$$z_t = x_t + v_t$$

Burada $z_t$ ölçülen değer, $x_t$ gerçek fakat doğrudan göremediğimiz durum, $v_t$ ise ölçüm gürültüsüdür. Filtrenin görevi, gözlemlerden yararlanarak $x_t$ için daha güvenilir bir tahmin üretmektir.

Ancak önemli bir ayrıntı vardır: Gürültü her zaman anlık sıçrama değildir. Küçük ve rastgele dalgalanmalar, sabit sapmalar ve uç değerler farklı davranır. Hareketli ortalama özellikle kısa süreli dalgalanmaları yumuşatırken Kalman filtresi sistemin zaman içindeki hareketini de modele katar.

## Hareketli ortalama: Basit ve etkili

$N$ noktalı basit hareketli ortalama şu şekilde hesaplanır:

$$y_t = \frac{1}{N}\sum_{i=0}^{N-1} z_{t-i}$$

Örneğin pencere boyutu 5 ise son beş ölçüm toplanır ve beşe bölünür. Tek bir sıçramanın etkisi böylece komşu örneklere dağıtılır.

```python
from collections import deque

class MovingAverage:
    def __init__(self, window_size=5):
        self.values = deque(maxlen=window_size)

    def update(self, measurement):
        self.values.append(measurement)
        return sum(self.values) / len(self.values)

sensor_data = [22.0, 22.2, 21.9, 47.0, 22.1, 22.0]
filter_ma = MovingAverage(window_size=3)
filtered = [filter_ma.update(value) for value in sensor_data]
print(filtered)
```

Bu kod sabit miktarda geçmiş veri saklar ve her yeni ölçümde ortalamayı günceller. Pencere büyüdükçe çıktı daha pürüzsüz olur; fakat gerçek değişikliklere verilen tepki gecikir. Üstelik çok büyük bir uç değer, pencere boyunca sonucu etkilemeye devam eder.

## Kalman filtresi: Tahmin ile ölçümün uzlaşması

Kalman filtresi yalnızca geçmiş değerleri ortalamaz; sistemin bir sonraki durumunu tahmin eder. Basit, tek boyutlu ve sabit durum modelinde önce belirsizlik güncellenir:

$$P_t^- = P_{t-1} + Q$$

Ardından Kalman kazancı hesaplanır:

$$K_t = \frac{P_t^-}{P_t^- + R}$$

Tahmin ise ölçüme doğru kontrollü biçimde çekilir:

$$\hat{x}_t = \hat{x}_t^- + K_t(z_t - \hat{x}_t^-)$$

Burada $Q$ sistemin ne kadar değişebileceğini, $R$ sensöre ne kadar güvenildiğini ve $P$ tahmin belirsizliğini temsil eder.

```python
class Kalman1D:
    def __init__(self, estimate=22.0, uncertainty=1.0, q=0.01, r=4.0):
        self.x = estimate
        self.p = uncertainty
        self.q = q
        self.r = r

    def update(self, measurement):
        self.p += self.q              # Tahmin belirsizliği
        gain = self.p / (self.p + self.r)
        self.x += gain * (measurement - self.x)
        self.p *= (1 - gain)
        return self.x
```

$R$ büyütülürse filtre sensöre daha az güvenir ve sıçramaları daha güçlü bastırır. $Q$ büyütülürse gerçek değişimlerin hızlı olabileceği kabul edilir; filtre ölçümlere daha çabuk yaklaşır.

## Hangi yöntemi seçmeli?

| Özellik | Hareketli Ortalama | Kalman Filtresi |
|---|---|---|
| Kurulum | Çok kolay | Model ve parametre ayarı gerekir |
| Hesaplama maliyeti | Düşük | Düşük-orta |
| Gecikme | Pencere büyüdükçe artar | Doğru ayarla daha az olabilir |
| Sistem bilgisi | Kullanmaz | Durum modelinden yararlanır |
| Uyarlanabilirlik | Sınırlı | Belirsizliğe göre değişir |
| Hata ayıklama | Kolay | Daha dikkatli analiz ister |

Basit gösterge panelleri ve düşük güçlü cihazlar için hareketli ortalama iyi bir başlangıçtır. Robot konumu, araç hızı veya birden fazla sensörün birleştirilmesi gibi dinamik uygulamalarda Kalman filtresi daha güçlüdür. Bununla birlikte çok sert uç değerlerde iki yöntem de tek başına kusursuz değildir. Önce fiziksel sınır kontrolü veya medyan filtresi uygulayıp ardından Kalman filtresi kullanmak genellikle daha sağlam bir mimari oluşturur. Kısacası en karmaşık filtre değil, sensörün fiziğine ve uygulamanın gecikme toleransına uyan filtre kazanır.
