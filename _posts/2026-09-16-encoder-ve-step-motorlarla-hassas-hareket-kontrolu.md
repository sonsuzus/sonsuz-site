---
layout: post
title: "Encoder ve Step Motorlarla Hassas Hareket Kontrolü"
math: true
categories: 
  - Bilgi
tags: 
  - encoder
  - step-motor
  - pid
  - arduino
  - hareket-kontrolü
  - otomasyon
toc: true
---

Step motorlar komutları adım adım uygulayan disiplinli çalışanlara benzer; encoderlar ise işin gerçekten yapılıp yapılmadığını denetleyen dikkatli yöneticilerdir. Bu ikili doğru bir kontrol algoritmasıyla birleştirildiğinde CNC tezgâhlarından robot kollarına kadar pek çok sistemde hassas, tekrarlanabilir ve güvenilir hareket elde edilir. Gelin açık çevrim rahatlığından kapalı çevrim hassasiyetine uzanan bu mekanik yolculuğa çıkalım.

``

## Step motorun hareket mantığı

Step motor, elektrik darbelerini belirli açısal hareketlere dönüştürür. Örneğin tur başına 200 adımı bulunan bir motorun doğal adım açısı:

$$
A = 360 / 200 = 1.8^\circ
$$

Sürücü 16 mikro adım modunda çalıştırılırsa teorik çözünürlük tur başına $200 \times 16 = 3200$ mikro adıma yükselir. Hedef açı için gönderilmesi gereken darbe sayısı şöyle hesaplanır:

$$
N = (H / 360) \times S \times M
$$

Burada $H$ hedef açıyı, $S$ motorun tam adım sayısını, $M$ ise mikro adım katsayısını ifade eder. Ancak mikro adım kullanmak her zaman aynı oranda gerçek mekanik doğruluk sağlamaz. Motor torku, yük, boşluk ve sürtünme sonucu etkiler.

## Encoder neden gereklidir?

Step motor sürücüsü darbe gönderildiğinde motorun hareket ettiğini varsayar. Yük fazla gelirse motor adım kaçırabilir ve kontrol sistemi bundan haberdar olmayabilir. Encoder ise motor milinin gerçek konumunu ölçerek varsayımı ölçülebilir bilgiye dönüştürür.

Artımlı quadrature encoderlarda A ve B adlı iki kanal arasında faz farkı bulunur. Bu sayede hem hareket miktarı hem de yön belirlenebilir. Encoder tur başına $P$ darbe üretiyor ve dört kenar sayımı kullanılıyorsa açısal konum yaklaşık olarak:

$$
Q = C \times 360 / (4P)
$$

formülüyle bulunur. Burada $C$, sayılan encoder kenarıdır.

| Özellik | Açık çevrim step motor | Encoder geri beslemeli sistem |
|---|---|---|
| Konum bilgisi | Tahmin edilir | Ölçülür |
| Adım kaçırma | Fark edilmez | Algılanabilir |
| Yazılım karmaşıklığı | Düşük | Orta veya yüksek |
| Yük değişimine dayanım | Sınırlı | Daha güçlü |
| Kalibrasyon ihtiyacı | Az | Daha fazla |

## Kapalı çevrim kontrol

Kontrol sisteminde hedef konum ile encoderın ölçtüğü konum karşılaştırılır:

$$
e(t) = hedef(t) - ölçüm(t)
$$

Ortaya çıkan hata pozitifse motor ileri, negatifse geri hareket ettirilir. Basit uygulamalarda hata büyüklüğüne göre step frekansı ayarlanabilir. Daha akıcı sistemlerde PID kontrolü kullanılır:

$$
u(t) = K_p e(t) + K_i \int e(t)dt + K_d de(t)/dt
$$

Oransal terim mevcut hataya tepki verir, integral terimi kalıcı hatayı azaltır, türev terimi ise ani değişimleri frenler. Yanlış ayarlanmış PID, hassasiyet yerine masada dans eden bir motor üretebilir; bu nedenle düşük kazançlarla başlamak güvenlidir.

## Arduino ile temel uygulama

Aşağıdaki örnek encoder sayımını izler ve hedefe göre motor yönünü belirler. Kesme kullanılması, hızlı encoder darbelerinin kaçırılma riskini azaltır.

```cpp
const int stepPin = 5;
const int dirPin = 6;
const int encA = 2;
const int encB = 3;

volatile long encoderCount = 0;
long targetCount = 4000;

void readEncoder() {
  if (digitalRead(encA) == digitalRead(encB))
    encoderCount++;
  else
    encoderCount--;
}

void makeStep() {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(4);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(500);
}

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(encA, INPUT_PULLUP);
  pinMode(encB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encA), readEncoder, CHANGE);
}

void loop() {
  long error = targetCount - encoderCount;

  if (abs(error) > 2) {
    digitalWrite(dirPin, error > 0 ? HIGH : LOW);
    makeStep();
  }
}
```

İki sayımlık tolerans bölgesi motorun hedef çevresinde sürekli ileri geri titreşmesini önler. Gerçek projede hızlanma ve yavaşlama rampaları eklenmeli; aksi hâlde motor yüksek frekansta aniden başlatıldığında adım kaçırabilir.

## Mekanik ayrıntıları unutmayın

Yazılım kusursuz olsa bile kaplin boşluğu, kayış esnemesi ve rulman toleransı sonucu bozabilir. Encoder motor milindeyse motor hareketini ölçer, fakat yük tarafındaki boşluğu göremeyebilir. Çok yüksek doğruluk gereken makinelerde encoderın doğrudan hareketli eksene yerleştirilmesi daha doğrudur.

Sonuç olarak step motor komutu, encoder gerçeği, kontrol algoritması ise ikisi arasındaki uzlaşmayı temsil eder. Sağlam mekanik, doğru elektrik bağlantıları ve dikkatli ayarlanmış kontrol parametreleri birleştiğinde mikrometre seviyesine yaklaşan hareketler ulaşılabilir bir mühendislik hedefi hâline gelir.
