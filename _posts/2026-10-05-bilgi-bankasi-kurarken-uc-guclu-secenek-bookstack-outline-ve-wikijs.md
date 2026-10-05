---
layout: post
title: "Bilgi Bankası Kurarken Üç Güçlü Seçenek: BookStack, Outline ve Wiki.js"
math: true
categories: 
  - Program
tags: 
  - bilgi-bankası
  - bookstack
  - outline
  - wiki.js
  - dokümantasyon
  - açık-kaynak
toc: true
image: /img/bilgi-bankasi-kurarken-97.png
---

Dağınık belgeler, sohbet kanallarında kaybolan çözümler ve yalnızca bir ekip arkadaşının bildiği gizemli süreçler… Kurumsal hafızanın doğal düşmanları bunlardır. BookStack, Outline ve Wiki.js ise bilgiyi merkezi, aranabilir ve düzenli hâle getiren üç güçlü bilgi bankası çözümüdür. Benzer amaçlara hizmet etseler de içerik organizasyonu, kullanım kolaylığı ve teknik gereksinimler bakımından farklı karakterlere sahiptirler.

``

## Bilgi bankası neden gereklidir?

Bilgi bankası; kullanım kılavuzlarını, teknik kararları, şirket politikalarını ve sık karşılaşılan sorunların çözümlerini tek noktada toplar. Temel hedef yalnızca belge saklamak değil, doğru bilgiye ulaşma süresini azaltmaktır.

Bir sistemin sağladığı yaklaşık zaman kazancını şöyle düşünebiliriz:

$$K = A \times (T_e - T_b)$$

Burada $A$ aylık arama sayısını, $T_e$ eski yöntemdeki ortalama erişim süresini, $T_b$ ise bilgi bankasıyla erişim süresini temsil eder. Ayda 300 arama yapılıyor, eski yöntemde bilgi 8 dakikada, yeni sistemde 2 dakikada bulunuyorsa toplam kazanç $300 \times 6 = 1800$ dakika olur. Bu da aylık 30 saatlik ciddi bir tasarruftur.

## Üç platformun yaklaşımı

| Özellik | BookStack | Outline | Wiki.js |
|---|---|---|---|
| Organizasyon | Raf, kitap, bölüm, sayfa | Koleksiyon ve belge | Klasör ve sayfa |
| Arayüz | Basit ve geleneksel | Modern ve akıcı | Modern ve özelleştirilebilir |
| Editör | WYSIWYG ve Markdown | Markdown odaklı | Markdown ve görsel editör |
| Kimlik doğrulama | LDAP, SAML2, OIDC | OIDC, SAML, Slack | LDAP, OAuth2, SAML |
| Teknik zorluk | Düşük-orta | Orta-yüksek | Orta |
| İdeal kullanıcı | Düzenli hiyerarşi isteyen ekip | Şık iç wiki arayan şirket | Esneklik isteyen teknik ekip |

### BookStack: Dijital kütüphane düzeni

BookStack, içeriği gerçek bir kütüphane gibi raflara, kitaplara, bölümlere ve sayfalara ayırır. Bu model özellikle prosedürleri ve eğitim belgelerini katmanlı biçimde yöneten ekipler için anlaşılırdır. PHP ve Laravel tabanlıdır; MariaDB veya MySQL kullanır. Yönetim paneli sade olduğundan teknik olmayan kullanıcılar da sisteme hızlıca alışabilir.

Bununla birlikte katı hiyerarşi, çok sayıda çapraz ilişkiye sahip içeriklerde sınırlayıcı olabilir. Yine de “hangi belge hangi kitabın içinde?” sorusunun net bir cevabı vardır.

### Outline: Şık ve hızlı ekip wikisi

Outline, Notion benzeri temiz arayüzü ve gerçek zamanlı düzenleme deneyimiyle öne çıkar. Belgeler koleksiyonlar içinde tutulur; paylaşım, izin ve arama özellikleri oldukça başarılıdır. Özellikle ürün, tasarım ve yazılım ekiplerinin birlikte çalıştığı ortamlarda keyifli bir deneyim sunar.

Kurulum tarafında PostgreSQL ve Redis gibi ek servisler gerektiğinden BookStack kadar hafif değildir. Buna karşılık modern kullanıcı deneyimi, entegrasyon seçenekleri ve ortak düzenleme yetenekleri güçlüdür.

### Wiki.js: Teknik ekiplerin İsviçre çakısı

Node.js tabanlı Wiki.js; tema, kimlik doğrulama, depolama ve editör seçenekleriyle yüksek esneklik sunar. İçeriklerin Git deposuyla eşitlenebilmesi, sürüm kontrolüne alışkın geliştiriciler için önemli bir avantajdır. Ancak seçeneklerin bolluğu, ilk yapılandırmayı biraz daha dikkat isteyen bir işe dönüştürebilir.

## Docker ile örnek Wiki.js kurulumu

Aşağıdaki yapı, Wiki.js ile PostgreSQL servislerini birlikte başlatır:

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: wiki
      POSTGRES_USER: wiki
      POSTGRES_PASSWORD: guclu_bir_parola
    volumes:
      - db_data:/var/lib/postgresql/data

  wiki:
    image: requarks/wiki:2
    ports:
      - "3000:3000"
    environment:
      DB_TYPE: postgres
      DB_HOST: db
      DB_NAME: wiki
      DB_USER: wiki
      DB_PASS: guclu_bir_parola
    depends_on:
      - db

volumes:
  db_data:
```

Dosya `compose.yml` adıyla kaydedilip `docker compose up -d` komutuyla çalıştırılabilir. Gerçek ortamda parolaları dosyaya açıkça yazmak yerine secret veya ortam değişkeni kullanmak gerekir.

## Hangisini seçmeli?

Düzenli bir kitap mantığı ve kolay yönetim istiyorsanız **BookStack**, modern ekip çalışması ve zarif arayüz önceliğinizse **Outline**, ayrıntılı özelleştirme ve Git entegrasyonu arıyorsanız **Wiki.js** daha uygun olacaktır. En iyi platform, en fazla özelliğe sahip olan değil; ekibin gerçekten belge yazmasını ve güncel tutmasını sağlayandır. Çünkü kullanılmayan bilgi bankası, yalnızca daha düzenli görünen bir dijital çekmecedir.

![bilgi-bankasi-kurarken-97](/img/bilgi-bankasi-kurarken-97.svg)

