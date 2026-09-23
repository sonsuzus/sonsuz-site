---
layout: post
title: "UART ve Seri Haberleşme: İki Cihazın En Sade Sohbet Protokolü"
math: true
categories: 
  - Bilgi
tags: 
  - uart
  - seri haberleşme
  - mikrodenetleyici
  - gömülü sistemler
  - elektronik
  - protokoller
toc: true
---

Bir mikrodenetleyicinin sensörle, bilgisayarla veya başka bir kartla konuşmasını sağlamanın en kolay yollarından biri UART’tır. Karmaşık ağ katmanları, IP adresleri ya da bağlantı pazarlıkları yoktur; iki taraf doğru hızda dinler ve bitler sırayla yola çıkar. Kısacası UART, elektronik dünyasının “aynı dili ve tempoyu biliyorsak konuşabiliriz” anlaşmasıdır.

``

## UART tam olarak nedir?

UART, **Universal Asynchronous Receiver/Transmitter** ifadesinin kısaltmasıdır. Aslında fiziksel bir kablo standardından çok, paralel veriyi seri bitlere dönüştüren ve gelen seri bitleri yeniden paralel veriye çeviren donanım birimidir.

“Asenkron” kelimesi, cihazların ortak bir saat hattı kullanmadığını belirtir. SPI’daki gibi ayrıca bir clock kablosu bulunmaz. Bunun yerine iki cihaz önceden aynı **baud rate**, veri biti, parity ve stop biti ayarlarında anlaşır.

| Özellik | UART | SPI | I²C |
|---|---|---|---|
| Saat hattı | Yok | Var | Var |
| Tipik veri hattı | TX ve RX | MOSI ve MISO | SDA |
| Cihaz sayısı | Genellikle iki | Birden fazla | Birden fazla |
| Karmaşıklık | Düşük | Orta | Orta |
| Adresleme | Yok | Chip Select ile | Adresle |

## TX, RX ve GND üçlüsü

Temel UART bağlantısında üç hat yeterlidir:

- **TX:** Cihazın veri gönderdiği hat.
- **RX:** Cihazın veri aldığı hat.
- **GND:** İki cihazın ortak elektriksel referansı.

Bağlantı çapraz yapılır: Birinci cihazın TX pini ikinci cihazın RX pinine, RX pini ise ikinci cihazın TX pinine gider. TX’i TX’e bağlamak, iki kişinin aynı anda konuşup kimsenin dinlememesine benzer.

Gerilim seviyeleri de önemlidir. 3,3 V ile çalışan bir mikrodenetleyiciye doğrudan 5 V sinyal uygulamak zarar verebilir. Ayrıca UART mantığı ile RS-232 elektrik standardı aynı değildir; klasik RS-232 daha yüksek ve terslenmiş gerilimler kullanabilir. Böyle durumlarda seviye dönüştürücü gerekir.

## Bir karakter nasıl yolculuk eder?

UART hattı boşta genellikle lojik 1 seviyesindedir. İletim bir **start biti** ile başlar, veri bitleriyle devam eder ve bir veya daha fazla **stop biti** ile biter. Yaygın `8N1` ayarı şunları söyler:

| Sembol | Anlamı |
|---|---|
| 8 | Sekiz veri biti |
| N | Parity biti yok |
| 1 | Bir stop biti |

Bir çerçevenin toplam bit sayısı yaklaşık olarak:

$$N_{çerçeve}=1+N_{veri}+N_{parity}+N_{stop}$$

`8N1` için sonuç $1+8+0+1=10$ bittir. Baud rate 9600 ise teorik karakter hızı:

$$R_{karakter}=\frac{9600}{10}=960\ \text{karakter/saniye}$$

Yani “9600 baud” her zaman saniyede 9600 karakter demek değildir; çerçeveleme bitleri de bant genişliği tüketir.

## Baud rate neden iki tarafta aynı olmalı?

Alıcı, start bitini görünce veri bitlerini belirli zaman aralıklarında örnekler. Bir bitin süresi:

$$T_{bit}=\frac{1}{baud}$$

115200 baud için bu süre yaklaşık $8{,}68\ \mu s$ olur. Saatler fazla farklıysa örnekleme noktası giderek kayar; sonuçta anlamsız karakterler, eksik paketler ve terminalde modern sanat eserleri belirir.

## Mikrodenetleyicide basit kullanım

Aşağıdaki Arduino kodu, bilgisayardan gelen karakterleri okuyup geri yollar. Bu davranışa **echo** denir ve bağlantı testi için oldukça kullanışlıdır.

```cpp
void setup() {
  Serial.begin(9600); // UART birimini 9600 baud ile başlatır
}

void loop() {
  if (Serial.available() > 0) {
    char gelen = Serial.read();
    Serial.print("Alindi: ");
    Serial.println(gelen);
  }
}
```

Seri monitör de 9600 baud ve uygun satır sonu ayarıyla açılmalıdır. Aksi hâlde kod doğru olsa bile iletişim bozuk görünebilir.

## Daha güvenilir mesajlar tasarlamak

UART yalnızca bitlerin taşınmasını sağlar; mesajın nerede başladığını veya ne anlama geldiğini kendiliğinden bilmez. Uygulama seviyesinde örneğin `SICAKLIK:24.5\n` biçimi kullanılabilir. Daha sağlam sistemlerde başlangıç baytı, uzunluk alanı ve checksum eklenir.

Basit bir checksum şöyle tanımlanabilir:

$$C=\left(\sum_{i=1}^{n} veri_i\right)\bmod 256$$

Alıcı aynı hesabı yapıp gelen checksum ile karşılaştırır. Değerler farklıysa aktarım sırasında hata oluşmuş olabilir.

UART; düşük maliyeti, kolay hata ayıklanması ve hemen her mikrodenetleyicide bulunması sayesinde hâlâ vazgeçilmezdir. TX ile RX’i çaprazla, GND’yi unutma, ayarları eşitle ve sohbet başlasın!
