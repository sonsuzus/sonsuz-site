---
layout: post
title: "Flarum’da Deneysel Veri Sorgulama: JSON:API’den GraphQL Katmanına"
math: true
categories: 
  - Program
tags: 
  - flarum
  - graphql
  - apı mimarisi
toc: true
---

Flarum, standart kurulumunda düzenli ve öngörülebilir bir JSON:API yaklaşımı sunar. Ancak bir tartışmanın yazarını, etiketlerini, son yanıtlarını ve özel uzantı alanlarını tek ekranda göstermek istediğimizde istemci tarafı küçük bir veri toplama dedektifine dönüşebilir. Deneysel bir sorgulama katmanı ekleyerek istemcinin ihtiyaç duyduğu alanları açıkça seçmesini, gereksiz veriyi azaltmasını ve Flarum uzantıları arasında daha esnek ilişkiler kurmasını sağlayabiliriz.
``

## Geleneksel yaklaşım neden zorlanır?

REST veya Flarum’un kullandığı JSON:API kötü değildir; aksine önbellekleme, kaynak keşfi ve standartlaştırılmış ilişkiler konusunda oldukça başarılıdır. Sorun, ekranların veri gereksinimleri karmaşıklaştığında ortaya çıkar. Bir istemci ya çok sayıda uç noktaya gider ya da her ihtimali karşılayan büyük yanıtlar indirir.

| Yaklaşım | Güçlü tarafı | Muhtemel sorun |
|---|---|---|
| JSON:API | Standart kaynak ve ilişki modeli | Karmaşık ekranlarda fazla veri |
| GraphQL | Alan bazlı esnek sorgulama | Karmaşıklık ve yetkilendirme maliyeti |
| Özel sorgu DSL’i | Flarum’a özel kontrol | Yeni bir söz dizimi öğrenme gereksinimi |
| BFF katmanı | İstemciye özel optimize edilmiş yanıt | Bakım yükü ve servis çoğalması |

Aktarılan toplam veriyi basitçe $D = \sum_{i=1}^{n} r_i$ biçiminde düşünebiliriz. Burada $r_i$, her isteğin yanıt boyutudur. Alan seçebilen bir API’de hedef, gerekli alan kümesi $F_g$ ile döndürülen alan kümesi $F_r$ arasındaki farkı, yani $\vert F_r - F_g\vert $ değerini küçültmektir.

## Flarum’un üzerine GraphQL cephesi kurmak

En güvenli deneysel tasarım, mevcut modelleri ve yetkilendirme kurallarını çöpe atmak yerine bunların üzerine bir sorgu cephesi yerleştirmektir. İstek önce GraphQL şemasına gelir; resolver, Flarum servislerini çağırır; sonuç yeniden istemciye döner. Böylece GraphQL doğrudan veritabanına açılan sınırsız bir tünel olmaz.

Örnek sorgu şöyle görünebilir:

```graphql
query DiscussionCard($id: ID!) {
  discussion(id: $id) {
    title
    commentCount
    user { username }
    tags { name slug }
    posts(limit: 3) {
      number
      contentHtml
    }
  }
}
```

Bu sorgu yalnızca kartın ihtiyaç duyduğu alanları ister. Resolver tarafında ise erişim kontrolü mutlaka Flarum aktörü üzerinden yürütülmelidir:

```php
final class DiscussionResolver
{
    public function __invoke($root, array $args, Context $context)
    {
        $actor = $context->actor;
        $discussion = Discussion::findOrFail($args['id']);

        // Flarum'un mevcut izin politikasını yeniden kullanır.
        $actor->assertCan('view', $discussion);

        return $discussion;
    }
}
```

Buradaki kritik fikir, resolver’ın yalnızca veri bulmaması; görünürlük, askıya alınmış kullanıcılar ve özel tartışmalar gibi kuralları da korumasıdır. Aksi durumda esnek API, güvenlik duvarında açılmış şık bir pencereye dönüşür.

## N+1 canavarını evcilleştirmek

Bir sorgu on tartışma ve her tartışmanın yazarını istediğinde saf resolver tasarımı $1 + N$ veritabanı sorgusu üretebilir. DataLoader benzeri toplu yükleme mekanizması yazar kimliklerini biriktirerek işlemi yaklaşık iki sorguya indirir:

$$Q_{saf}=1+N, \qquad Q_{toplu}\approx 2$$

Ayrıca sorgu derinliği, alan maliyeti ve sonuç limiti belirlenmelidir. Örneğin `posts(limit: 50000)` masum görünmez; sunucuya gönderilmiş performans temalı bir korku filmidir. Her alan için maliyet tanımlanıp toplam maliyeti belirli bir eşiği aşan sorgular reddedilebilir.

## Uzantılarla büyüyen şema

Flarum uzantıları merkezi şemaya yeni türler ve alanlar ekleyebilir. Bir rozet uzantısı `User.badges`, anket uzantısı ise `Discussion.poll` alanını kaydedebilir. Bunun için uzantılara kontrollü bir `SchemaRegistry` sunmak, çekirdek dosyalarını değiştirmekten daha sürdürülebilirdir.

Deneysel entegrasyon önce salt okunur sorgularla başlamalıdır. İzleme kayıtları, sorgu süresi, SQL sayısı ve yanıt boyutu ölçülmeli; mutation işlemleri daha sonra eklenmelidir. Böylece mevcut JSON:API korunurken GraphQL veya özel DSL, belirli istemciler için isteğe bağlı bir hızlandırıcı olur. Amaç eski yolu yıkmak değil, Flarum’un veri katmanına güvenli ve ölçülebilir yeni bir kapı açmaktır.
