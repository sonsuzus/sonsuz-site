---
layout: post
title: "Veritabanı Yönetim Arenası: phpMyAdmin, Adminer ve CloudBeaver"
math: true
categories: 
  - Bilgi
tags: 
  - veritabanı
  - phpmyadmin
  - adminer
  - cloudbeaver
  - sql
  - devops
toc: true
image: /img/veritabani-yonetim-arenasi-20.png
---

Veritabanını yalnızca terminal üzerinden yönetmek mümkündür; ancak yüzlerce tablo, karmaşık ilişkiler ve acil bir veri düzeltmesi söz konusu olduğunda görsel yönetim panelleri hayat kurtarır. Bu alanda phpMyAdmin köklü bir klasik, Adminer hafif bir cep çakısı, CloudBeaver ise çok sayıda veritabanını yönetebilen modern bir kontrol merkezi gibidir.

``

## Yönetim paneli ne işe yarar?

Bir veritabanı yönetim paneli; SQL sorgusu çalıştırma, tablo oluşturma, kayıt düzenleme, kullanıcı yetkilerini denetleme ve yedek alma gibi işlemleri grafiksel arayüz üzerinden gerçekleştirir. Panel, veritabanının yerine geçmez; istemci olarak veritabanı sunucusuna bağlanır ve komutları kullanıcı adına iletir.

Performansı kabaca değerlendirmek için basit bir maliyet modeli kullanabiliriz:

$$T_{toplam} = T_{bağlantı} + T_{sorgu} + T_{arayüz}$$

Burada $T_{arayüz}$ panelin sonucu işleme ve tarayıcıya gönderme süresidir. Milyonlarca satırın tamamını ekranda açmaya çalışırsanız en şık panel bile küçük bir kahve molası talep edebilir. Bu nedenle sayfalama ve `LIMIT` kullanımı önemlidir.

## Üç aracın karakteri

| Özellik | phpMyAdmin | Adminer | CloudBeaver |
|---|---|---|---|
| Temel teknoloji | PHP | Tek PHP dosyası | Java ve web arayüzü |
| Veritabanı desteği | MySQL, MariaDB | MySQL, PostgreSQL, SQLite ve diğerleri | PostgreSQL, MySQL, Oracle, SQL Server ve daha fazlası |
| Kaynak tüketimi | Orta | Çok düşük | Görece yüksek |
| Kurulum yaklaşımı | Web sunucusuna dağıtım | Tek dosya | Sunucu veya Docker |
| İdeal kullanım | MySQL odaklı hosting | Hızlı ve geçici yönetim | Ekipler ve çoklu bağlantılar |

### phpMyAdmin: Tanıdık klasik

phpMyAdmin, özellikle paylaşımlı hosting dünyasının demirbaşlarındandır. MySQL ve MariaDB üzerinde tablo tasarlamak, içe aktarma yapmak, indeksleri incelemek ve kullanıcı yetkilerini düzenlemek için geniş bir araç seti sunar. Arayüzü bazen bir uçağın kokpiti kadar düğmeli görünse de kapsamlıdır.

Dezavantajı, yalnızca MySQL ekosistemine odaklanması ve internete açık bırakıldığında saldırganların dikkatini çekmesidir. Güncel sürüm kullanmak, IP kısıtlaması uygulamak ve çok faktörlü kimlik doğrulamayı ters proxy üzerinden sağlamak gerekir.

### Adminer: Tek dosyalık kahraman

Adminer’ın en dikkat çekici özelliği tek bir PHP dosyası olarak çalışabilmesidir. PHP destekli bir dizine dosyayı yerleştirerek arayüzü açabilirsiniz:

```bash
mkdir -p /var/www/tools/adminer
cd /var/www/tools/adminer
wget https://www.adminer.org/latest.php -O index.php
```

Bu komutlar Adminer’ın güncel sürümünü indirip `index.php` adıyla kaydeder. Hafifliği geliştirme ortamları ve kısa süreli bakım görevleri için mükemmeldir. Ancak işiniz bittiğinde dosyayı kaldırmak akıllıca olur; unutulan yönetim araçları güvenlik dünyasının açık bırakılmış arka kapılarıdır.

### CloudBeaver: Takım oyuncusu

CloudBeaver, DBeaver ekosisteminin tarayıcı üzerinden çalışan çözümüdür. Farklı veritabanlarına merkezi bağlantılar tanımlayabilir, kullanıcı rolleri oluşturabilir ve ekiplerin aynı arayüzü kullanmasını sağlayabilirsiniz. Docker ile hızlıca denenebilir:

```bash
docker run --name cloudbeaver \
  --restart unless-stopped \
  -p 8978:8978 \
  -v cloudbeaver-data:/opt/cloudbeaver/workspace \
  dbeaver/cloudbeaver:latest
```

Komut, çalışma alanını kalıcı bir Docker volume içinde saklar ve paneli `8978` portunda yayımlar. Üretimde bu port doğrudan internete açılmamalı; HTTPS kullanan Nginx, Caddy veya benzeri bir ters proxy arkasına alınmalıdır.

## Hangisini seçmeli?

Seçimi bir puanlama modeliyle düşünebiliriz:

$$P = 0.4D + 0.3K + 0.2G + 0.1E$$

Burada $D$ veritabanı uyumu, $K$ kullanım kolaylığı, $G$ güvenlik gereksinimleri ve $E$ ekip özellikleridir. Yalnızca MySQL yönetiyorsanız phpMyAdmin, hızlı ve minimal bir çözüm istiyorsanız Adminer, farklı sistemlere bağlanan bir ekibiniz varsa CloudBeaver öne çıkar.

Hangi aracı seçerseniz seçin paneli güncel tutun, HTTPS kullanın, varsayılan hesapları kapatın ve en az yetki ilkesini uygulayın. Çünkü güzel bir arayüz işleri kolaylaştırır; yanlış yetkilendirilmiş güzel bir arayüz ise felaketi yalnızca daha tıklanabilir hâle getirir.

![veritabani-yonetim-arenasi-20](/img/veritabani-yonetim-arenasi-20.svg)

