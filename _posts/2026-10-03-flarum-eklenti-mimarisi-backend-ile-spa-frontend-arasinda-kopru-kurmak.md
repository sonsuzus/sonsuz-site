---
layout: post
title: "Flarum Eklenti Mimarisi: Backend ile SPA Frontend Arasında Köprü Kurmak"
math: true
categories: 
  - Program
tags: 
  - flarum
  - php
  - javascript
  - spa
  - json-api
  - eklenti-geliştirme
toc: true
image: /img/flarum-eklenti-mimarisi-58.png
---

Flarum’da eklenti geliştirmek, birkaç PHP dosyasını foruma iliştirmekten çok daha fazlasıdır. Bir tarafta Laravel bileşenlerinden yararlanan PHP backend, diğer tarafta Mithril tabanlı tek sayfa uygulaması bulunur. Güçlü bir eklenti yazmanın sırrı, bu iki dünyayı Flarum’un API, olay ve genişletici katmanları üzerinden konuşturmaktır.


![flarum-eklenti-mimarisi-58](/img/flarum-eklenti-mimarisi-58.svg)

``

## Büyük resim: İki uygulama, tek deneyim

Flarum’un forum ve yönetim arayüzleri SPA mantığıyla çalışır. Sayfa geçişlerinde belgenin tamamı yenilenmez; Mithril bileşenleri gerekli verileri API üzerinden alıp görünümü günceller. Backend ise kimlik doğrulama, yetkilendirme, veri saklama ve iş kurallarından sorumludur.

| Katman | Temel teknoloji | Sorumluluk |
|---|---|---|
| Backend | PHP, Composer, Illuminate bileşenleri | İş kuralları, izinler ve veritabanı |
| API | JSON:API | Verinin standart biçimde taşınması |
| Frontend | JavaScript, Mithril | Etkileşimli kullanıcı arayüzü |
| Paketleme | Composer ve npm | Bağımlılık ve sürüm yönetimi |

Bir ekranın yaklaşık yanıt süresini basitçe

$$T_{ekran}=T_{istek}+T_{backend}+T_{ağ}+T_{render}$$

şeklinde düşünebiliriz. Aynı bilgiyi ayrı isteklerle toplamak $T_{istek}$ ve $T_{ağ}$ maliyetini artırır. Bu nedenle ihtiyaç duyulan küçük alanları mevcut JSON:API kaynaklarına eklemek çoğu zaman yeni endpoint açmaktan daha verimlidir.

## Backend’i genişleticilerle kurmak

Eklentinin giriş noktası genellikle `extend.php` dosyasıdır. Flarum’un extender yaklaşımı, çekirdek sınıfları değiştirmeden API serileştiricilerine alan eklemeyi, rotalar tanımlamayı ve olayları dinlemeyi sağlar.

```php
<?php

use Flarum\Api\Serializer\UserSerializer;
use Flarum\Extend;

return [
    (new Extend\ApiSerializer(UserSerializer::class))
        ->attribute('reputation', function ($serializer, $user) {
            return (int) ($user->reputation ?? 0);
        }),
];
```

Bu örnek, kullanıcı kaynağına `reputation` alanını ekler. Gerçek bir projede sütun önce migration ile oluşturulmalı; değeri değiştiren işlemler doğrulanmalı ve yalnızca yetkili aktörlere açılmalıdır. Frontend’den gelen veriye güvenmek, forum kapısına “Lütfen kötü niyetli olmayın” tabelası asmaktan pek farklı değildir.

Daha karmaşık işlemlerde route-handler ikilisi yerine komut, handler ve event katmanları kullanmak yararlıdır. Böylece “itibar puanı ver” işlemi API çağrısından, konsol komutundan veya başka bir eklentiden tekrar kullanılabilir.

## Frontend’de modeli ve görünümü genişletmek

Backend alanı gönderdiğinde frontend modeline bu alanı tanıtabiliriz:

```javascript
import app from 'flarum/forum/app';
import Model from 'flarum/common/Model';
import User from 'flarum/common/models/User';

app.initializers.add('acme-reputation', () => {
  User.prototype.reputation = Model.attribute('reputation');

  console.log('İtibar eklentisi hazır!');
});
```

Artık bir kullanıcı nesnesinde `user.reputation()` çağrısı yapılabilir. Görünümü değiştirmek için Flarum bileşenlerini doğrudan kopyalamak yerine `extend` veya `override` yardımcıları kullanılmalıdır. `extend`, mevcut davranışa ekleme yaptığı için diğer eklentilerle daha barışçıldır; `override` ise ancak davranışın tamamen değiştirilmesi gerektiğinde tercih edilmelidir.

| Yaklaşım | Uyumluluk | Kullanım amacı |
|---|---:|---|
| `extend` | Yüksek | Listeye düğme, rozet veya içerik eklemek |
| `override` | Orta/düşük | Mevcut davranışı bütünüyle değiştirmek |
| DOM’a elle müdahale | Çok düşük | Mümkünse kaçınılması gereken kestirme yol |

## Ekosistem dinamikleri ve sağlamlık

Flarum eklentileri izole yaşamaz. Başka eklentiler aynı serializer’ı, modeli veya bileşeni genişletebilir. Bu nedenle benzersiz paket adları, önekli veritabanı sütunları ve dar kapsamlı CSS sınıfları kullanılmalıdır. Composer sürüm kısıtları Flarum çekirdeğiyle uyumluluğu açıkça belirtmeli; JavaScript bağımlılıkları da gereksiz yere çoğaltılmamalıdır.

API işlemlerinde yetki backend’de denetlenmeli, hata yanıtları frontend’de yakalanmalı ve kullanıcıya anlaşılır bildirim gösterilmelidir. Geliştirme döngüsünde PHP testleri iş kurallarını, frontend testleri bileşen davranışını doğrulamalıdır. Sonuçta iyi bir Flarum eklentisi yalnızca çalışan değil; çekirdeğe dokunmadan genişleyen, diğer paketlerle kavga etmeyen ve sürüm yükseltmelerinden sağ çıkabilen eklentidir.
