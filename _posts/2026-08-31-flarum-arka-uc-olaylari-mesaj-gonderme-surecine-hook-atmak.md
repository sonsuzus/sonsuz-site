---
layout: post
title: "Flarum Arka Uç Olayları: Mesaj Gönderme Sürecine Hook Atmak"
math: true
categories: 
  - Bilgi
tags: 
  - flarum
  - php
  - event hooks
toc: true
---

Bir kullanıcı Flarum’da “Gönder” düğmesine bastığında mesaj doğrudan veritabanına ışınlanmaz. İçerik doğrulanır, yetkiler denetlenir, model hazırlanır ve kayıt işlemi tamamlanır. Flarum’un arka uç olayları, eklentilerin bu akışın belirli noktalarına dinleyici yerleştirmesine izin verir. Böylece çekirdek kodu değiştirmeden mesajı denetleyebilir, dönüştürebilir veya tamamen reddedebiliriz.
``
## Olay tabanlı genişletilebilirlik

Bir **event**, sistemde anlamlı bir şeyin gerçekleşmek üzere olduğunu veya gerçekleştiğini bildiren PHP nesnesidir. **Listener** ise bu bildirimi alan ve kendi işini yapan sınıftır. Hook sözcüğü genel mekanizmayı anlatırken event ve listener, Flarum’daki somut parçaları ifade eder.

Mesaj kaydetme sürecini basitleştirerek şöyle modelleyebiliriz:

$$İstek \rightarrow Doğrulama \rightarrow Saving \rightarrow Kayıt \rightarrow Posted$$

Bir olaya bağlı toplam çalışma maliyeti kabaca

$$T_{toplam}=T_{çekirdek}+\sum_{i=1}^{n}T_{listener_i}$$

şeklindedir. Yani her dinleyici esneklik kazandırırken küçük de olsa maliyet ekler. Listener içinde yavaş bir harici API çağrısı yapmak, kullanıcının gönderim ekranında beklemesine yol açabilir.

| Aşama | Ne zaman çalışır? | Uygun kullanım |
|---|---|---|
| `Saving` | Model kaydedilmeden önce | İçeriği değiştirme, doğrulama, gönderimi engelleme |
| `Posted` | Yeni mesaj oluşturulduktan sonra | Bildirim, log, kuyruk işi başlatma |
| `Revised` | Mesaj düzenlendikten sonra | Değişiklik kaydı, yeniden indeksleme |

En kritik ayrım şudur: Öncesi olaylarında karar verebiliriz; sonrası olaylarında ise genellikle gerçekleşen sonuca tepki veririz.

## Listener’ı kaydetmek

Bir Flarum eklentisinin `extend.php` dosyasında dinleyici şu şekilde bağlanabilir:

```php
<?php

use Flarum\Extend;
use Flarum\Post\Event\Saving;
use Acme\Guard\Listener\InspectPost;

return [
    (new Extend\Event())
        ->listen(Saving::class, InspectPost::class),
];
```

Bu tanım, `Saving` olayı yayımlandığında `InspectPost` sınıfının çağrılmasını sağlar. İş mantığını `extend.php` içine doldurmak yerine ayrı sınıfta tutmak test edilebilirliği artırır.

## Mesajın arasına girmek

Aşağıdaki listener, yeni mesajlardaki gereksiz boşlukları temizler ve yasaklı bir ifade görürse gönderimi durdurur:

```php
<?php

namespace Acme\Guard\Listener;

use Flarum\Post\Event\Saving;
use Flarum\User\Exception\PermissionDeniedException;

class InspectPost
{
    public function handle(Saving $event): void
    {
        $attributes = $event->data['attributes'] ?? [];

        if (! array_key_exists('content', $attributes)) {
            return;
        }

        $content = trim($attributes['content']);
        $content = preg_replace('/[ \t]+/', ' ', $content);

        if (str_contains(mb_strtolower($content), 'yasaklı-ifade')) {
            throw new PermissionDeniedException();
        }

        $event->post->content = $content;
    }
}
```

`$event->data`, istemciden gelen değişiklikleri taşır; `$event->post` ise kaydedilecek modeli temsil eder. `content` her istekte bulunmayabileceği için önce anahtar kontrolü yapılır. İstisna fırlatıldığında normal kayıt akışı kesilir ve kullanıcıya hata yanıtı döner. Gerçek projelerde genel yetki hatası yerine çevrilebilir, açıklayıcı bir doğrulama hatası tercih edilebilir.

## Sağlam hook tasarımının kuralları

Listener mümkün olduğunca **tek sorumluluklu** ve **idempotent** olmalıdır. Aynı işlem iki kez çalıştığında sonuç değişmiyorsa idempotent kabul edilir:

$$f(f(x))=f(x)$$

Örneğin baştaki ve sondaki boşlukları temizlemek idempotenttir; mesaja her çalışmada yeniden imza eklemek değildir. Ayrıca kullanıcı girdisine güvenilmemeli, aktörün yetkileri `$event->actor` üzerinden kontrol edilmeli ve ağır işler kuyruk sistemine aktarılmalıdır.

Kısacası Flarum events, çekirdek dosyalara tornavidayla dalmadan davranış değiştirmeyi sağlar. Doğru olayı seçen, küçük ve öngörülebilir listener’lar yazan bir eklenti; spam filtresinden otomatik etiketlemeye kadar pek çok özelliği forumun doğal parçasıymış gibi çalıştırabilir.
