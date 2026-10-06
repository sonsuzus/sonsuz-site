---
layout: post
title: "Kendi Bulutunu Kur: Nextcloud, ownCloud ve Seafile Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - nextcloud
  - owncloud
  - seafile
  - bulut
  - dosya-paylaşımı
  - açık-kaynak
toc: true
image: /img/kendi-bulutunu-kur-72.png
---

![kendi-bulutunu-kur-72](/img/kendi-bulutunu-kur-72.svg)


Google Drive veya Dropbox kullanışlıdır; ancak verilerinizin nerede tutulduğu, kimler tarafından işlendiği ve hizmet koşullarının ne zaman değişeceği sizin kontrolünüzde değildir. Nextcloud, ownCloud ve Seafile ise kendi sunucunuzda çevrim içi dosya paylaşım sistemi kurmanıza olanak tanır. Böylece bulutun anahtarı gerçekten cebinizde olur—tabii sunucu parolasını unutmazsanız!
``

## Kişisel bulutun temel mantığı

Bu sistemlerin merkezinde **istemci-sunucu mimarisi** bulunur. Dosyalar merkezi bir sunucuda saklanır; masaüstü uygulaması, mobil uygulama veya web tarayıcısı üzerinden erişilir. Bir dosya değiştirildiğinde istemci, değişikliği sunucuya gönderir ve diğer cihazlar güncel sürümü indirir.

Basit bir senkronizasyon süresi yaklaşık olarak şöyle modellenebilir:

$$
T = \frac{S}{B} + L
$$

Burada $S$ dosya boyutunu, $B$ kullanılabilir aktarım hızını, $L$ ise ağ gecikmesi ve işlem maliyetini temsil eder. Örneğin 100 MB büyüklüğündeki dosyanın gerçek yükleme hızı 10 MB/s ise gecikmeler hariç aktarım yaklaşık $10$ saniye sürer.

Dosya bütünlüğü için karma değerleri kullanılır. Sistem, dosyanın önceki ve sonraki özetlerini karşılaştırır:

$$
H_{yerel} = H_{sunucu}
$$

Eşitlik sağlanıyorsa iki kopya aynıdır. Sağlanmıyorsa senkronizasyon veya çakışma çözümü gerekir.

## Üç sistem arasındaki farklar

| Özellik | Nextcloud | ownCloud | Seafile |
|---|---|---|---|
| Temel yaklaşım | Tam kapsamlı iş birliği platformu | Kurumsal dosya paylaşımı | Hızlı dosya senkronizasyonu |
| Eklenti ekosistemi | Çok geniş | Daha kontrollü | Daha sınırlı |
| Takvim ve kişiler | Yerleşik uygulamalarla güçlü | Desteklenir | Ana odak değildir |
| Büyük dosya performansı | İyi | İyi | Genellikle çok iyi |
| Kaynak tüketimi | Görece yüksek | Orta | Görece düşük |
| Uygun kullanım | Kişisel bulut ve ekip çalışması | Kurumsal ortam | Performans odaklı arşivleme |

**Nextcloud**, dosya depolamanın ötesine geçer. Takvim, kişiler, görüntülü görüşme, görev yönetimi ve çevrim içi ofis entegrasyonları sunar. “Kendi Google Workspace’imi kurayım” diyenler için güçlü bir seçimdir.

**ownCloud**, Nextcloud ile ortak bir geçmişe sahiptir; ancak günümüzde özellikle kurumsal yönetim, güvenlik politikaları ve ölçeklenebilir dağıtımlar üzerinde yoğunlaşır. Daha kontrollü ve profesyonel destek gerektiren şirket ortamlarında öne çıkar.

**Seafile** ise dosyaları bloklara ayırarak yönetir. Yalnızca değişen blokların aktarılması, büyük dosyalarda ciddi hız avantajı sağlayabilir. Bir dosyanın yalnızca $p$ oranı değişmişse yaklaşık aktarım miktarı $S \times p$ olur. 2 GB dosyanın %5’i değiştiğinde teorik olarak 2 GB yerine yaklaşık 100 MB aktarılması yeterlidir.

## Docker ile örnek Nextcloud kurulumu

Aşağıdaki yapı, Nextcloud ile MariaDB servislerini çalıştırır:

```yaml
services:
  db:
    image: mariadb:11
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: guclu-root-parolasi
      MYSQL_DATABASE: nextcloud
      MYSQL_USER: nextcloud
      MYSQL_PASSWORD: guclu-kullanici-parolasi
    volumes:
      - db_data:/var/lib/mysql

  app:
    image: nextcloud:apache
    restart: always
    ports:
      - "8080:80"
    environment:
      MYSQL_HOST: db
      MYSQL_DATABASE: nextcloud
      MYSQL_USER: nextcloud
      MYSQL_PASSWORD: guclu-kullanici-parolasi
    volumes:
      - nextcloud_data:/var/www/html
    depends_on:
      - db

volumes:
  db_data:
  nextcloud_data:
```

Dosyayı `compose.yaml` adıyla kaydettikten sonra şu komut servisleri arka planda başlatır:

```bash
docker compose up -d
```

Ardından `http://sunucu-adresi:8080` açılarak yönetici hesabı oluşturulur. Gerçek kullanımda HTTPS, güvenlik duvarı, düzenli güncelleme ve harici yedekleme mutlaka yapılandırılmalıdır. Unutmayın: RAID erişilebilirliği artırabilir, fakat tek başına yedek değildir.

## Hangisini seçmelisiniz?

Takvim, ofis, sohbet ve bol eklenti istiyorsanız **Nextcloud**; kurumsal politika ve profesyonel destek öncelikliyse **ownCloud**; yüksek hızlı senkronizasyon ve verimli depolama arıyorsanız **Seafile** daha uygundur. En iyi sistem, en çok özelliğe sahip olan değil; bakımını sürdürebileceğiniz, güvenliğini sağlayabileceğiniz ve gerçekten kullanacağınız sistemdir.
