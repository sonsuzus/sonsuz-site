---
layout: post
title: "ADC ve DAC: Gerçek Dünya ile Dijital Evren Arasındaki Köprü"
math: true
categories: 
  - Bilgi
tags: 
  - adc
  - dac
  - elektronik
  - sinyal işleme
  - mikrodenetleyici
  - örnekleme
toc: true
image: /img/adc-ve-dac-33.png
---

Bir mikrodenetleyici sıcaklığı nasıl “görür”, hoparlör ise bir sayı dizisini nasıl müziğe dönüştürür? Bu sihrin arkasında iki temel devre bulunur: analogdan dijitale dönüştürücü **ADC** ve dijitalden analoğa dönüştürücü **DAC**. Biri fiziksel dünyayı sayılara çevirirken diğeri bu yolculuğu tersine çevirir.

``

## Analog ve dijital dünya

Sıcaklık, ses, ışık ve basınç gibi fiziksel büyüklükler çoğunlukla süreklidir. Örneğin bir mikrofonun çıkış gerilimi, ses dalgasına bağlı olarak zaman içinde kesintisiz biçimde değişir. Bilgisayarlar ise sürekli değerlerle değil, sonlu sayı kümeleriyle çalışır.

ADC, analog giriş gerilimini belirli aralıklarla ölçerek sayısal bir koda dönüştürür. DAC ise verilen sayısal kodu karşılık gelen analog gerilim veya akım olarak üretir.

| Özellik | ADC | DAC |
|---|---|---|
| Dönüşüm yönü | Analogdan dijitale | Dijitalden analoğa |
| Tipik giriş | Gerilim, akım | İkili sayı |
| Tipik çıkış | İkili sayı | Gerilim, akım |
| Kullanım alanı | Sensörler, mikrofonlar | Hoparlörler, motor kontrolü |
| Temel problem | Örnekleme ve nicemleme | Basamaklı çıkış ve filtreleme |

## ADC nasıl çalışır?

ADC işlemi üç aşamada düşünülebilir: **örnekleme**, **nicemleme** ve **kodlama**. Örnekleme sırasında sinyalin belirli anlardaki değeri alınır. Nicemleme, bu değeri izin verilen en yakın seviyeye yuvarlar. Son olarak seviye, ikili sayı biçiminde kodlanır.

$n$ bit çözünürlüğe sahip bir ADC’nin seviye sayısı:

$$L = 2^n$$

Örneğin 10 bit ADC, $2^{10}=1024$ farklı değer üretebilir. Referans gerilimi $V_{ref}=5\text{ V}$ ise yaklaşık adım büyüklüğü:

$$\Delta V = \frac{V_{ref}}{2^n} = \frac{5}{1024} \approx 4.88\text{ mV}$$

Bu durumda ADC, 2,500 V ile 2,503 V arasındaki küçücük farkı ayırt edemeyebilir. Dijital dünyanın “her şeyi bilen robot” değil, elindeki cetvel kadar hassas bir ölçümcü olduğunu söyleyebiliriz.

Örnekleme hızı da önemlidir. Nyquist teoremine göre en yüksek frekansı $f_{max}$ olan bir sinyal için:

$$f_s \geq 2f_{max}$$

Aksi hâlde **aliasing** oluşur; yüksek frekanslar yanlışlıkla daha düşük frekanslarmış gibi görünür. Bu nedenle ADC girişinde sıklıkla alçak geçiren filtre kullanılır.

## DAC sayıları nasıl elektriğe çevirir?

DAC, dijital kodun oranına göre analog çıkış üretir. İdeal bir tek kutuplu DAC için yaklaşık ilişki şöyledir:

$$V_{out}=V_{ref}\frac{D}{2^n-1}$$

Burada $D$, dijital kodun ondalık değeridir. Örneğin 8 bit, 5 V referanslı bir DAC’a 128 gönderildiğinde çıkış yaklaşık 2,51 V olur.

Gerçek DAC çıkışı anında kusursuz bir eğri oluşturmaz; basamaklara benzeyen bir sinyal üretir. Çıkıştaki yeniden yapılandırma filtresi bu basamakların yüksek frekanslı bileşenlerini azaltarak daha pürüzsüz bir sinyal sağlar.

## Mikrodenetleyici üzerinde küçük bir örnek

Aşağıdaki Arduino kodu, potansiyometreden ADC ile değer okur ve PWM destekli çıkışa aktarır. PWM gerçek bir DAC değildir; görev döngüsünü değiştirir. Alçak geçiren filtre eklendiğinde ortalama gerilim analog çıkış gibi kullanılabilir.

```cpp
const int sensorPin = A0;
const int outputPin = 9;

void setup() {
  pinMode(outputPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int adcValue = analogRead(sensorPin);      // 0-1023
  int pwmValue = map(adcValue, 0, 1023, 0, 255);

  analogWrite(outputPin, pwmValue);          // PWM görev döngüsü
  Serial.println(adcValue);
  delay(10);
}
```

| Yöntem | Gerçek analog çıkış | Ek filtre ihtiyacı | Tipik maliyet |
|---|---:|---:|---:|
| Dahili DAC | Evet | Bazen | Orta |
| PWM | Hayır | Genellikle | Düşük |
| Harici DAC | Evet | Uygulamaya bağlı | Daha yüksek |

## Pratikte nelere dikkat edilmeli?

Bit sayısı tek başına kalite garantisi değildir. Referans geriliminin kararlılığı, elektriksel gürültü, dönüşüm hızı, doğrusal olmama hataları ve devre yerleşimi sonucu doğrudan etkiler. 16 bit etiketi taşıyan gürültülü bir ADC, pratikte 12 bitlik temiz bir ADC’den daha kötü sonuç verebilir.

Özetle ADC, sensörlerin dilini yazılıma tercüme eder; DAC ise yazılımın sayılarını fiziksel dünyaya anlatır. Telefon görüşmesinden dijital termometreye, müzik sisteminden endüstriyel motorlara kadar bu iki dönüştürücü, kod ile elektriğin sürekli el sıkışmasını sağlar.

![adc-ve-dac-33](/img/adc-ve-dac-33.svg)

