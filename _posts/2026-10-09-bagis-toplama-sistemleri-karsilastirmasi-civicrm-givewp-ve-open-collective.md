---
layout: post
title: "Bağış Toplama Sistemleri Karşılaştırması: CiviCRM, GiveWP ve Open Collective"
math: true
categories: 
  - Program
tags: 
  - bağış
  - civicrm
  - givewp
  - open-collective
  - wordpress
  - açık-kaynak
  - fintech
toc: true
image: /img/bagis-toplama-sistemleri-54.png
---

Bir bağış sistemi seçmek, web sitesine yalnızca renkli bir “Destek Ol” düğmesi eklemekten çok daha fazlasıdır. Bağışçı ilişkileri, ödeme altyapısı, kampanya takibi, şeffaflık ve raporlama gibi parçalar doğru biçimde birleşmelidir. CiviCRM, GiveWP ve Open Collective aynı amaca hizmet ediyor gibi görünse de farklı organizasyon modellerine hitap eder: biri kapsamlı bir ilişki yönetim sistemi, biri WordPress odaklı bağış eklentisi, diğeri ise şeffaf topluluk finansmanı platformudur.

``

## Önce temel mantık: Bağış sistemi nasıl çalışır?

Tipik bir bağış akışı; bağışçı, form, ödeme sağlayıcısı, işlem kaydı ve raporlama katmanlarından oluşur. Kullanıcı formu doldurduğunda sistem ödeme sağlayıcısına bir istek gönderir. Başarılı işlem sonrasında bağış kaydedilir, makbuz oluşturulur ve gerekiyorsa bağışçıya otomatik e-posta gönderilir.

Bir kampanyanın net geliri basitçe şöyle modellenebilir:

$$G_{net} = G_{brüt} - (G_{brüt} \times o_{komisyon}) - M_{sabit} - G_{iade}$$

Burada $o_{komisyon}$ ödeme sağlayıcısının oransal kesintisini, $M_{sabit}$ işlem başına sabit maliyetleri temsil eder. Dolayısıyla yalnızca yazılımın fiyatını değil, ödeme komisyonlarını ve operasyon yükünü de karşılaştırmak gerekir.

## Üç sistemin karakteri

| Sistem | Temel yaklaşım | Güçlü olduğu alan | Teknik ihtiyaç |
|---|---|---|---|
| CiviCRM | CRM ve bağış yönetimi | STK, dernek, üyelik ve etkinlik takibi | Orta-yüksek |
| GiveWP | WordPress bağış eklentisi | Hızlı kampanya sayfaları ve formlar | Orta |
| Open Collective | Şeffaf mali yönetim platformu | Açık kaynak ve topluluk projeleri | Düşük-orta |

![bagis-toplama-sistemleri-54](/img/bagis-toplama-sistemleri-54.svg)


### CiviCRM: Kurumsal hafıza isteyenlere

CiviCRM yalnızca ödeme almakla kalmaz; bağışçıları, üyelikleri, etkinlikleri, e-postaları ve geçmiş etkileşimleri tek profilde toplar. Drupal, Joomla veya WordPress ile çalışabilir. Özellikle aynı destekçiyle yıllar boyunca ilişki kuran kuruluşlar için güçlüdür.

Bunun karşılığında kurulum ve bakım daha zahmetlidir. Veri modeli, roller, izinler ve zamanlanmış görevler doğru yapılandırılmalıdır. Küçük bir kampanya için ağır gelebilir; fakat binlerce kişiyle çalışan bir STK için adeta dijital genel merkezdir.

### GiveWP: WordPress içinde pratik çözüm

GiveWP, mevcut WordPress sitesini bağış platformuna dönüştürür. Kampanya formları, hedef göstergeleri, bağışçı panelleri ve tekrarlayan ödeme özellikleri sunar. İçerik ekibinin WordPress’e aşina olması önemli bir avantajdır.

Basit bir entegrasyon mantığı şu şekilde düşünülebilir:

```php
add_action('give_insert_payment', function ($payment_id) {
    $amount = give_get_payment_total($payment_id);
    error_log('Yeni bağış tutarı: ' . $amount);
});
```

Bu örnek, yeni ödeme kaydedildiğinde bağış tutarını günlük dosyasına yazar. Gerçek projede aynı kanca CRM bildirimi göndermek veya özel bir teşekkür süreci başlatmak için kullanılabilir. Ancak ücretli eklentiler, ödeme ağ geçitleri ve WordPress güvenliği toplam maliyete eklenmelidir.

### Open Collective: Şeffaflık varsayılan ayar

Open Collective özellikle açık kaynak projeleri, yerel topluluklar ve gayriresmî gruplar için dikkat çekicidir. Gelirler ve giderler herkese açık gösterilebilir. Bir mali sponsor kullanıldığında topluluk, ayrı bir tüzel kişilik kurmadan para kabul etme ve harcama olanağı bulabilir.

Platformun en güçlü tarafı şeffaflıktır; ancak klasik CRM özellikleri veya tamamen özelleştirilebilir bağış deneyimi bekleyen kuruluşlar için sınırlı kalabilir.

## Hangisini seçmeli?

| İhtiyaç | Önerilen seçenek |
|---|---|
| Ayrıntılı bağışçı geçmişi ve üyelik yönetimi | CiviCRM |
| WordPress üzerinde hızlı bağış kampanyası | GiveWP |
| Herkese açık gelir-gider takibi | Open Collective |
| İleri düzey özelleştirme ve veri sahipliği | CiviCRM veya GiveWP |
| Minimum altyapı yönetimi | Open Collective |

Karar verirken bağış hacmi, ekip kapasitesi, veri gizliliği ve raporlama gereksinimleri birlikte değerlendirilmelidir. Kısacası CiviCRM ilişkiyi, GiveWP dönüşümü, Open Collective ise güveni ve şeffaflığı merkeze koyar. En iyi sistem en fazla özelliğe sahip olan değil, kuruluşunuzun günlük iş akışına en az sürtünmeyle uyum sağlayandır.
