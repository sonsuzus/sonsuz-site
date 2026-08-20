---
layout: post
title: "Ruby on Rails ile Hızlı Prototipleme: Şemadan Arayüze Giden Kısa Yol"
math: true
categories: 
  - Proje
tags: 
  - ruby on rails
  - hızlı prototipleme
  - convention over configuration
---

Bir fikri doğrulamak için haftalarca form, liste, doğrulama ve ilişki kodu yazmak zorunda değilsiniz. Ruby on Rails, **Convention over Configuration** yaklaşımıyla veritabanı şemasını uygulamanın omurgası kabul eder; doğru isimlendirilmiş tablolar, alanlar ve ilişkilerden yola çıkarak işlevsel bir yönetim arayüzü üretmeyi oldukça hızlandırır. Amaç kusursuz ürünü ilk günde yayınlamak değil, kullanıcıdan erken geri bildirim alacak kadar gerçek bir prototip oluşturmaktır.

``

Rails’in sihri sihirbazlık değil, öngörülebilir kurallardır. Örneğin `products` tablosu varsayılan olarak `Product` modeliyle eşleşir. Modelin `belongs_to :category` demesi, `products` tablosunda `category_id` alanı bulunacağını anlatır. Benzer biçimde REST rotaları, denetleyici eylemleri ve görünüm klasörleri de standart isimlerle birbirine bağlanır. Böylece geliştirici her bağlantıyı tek tek tarif etmek yerine yalnızca istisnaları tanımlar.

Bu yaklaşımın prototiplemedeki değerini kabaca şöyle düşünebiliriz:

$$T_{prototip} = T_{iş\ kuralı} + T_{özel\ deneyim} + T_{tekrar\ eden\ yapı}$$

Rails, tekrar eden yapı kısmını generator’lar, migration’lar ve varsayılanlar sayesinde küçültür. Sonuçta ekip zamanını gerçekten belirsiz olan iş kurallarına ayırır.

| Yaklaşım | Başlangıç hızı | Esneklik | Bakım maliyeti |
|---|---:|---:|---:|
| Her şeyi elle yapılandırmak | Düşük | Çok yüksek | Başta ve sonrada yüksek |
| Rails varsayımlarıyla ilerlemek | Yüksek | Yüksek | Düşük-orta |
| Admin panel gem’i kullanmak | Çok yüksek | Orta | Düşük |

Örnek olarak küçük bir stok takip uygulaması düşünelim. Önce şemayı kurarız. Migration, veritabanındaki değişikliklerin sürüm kontrollü tarifidir; yani “tabloda ne var?” sorusunun güvenilir cevabıdır.

```bash
bin/rails generate model Category name:string
bin/rails generate model Product name:string price:decimal stock:integer category:references
bin/rails db:migrate
```

Bu komutlar modelleri, migration dosyalarını ve ilişki için gerekli `category_id` alanını üretir. Ardından model katmanına temel doğrulamaları ekleyerek hatalı verinin arayüze kadar ulaşmasını engelleriz:

```ruby
# app/models/product.rb
class Product < ApplicationRecord
  belongs_to :category

  validates :name, presence: true
  validates :price, numericality: { greater_than_or_equal_to: 0 }
  validates :stock, numericality: { only_integer: true, greater_than_or_equal_to: 0 }
end
```

Prototipte elle CRUD ekranı yazmak yerine ActiveAdmin veya RailsAdmin gibi araçlar kullanılabilir. Bu araçlar modelleri ve alanları okuyarak listeleme, oluşturma, düzenleme ve silme sayfaları üretir. Örneğin ActiveAdmin kurulduktan sonra şu kayıt yeterlidir:

```ruby
# app/admin/products.rb
ActiveAdmin.register Product do
  permit_params :name, :price, :stock, :category_id

  filter :name
  filter :category
  filter :stock
end
```

Bu tanım, ürünler için filtrelenebilir bir tablo ve güvenli parametre listesi oluşturur. `permit_params` özellikle önemlidir: Tarayıcıdan gelen her alanın toplu biçimde veritabanına yazılmasını engeller.

| Şema öğesi | Rails yorumu | Arayüzdeki olası karşılığı |
|---|---|---|
| `string` | Kısa metin | Metin kutusu |
| `decimal` | Hassas sayısal değer | Fiyat alanı |
| `integer` | Tam sayı | Stok girişi |
| `references` | Model ilişkisi | Seçim listesi |
| `null: false` | Zorunlu veri | Zorunlu form alanı |

Elbette otomatik arayüz, nihai müşteri deneyimi değildir. Yetkilendirme, özel iş akışları, performans, erişilebilirlik ve marka tasarımı prototip büyüdükçe bilinçli biçimde ele alınmalıdır. Yine de doğru şema tasarımı, prototipin yalnızca veri saklamasını değil; filtrelenmesini, doğrulanmasını ve anlamlı ekranlarda yönetilmesini sağlar.

İyi başlangıç stratejisi nettir: önce varlıkları ve ilişkileri modelleyin, ardından otomatik CRUD ile akışı kullanıcıya gösterin. Kullanıcı “burada toplu fiyat güncellemesi gerekli” dediğinde, ancak o zaman özel ekranı yazın. Rails’in felsefesi tam olarak bunu destekler: önce çalışan konvansiyon, sonra gerekli özelleştirme.
