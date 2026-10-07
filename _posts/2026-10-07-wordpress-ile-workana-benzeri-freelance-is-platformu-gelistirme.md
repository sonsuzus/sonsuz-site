---
layout: post
title: "WordPress ile Workana Benzeri Freelance İş Platformu Geliştirme"
math: true
categories: 
  - Proje
tags: 
  - wordpress
  - freelance
  - php
  - woocommerce
  - pazaryeri
  - web geliştirme
toc: true
image: /img/wordpress-ile-workana-80.png
---

Bir freelance iş platformu; müşterilerin proje yayımladığı, uzmanların teklif verdiği ve ödemenin güvenli biçimde yönetildiği iki taraflı bir pazaryeridir. WordPress eklentileriyle birkaç haftada MVP hazırlamak mümkünken Workana benzeri özel bir sistem; teklif algoritması, komisyon, mesajlaşma ve uyuşmazlık yönetimi gibi konularda daha fazla kontrol sağlar. Kısacası mesele yalnızca ilan listelemek değil, güven üreten dijital bir ekonomi kurmaktır.

![wordpress-ile-workana-80](/img/wordpress-ile-workana-80.svg)

``

## Sistemin temel mantığı

Platformda iki ana kullanıcı rolü bulunur: **müşteri** ve **freelancer**. Müşteri bütçe, teslim tarihi ve gerekli yetenekleri belirterek iş açar. Freelancer ise profilini, fiyatını ve tahmini teslim süresini içeren bir teklif gönderir. Teklif kabul edildiğinde proje aktifleşir; ödeme mümkünse emanet, yani escrow mantığıyla tutulur.

Platform gelirini sabit üyelikten, ilan ücretinden veya işlem komisyonundan sağlayabilir. Komisyon hesabı basitçe şöyledir:

$$K = B \times \frac{r}{100}$$

Burada $B$ proje bedelini, $r$ komisyon oranını ve $K$ platform gelirini gösterir. Örneğin 10.000 TL değerindeki bir projede yüzde 12 komisyon uygulanırsa platform geliri 1.200 TL olur. Freelancer’a aktarılacak net tutar ise $N = B - K$ formülüyle 8.800 TL’dir.

## WordPress eklentisi mi, özel yazılım mı?

| Ölçüt | WordPress tabanlı çözüm | Özel Workana benzeri sistem |
|---|---|---|
| İlk geliştirme süresi | Kısa | Orta veya uzun |
| Başlangıç maliyeti | Düşük | Yüksek |
| Özelleştirme | Tema ve eklenti sınırlarında | Neredeyse sınırsız |
| Ölçeklenebilirlik | İyi yapılandırılırsa orta-yüksek | Mimariye bağlı olarak yüksek |
| Bakım | Eklenti güncellemeleri gerekir | Yazılım ekibi gerekir |
| MVP uygunluğu | Çok uygun | Büyük hedeflerde uygun |

WordPress tarafında **WP Job Manager**, **FreelanceEngine**, **TaskHive** veya çok satıcılı yapı için **WooCommerce** ile **Dokan** değerlendirilebilir. Ancak her eklenti gerçek teklif yönetimi ya da escrow sağlamaz. Lisans satın almadan önce rol yönetimi, komisyon, mesajlaşma, para çekme ve ödeme ağ geçidi desteği mutlaka incelenmelidir.

## WordPress üzerinde veri modeli

Projeler bir özel yazı türü, teklifler ise ayrı bir özel yazı türü veya özel veritabanı tablosu olarak saklanabilir. Küçük bir MVP için özel yazı türü pratiktir:

```php
// Yönetim paneline "Projeler" içerik türünü ekler.
add_action('init', function () {
    register_post_type('freelance_project', [
        'label' => 'Projeler',
        'public' => true,
        'show_in_rest' => true,
        'supports' => ['title', 'editor', 'author'],
        'has_archive' => true,
    ]);
});
```

Bu kod projelerin WordPress panelinden yönetilmesini ve REST API üzerinden mobil uygulamalara açılmasını sağlar. Teklif sayısı büyüdüğünde her teklifi `post_meta` içinde tutmak sorguları yavaşlatabilir. Bu nedenle teklif, mesaj ve finansal hareketler için indekslenmiş özel tablolar daha sağlıklıdır.

## Teklifleri nasıl sıralamalıyız?

Yalnızca en ucuz teklifi öne çıkarmak kaliteyi düşürebilir. Bunun yerine puan, fiyat uygunluğu ve teslim süresini birleştiren ağırlıklı bir skor kullanılabilir:

$$S = 0.5R + 0.3P + 0.2T$$

$R$ freelancer değerlendirme puanını, $P$ fiyat uygunluğunu, $T$ ise teslim süresi puanını temsil eder. Değerlerin aynı ölçeğe normalize edilmesi gerekir. Ayrıca yeni kullanıcıların görünmez hâle gelmemesi için deneyim etkisine bir üst sınır konulmalıdır.

## Güvenlik ve ödeme katmanı

Kullanıcı girdileri temizlenmeli, formlarda nonce doğrulaması yapılmalı ve yetkiler rol bazında kontrol edilmelidir. Ödeme sonucu tarayıcıdan gelen yönlendirmeye göre değil, ödeme sağlayıcısının imzalı webhook bildirimiyle kesinleştirilmelidir. Kart bilgileri platform sunucusunda tutulmamalıdır.

Escrow özelliği hukuki ve finansal sorumluluk doğurabileceğinden Stripe Connect, iyzico veya benzeri pazaryeri çözümlerinin ülke desteği araştırılmalıdır. İptal, kısmi ödeme, teslim onayı ve uyuşmazlık senaryoları daha kod yazılmadan akış diyagramına dökülmelidir.

En mantıklı yol, önce WordPress ile dar kapsamlı bir MVP kurup gerçek kullanıcı davranışını ölçmektir. İşlem hacmi, mesaj trafiği ve özel süreçler büyüdüğünde teklif ve ödeme modülleri bağımsız servislere taşınabilir. Böylece ilk günden uzay gemisi inşa etmek yerine çalışan bir bisikletle yola çıkılır; ihtiyaç oluşunca motor eklenir.
