---
layout: post
title: "Kendi Web Tabanlı E-Posta Sisteminizi Kurun: Roundcube, SnappyMail ve RainLoop Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - webmail
  - roundcube
  - snappymail
  - rainloop
  - e-posta
  - imap
  - smtp
  - linux
toc: true
image: /img/kendi-web-tabanli-32.png
---

Tarayıcıdan e-posta okumak basit görünür: adresi aç, şifreyi gir ve gelen kutusuna dal. Ancak perde arkasında IMAP, SMTP, MIME, TLS ve PHP gibi birçok bileşen birlikte çalışır. Roundcube, SnappyMail ve RainLoop; mevcut posta sunucularına kullanıcı dostu bir web arayüzü ekleyen, kendi sunucunuzda barındırabileceğiniz webmail uygulamalarıdır.
``
## Webmail gerçekte ne yapar?

Bu uygulamalar genellikle e-postaları kendi başına taşımaz veya saklamaz. Tarayıcı ile posta altyapısı arasında istemci görevi görürler. Gelen mesajlar **IMAP** üzerinden okunurken giden mesajlar **SMTP** sunucusuna teslim edilir.

Basitleştirilmiş akış şöyledir:

$$Tarayıcı \rightarrow Webmail \rightarrow IMAP/SMTP \rightarrow Posta\ Sunucusu$$

IMAP klasörleri ve okunma durumlarını sunucuda tutar. Bu nedenle telefonda okunan mesaj webmail üzerinde de okunmuş görünür. SMTP ise mesajı alıcı sunucuya gönderen posta aktarım mekanizmasıdır. Webmail kurmak, tek başına tam bir e-posta sunucusu kurmak anlamına gelmez; Dovecot, Postfix veya harici bir e-posta hizmeti hâlâ gereklidir.

Bir webmail sisteminin yaklaşık yanıt süresini şöyle düşünebiliriz:

$$T_{toplam}=T_{tarayıcı}+T_{PHP}+T_{IMAP}+T_{ağ}$$

Büyük posta kutularında IMAP sorguları ve ağ gecikmesi yükseldikçe arayüz yavaşlayabilir. Önbellekleme ve doğru PHP yapılandırması bu yüzden önemlidir.

## Üç adayın karşılaştırması

| Özellik | Roundcube | SnappyMail | RainLoop |
|---|---|---|---|
| Proje durumu | Aktif ve olgun | Aktif, modern çatallanma | Büyük ölçüde terk edilmiş | 
| Arayüz | Klasik ve işlevsel | Hızlı ve modern | Sade ve modern |
| Eklenti ekosistemi | Çok geniş | Gelişmekte | Sınırlı |
| Veritabanı | Genellikle gerekli | Temel kullanımda gerekmeyebilir | Temel kullanımda gerekmeyebilir |
| Çoklu hesap | Eklentilerle veya yapılandırmayla | Güçlü destek | Desteklenir |
| Uygun senaryo | Kurumsal ve kararlı sistemler | Hafif, kişisel veya modern kurulumlar | Yeni kurulumlarda önerilmez |

### Roundcube

Roundcube yıllardır kullanılan, güvenilir ve geniş eklenti desteğine sahip bir seçenektir. Kişiler, filtreler, takvim eklentileri ve kurumsal kimlik doğrulama çözümleriyle genişletilebilir. Dezavantajı, SnappyMail'e göre daha ağır hissettirebilmesi ve kurulumda bir veritabanı istemesidir. Uzun vadeli bakım ve topluluk desteği sizin için önemliyse güçlü adaydır.

### SnappyMail

SnappyMail, RainLoop kod tabanından doğmuş, güvenlik ve modernizasyon odaklı bir devam projesidir. Hafif yapısı, birden fazla hesabı aynı arayüzde kullanabilmesi ve kolay yönetim paneliyle dikkat çeker. Küçük sunucular ve kişisel alan adları için oldukça pratiktir. Yine de üretim ortamında sürümleri düzenli takip etmek gerekir.

### RainLoop

RainLoop bir dönem şık arayüzü ve kolay kurulumu sayesinde çok popülerdi. Fakat projenin bakım temposu ciddi biçimde düştü ve güvenlik güncellemeleri konusunda belirsizlik oluştu. Çalışan eski sistemlerde görülebilir; ancak internete açık yeni bir kurulum için SnappyMail'e geçmek daha sağlıklı bir tercihtir.

## Örnek SnappyMail kurulumu

Ubuntu üzerinde gerekli paketleri yükleyelim:

```bash
sudo apt update
sudo apt install nginx php-fpm php-curl php-xml php-mbstring php-zip unzip
sudo mkdir -p /var/www/snappymail
sudo chown -R www-data:www-data /var/www/snappymail
```

Bu komutlar web sunucusunu, PHP çalışma ortamını ve SnappyMail'in ihtiyaç duyduğu uzantıları hazırlar. Ardından resmi dağıtım paketi proje sitesinden indirilip bu dizine açılmalıdır. Dosyaları rastgele kaynaklardan indirmek, webmail şifrelerini saldırganlara hediye etmekle eşdeğerdir.

Nginx tarafında temel kök dizin tanımlaması şöyle olabilir:

```nginx
server {
    listen 443 ssl;
    server_name mail.ornek.com;
    root /var/www/snappymail;
    index index.php;

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php-fpm.sock;
    }
}
```

Gerçek kurulumda PHP soket yolu sürüme göre düzenlenmeli, TLS sertifikası eklenmeli ve yönetim paneli güçlü bir parolayla korunmalıdır.

## Hangisini seçmelisiniz?

Kararlılık, eklenti çeşitliliği ve kurumsal kullanım için **Roundcube**; hızlı, hafif ve çağdaş bir deneyim için **SnappyMail** daha uygundur. **RainLoop** ise tarihsel açıdan önemli olsa da yeni projelerde tercih edilmemelidir. Hangi uygulamayı seçerseniz seçin HTTPS, güncel paketler, güçlü parolalar, iki aşamalı doğrulama ve düzenli yedekleme zorunlu olmalıdır. Sonuçta webmail yalnızca güzel bir gelen kutusu değil, dijital hayatınızın ön kapısıdır.

![kendi-web-tabanli-32](/img/kendi-web-tabanli-32.svg)

