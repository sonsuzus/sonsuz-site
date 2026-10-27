---
layout: post
title: "Akıllı Sulama Sistemlerinde Optimizasyon: Her Damlayı Algoritmayla Yönetmek"
math: true
categories: 
  - Proje
tags: 
  - akıllı sulama
  - optimizasyon
  - nesnelerin interneti
  - python
  - tarım teknolojileri
  - sensörler
toc: true
image: /img/akilli-sulama-sistemlerinde-76.png
---

Geleneksel sulamada karar çoğu zaman takvime göre verilir: “Salı günü tarlayı sula.” Akıllı sulama sistemi ise daha meraklıdır; toprağın nemini, bitkinin gelişim dönemini, hava tahminini ve su deposunun durumunu sorgular. Böylece yalnızca gerekli bölgeye, gerekli zamanda ve gerekli miktarda su gönderir. Amaç musluğu robotlaştırmak değil, sınırlı suyu ölçülebilir bir optimizasyon problemi olarak yönetmektir.

``

## Bitkinin su ihtiyacı nasıl hesaplanır?

Sistemin temel girdilerinden biri **referans evapotranspirasyon** değeridir. Evapotranspirasyon, topraktan buharlaşan ve bitkinin yapraklarından atmosfere aktarılan toplam suyu ifade eder. Belirli bir bitkinin yaklaşık ihtiyacı şöyle bulunabilir:

$$ET_c = K_c \times ET_0$$

Burada $ET_0$ hava koşullarına bağlı referans evapotranspirasyon, $K_c$ ise bitki katsayısıdır. Örneğin domatesin gelişim dönemindeki katsayısı, yeni ekilmiş bir bitkininkinden farklıdır.

Yağış ve mevcut toprak nemi de hesaba katıldığında net sulama ihtiyacı basitleştirilmiş biçimde şöyle modellenebilir:

$$D = max(0, ET_c - P_e - M)$$

$D$ verilecek suyu, $P_e$ etkili yağışı, $M$ ise kök bölgesinde kullanılabilir nem katkısını gösterir. `max` işlemi, yağış ihtiyacı zaten karşıladıysa negatif miktarda sulama yapılmasını engeller.

## Takvim tabanlı ve akıllı sulama karşılaştırması

| Özellik | Takvim tabanlı sulama | Akıllı sulama |
|---|---|---|
| Karar kaynağı | Sabit gün ve saat | Sensörler ve tahminler |
| Su miktarı | Genellikle sabit | Bitki ihtiyacına göre değişken |
| Yağmur tepkisi | Manuel müdahale gerekir | Sulama otomatik ertelenebilir |
| Bölgesel kontrol | Sınırlı | Her vana ayrı yönetilebilir |
| Risk | Fazla veya yetersiz sulama | Sensör hatasına bağımlılık |

Akıllı yaklaşım açıkça avantajlı görünse de sensör kalibrasyonu ihmal edilirse sistem son derece kararlı biçimde yanlış karar verebilir. Başka bir deyişle, kötü veri kullanan harika bir algoritma hâlâ kötü bir sulamacıdır.

## Optimizasyon problemi

Bir tarlada birden fazla sulama bölgesi bulunduğunu düşünelim. Her bölgenin ihtiyacı farklıdır, fakat pompanın debisi ve depodaki su sınırlıdır. Hedef fonksiyonu, ihtiyaç ile verilen su arasındaki farkı küçültebilir:

$$minimize \sum_i w_i(D_i - x_i)^2$$

Burada $D_i$ bölgenin ihtiyacı, $x_i$ tahsis edilen su ve $w_i$ öncelik katsayısıdır. Yeni dikilmiş veya su stresine hassas bitkilere daha yüksek ağırlık verilebilir. Model ayrıca şu kısıtları taşıyabilir:

- Toplam dağıtılan su depo kapasitesini aşmamalıdır.
- Bir vananın çalışma süresi teknik sınırlar içinde kalmalıdır.
- Yağmur olasılığı yüksekse tahsis azaltılmalıdır.
- Pompa aynı anda yalnızca belirli sayıda bölgeyi beslemelidir.

## Basit bir Python karar mekanizması

Aşağıdaki fonksiyon, nem eşiklerini ve beklenen yağışı kullanarak sulama süresi üretir:

```python
def sulama_suresi(nem, hedef_nem, alan_m2,
                   yagis_mm, debi_litre_dk):
    nem_acigi = max(0, hedef_nem - nem)

    # Beklenen yağmur arttıkça ihtiyaç azaltılır.
    gerekli_mm = max(0, nem_acigi * 0.5 - yagis_mm)

    # 1 mm yağış, 1 m² alanda yaklaşık 1 litre sudur.
    gerekli_litre = gerekli_mm * alan_m2
    dakika = gerekli_litre / debi_litre_dk

    return round(dakika, 1)

sure = sulama_suresi(
    nem=24,
    hedef_nem=35,
    alan_m2=120,
    yagis_mm=2,
    debi_litre_dk=18
)
print(f'Sulama süresi: {sure} dakika')
```

Bu örnek üretim sistemi için tek başına yeterli değildir; ancak sensör verisinin fiziksel su miktarına ve vana süresine nasıl dönüştürüldüğünü gösterir. Gerçek projede sensör okumaları filtrelenmeli, anormal değerler elenmeli ve vana komutları kayıt altına alınmalıdır.

## Daha akıllı bir mimari

Uygulamada nem sensörleri MQTT gibi bir protokolle merkezi sunucuya veri gönderebilir. Sunucu hava tahminini alır, optimizasyonu çalıştırır ve vanalara komut iletir. Elektrik veya internet kesintisine karşı yerel denetleyicide güvenli bir varsayılan program bulunması önemlidir.

Sonuç olarak akıllı sulama; sensör, tarım bilgisi ve optimizasyonun ortak çalışmasıdır. Başarı yalnızca su tasarrufuyla değil, bitki sağlığı, enerji tüketimi ve ürün verimi birlikte izlenerek ölçülmelidir. En iyi sistem en çok sulayan değil, doğru damlayı doğru köke ulaştırandır.

![akilli-sulama-sistemlerinde-76](/img/akilli-sulama-sistemlerinde-76.svg)

