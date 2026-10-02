---
layout: post
title: "GraphQL Subscription ile WebSocket Üzerinden Gerçek Zamanlı Veri Akışı"
math: true
categories: 
  - Bilgi
tags: 
  - graphql
  - websocket
  - subscription
  - gerçek-zamanlı
  - javascript
  - apollo
toc: true
image: /img/graphql-subscription-ile-19.png
---

Bir mesaj uygulamasında yeni iletileri görmek için sayfayı sürekli yenilemek zorunda kaldığınızı düşünün. Pek modern sayılmaz, değil mi? GraphQL Subscription, sunucuda gerçekleşen olayları WebSocket bağlantısı üzerinden istemciye anında ileterek bu sorunu çözer. Böylece sohbet mesajları, bildirimler, canlı skorlar ve sipariş durumları gecikmeden arayüze yansıtılabilir.

![graphql-subscription-ile-19](/img/graphql-subscription-ile-19.svg)

``

## İstek-cevap modelinden olay akışına

Klasik GraphQL sorguları çoğunlukla HTTP üzerinden çalışır. İstemci bir `query` veya `mutation` gönderir, sunucu işlemi tamamlar ve tek bir yanıt döndürür. Subscription ise aynı GraphQL şemasını kullansa da farklı bir yaşam döngüsüne sahiptir: İstemci bağlantıyı açık tutar ve ilgilendiği olay meydana geldikçe birden fazla sonuç alır.

| Özellik | Query / Mutation | Subscription |
|---|---|---|
| İletişim modeli | İstek-cevap | Yayın-abonelik |
| Tipik taşıma | HTTP | WebSocket |
| Yanıt sayısı | Genellikle bir | Bağlantı boyunca çok sayıda |
| Kullanım alanı | Veri okuma ve değiştirme | Canlı güncellemeler |
| Bağlantı ömrü | Kısa | Uzun |

Sürekli HTTP sorgusu gönderen polling yaklaşımında saniyede $r$ istek ve $n$ istemci varsa yaklaşık istek yükü

$$L = n \times r$$

olur. Subscription modelinde ise istemciler kalıcı bağlantılar kurar; veri yalnızca olay oluştuğunda taşınır. Olay sayısı düşükken gereksiz ağ trafiği ciddi biçimde azalır. Elbette açık bağlantıları yönetmenin de bellek, güvenlik ve ölçekleme maliyeti vardır.

## WebSocket bağlantısında neler olur?

WebSocket, HTTP ile başlayan bir el sıkışmanın ardından çift yönlü ve kalıcı bir iletişim kanalı oluşturur. GraphQL dünyasında mesajların biçimini belirlemek için güncel olarak `graphql-transport-ws` protokolü tercih edilir. Genel akış şöyledir:

1. İstemci WebSocket bağlantısını açar.
2. Kimlik doğrulama bilgilerini bağlantı parametreleriyle yollar.
3. Sunucu bağlantıyı onaylar.
4. İstemci bir subscription operasyonu başlatır.
5. Sunucu ilgili olayları bağlantı üzerinden iter.
6. İstemci aboneliği veya bağlantıyı kapatır.

Örnek bir şema, yeni mesaj olayını güçlü tiplerle tanımlayabilir:

```graphql
type Message {
  id: ID!
  roomId: ID!
  text: String!
  createdAt: String!
}

type Subscription {
  messageAdded(roomId: ID!): Message!
}
```

Buradaki `roomId`, her istemcinin yalnızca ilgilendiği odanın mesajlarını almasını sağlar. Ancak filtreleme tek başına yetkilendirme değildir; kullanıcının odaya erişimi resolver içinde ayrıca doğrulanmalıdır.

## Sunucuda yayınlama ve dinleme

Node.js tabanlı basitleştirilmiş bir resolver şu şekilde yazılabilir:

```javascript
const resolvers = {
  Subscription: {
    messageAdded: {
      subscribe: (_, { roomId }, context) => {
        if (!context.user) throw new Error("Yetkisiz bağlantı");
        return pubsub.asyncIterableIterator(`ROOM_${roomId}`);
      }
    }
  }
};

// Yeni mesaj kaydedildikten sonra olayı abonelere yayınlar.
await pubsub.publish(`ROOM_${roomId}`, {
  messageAdded: savedMessage
});
```

`subscribe` fonksiyonu bir `AsyncIterable` üretir. Her yayın, asenkron akışın yeni elemanı gibi davranır. Bellek içi PubSub geliştirme ortamında yeterlidir; birden fazla sunucu örneği çalıştığında Redis, Kafka veya NATS gibi ortak bir mesaj altyapısı kullanılmalıdır.

İstemci tarafındaki operasyon ise oldukça tanıdıktır:

```graphql
subscription WatchRoom($roomId: ID!) {
  messageAdded(roomId: $roomId) {
    id
    text
    createdAt
  }
}
```

Apollo Client gibi araçlar HTTP sorgularını normal bağlantıya, subscription operasyonlarını ise WebSocket bağlantısına yönlendirebilir. Gelen her sonuç önbelleğe eklenerek arayüz yeniden çizilir.

## Üretimde dikkat edilmesi gerekenler

Bağlantı kurulurken JWT doğrulamak yeterli değildir; uzun süre açık kalan bağlantılarda token süresi dolabilir. Yeniden bağlanma, üstel geri çekilme, heartbeat mesajları ve abonelik temizliği planlanmalıdır. Ayrıca kullanıcı başına bağlantı sınırı ve olay hızlandırma politikaları uygulanmalıdır.

Subscription her veri için sihirli değnek değildir. Seyrek değişen ekranlarda normal sorgu veya kontrollü polling daha basit olabilir. Fakat olayların düşük gecikmeyle ulaştırılması gerekiyorsa GraphQL Subscription, tip güvenli GraphQL deneyimini WebSocket’in çift yönlü gücüyle birleştiren son derece etkili bir çözümdür.
