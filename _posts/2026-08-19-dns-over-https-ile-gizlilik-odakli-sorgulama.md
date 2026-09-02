---
layout: post
title: "DNS-over-HTTPS ile Gizlilik Odaklı Sorgulama"
math: true
categories: 
  - Bilgi
tags: 
  - dns
  - doh
  - gizlilik
  - ağ güvenliği
toc: true
image: /img/dns-over-https-51.png
---

İnternette bir siteye girmeden önce tarayıcınızın yaptığı ilk iş, alan adını IP adresine çevirmektir. Klasik DNS sorguları çoğu zaman şifresiz taşındığından, aynı ağdaki bir gözlemci hangi alan adlarını ziyaret etmek istediğinizi görebilir. DNS-over-HTTPS (DoH), bu sorguları HTTPS trafiğinin içine alarak meraklı ağ yöneticileri, açık Wi-Fi dinleyicileri ve bazı servis sağlayıcıları için görünürlüğü önemli ölçüde azaltır.
``

## DNS neden gizlilik meselesidir?

Bir web sayfasının içeriği HTTPS ile şifrelense bile DNS istekleri ayrı bir kanaldan gidebilir. Örneğin tarayıcı `ornek.com` adresini açmadan önce genellikle bir DNS çözümleyicisine “Bu alan adının IP adresi nedir?” diye sorar. Geleneksel DNS, çoğunlukla UDP veya TCP üzerinde 53 numaralı portu kullanır. Paket içeriği okunabilir olduğundan sorgulanan alan adı ağdaki gözlemciler için açık bir sinyaldir.

Basitleştirilmiş akış şöyledir:

$$\text{Tarayıcı} \rightarrow \text{DNS sorgusu} \rightarrow \text{IP adresi} \rightarrow \text{HTTPS bağlantısı}$$

DoH ise DNS mesajını HTTP isteğinin gövdesine veya parametrelerine yerleştirir ve TLS ile şifreler:

$$\text{DNS mesajı} \xrightarrow{\text{HTTPS/TLS}} \text{DoH çözümleyicisi}$$

Böylece yerel ağdaki biri DNS paketinin içeriğini doğrudan okuyamaz. Ancak “şifreleme her şeyi görünmez yapar” sonucuna atlamamak gerekir: bağlantı kurulan IP adresleri, trafik zamanlaması ve veri miktarı hâlâ bazı çıkarımlara izin verebilir.

| Özellik | Geleneksel DNS | DNS-over-HTTPS |
|---|---|---|
| Taşıma katmanı | UDP/TCP, genelde port 53 | HTTPS, genelde port 443 |
| Sorgu içeriği | Çoğunlukla düz metin | TLS ile şifreli |
| Ağda engellenme | Kolayca filtrelenebilir | HTTPS trafiği arasında ayırt etmek daha zor |
| Güven modeli | Yerel/ISS çözümleyicisi | Seçilen DoH sağlayıcısı |

## DoH hangi tehdidi azaltır?

Bir kafedeki açık Wi-Fi ağına bağlandığınızı düşünün. Kötü niyetli bir kişi aynı ağdaki DNS isteklerini izleyerek ilgi alanlarınız, kullandığınız servisler veya kurum içi uygulamalar hakkında fikir edinebilir. DoH, sorgu ile çözümleyici arasındaki yolu TLS ile korur. Ayrıca bazı ağların DNS yanıtını değiştirerek kullanıcıyı reklam veya sahte sayfalara yönlendirmesini zorlaştırır.

Fakat DoH, VPN değildir. Çözümleyici sağlayıcısı sorgularınızı görebilir; hedef sunucu da bağlantınızı görür. Bu nedenle gizlilik, tek bir protokol seçimi değil, güvenilen tarafların azaltılması problemidir. Kabaca risk yüzeyi şu şekilde düşünülebilir:

$$R \approx R_{\text{çözümleyici}} + R_{\text{uç nokta}} + R_{\text{meta veri}}$$

DoH ilk terimdeki yerel ağ gözlemcisi riskini azaltır; diğer terimleri sıfırlamaz.

## Tarayıcıda etkinleştirme ve doğrulama

Modern tarayıcılar genellikle ayarlarda “Güvenli DNS”, “Secure DNS” veya “DNS over HTTPS” adıyla bir seçenek sunar. Burada otomatik mod yerine, gizlilik politikasını incelediğiniz bir çözümleyiciyi seçebilirsiniz. Kurumsal ağlarda bu değişiklikten önce politika ve güvenlik ekibi kurallarını kontrol etmek önemlidir; kurum içi alan adları özel DNS sunucularına bağlı olabilir.

Komut satırında DoH uç noktasını test etmek için `curl` kullanılabilir. Aşağıdaki örnek, RFC 8484 uyumlu JSON yanıtı veren bir uç noktaya A kaydı sorar:

```bash
curl -H "accept: application/dns-json" \
  "https://cloudflare-dns.com/dns-query?name=example.com&type=A"
```

Yanıtta `Answer` alanında IP kayıtları görülür. Bu komut, tarayıcınızın gerçekten DoH kullandığını tek başına kanıtlamaz; yalnızca uç noktanın çalıştığını gösterir. Tarayıcı ayarlarını, işletim sistemi DNS yapılandırmasını ve ağınızın olası kurumsal yönlendirmelerini birlikte denetleyin.

## Sağlıklı kullanım için kısa kontrol listesi

- Şeffaf günlük tutma ve gizlilik politikası olan bir DoH sağlayıcısı seçin.
- Tarayıcı ile işletim sisteminin farklı DNS yolları kullanabileceğini unutmayın.
- HTTPS sertifika uyarılarını asla görmezden gelmeyin; DoH, sahte siteleri otomatik olarak engellemez.
- Reklam engelleme veya aile filtresi için DNS kullanıyorsanız, DoH’un bu politikaları baypas edip etmediğini test edin.

DoH, alan adı sorgularını “açık kartpostal” olmaktan çıkarıp şifreli bir zarfın içine koyar. Doğru sağlayıcı seçimi, güncel tarayıcı ayarları ve gerçekçi tehdit modeliyle birleştiğinde günlük internet kullanımında anlamlı bir mahremiyet katmanı sağlar.

![dns-over-https-51](/img/dns-over-https-51.svg)

