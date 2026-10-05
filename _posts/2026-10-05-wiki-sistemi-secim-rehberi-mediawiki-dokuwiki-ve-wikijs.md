---
layout: post
title: "Wiki Sistemi Seçim Rehberi: MediaWiki, DokuWiki ve Wiki.js"
math: true
categories: 
  - Program
tags: 
  - wiki
  - mediawiki
  - dokuwiki
  - wikijs
  - bilgi-yönetimi
  - dokümantasyon
toc: true
image: /img/wiki-sistemi-secim-69.png
---

Bir ekibin bilgisi yalnızca insanların zihninde yaşıyorsa, o bilgi tatilde, iş değişikliğinde veya meşhur “Bunu kim yapmıştı?” anında kaybolabilir. Wiki sistemleri; belgeleri merkezi, aranabilir ve sürümlenebilir hâle getirerek kurumsal hafızayı korur. Ancak MediaWiki, DokuWiki ve Wiki.js aynı sorunu farklı mimarilerle çözer. Gelin bu üç popüler seçeneği teknik özellikleri, kullanım kolaylıkları ve bakım maliyetleri açısından karşılaştıralım.


![wiki-sistemi-secim-69](/img/wiki-sistemi-secim-69.svg)

``

## Wiki mantığı nasıl çalışır?

Wiki, kullanıcıların sayfaları okuyabildiği, düzenleyebildiği ve birbirine bağlayabildiği ortak bir bilgi tabanıdır. Klasik bir içerik yönetim sisteminden farklı olarak esas amaç yayın yapmak değil, bilginin birlikte geliştirilmesini sağlamaktır.

Bir wiki sayfasının değeri yalnızca içeriğine değil; bağlantılarına, değişiklik geçmişine ve bulunabilirliğine de bağlıdır. Basitleştirilmiş bir seçim puanı şöyle modellenebilir:

$$
P = 0.30K + 0.25Y + 0.20A + 0.15E + 0.10G
$$

Burada $K$ kurulum kolaylığını, $Y$ yönetilebilirliği, $A$ arama yeteneğini, $E$ eklenti ekosistemini ve $G$ görsel deneyimi temsil eder. Katsayılar ihtiyaca göre değişir. Örneğin geliştirici ekiplerde Git entegrasyonunun ağırlığı artırılabilir.

Wiki sistemleri genellikle iki depolama yaklaşımından birini kullanır:

- **Veritabanı tabanlı yapı:** İçerik ve sürümler ilişkisel veritabanında tutulur.
- **Dosya tabanlı yapı:** Sayfalar düz metin dosyaları olarak saklanır.

Dosya tabanlı sistemler basit yedeklenirken veritabanlı sistemler büyük ölçekli sorgulama ve yetkilendirmede daha güçlüdür.

## Üç sistemin karşılaştırması

| Özellik | MediaWiki | DokuWiki | Wiki.js |
|---|---|---|---|
| Teknoloji | PHP | PHP | Node.js |
| Depolama | MySQL/MariaDB | Düz metin dosyaları | PostgreSQL |
| Kurulum | Orta | Kolay | Orta |
| Arayüz | Geleneksel | Sade | Modern |
| Ölçeklenme | Çok güçlü | Küçük ve orta ölçek | Orta ve büyük ölçek |
| İdeal kullanım | Kamusal bilgi platformu | Küçük ekip dokümantasyonu | Modern kurumsal wiki |

### MediaWiki: Ansiklopedi ustası

Wikipedia’nın arkasındaki motor olan MediaWiki, yüksek trafik ve çok sayıda katkıcı için geliştirilmiştir. Şablonlar, kategoriler, tartışma sayfaları ve ayrıntılı sürüm geçmişi oldukça güçlüdür. Buna karşılık yönetimi zaman zaman “küçük bir wiki kurdum, yanlışlıkla ansiklopedi yöneticisi oldum” hissi verebilir.

MediaWiki; geniş topluluk, kapsamlı eklenti ekosistemi ve gelişmiş kullanıcı rolleri isteyen projelerde öne çıkar. Tema özelleştirme ve bazı eklentilerin bakımı ise ek teknik emek gerektirir.

### DokuWiki: Veritabanına gerek yok

DokuWiki’nin en dikkat çekici özelliği veritabanı kullanmamasıdır. Sayfaları metin dosyalarında sakladığı için taşıma ve yedekleme işlemleri son derece rahattır:

```bash
# Wiki içeriğini tarih bilgisiyle arşivler.
tar -czf dokuwiki-yedek-$(date +%F).tar.gz /var/www/dokuwiki/data
```

Bu komut içerik, medya ve sürüm verilerini sıkıştırılmış bir arşive dönüştürür. DokuWiki; iç ağ belgeleri, kullanım kılavuzları ve küçük ekipler için idealdir. Çok büyük veri kümelerinde dosya tabanlı arama ve eşzamanlı düzenleme sınırlamaları hissedilebilir.

### Wiki.js: Modern ve geliştirici dostu

Wiki.js, modern arayüzü ve Markdown desteğiyle özellikle yazılım ekiplerine göz kırpar. PostgreSQL kullanır; Git, LDAP ve OAuth gibi servislerle bütünleşebilir. Docker ile örnek bir servis şöyle tanımlanabilir:

```yaml
services:
  wiki:
    image: requarks/wiki:2
    ports:
      - "3000:3000"
    environment:
      DB_TYPE: postgres
      DB_HOST: db
      DB_NAME: wiki
```

Bu yapı Wiki.js konteynerini çalıştırır ve PostgreSQL servisine bağlanacak temel değişkenleri tanımlar. Gerçek ortamda kullanıcı adı, parola, kalıcı disk ve HTTPS ayarları da eklenmelidir.

## Hangisini seçmelisiniz?

Herkese açık, yoğun katkılı ve kapsamlı bir bilgi platformu hedefliyorsanız **MediaWiki** güçlü seçimdir. Kurulumu hızlı, yedeklemesi kolay bir ekip dokümantasyonu arıyorsanız **DokuWiki** daha pratiktir. Modern tasarım, Markdown ve kurumsal kimlik doğrulama önemliyse **Wiki.js** öne çıkar.

Son kararı yalnızca özellik listesine göre vermeyin. Güncelleme sıklığı, yedekleme planı, ekip becerileri ve beş yıl sonraki içerik hacmini düşünün. En iyi wiki, en fazla düğmeye sahip olan değil; ekibin gerçekten düzenli kullandığı sistemdir.
