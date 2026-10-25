---
layout: post
title: "Robotik Algılamada LIDAR mı Kamera mı? Doğruluk ve Maliyet Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - lidar
  - kamera
  - algılama
  - bilgisayarlı görü
  - sensör füzyonu
toc: true
image: /img/robotik-algilamada-lidar-35.png
---

Bir robotun çevresini anlaması, yalnızca önündeki nesneleri “görmesinden” ibaret değildir. Robot; nesnenin uzaklığını, biçimini, hareketini ve mümkünse ne olduğunu belirlemelidir. Bu noktada iki popüler seçenek karşımıza çıkar: lazer darbeleriyle mesafe ölçen LIDAR ve görüntülerden anlam çıkaran kamera. Peki hangisi daha doğru, hangisi daha ekonomik?
``

## Algılama yöntemleri nasıl çalışır?

LIDAR, çevreye lazer darbeleri gönderir ve ışığın geri dönme süresini ölçerek uzaklığı hesaplar. Temel ilişki şöyledir:

$$d = c t / 2$$

Burada $d$ mesafe, $c$ ışık hızı ve $t$ darbenin gidiş-dönüş süresidir. İkiye bölmemizin nedeni, ölçülen sürenin ışığın hem nesneye gidişini hem de sensöre dönüşünü kapsamasıdır. Binlerce ölçüm birleştirildiğinde çevrenin üç boyutlu “nokta bulutu” oluşur.

Kamera ise sahneyi piksel matrisi olarak kaydeder. Derinlik doğrudan ölçülmez; stereo kamera, hareket analizi veya yapay sinir ağlarıyla tahmin edilir. Stereo sistemlerde yaklaşık derinlik bağıntısı şöyledir:

$$Z = fB / p$$

Burada $Z$ derinlik, $f$ odak uzaklığı, $B$ iki kamera arasındaki mesafe ve $p$ aynı noktanın görüntülerdeki konum farkıdır. Konum farkındaki küçük hatalar, özellikle uzaktaki nesnelerde büyük derinlik hatalarına dönüşebilir.

## Doğruluk karşılaştırması

| Özellik | LIDAR | Kamera |
|---|---|---|
| Mesafe ölçümü | Doğrudan ve yüksek doğrulukta | Tahmine veya stereo geometrisine bağlı |
| Renk ve doku | Çok sınırlı | Oldukça zengin |
| Gece performansı | Genellikle güçlü | Ek aydınlatma yoksa zayıflayabilir |
| Sis, yağmur, kar | Ölçümler bozulabilir | Görüş ciddi biçimde azalabilir |
| Nesne sınıflandırma | Tek başına sınırlı | Derin öğrenmeyle başarılı |
| 3B haritalama | Doğal olarak uygun | Ek hesaplama gerektirir |

LIDAR, SLAM ve engelden kaçınma gibi geometrinin kritik olduğu görevlerde avantajlıdır. Kamera ise trafik levhası okumak, insan tanımak veya nesnenin rengini ayırt etmek gibi anlamsal görevlerde öne çıkar. Kısacası LIDAR “Nerede?”, kamera ise “Ne?” sorusuna daha rahat cevap verir.

## Maliyet yalnızca sensör fiyatı değildir

Kameralar genellikle daha ucuz, küçük ve kolay erişilebilirdir. Ancak yüksek çözünürlüklü görüntülerin gerçek zamanlı işlenmesi için güçlü GPU, daha fazla bellek ve karmaşık yapay zekâ modelleri gerekebilir. Bu nedenle toplam maliyet şu şekilde düşünülmelidir:

$$M_{toplam} = M_{sensör} + M_{işlem} + M_{geliştirme} + M_{bakım}$$

LIDAR’ın satın alma fiyatı daha yüksek olabilir; buna karşılık hazır 3B ölçüm sağlaması bazı algoritmaları basitleştirir. Mekanik döner modeller bakım gerektirebilirken katı hâl LIDAR’lar daha dayanıklıdır. Kamera lenslerinin kirlenmesi, ışık değişimleri ve modelin yeniden eğitilmesi de görünmeyen maliyetlerdir.

## Basit bir seçim puanlaması

Aşağıdaki Python kodu, projedeki önceliklere göre iki sensörü kabaca puanlar:

```python
weights = {
    "distance_accuracy": 0.40,
    "semantic_detail": 0.25,
    "low_cost": 0.35,
}

scores = {
    "lidar":  {"distance_accuracy": 9, "semantic_detail": 3, "low_cost": 4},
    "camera": {"distance_accuracy": 6, "semantic_detail": 9, "low_cost": 9},
}

for sensor, criteria in scores.items():
    total = sum(criteria[key] * weights[key] for key in weights)
    print(sensor, round(total, 2))
```

Kod, her ölçütün önem katsayısını sensör puanıyla çarpar. Gerçek projede enerji tüketimi, görüş alanı ve hava koşulları gibi yeni ölçütler eklenebilir. Bu yaklaşım kesin karar vermez; ekip içindeki “Bence kamera daha havalı!” tartışmasını ölçülebilir hâle getirir.

## Sonuç: Rakip değil, takım arkadaşı

Düşük bütçeli iç mekân robotlarında kamera çoğu zaman yeterlidir. Hassas haritalama, otonom sürüş veya güvenlik kritik uygulamalarda LIDAR daha güvenilir geometrik veri sunar. En güçlü çözüm ise sensör füzyonudur: LIDAR’ın mesafe doğruluğu, kameranın renk ve anlam bilgisiyle birleştirilir. Bütçe izin veriyorsa doğru soru “Hangisini seçmeliyim?” değil, “Bu ikisini nasıl konuşturmalıyım?” olabilir.

![robotik-algilamada-lidar-35](/img/robotik-algilamada-lidar-35.svg)

