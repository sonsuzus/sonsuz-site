---
layout: post
title: "API Tasarımında HATEOAS: İstemciye Yol Gösteren Öz-Keşifli REST API’ler"
math: true
categories: 
  - Bilgi
tags: 
  - hateoas
  - rest
  - api
  - web servisleri
  - http
  - yazılım mimarisi
toc: true
image: /img/api-tasariminda-hateoas-96.png
---

Bir API istemcisinin bütün URL’leri önceden ezberlemesi gerekmeseydi nasıl olurdu? Kullanıcı bir siparişi görüntülediğinde API yalnızca sipariş verisini değil, o anda yapılabilecek “iptal et”, “öde” veya “kargoyu takip et” gibi eylemlerin bağlantılarını da döndürebilir. İşte HATEOAS, biraz ürkütücü açılımının arkasında tam olarak bu yönlendirici fikri taşır.
``
## HATEOAS nedir?

**HATEOAS**, *Hypermedia as the Engine of Application State* ifadesinin kısaltmasıdır. Türkçeye “Uygulama durumunun motoru olarak hipermedya” şeklinde çevrilebilir. REST mimarisinin önemli kısıtlarından biri olan bu yaklaşımda istemci, API içindeki sonraki adımları sunucunun yanıtlarına eklediği bağlantılar üzerinden keşfeder.

Bir web sitesini düşünelim: Ana sayfaya girdikten sonra ürünlere, sepete veya profil sayfasına bağlantılarla ulaşırsınız. Tarayıcı bütün adresleri önceden bilmez; gelen HTML belgesindeki bağlantıları takip eder. HATEOAS aynı fikri makineler arasında uygular.

Richardson Olgunluk Modeli’nde API’ler genel olarak dört seviyede ele alınır:

| Seviye | Temel özellik | Örnek |
|---|---|---|
| 0 | HTTP yalnızca taşıma aracı | Tek bir servis adresi |
| 1 | Kaynak odaklı adresler | `/orders/42` |
| 2 | HTTP metotları ve durum kodları | `GET`, `POST`, `404` |
| 3 | Hipermedya kontrolleri | Yanıtta sonraki işlem bağlantıları |

HATEOAS, bu modelin 3. seviyesidir. Ancak bu, HATEOAS kullanmayan her API’nin otomatik olarak kötü olduğu anlamına gelmez; yaklaşımın maliyeti ve yararı projeye göre değerlendirilmelidir.

## Durum makinesi olarak API

HATEOAS destekli bir API’yi yönlü bir grafik gibi düşünebiliriz:

$$G = (V, E)$$

Burada $V$ kaynakların veya uygulama durumlarının, $E$ ise bu durumlar arasındaki geçiş bağlantılarının kümesidir. Örneğin “ödenmemiş sipariş” düğümünden “ödenmiş sipariş” düğümüne geçiş, `pay` bağlantısıyla temsil edilebilir. Sipariş ödendikten sonra aynı bağlantının yanıttan kaldırılması, istemciye bu işlemin artık geçerli olmadığını anlatır.

Klasik ve HATEOAS tabanlı yaklaşımlar arasındaki fark şöyledir:

| Klasik istemci | HATEOAS istemcisi |
|---|---|
| URL şablonlarını bilir | Bağlantıları yanıttan keşfeder |
| İş kurallarını daha fazla taşır | Sunucunun sunduğu eylemleri izler |
| Adres değişikliklerinden kolay etkilenir | İlişki adlarına bağlı çalışabilir |
| Genellikle daha basittir | Daha esnek fakat daha karmaşıktır |

## Örnek bir yanıt

Bir sipariş kaynağı HAL benzeri bir gösterimle şöyle dönebilir:

```json
{
  "id": 42,
  "status": "awaiting_payment",
  "total": 799.90,
  "_links": {
    "self": { "href": "/orders/42" },
    "pay": { "href": "/orders/42/payment" },
    "cancel": { "href": "/orders/42/cancellation" },
    "customer": { "href": "/customers/7" }
  }
}
```

İstemci, ödeme adresini kendisi üretmek yerine `pay` ilişkisini takip eder. Sipariş kargolandığında sunucu `pay` ve `cancel` bağlantılarını kaldırıp `track` bağlantısını ekleyebilir. Böylece yanıt, yalnızca mevcut durumu değil, izin verilen geçişleri de açıklar.

Node.js ve Express ile bağlantıları duruma göre üretmek mümkündür:

```javascript
app.get("/orders/:id", async (req, res) => {
  const order = await findOrder(req.params.id);

  const links = {
    self: { href: `/orders/${order.id}` },
    customer: { href: `/customers/${order.customerId}` }
  };

  if (order.status === "awaiting_payment") {
    links.pay = { href: `/orders/${order.id}/payment` };
    links.cancel = { href: `/orders/${order.id}/cancellation` };
  }

  res.json({ ...order, _links: links });
});
```

Bu kod, bağlantıları siparişin durumuna göre ekler. Yine de bağlantının görünmemesi tek başına güvenlik önlemi değildir; sunucu her istekte yetkilendirme ve durum doğrulaması yapmalıdır.

## Tasarımda dikkat edilecekler

İlişki adları `pay`, `cancel` ve `next` gibi kararlı ve anlamlı olmalıdır. HAL, JSON:API, Siren veya Hydra gibi standartlar kullanılabilir; fakat ekip yalnızca bağlantı biçimini değil, istemcinin bu ilişkileri nasıl yorumlayacağını da belgelemelidir.

HATEOAS özellikle uzun ömürlü, iş akışı yoğun ve farklı istemciler tarafından tüketilen API’lerde güçlüdür. Basit CRUD servislerinde ise gereksiz karmaşıklık yaratabilir. Doğru yerde kullanıldığında API, adres listesinden ibaret olmaktan çıkar ve istemciye sürekli “Buradasın; şimdi şunları yapabilirsin” diyen etkileşimli bir rehbere dönüşür.

![api-tasariminda-hateoas-96](/img/api-tasariminda-hateoas-96.svg)

