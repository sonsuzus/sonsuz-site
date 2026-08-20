---
layout: post
title: "WebSocket Protokolü: HTTP Sınırlarını Aşan Gerçek Zamanlı İletişim"
math: true
categories: 
  - Bilgi
tags: 
  - websocket
  - http
  - gerçek zamanlı iletişim
toc: true
---

Bir sohbet uygulamasında yeni mesajın sayfayı yenilemeden ekrana düşmesi, borsa fiyatlarının anlık değişmesi veya çok oyunculu bir oyunda rakibinizin hareketini gecikmeden görmeniz tesadüf değildir. Bu deneyimlerin arkasında çoğunlukla WebSocket bulunur. WebSocket, istemci ile sunucu arasında uzun ömürlü ve çift yönlü bir iletişim kanalı kurarak klasik web istek-cevap döngüsünün sınırlarını aşar.
``
## HTTP neden tek başına yeterli değildir?

HTTP doğası gereği **istemci başlatmalı** bir protokoldür: Tarayıcı istek gönderir, sunucu yanıt üretir ve işlem biter. Sunucunun istemciye kendiliğinden veri göndermesi gerektiğinde geleneksel yaklaşım *polling* olur. İstemci belirli aralıklarla “Yeni veri var mı?” diye sorar. Veri yoksa bile ağ trafiği, işlem maliyeti ve gecikme oluşur.

Bir istemci her $T$ saniyede sorgu yapıyorsa, yeni bir olayın kullanıcıya ulaşması için ortalama bekleme süresi yaklaşık olarak $T/2$ olur. Örneğin $T=10$ saniye seçildiğinde ortalama gecikme $5$ saniyedir. Daha sık sorgulamak gecikmeyi azaltır; fakat gereksiz istek sayısını yükseltir. WebSocket bu denge problemini sürekli açık bir bağlantıyla çözer.

| Özellik | HTTP Polling | Long Polling | WebSocket |
|---|---|---|---|
| Bağlantı modeli | Her sorguda yeni istek | Yanıt gelene kadar istek açık | Tek, kalıcı bağlantı |
| İletişim yönü | İstemci → sunucu | Temelde istemci → sunucu | Çift yönlü |
| Gecikme | Sorgu aralığına bağlı | Orta | Genellikle düşük |
| Başlık maliyeti | Her istekte tekrar eder | Sık tekrar eder | Başlangıçtan sonra düşüktür |

## HTTP'den WebSocket'e geçiş: Handshake

WebSocket bağlantısı aslında bir HTTP isteğiyle başlar. Tarayıcı, sunucuya `Upgrade: websocket` başlığını içeren özel bir istek yollar. Sunucu uygunsa `101 Switching Protocols` yanıtını verir. Bu noktadan sonra bağlantı artık sıradan HTTP yanıtları taşımaz; WebSocket çerçeveleri (*frame*) üzerinden mesaj alışverişi yapılır.

Bu tasarım akıllıcadır: Başlangıçta mevcut HTTP altyapısı, alan adları ve çoğu proxy ile uyumluluk korunur. Ancak yükseltme tamamlandıktan sonra hem istemci hem sunucu istediği anda mesaj gönderebilir. Yani bağlantı bir telefon görüşmesi gibidir; karşı tarafın yeniden aramasını beklemeniz gerekmez.

## Tarayıcı tarafında temel kullanım

Aşağıdaki örnek, bir WebSocket sunucusuna bağlanır, bağlantı açıldığında mesaj yollar ve gelen veriyi ekrana yazar:

```javascript
const socket = new WebSocket("wss://example.com/chat");

socket.addEventListener("open", () => {
  console.log("Bağlantı kuruldu");
  socket.send(JSON.stringify({ type: "message", text: "Merhaba!" }));
});

socket.addEventListener("message", (event) => {
  const data = JSON.parse(event.data);
  console.log("Sunucudan geldi:", data);
});

socket.addEventListener("close", () => {
  console.log("Bağlantı kapandı; yeniden bağlanma planlanabilir.");
});
```

Buradaki `wss://`, HTTPS'nin WebSocket karşılığı olan şifreli bağlantıyı ifade eder. Üretim ortamında özellikle oturum bilgileri veya kullanıcı mesajları taşınıyorsa `ws://` yerine mutlaka `wss://` tercih edilmelidir.

## Mesajlar, kalp atışları ve dayanıklılık

WebSocket mesajları metin veya ikili veri olabilir. JSON, olay türü ve veri içeriğini birlikte taşıdığı için yaygındır. Örneğin `{ "type": "typing", "userId": 42 }` gibi bir yapı, istemcinin mesajın nasıl işleneceğini anlamasını kolaylaştırır.

Kalıcı bağlantı, sonsuza kadar sağlıklı kalacağı anlamına gelmez. Mobil ağ değişimleri, uyuyan cihazlar ve proxy zaman aşımları bağlantıyı koparabilir. Bu nedenle uygulamalar **heartbeat** (ping/pong) ve artan beklemeli yeniden bağlanma stratejileri kullanır. Örneğin $d_n = \min(1000 \times 2^n, 30000)$ formülüyle her başarısız denemede bekleme artırılabilir; üst sınır ise kullanıcıyı gereksiz yere bekletmez.

WebSocket; sohbet, canlı bildirim, ortak doküman düzenleme, telemetri panelleri ve oyunlar için güçlü bir seçimdir. Yine de her API çağrısını WebSocket'e taşımak gerekmez. Kaynak listeleme, form gönderme ve önbelleklenebilir verilerde HTTP hâlâ sade, görünür ve etkili bir çözümdür. Doğru protokol, “anlık olma” ihtiyacının gerçekten var olduğu yerde seçilmelidir.
