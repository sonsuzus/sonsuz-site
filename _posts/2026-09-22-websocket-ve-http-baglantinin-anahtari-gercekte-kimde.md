---
layout: post
title: "WebSocket ve HTTP: Bağlantının Anahtarı Gerçekte Kimde?"
math: true
categories: 
  - Bilgi
tags: 
  - websocket
  - http
  - tcp
  - ağ-programlama
  - istemci-sunucu
  - web
toc: true
image: /img/websocket-ve-http-81.png
---

Bir tarayıcı sunucuya bağlandığında bağlantıyı kim yönetir: istemci mi, sunucu mu? HTTP ile WebSocket karşılaştırılırken sıkça “HTTP’de istemci, WebSocket’te iki taraf kontrol sahibidir” denir. Bu kullanışlı ama eksik bir özettir. Gerçekte TCP bağlantısının iki ucu, protokol kuralları, proxy zaman aşımı ve uygulama yaşam döngüsü birlikte söz sahibidir.


![websocket-ve-http-81](/img/websocket-ve-http-81.svg)

``

## Önce katmanları ayıralım

HTTP ve WebSocket çoğunlukla TCP üzerinde çalışan **uygulama katmanı protokolleridir**. TCP bağlantısını genellikle istemci başlatır; sunucu ise belirli bir portta bağlantı bekler. Bağlantı kurulduktan sonra ortaya iki uçlu bir kanal çıkar:

$$
TCP\ bağlantısı = (istemci\ IP, istemci\ port, sunucu\ IP, sunucu\ port)
$$

Dolayısıyla bağlantının tek bir sahibi yoktur. Her iki taraf da veri gönderebilir ve bağlantıyı kapatabilir. Asıl fark, uygulama protokolünün bu kanal üzerinde taraflara **ne zaman mesaj gönderebilme izni verdiğidir**.

## HTTP: Sözü istemci başlatır

Klasik HTTP modeli istek-cevap düzenindedir. İstemci bir istek yollar, sunucu buna yanıt verir:

$$
İstek \rightarrow Yanıt
$$

Sunucu, ortada bir istek yokken aynı HTTP etkileşimi içinde keyfî biçimde yeni bir yanıt başlatmaz. Bu nedenle iletişim akışının mantıksal tetikleyicisi istemcidir. Ancak bu, her yanıttan sonra TCP bağlantısının kapandığı anlamına gelmez. HTTP/1.1 `keep-alive` ile bağlantıyı yeniden kullanabilir; HTTP/2 ise tek bağlantı üzerinde birden fazla akışı eşzamanlı taşıyabilir.

HTTP’nin “durumsuz” olması da bağlantısız olması demek değildir. Durumsuzluk, her isteğin işlenmesi için gereken bağlamı taşıması gerektiğini anlatır. Oturum bilgisi cookie, token veya sunucu tarafındaki bir kayıtla ayrıca tutulabilir.

## WebSocket: El sıkışmadan sonra çift yönlü kanal

WebSocket bağlantısı çoğunlukla bir HTTP isteğiyle başlar. İstemci protokol yükseltmesi ister:

```http
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
```

Sunucu kabul ederse `101 Switching Protocols` yanıtını verir. Bu noktadan sonra iletişim HTTP istek-cevap kalıbından çıkar ve WebSocket çerçeveleriyle devam eder. Artık sunucu yeni bir istemci isteğini beklemeden mesaj gönderebilir. Sohbet mesajları, oyun konumları ve canlı fiyat akışları bu modele uygundur.

| Özellik | HTTP | WebSocket |
|---|---|---|
| İletişimi başlatan | Genellikle istemci | İlk bağlantıyı istemci |
| Mesaj akışı | İstek-cevap | Tam çift yönlü |
| Sunucudan anlık gönderim | Ek teknik gerekir | Doğrudan mümkündür |
| Bağlantı süresi | Kısa veya yeniden kullanılan | Genellikle uzun ömürlü |
| İdeal kullanım | API, sayfa ve dosya aktarımı | Sohbet, oyun, canlı veri |

## Küçük bir WebSocket örneği

Aşağıdaki Node.js sunucusu, bağlantı kuran istemciye periyodik olarak saat gönderir. Burada sunucu, istemciden yeni bir istek beklemeden veri üretir:

```javascript
import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });

wss.on("connection", socket => {
  const timer = setInterval(() => {
    socket.send(JSON.stringify({ time: Date.now() }));
  }, 1000);

  socket.on("message", data => {
    console.log("İstemciden geldi:", data.toString());
  });

  socket.on("close", () => clearInterval(timer));
});
```

Tarayıcı tarafında aynı kanal üzerinden hem mesaj alınabilir hem de gönderilebilir:

```javascript
const socket = new WebSocket("ws://localhost:8080");

socket.onmessage = event => console.log(event.data);
socket.onopen = () => socket.send("Merhaba sunucu!");
```

Uzun ömürlü kanal, tekrar tekrar bağlantı kurma maliyetini azaltır. Yaklaşık toplam gecikme şöyle düşünülebilir:

$$
T_{HTTP} \approx T_{bağlantı} + T_{istek} + T_{yanıt}
$$

WebSocket kurulduktan sonraki mesajlarda ise çoğunlukla yalnızca $T_{mesaj}$ maliyeti kalır.

## Peki bağlantı gerçekten kimde?

Bağlantıyı teknik olarak iki uç birlikte yaşatır. İstemci başlatır, sunucu kabul eder; her iki taraf da kapatabilir. Üstelik yük dengeleyici, güvenlik duvarı veya proxy zaman aşımı nedeniyle kanalı sonlandırabilir. HTTP’de konuşma sırasını çoğunlukla istemci belirlerken WebSocket’te iki taraf da bağımsız konuşur. Yani mesele “bağlantının sahibi” değil, **iletişimi kimin ve ne zaman başlatabildiğidir**.
