---
layout: post
title: "Hassas Montajda Robotun Dokunma Duyusu: Kuvvet Geri Beslemeli Manipülasyon"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - kuvvet-kontrolü
  - hassas-montaj
  - empedans-kontrolü
  - otomasyon
  - sensör
toc: true
image: /img/hassas-montajda-robotun-96.png
---

Bir robotun milimetrenin altında toleransa sahip bir parçayı yuvasına yerleştirdiğini düşünün. Yalnızca konum komutlarını takip eden robot, küçük bir hizalama hatasında parçayı sıkıştırabilir veya kırabilir. Kuvvet geri beslemeli manipülasyon ise robota adeta bir dokunma duyusu kazandırır: Robot sadece nerede olduğunu değil, çevreyle nasıl temas kurduğunu da anlayarak hareketini düzenler.
``

## Neden yalnızca konum kontrolü yetmez?

Geleneksel konum kontrolünde amaç, robotun gerçek konumunu hedef konuma yaklaştırmaktır. Basitleştirilmiş kontrol hatası

$$e_x = x_d - x$$

şeklinde tanımlanır. Burada $x_d$ hedef, $x$ ise ölçülen konumdur. Robot bu hatayı azaltmaya çalışır. Ancak montaj ortamında parça ölçüleri, fikstür konumu veya yüzey geometrisi kusursuz değildir. Robot hedefe kararlılıkla ilerlerken beklenmedik bir temas gerçekleşirse büyük kuvvetler oluşabilir.

Kuvvet geri beslemesinde bilek tipi kuvvet-tork sensörü, eklem tork sensörleri veya motor akımı üzerinden tahmin edilen temas kuvveti kullanılır. Kuvvet hatası

$$e_f = F_d - F_m$$

olarak ifade edilir. $F_d$ istenen temas kuvveti, $F_m$ ölçülen kuvvettir. Kontrolcü bu farkı kullanarak robotun hızını, konumunu ya da uyguladığı torku günceller.

| Yaklaşım | Öncelikli bilgi | Güçlü yönü | Temel risk |
|---|---|---|---|
| Konum kontrolü | Pozisyon ve yönelim | Serbest uzayda yüksek doğruluk | Temasta aşırı kuvvet |
| Kuvvet kontrolü | Temas kuvveti | Güvenli ve kararlı temas | Serbest uzayda anlamlı değildir |
| Hibrit kontrol | Konum ve kuvvet | Montaj eksenlerini ayrı yönetir | Model ve ayar karmaşıktır |
| Empedans kontrolü | Kuvvet-hareket ilişkisi | Esnek, doğal etkileşim | Yanlış parametreler salınım üretir |

## Empedans: Robotun sanal yayları

Hassas montajda en yaygın fikirlerden biri empedans kontrolüdür. Robotun çevreye karşı yay, sönümleyici ve kütle gibi davranması hedeflenir:

$$M_d\ddot{x}+D_d\dot{x}+K_d(x-x_d)=F_{ext}$$

Burada $M_d$ sanal kütleyi, $D_d$ sönümü, $K_d$ ise sanal rijitliği temsil eder. Büyük $K_d$ robotu sert ve konuma bağlı yapar; küçük $K_d$ ise uyumluluğu artırır. Fazla yumuşak robot hedefi bulmakta zorlanabilir, fazla sert robot da parçaya “ben geldim!” diye kafa atabilir. Bu nedenle parametreler görev eksenlerine göre ayrı seçilir.

Örneğin pim-delik montajında robot, dikey eksende kontrollü bir yerleştirme kuvveti uygularken yatay eksenlerde küçük düzeltmelere izin verebilir. Böylece pimin kenara temasından doğan kuvvet, hizalama için bilgiye dönüşür. Bu yaklaşım arama, yüzey takip etme, konnektör takma ve hassas geçme işlemlerinde oldukça etkilidir.

## Basit bir geri besleme örneği

Aşağıdaki Python benzeri kod, ölçülen dikey kuvvete göre robot hızını düzeltir. Gerçek sistemlerde güvenlik sınırları, filtreleme ve gerçek zamanlı haberleşme ayrıca uygulanmalıdır.

```python
TARGET_FORCE = 8.0       # İstenen temas kuvveti, N
MAX_FORCE = 20.0         # Güvenlik sınırı, N
GAIN = 0.002             # Kuvvet hatasından hız üretir

while assembly_active:
    measured_force = sensor.read_force_z()

    if abs(measured_force) > MAX_FORCE:
        robot.stop()
        raise RuntimeError("Aşırı temas kuvveti")

    force_error = TARGET_FORCE - measured_force
    vertical_speed = GAIN * force_error
    robot.command_velocity(z=vertical_speed)
```

Bu döngüde kuvvet düşükse robot temasa doğru ilerler; kuvvet hedefi aşarsa geri çekilir. Ancak sensör gürültüsü doğrudan komuta aktarılırsa titreşim oluşabilir. Bu yüzden alçak geçiren filtre, uygun örnekleme süresi ve gecikme analizi kritik önem taşır.

## Hassasiyet kadar süreç bilgisi de sağlar

Kuvvet verileri yalnızca kontrol amacıyla kullanılmaz. Kuvvet-zaman veya kuvvet-konum eğrileri; parçanın sıkıştığını, contanın doğru oturduğunu ya da konnektörün kilitlendiğini gösterebilir. Böylece sistem, montajı tamamlamakla kalmaz, işlemin kalitesini de denetler.

Sonuç olarak kuvvet geri beslemesi, geometrik belirsizlikleri fiziksel temas üzerinden yöneterek hata oranını ve parça hasarını azaltır. Başarılı bir uygulama için doğru sensör, kararlı kontrol algoritması, görev yönlerine uygun uyumluluk ve kesin güvenlik eşikleri birlikte tasarlanmalıdır. Robotun gözü kameraysa, kuvvet geri beslemesi de parmak uçlarıdır.

![hassas-montajda-robotun-96](/img/hassas-montajda-robotun-96.svg)

