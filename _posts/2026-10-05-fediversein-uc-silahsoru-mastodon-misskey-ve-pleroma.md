---
layout: post
title: "Fediverse’in Üç Silahşörü: Mastodon, Misskey ve Pleroma"
math: true
categories: 
  - Bilgi
tags: 
  - mastodon
  - misskey
  - pleroma
  - fediverse
  - activitypub
  - mikroblog
  - açık-kaynak
toc: true
image: /img/fediversein-uc-silahsoru-93.png
---

![fediversein-uc-silahsoru-93](/img/fediversein-uc-silahsoru-93.svg)


Twitter benzeri bir mikroblog sistemi kurmak istiyor, fakat kullanıcıların ve verilerin tek bir şirketin sunucusunda hapsolmasını istemiyorsanız Fediverse dünyasına hoş geldiniz. Mastodon, Misskey ve Pleroma; farklı arayüzlere, özelliklere ve teknik önceliklere sahip olsalar da aynı federasyon protokolü sayesinde birbirleriyle iletişim kurabilir. Kısacası biri kahve dükkânı, biri oyun salonu, diğeri hafif bir kamp çadırı gibidir; buna rağmen üçündeki kullanıcılar aynı meydanda sohbet edebilir.
``

## Önce temel kavram: Federasyon

Geleneksel sosyal ağlar merkezîdir. Bütün hesaplar, gönderiler ve kurallar tek işletmenin kontrolündeki altyapıda bulunur. Federasyon modelindeyse bağımsız sunucular, yani **instance** veya **örnekler**, ortak bir protokol üzerinden haberleşir.

Bu sistemlerin temelinde çoğunlukla W3C standardı olan **ActivityPub** bulunur. Her kullanıcı bir aktör, gönderiler ise etkinlik olarak temsil edilir. Örneğin bir paylaşım oluşturmak kabaca `Create`, bir kullanıcıyı takip etmek `Follow`, beğeni göndermek ise `Like` etkinliğidir.

Bir ağın toplam erişimini basitçe şöyle düşünebiliriz:

$$R = \sum_{i=1}^{n} U_i - D$$

Burada $U_i$, federasyona katılan her sunucudaki erişilebilir kullanıcı sayısını; $D$ ise engellemeler, kapalı kayıtlar ve yinelenen bağlantılar nedeniyle oluşan kaybı temsil eder. Yani daha fazla sunucu teorik olarak daha geniş erişim sağlar, ancak moderasyon kararları gerçek ağı şekillendirir.

## Üç platformun karakteri

| Özellik | Mastodon | Misskey | Pleroma |
|---|---|---|---|
| Ana yaklaşım | Dengeli ve yaygın | Özellik zengini ve eğlenceli | Hafif ve esnek |
| Sunucu ihtiyacı | Orta-yüksek | Orta-yüksek | Düşük-orta |
| Arayüz | Sade, tanıdık | Renkli, özelleştirilebilir | İstemciye göre değişken |
| Öne çıkan taraf | Büyük topluluk | Tepkiler, widget’lar, drive | Kaynak verimliliği |
| Uygun kullanıcı | Genel topluluklar | Etkileşim ve kişiselleştirme sevenler | Küçük sunucu yöneticileri |

**Mastodon**, Fediverse’in en bilinen yüzüdür. Güçlü moderasyon araçları, gelişmiş istemci ekosistemi ve geniş dokümantasyonu sayesinde yeni başlayanlar için güvenli bir seçimdir. Buna karşılık daha fazla bellek ve işlem gücü isteyebilir.

**Misskey**, gönderilere farklı emojilerle tepki verme, gelişmiş profil düzenleme, dosya alanı ve widget gibi özelliklerle daha oyuncaklıdır. Kullanıcı deneyimini kişiselleştirmek isteyen topluluklar için oldukça çekicidir.

**Pleroma** ise daha az kaynakla çalışmaya odaklanır. Küçük bir VPS üzerinde kişisel veya dar kapsamlı bir topluluk kurmak isteyenler için mantıklıdır. Arayüzü ayrı ön yüzlerle değiştirilebildiğinden teknik kullanıcıların hoşuna gider.

## ActivityPub mesajı nasıl görünür?

Aşağıdaki sadeleştirilmiş JSON, başka bir sunucuya gönderilebilecek paylaşım etkinliğini gösterir:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Create",
  "actor": "https://ornek.social/users/ada",
  "object": {
    "type": "Note",
    "content": "Federasyon çalışıyor!",
    "to": ["https://www.w3.org/ns/activitystreams#Public"]
  }
}
```

Burada `actor` paylaşımı yapan hesabı, `object` gönderiyi, `to` ise hedef kitleyi belirtir. Gerçek uygulamada nesne kimlikleri, zaman damgaları ve HTTP imzaları da kullanılır. İmzalar, başka bir sunucunun “Bu mesaj gerçekten Ada’dan mı geldi?” sorusunu doğrulamasına yardımcı olur.

## Hangisini seçmelisiniz?

Büyük ve genel amaçlı bir topluluk hedefliyorsanız **Mastodon**, zengin etkileşim seçenekleri istiyorsanız **Misskey**, sınırlı donanımla esnek bir kurulum arıyorsanız **Pleroma** iyi bir başlangıçtır. Yine de yazılım seçimi tek başına yeterli değildir. Yedekleme, medya depolama, spam önleme, alan adı yönetimi ve moderasyon politikası en az teknik kurulum kadar önemlidir.

Fediverse’in asıl gücü, herkesin aynı yazılımı kullanması değil, farklı yazılımların ortak bir dil konuşabilmesidir. Böylece kullanıcılar platforma değil, topluluklarına bağlanır; sunucu yöneticileri de dijital mahallelerinin kurallarını kendileri belirler.
