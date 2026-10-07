---
layout: post
title: "İlan Sitesi Kurmak: Osclass, OpenClassify ve WordPress Temaları Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - ilan sitesi
  - osclass
  - openclassify
  - wordpress
  - web geliştirme
  - pazar yeri
toc: true
image: /img/ilan-sitesi-kurmak-90.png
---

Bir ilan sitesi kurmak, birkaç form alanı ekleyip “Yayınla” düğmesine basmaktan ibaret değildir. Kullanıcı yönetimi, kategori ağacı, konum filtreleri, fotoğraf yükleme, moderasyon ve ödeme gibi parçalar işin içine girince proje küçük bir dijital çarşıya dönüşür. Neyse ki Osclass, OpenClassify ve WordPress ilan temaları bu çarşıyı sıfırdan inşa etme zahmetini azaltır.

![ilan-sitesi-kurmak-90](/img/ilan-sitesi-kurmak-90.svg)

``
## Önce ilan sitesinin mantığı

Bir ilan platformunun merkezinde **ilan** varlığı bulunur. Her ilan genellikle kullanıcı, kategori ve konum kayıtlarıyla ilişkilidir. Basitleştirilmiş veri modeli şöyle düşünülebilir:

```text
Kullanıcı 1 --- N İlan N --- 1 Kategori
                    |
                    N
                    |
                 Fotoğraf
```

Arama performansı da önemlidir. Toplam $N$ ilan içinde doğrusal arama yaklaşık $O(N)$ maliyetliyken, doğru indekslenmiş kategori veya fiyat alanlarında arama pratikte $O(\log N)$ seviyesine yaklaşabilir. Yani on bin ilanınız olduğunda veritabanı indeksleri süs değil, can simididir.

Platform seçerken yaklaşık toplam maliyeti şu şekilde modelleyebiliriz:

$$T = K + G \times S + B + U$$

Burada $K$ kurulum, $G$ geliştirme süresi, $S$ saatlik maliyet, $B$ bakım ve $U$ üçüncü taraf uzantı ücretidir. “Ücretsiz yazılım” ifadesi, bu denklemin tamamının sıfır olduğu anlamına gelmez.

## Üç yaklaşımın karşılaştırması

| Seçenek | Güçlü yanı | Zayıf yanı | Uygun senaryo |
|---|---|---|---|
| Osclass | İlan odaklı çekirdek ve sade yönetim | Eklenti kalitesi değişken olabilir | Hızlı ve klasik ilan portalı |
| OpenClassify | Geliştirici dostu, özelleştirilebilir yapı | Kurulum ve bakım daha teknik olabilir | Özel iş kuralları bulunan proje |
| WordPress temaları | Büyük tema ve eklenti ekosistemi | Eklenti çatışması ve performans riski | İçerik ile ilanı birleştiren site |

### Osclass

Osclass doğrudan seri ilan mantığı için tasarlanmıştır. Kategori, kullanıcı, konum ve ilan yönetimi çekirdeğin doğal parçalarıdır. Bu nedenle genel amaçlı bir içerik yönetim sistemini ilana dönüştürmek için daha az uğraşırsınız. Küçük ekipler ve hızlı MVP çalışmaları için güçlü bir adaydır.

Ancak tema veya eklenti satın almadan önce kullanılan Osclass sürümüyle uyumluluğu, geliştiricinin güncelleme geçmişini ve güvenlik desteğini kontrol edin. Ucuz bir eklenti bazen pahalı bir hafta sonuna dönüşebilir.

### OpenClassify

OpenClassify, daha fazla teknik kontrol isteyen geliştiricilere hitap eder. Kod tabanı üzerinde yeni ilan türleri, özel filtreler veya kurumsal iş akışları geliştirilebilir. Buna karşılık sunucu yapılandırması, bağımlılık yönetimi ve güncelleme süreçleri daha fazla yazılım bilgisi gerektirir.

Projenin sürümünü, depo etkinliğini ve güncel PHP bağımlılıklarını kurulumdan önce doğrulamak özellikle önemlidir. Bakımı yavaşlamış bir paketle başlamak, gelecekte teknik borcu büyütebilir.

### WordPress ilan temaları

WordPress tarafında ilan özellikleri çoğunlukla tema ve eklentilerle sağlanır. Blog, rehber içerikleri, SEO sayfaları ve ilanları aynı panelden yönetmek büyük avantajdır. Buna karşın iş mantığını yalnızca temaya bağlamak risklidir; tema değiştiğinde ilan özellikleri kaybolabilir. Mümkünse ilan veri modeli bir eklentide, görsel sunum ise temada tutulmalıdır.

Örneğin özel ilan türü oluşturan basit bir WordPress kodu şöyledir:

```php
add_action('init', function () {
    register_post_type('ilan', [
        'label' => 'İlanlar',
        'public' => true,
        'has_archive' => true,
        'supports' => ['title', 'editor', 'thumbnail', 'author'],
        'show_in_rest' => true,
    ]);
});
```

Bu kod, yönetim paneline ilan bölümü ekler ve REST API desteğini açar. Fiyat, şehir ve durum gibi alanlar için ayrıca özel alanlar ve doğrulama kuralları gerekir.

## Hangisini seçmeli?

Hızlı, yalnızca ilana odaklı bir portal için **Osclass**; yoğun özelleştirme ve geliştirici kontrolü için güncelliği doğrulanmış **OpenClassify**; blog, SEO ve ilanı birlikte yönetecek ekipler için **WordPress** mantıklıdır. Seçimden önce mobil uyumluluk, spam koruması, yedekleme, KVKK süreçleri ve ödeme altyapısını test edin. En güzel tema ziyaretçiyi getirir; iyi veri modeli, güvenlik ve performans ise onun kaçmasını engeller.
