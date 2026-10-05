---
layout: post
title: "Kendi Fotoğraf Bulutunu Kur: Pixelfed, Piwigo ve Lychee Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - pixelfed
  - piwigo
  - lychee
  - self-hosted
  - fotoğraf
  - docker
toc: true
image: /img/kendi-fotograf-bulutunu-34.png
---

![kendi-fotograf-bulutunu-34](/img/kendi-fotograf-bulutunu-34.svg)


Fotoğraflarınızı büyük sosyal ağlara teslim etmeden paylaşmak istiyorsanız, kendi sunucunuzu kurmak oldukça özgürleştirici bir seçenek. Pixelfed, Piwigo ve Lychee aynı fotoğraf dosyalarını sergiliyor gibi görünse de farklı problemlere odaklanıyor: Pixelfed sosyal etkileşimi, Piwigo arşiv yönetimini, Lychee ise sade ve kişisel galerileri öne çıkarıyor.
``

## Üç farklı yaklaşım

Pixelfed, Instagram benzeri bir deneyimi açık kaynak dünyasına taşır. Kullanıcılar hesap açabilir, birbirini takip edebilir, gönderileri beğenebilir ve yorum yazabilir. En önemli özelliği, ActivityPub protokolü sayesinde Mastodon gibi diğer Fediverse uygulamalarıyla iletişim kurabilmesidir.

Piwigo daha çok kapsamlı bir dijital fotoğraf arşividir. Albümler, etiketler, kullanıcı yetkileri, toplu yükleme ve eklenti sistemi sunar. Bir fotoğraf kulübü, okul, şirket veya yıllara yayılan aile arşivi için güçlü bir seçimdir.

Lychee ise işleri basit tutar. Temiz arayüzü, hızlı albüm oluşturma sistemi ve bağlantıyla paylaşma özellikleriyle kişisel sunucusunda şık bir galeri isteyenlere hitap eder.

| Özellik | Pixelfed | Piwigo | Lychee |
|---|---|---|---|
| Temel amaç | Sosyal fotoğraf ağı | Arşiv ve galeri yönetimi | Minimal kişisel galeri |
| Çoklu kullanıcı | Güçlü | Güçlü ve yetkilendirilebilir | Daha sınırlı |
| Federasyon | ActivityPub | Yerleşik değil | Yerleşik değil |
| Eklenti desteği | Sınırlı | Çok geniş | Sınırlı |
| Kurulum zorluğu | Yüksek | Orta | Düşük-orta |
| En uygun senaryo | Topluluk | Büyük arşiv | Kişisel kullanım |

## Teknik mantık: Fotoğraf sunmak neden maliyetlidir?

Bir fotoğraf platformu yalnızca dosyayı diske kaydetmez. Yüklenen görselin küçük önizlemelerini üretir, EXIF bilgilerini okuyabilir, erişim izinlerini denetler ve dosyayı web üzerinden iletir. Yaklaşık depolama ihtiyacı şöyle hesaplanabilir:

$$D = N \times (O + T)$$

Burada $N$ fotoğraf sayısı, $O$ ortalama orijinal dosya boyutu, $T$ ise küçük ve orta boy önizlemelerin toplamıdır. Örneğin 10.000 adet 6 MB fotoğraf ve fotoğraf başına 1 MB önizleme için yaklaşık $10.000 \times 7 = 70.000$ MB, yani 70 GB gerekir. Yedekleme alanı bunun dışında düşünülmelidir.

Pixelfed; web uygulamasına ek olarak kuyruk çalışanları, önbellek ve zamanlanmış görevler kullanabildiği için daha fazla RAM ve yönetim ister. Piwigo klasik PHP ve veritabanı mimarisiyle daha tanıdıktır. Lychee de PHP tabanlıdır ve küçük kurulumlarda oldukça hafif çalışabilir.

## Docker ile temel hazırlık

Ürüne özel dosyalar değişebilse de bütün kurulumlarda kalıcı veri mantığı aynıdır. Aşağıdaki örnek, bir galeri uygulamasının veritabanı parolasını çevre değişkenlerinden almasını ve fotoğrafları kalıcı bir dizinde saklamasını gösterir:

```yaml
services:
  gallery:
    image: uygulama-imaji:latest
    restart: unless-stopped
    environment:
      DB_HOST: database
      DB_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./photos:/var/www/html/uploads
    depends_on:
      - database

  database:
    image: mariadb:11
    restart: unless-stopped
    environment:
      MARIADB_ROOT_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./database:/var/lib/mysql
```

Bu yapıdaki `volumes` bölümü kritiktir; konteyner silinse bile fotoğraflar ve veritabanı korunur. Gerçek kurulumda uygulamanın resmî Docker belgelerindeki imaj adı, dizin yolları ve değişkenler kullanılmalıdır. Ayrıca HTTPS için Caddy, Traefik veya Nginx gibi bir ters vekil eklenmelidir.

## Hangisini seçmelisiniz?

Kararı küçük bir ağırlıklı puan modeliyle verebilirsiniz:

$$P = 0.4S + 0.35A + 0.25K$$

Burada $S$ sosyal özellikler, $A$ arşiv yetenekleri, $K$ ise kurulum kolaylığı puanıdır. Sosyal ağ kurmak istiyorsanız Pixelfed açık ara öne çıkar. On binlerce fotoğrafı sınıflandırmak ve farklı kullanıcılara yetki vermek için Piwigo daha mantıklıdır. Hafta sonu kurulabilecek şık, özel ve dikkat dağıtmayan bir galeri arıyorsanız Lychee tatlı noktayı yakalar.

Hangi uygulamayı seçerseniz seçin, otomatik yedekleme, HTTPS, güçlü parolalar ve düzenli güncelleme zorunludur. Çünkü fotoğraf sunucusunda kaybedilen şey yalnızca birkaç dosya değil, çoğu zaman yılların anılarıdır.
