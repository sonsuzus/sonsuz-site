---
layout: post
title: "I²C Protokolü: Mikrodenetleyiciler Sensörlerle Nasıl Konuşuyor?"
math: true
categories: 
  - Bilgi
tags: 
  - i2c
  - mikrodenetleyici
  - sensör
  - gömülü sistemler
  - arduino
  - elektronik
toc: true
image: /img/i2c-protokolu-mikrodenetleyiciler-19.png
---

Bir mikrodenetleyicinin sıcaklık sensörüne “Orası kaç derece?” diye sorduğunu hayal edin. Sensör elbette konuşamaz; ancak I²C protokolü sayesinde ölçüm verilerini elektriksel sinyallerle iletebilir. Üstelik bunun için yalnızca iki haberleşme hattı gerekir. Arduino, ESP32, Raspberry Pi Pico ve benzeri kartların sensörlerle kurduğu bu küçük ama düzenli sohbetin arkasında adresler, saat darbeleri ve onay bitleri bulunur.

``

## I²C nedir?

I²C, “Inter-Integrated Circuit” ifadesinin kısaltmasıdır. Philips tarafından geliştirilen bu senkron seri haberleşme protokolü, aynı veri yolu üzerinde birden fazla çevre biriminin çalışmasına olanak tanır. Temel olarak iki hat kullanır:

- **SDA (Serial Data):** Adreslerin ve verilerin taşındığı hat.
- **SCL (Serial Clock):** Veri aktarımının zamanlamasını belirleyen saat hattı.

Senkron haberleşmede taraflar aynı ritmi takip eder. SCL hattı metronom, SDA hattı ise konuşmacı gibidir. Veri genellikle SCL düşükken değiştirilir ve yüksekken okunur.

| Özellik | I²C | SPI | UART |
|---|---|---|---|
| Temel hat sayısı | 2 | Genellikle 4+ | 2 |
| Saat hattı | Var | Var | Yok |
| Adresleme | Var | Çip seçme hattı kullanır | Yok |
| Birden fazla cihaz | Kolay | Ek hat gerektirir | Ek donanım gerekebilir |
| Tipik kullanım | Sensörler, RTC, EEPROM | Ekranlar, hızlı ADC | Bilgisayar ve modül iletişimi |

## Adresler neden gerekli?

Aynı SDA ve SCL hatlarına ivmeölçer, sıcaklık sensörü ve ekran bağlanabilir. Mikrodenetleyici hangi cihazla konuşacağını, aktarımın başında bir adres göndererek belirtir. Çoğu I²C cihazı **7 bit adres** kullanır. Teorik adres uzayı

$$2^7 = 128$$

olsa da bazı adresler özel amaçlara ayrılmıştır. Örneğin bir sensörün adresi `0x76`, ekranın adresi `0x3C` olabilir. Aynı sabit adrese sahip iki cihaz veri yoluna bağlanırsa adres çakışması yaşanır. Bu durumda adres seçim pini, I²C çoklayıcı veya ayrı veri yolu kullanılabilir.

## Bir veri aktarımı nasıl gerçekleşir?

İletişimi çoğunlukla **controller** rolündeki mikrodenetleyici başlatır. Sensör ise **target** olarak yanıt verir. Tipik okuma sırası şöyledir:

1. Controller bir **START** koşulu üretir.
2. Hedef cihazın adresini ve okuma/yazma bitini gönderir.
3. Hedef cihaz bir **ACK** bitiyle “Buradayım!” der.
4. Register adresi veya veri baytları aktarılır.
5. Controller bir **STOP** koşuluyla görüşmeyi bitirir.

Bir bayt 8 veri bitinden oluşur ve ardından ACK/NACK biti gelir. Saat frekansı $f_{SCL}$ ise tek bir bitin yaklaşık süresi

$$T_{bit} = \frac{1}{f_{SCL}}$$

şeklindedir. Örneğin 100 kHz hızda bir saat periyodu yaklaşık $10\,\mu s$ olur. ACK bitleri ve protokol koşulları nedeniyle gerçek veri hızı teorik üst sınırdan daha düşüktür.

## Pull-up dirençleri neden şart?

SDA ve SCL çıkışları genellikle **open-drain** yapısındadır. Cihazlar hattı doğrudan yüksek seviyeye sürmez; yalnızca aşağı çekebilir. Hatların tekrar lojik 1 seviyesine çıkması için VCC’ye bağlı pull-up dirençleri gerekir.

| Direnç durumu | Olası sonuç |
|---|---|
| Çok büyük | Sinyal yavaş yükselir, yüksek hızda hata oluşur |
| Çok küçük | Gereksiz akım tüketilir |
| Uygun değer | Temiz kenarlar ve güvenilir iletişim sağlanır |

Kısa bağlantılarda 4.7 kΩ sık kullanılan bir başlangıç değeridir; ideal değer hat kapasitansına, gerilime ve haberleşme hızına bağlıdır.

## Arduino ile sensör register’ı okumak

Aşağıdaki örnek, `0x76` adresli cihazın `0xD0` register’ından bir bayt okur:

```cpp
#include <Wire.h>

const byte DEVICE_ADDRESS = 0x76;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  Wire.beginTransmission(DEVICE_ADDRESS);
  Wire.write(0xD0);              // Okunacak register adresi
  Wire.endTransmission(false);   // STOP göndermeden devam et

  Wire.requestFrom(DEVICE_ADDRESS, (byte)1);
  if (Wire.available()) {
    byte value = Wire.read();
    Serial.println(value, HEX);
  }
}

void loop() {}
```

`endTransmission(false)` tekrarlanan START üreterek register seçimi ile okuma işlemini tek oturumda tutar. Sensör cevap vermiyorsa önce adresi, kabloları, ortak GND bağlantısını, besleme gerilimini ve pull-up dirençlerini kontrol edin. Bir logic analyzer kullanmak da SDA ve SCL üzerindeki görünmez sohbeti ekranda okunabilir hâle getirir. I²C’nin büyüsü tam burada yatar: iki kablo, çok sayıda cihaz ve şaşırtıcı derecede düzenli bir dijital konuşma!

![i2c-protokolu-mikrodenetleyiciler-19](/img/i2c-protokolu-mikrodenetleyiciler-19.svg)

