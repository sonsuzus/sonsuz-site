---
layout: post
title: "Kendi Takvim Sunucunu Seç: Nextcloud Calendar, Radicale ve Baïkal"
math: true
categories: 
  - Program
tags: 
  - takvim
  - caldav
  - nextcloud
  - radicale
  - baikal
  - açık-kaynak
toc: true
image: /img/kendi-takvim-sunucunu-17.png
---

![kendi-takvim-sunucunu-17](/img/kendi-takvim-sunucunu-17.svg)


Toplantılar, doğum günleri ve sürekli ertelediğimiz görevler dijital takvimlerde yaşarken bu verileri kimin sakladığı önemli bir soruya dönüşüyor. Nextcloud Calendar, Radicale ve Baïkal; takvimlerinizi kendi sunucunuzda barındırmanızı sağlayan üç açık kaynaklı seçenek. Aynı protokolleri konuşsalar da kaynak tüketimi, yönetim biçimi ve sundukları ek özellikler bakımından oldukça farklı karakterlere sahipler.
``

## Temel mantık: CalDAV ne yapar?

Bu sistemlerin merkezinde **CalDAV** bulunur. CalDAV, HTTP tabanlı WebDAV protokolünü takvim verileri için genişletir. Etkinlikler çoğunlukla iCalendar biçiminde saklanır ve `.ics` uzantısıyla taşınabilir. Böylece Android, iOS, macOS, Thunderbird ve DAVx⁵ gibi istemciler aynı sunucuyla iletişim kurabilir.

Basitleştirilmiş bir senkronizasyon maliyetini şöyle düşünebiliriz:

$$T = L + \frac{D}{B} + P$$

Burada $L$ ağ gecikmesini, $D$ aktarılan veri miktarını, $B$ bant genişliğini ve $P$ sunucunun işleme süresini temsil eder. Küçük bir aile takviminde üç çözüm de hızlıdır. Binlerce etkinlik ve çok sayıda kullanıcı olduğunda ise veritabanı, önbellek ve PHP/Python süreçlerinin yapılandırılması daha önemli hâle gelir.

CalDAV istemcisi önce takvim koleksiyonlarını keşfeder, değişen nesneleri sorgular ve ardından etkinlikleri indirir. Çakışmalar genellikle `ETag` değerleriyle algılanır. Yani iki cihaz aynı etkinliği değiştirirse sunucu, eski sürüm üzerine sessizce yazmak yerine istemciye değişiklik olduğunu bildirebilir.

## Üç adayın karşılaştırması

| Özellik | Nextcloud Calendar | Radicale | Baïkal |
|---|---|---|---|
| Temel teknoloji | PHP, Nextcloud uygulaması | Python | PHP, SabreDAV |
| Kurulum ağırlığı | Yüksek | Çok düşük | Düşük |
| Web takvim arayüzü | Gelişmiş | Yok denecek kadar sınırlı | Yönetim odaklı |
| Kişiler desteği | Contacts uygulamasıyla | CardDAV ile | CardDAV ile |
| Çok kullanıcılı kullanım | Çok güçlü | Basit ve esnek | Orta düzey |
| En uygun senaryo | Hepsi bir arada bulut | Minimal CalDAV sunucusu | Hafif, panelli DAV sunucusu |

### Nextcloud Calendar

Nextcloud Calendar yalnızca bir CalDAV uç noktası değildir; dosyalar, kişiler, görevler, paylaşım ve kullanıcı yönetimiyle bütünleşen bir platformun parçasıdır. Tarayıcıdan kullanılabilen modern arayüzü sayesinde teknik olmayan kullanıcılar için en rahat seçenektir. Buna karşılık web sunucusu, PHP, veritabanı ve düzenli bakım ister. Zaten Nextcloud kullanıyorsanız takvim uygulamasını eklemek son derece mantıklıdır; yalnızca iki kişinin takvimini barındıracaksanız biraz topa serçeyle ateş etmek olabilir.

### Radicale

Radicale, sadeliği sevenlerin küçük ama becerikli aracıdır. Python ile geliştirilmiştir ve CalDAV ile CardDAV hizmetlerine odaklanır. Kendi gelişmiş takvim arayüzünü sunmaz; kullanıcıların Thunderbird, mobil takvim veya DAVx⁵ gibi istemciler kullanması beklenir. Düşük RAM tüketimi sayesinde Raspberry Pi ve küçük VPS sistemlerinde güzel çalışır.

Örneğin temel bir yapılandırma şöyle olabilir:

```ini
[server]
hosts = 0.0.0.0:5232

[auth]
type = htpasswd
htpasswd_filename = /etc/radicale/users
htpasswd_encryption = bcrypt

[storage]
filesystem_folder = /var/lib/radicale/collections
```

Bu ayar Radicale'i `5232` portunda dinletir, kullanıcı doğrulamasını bcrypt ile korunan bir parola dosyasına bağlar ve koleksiyonları belirlenen dizinde saklar. İnternete açarken önüne Nginx veya Caddy koyup HTTPS kullanmak gerekir.

### Baïkal

Baïkal da CalDAV ve CardDAV odaklıdır ancak web tabanlı yönetim paneliyle Radicale'den daha görsel bir deneyim sunar. SabreDAV üzerine kuruludur ve PHP destekleyen klasik hosting ortamlarında çalıştırılabilir. Kullanıcı ve veritabanı yönetimi kolaydır; buna rağmen son kullanıcıya Nextcloud seviyesinde bir takvim ekranı sağlamaz. Panel, yöneticiler içindir; etkinlikleri görüntülemek için yine harici istemci gerekir.

## Hangisini seçmelisiniz?

Web arayüzü, paylaşım ve ekip özellikleri arıyorsanız **Nextcloud Calendar** öne çıkar. En az kaynakla yalnızca güvenilir senkronizasyon istiyorsanız **Radicale** daha temiz bir seçimdir. PHP hostinginiz varsa ve kullanıcıları panelden yönetmek istiyorsanız **Baïkal** iyi bir orta yol sunar.

Hangi çözümü seçerseniz seçin HTTPS, güçlü parolalar, düzenli yedekleme ve güncelleme şarttır. Takvim verisi küçük görünebilir; fakat ne zaman evde olmadığınızı dünyaya ilan eden oldukça konuşkan bir veri kümesidir.
