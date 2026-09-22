---
layout: post
title: "TCP Üçlü El Sıkışması: Bağlantı Kurulurken Gerçekte Ne Oluyor?"
math: true
categories: 
  - Bilgi
tags: 
  - tcp
  - ağ
  - protokol
  - üçlü el sıkışma
  - 网络 programlama
  - wireshark
toc: true
---

Tarayıcıya bir adres yazıp Enter tuşuna bastığınızda veri hemen akmaya başlamaz. TCP kullanan istemci ile sunucu önce birbirlerini bulduklarını, iletişime hazır olduklarını ve başlangıç sıra numaralarını kabul ettiklerini doğrular. **TCP üçlü el sıkışması** denilen SYN, SYN-ACK ve ACK paketleri tam olarak bu hazırlığı gerçekleştirir.

``

## Neden el sıkışmaya ihtiyaç var?

TCP, UDP’den farklı olarak bağlantı odaklı ve güvenilir bir taşıma katmanı protokolüdür. Paketlerin sırasını takip eder, kayıpları algılar, yeniden iletim yapar ve alıcının kapasitesine göre veri akışını düzenler. Bütün bunlar için iki tarafın da bağlantıya ait bir durum kaydı tutması gerekir.

El sıkışma sırasında taraflar özellikle şunlarda anlaşır:

- Bağlantının iki yönlü olarak çalıştığı,
- Başlangıç sıra numaraları,
- Maksimum segment boyutu gibi TCP seçenekleri,
- Pencere ölçeklendirme ve SACK desteği,
- Bağlantıyı tanımlayan IP ve port çiftleri.

Bir TCP bağlantısı şu dörtlüyle benzersiz biçimde tanımlanır:

$$
(istemci\ IP, istemci\ portu, sunucu\ IP, sunucu\ portu)
$$

Örneğin `192.168.1.20:53142` adresinden `203.0.113.10:443` adresine yapılan bağlantı ayrı bir TCP oturumudur.

## Üç adımda neler oluyor?

İstemcinin başlangıç sıra numarasını $x$, sunucunun başlangıç sıra numarasını ise $y$ olarak düşünelim.

| Adım | Gönderen | Bayraklar | Sıra numarası | Onay numarası | Anlamı |
|---|---|---|---:|---:|---|
| 1 | İstemci | SYN | $x$ | — | Bağlantı kurmak istiyorum |
| 2 | Sunucu | SYN, ACK | $y$ | $x+1$ | İsteğini aldım, ben de hazırım |
| 3 | İstemci | ACK | $x+1$ | $y+1$ | Hazır olduğunu doğruladım |

### 1. SYN

İstemci, sunucunun dinlediği porta `SYN` bayraklı bir segment yollar ve `SYN-SENT` durumuna geçer. Sıra numarası rastgele görünse de işletim sistemi bunu belirli algoritmalarla üretir. Tahmin edilmesi zor numaralar, eski paketlerin yeni bağlantılarla karışmasını ve bazı saldırıları önlemeye yardımcı olur.

### 2. SYN-ACK

Sunucu portu açıksa isteği kabul eder, bağlantı için kaynak ayırır ve `SYN-RECEIVED` durumuna geçer. Gönderdiği segment hem kendi `SYN` bayrağını hem de istemcinin SYN paketini onaylayan `ACK` bayrağını taşır.

SYN bir sıra numarası tükettiği için onay değeri şöyledir:

$$
ACK = x + 1
$$

Bu aşama iki ayrı paket yerine tek bir SYN-ACK paketiyle yapılarak gereksiz ağ trafiği azaltılır.

### 3. ACK

İstemci, sunucunun başlangıç sıra numarasını $y+1$ değeriyle onaylar ve `ESTABLISHED` durumuna geçer. Sunucu bu ACK paketini alınca o da bağlantıyı kurulmuş kabul eder. Artık HTTP isteği, TLS el sıkışması veya uygulamanın başka verileri taşınabilir.

## Paket kaybolursa ne olur?

TCP hemen pes etmez. SYN veya SYN-ACK kaybolursa belirli bir zaman aşımından sonra paket yeniden gönderilir. Deneme sınırı aşılırsa uygulama bağlantı hatası alır. Sunucu kapalı bir porta erişildiğinde ise çoğunlukla `RST` paketi döner.

| Durum | Olası sonuç |
|---|---|
| Port açık | SYN-ACK gelir |
| Port kapalı | RST gelir |
| Güvenlik duvarı paketi düşürüyor | Yanıt gelmez, zaman aşımı oluşur |
| Ağda paket kaybı var | Yeniden iletim görülür |

## Trafiği canlı izlemek

Linux veya macOS üzerinde el sıkışmayı `tcpdump` ile gözlemleyebilirsiniz:

```bash
sudo tcpdump -i any -nn 'tcp port 443'
```

Ardından başka bir terminalde bağlantı başlatın:

```bash
curl https://example.com
```

Çıktıda önce `[S]`, ardından `[S.]` ve son olarak `[.]` işaretlerini görürsünüz. Bunlar sırasıyla SYN, SYN-ACK ve ACK paketleridir. Wireshark kullanıyorsanız `tcp.flags.syn == 1` filtresi başlangıç paketlerini bulmayı kolaylaştırır.

Üçlü el sıkışma yalnızca törensel bir merhaba değildir; iki yönlü erişilebilirliği kanıtlayan, sıra numaralarını eşitleyen ve TCP yeteneklerini belirleyen temel mekanizmadır. Web sayfasının arkasındaki ilk görünmez sohbet tam olarak burada başlar.
