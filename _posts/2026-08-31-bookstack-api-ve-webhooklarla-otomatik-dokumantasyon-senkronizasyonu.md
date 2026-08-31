---
layout: post
title: "BookStack API ve Webhooklarla Otomatik Dokümantasyon Senkronizasyonu"
math: true
categories: 
  - Proje
tags: 
  - bookstack
  - webhook
  - apı entegrasyonu
toc: true
---

Kurumsal dokümantasyon büyüdükçe aynı bilginin destek sistemi, intranet, arama motoru ve yedekleme servisleri arasında elle taşınması sürdürülemez hâle gelir. BookStack API ve webhooklarını birlikte kullanarak bir sayfa değiştiğinde diğer sistemleri otomatik güncelleyen, hızlı ve denetlenebilir bir entegrasyon hattı kurabiliriz.

``

## Webhook ve API neden birlikte kullanılmalı?

Webhook, BookStack içinde gerçekleşen bir olayı dış sisteme bildiren HTTP isteğidir. API ise kitap, bölüm ve sayfa gibi kaynakları programatik olarak okumamızı veya değiştirmemizi sağlar. Kısacası webhook **“bir şey değişti”**, API ise **“güncel veriyi getir”** der.

Sadece belirli aralıklarla API sorgulamak, gereksiz trafik oluşturur. Dakikada bir sorgulama yapılan sistemde günlük istek sayısı yaklaşık olarak:

$$R = 60 \times 24 = 1440$$

olur. Oysa günde yalnızca 40 değişiklik varsa webhook tabanlı model, temel senaryoda bunu yaklaşık 40 bildirime düşürür. API yine kullanılır; ancak yalnızca gerekli kaynağın güncel ve tam durumunu almak için çağrılır.

| Yaklaşım | Avantaj | Dezavantaj | Uygun kullanım |
|---|---|---|---|
| Periyodik API sorgusu | Kurulumu basittir | Gecikme ve gereksiz trafik üretir | Küçük sistemler |
| Yalnızca webhook verisi | Hızlı bildirim sağlar | Olay yükü eksik olabilir | Basit bildirimler |
| Webhook + API | Güncel ve güvenilir veri sunar | Biraz daha fazla mimari ister | Kurumsal senkronizasyon |

## Önerilen entegrasyon akışı

BookStack yönetim panelinden ilgili sayfa, kitap veya bölüm olayları için bir webhook tanımlanır. Hedef olarak doğrudan ana uygulamayı göstermek yerine küçük bir entegrasyon servisi kullanmak daha güvenlidir.

Akış şu şekilde ilerler:

1. Kullanıcı BookStack sayfasını günceller.
2. BookStack webhook alıcısına bir `POST` isteği yollar.
3. Alıcı isteği doğrular ve olayı kuyruğa ekler.
4. İşçi süreç, BookStack API üzerinden güncel kaynağı getirir.
5. Veri hedef sisteme uygun biçime dönüştürülür.
6. Arama indeksi, yardım masası veya başka bir platform güncellenir.

Kuyruk kullanımı önemlidir; çünkü webhook isteğini işlerken hedef sistem yavaşlarsa BookStack tarafında zaman aşımı yaşanabilir. Alıcının hızlıca `2xx` yanıtı vermesi, ağır işi arka planda yürütmesi gerekir.

## Node.js ile webhook alıcısı

Aşağıdaki Express örneği olay yükünü kabul eder, temel alanları denetler ve senkronizasyon kuyruğuna gönderir:

```javascript
import express from "express";

const app = express();
app.use(express.json({ limit: "1mb" }));

app.post("/webhooks/bookstack", async (req, res) => {
  const event = req.body.event;
  const item = req.body.related_item;

  if (!event || !item?.id) {
    return res.status(400).json({ error: "Geçersiz webhook yükü" });
  }

  await syncQueue.add("bookstack-sync", {
    event,
    resourceId: item.id,
    resourceType: item.type
  });

  res.status(202).json({ accepted: true });
});

app.listen(3000);
```

Alan adları BookStack sürümüne ve olay türüne göre farklılaşabileceğinden gerçek webhook örnekleri kaydedilmeli, şema buna göre uyarlanmalıdır.

## API üzerinden güncel sayfayı alma

BookStack API kimlik doğrulamasında token kimliği ve token gizlisi kullanılır. Bu bilgiler kod içine yazılmamalı, ortam değişkenlerinde veya bir gizli bilgi kasasında saklanmalıdır.

```javascript
async function getPage(pageId) {
  const response = await fetch(
    `${process.env.BOOKSTACK_URL}/api/pages/${pageId}`,
    {
      headers: {
        Authorization: `Token ${process.env.BS_TOKEN_ID}:${process.env.BS_TOKEN_SECRET}`
      }
    }
  );

  if (!response.ok) {
    throw new Error(`BookStack API hatası: ${response.status}`);
  }

  return response.json();
}
```

## Güvenilirlik ve güvenlik

Webhook uç noktası HTTPS kullanmalı; mümkünse ters proxy, IP kısıtlaması veya ağ geçidi doğrulamasıyla korunmalıdır. BookStack sürümünün sunduğu imza mekanizması varsa ham istek gövdesi üzerinden doğrulanmalıdır. Ayrıca aynı olay birden fazla kez gelebileceği için işlemler idempotent tasarlanmalıdır.

Örneğin `kaynak_türü + kaynak_id + güncellenme_zamanı` birleşimi benzersiz anahtar yapılabilir. Başarısız işlemler üstel gecikmeyle yeniden denenebilir:

$$t_n = \min(t_{max}, t_0 \times 2^n)$$

Böylece kısa süreli ağ sorunları veri kaybına dönüşmez. Sonuçta webhooklar hızı, API ise doğruluğu sağlar; kuyruk, kayıt tutma ve idempotent işlemler de entegrasyonu kurumsal ölçekte dayanıklı hâle getirir.
