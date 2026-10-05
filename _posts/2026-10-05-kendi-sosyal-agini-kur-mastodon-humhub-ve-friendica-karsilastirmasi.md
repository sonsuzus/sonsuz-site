---
layout: post
title: "Kendi Sosyal Ağını Kur: Mastodon, HumHub ve Friendica Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - mastodon
  - humhub
  - friendica
  - fediverse
  - activitypub
  - sosyal ağ
  - açık kaynak
toc: true
image: /img/kendi-sosyal-agini-68.png
---

Sosyal medya denince akla yalnızca dev platformlar gelmek zorunda değil. Mastodon, HumHub ve Friendica; verilerinizi kendi sunucunuzda tutabileceğiniz, topluluğun kurallarını belirleyebileceğiniz açık kaynaklı sosyal ağ sistemleridir. Üçü de “kendi dijital mahalleni kur” fikrine yaklaşsa da Mastodon kalabalık bir meydan, HumHub düzenli bir şirket kampüsü, Friendica ise farklı ağlara açılan çok yönlü bir ev gibidir.

``

## Merkezi ve federe ağ mantığı

Merkezi bir sosyal ağda kullanıcılar, içerikler ve moderasyon tek bir işletmenin altyapısına bağlıdır. Federe yapıda ise birbirinden bağımsız sunucular iletişim kurar. E-posta sistemini düşünün: Gmail kullanıcısı başka bir sağlayıcıdaki kullanıcıya mesaj gönderebilir. Fediverse de benzer biçimde çalışır.

Mastodon ve Friendica, sunucular arası iletişimde ağırlıklı olarak **ActivityPub** protokolünden yararlanır. Bir kullanıcı başka sunucudaki hesabı takip ettiğinde içerikler kendi sunucusuna iletilir. HumHub ise öncelikle kapalı veya kurumsal topluluklara odaklanır; federasyon onun temel kullanım amacı değildir.

Bir sosyal ağın faydasını basitleştirilmiş şekilde şöyle düşünebiliriz:

$$D = U + I + G - Y$$

Burada $U$ kullanıcı kontrolünü, $I$ birlikte çalışabilirliği, $G$ gizliliği ve $Y$ yönetim yükünü temsil eder. Kendi sunucunuzu çalıştırmak kontrolü artırır; fakat güncelleme, yedekleme ve moderasyon sorumluluğunu da beraberinde getirir. Özgürlük bedava olabilir, sistem yöneticisinin kahvesi olmayabilir!

## Üç platformun karşılaştırması

| Özellik | Mastodon | HumHub | Friendica |
|---|---|---|---|
| Temel amaç | Kamusal mikroblog | Kurum içi topluluk | Çok protokollü sosyal ağ |
| Yapı | Güçlü federasyon | Alan ve grup merkezli | Federasyon ve bağlantı merkezli |
| Teknoloji | Ruby on Rails | PHP / Yii | PHP |
| Arayüz yaklaşımı | Akış ve kısa gönderiler | Modüler çalışma alanları | Klasik sosyal ağ |
| İdeal kullanım | Açık topluluklar | Şirket, okul, dernek | Kişisel veya küçük topluluk |
| Yönetim zorluğu | Orta-yüksek | Orta | Orta |

![kendi-sosyal-agini-68](/img/kendi-sosyal-agini-68.svg)


### Mastodon

Mastodon; zaman akışları, etiketler, takip sistemi ve içerik uyarılarıyla X benzeri bir mikroblog deneyimi sunar. Her sunucu kendi kayıt politikasına ve moderasyon kurallarına sahiptir. Ruby uygulaması, PostgreSQL, Redis ve medya depolama bileşenleri nedeniyle küçük bir deneme kurulumundan büyük bir topluluğa geçerken kaynak planlaması önemlidir.

### HumHub

HumHub’da kullanıcılar “Space” adı verilen alanlarda buluşur. Dosya paylaşımı, takvim, görevler, wiki ve etkinlik modülleri sayesinde sosyal ağ ile ekip çalışmasını birleştirir. İnsan kaynakları portalı, okul ağı veya dernek platformu geliştirmek isteyenler için güçlüdür. Dış dünyaya açık dev bir ağdan çok, giriş kartı olan dijital bir bina gibi davranır.

### Friendica

Friendica, klasik arkadaşlık ilişkilerini ve uzun gönderileri destekler. ActivityPub yanında farklı bağlantı yöntemlerine önem vermesiyle çeşitli ağlar arasında köprü görevi görebilir. Facebook tarzı bir deneyim isteyen, ancak merkezi platform bağımlılığından kaçınan küçük topluluklar için dengeli bir seçenektir.

## Basit bir kurulum planı

Üretim ortamında doğrudan rastgele bir Docker imajı çalıştırmak yerine projenin resmî belgeleri izlenmelidir. Yine de temel mimariyi bir Compose taslağıyla görebiliriz:

```yaml
services:
  app:
    image: friendica:stable
    restart: unless-stopped
    depends_on:
      - database
    environment:
      MYSQL_HOST: database
      MYSQL_DATABASE: social

  database:
    image: mariadb:11
    restart: unless-stopped
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

Bu örnek uygulama ile veritabanını ayrı servisler olarak tanımlar ve verileri kalıcı diskte saklar. Gerçek kurulumda güçlü parolalar, HTTPS sağlayan ters vekil sunucu, e-posta servisi, günlük izleme ve otomatik yedekleme eklenmelidir.

## Hangisini seçmeli?

Herkese açık, Twitter benzeri federe bir topluluk için **Mastodon**; ekip iletişimi ve kurumsal alanlar için **HumHub**; esnek arkadaşlık modeli ve farklı ağlarla bağlantı için **Friendica** öne çıkar. Seçimi yalnızca özellik listesine göre değil, hedef kitlenin davranışına ve yönetim kapasitesine göre yapmak gerekir. En iyi sosyal ağ yazılımı, sunucuda çalışan değil, topluluğun gerçekten kullanmak istediği yazılımdır.
