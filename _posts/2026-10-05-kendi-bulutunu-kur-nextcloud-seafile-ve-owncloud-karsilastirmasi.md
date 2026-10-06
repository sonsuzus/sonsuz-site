---
layout: post
title: "Kendi Bulutunu Kur: Nextcloud, Seafile ve ownCloud Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - bulut depolama
  - nextcloud
  - seafile
  - owncloud
  - docker
  - dosya senkronizasyonu
toc: true
image: /img/kendi-bulutunu-kur-82.png
---

Fotoğraflarınızın, belgelerinizin ve projelerinizin başkasının sunucusunda yaşamasından sıkıldıysanız kendi bulut depolama sisteminizi kurabilirsiniz. Nextcloud, Seafile ve ownCloud; dosyaları cihazlar arasında eşitleyen, paylaşım bağlantıları oluşturan ve verinin kontrolünü size bırakan üç güçlü açık kaynak çözümüdür. Ancak benzer görünseler de depolama mimarileri, performansları ve sundukları araçlar bakımından farklı karakterlere sahiptir.


![kendi-bulutunu-kur-82](/img/kendi-bulutunu-kur-82.svg)

``

## Kişisel bulut gerçekte nasıl çalışır?

Kişisel bulut, yalnızca internetten erişilen süslü bir klasör değildir. Sistem genellikle bir web uygulaması, veritabanı, dosya depolama alanı ve masaüstü ya da mobil istemcilerden oluşur. İstemci bir dosyanın değiştiğini algılar, sunucuya gönderir ve diğer cihazlara yeni sürümün bulunduğunu bildirir.

Kabaca toplam aktarım süresi şu şekilde modellenebilir:

$$T = L + S / B + P$$

Burada $L$ ağ gecikmesini, $S$ dosya boyutunu, $B$ kullanılabilir bant genişliğini ve $P$ sunucunun işleme süresini ifade eder. Küçük dosyaların sayısı arttığında gecikme ve işleme maliyeti daha görünür hâle gelir. Bu nedenle sadece internet hızına bakarak performans tahmini yapmak yanıltıcıdır.

Senkronizasyon sırasında dosya sürümleri ve çakışmalar da önemlidir. Aynı belge iki cihazda çevrim dışı düzenlenirse sistem çoğunlukla iki kopyayı da korur. Böylece veri kaybı önlenir; fakat hangi sürümün doğru olduğuna kullanıcının karar vermesi gerekebilir.

## Üç platformun karakteri

| Özellik | Nextcloud | Seafile | ownCloud |
|---|---|---|---|
| Temel yaklaşım | Uygulama ekosistemi | Hızlı dosya eşitleme | Kurumsal dosya paylaşımı |
| Dosya yapısı | Doğrudan dosyalar | Blok ve kütüphane temelli | Doğrudan dosyalar |
| Ek araçlar | Takvim, kişiler, ofis, sohbet | Daha sınırlı | Sürüme göre değişken |
| Yönetim kolaylığı | Orta | Orta | Orta |
| Uygun senaryo | Hepsi bir arada bulut | Büyük ve sık değişen dosyalar | Kurumsal entegrasyon |

**Nextcloud**, yalnızca depolama değil, küçük bir dijital çalışma alanı sunar. Takvim, görev, kişi yönetimi, görüntülü görüşme ve çevrim içi ofis entegrasyonları kurulabilir. Eklenti bolluğunun bedeli ise daha yüksek RAM tüketimi ve bakım ihtiyacıdır.

**Seafile**, dosyaları bloklara ayıran yaklaşımıyla özellikle büyük dosyalardaki küçük değişiklikleri verimli aktarabilir. Örneğin 2 GB büyüklüğündeki bir dosyanın yalnızca belirli blokları değiştiyse her seferinde dosyanın tamamını göndermek gerekmeyebilir. Buna karşılık dosyalara sunucunun diskinden doğrudan müdahale etmek uygun değildir; veriler Seafile’ın yönettiği yapı içinde tutulur.

**ownCloud**, Nextcloud ile ortak bir geçmişe sahiptir ve dosya paylaşımı odağını korur. Kurumsal kimlik doğrulama, erişim politikaları ve destek beklentisi bulunan yapılarda değerlendirilebilir. Ürün seçerken Community ve kurumsal sürümlerdeki özellik farkları mutlaka incelenmelidir.

## Docker ile örnek Nextcloud kurulumu

Aşağıdaki `compose.yaml`, deneme ortamı için Nextcloud ile MariaDB servislerini başlatır:

```yaml
services:
  db:
    image: mariadb:11
    restart: unless-stopped
    environment:
      MARIADB_DATABASE: nextcloud
      MARIADB_USER: nextcloud
      MARIADB_PASSWORD: guclu-parola
      MARIADB_ROOT_PASSWORD: kok-parolasi
    volumes:
      - db_data:/var/lib/mysql

  app:
    image: nextcloud:apache
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      MYSQL_DATABASE: nextcloud
      MYSQL_USER: nextcloud
      MYSQL_PASSWORD: guclu-parola
      MYSQL_HOST: db
    volumes:
      - nextcloud_data:/var/www/html
    depends_on:
      - db

volumes:
  db_data:
  nextcloud_data:
```

Dosyanın bulunduğu dizinde `docker compose up -d` komutunu çalıştırdıktan sonra `http://sunucu-ip:8080` adresi açılır. Parolaları gerçek kurulumda `.env` dosyasına veya bir secret yöneticisine taşımak gerekir.

## Güvenlik ve yedekleme unutulmamalı

Kendi bulutunuzu yönetmek özgürlük kadar sorumluluk da getirir. HTTPS kullanın, çok faktörlü kimlik doğrulamayı etkinleştirin, yazılımları güncel tutun ve yönetici hesabını günlük kullanım için tercih etmeyin. Ayrıca RAID’in yedekleme olmadığını hatırlayın. Sağlam bir plan; veritabanını, yapılandırmayı ve dosyaları ayrı bir ortama düzenli olarak kopyalamalıdır.

Geniş uygulama dünyası istiyorsanız Nextcloud, ham senkronizasyon performansına öncelik veriyorsanız Seafile, kurumsal dosya paylaşımı ve profesyonel destek arıyorsanız ownCloud güçlü adaydır. En iyi seçim, özellik listesinden çok kullanım senaryonuza ve sistemi ne kadar bakım yaparak sürdürebileceğinize bağlıdır.
