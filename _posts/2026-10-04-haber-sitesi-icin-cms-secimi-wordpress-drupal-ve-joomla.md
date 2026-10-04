---
layout: post
title: "Haber Sitesi İçin CMS Seçimi: WordPress, Drupal ve Joomla"
math: true
categories: 
  - Bilgi
tags: 
  - wordpress
  - drupal
  - joomla
  - cms
  - haber sitesi
  - web geliştirme
toc: true
image: /img/haber-sitesi-icin-85.png
---

Bir haber sitesi kurarken manşetlerden önce verilmesi gereken önemli bir karar vardır: İçerik yönetim sistemi seçimi. WordPress, Drupal ve Joomla aynı işi yapıyor gibi görünse de editoryal süreç, performans, güvenlik ve özelleştirme konularında farklı karakterlere sahiptir. Biri hızlıca yayına çıkmayı, diğeri karmaşık içerik ilişkilerini, öteki ise ikisi arasında denge kurmayı hedefler.


![haber-sitesi-icin-85](/img/haber-sitesi-icin-85.svg)

``

## CMS seçimi neden önemlidir?

Haber siteleri sıradan kurumsal sitelerden daha hareketlidir. Gün boyunca yeni içerikler yayımlanır, eski haberler güncellenir ve çok sayıda kullanıcı aynı anda sisteme erişir. Ayrıca muhabir, editör, yayın yönetmeni ve yönetici gibi farklı roller bulunabilir.

Basitleştirilmiş bir seçim puanı şu şekilde modellenebilir:

$$S = 0.30K + 0.25P + 0.20G + 0.15E + 0.10M$$

Burada $K$ kullanım kolaylığını, $P$ performansı, $G$ güvenliği, $E$ esnekliği ve $M$ maliyet avantajını temsil eder. Katsayılar projenin önceliklerine göre değiştirilebilir. Örneğin ulusal ölçekte bir haber portalında güvenlik ve performansın ağırlığı artırılmalıdır.

## Üç CMS’in temel farkları

| Özellik | WordPress | Drupal | Joomla |
|---|---|---|---|
| Kurulum kolaylığı | Çok kolay | Orta-zor | Orta |
| Editör deneyimi | Çok başarılı | Eğitim gerektirebilir | Dengeli |
| İçerik modelleme | Eklentilerle güçlü | Yerleşik olarak çok güçlü | Yeterli |
| Eklenti ekosistemi | Çok geniş | Teknik ve modüler | Orta büyüklükte |
| Güvenlik yönetimi | Düzenli bakım ister | Kurumsal düzeyde güçlü | İyi |
| Haber sitesi uygunluğu | Küçük ve orta ölçek | Büyük ve karmaşık projeler | Orta ölçek |

### WordPress: Hızlı yayıncının favorisi

WordPress, kullanıcı dostu yönetim paneli ve geniş tema ekosistemi sayesinde haber sitesini kısa sürede yayına almayı sağlar. Gutenberg editörü, teknik bilgisi sınırlı ekiplerin bile görsel açıdan zengin haberler hazırlamasına yardımcı olur. SEO, önbellekleme, üyelik ve reklam yönetimi için çok sayıda eklenti bulunur.

Ancak her ihtiyacı yeni bir eklentiyle çözmek performans ve güvenlik sorunlarına yol açabilir. Özellikle yoğun trafik alan projelerde sayfa önbelleği, CDN ve veritabanı optimizasyonu zorunlu hâle gelir.

Aşağıdaki örnek, WordPress’te haber sorgusunu sınırlayarak gereksiz veritabanı yükünü azaltır:

```php
$news = new WP_Query([
    'post_type'      => 'post',
    'posts_per_page' => 10,
    'no_found_rows'  => true
]);
```

`no_found_rows` seçeneği sayfalama gerekmiyorsa toplam kayıt hesabını kapatır ve sorguyu hafifletir.

### Drupal: Büyük yayın merkezinin kontrol odası

Drupal; içerik türleri, alanlar, kategoriler, kullanıcı izinleri ve iş akışları konusunda oldukça güçlüdür. Bir haberin muhabirden editöre, editörden yayın yönetmenine gönderildiği çok aşamalı süreçler kod yazmadan modellenebilir. Çok dilli yayıncılık ve API tabanlı, yani headless mimariler için de etkili bir seçenektir.

Bunun bedeli daha dik bir öğrenme eğrisidir. Drupal kurulumu kolay olsa da doğru içerik mimarisini ve önbellek katmanlarını tasarlamak deneyim ister. Büyük ve uzun ömürlü projelerde bu başlangıç maliyeti genellikle karşılığını verir.

### Joomla: Dengeli ama daha sakin seçenek

Joomla, WordPress’in kullanım kolaylığı ile Drupal’ın gelişmiş yetkilendirme yaklaşımı arasında konumlanır. Yerleşik çok dil desteği ve erişim kontrol sistemi güçlüdür. Buna karşın tema, eklenti ve uzman geliştirici havuzu WordPress kadar geniş değildir.

## Performans yalnızca CMS değildir

Bir sayfanın yaklaşık yanıt süresi şöyle düşünülebilir:

$$T_{toplam} = T_{sunucu} + T_{veritabanı} + T_{ağ} + T_{tarayıcı}$$

Dolayısıyla CMS seçmek tek başına hızlı bir site oluşturmaz. Görseller WebP veya AVIF biçimine dönüştürülmeli, CDN kullanılmalı, sorgular izlenmeli ve önbellek doğru yapılandırılmalıdır.

## Hangisini seçmelisiniz?

Küçük ya da orta ölçekli, hızlı kurulması gereken bir haber sitesi için **WordPress** en pratik tercihtir. Karmaşık editoryal akışlara, ayrıntılı izinlere ve çok kanallı yayına ihtiyaç duyan büyük kuruluşlar için **Drupal** öne çıkar. Yerleşik çok dil desteği isteyen ve daha kontrollü bir yapı arayan ekipler ise **Joomla** değerlendirebilir.

Kısacası kazanan CMS, en fazla özelliğe sahip olan değil; ekibin becerilerine, trafik beklentisine ve yayın modeline en iyi uyan sistemdir.
