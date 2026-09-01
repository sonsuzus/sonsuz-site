---
layout: post
title: "Sağlam Sohbet Uygulamaları İçin WebSocket Reconnection ve Heartbeat Rehberi"
math: true
categories: 
  - Program
tags: 
  - websocket
  - javascript
  - reconnection
  - heartbeat
  - sohbet uygulaması
toc: true
image: /img/saglam-sohbet-uygulamalari-16.png
---

Gerçek zamanlı sohbet uygulamalarında kullanıcılar bağlantının her zaman açık kalmasını bekler. Ancak mobil ağ değişimleri, tarayıcının uykuya geçmesi, sunucu yeniden başlatmaları ve geçici paket kayıpları bu beklentiyi kolayca bozar. Sağlam bir WebSocket istemcisi, kopmayı bir hata sonu değil, yönetilmesi gereken normal bir durum olarak görür. Bu noktada iki temel araç devreye girer: yeniden bağlanma (reconnection) ve heartbeat, yani nabız kontrolü.


![saglam-sohbet-uygulamalari-16](/img/saglam-sohbet-uygulamalari-16.svg)

``

WebSocket, TCP üzerinde çalışan kalıcı ve çift yönlü bir bağlantıdır. TCP bağlantısı açık görünse bile uygulama katmanında karşı tarafın gerçekten erişilebilir olduğundan emin olmak her zaman mümkün değildir. Örneğin cihaz Wi-Fi'dan mobil veriye geçtiğinde eski soket, tarayıcı açısından hemen `close` olayı üretmeyebilir. Heartbeat mesajları bu "sessiz kopuklukları" yakalar; reconnection mekanizması ise bağlantıyı kontrollü biçimde yeniden kurar.

## Neden sürekli yeniden bağlanmayı denememeliyiz?

Bağlantı düştüğünde her milisaniyede tekrar denemek, hem istemciyi hem sunucuyu gereksiz yükler. Özellikle sunucu kısa süreliğine erişilemez olduğunda binlerce kullanıcı aynı anda tekrar bağlanmaya çalışırsa **thundering herd** etkisi oluşur. Bunun ilacı exponential backoff ve jitter'dır.

Gecikme genel olarak şu şekilde hesaplanabilir:

$$d_n = \min(d_{max}, d_0 \times 2^n) + r$$

Burada $d_0$ başlangıç gecikmesi, $n$ başarısız deneme sayısı, $d_{max}$ üst sınır ve $r$ rastgele jitter değeridir. Jitter, istemcilerin aynı anda kapıya yüklenmesini önleyen küçük ama kahramanca bir ayrıntıdır.

| Yaklaşım | Davranış | Risk / Avantaj |
|---|---|---|
| Sabit gecikme | Her denemede örneğin 2 saniye bekler | Basit, ancak eşzamanlı yük oluşturabilir |
| Exponential backoff | Bekleme süresi katlanarak artar | Sunucuyu korur, toparlanması yavaş olabilir |
| Backoff + jitter | Artan süreye rastgelelik ekler | Dağıtık sistemler için en dengeli seçenek |

## İstemci tarafında dayanıklı bir bağlantı yöneticisi

Aşağıdaki örnek, bağlantı kurar, `ping` mesajı gönderir, `pong` bekler ve zaman aşımında soketi kapatarak normal yeniden bağlanma akışını tetikler. Uygulamanızdaki mesaj protokolünün JSON tabanlı olduğunu varsayar.

```js
class ChatSocket {
  constructor(url) {
    this.url = url;
    this.attempt = 0;
    this.maxDelay = 30_000;
    this.heartbeatTimer = null;
    this.pongTimer = null;
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.attempt = 0;
      console.log("Sohbet bağlantısı kuruldu");
      this.startHeartbeat();
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === "pong") this.confirmPong();
      else this.handleMessage(message);
    };

    this.ws.onclose = () => {
      this.stopHeartbeat();
      this.scheduleReconnect();
    };

    this.ws.onerror = () => this.ws.close();
  }

  scheduleReconnect() {
    const base = Math.min(1000 * 2 ** this.attempt++, this.maxDelay);
    const jitter = Math.random() * 500;
    setTimeout(() => this.connect(), base + jitter);
  }

  startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      if (this.ws.readyState !== WebSocket.OPEN) return;
      this.ws.send(JSON.stringify({ type: "ping" }));
      this.pongTimer = setTimeout(() => this.ws.close(), 5_000);
    }, 20_000);
  }

  confirmPong() {
    clearTimeout(this.pongTimer);
  }

  stopHeartbeat() {
    clearInterval(this.heartbeatTimer);
    clearTimeout(this.pongTimer);
  }

  handleMessage(message) {
    console.log("Yeni mesaj:", message);
  }
}
```

Bu kodda `onerror` içinde doğrudan yeniden bağlanmak yerine `close()` çağrılması önemlidir. Böylece tüm kopuş senaryoları tek bir kapıdan, yani `onclose` üzerinden yönetilir. Ayrıca bağlantı başarıyla açıldığında `attempt` sayacını sıfırlamak gerekir; aksi halde kısa bir kesintiden sonra bile istemci gereksiz uzun süre bekler.

## Heartbeat protokolünü netleştirin

Tarayıcıdaki standart WebSocket API'si gerçek WebSocket `PING/PONG` frame'lerini doğrudan göndermez. Bu nedenle uygulama seviyesinde `{ type: "ping" }` ve `{ type: "pong" }` mesajları tasarlamak yaygındır. Sunucu ping aldığında hızlıca pong dönmelidir; bu mesajları veritabanına yazmak veya sohbet geçmişine eklemek gereksizdir.

| Olay | İstemci davranışı | Sunucu davranışı |
|---|---|---|
| `ping` gönderildi | Pong için zamanlayıcı başlatır | `pong` yanıtı üretir |
| `pong` alındı | Zaman aşımını iptal eder | Ek işlem yapmaz |
| Pong zaman aşımı | Soketi kapatır ve backoff uygular | Bağlantı kapanışını temizler |
| Yeniden bağlanma | Oturum/kimlik bilgilerini tekrar iletir | Kullanıcıyı yeniden doğrular |

Son olarak, yeniden bağlanma sonrası kaçırılmış mesajları düşünün. İstemci son görülen mesaj kimliğini saklayıp yeniden bağlandığında sunucudan bu kimlikten sonraki olayları isteyebilir. Heartbeat bağlantının canlılığını, reconnection erişilebilirliği, mesaj senkronizasyonu ise sohbetin tutarlılığını korur. Üçü birlikte çalıştığında kullanıcı, ağın küçük dramalarını neredeyse hiç fark etmez.
