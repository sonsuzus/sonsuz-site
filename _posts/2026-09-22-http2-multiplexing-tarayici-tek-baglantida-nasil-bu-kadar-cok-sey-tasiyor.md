---
layout: post
title: "HTTP/2 Multiplexing: Tarayıcı Tek Bağlantıda Nasıl Bu Kadar Çok Şey Taşıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - http2
  - multiplexing
  - web
  - tarayıcı
  - tcp
  - performans
toc: true
image: /img/http2-multiplexing-tarayici-69.png
---

![http2-multiplexing-tarayici-69](/img/http2-multiplexing-tarayici-69.svg)


Bir web sayfası açıldığında tarayıcı yalnızca HTML indirmez; CSS, JavaScript, font, görsel ve API yanıtları gibi onlarca kaynağa ihtiyaç duyar. HTTP/1.1 döneminde bu kalabalığı yönetmek için birden fazla TCP bağlantısı açılırdı. HTTP/2 ise multiplexing sayesinde aynı bağlantıyı çok şeritli bir otoyola dönüştürür: farklı istek ve yanıtlar, birbirini tamamlamayı beklemeden eş zamanlı biçimde taşınabilir.

``

## Önce temel problem: HTTP/1.1 sıralaması

HTTP/1.1 kalıcı bağlantıları desteklese de bir bağlantı üzerindeki yanıtların sırası önemliydi. İlk istek yavaş kaldığında arkasındaki işler de bekleyebiliyordu. Buna **head-of-line blocking**, yani sıra başı engellemesi denir.

Tarayıcılar çözüm olarak aynı origin için genellikle birkaç paralel TCP bağlantısı açtı. Fakat her bağlantının TCP ve TLS kurulumu maliyetliydi. Ayrıca bağlantılar ağ kapasitesini paylaşırken gereksiz rekabet oluşturabiliyordu.

| Özellik | HTTP/1.1 | HTTP/2 |
|---|---|---|
| Veri gösterimi | Metin tabanlı | İkili çerçeveler |
| Paralel istekler | Genellikle çoklu bağlantılarla | Tek bağlantıda stream'lerle |
| Başlık sıkıştırma | Sınırlı veya yok | HPACK |
| Yanıt sıralaması | Bağlantı sırasına bağımlı | Stream bazında bağımsız |
| TCP bağlantısı ihtiyacı | Origin başına birden fazla olabilir | Çoğunlukla origin başına bir tane |

## Multiplexing nasıl çalışır?

HTTP/2 iletişimi **stream**, **message** ve **frame** katmanlarına ayırır. Stream, bağlantı içindeki mantıksal iletişim kanalıdır. Her stream benzersiz bir kimlik taşır. İstek ve yanıt mesajları ise `HEADERS` ve `DATA` gibi küçük ikili frame'lere bölünür.

Örneğin tarayıcı aynı anda üç kaynak istesin:

- Stream 1: `index.html`
- Stream 3: `app.js`
- Stream 5: `logo.png`

Sunucu frame'leri şu sırayla gönderebilir:

```text
[Stream 1: HEADERS]
[Stream 3: HEADERS]
[Stream 1: DATA]
[Stream 5: HEADERS]
[Stream 3: DATA]
[Stream 5: DATA]
```

Frame'ler ağ üzerinde iç içe geçse de tarayıcı, stream kimliklerine bakarak parçaları doğru mesaja yerleştirir. Bir yapboz kutusundaki parçaların renklerine göre ayrılması gibi! Böylece büyük bir görselin aktarımı, küçük bir CSS dosyasının gönderilmesini uygulama katmanında engellemez.

Teorik olarak bağlantının toplam bant genişliği $B$ ve aynı anda etkin stream sayısı $n$ ise adil paylaşım altında stream başına yaklaşık kapasite şöyle düşünülebilir:

$$b_i \approx \frac{B}{n}$$

Gerçekte öncelikler, akış kontrolü, dosya boyutları ve ağ koşulları nedeniyle dağılım eşit olmak zorunda değildir.

## Küçük bir HTTP/2 örneği

Node.js ile TLS kullanan basit bir HTTP/2 sunucusu oluşturabiliriz:

```javascript
const http2 = require('http2');
const fs = require('fs');

const server = http2.createSecureServer({
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
});

server.on('stream', (stream, headers) => {
  const path = headers[':path'];
  stream.respond({ ':status': 200, 'content-type': 'text/plain' });
  stream.end(`${path} kaynağından merhaba!`);
});

server.listen(8443);
```

Buradaki `stream` olayı her HTTP/2 isteğini bağımsız bir mantıksal kanal olarak ele alır. Birden fazla istek aynı TLS/TCP bağlantısından gelse bile sunucu bunlara ayrı stream nesneleriyle yanıt verir.

## Her şey tamamen engelsiz mi?

Hayır. HTTP/2, HTTP katmanındaki sıra problemini büyük ölçüde çözer; ancak TCP kaybolan paketleri sırasıyla yeniden oluşturur. Tek bir TCP paketi kaybolduğunda aynı bağlantıdaki bütün HTTP/2 stream'leri kısa süreliğine bekleyebilir. Bu, **TCP seviyesinde head-of-line blocking** problemidir.

HTTP/3 bu noktada TCP yerine QUIC kullanır. QUIC stream'leri taşıma katmanında da bağımsız tuttuğu için bir stream'deki paket kaybı diğerlerini aynı ölçüde durdurmaz.

Sonuç olarak tarayıcının “tek bağlantı sihri”, veriyi küçük frame'lere bölmesi, her parçayı bir stream kimliğiyle etiketlemesi ve alıcı tarafta yeniden birleştirmesidir. Tek bir kamyon sırasından çok, paketleri ortak tünelden geçiren akıllı bir lojistik sistemi düşünmek daha doğrudur.
