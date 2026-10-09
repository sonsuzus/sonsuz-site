---
layout: post
title: "Üyelik ve Topluluk Sistemi Seçimi: HumHub, BuddyPress ve Discourse"
math: true
categories: 
  - Program
tags: 
  - humhub
  - buddypress
  - discourse
  - topluluk
  - üyelik
  - açık-kaynak
toc: true
image: /img/uyelik-ve-topluluk-97.png
---

![uyelik-ve-topluluk-97](/img/uyelik-ve-topluluk-97.svg)


Bir topluluk platformu kurmak, yalnızca kullanıcıların kayıt olabileceği bir sayfa hazırlamak değildir. Profil yönetimi, içerik üretimi, bildirimler, moderasyon, yetkilendirme ve kullanıcıların geri dönmesini sağlayan sosyal mekanikler birlikte düşünülmelidir. HumHub, BuddyPress ve Discourse bu problemi farklı açılardan çözer: biri sosyal ağ, biri WordPress eklentisi, diğeri ise modern forum yaklaşımını benimser.

``

## Önce topluluk sisteminin mantığı

Bir üyelik sisteminin merkezinde **kimlik**, **yetki** ve **etkileşim** bulunur. Kimlik katmanı kullanıcının kim olduğunu; yetkilendirme katmanı hangi işlemleri yapabileceğini; etkileşim katmanı ise diğer üyelerle nasıl iletişim kuracağını belirler.

Basit bir topluluk veri modeli şöyle düşünülebilir:

```text
Kullanıcı → Profil → Rol
Kullanıcı → İçerik → Yorum
Kullanıcı → Grup → Üyelik
İçerik → Bildirim → Kullanıcı
```

Topluluk sağlığını ölçmek için yalnızca kayıtlı kullanıcı sayısına bakmak yanıltıcıdır. Daha anlamlı bir ölçü, aktif kullanıcı oranıdır:

$$
A = \frac{Günlük\ aktif\ kullanıcı}{Toplam\ kayıtlı\ kullanıcı} \times 100
$$

Örneğin 10.000 üyenin yalnızca 200'ü günlük olarak geri dönüyorsa aktiflik oranı yüzde 2'dir. Dolayısıyla yazılım seçerken özellik listesinden çok, hedeflenen etkileşim biçimine odaklanmak gerekir.

## Üç platformun karakteri

| Platform | Temel yaklaşım | Güçlü olduğu alan | Teknik yapı |
|---|---|---|---|
| HumHub | Özel sosyal ağ | Gruplar, profiller, kurum içi iletişim | PHP, Yii, MySQL |
| BuddyPress | WordPress'e sosyal katman | İçerik sitesiyle üyeliği birleştirme | PHP, WordPress, MySQL |
| Discourse | Tartışma ve bilgi paylaşımı | Forumlar, destek toplulukları | Ruby on Rails, PostgreSQL, Redis |

### HumHub

HumHub, Facebook benzeri akışların ve çalışma alanlarının önemli olduğu projelerde öne çıkar. Kullanıcılar profil oluşturabilir, alanlara katılabilir, gönderi paylaşabilir ve birbirlerini takip edebilir. Üniversite kulübü, şirket içi ağ veya kapalı meslek topluluğu için doğal bir seçimdir.

Modüler yapısı sayesinde takvim, görev ve dosya paylaşımı gibi yetenekler eklenebilir. Ancak tema ve modül ekosistemi WordPress kadar geniş değildir. Sunucu yönetimi konusunda temel Linux, PHP ve veritabanı bilgisi gerekir.

### BuddyPress

BuddyPress bağımsız bir uygulama değil, WordPress'i topluluk sistemine dönüştüren bir eklentidir. Mevcut sitenizde blog, kurs, mağaza veya üyelik altyapısı varsa oldukça pratiktir. WooCommerce ve LMS eklentileriyle beraber kullanıldığında ücretli topluluklar kurulabilir.

WordPress kancaları üzerinden davranış eklemek mümkündür:

```php
add_action('bp_init', function () {
    // BuddyPress yüklendikten sonra özel topluluk işlemlerini başlatır.
    if (is_user_logged_in()) {
        update_user_meta(get_current_user_id(), 'son_topluluk_girisi', time());
    }
});
```

Bu kod, giriş yapmış üyenin son topluluk ziyaretini kaydeder. Böylece geri dönüş oranı veya pasif üyeler analiz edilebilir. Bununla birlikte çok sayıda eklenti kullanmak performans, güvenlik ve uyumluluk sorunları doğurabilir.

### Discourse

Discourse, klasik forumları daha akıcı hale getirir. Güven seviyeleri, güçlü moderasyon araçları, e-posta ile yanıt, rozetler ve gerçek zamanlı bildirimler hazır gelir. Teknik destek, açık kaynak proje veya soru-cevap odaklı topluluklar için başarılıdır.

Platformun güven sistemi, olumlu davranış sergileyen kullanıcılara zamanla daha fazla yetki verir. Bu yaklaşım moderasyon yükünü topluluğa dağıtır. Docker tabanlı önerilen kurulum güvenilir olsa da düşük kaynaklı paylaşımlı hosting paketlerine pek uygun değildir.

## Hangisini seçmelisiniz?

| İhtiyaç | Öneri |
|---|---|
| Kurum içi sosyal ağ | HumHub |
| WordPress tabanlı üyelik sitesi | BuddyPress |
| Destek, tartışma ve bilgi arşivi | Discourse |
| E-ticaretle bütünleşme | BuddyPress |
| Güçlü yerleşik moderasyon | Discourse |

Karar verirken toplam maliyeti $M = K + B + E$ biçiminde değerlendirebilirsiniz. Burada $K$ kurulum, $B$ bakım, $E$ ise eklenti ve entegrasyon gideridir. Yazılımların açık kaynak olması, işletmenin tamamen ücretsiz olacağı anlamına gelmez.

Özetle sosyal akış ve gruplar için HumHub, WordPress ekosistemi için BuddyPress, uzun ömürlü tartışmalar için Discourse daha uygundur. En iyi platform, en çok özelliğe sahip olan değil; üyelerin neden geri geleceği sorusuna en net cevabı verendir.
