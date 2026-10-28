---
layout: post
title: "Kozmik Samanlıkta İğne Aramak: SETI ve Radyo Sinyal İşleme"
math: true
categories: 
  - Bilgi
tags: 
  - seti
  - sinyal işleme
  - radyo astronomi
  - python
  - veri analizi
  - uzay
toc: true
image: /img/kozmik-samanlikta-igne-91.png
---

Gökyüzüne çevrilmiş bir radyo teleskop, yalnızca yıldızları dinlemez; yıldırımlardan uydulara, pulsarlardan mikrodalga fırınlara kadar sayısız kaynağın oluşturduğu dev bir elektromanyetik kalabalığı kaydeder. SETI’nin, yani Dünya Dışı Akıllı Yaşam Araştırması’nın temel problemi de bu kozmik gürültü içinde yapay olabilecek kadar düzenli, dar bantlı veya tekrarlayan sinyalleri bulmaktır. Kısacası mesele sadece “uzaylıları dinlemek” değil, olağanüstü zor bir veri ayıklama problemidir.

``

## Radyo teleskop gerçekte ne kaydeder?

Bir radyo teleskop, belirli zamanlarda ölçülen elektriksel gerilim örnekleri üretir. Ham zaman serisini kabaca şöyle modelleyebiliriz:

$$x(t) = s(t) + n(t) + r(t)$$

Burada $s(t)$ aradığımız göksel sinyal, $n(t)$ doğal ve elektronik gürültü, $r(t)$ ise radyo frekansı girişimidir (RFI). Cep telefonu baz istasyonları, GPS uyduları ve radar sistemleri RFI oluşturabilir. İşin eğlenceli kısmı şudur: İlk bakışta “uzaylı mesajı” gibi görünen güçlü bir çizgi, yakındaki bir cihazın paraziti çıkabilir.

Sinyalin gücünü değerlendirmek için sinyal-gürültü oranı kullanılır:

$$\mathrm{SNR} = \frac{P_{sinyal}}{P_{gürültü}}$$

SNR yükseldikçe algılama kolaylaşır; ancak zayıf bir sinyal, uzun süre gözlemlenip örnekler birleştirilerek görünür hâle getirilebilir.

## Zaman alanından frekans alanına

Ham örneklerde düzen görmek zordur. Bu nedenle Hızlı Fourier Dönüşümü (FFT), sinyali zaman alanından frekans alanına taşır. Sonuç çoğunlukla zaman, frekans ve güç eksenlerinden oluşan bir **spektrogram** olarak incelenir.

| Yaklaşım | Gösterdiği bilgi | SETI açısından kullanım |
|---|---|---|
| Zaman serisi | Genliğin zamana göre değişimi | Darbe ve tekrar arama |
| Güç spektrumu | Enerjinin frekans dağılımı | Dar bantlı taşıyıcı bulma |
| Spektrogram | Frekansın zamanla değişimi | Doppler kaymasını izleme |
| Korelasyon | İki örüntünün benzerliği | Bilinen şablonları arama |

![kozmik-samanlikta-igne-91](/img/kozmik-samanlikta-igne-91.svg)


Uzak bir verici tek frekansta yayın yapsa bile gezegenlerin dönmesi ve yörünge hareketleri Doppler kaymasına yol açar. Gözlenen frekans yaklaşık olarak

$$f' = f\left(1 + \frac{v}{c}\right)$$

biçiminde değişir. Burada $v$ göreli radyal hız, $c$ ışık hızıdır. Spektrogramda bu etki düz bir çizgi yerine eğimli bir iz oluşturabilir.

## Basit bir dar bant sinyali arama

Aşağıdaki Python örneği, gürültülü bir zaman serisinin spektrumunu hesaplar ve en güçlü frekans bileşenini bulur:

```python
import numpy as np

ornekleme_hizi = 4096
sure = 2
t = np.arange(ornekleme_hizi * sure) / ornekleme_hizi

# 730 Hz yapay sinyali beyaz gürültü içine saklıyoruz.
veri = 0.25 * np.sin(2 * np.pi * 730 * t)
veri += np.random.normal(0, 1, len(t))

# Pencereleme, spektral sızıntıyı azaltır.
pencere = np.hanning(len(veri))
spektrum = np.abs(np.fft.rfft(veri * pencere)) ** 2
frekanslar = np.fft.rfftfreq(len(veri), 1 / ornekleme_hizi)

tepe = np.argmax(spektrum[1:]) + 1
print(f"Aday frekans: {frekanslar[tepe]:.2f} Hz")
```

Bu yöntem öğretici olsa da gerçek gözlemlerde milyonlarca frekans kanalı ve saatlerce kayıt bulunur. Ayrıca tek bir güçlü tepe, keşif ilan etmek için kesinlikle yeterli değildir.

## Bir sinyal ne zaman aday olur?

SETI işlem hatları adayları çeşitli testlerden geçirir:

1. Sinyal teleskop gökyüzünden ayrıldığında kaybolmalı, hedefe dönüldüğünde tekrar görünmelidir.
2. Aynı sinyal farklı yönlerde eşzamanlı görülüyorsa muhtemelen yerel RFI’dır.
3. Doppler sürüklenmesi fiziksel olarak makul olmalıdır.
4. Bağımsız teleskopların doğrulaması aranmalıdır.
5. Tekrarlanabilirlik, tek seferlik heyecandan daha değerlidir.

Makine öğrenmesi de spektrogram görüntülerini sınıflandırmak ve alışılmadık örüntüleri sıralamak için kullanılabilir. Fakat model, eğitim verisindeki insan yapımı parazitleri öğrenip önyargılı sonuçlar üretebilir. Bu yüzden otomasyon adayları azaltır; nihai bilimsel yorumun yerini almaz.

SETI, sabır ile istatistiğin buluştuğu bir alandır. Anlamlı bir sinyal bulunmasa bile geliştirilen FFT, filtreleme, anomali tespiti ve büyük veri teknikleri astronomiden haberleşmeye kadar pek çok alana katkı sağlar. Kozmik samanlık çok büyük olabilir; fakat arama araçlarımız her geçen gün daha keskin hâle geliyor.
