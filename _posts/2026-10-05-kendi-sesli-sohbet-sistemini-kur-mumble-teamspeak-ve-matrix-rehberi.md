---
layout: post
title: "Kendi Sesli Sohbet Sistemini Kur: Mumble, TeamSpeak ve Matrix Rehberi"
math: true
categories: 
  - Proje
tags: 
  - mumble
  - teamspeak
  - matrix
  - webrtc
  - voip
  - docker
  - sesli-sohbet
toc: true
image: /img/kendi-sesli-sohbet-78.png
---

Arkadaş grubunuz, oyuncu topluluğunuz veya uzaktan çalışan ekibiniz için bir sesli sohbet sistemi kurmak istiyorsanız Discord tek seçeneğiniz değil. Mumble ve TeamSpeak düşük gecikmeli klasik sunucu deneyimi sunarken Matrix, merkeziyetsiz yapısı ve modern WebRTC araçlarıyla daha esnek bir dünya vadeder. Gelin bu seçeneklerin çalışma mantığını inceleyip kendi altyapımızı kurmak için ilk adımları atalım.

``

## Sesli iletişimin temel mantığı

Bir sesli sohbet uygulaması önce mikrofon sinyalini örnekler, ardından Opus gibi bir codec ile sıkıştırır. Sıkıştırılmış paketler ağ üzerinden diğer katılımcılara gönderilir ve tekrar sese dönüştürülür. Uçtan uca hissedilen yaklaşık gecikme şöyle düşünülebilir:

$$G = G_{kodlama} + G_{ag} + G_{tampon} + G_{cozme}$$

Örneğin kodlama 20 ms, ağ yolculuğu 35 ms, jitter tamponu 30 ms ve çözme 10 ms sürerse toplam gecikme $G = 95\,ms$ olur. 150 ms altındaki değerler genellikle doğal konuşma için yeterlidir. Gecikme arttıkça insanlar farkında olmadan birbirinin sözünü kesmeye başlar; yani sorun yalnızca teknik değil, sosyal de olur.

UDP bu nedenle ses taşımada sık kullanılır. Kaybolan eski bir ses paketini yeniden istemek yerine yeni paketi zamanında oynatmak çoğunlukla daha değerlidir.

## Üç yaklaşımın karşılaştırması

| Özellik | Mumble | TeamSpeak | Matrix |
|---|---|---|---|
| Mimari | Merkezi ses sunucusu | Merkezi ses sunucusu | Federe iletişim ağı |
| Lisans | Açık kaynak | Tescilli | Açık standart, çeşitli istemciler |
| Gecikme | Çok düşük | Çok düşük | Kuruluma ve WebRTC topolojisine bağlı |
| Metin iletişimi | Temel | Orta düzey | Gelişmiş odalar ve geçmiş |
| Yönetim | Basit | Ayrıntılı izin sistemi | Esnek fakat daha karmaşık |
| En uygun kullanım | Oyun ve küçük topluluk | Kurumsal oyun toplulukları | Birleşik mesajlaşma ve görüşme |

![kendi-sesli-sohbet-78](/img/kendi-sesli-sohbet-78.svg)


Mumble'ın sunucu bileşeni **Murmur** adıyla bilinir. Hafiftir, düşük kaynakla çalışır ve konumsal ses desteği sunabilir. TeamSpeak ise gelişmiş kanal izinleri ve oturmuş yönetim araçlarıyla öne çıkar; ancak lisans koşulları, kendi çözümünü tamamen özgür biçimde şekillendirmek isteyenleri sınırlayabilir.

Matrix doğrudan bir ses codec'i değildir. Odaları, kullanıcı kimliklerini ve olayları yöneten federe bir protokoldür. Sesli görüşmeler genellikle WebRTC ve MatrixRTC tabanlı istemciler üzerinden gerçekleştirilir. Element ve Element Call bu ekosistemin bilinen örnekleridir.

## Docker ile Mumble kurulumu

Aşağıdaki Compose dosyası kalıcı veri kullanan temel bir Mumble sunucusu başlatır:

```yaml
services:
  mumble:
    image: mumblevoip/mumble-server:latest
    container_name: mumble-server
    restart: unless-stopped
    ports:
      - '64738:64738/tcp'
      - '64738:64738/udp'
    volumes:
      - mumble-data:/data

volumes:
  mumble-data:
```

Dosyayı `compose.yml` adıyla kaydedip şu komutu çalıştırabilirsiniz:

```bash
docker compose up -d
docker compose logs -f mumble
```

TCP bağlantısı yönetim ve kontrol işlemlerinde, UDP ise gecikmeye duyarlı ses paketlerinde kullanılır. Güvenlik duvarında her iki protokol için 64738 portunu açmayı unutmayın. Üretim ortamında güçlü bir yönetici parolası belirlemek ve düzenli yedek almak da şarttır.

## Matrix ne zaman daha mantıklı?

Yalnızca oyun sırasında konuşulacaksa Mumble çoğu ekip için en hızlı çözümdür. Ayrıntılı rol ve kanal yönetimi gerekiyorsa TeamSpeak değerlendirilebilir. Metin mesajları, dosyalar, botlar, farklı sunucular arasında iletişim ve sesli toplantılar tek sistemde birleşecekse Matrix daha güçlüdür.

Matrix kurulumu; Synapse gibi bir homeserver, PostgreSQL veritabanı, ters proxy, TLS sertifikası ve görüşmenin yapısına göre TURN veya MatrixRTC bileşenleri gerektirebilir. Özellikle NAT arkasındaki kullanıcılar doğrudan bağlantı kuramadığında TURN devreye girer. Bu durumda sunucunun bant genişliği ihtiyacı yaklaşık $B_{toplam} = n \times B_{kullanici}$ ilişkisiyle büyür.

Son kararınız yalnızca özellik listesine bağlı olmamalı. On kişilik bir oyun grubuna Matrix kümesi kurmak biraz mahalle maçına stadyum kiralamaya benzer. Küçük ve hızlı başlangıç için Mumble, sıkı izin yönetimi için TeamSpeak, uzun vadeli ve merkeziyetsiz bir iletişim platformu için Matrix seçmek daha dengeli bir yaklaşım olacaktır.
