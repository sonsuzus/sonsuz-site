---
layout: post
title: "PWM ile Motor Hızı ve LED Parlaklığı Kontrolü"
math: true
categories: 
  - Bilgi
tags: 
  - pwm
  - arduino
  - motor kontrolü
  - led
  - elektronik
  - gömülü sistemler
toc: true
image: /img/pwm-ile-motor-40.png
---

Bir mikrodenetleyicinin yalnızca HIGH ve LOW üretebildiğini düşünürsek, bir LED’i nasıl yarı parlak yakabilir veya motoru yarı hızda döndürebiliriz? Cevap, elektroniğin hızlı aç-kapa illüzyonu olan PWM tekniğidir. PWM sayesinde dijital bir çıkış, analog çıkışa benzer bir davranış sergiler.
``
## PWM nedir?

PWM, **Pulse Width Modulation**, yani **Darbe Genişlik Modülasyonu** anlamına gelir. Bir dijital pin çok hızlı biçimde açılıp kapatılır. Bağlı cihaz bu geçişlerin her birine ayrı ayrı tepki vermek yerine ortalama enerjiyi hisseder.

Bir PWM sinyalinin en önemli özelliği **görev döngüsüdür**. Görev döngüsü, sinyalin bir periyot boyunca ne kadar süre HIGH seviyesinde kaldığını gösterir:

$$D = \frac{t_{HIGH}}{T} \times 100$$

Burada $D$ görev döngüsü, $t_{HIGH}$ açık kalma süresi ve $T$ toplam periyottur. Örneğin sinyal 10 milisaniyelik periyodun 7 milisaniyesinde açıksa görev döngüsü şöyledir:

$$D = \frac{7}{10} \times 100 = 70\%$$

Besleme gerilimi 5 V olduğunda ideal ortalama gerilim yaklaşık olarak hesaplanabilir:

$$V_{ortalama} = D \times V_{besleme}$$

Görev döngüsünü ondalık olarak $0{,}70$ alırsak sonuç $3{,}5$ V olur. Ancak PWM çıkışının gerçekte sürekli 3,5 V üretmediğini unutmayın; çıkış hâlâ 0 V ile 5 V arasında geçiş yapar.

| Görev döngüsü | Çıkış davranışı | LED | DC motor |
|---:|---|---|---|
| %0 | Sürekli LOW | Sönük | Durur |
| %25 | Kısa süre HIGH | Az parlak | Yavaş döner |
| %50 | Eşit aç-kapa | Orta parlak | Orta hız |
| %100 | Sürekli HIGH | Tam parlak | Tam hız |

![pwm-ile-motor-40](/img/pwm-ile-motor-40.svg)


## Frekans neden önemlidir?

PWM frekansı, aç-kapa işleminin saniyede kaç kez tekrarlandığını belirtir:

$$f = \frac{1}{T}$$

Frekans çok düşük olursa LED’de titreme görülebilir, motordan da rahatsız edici bir vınlama duyulabilir. Çok yüksek frekans ise sürücü devresindeki anahtarlama kayıplarını artırabilir. Dolayısıyla görev döngüsü verilen enerji miktarını, frekans ise bu enerjinin ne kadar hızlı paketlendiğini belirler.

## Arduino ile LED parlaklığı

Arduino Uno’da `analogWrite()` fonksiyonu 0 ile 255 arasında değer alır. Bu değer 8 bitlik PWM çözünürlüğünden gelir: $2^8 = 256$ farklı seviye vardır.

```cpp
const int ledPin = 9; // PWM destekli pin

void setup() {
  pinMode(ledPin, OUTPUT);
}

void loop() {
  for (int parlaklik = 0; parlaklik <= 255; parlaklik++) {
    analogWrite(ledPin, parlaklik);
    delay(5);
  }

  for (int parlaklik = 255; parlaklik >= 0; parlaklik--) {
    analogWrite(ledPin, parlaklik);
    delay(5);
  }
}
```

Bu kod görev döngüsünü kademeli olarak artırıp azaltarak LED’in nefes alıyormuş gibi görünmesini sağlar. LED’e uygun değerde seri direnç bağlanmalıdır.

## DC motor hız kontrolü

Motoru doğrudan mikrodenetleyici pinine bağlamak tehlikelidir. Motor, pinin sağlayabileceğinden çok daha fazla akım çeker ve oluşan ters elektromotor kuvveti karta zarar verebilir. Bu nedenle MOSFET veya motor sürücü kullanılmalıdır.

| Bileşen | Görevi |
|---|---|
| MOSFET | Motor akımını hızlı biçimde anahtarlar |
| Flyback diyot | Motor kapatıldığında oluşan gerilim darbesini bastırır |
| PWM pini | MOSFET’in görev döngüsünü belirler |
| Ortak toprak | Kontrol ve güç devrelerine aynı referansı sağlar |

```cpp
const int motorPwm = 10;

void setup() {
  pinMode(motorPwm, OUTPUT);
}

void loop() {
  analogWrite(motorPwm, 64);  // Yaklaşık %25 güç
  delay(2000);

  analogWrite(motorPwm, 128); // Yaklaşık %50 güç
  delay(2000);

  analogWrite(motorPwm, 255); // Tam güç
  delay(2000);
}
```

PWM motorun aldığı ortalama enerjiyi değiştirir; fakat hız ile görev döngüsü her zaman doğrusal değildir. Yük, sürtünme, besleme gerilimi ve motor karakteristiği sonucu etkiler. Ayrıca düşük görev döngüsünde motorun ilk hareket için yeterli torku üretememesi mümkündür.

Kısacası PWM, enerjiyi direnç üzerinde harcamak yerine anahtarlayarak kontrol ettiği için verimli ve pratiktir. LED’de parlaklık, motorda hız kontrolü sağlar; fakat doğru frekans, uygun sürücü ve güvenli devre tasarımı işin sihirli duman çıkarmayan kısmıdır!
