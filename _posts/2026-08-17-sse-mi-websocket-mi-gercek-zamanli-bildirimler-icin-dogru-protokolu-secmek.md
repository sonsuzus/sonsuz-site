---
layout: post
title: "SSE mi WebSocket mi? Gerçek Zamanlı Bildirimler İçin Doğru Protokolü Seçmek"
math: true
categories: 
  - Bilgi
tags: 
  - sse
  - websocket
  - gerçek zamanlı sistemler
toc: true
image: /img/sse-mi-websocket-57.png
---

Bir kullanıcıya yeni sipariş, mesaj, fiyat değişimi veya sistem alarmı ulaştırmak istediğinizde klasik HTTP istek-cevap modeli yetersiz kalır. Tarayıcının sürekli “Yeni bir şey var mı?” diye sorması hem gecikme hem de gereksiz sunucu yükü üretir. SSE (Server-Sent Events) ve WebSocket, sunucu ile istemci arasındaki bağlantıyı canlı tutarak bu sorunu çözer; fakat aynı probleme farklı yönlerden yaklaşırlar.
``
## Temel iletişim modeli

SSE, HTTP üzerinden **sunucudan istemciye tek yönlü** olay akışı sağlar. Tarayıcı bir `EventSource` bağlantısı açar, sunucu da bağlantıyı kapatmadan metin tabanlı olaylar gönderir. WebSocket ise HTTP ile başlayan bağlantıyı yükselterek iki tarafın da istediği an veri gönderebildiği **çift yönlü** bir kanal oluşturur.

Bu farkı basitçe iletişim yönüyle ifade edebiliriz:

$$
SSE: Sunucu \rightarrow İstemci \\
WebSocket: Sunucu \leftrightarrow İstemci
$$

Sadece bildirim yayımlayan bir sistemde istemcinin sunucuya sürekli veri göndermesi gerekmiyorsa, WebSocket’in sunduğu esneklik gereksiz karmaşıklığa dönüşebilir. Buna karşılık sohbet, canlı oyun veya ortak belge düzenleme gibi senaryolarda iki yönlü akış temel ihtiyaçtır.

| Özellik | SSE | WebSocket |
|---|---|---|
| İletişim yönü | Tek yönlü: sunucu → istemci | Çift yönlü |
| Temel taşıma | Standart HTTP | HTTP Upgrade sonrası WebSocket |
| Veri formatı | UTF-8 metin | Metin ve ikili veri |
| Otomatik yeniden bağlanma | Tarayıcıda yerleşik | Uygulama tarafından yazılır |
| Karmaşıklık | Düşük | Orta / yüksek |
| Uygun örnek | Panel bildirimi, log akışı | Sohbet, oyun, canlı ortak çalışma |

## SSE neden bildirim sistemlerinde güçlüdür?

SSE’nin en büyük avantajı, web altyapısıyla doğal uyumudur. Yetkilendirme için cookie kullanılabilir; ters vekiller, HTTP yönlendirmeleri ve gözlemlenebilirlik araçlarıyla çalışmak genellikle daha kolaydır. Bağlantı koptuğunda `EventSource`, varsayılan olarak yeniden bağlanmayı dener. Sunucu `id:` alanı gönderirse istemci son aldığı olayı `Last-Event-ID` başlığıyla bildirebilir; böylece kaçırılan bildirimler yeniden oynatılabilir.

Örneğin yönetim paneline sipariş durumu gönderen basit bir SSE uç noktası şöyledir:

```javascript
app.get('/events/orders', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  const sendOrder = (order) => {
    res.write(`id: ${order.id}\n`);
    res.write('event: order-update\n');
    res.write(`data: ${JSON.stringify(order)}\n\n`);
  };

  orderBus.on('updated', sendOrder);
  req.on('close', () => orderBus.off('updated', sendOrder));
});
```

Burada çift satır sonu bir olayın bittiğini belirtir. İstemci tarafında `order-update` olayı dinlenir; bağlantı kesildiğinde tarayıcı yeniden bağlanma davranışını kendisi yönetir.

## WebSocket ne zaman gerekli olur?

İstemcinin sunucuya sık ve düşük gecikmeli mesaj yollaması gerekiyorsa WebSocket seçilmelidir. Bir sohbet odasında kullanıcı mesajları, yazıyor bilgisi, okundu durumu ve çevrimiçi varlığı aynı kanal üzerinden akar. Ayrıca ses verisi, oyun paketleri veya özel ikili protokoller için WebSocket’in binary frame desteği değerlidir.

```javascript
wss.on('connection', (socket) => {
  socket.on('message', (raw) => {
    const message = JSON.parse(raw);
    room.broadcast(JSON.stringify({
      type: 'chat-message',
      text: message.text
    }));
  });
});
```

Bu kod, istemciden gelen mesajı işleyip odadaki diğer katılımcılara dağıtır. Ancak yeniden bağlanma, mesaj sıralama, tekrar denemeleri ve yetkilendirme yenileme gibi ayrıntılar uygulama tasarımına bırakılmıştır.

## Karar verirken kontrol listesi

| Sorunuz | Tercih |
|---|---|
| Veri ağırlıkla sadece sunucudan mı akıyor? | SSE |
| İstemci sürekli komut veya veri mi yolluyor? | WebSocket |
| Olayları HTTP altyapısında kolay işletmek mi istiyorsunuz? | SSE |
| İkili veri ya da çok düşük gecikmeli etkileşim var mı? | WebSocket |

Pratik kural nettir: Bildirim, fiyat ekranı, iş ilerleme çubuğu ve canlı log için önce SSE düşünün. Karşılıklı, yoğun ve etkileşimli iletişim gerekiyorsa WebSocket’e geçin. Doğru seçim “en güçlü” teknolojiyi değil, veri akışınızın yönüne ve operasyonel maliyetinize en uygun olanı kullanmaktır.

![sse-mi-websocket-57](/img/sse-mi-websocket-57.svg)

