---
layout: post
title: "WebRTC ile Tarayıcılar Arası Görüntülü Konferans: NAT Geçişi ve Eşler Arası Bağlantı"
math: true
categories: 
  - Bilgi
tags: 
  - webrtc
  - javascript
  - nat
  - stun
  - turn
---

Tarayıcıdan tarayıcıya görüntülü görüşme fikri kulağa sihir gibi gelir: video akışı merkezi bir medya sunucusundan geçmeden iki kullanıcı arasında akar. WebRTC bunu `getUserMedia`, `RTCPeerConnection` ve güvenli medya taşıma protokolleriyle mümkün kılar. Ancak internetin görünmez kapı bekçisi NAT yüzünden iki cihazın birbirini bulması çoğu zaman sandığınız kadar doğrudan değildir.
``
WebRTC'nin temel hedefi eşler arası, yani **peer-to-peer (P2P)** iletişimdir. Tarayıcı kamerayı ve mikrofonu kullanıcı izniyle alır; ardından iki uç, hangi ses/video biçimlerini anlayabildiğini ve internette erişilebilir aday adreslerini paylaşır. Bu paylaşım işlemine **signaling** denir. Önemli ayrım şudur: WebRTC standartı signaling kanalını tanımlamaz. WebSocket, Socket.IO, HTTP ya da başka bir yöntemle teklifleri taşıyabilirsiniz.

NAT, ev veya ofis ağındaki özel IP adreslerini tek bir genel IP arkasında saklar. Örneğin `192.168.1.20` adresindeki bir tarayıcı internete doğrudan görünmez. NAT tablosu, iç ağdan dışarı açılan bağlantıları eşler; dışarıdan gelen beklenmedik paketi ise genellikle reddeder. Bu nedenle iki kullanıcının yalnızca yerel IP adreslerini bilmesi görüntülü görüşme başlatmak için yeterli değildir.

| Bileşen | Görevi | Medya akışını taşır mı? |
|---|---|---:|
| Signaling sunucusu | SDP teklif/cevap ve ICE adaylarını iletir | Hayır |
| STUN sunucusu | Tarayıcının dışarıdan görünen IP/port bilgisini keşfeder | Hayır |
| TURN sunucusu | Doğrudan yol başarısızsa paketleri röleler | Evet |
| `RTCPeerConnection` | Bağlantı, şifreleme ve codec pazarlığını yönetir | Evet |

Bağlantı kurma sürecinin kalbinde **ICE** (Interactive Connectivity Establishment) vardır. ICE, farklı bağlantı adaylarını toplar ve en iyi çalışan yolu sınar. Adaylar yerel ağ adresi, STUN ile bulunan genel adres veya TURN röle adresi olabilir. Seçim yalnızca teorik hızla ilgili değildir; erişilebilirlik de belirleyicidir. Yaklaşık uçtan uca gecikme şöyle modellenebilir:

$$D_{toplam} = D_{yakalama} + D_{kodlama} + D_{ağ} + D_{jitter} + D_{çözme}$$

TURN kullanıldığında ağ bileşenine ek bir röle sıçraması eklenir. Bu nedenle P2P başarılı olduğunda maliyet ve gecikme genellikle daha düşüktür; fakat TURN, kurumsal güvenlik duvarları ve simetrik NAT gibi zor ağlarda konferansın kurtarıcısıdır.

Aşağıdaki örnek, bir eş bağlantısı oluşturur. `sendSignal` ve `onSignal` uygulamanızın WebSocket tabanlı signaling katmanını temsil eder; yani bu fonksiyonları sizin yazmanız gerekir.

```js
const pc = new RTCPeerConnection({
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" },
    {
      urls: "turn:turn.ornek.com:3478",
      username: "kullanici",
      credential: "guclu-gecici-parola"
    }
  ]
});

const stream = await navigator.mediaDevices.getUserMedia({
  video: true,
  audio: true
});
stream.getTracks().forEach(track => pc.addTrack(track, stream));

pc.ontrack = ({ streams }) => {
  remoteVideo.srcObject = streams[0];
};

pc.onicecandidate = ({ candidate }) => {
  if (candidate) sendSignal({ type: "ice", candidate });
};
```

Aramayı başlatan taraf SDP offer üretir; karşı taraf bunu `setRemoteDescription` ile uygular, answer üretir ve geri yollar. Ardından her iki taraf ICE adaylarını karşılıklı olarak `addIceCandidate` ile ekler. SDP, "video istiyorum" demenin ötesinde codec, çözünürlük, medya yönü ve şifreleme ayrıntılarını içeren bir pazarlık belgesidir.

| Aşama | Başlatan eş | Karşılayan eş |
|---|---|---|
| Medya erişimi | Kamera/mikrofon izni alır | Kamera/mikrofon izni alır |
| SDP pazarlığı | Offer oluşturur ve yollar | Offer'ı uygular, answer yollar |
| ICE | Aday toplar ve gönderir | Aday toplar, dener ve yanıtlar |
| Medya | Seçilen yoldan SRTP gönderir | Seçilen yoldan SRTP alır/gönderir |

"Sunucusuz" ifadesi medya açısından doğrudur, fakat pratikte signaling ve çoğu üretim ortamında TURN altyapısı gerekir. Ayrıca medya WebRTC'de DTLS-SRTP ile şifrelenir; yine de HTTPS kullanmak, TURN kimlik bilgilerini kısa ömürlü üretmek ve kullanıcı izinlerini dikkatle yönetmek zorunludur. İki kişilik görüşmede P2P harikadır; çok katılımcılı odalarda ise herkesin herkese akış göndermesi bant genişliğini hızla tüketir. Bu noktada SFU mimarisi, saf P2P'nin eğlenceli ama pahalı partisinin daha ölçeklenebilir alternatifi olur.
