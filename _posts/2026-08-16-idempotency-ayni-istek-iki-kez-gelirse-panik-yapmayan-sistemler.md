---
layout: post
title: "Idempotency: Aynı İstek İki Kez Gelirse Panik Yapmayan Sistemler"
math: true
categories: 
  - Bilgi
tags: 
  - idempotency
  - api tasarımı
  - dağıtık sistemler
image: /img/idempotency-ayni-istek-23.png
---

Bir kullanıcı “Öde” düğmesine bastığında internet bağlantısı kopabilir, tarayıcı isteği yeniden gönderebilir veya mobil uygulama zaman aşımı nedeniyle otomatik tekrar deneyebilir. Sisteminiz ikinci isteği yeni bir ödeme gibi algılarsa, kullanıcı iki kez ücretlendirilir. **Idempotency (yan etkisizlik)**, aynı işlemin birden fazla kez uygulanmasının sistemde ilk uygulamadan farklı bir sonuç üretmemesini hedefleyen tasarım ilkesidir. Kısacası: tekrarlar kaçınılmazdır; hasar olmak zorunda değildir.

``

Matematikte bir fonksiyon, kendisine tekrar uygulandığında sonucu değişmiyorsa idempotenttir:

$$f(f(x)) = f(x)$$

Örneğin bir kullanıcının durumunu `aktif` yapmak idempotenttir. Kullanıcı zaten aktifse işlemi yeniden çalıştırmak durumu değiştirmez. Buna karşılık bakiyeye 100 TL eklemek idempotent değildir; her çağrı bakiyeyi tekrar artırır. API tasarımında kritik soru şudur: “Bu isteği ağ sorunları nedeniyle üç kez işlersem, iş sonucu güvenli kalır mı?”

HTTP metotları bu fikri anlatmak için faydalı bir başlangıçtır. Ancak metodun teorik özelliği ile uygulamanın gerçek davranışı aynı şey değildir. Örneğin `DELETE /users/42` isteği ikinci kez çağrıldığında kaynak zaten silinmiş olabilir; yine de hedeflenen nihai durum “kullanıcı yok” olduğu için idempotent kabul edilir.

| İşlem | Tipik idempotent mi? | Neden? |
|---|---:|---|
| `GET /products/7` | Evet | Yalnızca veri okur, durum değiştirmez. |
| `PUT /users/7/status` | Evet | Durumu belirli bir değere ayarlar. |
| `DELETE /cart/7` | Evet | Nihai hedef sepetin olmamasıdır. |
| `POST /payments` | Genellikle hayır | Her çağrı yeni bir ödeme oluşturabilir. |
| `balance += 100` | Hayır | Tekrar eden her çağrı yeni yan etki üretir. |

![idempotency-ayni-istek-23](/img/idempotency-ayni-istek-23.svg)


Özellikle ödeme, sipariş, e-posta gönderimi ve stok düşme gibi `POST` tabanlı işlemlerde **idempotency key** kullanılır. İstemci her mantıksal işlem için benzersiz bir anahtar üretir ve yeniden denemelerde aynı anahtarı yollar. Sunucu bu anahtarı daha önce görmüşse işlemi yeniden icra etmek yerine sakladığı sonucu döndürür.

```http
POST /payments
Idempotency-Key: 8eab4b8d-7b28-4ba9-a9f0-2d129ac0d9f2
Content-Type: application/json

{
  "orderId": "ORD-1042",
  "amount": 499.90,
  "currency": "TRY"
}
```

Sunucu tarafında anahtarın yalnızca “görüldü” olarak işaretlenmesi yeterli değildir. İstek gövdesi, işlem durumu ve üretilen yanıt da kaydedilmelidir. Aynı anahtar farklı bir gövdeyle gelirse bu, istemci hatası veya kötüye kullanım olabilir; işlem sessizce tekrar edilmemelidir.

```python
# Aynı anahtarın ikinci kez yeni ödeme üretmesini engeller.
def create_payment(key, payload):
    cached = idempotency_store.get(key)
    if cached:
        if cached["payload_hash"] != hash_payload(payload):
            raise ValueError("Anahtar farklı istek gövdesiyle kullanıldı")
        return cached["response"]

    payment = charge_card(payload)  # Dış sistemde gerçek yan etki
    response = {"paymentId": payment.id, "status": "paid"}
    idempotency_store.save(key, hash_payload(payload), response)
    return response
```

Buradaki en sinsi problem yarış koşuludur. İki aynı istek aynı anda `get` kontrolünü geçerse ikisi de kartı çekebilir. Çözüm; veritabanında `idempotency_key` üzerinde benzersiz indeks, atomik ekleme veya dağıtık kilit kullanmaktır. Anahtar kaydı ile iş kaydını mümkünse aynı veritabanı işlemi içinde ele almak da tutarlılığı güçlendirir.

| Tasarım yaklaşımı | Avantaj | Risk |
|---|---|---|
| İstemci tarafı tekrar engelleme | Hızlı kullanıcı deneyimi | Tek başına güvenlik sağlamaz. |
| Idempotency key | Ağ tekrarlarını güvenle yönetir | Saklama süresi ve eşzamanlılık gerekir. |
| Benzersiz veritabanı kısıtı | Yarış koşullarına dayanıklıdır | İş kuralını doğru modellemek gerekir. |
| Mesaj tüketicisinde olay kimliği | Kuyruk tekrarlarını önler | Tüketilmiş olayların takibi gerekir. |

Anahtarlar için makul bir TTL belirlemek önemlidir: ödeme gibi kritik işlemlerde günlerce saklama gerekebilir, geçici işlemlerde daha kısa süre yeterlidir. Ayrıca loglara anahtarı yazmak, tekrar denemeleri ve beklenmedik çakışmaları izlemenizi sağlar. Idempotency, “istek hiç iki kez gelmez” varsayımını terk eder; sisteminizi gerçek dünyanın gecikmelerine, zaman aşımlarına ve sabırsız kullanıcı tıklamalarına hazırlayan güvenlik kemeridir.
