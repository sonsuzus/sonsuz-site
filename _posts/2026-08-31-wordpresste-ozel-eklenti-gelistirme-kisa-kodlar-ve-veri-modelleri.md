---
layout: post
title: "WordPress’te Özel Eklenti Geliştirme: Kısa Kodlar ve Veri Modelleri"
math: true
categories: 
  - Program
tags: 
  - wordpress
  - php
  - eklenti geliştirme
toc: true
---

Hazır WordPress temaları hızlı başlangıç sağlar; ancak etkinlik kataloğu, ekip listesi veya projeye özgü bir başvuru sistemi istediğinizde tema seçenekleri duvara toslayabilir. Çözüm, `functions.php` dosyasını yamalı bohçaya çevirmek değil, iş mantığını bağımsız bir eklentiye taşımaktır. Böylece tema değişse bile kısa kodlarınız ve verileriniz yerinde kalır.

``

## Eklenti mi, tema kodu mu?

Temanın görevi sunum, eklentinin görevi davranış ve veri yönetimidir. Bir özellik tema değiştirildiğinde de gerekli olacaksa eklentiye aittir. Örneğin kurumsal projeleri saklayan veri modeli içeriktir; kartların rengi ise temanın sorumluluğudur.

| İhtiyaç | Tema | Özel eklenti |
|---|---:|---:|
| Renk ve tipografi | Uygun | Gereksiz |
| Özel içerik türü | Riskli | Uygun |
| Kısa kod | Mümkün | Daha sürdürülebilir |
| Tema değişiminden etkilenmeme | Hayır | Evet |
| Yeniden kullanılabilirlik | Düşük | Yüksek |

Basitçe bir özelliği $F = V + L + D$ şeklinde düşünebiliriz. Burada $V$ görünüm, $L$ iş mantığı, $D$ ise veridir. Tema ağırlıklı olarak $V$ ile, eklenti ise $L$ ve $D$ ile ilgilenmelidir. Bu ayrım teknik borcu azaltır.

## Eklenti iskeletini oluşturmak

`wp-content/plugins` altında `ozel-projeler` klasörü ve içinde `ozel-projeler.php` dosyası oluşturun:

```php
<?php
/**
 * Plugin Name: Özel Projeler
 * Description: Proje veri modeli ve listeleme kısa kodu ekler.
 * Version: 1.0.0
 */

defined('ABSPATH') || exit;

function op_register_project_type() {
    register_post_type('op_project', [
        'labels' => [
            'name' => 'Projeler',
            'singular_name' => 'Proje'
        ],
        'public' => true,
        'show_in_rest' => true,
        'has_archive' => true,
        'rewrite' => ['slug' => 'projeler'],
        'supports' => ['title', 'editor', 'thumbnail', 'excerpt']
    ]);
}
add_action('init', 'op_register_project_type');
```

`register_post_type`, WordPress’in yazı altyapısını yeni bir veri modeline dönüştürür. `show_in_rest` Gutenberg ve REST API desteğini, `supports` ise yönetim ekranındaki alanları belirler. Fonksiyonun `init` kancasına bağlanması önemlidir; WordPress yolları hazırlamadan önce içerik türü kaydedilmemelidir.

## Dinamik kısa kod yazmak

Şimdi ziyaretçinin `[proje_listesi adet="6"]` yazarak projeleri çağırmasını sağlayalım:

```php
function op_project_shortcode($atts) {
    $atts = shortcode_atts(['adet' => 6], $atts);
    $limit = max(1, min(20, absint($atts['adet'])));

    $query = new WP_Query([
        'post_type' => 'op_project',
        'posts_per_page' => $limit,
        'post_status' => 'publish'
    ]);

    ob_start();
    echo '<div class="op-projects">';

    while ($query->have_posts()) {
        $query->the_post();
        printf(
            '<article><h3><a href="%s">%s</a></h3><p>%s</p></article>',
            esc_url(get_permalink()),
            esc_html(get_the_title()),
            esc_html(get_the_excerpt())
        );
    }

    echo '</div>';
    wp_reset_postdata();
    return ob_get_clean();
}
add_shortcode('proje_listesi', 'op_project_shortcode');
```

Kısa kod fonksiyonu çıktıyı doğrudan basmak yerine döndürmelidir. `ob_start()` üretilen HTML’yi tamponlar; `ob_get_clean()` ise onu metin olarak geri verir. `absint` kullanıcı parametresini sayıya dönüştürür, `min` sorgunun kontrolden çıkmasını önler. Yaklaşık sorgu yükünü $Y \propto n \times a$ olarak düşünebiliriz: $n$ içerik sayısı, $a$ ise getirilen ek alanların maliyetidir.

## Güvenlik ve performans

WordPress geliştirmede “çalışıyor” yeterli değildir. URL’leri `esc_url`, düz metinleri `esc_html`, HTML özniteliklerini `esc_attr` ile kaçırın. Yönetim formu eklerseniz nonce doğrulaması ve `current_user_can()` yetki kontrolü kullanın. Veritabanına doğrudan sorgu göndermeniz gerekirse `$wpdb->prepare()` zorunlu arkadaşınızdır.

Çok ziyaret edilen listeleri Transients API ile önbelleğe almak da mantıklıdır. Böylece her sayfa açılışında aynı sorgu tekrarlanmaz. Sonuçta iyi bir özel eklenti; veriyi modelleyen, girdiyi doğrulayan, çıktıyı kaçıran ve temadan bağımsız çalışan küçük ama disiplinli bir uygulamadır.
