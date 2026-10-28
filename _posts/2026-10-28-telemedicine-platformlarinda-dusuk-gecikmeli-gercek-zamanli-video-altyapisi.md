---
layout: post
title: "Telemedicine Platformlarında Düşük Gecikmeli Gerçek Zamanlı Video Altyapısı"
math: true
categories: 
  - Bilgi
tags: 
  - telemedicine
  - webrtc
  - video
  - düşük-gecikme
  - sağlık-teknolojileri
  - gerçek-zamanlı-iletişim
toc: true
image: /img/telemedicine-platformlarinda-dusuk-29.png
---

Uzaktan muayenede görüntünün birkaç saniye geriden gelmesi yalnızca can sıkıcı değildir; doktor ile hastanın doğal iletişimini bozabilir ve görsel belirtilerin değerlendirilmesini zorlaştırabilir. Telemedicine platformları bu nedenle videoyu basitçe karşı tarafa göndermek yerine gecikme, görüntü kalitesi, ağ kararlılığı, güvenlik ve ölçeklenebilirlik arasında sürekli denge kuran gerçek zamanlı iletişim altyapıları kullanır.

``

## Temel teknoloji: WebRTC

Modern telemedicine uygulamalarının büyük bölümü **WebRTC** teknolojisinden yararlanır. WebRTC, tarayıcılar ve mobil uygulamalar arasında eklenti gerektirmeden gerçek zamanlı ses, video ve veri aktarımı sağlar. İletişim mümkün olduğunda eşler arası, yani **P2P** kurulur. Böylece medya paketleri gereksiz bir uygulama sunucusu turu yapmaz.

Bir görüşmenin yaklaşık uçtan uca gecikmesi şöyle modellenebilir:

$$
T_{toplam} = T_{yakalama} + T_{kodlama} + T_{ağ} + T_{çözme} + T_{oynatma}
$$

Burada kamera görüntüsünün alınması, sıkıştırılması, ağ üzerinden taşınması, çözülmesi ve ekranda gösterilmesi ayrı ayrı gecikme üretir. Akıcı bir görüşme için toplam gecikmenin genellikle 300 milisaniyenin altında tutulması hedeflenir.

| Aktarım yaklaşımı | Tipik gecikme | Avantajı | Telemedicine uygunluğu |
|---|---:|---|---|
| WebRTC | 100–500 ms | Gerçek zamanlı ve etkileşimli | Çok yüksek |
| HLS | 6–30 sn | Büyük kitlelere kolay yayın | Düşük |
| RTMP | 1–5 sn | Yayın sistemleriyle uyumlu | Orta-düşük |

## Bağlantı nasıl kuruluyor?

WebRTC medya aktarımını yönetir ancak tarafların birbirini bulması için bir **signaling sunucusu** gerekir. Bu sunucu SDP adı verilen oturum bilgilerini ve ICE adaylarını aktarır. Ardından STUN sunucusu cihazların genel ağ adreslerini keşfetmesine yardımcı olur. Kurumsal ağ veya sıkı bir güvenlik duvarı doğrudan bağlantıyı engellerse trafik TURN sunucusu üzerinden geçirilir.

```javascript
const connection = new RTCPeerConnection({
  iceServers: [
    { urls: "stun:stun.example.com:3478" },
    {
      urls: "turn:turn.example.com:3478",
      username: "temporary-user",
      credential: "temporary-password"
    }
  ]
});

const stream = await navigator.mediaDevices.getUserMedia({
  video: { width: 1280, height: 720 },
  audio: { echoCancellation: true, noiseSuppression: true }
});

stream.getTracks().forEach(track => connection.addTrack(track, stream));
```

Bu örnek, kamera ve mikrofon akışını alarak WebRTC bağlantısına ekler. Gerçek sistemlerde TURN kimlik bilgileri kısa ömürlü üretilmeli; kaynak koduna sabit parola yazılmamalıdır.

## Değişken ağ koşullarına uyum

Hastalar her zaman güçlü Wi-Fi kullanmaz. Paket kaybı, düşük bant genişliği ve titreşim anlamına gelen **jitter**, görüntüyü bozabilir. Platformlar bu sorunlara uyarlanabilir bit hızıyla karşılık verir. Ağ kötüleştiğinde önce çözünürlük veya kare hızı azaltılır; bağlantı iyileştiğinde kalite yeniden yükseltilir.

Gerekli ham veri miktarı kabaca şu ilişkiyle düşünülebilir:

$$
B \propto W \times H \times FPS \times Q
$$

$W$ ve $H$ çözünürlüğü, $FPS$ saniyedeki kare sayısını, $Q$ ise kalite katsayısını temsil eder. H.264, VP8, VP9 veya AV1 gibi codec'ler bu ham veriyi sıkıştırır. H.264 geniş cihaz desteği sunarken AV1 daha verimli sıkıştırma sağlayabilir fakat eski cihazlarda daha yüksek işlem yükü oluşturabilir.

## SFU, kayıt ve ölçeklendirme

İki kişilik muayenede P2P yeterli olabilir. Görüşmeye uzman, tercüman veya hasta yakını katıldığında **SFU** kullanmak daha verimlidir. SFU, her katılımcıdan tek akış alır ve uygun kalitedeki katmanları diğer katılımcılara yönlendirir. Simulcast sayesinde istemci aynı videoyu düşük, orta ve yüksek kalite seçenekleriyle gönderebilir.

Sağlık verisi sıradan toplantı verisi değildir. Aktarım DTLS-SRTP ile şifrelenmeli, erişimler yetkilendirilmeli, kayıtlar açık rızaya bağlanmalı ve KVKK gibi düzenlemelere uygun saklanmalıdır. Ayrıca paket kaybı, gidiş-dönüş süresi, bitrate ve bağlantı kopmaları izlenmelidir. Kısacası başarılı bir telemedicine deneyimi yalnızca net görüntü değil; düşük gecikme, güvenli tasarım ve kötü ağlarda bile kontrollü biçimde çalışabilen dayanıklı bir sistem gerektirir.

![telemedicine-platformlarinda-dusuk-29](/img/telemedicine-platformlarinda-dusuk-29.svg)

