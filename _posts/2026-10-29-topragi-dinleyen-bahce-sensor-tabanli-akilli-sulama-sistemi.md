---
layout: post
title: "Toprağı Dinleyen Bahçe: Sensör Tabanlı Akıllı Sulama Sistemi"
math: true
categories: 
  - Proje
tags: 
  - akıllı sulama
  - bahçe otomasyonu
  - nem sensörü
  - arduino
  - iot
  - sensörler
toc: true
image: /img/topragi-dinleyen-bahce-48.png
---

Bitkileri düzenli sulamak kolay görünür; ancak doğru miktarı doğru zamanda vermek bambaşka bir meseledir. Hava sıcaklığı, yağış, toprak türü ve bitkinin gelişim dönemi su ihtiyacını sürekli değiştirir. Sensör tabanlı akıllı sulama sistemi, sabit saatlere bağlı kalmak yerine toprağın gerçek durumunu ölçer ve yalnızca ihtiyaç olduğunda pompayı çalıştırır. Böylece hem bitkiler hem de su faturası rahat bir nefes alır.

``

## Sistemin Temel Mantığı

Bir nem sensörü, toprağın elektriksel özelliklerini ölçerek mikrodenetleyiciye analog bir değer gönderir. Arduino veya ESP32 gibi bir kart bu değeri okur, önceden belirlenen eşiklerle karşılaştırır ve röle üzerinden su pompasını kontrol eder.

Sistemin karar zinciri şöyledir:

1. Toprak nemi ölçülür.
2. Ham sensör değeri filtrelenir.
3. Değer, nem yüzdesine dönüştürülür.
4. Nem alt sınırın altındaysa pompa açılır.
5. Yeterli neme ulaşıldığında pompa kapatılır.

Sensörün kuru topraktaki değeri $R_{kuru}$, ıslak topraktaki değeri $R_{islak}$ ve anlık ölçüm $R$ olsun. Yaklaşık nem yüzdesi şu şekilde hesaplanabilir:

$$
Nem(\%) = \frac{R_{kuru}-R}{R_{kuru}-R_{islak}} \times 100
$$

Bazı sensörlerde ölçüm yönü ters olabilir. Bu nedenle formülü ezberlemek yerine kalibrasyon sonuçlarına göre uyarlamak gerekir.

## Hangi Nem Sensörü?

Bahçe projelerinde çoğunlukla dirençli veya kapasitif sensörler kullanılır.

| Özellik | Dirençli sensör | Kapasitif sensör |
|---|---|---|
| Ölçüm yöntemi | İki prob arasındaki iletkenlik | Dielektrik değişimi |
| Fiyat | Daha düşük | Biraz daha yüksek |
| Korozyon | Yüksek | Düşük |
| Uzun süreli kullanım | Zayıf | Daha uygun |
| Bahçe otomasyonu | Deneme projeleri | Kalıcı sistemler |

Dirençli modeller ekonomik olsa da problardan geçen akım zamanla oksitlenmeye yol açar. Uzun ömürlü bir sistem için kapasitif sensör genellikle daha iyi seçimdir. Sensör gövdesinin elektronik kısmı toprağa gömülmemeli ve yağmurdan korunmalıdır.

## Eşik Değil, Histerezis

Pompayı yalnızca tek bir eşik değeriyle yönetmek sorun çıkarabilir. Nem yüzde 39 ile 40 arasında dalgalanırsa röle sürekli açılıp kapanabilir. Bunun yerine iki farklı eşik kullanılır:

- Nem yüzde 35'in altına düşünce pompayı aç.
- Nem yüzde 55'e çıkınca pompayı kapat.

Bu iki değer arasındaki fark histerezis olarak adlandırılır. Matematiksel olarak açma eşiği $T_a$, kapatma eşiği $T_k$ ise güvenli çalışma için $T_a < T_k$ olmalıdır.

## Arduino ile Örnek Kontrol

Aşağıdaki kod sensörü okur, değeri yüzdeye çevirir ve histerezis kullanarak pompayı yönetir:

```cpp
const int sensorPin = A0;
const int relayPin = 7;
const int dryValue = 820;
const int wetValue = 360;

bool pumpRunning = false;

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);
}

void loop() {
  int rawValue = analogRead(sensorPin);
  int moisture = map(rawValue, dryValue, wetValue, 0, 100);
  moisture = constrain(moisture, 0, 100);

  if (moisture < 35) pumpRunning = true;
  if (moisture > 55) pumpRunning = false;

  digitalWrite(relayPin, pumpRunning ? HIGH : LOW);
  delay(2000);
}
```

`map` fonksiyonu kalibrasyon değerlerini yüzde aralığına dönüştürür. `constrain` ise hesaplanan sonucu 0 ile 100 arasında tutar. Röle modülünüz düşük seviyede tetikleniyorsa `HIGH` ve `LOW` mantığını ters çevirmek gerekebilir.

## Daha Güvenilir Kararlar

Tek bir ölçüme güvenmek yerine son beş ölçümün ortalamasını almak ani sıçramaları azaltır:

$$
\bar{x} = \frac{x_1+x_2+x_3+x_4+x_5}{5}
$$

Ayrıca pompaya azami çalışma süresi tanımlanmalıdır. Sensör arızalanırsa veya su deposu boşalırsa pompanın saatlerce çalışması önlenir. Depo seviye sensörü, yağmur sensörü ve akış ölçer eklenerek sistem daha güvenli hâle getirilebilir. ESP32 kullanıldığında ölçümler telefondan izlenebilir ve geçmiş veriler grafikleştirilebilir.

Başarılı bir akıllı sulama sistemi yalnızca toprağın kuru olduğunu fark etmez; ölçümü doğrular, dalgalanmayı filtreler ve güvenli sınırlar içinde karar verir. Kısacası bahçeye otomasyon eklemek, pompaya zamanlayıcı bağlamaktan çok daha akıllı bir iştir.

![topragi-dinleyen-bahce-48](/img/topragi-dinleyen-bahce-48.svg)

