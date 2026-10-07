---
layout: post
title: "WordPress, Grav ve Hugo ile Portföy Oluşturma Sistemi"
math: true
categories: 
  - Proje
tags: 
  - wordpress
  - grav
  - hugo
  - portföy
  - statik site
  - cms
  - web geliştirme
toc: true
image: /img/wordpress-grav-ve-28.png
---

İyi bir portföy, yalnızca projelerin sıralandığı dijital bir vitrin değildir; becerilerinizi, çalışma biçiminizi ve teknik tercihlerinizi anlatan yaşayan bir sistemdir. Bu sistemi WordPress, Grav veya Hugo ile kurabilirsiniz. Üç araç da aynı hedefe ulaşır fakat içerik yönetimi, performans ve bakım açısından farklı yollar izler. Gelin seçenekleri karşılaştırıp yeniden kullanılabilir bir portföy mimarisi tasarlayalım.


![wordpress-grav-ve-28](/img/wordpress-grav-ve-28.svg)

``

## Önce sistemi modelleyelim

Bir portföyün temel veri birimi **proje**dir. Her proje; başlık, açıklama, teknoloji listesi, görseller, bağlantılar ve yayın tarihi içerir. Platformdan bağımsız basit modelimiz şöyle düşünülebilir:

$$
P = (b, a, t, g, l, d)
$$

Burada $b$ başlığı, $a$ açıklamayı, $t$ teknolojileri, $g$ görselleri, $l$ bağlantıları ve $d$ tarihi temsil eder. Bu yaklaşım önemlidir: Önce içerik modelini kurar, sonra onu yönetecek aracı seçeriz. Aksi hâlde portföyümüz, kullandığımız temanın izin verdiği kadar özgün olur.

Bir ziyaretçinin projeye ulaşma süresini kabaca şu şekilde değerlendirebiliriz:

$$
T_{toplam} = T_{sunucu} + T_{veri} + T_{arayüz}
$$

Statik sistemler genellikle veri tabanı aşamasını ortadan kaldırdığı için daha hızlıdır. Ancak kullanım kolaylığı ve editör deneyimi de hesaba katılmalıdır.

## Üç farklı yaklaşım

| Özellik | WordPress | Grav | Hugo |
|---|---|---|---|
| Mimari | Veri tabanlı CMS | Dosya tabanlı CMS | Statik site üreticisi |
| Yönetim paneli | Hazır ve güçlü | Eklentiyle kullanılabilir | Varsayılan olarak yok |
| Performans | Önbellekleme gerektirebilir | Hızlı | Çok hızlı |
| İçerik biçimi | Editör ve veri tabanı | Markdown | Markdown |
| Öğrenme eğrisi | Düşük | Orta | Orta |
| Dağıtım | PHP sunucusu | PHP sunucusu | Statik hosting |

### WordPress: Konforlu yönetim

Sık sık proje ekleyecek, teknik olmayan kişilere içerik düzenletecek veya iletişim formu, çoklu dil ve SEO eklentileri kullanacaksanız WordPress güçlü bir seçimdir. Projeleri normal yazılar yerine özel içerik türü olarak tanımlamak düzeni korur:

```php
function portfolio_project_type() {
    register_post_type('project', [
        'label' => 'Projeler',
        'public' => true,
        'has_archive' => true,
        'supports' => ['title', 'editor', 'thumbnail']
    ]);
}
add_action('init', 'portfolio_project_type');
```

Bu kod yönetim paneline “Projeler” bölümü ekler. Teknolojiler için özel taksonomi, canlı demo ve GitHub adresleri için özel alanlar tanımlanabilir.

### Grav: Veri tabansız CMS dengesi

Grav, Markdown dosyalarını klasör yapısıyla yönetir. WordPress kadar ağır değildir; buna rağmen yönetim paneli eklenebilir. Bir proje dosyası şöyle görünebilir:

```yaml
---
title: Hava Durumu Uygulaması
date: 2026-09-01
technologies: [JavaScript, API, CSS]
demo: https://example.com
---
Gerçek zamanlı hava verilerini gösteren responsive uygulama.
```

Ön bölümdeki YAML alanları şablon tarafından okunur. Böylece içerik ile tasarım ayrılır; Git üzerinden sürüm takibi yapmak da kolaylaşır.

### Hugo: Hız tutkunu geliştiriciler için

Hugo, Markdown içeriklerini önceden HTML dosyalarına dönüştürür. Sunucuda PHP veya veri tabanı çalışmadığından saldırı yüzeyi küçülür. Yeni bir proje oluşturmak için:

```bash
hugo new projects/hava-durumu.md
hugo server -D
```

İlk komut içerik dosyasını üretir, ikincisi yerel geliştirme sunucusunu başlatır. GitHub Actions ile her gönderimde otomatik derleme yaparak siteyi Netlify, Cloudflare Pages veya GitHub Pages üzerinde yayımlayabilirsiniz.

## Hangisini seçmelisiniz?

| İhtiyaç | Öneri |
|---|---|
| Kod yazmadan içerik yönetmek | WordPress |
| Markdown ve yönetim panelini birleştirmek | Grav |
| En yüksek hız ve Git tabanlı süreç | Hugo |
| Çok sayıda hazır eklenti kullanmak | WordPress |
| Basit sunucu ve taşınabilir içerik | Grav veya Hugo |

Son karar yalnızca hız testine dayanmamalıdır. Tek başınıza çalışan bir geliştiriciyseniz Hugo, müşteriye teslim edilecek kolay yönetilebilir bir sistem arıyorsanız WordPress, iki dünyanın arasında hafif bir çözüm istiyorsanız Grav mantıklıdır. Hangi aracı seçerseniz seçin; tutarlı proje modeli, responsive tasarım, erişilebilirlik, sıkıştırılmış görseller ve açık iletişim bağlantıları başarılı portföyün gerçek temelidir.
