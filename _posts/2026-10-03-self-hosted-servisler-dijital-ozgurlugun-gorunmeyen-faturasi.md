---
layout: post
title: "Self-Hosted Servisler: Dijital Özgürlüğün Görünmeyen Faturası"
math: true
categories: 
  - Bilgi
tags: 
  - self-hosted
  - açık kaynak
  - veri mahremiyeti
  - devops
  - yedekleme
  - siber güvenlik
toc: true
image: /img/self-hosted-servisler-41.png
---

Şirket verilerini başka bir firmanın bulutuna emanet etmek yerine kendi sunucunuzda saklamak kulağa dijital bağımsızlık bildirgesi gibi gelir. Nextcloud, GitLab, Mattermost veya Bitwarden gibi açık kaynak servislerle verinin nerede durduğunu bilirsiniz. Ancak özgürlük paketinden yalnızca mahremiyet çıkmaz; yanında güncelleme, izleme, güvenlik ve yedekleme sorumluluğu da gelir.


![self-hosted-servisler-41](/img/self-hosted-servisler-41.svg)

``

## Self-hosted tam olarak ne demek?

Self-hosted yaklaşımda uygulama, veritabanı ve dosyalar sizin yönettiğiniz fiziksel ya da sanal altyapıda çalışır. Sunucu şirket ofisinde bulunabilir veya kiraladığınız bir veri merkezinde barındırılabilir. Temel ayrım, donanımın konumundan çok **yönetim yetkisinin ve sorumluluğun kimde olduğudur**.

Bir SaaS ürününde güncellemeleri sağlayıcı gerçekleştirir. Kendi sisteminizdeyse gece yarısı gelen kritik güvenlik duyurusu doğrudan sizin yapılacaklar listenize eklenir. Başka bir deyişle kontrol arttıkça operasyon yükü de büyür.

Bu ilişkiyi basitçe şöyle düşünebiliriz:

$$
Toplam\ Maliyet = Altyapı + İşçilik + Risk + Kesinti\ Maliyeti
$$

Lisans ücretinin sıfır olması, toplam maliyetin de sıfır olduğu anlamına gelmez. Bir sistem yöneticisinin zamanı, test ortamı ve felaket kurtarma çalışmaları görünmeyen maliyetlerdir.

## Bulut mu, kendi kalen mi?

| Ölçüt | Self-hosted | Yönetilen bulut servisi |
|---|---|---|
| Veri kontrolü | Çok yüksek | Sağlayıcı politikalarına bağlı |
| İlk kurulum | Daha zahmetli | Genellikle birkaç dakika |
| Güncelleme | Ekibin sorumluluğunda | Sağlayıcı tarafından yapılır |
| Özelleştirme | Oldukça esnek | Paketle sınırlı olabilir |
| Yedekleme | Tasarlanmalı ve sınanmalı | Çoğunlukla hazır sunulur |
| Operasyon riski | Kurumda | Kısmen sağlayıcıda |

Self-hosting özellikle kişisel veri, ticari sır, kaynak kodu veya mevzuata tabi kayıt işleyen şirketler için güçlü bir seçenektir. Buna karşılık yeterli teknik kadrosu bulunmayan küçük bir ekip, verilerini korumaya çalışırken yanlış yapılandırılmış bir sunucuyla daha büyük bir güvenlik açığı oluşturabilir.

## Yedek varsa huzur var mı?

Hayır; yalnızca geri yüklenebilen yedek gerçektir. Sağlam bir yaklaşım için **3-2-1 kuralı** uygulanabilir: Verinin üç kopyası, iki farklı ortamı ve bunlardan birinin farklı bir konumda bulunması.

Kabul edilebilir veri kaybı RPO, hizmetin ne kadar sürede geri dönmesi gerektiği ise RTO ile ifade edilir. Saatte bir yedek alıyorsanız teorik olarak:

$$
RPO \leq 1\ saat
$$

Ancak bozuk yedekleri aylarca çoğaltıyorsanız bu denklem yalnızca moral verir. Periyodik geri yükleme tatbikatları bu nedenle zorunludur.

Aşağıdaki örnek, Docker Compose ile çalışan bir PostgreSQL veritabanını tarih damgasıyla yedekler:

```bash
#!/bin/bash
set -e
DATE=$(date +%F-%H%M)
BACKUP_DIR=/srv/backups

mkdir -p "$BACKUP_DIR"
docker compose exec -T db \
  pg_dump -U appuser appdb | gzip \
  > "$BACKUP_DIR/appdb-$DATE.sql.gz"

find "$BACKUP_DIR" -type f -mtime +14 -delete
```

Betik veritabanı dökümünü sıkıştırır ve 14 günden eski yerel kopyaları siler. Fakat tek başına yeterli değildir: Çıktı şifrelenmeli, uzak bir konuma aktarılmalı, işlem sonucu izlenmeli ve geri yükleme testi yapılmalıdır.

## Yönetim yükü nasıl azaltılır?

Öncelikle her şeyi self-hosted yapmaya çalışmayın. Verinin hassasiyeti ile operasyon becerisini birlikte değerlendirin. Kimlik yönetimi, otomatik güvenlik güncellemeleri, merkezi loglama ve çalışma süresi izleme başlangıçtan itibaren tasarlanmalıdır.

Ansible gibi yapılandırma araçları tekrar eden işleri otomatikleştirirken Docker sürüm tutarlılığı sağlayabilir. Yine de otomasyon, sorumluluğu ortadan kaldırmaz; yalnızca insan hatasının dolaşabileceği alanı küçültür.

En dengeli model çoğu zaman hibrittir: Kritik veriler kurum kontrolünde tutulurken e-posta teslimatı veya trafik filtreleme gibi uzmanlık isteyen hizmetler güvenilir sağlayıcılara bırakılır. Self-hosting bir prestij rozeti değil, bilinçli bir risk yönetimi kararıdır. Özgürlüğün tadını çıkarabilmek için sunucunun bakım takvimini de sevmek gerekir.
