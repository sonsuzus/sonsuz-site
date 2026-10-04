---
layout: post
title: "WordPress, Ghost ve WriteFreely: Hangi Blog Sistemi Size Göre?"
math: true
categories: 
  - Bilgi
tags: 
  - wordpress
  - ghost
  - writefreely
  - blog
  - cms
  - açık kaynak
toc: true
image: /img/wordpress-ghost-ve-83.png
---

Bir blog sistemi seçmek, yalnızca yazı yayımlayacağınız bir araç belirlemek değildir; içerik üretim sürecinizi, bakım yükünüzü ve gelecekteki büyüme seçeneklerinizi de şekillendirir. WordPress devasa ekosistemiyle İsviçre çakısını, Ghost yayıncılık odaklı modern bir çalışma masasını, WriteFreely ise dikkatinizi dağıtmayan sade bir daktiloyu andırır. Gelin bu üç sistemi teknik temelleri, kullanım senaryoları ve kurulum seçenekleriyle karşılaştıralım.
``

## Üç Farklı Yayıncılık Felsefesi

**WordPress**, PHP ve MySQL tabanlı genel amaçlı bir içerik yönetim sistemidir. Tema ve eklenti mimarisi sayesinde blogdan e-ticaret mağazasına kadar dönüşebilir. Esnekliğinin karşılığında güncelleme, güvenlik ve performans optimizasyonu ister.

**Ghost**, Node.js üzerinde çalışan ve profesyonel yayıncılığa odaklanan bir platformdur. Üyelik, ücretli abonelik, e-posta bülteni ve SEO özellikleri çekirdeğe daha yakın konumlanır. Bu nedenle içerikten gelir elde etmek isteyen ekipler için güçlüdür.

**WriteFreely** ise Go diliyle geliştirilmiş, minimal ve federasyon dostu bir yazma platformudur. ActivityPub desteği sayesinde içerikler merkezi olmayan sosyal ağlara ulaşabilir. Yönetim panelinde kaybolmadan yalnızca yazmak isteyenler için biçilmiş kaftandır.

| Özellik | WordPress | Ghost | WriteFreely |
|---|---|---|---|
| Teknoloji | PHP, MySQL | Node.js, MySQL | Go, SQLite/MySQL |
| Öğrenme eğrisi | Orta | Orta | Düşük |
| Özelleştirme | Çok yüksek | Yüksek | Sınırlı |
| Üyelik ve bülten | Eklenti gerekir | Yerleşik | Temel |
| Federasyon | Eklentiyle | Sınırlı | Yerleşik |
| Bakım yükü | Orta-yüksek | Orta | Düşük |

## Kararı Sayısallaştırmak

Seçimi biraz daha sistematik yapmak için basit bir uygunluk puanı tanımlayabiliriz:

$$S = 0.35E + 0.25Y + 0.20P + 0.20B$$

Burada $E$ esneklik, $Y$ yayıncılık özellikleri, $P$ performans kolaylığı ve $B$ bakım rahatlığıdır. Her başlığa 1 ile 10 arasında puan verilir. Katsayılar ihtiyaçlarınıza göre değişebilir. Örneğin kişisel bir günlükte bakım rahatlığının katsayısını artırmak WriteFreely’yi öne çıkarırken, eklenti çeşitliliğine önem vermek WordPress’in puanını yükseltir.

## Docker ile Ghost Kurulumu

Ghost’u denemek için aşağıdaki orta düzey Docker Compose yapılandırması kullanılabilir:

```yaml
services:
  ghost:
    image: ghost:5-alpine
    restart: unless-stopped
    ports:
      - 2368:2368
    environment:
      url: http://localhost:2368
    volumes:
      - ghost_data:/var/lib/ghost/content

volumes:
  ghost_data:
```

Bu yapılandırma Ghost konteynerini başlatır, yönetim arayüzünü `2368` portunda sunar ve yazıları kalıcı bir Docker volume içinde saklar. Üretim ortamında HTTPS, alan adı, düzenli yedekleme ve harici MySQL veritabanı eklenmelidir.

```bash
docker compose up -d
docker compose logs -f ghost
```

İlk komut sistemi arka planda çalıştırır; ikinci komut ise başlangıç hatalarını ve uygulama günlüklerini takip etmenizi sağlar.

## Hangi Durumda Hangisi?

- Kurumsal site, mağaza, eğitim portalı veya yoğun özelleştirme istiyorsanız **WordPress** seçin.
- Ücretli üyelik, bülten ve profesyonel yayın akışı önceliğinizse **Ghost** daha doğal bir tercihtir.
- Minimal kişisel blog, düşük sunucu tüketimi ve federasyon ilginizi çekiyorsa **WriteFreely** kullanın.

Sonuçta mutlak bir kazanan yoktur. En iyi platform, en fazla özelliğe sahip olan değil, kullanmayacağınız özellikler için size bakım faturası çıkarmayandır. WordPress büyük bir atölye, Ghost düzenli bir yayınevi, WriteFreely ise sessiz bir yazı köşesidir; seçim, ne inşa etmek istediğinize bağlıdır.

![wordpress-ghost-ve-83](/img/wordpress-ghost-ve-83.svg)

