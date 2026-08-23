---
layout: post
title: "GraphQL ile Veri Sorgulama: Yalnızca İhtiyacın Kadar Veri"
math: true
categories: 
  - Bilgi
tags: 
  - graphql
  - apı
  - javascript
toc: true
---

Modern uygulamalarda veriyi almak, çoğu zaman veriyi göstermekten daha karmaşık hâle gelir. Geleneksel REST API'lerde bir ekran için birden fazla uç noktaya istek atmak veya gereğinden büyük JSON yanıtları indirmek sık rastlanan bir durumdur. GraphQL, istemcinin ihtiyaç duyduğu alanları açıkça tarif ettiği bir sorgu dili ve API çalışma zamanı sunar. Böylece mobil uygulama, web arayüzü ve yönetim paneli aynı veri kaynağından farklı şekillerde beslenebilir.
``
## REST'teki iki klasik problem

REST yaklaşımında `/users/42` çağrısı kullanıcının çok sayıda alanını döndürebilir. Oysa profil kartında yalnızca ad ve avatar gerekli olabilir. Bu **over-fetching** yani fazla veri çekme problemidir. Tersine, kullanıcıyı, yazılarını ve her yazının yorum sayısını göstermek için ayrı ayrı uç noktalara gitmek gerekebilir. Bu da **under-fetching** olarak bilinir.

GraphQL'de istemci, sunucuya sadece sonuç biçimini bildirir. Sunucu ise şemada tanımlanan kurallara göre bu biçimi üretir. Veri maliyetini kabaca şöyle düşünebiliriz:

$$Maliyet \approx İstek\ Sayısı \times Gecikme + Aktarılan\ Veri\ Boyutu$$

GraphQL her zaman bu maliyeti otomatik olarak en aza indirmez; ancak istemciye veri boyutunu ve ilişkisel sorguları hassas biçimde yönetme olanağı verir.

| Özellik | REST | GraphQL |
|---|---|---|
| Veri şekli | Sunucu belirler | İstemci alan seçer |
| Uç nokta | Genellikle çok sayıda | Çoğunlukla tek uç nokta |
| Dokümantasyon | Harici olabilir | Şema üzerinden keşfedilebilir |
| İlişkili veri | Birden çok çağrı gerekebilir | Tek sorguda istenebilir |

## Şema: API'nin sözleşmesi

GraphQL sisteminin kalbinde **schema** bulunur. Şema; hangi nesnelerin, alanların ve işlemlerin kullanılabileceğini tanımlar. `User` türünün `id`, `name` ve `posts` alanlarına sahip olduğunu düşünelim. `Query` türü ise dışarıdan erişilebilen başlangıç noktalarını sunar.

```graphql
type Post {
  id: ID!
  title: String!
  likes: Int!
}

type User {
  id: ID!
  name: String!
  avatarUrl: String
  posts: [Post!]!
}

type Query {
  user(id: ID!): User
}
```

Buradaki `!`, alanın boş olamayacağını belirtir. `[Post!]!` ifadesi hem listenin boş olmamasını hem de listedeki öğelerin `null` olmamasını garanti eder. Bu tip sistemi, istemcinin daha geliştirme aşamasında hatalı alan taleplerini yakalamasına yardımcı olur.

## İstemci odaklı sorgu yazmak

Profil kartı için bütün kullanıcı kaydını istemek yerine, görünümün kullandığı alanları seçebiliriz:

```graphql
query GetProfile($userId: ID!) {
  user(id: $userId) {
    name
    avatarUrl
    posts {
      title
      likes
    }
  }
}
```

Değişkenler ayrı gönderilir:

```json
{ "userId": "42" }
```

Bu sorgu, SQL yazmak değildir. İstemci verinin **nasıl** bulunacağını değil, **hangi biçimde** dönmesini istediğini ifade eder. Arka planda alanları çözme görevini resolver'lar üstlenir. Örneğin `user` resolver'ı kullanıcıyı veritabanından bulur; `posts` resolver'ı ise o kullanıcının yazılarını getirir.

## Dikkat: Tek sorgu, sınırsız maliyet demek değildir

GraphQL'in esnekliği kontrol edilmezse pahalı iç içe sorgulara dönüşebilir. Özellikle liste içindeki her öğe için yeniden veritabanı sorgusu çalıştırılması **N+1 problemi** yaratır. Bunu önlemek için DataLoader benzeri toplu yükleme araçları, sorgu derinliği limitleri ve karmaşıklık analizi kullanılır.

| İhtiyaç | Öneri |
|---|---|
| Tekil profil görünümü | Alanları açıkça seçen query |
| Kayıt oluşturma | `mutation` |
| Canlı bildirim | `subscription` |
| Büyük liste | Sayfalama ve `first/after` parametreleri |

Sonuç olarak GraphQL, “tek endpoint her derdi çözer” sloganından çok daha fazlasıdır: güçlü bir API sözleşmesidir. İyi tasarlanmış bir şema, sınırlandırılmış sorgu maliyetleri ve sayfalama kurallarıyla birleştiğinde, istemci ekiplerinin daha az gereksiz veri taşıyarak daha hızlı ve esnek arayüzler geliştirmesini sağlar.
