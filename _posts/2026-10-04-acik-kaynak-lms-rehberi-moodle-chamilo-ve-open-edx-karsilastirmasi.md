---
layout: post
title: "Açık Kaynak LMS Rehberi: Moodle, Chamilo ve Open edX Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - lms
  - moodle
  - chamilo
  - open-edx
  - eğitim-teknolojileri
  - açık-kaynak
toc: true
image: /img/acik-kaynak-lms-79.png
---

![acik-kaynak-lms-79](/img/acik-kaynak-lms-79.svg)


Dijital eğitimin görünmez kahramanı olan LMS, yani Öğrenme Yönetim Sistemi; ders içeriklerini, öğrencileri, sınavları ve raporları tek merkezde buluşturur. Moodle, Chamilo ve Open edX ise açık kaynak dünyasının öne çıkan üç seçeneğidir. Üçü de eğitim sunar; ancak bunu farklı ölçek, mimari ve kullanıcı deneyimi anlayışlarıyla gerçekleştirir. Dolayısıyla seçim yaparken yalnızca özellik listesine değil, kurumun hedeflerine de bakmak gerekir.

``

## LMS tam olarak ne yapar?

Bir LMS'nin temel görevi, öğrenme sürecini ölçülebilir ve yönetilebilir hâle getirmektir. Tipik bir sistemde kullanıcı yönetimi, ders oluşturma, içerik sunma, sınav hazırlama, ödev toplama, sertifika üretme ve ilerleme takibi bulunur.

Öğrenci başarısını basitçe aşağıdaki ağırlıklı modelle ifade edebiliriz:

$$
Başarı = 0.4S + 0.3Ö + 0.2K + 0.1E
$$

Burada $S$ sınav puanını, $Ö$ ödevleri, $K$ içerik tamamlama oranını ve $E$ etkileşim düzeyini temsil eder. Gerçek sistemlerde katsayılar ders tasarımına göre değiştirilebilir. LMS'nin önemli avantajı, bu verileri elle hesaplamak yerine otomatik olarak işlemesidir.

## Üç platformun karakteri

| Özellik | Moodle | Chamilo | Open edX |
|---|---|---|---|
| Temel hedef | Okul ve kurum eğitimi | Kolay ve hızlı eğitim yönetimi | Büyük ölçekli çevrim içi kurslar |
| Öğrenme eğrisi | Orta | Düşük | Yüksek |
| Teknik gereksinim | Orta | Düşük-Orta | Yüksek |
| Eklenti ekosistemi | Çok geniş | Daha sınırlı | Güçlü fakat karmaşık |
| Ölçeklenebilirlik | Yüksek | Orta | Çok yüksek |
| İdeal kullanım | Üniversite, şirket, okul | KOBİ, kurs merkezi | MOOC ve geniş kitleler |

### Moodle

Moodle, modüler yapısı ve geniş eklenti pazarıyla İsviçre çakısı gibidir. Quiz, forum, rozet, SCORM paketi, not defteri ve harici servis entegrasyonları oldukça gelişmiştir. PHP tabanlı olduğu için yaygın sunucularda çalıştırılabilir. Buna karşılık çok fazla eklenti kullanmak bakım maliyetini ve sürüm yükseltme riskini artırabilir.

### Chamilo

Chamilo, daha sade yönetim paneli ve düşük sistem gereksinimleriyle hızlı başlangıç yapmak isteyenlere hitap eder. Ders yolları, sınavlar, sertifikalar ve kullanıcı takibi gibi temel ihtiyaçları fazla karmaşa çıkarmadan karşılar. Küçük bir eğitim ekibiniz varsa ve “önce sistemi kuralım, sonra kahve içeriz” yaklaşımını seviyorsanız güçlü bir adaydır.

### Open edX

Open edX, büyük kitlelere açık kurslar sunmak için tasarlanmıştır. Video, tartışma, gelişmiş değerlendirme ve öğrenme analitiği konusunda iddialıdır. Python ve Django ekosistemini kullanır; servis tabanlı yapısı nedeniyle kurulumu diğer iki seçeneğe göre daha zahmetlidir. Ancak binlerce öğrencinin aynı anda eğitim aldığı projelerde bu karmaşıklık karşılığını verir.

## Basit bir Moodle kurulumu

Aşağıdaki Docker Compose örneği, deneme ortamında Moodle ile MariaDB servislerini başlatır:

```yaml
services:
  moodle:
    image: bitnami/moodle:latest
    ports:
      - '8080:8080'
    environment:
      - MOODLE_DATABASE_HOST=db
      - MOODLE_DATABASE_USER=moodle
      - MOODLE_DATABASE_PASSWORD=guclu_parola
      - MOODLE_DATABASE_NAME=moodle
    depends_on:
      - db
  db:
    image: bitnami/mariadb:latest
    environment:
      - MARIADB_USER=moodle
      - MARIADB_PASSWORD=guclu_parola
      - MARIADB_DATABASE=moodle
      - MARIADB_ROOT_PASSWORD=root_parolasi
```

Dosyayı `compose.yml` adıyla kaydettikten sonra `docker compose up -d` komutu çalıştırılır. Bu örnek geliştirme ve inceleme içindir; üretimde kalıcı diskler, HTTPS, yedekleme, gizli değişken yönetimi ve sabit imaj sürümleri kullanılmalıdır.

## Hangisini seçmeli?

Kararı puanlamak için şu model kullanılabilir:

$$
P = 0.30K + 0.25Ö + 0.20B + 0.15E + 0.10D
$$

Burada $K$ kullanım kolaylığı, $Ö$ ölçeklenebilirlik, $B$ bakım kolaylığı, $E$ eklenti desteği ve $D$ dokümantasyon kalitesidir. Küçük ekipler Chamilo'ya, esneklik arayan kurumlar Moodle'a, devasa çevrim içi akademiler ise Open edX'e daha yüksek puan verecektir.

Sonuç olarak en güçlü LMS diye evrensel bir kazanan yoktur. En doğru platform; öğrenci sayısına, teknik ekibe, bütçeye, içerik modeline ve büyüme planına en iyi uyum sağlayandır.
