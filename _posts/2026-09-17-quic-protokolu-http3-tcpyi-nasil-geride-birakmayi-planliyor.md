---
layout: post
title: "QUIC Protokolü: HTTP/3, TCP’yi Nasıl Geride Bırakmayı Planlıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - quic
  - http3
  - tcp
  - udp
  - web performansı
  - ağ protokolleri
toc: true
---

Web’in hız sınırlarını yalnızca daha güçlü sunucular veya küçültülmüş JavaScript dosyaları belirlemiyor. Tarayıcı ile sunucu arasındaki bağlantının nasıl kurulduğu da performansın başrol oyuncularından biri. QUIC, onlarca yıldır internetin omurgasında çalışan TCP’nin bazı kronik sorunlarını aşmak için UDP üzerinde geliştirilen modern bir taşıma protokolü; HTTP/3 ise onun web dünyasındaki en önemli yolcusu.

``

## Önce temel soru: TCP neden yetmiyor?

TCP güvenilir, sıralı ve bağlantı odaklı veri aktarımı sağlar. Paket kaybolduğunda eksik parçayı yeniden ister; verilerin uygulamaya doğru sırada teslim edilmesini garanti eder. Ancak HTTPS bağlantısında TCP el sıkışmasına TLS görüşmesi de eklenir. Yeni bir bağlantının veri taşımaya başlaması birkaç ağ turu gerektirebilir.

Bir ağ turunun süresi **RTT** olsun. Klasik bir TCP ve TLS 1.2 bağlantısının yaklaşık başlangıç maliyeti şöyle düşünülebilir:

$$T_{başlangıç} \approx 1\,RTT_{TCP} + 2\,RTT_{TLS} = 3\,RTT$$

RTT değeri 100 ms olduğunda, uygulama verisi gönderilmeden yaklaşık 300 ms harcanabilir. TLS 1.3 bu maliyeti azaltır; QUIC ise taşıma ve şifreleme el sıkışmalarını birleştirerek çoğu yeni bağlantıda **1-RTT**, daha önce görüşülmüş bağlantılarda ise uygun koşullarda **0-RTT** veri aktarımı sunar.

## QUIC neden UDP kullanıyor?

UDP kendi başına paket sıralama, yeniden iletim veya akış kontrolü sağlamaz. QUIC’in yaptığı numara, bu özellikleri kullanıcı alanında yeniden ve daha esnek biçimde uygulamaktır. Böylece işletim sistemlerindeki TCP çekirdeğinin yıllar süren güncelleme döngüsüne bağlı kalmadan protokol geliştirilebilir.

| Özellik | TCP + HTTP/2 | QUIC + HTTP/3 |
|---|---|---|
| Taşıma temeli | TCP | UDP üzerinde QUIC |
| Şifreleme | Sonradan TLS | TLS 1.3 zorunlu ve bütünleşik |
| İlk bağlantı | Genellikle daha fazla RTT | Çoğunlukla 1-RTT |
| Tekrar bağlantı | TLS oturumuna bağlı | Uygun durumda 0-RTT |
| Paket kaybı etkisi | Tüm akışlar bekleyebilir | Genellikle yalnızca ilgili akış bekler |
| Ağ değişimi | Bağlantı kopabilir | Connection ID ile sürdürülebilir |

## Head-of-line blocking meselesi

HTTP/2, tek TCP bağlantısı üzerinde birden fazla mantıksal akış taşır. Fakat TCP paketleri küresel olarak sıraladığı için bir paket kaybolduğunda bağımsız HTTP/2 akışları bile bekleyebilir. Buna taşıma katmanı **head-of-line blocking** denir.

QUIC’te her akışın sıralaması ayrıdır. CSS dosyasına ait paket kaybolduğunda görsel akışı veya başka bir API yanıtı ilerlemeye devam edebilir. Kayıp oranı $p$, RTT değeri $r$ ise yeniden iletimin oluşturduğu gecikme kabaca ağ koşullarına bağlı olarak $p \times r$ ile büyür. QUIC kaybı yok etmez; kaybın diğer akışlara yaydığı cezayı sınırlar.

## Bağlantı göçü: Wi-Fi’dan mobile geçerken

TCP bağlantısı kaynak IP, kaynak port, hedef IP ve hedef port dörtlüsüyle tanımlanır. Telefon Wi-Fi’dan mobil veriye geçtiğinde IP değişir ve bağlantı çoğunlukla yeniden kurulmalıdır. QUIC ise bağlantıyı sabit ağ adresi yerine **Connection ID** ile takip edebilir. Yolculuk sırasında görüntülü görüşmenin veya dosya indirmesinin daha az kesilmesi bu yüzden mümkündür.

Bir sunucunun HTTP/3 desteğini komut satırından şöyle sınayabiliriz:

```bash
curl --http3 -I https://example.com
```

Bu komut, uygun QUIC desteğine sahip bir `curl` sürümüyle yalnızca HTTP başlıklarını ister. Çıktıda `HTTP/3` görülmesi, istemci ile sunucunun QUIC üzerinden anlaşabildiğini gösterir. Sunucunun UDP 443 portuna izin vermesi de gerekir; aksi durumda istemci genellikle HTTP/2 veya HTTP/1.1’e geri döner.

## Peki QUIC gerçekten TCP’yi bitirecek mi?

Muhtemelen hayır; en azından yakın zamanda. TCP, veritabanlarından SSH bağlantılarına kadar çok geniş bir ekosistemde güvenilirliğini kanıtladı. QUIC’in kullanıcı alanındaki şifreleme ve paket işleme maliyeti bazı sistemlerde daha fazla CPU tüketebilir. UDP’yi sınırlayan eski güvenlik duvarları ve kurumsal ağlar da dağıtımı zorlaştırabilir.

Buna rağmen HTTP/3; yüksek gecikmeli, paket kayıplı ve sık ağ değiştiren mobil ortamlarda güçlü avantajlar sunuyor. QUIC’in vaadi TCP’yi her alanda yenmek değil, modern web’in ihtiyaçlarına daha hızlı uyarlanabilen, güvenliği varsayılan ve akışları birbirinden daha iyi yalıtan bir temel oluşturmak. Kısacası TCP emekli olmuyor; fakat web performansı yarışında artık yanında oldukça çevik bir rakip koşuyor.
