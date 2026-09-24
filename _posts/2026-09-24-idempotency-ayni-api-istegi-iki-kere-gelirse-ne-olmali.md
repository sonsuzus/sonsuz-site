---
layout: post
title: "Idempotency: Aynı API İsteği İki Kere Gelirse Ne Olmalı?"
math: true
categories: 
  - Bilgi
tags: 
  - idempotency
  - api
  - backend
  - dağıtık-sistemler
  - http
  - veritabanı
toc: true
image: /img/idempotency-ayni-api-27.png
---

![idempotency-ayni-api-27](/img/idempotency-ayni-api-27.svg)


Bir kullanıcı “Öde” düğmesine bastı, internet bağlantısı kısa süreliğine koptu ve istemci aynı isteği yeniden gönderdi. Müşteriden iki kez para mı çekmeliyiz? Elbette hayır! İşte **idempotency**, aynı işlemin birden fazla kez talep edilmesine rağmen sistemin nihai durumunun yalnızca bir kez çalıştırılmış gibi kalmasını sağlayan tasarım ilkesidir.
``
## İdempotency tam olarak nedir?

Matematikte bir işlem, tekrar uygulandığında sonucu değişmiyorsa idempotent kabul edilir:

$$f(f(x)) = f(x)$$

Örneğin bir sayının mutlak değerini almak idempotenttir:

$$\vert \,\vert x\vert \,\vert  = \vert x\vert $$

API dünyasında da benzer bir fikir kullanılır. “Siparişin durumunu `iptal edildi` yap” işlemi tekrarlandığında durum yine `iptal edildi` kalır. Buna karşılık “bakiyeden 100 TL düş” işlemi iki kez çalışırsa toplam 200 TL düşebilir; dolayısıyla kendiliğinden idempotent değildir.

| İşlem | Tekrarlandığında sonuç | Doğal olarak idempotent mi? |
|---|---|---|
| Kullanıcı bilgisini getir | Aynı veri okunur | Evet |
| Sipariş durumunu `kargolandı` yap | Durum değişmeden kalır | Genellikle evet |
| Yeni sipariş oluştur | İkinci sipariş oluşabilir | Hayır |
| Bakiyeden para düş | Bakiye tekrar azalır | Hayır |
| Kaynağı sil | Kaynak zaten silinmiştir | Genellikle evet |

Buradaki önemli ayrıntı, iki yanıtın mutlaka birebir aynı olması gerekmediğidir. İlk `DELETE` isteği `204`, ikincisi `404` dönebilir; ancak sistemin **nihai durumu** aynıdır: kaynak mevcut değildir.

## HTTP metotları bize ne söyler?

HTTP semantiğinde `GET`, `PUT` ve `DELETE` idempotent kabul edilirken `POST` genellikle edilmez. `PUT /users/42` isteği belirli bir kaynağı aynı temsille günceller. Buna karşılık `POST /orders`, her çağrıda yeni bir sipariş üretebilir.

Fakat metodun adı tek başına sihirli kalkan değildir. `GET /transfer-money` gibi yan etkili ve hatalı tasarlanmış bir uç nokta idempotent olmayabilir. Davranışı güvenceye alan şey uygulama mantığıdır.

## Idempotency key yaklaşımı

Ödeme ve sipariş API’lerinde istemci her mantıksal işlem için benzersiz bir anahtar üretir:

```http
POST /payments HTTP/1.1
Content-Type: application/json
Idempotency-Key: 8d03d91e-4f51-4b65-a31b

{"amount": 750, "currency": "TRY"}
```

Sunucu bu anahtarı veritabanında veya hızlı bir depoda saklar. Anahtar ilk kez görülüyorsa işlem yürütülür ve sonuç kaydedilir. Aynı anahtar tekrar gelirse ödeme yeniden yapılmaz; önceden üretilen yanıt döndürülür.

```python
def create_payment(request):
    key = request.headers["Idempotency-Key"]
    previous = idempotency_store.get(key)

    if previous:
        return previous.response

    with database.transaction():
        payment = charge_customer(request.body)
        response = {"payment_id": payment.id, "status": "completed"}
        idempotency_store.save(key, request.body_hash, response)

    return response
```

Bu örnek önce anahtarı kontrol eder, ardından ödeme ile kayıt işlemini bir transaction içinde yürütür. Gerçek sistemde yalnızca `get` ve `save` kullanmak yarış koşullarına açıktır. Aynı iki istek eşzamanlı gelirse ikisi de kaydı boş görebilir. Bu nedenle anahtar üzerinde **unique constraint**, atomik ekleme veya dağıtık kilit kullanılmalıdır.

## Aynı anahtar, farklı içerik problemi

Bir istemci aynı idempotency anahtarını yanlışlıkla farklı isteklerde kullanabilir. Sunucu bu durumda sessizce eski yanıtı vermemelidir. İstek gövdesinin hash değeri saklanabilir:

$$h = H(\text{method} + \text{path} + \text{body})$$

Kayıtlı hash ile yeni hash farklıysa `409 Conflict` ya da `422 Unprocessable Content` döndürmek güvenli bir yaklaşımdır.

## Kayıtlar sonsuza kadar tutulmalı mı?

Genellikle hayır. Her anahtara ödeme gibi iş ihtiyaçlarına uygun bir **TTL** atanır; örneğin 24 saat. Ancak anahtar silindikten sonra aynı isteğin yeniden işlenebileceği belgelenmelidir. Kritik işlemlerde ayrıca sipariş numarası veya işlem referansı üzerinde veritabanı benzersizlik kısıtı bulunmalıdır.

Kısacası sistem, tekrar gönderilen isteği “yeni bir emir” değil, “önceki emrin güvenli tekrarı” olarak tanımalıdır. Ağlar kusursuz değildir; zaman aşımı, yeniden deneme ve çift tıklama kaçınılmazdır. Sağlam API tasarımı bunları istisna değil, normal çalışma koşulu kabul eder.
