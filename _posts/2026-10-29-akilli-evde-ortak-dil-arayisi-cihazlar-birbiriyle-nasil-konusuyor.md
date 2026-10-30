---
layout: post
title: "Akıllı Evde Ortak Dil Arayışı: Cihazlar Birbiriyle Nasıl Konuşuyor?"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı ev
  - interoperability
  - matter
  - zigbee
  - mqtt
  - iot
toc: true
image: /img/akilli-evde-ortak-16.png
---

Akıllı ampulünüz başka bir markanın hareket sensörünü görmüyor, robot süpürgeniz sesli asistana küsmüş, termostatınız ise yalnızca kendi uygulamasıyla konuşuyor olabilir. Akıllı ev ekosistemlerinde **birlikte çalışabilirlik**, farklı üreticilere ait cihazların ortak bir sistem içinde veri paylaşabilmesi ve birbirini kontrol edebilmesidir. Amaç, evinizi uygulama mezarlığına dönüştürmeden bütün cihazları uyumlu bir ekip hâline getirmektir.

``

## Birlikte çalışabilirlik neden zor?

Her akıllı cihaz fiziksel bağlantı, iletişim protokolü ve veri modeli olmak üzere birkaç katmanda çalışır. Wi-Fi veya Thread cihazın ağa nasıl bağlandığını; MQTT, Zigbee ya da Matter mesajların nasıl taşındığını; veri modeli ise bir mesajdaki `temperature` değerinin ne anlama geldiğini belirler.

İki cihazın yalnızca aynı kablosuz teknolojiyi kullanması yeterli değildir. İletişimi basitleştirerek şöyle gösterebiliriz:

$$Başarı = Bağlantı \times Protokol\ Uyumu \times Anlamsal\ Uyum$$

Katmanlardan herhangi biri sıfırsa toplam başarı da sıfır olur. Örneğin iki cihaz Wi-Fi kullanabilir, ancak biri üreticiye özel bulut API'siyle, diğeri yerel MQTT mesajlarıyla çalışıyorsa doğrudan anlaşamazlar.

| Teknoloji | Temel rolü | Güçlü yanı | Sınırlaması |
|---|---|---|---|
| Wi-Fi | IP tabanlı bağlantı | Yüksek hız ve yaygınlık | Daha fazla enerji tüketimi |
| Zigbee | Düşük güçlü örgü ağ | Sensörler için verimli | Genellikle köprü gerektirir |
| Thread | IP tabanlı örgü ağ | Yerel ve dayanıklı iletişim | Sınır yönlendirici ister |
| Matter | Ortak uygulama standardı | Markalar arası kontrol | Her cihaz özelliğini kapsamayabilir |
| MQTT | Mesajlaşma protokolü | Hafif ve esnek otomasyon | Ortak veri modeli zorunlu değildir |

## Entegrasyon yöntemleri

En kolay yöntem, cihazları Google Home, Apple Home, Amazon Alexa veya SmartThings gibi merkezi bir platformda toplamaktır. Platform, üreticilerin bulut servislerine bağlanarak farklı API'leri ortak bir arayüz altında sunar. Kurulumu rahattır; fakat internet kesintileri, abonelik değişiklikleri ve servislerin kapanması sistemi etkileyebilir.

İkinci yöntem **yerel merkez** kullanmaktır. Home Assistant, openHAB veya Hubitat gibi çözümler cihazlarla ev ağı üzerinden haberleşebilir. Böylece komutlar uzak bir sunucuya gidip dönmez. Yaklaşık tepki süresi şu şekilde düşünülebilir:

$$T_{toplam}=T_{ağ}+T_{işleme}+T_{bulut}$$

Yerel otomasyonda $T_{bulut}$ ortadan kalktığı için ışıklar daha hızlı yanar ve internet yokken de çalışabilir. Bunun bedeli, biraz daha fazla kurulum ve bakım gerektirmesidir.

Üçüncü yöntem ise köprü veya adaptör kullanmaktır. Köprü, farklı protokoller arasında tercümanlık yapar. Örneğin bir Zigbee sensöründen gelen hareket bilgisi MQTT konusuna çevrilebilir. Home Assistant için basit bir otomasyon şöyle tanımlanabilir:

```yaml
alias: Koridorda hareket algılanınca ışığı aç
trigger:
  - platform: state
    entity_id: binary_sensor.koridor_hareket
    to: 'on'
action:
  - service: light.turn_on
    target:
      entity_id: light.koridor
```

Bu yapı, sensör ve ampul farklı markalara ait olsa bile platformdaki standart varlık kimlikleri üzerinden çalışır. `trigger` olayı izler, `action` ise gerçekleşecek komutu belirtir.

## Matter her şeyi çözüyor mu?

Matter; Apple, Google, Amazon, Samsung ve çok sayıda üreticinin desteklediği ortak bir standarttır. IP tabanlı çalışır, cihazların güvenli biçimde eşleştirilmesini ve birden fazla ekosisteme bağlanmasını kolaylaştırır. **Multi-Admin** özelliği sayesinde aynı ampul hem Apple Home hem de Google Home tarafından yönetilebilir.

Yine de Matter sihirli değnek değildir. Eski cihazlar destek almayabilir; kamera veya robot süpürge gibi ürünlerin gelişmiş özellikleri standartta eksik kalabilir. Üreticiler ayrıca bazı işlevleri kendi uygulamalarına özel tutabilir.

## Sağlam bir ekosistem için öneriler

Cihaz satın alırken yalnızca kutudaki “akıllı” ifadesine değil; yerel API, Matter, Thread, Zigbee ve Home Assistant desteğine bakın. Kritik otomasyonları buluta bağımlı bırakmayın, cihazları ayrı bir IoT ağına yerleştirin ve düzenli güncelleme uygulayın. Mümkünse önce küçük bir uyumluluk haritası hazırlayın. Böylece eviniz, birbirine bağıran cihazlar topluluğu değil, aynı dili konuşan gerçek bir otomasyon sistemi olur.

![akilli-evde-ortak-16](/img/akilli-evde-ortak-16.svg)

