---
layout: post
title: "SPI Protokolü: Yüksek Hızlı Çevresel Donanım İletişiminin Mantığı"
math: true
categories: 
  - Bilgi
tags: 
  - spi
  - gömülü sistemler
  - mikrodenetleyici
  - donanım
  - seri iletişim
  - elektronik
toc: true
image: /img/spi-protokolu-yuksek-96.png
---

Bir mikrodenetleyicinin sensör, ekran, ADC, DAC veya flash bellek gibi çevresel donanımlarla hızlı konuşması gerektiğinde SPI çoğu zaman sahneye çıkar. Açılımı **Serial Peripheral Interface** olan bu protokol, veriyi bit bit aktarmasına rağmen yüksek saat frekansı ve basit çalışma mantığı sayesinde oldukça hızlıdır. Kısacası SPI, donanım dünyasının “lafı dolandırmadan doğrudan konuşan” iletişim yöntemlerinden biridir.
``

## SPI hangi hatları kullanır?

SPI haberleşmesinde genellikle bir **denetleyici** ve bir ya da daha fazla **çevresel cihaz** bulunur. Eski kaynaklarda bunlar master ve slave olarak da adlandırılır. Standart bir bağlantıda dört temel sinyal vardır:

| Hat | Açıklama | Veri yönü |
|---|---|---|
| SCLK | Seri saat sinyali | Denetleyiciden çevresel cihaza |
| MOSI | Denetleyiciden çıkan veri | Denetleyici → cihaz |
| MISO | Çevresel cihazdan çıkan veri | Cihaz → denetleyici |
| CS/SS | İletişim kurulacak cihazı seçer | Denetleyiciden cihaza |

Denetleyici, SCLK hattında saat darbeleri üretir. Her darbe sırasında MOSI üzerinden bir bit gönderilebilirken MISO üzerinden başka bir bit alınabilir. Bu nedenle SPI **tam çift yönlü**, yani full-duplex iletişimi destekler. Sekiz bitlik bir aktarım için temel süre yaklaşık olarak

$$t_{aktarim} = \frac{8}{f_{SCLK}}$$

şeklinde hesaplanabilir. Örneğin saat frekansı $8\,MHz$ ise teorik olarak bir baytın aktarımı $1\,\mu s$ sürer. Komutlar, CS geçişleri ve yazılım gecikmeleri gerçek süreyi biraz artırabilir.

## Saat kutbu ve fazı neden önemlidir?

SPI standardı tek bir saat davranışı dayatmaz. **CPOL**, saat hattının boşta hangi seviyede durduğunu; **CPHA** ise verinin hangi saat kenarında örnekleneceğini belirler. Bu iki değer dört SPI modu oluşturur:

| Mod | CPOL | CPHA | Boşta saat seviyesi |
|---|---:|---:|---|
| Mode 0 | 0 | 0 | Düşük |
| Mode 1 | 0 | 1 | Düşük |
| Mode 2 | 1 | 0 | Yüksek |
| Mode 3 | 1 | 1 | Yüksek |

Denetleyici ile çevresel cihaz farklı modlarda ayarlanırsa bitler yanlış kenarda okunur. Sonuç genellikle anlamsız veriler, kaymış bitler ve geliştiricinin osiloskoba uzun uzun bakmasıdır. Doğru mod, cihazın veri sayfasından öğrenilmelidir.

## Birden fazla cihaz nasıl bağlanır?

SCLK, MOSI ve MISO hatları cihazlar arasında paylaşılabilir; fakat çoğunlukla her cihaz için ayrı bir CS hattı gerekir. Denetleyici iletişim kuracağı cihazın CS hattını genellikle lojik sıfıra çeker, aktarımı gerçekleştirir ve ardından hattı tekrar bire yükseltir.

Bu yaklaşım hızlı ve öngörülebilirdir ancak cihaz sayısı arttıkça daha fazla GPIO pini tüketir. Ayrıca seçili olmayan cihazların MISO çıkışını yüksek empedans durumuna alması gerekir; aksi hâlde aynı hattı birden fazla cihaz sürmeye çalışabilir.

## Arduino ile örnek aktarım

Aşağıdaki örnek, SPI üzerinden bir çevresel cihaza komut gönderip yanıt baytı okur:

```cpp
#include <SPI.h>

const int CS_PIN = 10;

void setup() {
  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);
  SPI.begin();
}

uint8_t registerOku(uint8_t adres) {
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));
  digitalWrite(CS_PIN, LOW);

  SPI.transfer(adres | 0x80);       // Okuma komutunu gönderir
  uint8_t veri = SPI.transfer(0x00); // Saat üretirken yanıtı alır

  digitalWrite(CS_PIN, HIGH);
  SPI.endTransaction();
  return veri;
}
```

`SPISettings`, frekansı, bit sırasını ve SPI modunu tanımlar. `SPI.transfer()` çağrısı aynı anda hem veri gönderir hem veri alır. Yalnızca okuma yapılacak olsa bile saat sinyali üretmek için sahte bir bayt gönderilmesi bu yüzden gereklidir.

## SPI, I²C ve UART karşılaştırması

| Özellik | SPI | I²C | UART |
|---|---|---|---|
| Tipik hat sayısı | 4 veya daha fazla | 2 | 2 |
| Saat hattı | Var | Var | Yok |
| Full-duplex | Evet | Hayır | Evet |
| Cihaz adresleme | Genellikle CS ile | Protokol içinde | Doğrudan yok |
| Hız | Çok yüksek | Orta | Orta |

SPI; yüksek örnekleme hızlı ADC’ler, ekranlar ve harici bellekler için güçlü bir seçimdir. Buna karşılık pin sayısının kritik olduğu projelerde I²C daha avantajlı olabilir. En doğru protokol, yalnızca hız yarışını kazanan değil; pin sayısı, kablo uzunluğu, cihaz sayısı ve hata toleransı gibi proje ihtiyaçlarını birlikte karşılayandır.

![spi-protokolu-yuksek-96](/img/spi-protokolu-yuksek-96.svg)

