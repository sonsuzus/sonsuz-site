---
layout: post
title: "Fırtınada Bile Gören Robotlar: Otonom Araçlarda Sensör Füzyonu"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - otonom araçlar
  - sensör füzyonu
  - lidar
  - radar
  - bilgisayarlı görü
  - yapay zeka
toc: true
image: /img/firtinada-bile-goren-83.png
---

Güneşli bir günde yolu algılamak otonom araçlar için görece kolaydır. Ancak sis çöktüğünde, yağmur kamera görüntüsünü bozduğunda veya kar taneleri LiDAR ölçümlerinde hayalet noktalar oluşturduğunda işler değişir. Sensör füzyonu, farklı sensörlerin güçlü yanlarını birleştirerek aracın tek bir ölçüme körü körüne güvenmesini önler. Kısacası ekip çalışması yapar: Kamera renkleri söyler, radar mesafeyi ölçer, LiDAR çevrenin üç boyutlu haritasını çıkarır.


![firtinada-bile-goren-83](/img/firtinada-bile-goren-83.svg)

``

## Tek Bir Sensör Neden Yetmez?

Her sensör çevreyi farklı bir fiziksel ilkeye göre gözlemler. Kameralar görünür ışığı, radar elektromanyetik dalgaların yansımasını, LiDAR ise lazer darbelerinin dönüş süresini kullanır. Bu çeşitlilik aynı zamanda hata çeşitliliği demektir. Kamera sisi yoğun bir duvar gibi görebilirken radar sisin içinden çalışmayı sürdürebilir. Buna karşılık radar, nesnenin bisiklet mi yoksa trafik levhası mı olduğunu kamera kadar başarılı sınıflandıramaz.

| Sensör | Güçlü yönü | Kötü havadaki sorunu | Füzyondaki rolü |
|---|---|---|---|
| Kamera | Renk, şerit ve nesne sınıfı | Sis, karanlık ve su damlaları | Anlamsal bilgi sağlar |
| LiDAR | Hassas 3B geometri | Yağmur ve karda sahte yansımalar | Şekil ve konum üretir |
| Radar | Hız ve mesafe ölçümü | Düşük açısal çözünürlük | Zorlu havada kararlı ölçüm sağlar |
| Ultrasonik | Yakın mesafede ekonomiktir | Rüzgâr ve yüzey yapısından etkilenir | Park ve düşük hız desteği verir |
| GNSS/IMU | Araç konumu ve hareketi | Tünel, yansıma ve sürüklenme | Küresel ve göreli hareketi izler |

## Güven, Ağırlık ve Olasılık

Füzyonun temel fikri, bütün sensörlere eşit oy hakkı vermek değildir. Sistem, mevcut koşullara göre her ölçümün güvenilirliğini değerlendirir. Bir sensörün ölçümü $z_i$, güven ağırlığı $w_i$ ise basit bir birleşik tahmin şöyle yazılabilir:

$$x = (w_1z_1 + w_2z_2 + ... + w_nz_n) / (w_1 + w_2 + ... + w_n)$$

Yoğun siste kameranın $w$ değeri azaltılırken radarın ağırlığı artırılabilir. Daha gelişmiş sistemlerde Kalman filtresi, genişletilmiş Kalman filtresi, parçacık filtresi veya Bayesçi çıkarım kullanılır. Bayes yaklaşımı, yeni bir ölçüm geldiğinde önceki inancı günceller:

$$P(x\vert z) = P(z\vert x)P(x) / P(z)$$

Burada $P(x)$ önceki tahmini, $P(z\vert x)$ ölçümün bu tahmin altında görülme olasılığını, $P(x\vert z)$ ise güncellenmiş sonucu temsil eder. Böylece araç, “Radar önümde bir şey olduğunu söylüyor ama kamera emin değil” durumunu matematiksel olarak çözebilir.

## Basit Bir Uyarlanabilir Füzyon Örneği

Aşağıdaki Python kodu, hava durumuna göre kamera ve radar ölçümlerinin ağırlıklarını değiştirir. Gerçek araçlarda belirsizlik kovaryans matrisleri ve zaman senkronizasyonu kullanılır; bu örnek temel mantığı görünür kılar.

```python
def fuse_distance(camera, radar, weather):
    # Açık havada kamera daha güvenilirken siste radar öne çıkar.
    weights = {
        "clear": (0.6, 0.4),
        "rain":  (0.3, 0.7),
        "fog":   (0.15, 0.85)
    }

    camera_w, radar_w = weights.get(weather, (0.5, 0.5))
    return camera * camera_w + radar * radar_w

result = fuse_distance(camera=24.0, radar=21.5, weather="fog")
print(f"Tahmini mesafe: {result:.2f} metre")
```

Burada sisli havada radar ölçümü sonuca daha fazla yön verir. Fakat yalnızca hava etiketi kullanmak yeterli değildir. Kamera kontrastı, LiDAR dönüş yoğunluğu, radar sinyal-gürültü oranı ve sensör sıcaklığı gibi anlık kalite göstergeleri de ağırlıkları dinamik biçimde değiştirmelidir.

## Füzyonun Gizli Kahramanları

Başarılı bir sistem için sensörlerin kalibrasyonu ve zaman eşlemesi kritiktir. Milisaniyelik gecikme, hızlı hareket eden bir aracın farklı konumlarda algılanmasına yol açabilir. Ayrıca sensörler ortak koordinat sistemine dönüştürülmelidir. Aksi hâlde radarın “ön sağ” dediği nesne, kamera görüntüsünde yanlış piksele bağlanır.

Sonuç olarak sensör füzyonu kötü havayı ortadan kaldırmaz; belirsizliği yönetilebilir hâle getirir. Güvenilir otonomi, en parlak sensöre sahip olmak değil, hangi sensöre ne zaman güvenileceğini bilmektir. Robotik aracın süper gücü kusursuz görmek değil, şüphe etmeyi matematikle öğrenmektir.
