---
layout: post
title: "Mikrodenetleyiciler Arasında I2C ve SPI ile Güvenilir Seri Haberleşme"
math: true
categories: 
  - Bilgi
tags: 
  - ı2c
  - spı
  - mikrodenetleyici
toc: true
---

Bir mikrodenetleyiciyi sensörler, ekranlar veya başka işlemcilerle konuşturmak istediğimizde her bit için ayrı kablo çekmek pek akıllıca değildir. I2C ve SPI, verileri bit bit aktararak kablo sayısını azaltan iki popüler seri haberleşme standardıdır. İkisi de kısa mesafelerde hızlı ve güvenilir çalışır; ancak kablo yapıları, hızları ve cihaz seçme yöntemleri farklıdır.

``

## Seri haberleşmenin temel mantığı

Seri haberleşmede veri, ortak bir saat sinyaline göre sırayla gönderilir. Bir baytın sekiz bitten oluştuğunu düşünürsek ideal aktarım süresi yaklaşık olarak

$$t = \frac{N}{f_{clock}}$$

şeklinde hesaplanabilir. Burada $N$ gönderilen bit sayısını, $f_{clock}$ ise saat frekansını belirtir. Örneğin 400 kHz saat hızında sekiz bitin teorik aktarım süresi $20\,\mu s$ olur. Adres, onay ve protokol bitleri nedeniyle gerçek süre biraz daha uzundur.

Saat hattı sayesinde alıcı, veri hattını ne zaman okuyacağını bilir. Yine de iki cihazın aynı gerilim seviyesinde çalışması, ortak bir GND bağlantısına sahip olması ve kabloların gereksiz yere uzatılmaması gerekir. Aksi hâlde dijital sinyal, elektronik bir dedikoduya dönüşebilir.

## I2C: İki kabloyla kalabalık toplantı

I2C, **SDA** veri ve **SCL** saat olmak üzere iki sinyal hattı kullanır. Aynı veri yoluna birçok cihaz bağlanabilir. Kontrolcü haberleşmeyi başlatır ve iletişim kuracağı cihazı adresiyle çağırır. Cihaz da her bayttan sonra ACK biti göndererek veriyi aldığını bildirir.

SDA ve SCL hatları açık-kollektör yapıdadır. Bu nedenle hatların lojik 1 seviyesine çıkabilmesi için pull-up dirençleri gerekir. Yükselme süresi yaklaşık olarak

$$t_r \approx 0.8473 R_p C_b$$

ifadesiyle modellenebilir. $R_p$ pull-up direnci, $C_b$ ise toplam hat kapasitansıdır. Çok büyük direnç yavaş yükselmeye, çok küçük direnç ise gereksiz akıma neden olur.

```cpp
#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
}

void loop() {
  Wire.beginTransmission(0x48); // Sensörün I2C adresi
  Wire.write(0x00);             // Okunacak kayıt
  Wire.endTransmission(false);  // Veri yolunu bırakmadan devam et

  Wire.requestFrom(0x48, 2);
  if (Wire.available() == 2) {
    int value = (Wire.read() << 8) | Wire.read();
    Serial.println(value);
  }
  delay(500);
}
```

Bu örnek, `0x48` adresindeki sensörün bir kaydını seçer ve iki baytlık ölçümü birleştirir. Gerçek projede zaman aşımı ve hata kontrolü de eklenmelidir.

## SPI: Daha fazla kablo, daha yüksek hız

SPI genellikle **SCLK**, **MOSI**, **MISO** ve **CS** hatlarını kullanır. Adres gönderilmez; kontrolcü, konuşacağı cihazın CS hattını aktif eder. Veri aynı anda gönderilip alınabildiği için SPI tam çift yönlüdür ve çoğu uygulamada I2C’den daha yüksek hızlara çıkabilir.

```cpp
#include <SPI.h>

void setup() {
  SPI.begin();
  pinMode(10, OUTPUT);
  digitalWrite(10, HIGH);
}

uint8_t readRegister(uint8_t address) {
  SPI.beginTransaction(SPISettings(4000000, MSBFIRST, SPI_MODE0));
  digitalWrite(10, LOW);
  SPI.transfer(address | 0x80); // Okuma bitini etkinleştir
  uint8_t result = SPI.transfer(0x00);
  digitalWrite(10, HIGH);
  SPI.endTransaction();
  return result;
}
```

`SPISettings`, saat hızını, bit sırasını ve SPI modunu belirler. Bu değerler çevre biriminin veri sayfasıyla aynı olmalıdır.

## Hangisini seçmeliyiz?

| Özellik | I2C | SPI |
|---|---|---|
| Temel sinyal sayısı | 2 | 4 ve üzeri |
| Cihaz seçimi | Adres | Ayrı CS hattı |
| Tipik hız | 100 kHz–1 MHz | Birkaç MHz ve üzeri |
| İletişim yönü | Yarı çift yönlü | Tam çift yönlü |
| Donanım karmaşıklığı | Düşük | Orta |
| Uygun kullanım | Sensörler, RTC, EEPROM | Ekran, ADC, hızlı bellek |

Az pinle çok sayıda düşük hızlı sensör bağlanacaksa I2C iyi bir seçimdir. Yüksek örnekleme hızı, düşük gecikme veya hızlı ekran güncellemesi gerekiyorsa SPI öne çıkar. Her iki protokolde de kısa bağlantılar, doğru gerilim seviyeleri, temiz besleme ve üretici veri sayfasına uygun saat ayarları güvenilirliğin asıl anahtarıdır.
