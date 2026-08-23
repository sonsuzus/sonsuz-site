---
layout: post
title: "Idempotent API Tasarımı: Tekrarlanan İsteklerde Güvenli Servisler"
math: true
categories: 
  - Bilgi
tags: 
  - API
  - REST
  - Idempotency
  - Backend
---

Dağıtık sistemlerde aynı HTTP isteğinin yalnızca bir kez ulaştığını varsaymak, yağmurda şemsiyesiz dolaşmak gibidir: bazen sorun çıkmaz, ama çıktığında ıslanırsınız. Ağ zaman aşımları, istemcinin otomatik yeniden denemesi ve kullanıcıların iki kez tıklaması; ödeme alma, sipariş oluşturma veya e-posta gönderme gibi işlemleri istemeden çoğaltabilir. İdempotent API tasarımı, aynı isteğin tekrar edilmesi hâlinde sistemin nihai durumunu güvenli biçimde korur.
``

Matematikte bir fonksiyon, tekrar uygulandığında sonucu değişmiyorsa idempotenttir. Temel ifade şöyledir: $f(f(x)) = f(x)$. API dünyasında bu, aynı niyetle gönderilmiş bir isteğin ikinci, üçüncü veya onuncu kez çalışmasının ilk başarılı işlemin etkisini değiştirmemesi demektir. Burada önemli ayrım şudur: Yanıt gövdesi birebir aynı olmak zorunda değildir; iş kuralının ürettiği kalıcı sonuç aynı kalmalıdır.

HTTP metotları bu konuda ilk ipucunu verir:

| Metot | Varsayılan beklenti | Örnek | Risk |
|---|---|---|---|
| `GET` | İdempotent | Kullanıcı okuma | Yan etki oluşturmamalı |
| `PUT` | İdempotent | Profilin tamamını güncelleme | Gövde her seferinde aynı olmalı |
| `DELETE` | İdempotent | Kaynak silme | İkinci çağrı `404` dönebilir |
| `POST` | Genelde idempotent değil | Sipariş oluşturma | Yinelenen kayıt üretebilir |
| `PATCH` | Uygulamaya bağlı | Sayaç artırma | `+1` tekrarlandıkça değişir |

Örneğin `PUT /users/42` ile aynı kullanıcı profilini tekrar tekrar kaydetmek güvenlidir. Buna karşılık `POST /payments` çağrısını iki kez çalıştırmak iki tahsilat yaratabilir. İşte bu noktada **idempotency key** devreye girer. İstemci, her mantıksal işlem için rastgele ve benzersiz bir anahtar üretir; örneğin `Idempotency-Key: 8f3a...`. Sunucu bu anahtarı, istek gövdesinin özeti ve üretilen yanıtla birlikte saklar.

Basit akış şöyledir: İlk istek geldiğinde anahtar kilitlenir, işlem tamamlanır ve yanıt kaydedilir. Aynı anahtarla tekrar gelen istek, işlemi yeniden yürütmek yerine saklanan yanıtı döndürür. Ancak aynı anahtarın farklı gövdeyle gönderilmesi istemci hatasıdır; çoğu servis bunu `409 Conflict` veya `422 Unprocessable Content` ile reddeder.

```python
# Ödeme oluşturma için sadeleştirilmiş idempotency akışı
def create_payment(request, db):
    key = request.headers["Idempotency-Key"]
    body_hash = sha256(request.body).hexdigest()

    previous = db.idempotency.find_one({"key": key})
    if previous:
        if previous["body_hash"] != body_hash:
            return {"status": 409, "error": "Anahtar farklı istekle kullanıldı"}
        return previous["response"]

    # Gerçek uygulamada bu kayıt ve ödeme tek transaction içinde ele alınmalıdır.
    payment = charge_card(request.json["amount"], request.json["card_token"])
    response = {"status": 201, "payment_id": payment.id}
    db.idempotency.insert_one({"key": key, "body_hash": body_hash, "response": response})
    return response
```

Bu örnek fikri anlatır; üretimde yarış koşulları için anahtar alanında benzersiz indeks, atomik ekleme veya dağıtık kilit gerekir. İki istek aynı anda “kayıt yok” sonucunu görürse, ikisi de ödeme almaya kalkışabilir. Bu nedenle veritabanı kısıtı tasarımın süsü değil, güvenlik kemeridir.

| Tasarım tercihi | Avantaj | Dikkat edilmesi gereken |
|---|---|---|
| İstemci anahtarı | Yeniden denemeyi ayırt eder | Anahtarın yaşam süresi belirlenmeli |
| Yanıt önbelleği | Tekrar istekte hızlı yanıt | Hassas veri saklama politikası |
| Gövde hash'i | Anahtarın yanlış kullanımını yakalar | Kanonik JSON gerektirebilir |
| Benzersiz DB indeksi | Yarış koşullarını azaltır | Hata yönetimi tasarlanmalı |

Anahtarları sonsuza dek saklamak gerekmez. Ödeme gibi kritik işlemlerde iş gereksinimine göre 24 saat, birkaç gün veya daha uzun bir TTL seçilebilir. Ayrıca idempotency, her şeyi geri alan sihirli bir değnek değildir: E-posta, kuyruk mesajı ve üçüncü taraf çağrıları için transactional outbox, mesaj tüketicilerinde deduplikasyon ve telafi işlemleri gibi ek desenler gerekebilir.

Sonuç olarak güvenli API, “istek kaç kez geldi?” sorusundan çok “bu istek hangi kullanıcı niyetini temsil ediyor?” sorusuna odaklanır. İdempotency key, atomik veri yazımı ve iyi tanımlanmış hata yanıtları birleştiğinde, ağın kararsızlığı kullanıcılarınıza çift ödeme olarak dönmez.
