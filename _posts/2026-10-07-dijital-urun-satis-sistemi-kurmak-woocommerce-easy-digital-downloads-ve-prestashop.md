---
layout: post
title: "Dijital Ürün Satış Sistemi Kurmak: WooCommerce, Easy Digital Downloads ve PrestaShop"
math: true
categories: 
  - Proje
tags: 
  - woocommerce
  - easy-digital-downloads
  - prestashop
  - dijital-ürün
  - e-ticaret
  - wordpress
toc: true
image: /img/dijital-urun-satis-95.png
---

![dijital-urun-satis-95](/img/dijital-urun-satis-95.svg)


E-kitap, yazılım lisansı, tasarım şablonu veya çevrim içi eğitim satmak kulağa basit gelir: Dosyayı yükle, fiyatı belirle ve satışları bekle! Fakat güvenli teslimat, ödeme doğrulama, vergi, lisans yönetimi ve müşteri deneyimi devreye girdiğinde küçük dükkânımız gerçek bir yazılım projesine dönüşür. Bu yazıda WooCommerce, Easy Digital Downloads ve PrestaShop seçeneklerini karşılaştırarak doğru sistemi nasıl kurabileceğimizi inceleyeceğiz.

``

## Dijital satışın temel mantığı

Dijital ürünlerde fiziksel stok bulunmasa da erişim hakkı bir çeşit stok gibi düşünülmelidir. Başarılı bir siparişin yaşam döngüsü şöyledir:

1. Müşteri ürünü sepete ekler.
2. Ödeme sağlayıcısı işlemi doğrular.
3. Sistem siparişi tamamlandı durumuna geçirir.
4. Kullanıcıya süreli veya indirme sayısı sınırlı bir bağlantı verir.
5. İşlem fatura, e-posta ve kayıt mekanizmalarına aktarılır.

Dosyanın herkese açık bir klasörde tutulması büyük hatadır. Teslimat bağlantısı tahmin edilemez, kullanıcıya özel ve mümkünse zaman aşımına sahip olmalıdır. Örneğin bağlantının geçerliliği $T = 24$ saat, indirme limiti ise $L = 3$ olarak tanımlanabilir.

Satışın ekonomik tarafını da unutmamalıyız. Basitleştirilmiş net gelir hesabı:

$$N = F - K - V - I$$

Burada $F$ satış fiyatını, $K$ ödeme komisyonunu, $V$ vergiyi, $I$ ise iade maliyetini temsil eder. Platform seçerken yalnızca kurulum ücretine değil, bu değişkenlerin nasıl yönetildiğine de bakılmalıdır.

## Üç platformun karşılaştırması

| Özellik | WooCommerce | Easy Digital Downloads | PrestaShop |
|---|---|---|---|
| Altyapı | WordPress eklentisi | WordPress eklentisi | Bağımsız e-ticaret sistemi |
| Ana yaklaşım | Fiziksel ve dijital ürün | Dijital ürüne odaklı | Geniş kapsamlı mağaza |
| Kurulum kolaylığı | Kolay | Çok kolay | Orta |
| Özelleştirme | Çok yüksek | Yüksek | Yüksek |
| Kaynak tüketimi | Eklentilere bağlı | Genellikle düşük | Görece yüksek |
| Uygun senaryo | Karma mağaza | Dosya ve lisans satışı | Büyük katalog, çoklu mağaza |

**WooCommerce**, ileride fiziksel ürün satmayı düşünenler için esnek bir seçimdir. Tema ve eklenti ekosistemi oldukça geniştir; ancak gereksiz eklentiler performansı ve güvenliği olumsuz etkileyebilir.

**Easy Digital Downloads**, kısaca EDD, dijital teslimatı merkeze alır. İndirme kayıtları, müşteri geçmişi ve dosya erişimi daha sade biçimde yönetilir. Yazılım lisansı, üyelik veya abonelik için ücretli eklentiler gerekebilir.

**PrestaShop** ise bağımsız ve kapsamlı bir mağaza motorudur. Çoklu dil, para birimi ve büyük katalog yönetiminde güçlüdür. Yalnızca birkaç PDF satılacaksa biraz top ile sivrisinek avlamak sayılabilir!

## WooCommerce ile örnek erişim kontrolü

Aşağıdaki PHP kodu, tamamlanan sipariş sonrasında basit bir kayıt oluşturur. Gerçek projede kayıt; lisans anahtarı, süre sonu ve ürün kimliğiyle genişletilmelidir.

```php
add_action('woocommerce_order_status_completed', 'urun_erisim_kaydi');

function urun_erisim_kaydi($order_id) {
    $order = wc_get_order($order_id);

    foreach ($order->get_items() as $item) {
        if ($item->get_product()->is_downloadable()) {
            update_post_meta(
                $order_id,
                '_dijital_erisim_zamani',
                current_time('mysql')
            );
        }
    }
}
```

`woocommerce_order_status_completed` kancası sipariş tamamlandığında çalışır. Kod, siparişte indirilebilir ürün bulunursa erişim zamanını meta veri olarak saklar. Böylece destek, denetim veya özel lisans süreçleri için iz bırakılır.

## Hangi platformu seçmelisin?

Hızlıca e-kitap, müzik veya şablon satacaksan EDD en temiz başlangıçtır. Dijital ve fiziksel ürünleri aynı sepette buluşturmak istiyorsan WooCommerce daha mantıklıdır. Çok dilli, kapsamlı ve bağımsız bir mağaza hedefliyorsan PrestaShop öne çıkar.

Platform ne olursa olsun SSL, düzenli yedekleme, güvenli ödeme altyapısı, KVKK uyumu ve test siparişleri zorunlu kabul edilmelidir. En iyi sistem, en fazla özelliğe sahip olan değil; müşterinin ödemeden indirmeye kadar sorunsuz ilerlediği sistemdir.
