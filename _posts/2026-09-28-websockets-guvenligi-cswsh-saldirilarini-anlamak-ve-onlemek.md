---
layout: post
title: "WebSockets Güvenliği: CSWSH Saldırılarını Anlamak ve Önlemek"
math: true
categories: 
  - Bilgi
tags: 
  - websocket
  - cswsh
  - siber güvenlik
  - kimlik doğrulama
  - web güvenliği
  - csrf
toc: true
image: /img/websockets-guvenligi-cswsh-91.png
---

![websockets-guvenligi-cswsh-91](/img/websockets-guvenligi-cswsh-91.svg)


WebSocket, tarayıcı ile sunucu arasında sürekli ve çift yönlü iletişim kurarak sohbet, bildirim ve çevrim içi oyun gibi özellikleri mümkün kılar. Ancak bağlantı kurulurken yalnızca kullanıcının oturum çerezine güvenilirse saldırgan, kurbanın tarayıcısını adeta uzaktan kumanda edilen bir WebSocket istemcisine dönüştürebilir. Bu senaryoya **Cross-Site WebSocket Hijacking**, kısaca **CSWSH** denir.
``
## WebSocket bağlantısı nasıl kurulur?

WebSocket iletişimi bir HTTP yükseltme isteğiyle başlar. Tarayıcı aşağıdakine benzer bir istek gönderir:

```http
GET /socket HTTP/1.1
Host: uygulama.example
Upgrade: websocket
Connection: Upgrade
Origin: https://uygulama.example
Cookie: session=abc123
```

Sunucu isteği kabul ederse bağlantı kalıcı bir kanala dönüşür. Kritik ayrıntı şudur: Tarayıcı, hedef alan adına ait uygun çerezleri bağlantı isteğine otomatik olarak ekleyebilir. Sunucu yalnızca `session` çerezini kontrol ediyor fakat isteğin hangi sayfadan başlatıldığını doğrulamıyorsa güven sınırı delinmiş olur.

Kabaca risk şu şekilde modellenebilir:

$$Risk = Olasılık \times Etki$$

Oturum çerezinin otomatik gönderilmesi olasılığı, hassas mesajların okunabilmesi veya komut gönderilebilmesi ise etkiyi artırır.

## CSWSH saldırısının mantığı

Saldırgan kendi sitesine bir WebSocket istemcisi yerleştirir. Oturumu açık kullanıcı bu siteyi ziyaret ettiğinde kod, savunmasız uygulamanın WebSocket adresine bağlanmayı dener. Tarayıcı kullanıcının çerezini ekler; sunucu da bağlantıyı gerçek kullanıcıya ait sanabilir. Böylece saldırgan, tarayıcı üzerinden mesaj gönderebilir ve bağlantıdan dönen verileri kendi sayfasındaki kodla işleyebilir.

Bu saldırı CSRF’ye benzer, ancak tek bir HTTP işlemi yerine çift yönlü ve uzun ömürlü bir kanal hedeflenir.

| Özellik | Klasik CSRF | CSWSH |
|---|---|---|
| Hedef | HTTP isteği | WebSocket bağlantısı |
| İletişim | Genellikle tek yönlü | Çift yönlü |
| Temel sorun | Otomatik kimlik bilgisi | Otomatik kimlik bilgisi ve zayıf handshake |
| Muhtemel etki | Yetkisiz işlem | Veri okuma ve komut gönderme |

## Güvenli sunucu kontrolleri

İlk savunma, handshake sırasında `Origin` başlığını izin verilen adreslerle **tam eşleşme** kullanarak karşılaştırmaktır. `endsWith("example.com")` gibi gevşek kontroller, benzer alan adları veya ele geçirilmiş alt alanlar nedeniyle tehlikelidir.

```javascript
const allowedOrigins = new Set([
  "https://app.example.com"
]);

function verifyClient(info, callback) {
  const origin = info.origin;
  callback(allowedOrigins.has(origin), 403, "Origin reddedildi");
}
```

Bu örnek, yalnızca açıkça izin verilen kaynaktan gelen bağlantıları kabul eder. Yine de `Origin` kontrolü tek başına sihirli kalkan değildir; tarayıcı dışı istemciler bu başlığı taklit edebilir.

İkinci katmanda, sayfa yüklenirken üretilen kısa ömürlü ve kullanıcı oturumuna bağlı bir bağlantı belirteci kullanılabilir. Belirtecin tahmin edilmesi zor olmalıdır. Entropi yaklaşık olarak

$$H = \log_2(N)$$

ile ifade edilir; güvenli rastgele üretilmiş 128 bitlik bir değer pratikte tahmin saldırılarına karşı güçlüdür. Belirteci URL sorgusunda taşımak sunucu, proxy ve analiz günlüklarına sızmasına yol açabileceğinden dikkat ister. Mümkünse ilk mesajla doğrulama veya güvenli bir alt protokol tasarımı tercih edilmelidir.

## Savunma kontrol listesi

- Handshake sırasında katı `Origin` allowlist uygulayın.
- WebSocket için ayrı, kısa ömürlü ve tek kullanımlık yetkilendirme değeri üretin.
- Her mesajda kullanıcının ilgili işlem için yetkisini yeniden denetleyin.
- Bağlantı açmayı, mesaj hızını ve başarısız doğrulamaları sınırlandırın.
- Hassas işlemlerde yeniden kimlik doğrulama isteyin.
- `SameSite` çerezlerini ek savunma kabul edin; tek başına yeterli saymayın.
- Bağlantı, kullanıcı ve olay kimliklerini güvenli biçimde loglayın.

Özetle WebSocket güvenliği, “bağlantı açıldıysa kullanıcı güvenilirdir” varsayımına bırakılamaz. Güvenli tasarım; kaynağı doğrulayan, bağlantıyı ayrıca yetkilendiren ve her mesajın erişim hakkını kontrol eden katmanlı bir yaklaşım gerektirir. Gerçek zamanlı uygulamanız hızlı olabilir, fakat güvenlik kontrolleriniz ondan bir adım daha hızlı olmalıdır.
