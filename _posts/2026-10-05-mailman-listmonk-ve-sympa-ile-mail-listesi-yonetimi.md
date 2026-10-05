---
layout: post
title: "Mailman, Listmonk ve Sympa ile Mail Listesi Yönetimi"
math: true
categories: 
  - Program
tags: 
  - mailman
  - listmonk
  - sympa
  - e-posta
  - mail-listesi
  - açık-kaynak
toc: true
image: /img/mailman-listmonk-ve-60.png
---

E-posta listeleri sosyal medya algoritmalarına bağlı kalmadan topluluklara, müşterilere veya kurum içi ekiplere ulaşmanın en sağlam yollarından biridir. Ancak binlerce adresi bir dosyada tutup “Gönder” düğmesine basmak, liste yönetimi sayılmaz. Abonelik onayı, üyelikten ayrılma, hata takibi, arşivleme ve teslim edilebilirlik gibi işler için Mailman, Listmonk veya Sympa gibi özel bir sisteme ihtiyaç vardır.


![mailman-listmonk-ve-60](/img/mailman-listmonk-ve-60.svg)

``

## Mail listesi sistemi nasıl çalışır?

Bir mail listesi yöneticisi, kullanıcı veritabanı ile e-posta aktarım sunucusu arasında yer alır. Uygulama aboneleri ve kampanyaları yönetirken SMTP sunucusu mesajları alıcılara taşır. Başarılı bir mimaride süreç kabaca şöyledir:

1. Kullanıcı forma e-posta adresini girer.
2. Sistem bir doğrulama bağlantısı yollar.
3. Onaylanan adres ilgili listeye eklenir.
4. Mesaj, şablon ve kişiselleştirme kurallarına göre oluşturulur.
5. SMTP sunucusu gönderimi gerçekleştirir.
6. Geri dönen mesajlar ve abonelikten ayrılma istekleri işlenir.

Gönderim kapasitesini basitleştirilmiş biçimde

$$T = \frac{N}{r}$$

ile düşünebiliriz. Burada $N$ alıcı sayısı, $r$ saniyede gönderilebilen ileti sayısı, $T$ ise teorik gönderim süresidir. Örneğin 60.000 abone ve saniyede 20 ileti için ideal süre 3.000 saniyedir. Gerçekte SMTP gecikmeleri, hız sınırları ve yeniden denemeler bu süreyi artırır.

## Üç güçlü aday

| Özellik | Mailman | Listmonk | Sympa |
|---|---|---|---|
| Temel kullanım | Tartışma listeleri | Bülten ve kampanya | Kurumsal listeler |
| Teknoloji | Python | Go, PostgreSQL | Perl |
| Yönetim kolaylığı | Orta | Yüksek | Orta |
| Mesaj arşivi | Güçlü | Kampanya odaklı | Güçlü |
| Segmentasyon | Sınırlı | Çok güçlü | Kural tabanlı |
| Kurumsal yetkilendirme | Orta | Temel | Çok güçlü |
| Kaynak tüketimi | Orta | Düşük | Orta-yüksek |

### Mailman: Toplulukların emektarı

GNU Mailman, üyelerin aynı adrese mesaj göndererek birbiriyle konuştuğu tartışma listelerinde öne çıkar. Python tabanlı Mailman 3; REST API, web yönetim paneli ve HyperKitty arşiv arayüzü sunar. Yazılım toplulukları, üniversite grupları ve açık kaynak projeleri için iyi bir tercihtir.

Mailman’ın güçlü yanı konuşmaları konu başlıkları hâlinde arşivlemesidir. Buna karşılık pazarlama segmentleri, görsel kampanya raporları ve gelişmiş hedefleme gerektiğinde Listmonk kadar rahat değildir.

### Listmonk: Hızlı ve modern bülten motoru

Listmonk, tek bir Go uygulaması ve PostgreSQL ile yüksek performanslı kampanyalar yönetir. Aboneleri özelliklerine göre filtreleyebilir; örneğin yalnızca İstanbul’daki ücretli kullanıcılara mesaj gönderebilirsiniz. Docker ile temel kurulum şu şekilde başlatılabilir:

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: guclu-parola
      POSTGRES_DB: listmonk
  app:
    image: listmonk/listmonk:latest
    ports:
      - "9000:9000"
    depends_on:
      - db
```

Bu yapı PostgreSQL veritabanını ve Listmonk uygulamasını ayrı konteynerlerde çalıştırır. Gerçek ortamda kalıcı disk, ters vekil sunucu, TLS sertifikası ve gizli değişken yönetimi de eklenmelidir.

### Sympa: Kurumsal yetkilendirme ustası

Sympa, karmaşık organizasyonlarda rol ve senaryo tabanlı yetkilendirmesiyle dikkat çeker. LDAP entegrasyonu, otomatik liste üretimi, moderasyon ve kurum içi kimlik sistemleri konusunda güçlüdür. Büyük üniversiteler veya çok katmanlı departman yapıları için esnektir; ancak kurulumu ve özelleştirilmesi daha fazla sistem yönetimi bilgisi ister.

## Hangisini seçmeli?

Topluluk üyeleri birbirine yazacaksa **Mailman**, hızlı bültenler ve ayrıntılı segmentasyon gerekiyorsa **Listmonk**, LDAP ve gelişmiş kurumsal politikalar önemliyse **Sympa** daha mantıklıdır. Seçim yalnızca abone sayısına göre yapılmamalıdır; yönetim modeli, ekip deneyimi ve entegrasyon ihtiyaçları da hesaba katılmalıdır.

Son olarak SPF, DKIM ve DMARC kayıtlarını yapılandırmak; çift onaylı abonelik kullanmak ve kolay bir ayrılma bağlantısı sunmak şarttır. İyi mail sistemi çok mesaj gönderen değil, doğru kişiye izinli ve güvenilir mesaj ulaştıran sistemdir.
