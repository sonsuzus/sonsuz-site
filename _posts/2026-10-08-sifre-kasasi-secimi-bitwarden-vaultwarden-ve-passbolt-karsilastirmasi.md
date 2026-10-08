---
layout: post
title: "Şifre Kasası Seçimi: Bitwarden, Vaultwarden ve Passbolt Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - şifre yöneticisi
  - bitwarden
  - vaultwarden
  - passbolt
  - siber güvenlik
  - self-hosted
toc: true
image: /img/sifre-kasasi-secimi-59.png
---

![sifre-kasasi-secimi-59](/img/sifre-kasasi-secimi-59.svg)


Her hesapta aynı parolayı kullanmak, bütün kapıları tek anahtarla kilitlemeye benzer: Anahtar ele geçirilirse mahallede açık kapı bırakmazsınız. Şifre yöneticileri; güçlü parolalar üretir, bunları şifreli bir kasada saklar ve cihazlar arasında eşitler. Peki popüler Bitwarden, hafifliğiyle öne çıkan Vaultwarden ve ekip odaklı Passbolt arasında nasıl seçim yapılır? Gelin dijital anahtarlığımızı masaya yatıralım.

``

## Şifre yöneticisinin temel mantığı

Bir şifre yöneticisi, kayıtlarınızı ana paroladan türetilen bir anahtarla şifreler. Güvenilir sistemlerde sunucu kasanın açık hâlini veya ana parolayı bilmez; şifre çözme işlemi istemci cihazda gerçekleşir. Bu yaklaşım genellikle **sıfır bilgi mimarisi** olarak adlandırılır.

Rastgele üretilmiş bir parolanın teorik entropisi yaklaşık olarak şöyle hesaplanır:

$$H = L \times \log_2(N)$$

Burada $L$ parola uzunluğu, $N$ ise kullanılabilecek karakter sayısıdır. Örneğin 94 karakterlik bir kümeden üretilen 20 karakterli parola yaklaşık $20 \times \log_2(94) \approx 131$ bit entropiye sahiptir. İnsan zihninin ürettiği `Kedim123` benzeri parolalarda ise tahmin edilebilir kalıplar nedeniyle gerçek güvenlik çok daha düşüktür.

Ana parola güçlü ve benzersiz olmalı; ayrıca kasada **iki faktörlü kimlik doğrulama** etkinleştirilmelidir. Kasayı kendi sunucunuza kurmak kontrol sağlar, fakat bakım sorumluluğunu ortadan kaldırmaz.

## Üç çözümün karşılaştırması

| Özellik | Bitwarden | Vaultwarden | Passbolt |
|---|---|---|---|
| Temel hedef | Bireysel ve kurumsal kullanım | Hafif self-hosted kullanım | Ekip içi parola paylaşımı |
| Barındırma | Resmî bulut veya self-hosted | Self-hosted | Bulut veya self-hosted |
| Kaynak tüketimi | Görece yüksek | Genellikle düşük | Orta |
| İstemci ekosistemi | Geniş | Bitwarden istemcileriyle uyumlu | Web ve tarayıcı ağırlıklı |
| Paylaşım modeli | Organizasyon ve koleksiyon | Bitwarden modeline benzer | Kullanıcı ve grup merkezli |
| Öne çıkan yön | Dengeli, kullanımı kolay | Küçük sunucular için ekonomik | Ayrıntılı ekip paylaşımı |

### Bitwarden: Güvenli varsayılan seçenek

Bitwarden; mobil uygulamaları, tarayıcı eklentileri, masaüstü istemcileri ve komut satırı aracıyla eksiksiz bir ekosistem sunar. Teknik bakım yapmak istemeyen kullanıcılar resmî bulutu seçebilir. Kurumlar ise organizasyonlar, koleksiyonlar ve erişim politikalarıyla kayıtları yönetebilir.

Self-hosted kurulumu mümkündür; ancak resmî sunucu bileşenleri küçük bir ev sunucusu için ağır gelebilir. Buna karşılık resmî destek ve belgeler, kurumsal kullanımda önemli avantajdır.

### Vaultwarden: Küçük sunucunun çalışkan cücesi

Vaultwarden, Bitwarden sunucu API’sinin topluluk tarafından geliştirilen ve Rust ile yazılan uyumlu bir uygulamasıdır. Resmî Bitwarden istemcileriyle çalışır ve düşük kaynak tüketimi sayesinde Raspberry Pi, mini PC veya uygun bir VPS üzerinde sıkça tercih edilir.

Basitleştirilmiş bir Docker Compose servisi şöyle tanımlanabilir:

```yaml
services:
  vaultwarden:
    image: vaultwarden/server:latest
    restart: unless-stopped
    volumes:
      - ./vw-data:/data
    ports:
      - 127.0.0.1:8080:80
```

Bu yapı verileri kalıcı dizinde tutar ve servisi yalnızca yerel arayüzde açar. Dış erişim için HTTPS sağlayan bir ters vekil, düzenli güncelleme ve şifreli yedekleme gerekir. Vaultwarden resmî Bitwarden sunucusu değildir; özellik uyumluluğu ve destek beklentisi buna göre değerlendirilmelidir.

### Passbolt: Takım paylaşımının uzmanı

Passbolt özellikle sistem yöneticileri, ajanslar ve geliştirici ekipleri için tasarlanmıştır. Kayıtların kullanıcı veya gruplarla kontrollü paylaşılması, erişimlerin kaldırılması ve değişikliklerin izlenmesi temel senaryolardır. OpenPGP tabanlı yaklaşımı nedeniyle anahtar yönetimi önemli bir rol oynar.

Kişisel otomatik doldurma deneyimi önceliğinizse Bitwarden ailesi daha doğal gelebilir. Çok sayıda çalışanın ortak altyapı parolalarına farklı yetkilerle erişmesi gerekiyorsa Passbolt daha anlamlıdır.

## Hangisini seçmelisiniz?

Bakım istemeyen bireyler için **Bitwarden bulutu**, düşük kaynaklı kendi sunucusunu yönetecek meraklılar için **Vaultwarden**, ekip paylaşımını merkeze alan kuruluşlar için **Passbolt** güçlü adaylardır. Hangi aracı seçerseniz seçin; güçlü ana parola, MFA, HTTPS, güncelleme ve test edilmiş yedekler vazgeçilmezdir. Unutmayın: Self-hosted sistem otomatik olarak daha güvenli değil, yalnızca güvenlik sorumluluğunun adresi farklıdır.
