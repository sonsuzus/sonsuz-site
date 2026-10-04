---
layout: post
title: "Çok Yazarlı Blog Sistemi Seçimi: WordPress Multisite, Ghost ve Drupal"
math: true
categories: 
  - Bilgi
tags: 
  - wordpress
  - ghost
  - drupal
  - çok-yazarlı-blog
  - cms
  - multisite
toc: true
image: /img/cok-yazarli-blog-78.png
---

Birden fazla yazarın, editörün ve hatta bağımsız yayın ekibinin aynı altyapıda içerik ürettiği bir blog sistemi kurmak, yalnızca “yazı ekleme ekranı” seçmek değildir. Yetkilendirme, içerik akışı, site izolasyonu, bakım maliyeti ve ölçeklenebilirlik birlikte düşünülmelidir. Bu arenada WordPress Multisite pratikliğiyle, Ghost yayıncılık odaklı sadeliğiyle, Drupal ise ayrıntılı kontrol gücüyle öne çıkar.


![cok-yazarli-blog-78](/img/cok-yazarli-blog-78.svg)

``

## Önce kavramları ayıralım

**Çok yazarlılık**, aynı sitede farklı rollere sahip kullanıcıların çalışmasıdır. **Multisite** ise tek bir altyapıdan birden fazla sitenin yönetilmesidir. Her multisite kurulumu çok yazarlı olabilir; ancak her çok yazarlı sistem multisite olmak zorunda değildir.

Temel yetkilendirme modeli şu şekilde ifade edilebilir:

$$İzin = Kullanıcı \times Rol \times Kaynak \times İşlem$$

Örneğin bir “Yazar”, kendi yazısını oluşturabilir fakat yayımlayamayabilir; “Editör” ise tüm yazıları düzenleyip yayımlayabilir. Sistem seçerken sadece rol isimlerine değil, bu rollerin ne kadar özelleştirilebildiğine bakmak gerekir.

| Kriter | WordPress Multisite | Ghost | Drupal |
|---|---|---|---|
| Kurulum kolaylığı | Yüksek | Çok yüksek | Orta-düşük |
| Yerleşik multisite | Var | Yok | Yapılandırılabilir |
| Rol esnekliği | Orta | Basit ve yayın odaklı | Çok yüksek |
| İçerik modelleme | Eklentilerle gelişir | Sınırlı ve sade | Çok güçlü |
| Bakım karmaşıklığı | Orta | Düşük | Yüksek |
| En uygun kullanım | Blog ağı | Tek yayın/üyelik sitesi | Kurumsal içerik platformu |

## WordPress Multisite: Blog sitelerinin apartmanı

WordPress Multisite, tek çekirdek kurulum üzerinden bir site ağı oluşturur. Siteler aynı tema ve eklenti havuzunu paylaşabilirken içerikleri ayrı tablolarda tutulur. Ağ yöneticisi tüm sistemi, site yöneticileri ise kendilerine ait alanları yönetir.

Multisite özelliğini başlatmak için `wp-config.php` dosyasına şu tanım eklenir:

```php
// WordPress yönetim panelinde Ağ Kurulumu menüsünü etkinleştirir.
define('WP_ALLOW_MULTISITE', true);
```

Kurulum sonrasında WordPress, alt alan adı veya alt dizin modeline göre ek yapılandırma üretir. Ajanslar, üniversite bölümleri ve çok sayıda tematik blog için oldukça kullanışlıdır. Ancak kötü yazılmış tek bir eklenti bütün ağı etkileyebilir. Bu nedenle merkezi güncelleme avantajı, aynı zamanda merkezi risk anlamına gelir.

## Ghost: Hızlı, zarif ama tek evli

Ghost; yazma deneyimi, üyelik, e-posta bülteni ve ücretli abonelik konularına odaklanır. Node.js tabanlıdır ve arayüzü gereksiz seçeneklerle boğmaz. Yazar, editör, yönetici ve katkıcı gibi roller sunar.

Ghost’un önemli farkı, WordPress Multisite benzeri yerleşik bir site ağı sağlamamasıdır. Birden fazla bağımsız yayın için genellikle ayrı Ghost örnekleri çalıştırılır:

```bash
# Her yayın için ayrı dizin ve Ghost örneği oluşturur.
mkdir teknoloji-yayini && cd teknoloji-yayini
ghost install
```

Bu yaklaşım izolasyonu güçlendirir; fakat güncelleme ve izleme yükünü artırır. Tek bir profesyonel yayın, üyelik tabanlı blog veya bülten projesinde Ghost son derece keyiflidir. Onlarca bağlı site hedefleniyorsa orkestrasyon için Docker, otomasyon ve merkezi gözlem araçları gerekir.

## Drupal: İçerik mühendisliğinin İsviçre çakısı

Drupal, ayrıntılı rol ve izin sistemiyle karmaşık yayın organizasyonlarında parlar. İçerik türleri, alanlar, taksonomiler ve iş akışları çekirdek yeteneklerle modellenebilir. “Yazar gönderir, hukuk ekibi kontrol eder, editör onaylar” gibi aşamalı süreçler rahatlıkla kurulabilir.

Drupal multisite modelinde aynı kod tabanı paylaşılırken siteler farklı ayar ve veritabanlarına sahip olabilir. Bu güçlü bir modeldir; ancak dağıtım, modül uyumluluğu ve güvenlik güncellemeleri deneyimli bir ekip ister.

## Maliyet ve seçim formülü

Gerçek maliyet yalnızca barındırma ücretinden oluşmaz:

$$TCO = Kurulum + Bakım + Eğitim + Güvenlik + Ölçekleme$$

Hızla bir blog ağı kurmak istiyorsanız **WordPress Multisite**, tek ve modern bir üyelik yayını geliştiriyorsanız **Ghost**, karmaşık roller ve özel içerik modelleri gerekiyorsa **Drupal** daha mantıklıdır. Kısacası seçim, en popüler CMS’yi bulma yarışı değil; yayın ekibinizin iş akışına en az sürtünmeyle uyacak mimariyi seçme işidir.
