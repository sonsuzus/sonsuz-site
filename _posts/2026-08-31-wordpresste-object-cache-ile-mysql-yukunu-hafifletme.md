---
layout: post
title: "WordPress'te Object Cache ile MySQL Yükünü Hafifletme"
math: true
categories: 
  - Bilgi
tags: 
  - wordpress
  - object cache
  - mysql
toc: true
---

Yüksek trafikli bir WordPress sitesinde MySQL, aynı sorulara tekrar tekrar cevap veren yorgun bir danışmana dönüşebilir: “Bu yazının meta bilgileri nedir?”, “Menüde hangi bağlantılar var?”, “Bu ayarlar değişti mi?” Object Cache, sık kullanılan sonuçları bellekte tutarak danışmanın masasını gereksiz isteklerden temizler. Böylece hem sayfalar hızlanır hem de veritabanı gerçekten gerekli sorgularla ilgilenir.
``
## Object Cache tam olarak neyi önbellekler?

WordPress; yazılar, kullanıcılar, seçenekler ve sorgu sonuçları gibi birçok veriyi çalışırken nesnelere dönüştürür. Object Cache, bu nesneleri bir anahtar altında saklar. Aynı veri yeniden istendiğinde MySQL sorgusu çalıştırmak yerine sonuç doğrudan bellekten alınır.

Bir önbelleğin başarısını **isabet oranıyla** ifade edebiliriz:

$$H = \frac{C_{hit}}{C_{hit}+C_{miss}}$$

Burada $C_{hit}$ bellekte bulunan, $C_{miss}$ ise bulunamadığı için yeniden üretilen sonuç sayısıdır. Sayfa başına normalde $Q$ sorgu çalışıyorsa yaklaşık veritabanı yükü şöyle düşünülebilir:

$$Q_{etkin} \approx Q \times (1-H)$$

Örneğin 100 sorguluk bir istekte isabet oranı %80 ise MySQL'e ulaşan teorik yük yaklaşık 20 sorguya iner. Gerçek değer; sorgu türlerine, eklentilere ve önbellek geçersizleştirme davranışına bağlıdır.

## Varsayılan ve kalıcı önbellek farkı

WordPress'in yerleşik Object Cache sistemi yalnızca mevcut PHP isteği boyunca yaşar. Kalıcı bir altyapı kullanılmadığında sonraki ziyaretçi her şeye baştan başlar. Redis veya Memcached entegrasyonu ise nesneleri istekler arasında korur.

| Yöntem | Yaşam süresi | Uygun kullanım | Sınırlama |
|---|---:|---|---|
| Varsayılan Object Cache | Tek istek | Aynı işlemde tekrarlanan çağrılar | Sonraki isteğe aktarılmaz |
| Redis | Kalıcı, TTL kontrollü | Yoğun WordPress siteleri | Bellek ve servis yönetimi gerekir |
| Memcached | Kalıcı, TTL kontrollü | Basit ve dağıtık önbellekleme | Veri yapıları Redis'ten sınırlıdır |
| Sayfa önbelleği | Tüm HTML çıktısı | Anonim ziyaretçiler | Kişiselleştirilmiş içerikte dikkat ister |

Object Cache ile sayfa önbelleği rakip değildir. Sayfa önbelleği hazırlanmış HTML'yi sunarken Object Cache, HTML yeniden üretilmek zorunda kaldığında kullanılan verileri hızlandırır.

## Redis'i WordPress'e bağlamak

Sunucuda Redis kurulduktan sonra uyumlu bir eklenti etkinleştirilebilir. Bağlantı bilgileri `wp-config.php` dosyasında tanımlanır:

```php
// Redis sunucusunun adresi ve portu.
define("WP_REDIS_HOST", "127.0.0.1");
define("WP_REDIS_PORT", 6379);

// Aynı Redis'i kullanan sitelerin anahtarlarını ayırır.
define("WP_CACHE_KEY_SALT", "ornek-blog:");
```

Eklentinin `object-cache.php` drop-in dosyasını oluşturduğunu doğrulamak önemlidir. Yalnızca Redis servisinin çalışması, WordPress'in onu kullandığı anlamına gelmez.

## Özel sorguları bilinçli biçimde saklamak

Pahalı bir rapor sorgusu `wp_cache_get()` ve `wp_cache_set()` ile önbelleğe alınabilir:

```php
function populer_yazilar() {
    $key   = "populer_yazilar_v1";
    $group = "blog_raporlari";
    $data  = wp_cache_get($key, $group);

    if (false === $data) {
        // Yalnızca cache miss olduğunda pahalı sorguyu çalıştırır.
        $data = new WP_Query([
            "posts_per_page" => 10,
            "meta_key"       => "goruntulenme",
            "orderby"        => "meta_value_num"
        ]);

        wp_cache_set($key, $data, $group, 300);
    }

    return $data;
}
```

Beş dakikalık TTL, güncellik ile performans arasında denge kurar. Ancak içerik güncellendiğinde eski sonucu bekletmek yerine `save_post` kancasında `wp_cache_delete()` çağırmak daha temizdir.

## En sık yapılan hatalar

Çok uzun TTL kullanmak bayat içerik üretir; çok kısa TTL ise önbelleği pahalı bir süs eşyasına çevirir. Aynı anda süresi dolan popüler anahtarlar ayrıca **cache stampede** yaratabilir: Yüzlerce istek aynı sorguyu yeniden çalıştırır. TTL değerlerine küçük rastgele sapmalar eklemek ve kilitleme mekanizması kullanmak bu hücumu azaltır.

Son olarak Query Monitor, Redis istatistikleri ve MySQL slow query log birlikte izlenmelidir. Hedef “her şeyi cache'lemek” değil; yüksek maliyetli, sık tekrarlanan ve kabul edilebilir süre boyunca değişmeyen verileri saklamaktır. Doğru kurulan Object Cache, MySQL'i emekliye ayırmaz; ona hak ettiği sakin çalışma ortamını verir.
