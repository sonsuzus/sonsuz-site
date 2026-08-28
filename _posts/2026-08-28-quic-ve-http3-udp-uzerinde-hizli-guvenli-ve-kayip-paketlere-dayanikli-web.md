---
layout: post
title: "QUIC ve HTTP/3: UDP Üzerinde Hızlı, Güvenli ve Kayıp Paketlere Dayanıklı Web"
math: true
categories: 
  - Bilgi
tags: 
  - QUIC
  - HTTP/3
  - UDP
  - Performans
  - Ağ Protokolleri
---

Web performansında milisaniyeler bazen kullanıcı deneyimini, bazen de bir satışın gerçekleşip gerçekleşmeyeceğini belirler. HTTP/3, bu yarışta yalnızca HTTP başlıklarını değiştirmez; alttaki taşıma katmanını da TCP’den QUIC’e taşıyarak oyunun kurallarını yeniler. QUIC, UDP datagramları üzerinde çalışan ancak TLS 1.3 şifreleme, güvenilir teslim, akış kontrolü ve tıkanıklık kontrolü gibi modern taşıma özelliklerini kendi içinde sunan bir protokoldür.

``

## Neden TCP + TLS Yeterli Değildi?

Geleneksel HTTPS bağlantısında istemci önce TCP üçlü el sıkışmasını yapar, ardından TLS el sıkışmasıyla şifreleme anahtarlarını kurar. İlk bağlantıda bu maliyet kabaca iki gidiş-dönüş süresine (RTT) ulaşabilir:

$$T_{ilk} \approx RTT_{TCP} + RTT_{TLS} + T_{istek}$$

Örneğin mobil ağda $RTT=80\,ms$ ise, uygulama verisi gönderilmeden önce yaklaşık 160 ms yalnızca kurulum için harcanabilir. TLS 1.3 bu süreci iyileştirse de TCP’nin bağlantı kurulum adımı hâlâ vardır. QUIC ise TLS 1.3’ü taşıma protokolünün ayrılmaz parçası yapar ve çoğu yeni bağlantıda 1-RTT, daha önce ziyaret edilmiş güvenilir sunucularda ise 0-RTT veri gönderimi hedefler.

| Özellik | TCP + TLS + HTTP/2 | QUIC + HTTP/3 |
|---|---|---|
| Taşıma tabanı | TCP | UDP üzerinde QUIC |
| Şifreleme | Taşıma katmanından ayrı TLS | Varsayılan olarak TLS 1.3 entegre |
| Yeni bağlantı | Genellikle TCP + TLS maliyeti | Tipik olarak 1-RTT |
| Tekrar bağlantı | TLS oturum devamı mümkün | 0-RTT erken veri mümkün |
| Akışlar | TCP bayt akışı üzerinde | Bağımsız QUIC stream’leri |

## Paket Kaybı: Asıl Fark Nerede?

TCP güvenilirdir; kaybolan segmenti yeniden yollar ve sıra dışı gelen veriyi uygulamaya teslim etmeden bekler. HTTP/2 birden çok isteği tek TCP bağlantısında çoğulladığından, tek paketin kaybı tüm akışları etkileyebilir. Buna **transport-level head-of-line blocking** denir.

QUIC’te her HTTP/3 isteği bağımsız bir stream üzerinde ilerler. Bir stream’in paketi kaybolduğunda yalnızca o stream’in ilgili verisi bekler; başka stream’lerdeki veriler işlenmeye devam edebilir. Elbette ağdaki fiziksel kayıp ortadan kalkmaz; QUIC de kaybı algılar ve veriyi yeniden iletir. Kazanç, kaybın bağlantıdaki tüm işlemleri kilitlememesidir.

| Senaryo | HTTP/2 / TCP davranışı | HTTP/3 / QUIC davranışı |
|---|---|---|
| Görsel paketi kaybolur | Diğer yanıtlar da sıra bekleyebilir | Etkilenen stream yeniden iletim bekler |
| Ağ değişimi (Wi-Fi → 5G) | IP değişimi bağlantıyı koparabilir | Connection ID ile bağlantı taşınabilir |
| Paket sırası bozulur | TCP sıralı bayt akışını bekler | Stream bazında bağımsız işleme yapılır |

## Hızlı Bir Performans Modeli

Basitleştirilmiş bir sayfa yükleme süresi modeli şöyle düşünülebilir:

$$T_{yükleme}=T_{DNS}+T_{kurulum}+T_{TTFB}+T_{aktarim}+T_{kayıp}$$

QUIC özellikle $T_{kurulum}$ ve paket kaybının büyüttüğü $T_{kayıp}$ bileşenlerini azaltmayı amaçlar. Ancak her koşulda mucize değildir: UDP’nin bazı kurumsal ağlarda engellenmesi, CPU’ya binen kullanıcı alanı şifreleme maliyeti ve 0-RTT verisinin yeniden oynatma (replay) riski dikkatle ele alınmalıdır. Bu nedenle 0-RTT ile yalnızca idempotent, yani tekrar çalıştırılması zararsız GET benzeri istekler gönderilmelidir.

Aşağıdaki komut, bir sunucunun HTTP/3 desteğini ve ayrıntılı zamanlamayı gözlemlemek için pratik bir başlangıçtır:

```bash
curl --http3 -s -o /dev/null \
  -w 'connect=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n' \
  https://ornek.com
```

Bu komut yanıt gövdesini ekrana basmadan bağlantı, ilk bayt ve toplam süreyi gösterir. Sağlıklı bir analiz için aynı URL’yi HTTP/2 ve HTTP/3 ile, farklı ağ koşullarında ve çok sayıda tekrar ile ölçün. Özellikle yüksek RTT’li mobil bağlantılar ile %1-%3 paket kaybı eklenmiş test ortamları, QUIC’in avantajını masaüstü kablolu ağlardan çok daha görünür kılar.

Sonuç olarak HTTP/3, UDP’ye “güvenilirlik eklemekten” fazlasıdır: şifrelemeyi zorunlu kılar, bağlantı kurulumunu kısaltır, stream bağımsızlığı sağlar ve ağ değişimlerine daha zarif uyum sağlar. Modern web için bu, yalnızca daha hızlı bir protokol değil, gecikme ve kayıp karşısında daha dirençli bir iletişim modelidir.
