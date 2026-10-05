---
layout: post
title: "Açık Kaynak Newsletter Üçlüsü: Listmonk, Mautic ve phpList Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - newsletter
  - listmonk
  - mautic
  - phplist
  - e-posta
  - açık-kaynak
  - docker
toc: true
image: /img/acik-kaynak-newsletter-70.png
---

![acik-kaynak-newsletter-70](/img/acik-kaynak-newsletter-70.svg)


Bir newsletter sistemi seçmek, yalnızca “hangi araç e-posta gönderiyor?” sorusunu yanıtlamak değildir. Abone sayısı, otomasyon ihtiyacı, sunucu kapasitesi, ekip deneyimi ve gönderim sıklığı kararın parçalarıdır. Açık kaynak dünyasında Listmonk, Mautic ve phpList aynı hedefe farklı rotalardan gider: Listmonk hız ve sadeliğe, Mautic pazarlama otomasyonuna, phpList ise geleneksel liste yönetimine odaklanır.
``
## Önce temel mantık: Newsletter nasıl çalışır?

Bir newsletter altyapısı üç ana katmandan oluşur: kişi ve liste yönetimi, kampanya orkestrasyonu ve e-posta teslimatı. Uygulama mesajı hazırlar; gerçek gönderim çoğunlukla SMTP, Amazon SES veya Mailgun gibi bir servis üzerinden gerçekleşir. Dolayısıyla yazılımı kurmak, iletilerin otomatik olarak gelen kutusuna düşeceği anlamına gelmez.

Basit bir teslimat oranı şöyle ifade edilebilir:

$$
R = \frac{D}{S} \times 100
$$

Burada $S$ gönderilen, $D$ başarıyla teslim edilen e-posta sayısıdır. Örneğin 10.000 iletiden 9.700'ü teslim edilirse oran $R=97\%$ olur. Ancak açılma oranı, tıklama oranı, geri dönüşler ve spam şikâyetleri de izlenmelidir. SPF, DKIM ve DMARC yapılandırmaları ise alan adınızın dijital kimlik kartları gibidir.

## Üç aracın karakteri

| Özellik | Listmonk | Mautic | phpList |
|---|---|---|---|
| Temel yaklaşım | Hızlı newsletter yönetimi | Kapsamlı pazarlama otomasyonu | Klasik e-posta listeleri |
| Teknoloji | Go, PostgreSQL | PHP, MySQL/MariaDB | PHP, MySQL/MariaDB |
| Kaynak tüketimi | Düşük | Yüksek | Orta |
| Otomasyon | Sınırlı | Çok güçlü | Temel |
| Öğrenme eğrisi | Kolay | Dik | Orta |
| İdeal kullanıcı | Geliştirici ve yayıncı | Pazarlama ekibi | Topluluk ve kurum |

### Listmonk: Hızlı ve yalın

Listmonk, yüksek hacimli listeleri düşük kaynak tüketimiyle yönetmek isteyenler için güçlü bir seçenektir. Go ile yazılmış tek uygulaması ve PostgreSQL altyapısı sayesinde kurulumu nispeten rahattır. Segmentler, şablonlar, analitik ve API desteği sunar. Buna karşılık görsel otomasyon akışları veya ayrıntılı müşteri yolculukları bekleyen ekipleri sınırlayabilir.

Docker ile temel kurulum şu şekilde başlatılabilir:

```bash
# Yapılandırmayı hazırlar ve veritabanı tablolarını oluşturur.
docker compose run --rm app ./listmonk --install

# Uygulama ile PostgreSQL servisini arka planda çalıştırır.
docker compose up -d
```

Bu komutlardan sonra SMTP bilgileri yönetim panelinden tanımlanmalıdır. Üretimde güçlü parolalar, ters proxy, HTTPS ve düzenli yedekleme unutulmamalıdır.

### Mautic: Otomasyon canavarı

Mautic yalnızca newsletter göndermez; kişi puanlama, form oluşturma, açılış sayfaları, segmentler ve koşullu kampanyalar sunar. Örneğin kullanıcı bağlantıya tıklarsa puanını artırabilir, üç gün bekleyip farklı bir mesaj gönderebilirsiniz. Bu güç beraberinde cron görevleri, kuyruk yönetimi, önbellek ve daha ciddi sunucu gereksinimleri getirir.

Mautic şu mantıkla parlar:

```text
Form dolduruldu
  -> Kişiyi segmente ekle
  -> Hoş geldin e-postası gönder
  -> 3 gün bekle
  -> Tıklama varsa teklif gönder
```

Satış hunisi ve davranış tabanlı iletişim gerekiyorsa üçlü içindeki en yetenekli seçenek odur.

### phpList: Tecrübeli emektar

phpList uzun süredir kullanılan, güvenilir bir liste yönetim aracıdır. Kampanya zamanlama, şablon, abonelik sayfası ve liste bazlı gönderim gibi temel ihtiyaçları karşılar. Arayüzü modern rakipleri kadar akıcı görünmeyebilir; buna rağmen geleneksel PHP hosting ortamlarında çalışabilmesi önemli avantajdır. Karmaşık otomasyonlardan çok düzenli duyuru gönderen dernekler, okullar ve topluluklar için mantıklıdır.

## Hangisini seçmelisiniz?

Sade API, yüksek performans ve düşük bakım istiyorsanız **Listmonk**; davranış tabanlı pazarlama ve satış otomasyonu arıyorsanız **Mautic**; klasik liste yönetimi ile uyumlu hosting önceliğiniz varsa **phpList** seçin. Son kararı vermeden önce küçük bir deneme listesi oluşturun, SMTP teslimatını ölçün ve yedekleme senaryosunu test edin. Çünkü en iyi newsletter sistemi, özellik listesi en uzun olan değil, ekibinizin sürdürülebilir biçimde çalıştırabildiği sistemdir.
