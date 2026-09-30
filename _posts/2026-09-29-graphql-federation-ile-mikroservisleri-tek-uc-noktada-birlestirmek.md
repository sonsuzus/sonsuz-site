---
layout: post
title: "GraphQL Federation ile Mikroservisleri Tek Uç Noktada Birleştirmek"
math: true
categories: 
  - Bilgi
tags: 
  - graphql
  - federation
  - mikroservis
  - api
  - apollo-federation
  - dağıtık-sistemler
toc: true
image: /img/graphql-federation-ile-53.png
---

Mikroservis mimarisinde kullanıcılar, ürünler ve siparişler farklı ekiplerin yönettiği servislerde yaşayabilir. Ancak mobil uygulamanın bu servislerin adreslerini, sürümlerini ve aralarındaki ilişkileri bilmesi gerekmemelidir. GraphQL Federation, bağımsız GraphQL şemalarını bir **supergraph** altında birleştirerek istemciye tek ve tutarlı bir uç nokta sunar. Böylece arka tarafta dağıtık, ön tarafta ise şaşırtıcı derecede bütünleşik bir veri modeli elde edilir.


![graphql-federation-ile-53](/img/graphql-federation-ile-53.svg)

``

## Federation neden gerekli?

Klasik bir API Gateway çoğunlukla istekleri URL kurallarına göre ilgili servise yönlendirir. Federation router ise sorgunun anlamını bilir. GraphQL sorgusunu alanlara ayırır, hangi alanın hangi alt grafikten geleceğini belirler ve servis çağrılarını bir yürütme planına dönüştürür.

Toplam yanıt süresini kabaca şöyle düşünebiliriz:

$$
T_{toplam} = T_{planlama} + \sum T_{ardışık} + \max(T_{paralel})
$$

Bağımsız sorgular paralel çalıştırılabildiği için her servis süresi doğrudan birbirine eklenmez. Fakat servisler arası bağımlılıklar arttıkça ardışık çağrıların ve ağ maliyetinin etkisi büyür.

| Yaklaşım | Şema yönetimi | İstemci deneyimi | Servis bağımsızlığı |
|---|---|---|---|
| Ayrı GraphQL API'leri | Her serviste ayrı | Birden fazla uç nokta | Yüksek |
| Tek parça GraphQL | Merkezi şema | Tek uç nokta | Düşük |
| GraphQL Federation | Dağıtık alt şemalar | Tek uç nokta | Yüksek |

## Temel yapı taşları

Her mikroservis kendi **subgraph** şemasını ve resolver'larını yönetir. Bu şemalar birleştirilerek supergraph şeması üretilir. Router veya gateway gelen sorguyu analiz eder, uygun servislere dağıtır ve sonuçları tek JSON yanıtında birleştirir.

Federation'ın sihirli kelimesi **entity** kavramıdır. Bir servis tarafından tanımlanan varlık, başka bir servis tarafından ortak anahtarı üzerinden genişletilebilir. Örneğin kullanıcı servisi `User` nesnesinin kimliğini ve adını yönetirken sipariş servisi aynı kullanıcıya `orders` alanını ekleyebilir.

```graphql
# Kullanıcı subgraph'ı
type User @key(fields: "id") {
  id: ID!
  name: String!
}

type Query {
  user(id: ID!): User
}
```

Buradaki `@key`, `User` varlığının servisler arasında `id` alanıyla tanınacağını belirtir. Sipariş subgraph'ı ise bu varlığa kendi sorumluluğundaki alanı kazandırır:

```graphql
type User @key(fields: "id") {
  id: ID!
  orders: [Order!]!
}

type Order @key(fields: "id") {
  id: ID!
  total: Float!
}
```

İkinci servis kullanıcının adını saklamak zorunda değildir; yalnızca aldığı kullanıcı referansından siparişleri çözümler. Böylece veri sahipliği belirsizleşmez.

## İstemci ne görür?

İstemci servis sınırlarıyla uğraşmadan ilişkisel görünen tek bir sorgu gönderir:

```graphql
query GetUserProfile {
  user(id: "42") {
    name
    orders {
      id
      total
    }
  }
}
```

Router önce kullanıcı servisine giderek `name` ve entity anahtarını alır. Ardından bu anahtarı sipariş servisine göndererek `orders` alanını çözer. İstemci açısından ise yalnızca bir istek ve bir yanıt vardır.

## Tasarımda dikkat edilmesi gerekenler

Federation servis bağımsızlığını destekler ama kötü sınırları otomatik olarak düzeltmez. Bir sorgu onlarca servisi zincirleme çağırıyorsa sistem, dağıtık bir N+1 problemine dönüşebilir. DataLoader, önbellekleme, sorgu derinliği sınırları ve gözlemlenebilirlik bu nedenle önemlidir.

| Risk | Belirti | Önlem |
|---|---|---|
| N+1 sorguları | Artan veritabanı çağrısı | DataLoader ile toplama |
| Döngüsel bağımlılık | Karmaşık sorgu planı | Net domain sahipliği |
| Şema uyumsuzluğu | Yayınlama hatası | Composition kontrolleri |
| Yavaş alt servis | Tüm yanıtın gecikmesi | Timeout ve circuit breaker |

Şema değişiklikleri de CI/CD aşamasında uyumluluk testlerinden geçirilmelidir. Bir alanı kaldırmak, o alan başka bir ekip tarafından kullanılmasa bile aktif istemcileri bozabilir.

GraphQL Federation'ın asıl gücü yalnızca API'leri birleştirmesi değil, ekiplerin alan sahipliğini korurken ortak bir ürün şeması oluşturabilmesidir. Doğru domain sınırları, iyi izleme araçları ve kontrollü şema evrimiyle supergraph, mikroservis karmaşasını istemciden saklayan güçlü bir sözleşmeye dönüşür.
