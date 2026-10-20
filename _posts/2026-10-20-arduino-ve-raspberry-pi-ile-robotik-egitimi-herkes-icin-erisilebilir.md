---
layout: post
title: "Arduino ve Raspberry Pi ile Robotik Eğitimi Herkes İçin Erişilebilir"
math: true
categories: 
  - Bilgi
tags: 
  - arduino
  - raspberry pi
  - robotik
  - açık kaynak
  - stem
  - elektronik
toc: true
image: /img/arduino-ve-raspberry-56.png
---

Bir zamanlar robot geliştirmek; pahalı laboratuvarlara, özel üretim devrelere ve kalın mühendislik kitaplarına erişmeyi gerektiriyordu. Arduino ve Raspberry Pi gibi açık kaynaklı donanım platformları ise bu tabloyu önemli ölçüde değiştirdi. Öğrenciler artık birkaç sensör, motor ve internetten erişilebilen örneklerle çalışan bir robot geliştirebiliyor. Böylece robotik eğitimi, yalnızca uzmanların bulunduğu laboratuvarlardan çıkarak sınıflara, atölyelere ve hatta mutfak masalarına kadar ulaşıyor.

``

## Açık kaynak erişilebilirliği nasıl artırıyor?

Açık kaynaklı donanımda devre şemaları, yazılım araçları, kütüphaneler ve örnek projeler toplulukla paylaşılır. Kullanıcı yalnızca hazır bir ürünü tüketmez; sistemin nasıl çalıştığını inceleyebilir, değiştirebilir ve yeniden üretebilir. Bu yaklaşım erişilebilirliği üç yönden güçlendirir:

- **Ekonomik erişim:** Düşük maliyetli kartlar ve uyumlu yan ürünler kullanılabilir.
- **Bilgiye erişim:** Ücretsiz belgeler, videolar ve topluluk forumları öğrenme sürecini destekler.
- **Deneysel erişim:** Öğrenci, hata yapmaktan korkmadan devreyi ve kodu değiştirebilir.

Robotik sistemlerin temelinde algılama, karar verme ve hareket etme döngüsü bulunur. Sensör çevreden veri toplar, kontrol birimi bu veriyi işler ve aktüatörler fiziksel tepki üretir:

$$Algılama \rightarrow Karar \rightarrow Hareket$$

Örneğin ultrasonik sensörün gönderdiği ses dalgasının geri dönüş süresi $t$, ses hızı $v$ ve engel uzaklığı $d$ arasındaki ilişki şöyledir:

$$d = \frac{v \cdot t}{2}$$

İkiye bölünmesinin nedeni, ölçülen sürenin sesin engele gidişini ve geri dönüşünü birlikte içermesidir. Böyle bir formül, fizik bilgisini doğrudan çalışan bir robot üzerinde görünür hâle getirir.

## Arduino mu, Raspberry Pi mı?

Her iki platform da robotik eğitiminde değerlidir; ancak aynı işi yapmak üzere tasarlanmamıştır.

| Özellik | Arduino | Raspberry Pi |
|---|---|---|
| Yapı | Mikrodenetleyici kartı | Tek kart bilgisayar |
| İşletim sistemi | Yok | Genellikle Linux |
| Başlangıç süresi | Neredeyse anlık | İşletim sistemi açılışı gerekir |
| Güç tüketimi | Düşük | Daha yüksek |
| Uygun görevler | Sensör, motor, gerçek zamanlı kontrol | Görüntü işleme, yapay zekâ, ağ uygulamaları |
| Başlangıç zorluğu | Elektronik odaklı ve sade | Yazılım olanakları geniş, yapılandırması daha ayrıntılı |

![arduino-ve-raspberry-56](/img/arduino-ve-raspberry-56.svg)


Arduino, çizgi izleyen veya engelden kaçan bir robot için güçlü bir başlangıçtır. Raspberry Pi ise kamera görüntüsünden nesne tanıyan ya da web arayüzüyle yönetilen robotlarda öne çıkar. İki kart birlikte de kullanılabilir: Raspberry Pi yüksek seviyeli kararları verirken Arduino motorları zamanlamaya duyarlı biçimde kontrol edebilir.

## Küçük bir robot refleksi

Aşağıdaki Arduino kodu, bir dijital sensör engel algıladığında motor kontrol çıkışını durdurur. Bu örnek, algılama-karar-hareket döngüsünün en sade hâlidir:

```cpp
const int sensorPin = 2;
const int motorPin = 9;

void setup() {
  pinMode(sensorPin, INPUT);
  pinMode(motorPin, OUTPUT);
}

void loop() {
  bool engelVar = digitalRead(sensorPin);

  if (engelVar) {
    analogWrite(motorPin, 0);    // Motoru durdur
  } else {
    analogWrite(motorPin, 180);  // Orta-yüksek hızda ilerle
  }

  delay(20); // Sensörü saniyede yaklaşık 50 kez kontrol et
}
```

Kod yalnızca programlamayı değil, giriş-çıkış mantığını ve geri beslemeyi de öğretir. Öğrenci `180` değerini değiştirerek hızın davranışa etkisini gözlemleyebilir. Elbette gerçek bir motor doğrudan karta bağlanmamalı; motor sürücü devresi ve uygun güç kaynağı kullanılmalıdır.

## Erişilebilirlik yalnızca düşük fiyat değildir

Ucuz kartlar tek başına eşit eğitim fırsatı oluşturmaz. İnternet erişimi, yerelleştirilmiş içerik, öğretmen eğitimi, yedek parça bulunabilirliği ve güvenli çalışma ortamı da önemlidir. Ayrıca açık kaynak projelerde belgelerin güncelliği değişebilir ve Raspberry Pi gibi kartların toplam maliyetine güç kaynağı, hafıza kartı ve çevre birimleri eklenebilir.

Buna rağmen bu platformların en büyük katkısı, öğrenciyi pasif kullanıcıdan üreticiye dönüştürmesidir. Bir LED’i yakmakla başlayan yolculuk; otonom araçlara, tarım robotlarına veya yapay zekâ destekli sistemlere uzanabilir. Robotik böylece ulaşılmaz bir gelecek teknolojisi değil, parçalarına ayrılıp anlaşılabilen ve yeniden tasarlanabilen bir öğrenme alanı hâline gelir.
