---
layout: post
title: "Kamera-Robot Kalibrasyon Hataları El-Göz Koordinasyonunu Nasıl Bozar?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - kalibrasyon
  - bilgisayarlı görü
  - el-göz koordinasyonu
  - python
  - otomasyon
toc: true
image: /img/kamera-robot-kalibrasyon-39.png
---

Bir robotun kamerayla gördüğü parçayı doğru noktadan yakalaması, iki farklı dünyanın aynı koordinat dilini konuşmasına bağlıdır. Kamera-robot kalibrasyonundaki birkaç milimetrelik kayma veya küçük bir açı hatası, robot kolunun hedefi ıskalamasına, parçaya eğri yaklaşmasına, hatta pahalı bir çarpışmaya yol açabilir. Kısacası kamera doğru görse ve robot kusursuz hareket etse bile aralarındaki tercüman hatalıysa el-göz koordinasyonu bozulur.
``

## El-göz kalibrasyonu neyi çözer?

El-göz kalibrasyonunun amacı kamera koordinat sistemi ile robotun uç efektörü veya tabanı arasındaki dönüşümü bulmaktır. Kamera robotun bileğine takılıysa **eye-in-hand**, çalışma alanını dışarıdan izliyorsa **eye-to-hand** düzeni kullanılır.

Bir rijit dönüşüm, dönme matrisi $R$ ve öteleme vektörü $t$ ile ifade edilir:

$$
T = \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix}
$$

Klasik hand-eye problemi çoğunlukla şu denklem üzerinden çözülür:

$$
A_i X = X B_i
$$

Burada $A_i$ robotun iki poz arasındaki hareketini, $B_i$ kameranın aynı pozlar arasındaki hareketini, $X$ ise aranan kamera-robot dönüşümünü temsil eder. Ölçümler gürültülü olduğundan eşitlik pratikte tam sağlanmaz; algoritma en uygun $X$ dönüşümünü tahmin eder.

| Hata türü | Görülen belirti | Muhtemel kaynak |
|---|---|---|
| Öteleme hatası | Tüm hedeflerde benzer yönlü kaçırma | Yanlış TCP veya ölçüm |
| Dönme hatası | Uzak hedeflerde büyüyen sapma | Yetersiz poz çeşitliliği |
| Kamera iç kalibrasyon hatası | Görüntü kenarlarında bozulma | Lens distorsiyonu |
| Zamanlama hatası | Hareket sırasında değişken sonuç | Kamera-robot senkronizasyonu |

## Küçük açı, büyük sorun

Dönüş hataları özellikle sinsidir. Yaklaşık $theta$ radyanlık açısal hata, kameradan $d$ uzaklıktaki bir hedefte şu büyüklükte konum sapması oluşturabilir:

$$
e_p \approx d \cdot theta
$$

Örneğin $theta = 0.5° \approx 0.0087$ radyan ve $d = 1$ metre ise sapma yaklaşık $8.7$ milimetredir. Hassas montaj yapan bir robot için bu değer oldukça büyüktür. Üstelik TCP yanlış tanımlanmışsa hata, robot bileğini döndürdükçe yön değiştiren dairesel bir davranış gösterebilir.

Aşağıdaki Python kodu, küçük açı yaklaşımıyla uzaklığa bağlı yanal hatayı hesaplar:

```python
import math

def lateral_error(distance_m, angle_deg):
    # Dereceyi radyana çevirip yaklaşık yanal sapmayı bulur.
    angle_rad = math.radians(angle_deg)
    return distance_m * angle_rad

for distance in [0.25, 0.5, 1.0]:
    error_m = lateral_error(distance, 0.5)
    print(f"{distance:.2f} m -> {error_m * 1000:.2f} mm")
```

Bu basit hesap, kalibrasyon raporunda küçük görünen açısal artıkların neden çalışma alanının uzak bölgelerinde ciddi sonuçlar doğurduğunu gösterir.

## Kalibrasyon neden kötü çıkar?

En yaygın nedenlerden biri, örnek pozların birbirine fazla benzemesidir. Robot yalnızca doğrusal hareket ettirilirse sistem bazı dönüş bileşenlerini yeterince gözlemleyemez. Farklı eksenlerde dönüşler, çeşitli mesafeler ve çalışma hacmini kapsayan pozlar kullanılmalıdır. Bulanık görüntü, hatalı kalibrasyon deseni ölçüsü, gevşek kamera bağlantısı ve otomatik odak değişimi de sonucu bozar.

Yalnızca düşük yeniden izdüşüm hatasına güvenmek de tehlikelidir. Kamera iç kalibrasyonu başarılı görünürken kamera-robot dönüşümü yanlış olabilir. Bu nedenle doğrulama, eğitimde kullanılmamış pozlarla yapılmalıdır.

## Sağlam doğrulama stratejisi

Robotu bilinen kontrol noktalarına yönlendirin ve konum hatasını her eksen için ölçün. Ardından farklı bilek açılarını, yakın-uzak hedefleri ve görüntü merkezinden kenarlara doğru noktaları test edin. Hata mesafeyle büyüyorsa dönme; yaklaşık sabit kalıyorsa öteleme problemi düşünülmelidir.

Son olarak medyan hata kadar maksimum hatayı da raporlayın. Ortalama değer güzel görünürken tek bir uç poz üretim hattını durdurabilir. İyi el-göz koordinasyonu, yalnızca bir kalibrasyon matrisi hesaplamak değil; mekanik sağlamlık, zaman senkronizasyonu, çeşitli örnekleme ve bağımsız doğrulamayı birlikte yönetmektir.

![kamera-robot-kalibrasyon-39](/img/kamera-robot-kalibrasyon-39.svg)

