---
layout: post
title: "Mobil Uygulamadan Akıllı Prize: IoT Haberleşme Mimarisinin Perde Arkası"
math: true
categories: 
  - Bilgi
tags: 
  - iot
  - mobil uygulama
  - mqtt
  - akıllı ev
  - websocket
  - cihaz entegrasyonu
toc: true
image: /img/mobil-uygulamadan-akilli-19.png
---

Telefonunuzdaki düğmeye dokunduğunuzda akıllı prizin anında kapanması basit bir işlem gibi görünür. Oysa perde arkasında mobil uygulama, bulut servisi, mesaj aracısı ve fiziksel cihaz arasında küçük bir iletişim orkestrası çalışır. Üstelik internet kesintileri, güvenlik, gecikme ve cihaz durumunun doğru gösterilmesi gibi sorunların da yönetilmesi gerekir.

``

## Temel mimari: Kim, kiminle konuşuyor?

Tipik bir akıllı priz sistemi dört ana parçadan oluşur:

1. **Mobil uygulama:** Kullanıcının komut verdiği ve priz durumunu gördüğü arayüzdür.
2. **Backend API:** Kimlik doğrulama, cihaz sahipliği ve komut yetkilendirmesini yönetir.
3. **Mesaj aracısı:** MQTT gibi bir protokolle komutları cihazlara dağıtır.
4. **IoT cihazı:** Wi-Fi üzerinden internete bağlanır, komutları işler ve röleyi kontrol eder.

Mobil uygulama çoğu zaman prize doğrudan bağlanmaz. Bunun yerine uygulama komutu backend'e gönderir; backend de mesaj aracısı üzerinden cihaza iletir. Böylece cihazın IP adresini bilmek gerekmez ve farklı ağlardaki cihazlar güvenli biçimde yönetilebilir.

```text
Mobil Uygulama -> HTTPS API -> MQTT Broker -> Akıllı Priz
Mobil Uygulama <- WebSocket <- Backend    <- Durum Mesajı
```

Burada MQTT Broker, postane gibi düşünülebilir. Backend mesajı belirli bir konuya, örneğin `devices/priz-42/command` kanalına bırakır. Yalnızca bu kanala abone olan priz mesajı teslim alır.

## Neden yalnızca HTTP kullanılmıyor?

HTTP istek-cevap modelinde çalışırken MQTT ve WebSocket sürekli veya uzun ömürlü bağlantıları destekler. Cihazın durum değişikliğini telefona hızlıca bildirmek için bu özellik önemlidir.

| Teknoloji | Kullanım alanı | Güçlü yanı | Sınırlaması |
|---|---|---|---|
| HTTPS | Uygulamadan backend'e komut | Güvenli ve yaygın | Gerçek zamanlı bildirim için yetersiz |
| MQTT | Backend ile cihaz iletişimi | Hafif, düşük bant genişliği | Broker altyapısı gerektirir |
| WebSocket | Backend'den uygulamaya durum aktarımı | Çift yönlü ve hızlı | Bağlantı yönetimi ister |
| Bluetooth | İlk kurulum ve yerel kontrol | İnternetsiz çalışabilir | Kısa menzillidir |

Toplam hissedilen gecikme kabaca şu şekilde modellenebilir:

$$T_{toplam} = T_{uygulama} + T_{api} + T_{broker} + T_{cihaz} + T_{geri\ bildirim}$$

Her adım yalnızca birkaç milisaniye sürse bile zayıf Wi-Fi veya yoğun sunucu trafiği toplam süreyi artırabilir.

## Bir açma komutunun yolculuğu

Kullanıcı düğmeye bastığında uygulama önce erişim belirtecini kullanarak backend'e istek gönderir:

```dart
final response = await http.post(
  Uri.parse('https://api.example.com/devices/priz-42/commands'),
  headers: {'Authorization': 'Bearer $token'},
  body: jsonEncode({'action': 'turn_on'}),
);
```

Bu kod yalnızca komutun kabul edilmesini ister; prizin gerçekten açıldığını varsaymaz. Backend kullanıcının bu cihaza sahip olduğunu doğrular ve MQTT mesajını yayımlar:

```javascript
mqtt.publish('devices/priz-42/command', JSON.stringify({
  action: 'turn_on',
  commandId: 'cmd-781'
}), { qos: 1 });
```

`commandId`, komutun sonucunu takip etmeyi sağlar. `QoS 1` ise mesajın en az bir kez teslim edilmesini hedefler. Aynı mesaj iki kez gelebileceğinden cihazın işlemleri **idempotent**, yani tekrarlandığında zararsız olacak şekilde tasarlanması gerekir.

Priz röleyi açtıktan sonra `devices/priz-42/state` konusuna güncel durumunu yollar. Backend bu olayı WebSocket ile mobil uygulamaya aktarır. Uygulamadaki düğme ancak onay geldikten sonra kesin olarak “açık” durumuna geçirilir.

## Güvenlik ve çevrimdışı senaryolar

Her cihazın benzersiz kimliği ve sertifikası olmalıdır. MQTT bağlantısı TLS ile şifrelenmeli; kullanıcı belirteçleri güvenli depolamada tutulmalıdır. Bir cihaz yalnızca kendi komut ve durum kanallarına erişebilmelidir.

Cihaz çevrimdışıysa uygulama bunu açıkça göstermelidir. Komutu sonsuza kadar bekletmek yerine zaman aşımı uygulanabilir. Yerel ağ keşfi veya Bluetooth desteği eklenirse internet yokken sınırlı kontrol de sağlanabilir.

Başarılı bir IoT mimarisi yalnızca “aç” mesajını göndermekten ibaret değildir. Komutun yetkilendirilmesi, teslim edilmesi, uygulanması ve sonucunun doğrulanması gerekir. Telefon ekranındaki küçücük düğmenin arkasında güvenilir bir dağıtık sistem vardır; akıllı priz ise bu sistemin röle kullanan en çalışkan üyesidir.

![mobil-uygulamadan-akilli-19](/img/mobil-uygulamadan-akilli-19.svg)

