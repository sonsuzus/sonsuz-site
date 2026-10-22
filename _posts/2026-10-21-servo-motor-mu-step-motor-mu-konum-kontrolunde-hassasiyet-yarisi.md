---
layout: post
title: "Servo Motor mu Step Motor mu? Konum Kontrolünde Hassasiyet Yarışı"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - servo motor
  - step motor
  - konum kontrolü
  - arduino
  - otomasyon
toc: true
image: /img/servo-motor-mu-49.png
---

Robotik bir sistem tasarlarken motor seçimi, robotun ne kadar düzgün ve doğru hareket edeceğini doğrudan belirler. Servo motorlar ile step motorlar aynı hedefe, yani kontrollü konumlandırmaya hizmet etse de bu hedefe oldukça farklı yollarla ulaşır. Biri konumunu sürekli ölçerek ilerlerken diğeri verilen adımları sayar. Peki hangisi gerçekten daha hassastır?

``

## Hassasiyet, çözünürlük ve doğruluk

Öncelikle sıkça birbirine karıştırılan üç kavramı ayıralım:

- **Çözünürlük:** Motorun komut verilebilen en küçük hareket miktarıdır.
- **Doğruluk:** Motorun hedeflenen konuma ne kadar yaklaşabildiğidir.
- **Tekrarlanabilirlik:** Aynı hedefe tekrar tekrar giderken benzer sonuç üretmesidir.

Bir motorun çok küçük hareketler yapabilmesi, hedefe mutlaka doğru ulaştığı anlamına gelmez. Cetvelinizde milimetre çizgileri bulunması, her ölçümü kusursuz yapacağınızı garanti etmez!

## Step motor nasıl konumlanır?

Yaygın bir step motorun tam adım açısı $1.8^\circ$ değerindedir. Bir turdaki adım sayısı şöyle hesaplanır:

$$N = \frac{360^\circ}{1.8^\circ} = 200$$

Sürücü 16 mikro-adım modunda çalıştırılırsa teorik açısal çözünürlük:

$$\theta = \frac{1.8^\circ}{16} = 0.1125^\circ$$

olur. Bu etkileyici görünse de mikro-adımların mekanik olarak eşit büyüklükte gerçekleşmesi garanti değildir. Yük, sürtünme, rezonans ve sürücü akımı gerçek konumu etkiler. Ayrıca klasik step motor sistemleri açık çevrimlidir: Kontrolcü adım sinyalini gönderir fakat motorun gerçekten hareket edip etmediğini kontrol etmez. Motor adım kaçırırsa yazılım hâlâ doğru konumda olduğunu zanneder.

## Servo motor nasıl konumlanır?

Servo sisteminde enkoder, motor milinin konumunu ölçer. Kontrolcü hedef konum ile ölçülen konum arasındaki hatayı hesaplar:

$$e(t) = \theta_{hedef}(t) - \theta_{ölçülen}(t)$$

Ardından genellikle PID benzeri bir denetleyici bu hatayı azaltmaya çalışır. Böylece yük motoru geriye itse bile sistem bunu fark ederek düzeltme uygulayabilir. Servo motorun çözünürlüğü, enkoder çözünürlüğüne bağlıdır. Örneğin tur başına 4096 sayım üreten bir enkoderin teorik çözünürlüğü:

$$\frac{360^\circ}{4096} \approx 0.088^\circ$$

seviyesindedir. Endüstriyel enkoderlerde bu değer çok daha küçük olabilir.

| Özellik | Step motor | Servo motor |
|---|---|---|
| Kontrol yapısı | Genellikle açık çevrim | Kapalı çevrim |
| Konum geri bildirimi | Çoğunlukla yok | Enkoder ile var |
| Düşük hız performansı | Güçlü ve kararlı | Denetleyici ayarına bağlı |
| Yüksek hız performansı | Tork hızla azalabilir | Genellikle daha başarılı |
| Adım veya konum kaybı | Fark edilmeyebilir | Algılanıp düzeltilebilir |
| Maliyet | Daha düşük | Daha yüksek |
| Gerçek konum doğruluğu | Yüke oldukça bağlı | Genellikle daha yüksek |

## Basit bir step motor kontrolü

Aşağıdaki Arduino kodu, sürücüye 200 adım göndererek motoru teorik olarak bir tur döndürür:

```cpp
const int stepPin = 3;
const int dirPin = 4;

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  digitalWrite(dirPin, HIGH);

  for (int i = 0; i < 200; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(800);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(800);
  }
}

void loop() {}
```

Kod, darbeleri eksiksiz üretir; ancak milin gerçekten bir tur dönüp dönmediğini bilemez. Servo sistemindeki temel fark tam olarak budur: Enkoder değeri okunur, hedefle karşılaştırılır ve hata varsa yeni bir düzeltme komutu oluşturulur.

## Mekanik sistem de yarışa katılır

Motor ne kadar hassas olursa olsun redüktör boşluğu, kayış esnemesi, kaplin hatası ve rulman toleransı sonucu bozabilir. Toplam konum hatası kabaca şöyle düşünülebilir:

$$E_{toplam} = E_{motor} + E_{enkoder} + E_{mekanik} + E_{kontrol}$$

Bu nedenle yalnızca motor kataloğundaki çözünürlük değerine bakmak yanıltıcıdır. Hafif yük, düşük hız ve uygun maliyet gereken 3B yazıcı veya küçük CNC uygulamalarında step motor fazlasıyla yeterli olabilir. Değişken yük, yüksek hız ve konum kaybının kabul edilemediği robot kollarında ise servo motor belirgin biçimde avantajlıdır.

Kısacası step motor teorik olarak çok küçük adımlar sunabilir; servo motor ise geri bildirim sayesinde gerçek konumu daha güvenilir biçimde korur. Hassasiyet yarışının genel galibi servodur, fakat doğru motor her zaman uygulamanın hızına, yüküne, bütçesine ve hata toleransına göre seçilir.

![servo-motor-mu-49](/img/servo-motor-mu-49.svg)

