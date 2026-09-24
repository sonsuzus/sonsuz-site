---
layout: post
title: "Sensör Kalibrasyonu: Kusurlu Ölçüm Cihazından Güvenilir Veri Üretmek"
math: true
categories: 
  - Bilgi
tags: 
  - sensör
  - kalibrasyon
  - python
  - veri analizi
  - ölçüm
  - istatistik
toc: true
image: /img/sensor-kalibrasyonu-kusurlu-78.png
---

Bir sıcaklık sensörünü buzlu suya daldırdığınızda 0 °C yerine 2,4 °C göstermesi onun işe yaramaz olduğu anlamına gelmez. Sensör yalnızca biraz “dürüstlük eğitimine” ihtiyaç duyuyor olabilir! Kalibrasyon, cihazın ürettiği ham değerlerle güvenilir referans değerler arasındaki ilişkiyi modelleyerek ölçüm hatasını azaltma işlemidir.


![sensor-kalibrasyonu-kusurlu-78](/img/sensor-kalibrasyonu-kusurlu-78.svg)

``

## Sensörler neden hatalı ölçer?

Gerçek dünyada hiçbir sensör kusursuz değildir. Üretim toleransları, sıcaklık, yaşlanma, elektriksel gürültü ve besleme gerilimindeki değişimler ölçümleri etkileyebilir. Bu etkiler genellikle üç grupta incelenir:

| Hata türü | Belirti | Örnek |
|---|---|---|
| Ofset hatası | Tüm ölçümler sabit miktarda kayar | Gerçek 20 °C, ölçülen 22 °C |
| Kazanç hatası | Hata ölçüm büyüdükçe artar | Gerçek değer iki katına çıkınca hata da büyür |
| Doğrusal olmayan hata | Tek bir düzeltme katsayısı yetmez | Uç değerlerde sensör sapar |
| Rastgele gürültü | Aynı koşulda farklı sonuçlar çıkar | 20,1; 19,8; 20,3 °C |

Kalibrasyon sistematik hataları düzeltir. Rastgele gürültüyü tamamen yok etmez; bunun için filtreleme, ortalama alma veya daha iyi donanım gerekir.

## Doğrusal kalibrasyonun mantığı

Bir sensörün ham çıktısı $x$, referans cihazın gösterdiği gerçek değer $y$ olsun. Basit bir model şöyle yazılabilir:

$$y = ax + b$$

Burada $a$ kazanç düzeltmesini, $b$ ise ofset düzeltmesini temsil eder. İki kalibrasyon noktası biliniyorsa katsayılar doğrudan hesaplanabilir:

$$a = \frac{y_2-y_1}{x_2-x_1}$$

$$b = y_1-ax_1$$

Örneğin sensör, gerçekte 0 °C olan ortamı 2 °C; 100 °C olan ortamı 96 °C ölçsün. Bu durumda $a=100/94$ ve $b=-2a$ olur. Sonraki her ham ölçüm bu denklemden geçirilerek düzeltilir.

İkiden fazla referans noktası kullanmak daha güvenilirdir. Katsayılar, ölçülen ve tahmin edilen değerler arasındaki kare hata toplamını en aza indiren doğrusal regresyonla bulunabilir. Modelin başarısı RMSE ile değerlendirilebilir:

$$RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}$$

RMSE küçüldükçe düzeltilmiş değerler referansa yaklaşır. Ancak yalnızca eğitim noktalarındaki hataya bakmak, sınav sorularını önceden ezberletmek gibidir; modeli ayrı doğrulama ölçümleriyle de test etmek gerekir.

## Python ile kalibrasyon modeli

Aşağıdaki kod, referans değerlerle sensör okumaları arasındaki doğrusal ilişkiyi öğrenir ve yeni bir ölçümü düzeltir:

```python
import numpy as np

# Sensörün ham okumaları ve güvenilir referans değerleri
ham = np.array([2.0, 20.8, 49.0, 72.4, 96.0])
referans = np.array([0.0, 20.0, 50.0, 75.0, 100.0])

# y = a*x + b modelinin katsayılarını bulur
a, b = np.polyfit(ham, referans, 1)

def kalibre_et(ham_deger):
    """Ham sensör değerini kalibre edilmiş değere dönüştürür."""
    return a * ham_deger + b

olcum = 58.5
print(f"Model: y = {a:.4f}x + {b:.4f}")
print(f"Düzeltilmiş değer: {kalibre_et(olcum):.2f}")
```

`np.polyfit`, bütün noktaları aynı anda değerlendirerek en uygun eğimi ve ofseti hesaplar. Sensör belirgin biçimde doğrusal değilse ikinci dereceden polinom kullanılabilir; ancak daha karmaşık model her zaman daha iyi model değildir. Aşırı uyum, referans noktalarında mükemmel görünen fakat yeni ölçümlerde kötü çalışan bir sonuç doğurabilir.

## Sağlam bir kalibrasyon süreci

1. Ölçüm aralığına yayılmış güvenilir referans noktaları seçin.
2. Her noktada birden fazla ölçüm alıp ortalama ve standart sapmayı hesaplayın.
3. Uygun modeli kurun ve artık hataları inceleyin.
4. Modeli kullanılmayan referans değerlerle doğrulayın.
5. Katsayıları sürüm, tarih ve ortam koşullarıyla birlikte saklayın.
6. Sensör yaşlanabileceği için kalibrasyonu düzenli aralıklarla tekrarlayın.

Kalibrasyon, kötü veriyi sihirle kusursuzlaştırmaz; ölçüm zincirini anlaşılır ve izlenebilir hâle getirir. Doğru referans, uygun matematiksel model ve düzenli doğrulama birleştiğinde ucuz bir sensör bile şaşırtıcı derecede güvenilir sonuçlar üretebilir.
