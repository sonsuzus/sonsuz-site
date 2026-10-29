---
layout: post
title: "Dijital Bankacılığın Mimarisi: Mobil Dokunuştan Gerçek Zamanlı Para Transferine"
math: true
categories: 
  - Bilgi
tags: 
  - dijital bankacılık
  - yazılım mimarisi
  - fintech
  - mikroservisler
  - gerçek zamanlı sistemler
  - siber güvenlik
toc: true
image: /img/dijital-bankaciligin-mimarisi-54.png
---

![dijital-bankaciligin-mimarisi-54](/img/dijital-bankaciligin-mimarisi-54.svg)


Mobil bankacılıkta birkaç saniye içinde tamamlanan para transferi, kullanıcıya son derece basit görünür: IBAN yazılır, tutar girilir ve düğmeye dokunulur. Oysa bu kısa yolculuğun arkasında kimlik doğrulama servisleri, dolandırıcılık motorları, muhasebe kayıtları, mesaj kuyrukları ve dış ödeme ağlarından oluşan kalabalık bir ekip çalışır. Kısacası ekrandaki “Başarılı” mesajı, dağıtık sistemlerin birlikte verdiği küçük bir konserdir.

``

## Büyük resim: Katmanlı mimari

Dijital bankacılık mimarisi genellikle istemci, erişim, iş servisleri, veri ve entegrasyon katmanlarına ayrılır. Mobil uygulama doğrudan hesap veritabanına bağlanmaz; böyle bir tasarım güvenlik ekibinin uykularını kaçırırdı. Bunun yerine istekler önce API Gateway üzerinden geçer.

| Katman | Temel görev | Örnek teknolojiler |
|---|---|---|
| Mobil istemci | Arayüz, biyometri, cihaz güvenliği | Swift, Kotlin, Flutter |
| API Gateway | Yönlendirme, hız sınırlama, doğrulama | Kong, Apigee, NGINX |
| İş servisleri | Transfer ve hesap kuralları | Java, .NET, Go |
| Veri katmanı | Bakiye, işlem ve defter kayıtları | PostgreSQL, Oracle, Redis |
| Mesajlaşma | Asenkron olay dağıtımı | Kafka, RabbitMQ |
| Entegrasyon | Ödeme ağları ve diğer bankalar | REST, ISO 20022, gRPC |

Bu ayrımın amacı yalnızca düzen değildir. Her katman bağımsız ölçeklenebilir, izlenebilir ve güvenlik politikalarıyla sınırlandırılabilir.

## Bir transferin adım adım yolculuğu

Kullanıcı transfer emrini gönderdiğinde mobil uygulama, erişim belirtecini ve benzersiz işlem anahtarını isteğe ekler. API Gateway oturumu doğrular, olağan dışı istek sıklığını kontrol eder ve çağrıyı transfer servisine iletir.

Transfer servisi sırasıyla şu soruları sorar:

1. Hesap aktif mi ve kullanıcı yetkili mi?
2. Kullanılabilir bakiye yeterli mi?
3. Alıcı bilgileri biçimsel olarak doğru mu?
4. İşlem, kara para aklama veya dolandırıcılık kuralına takılıyor mu?
5. Aynı istek daha önce işlendi mi?

Son soru **idempotency** kavramına dayanır. Mobil bağlantı kopunca kullanıcı düğmeye tekrar basabilir. Aynı anahtarla gelen istek ikinci kez para düşürmemelidir.

```http
POST /transfers
Authorization: Bearer token
Idempotency-Key: tx-2026-8f31
Content-Type: application/json

{
  "sourceAccount": "TR-A",
  "targetIban": "TR-B",
  "amount": 1250.00,
  "currency": "TRY"
}
```

Sunucu, `Idempotency-Key` değerini sonuçla birlikte saklar. Aynı anahtar yeniden geldiğinde işlemi tekrarlamak yerine önceki yanıtı döndürür.

## Para neden yalnızca bir sayı değildir?

Bankalar bakiyeyi doğrudan değiştirip geçmez; çift taraflı muhasebe defteri kullanır. Bir hesaptaki azalma başka bir hesaptaki artışla dengelenmelidir. Temel eşitlik şöyledir:

$$Varlıklar = Yükümlülükler + Öz kaynak$$

Transfer özelinde defter hareketlerinin toplamı sıfır olmalıdır:

$$\sum_{i=1}^{n} hareket_i = 0$$

Gönderen için $-1250$ TL, alıcı için $+1250$ TL kaydedilir. Kayıtlar değiştirilmeye çalışılmaz; hata varsa ters kayıt oluşturulur. Böylece denetim izi korunur.

## Gerçek zamanlılık ve tutarlılık dengesi

Her adımı tek, devasa veritabanı işlemi içinde yürütmek güvenilir görünse de dış bankalar ve ağ gecikmeleri bunu zorlaştırır. Bu nedenle modern sistemler çoğunlukla olay güdümlü mimari ve **Saga** yaklaşımı kullanır.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Senkron işlem | Anında kesin yanıt | Gecikme ve zincirleme hata |
| Asenkron olay | Yüksek ölçeklenebilirlik | Gecikmeli tutarlılık |
| Saga | Dağıtık adımları yönetir | Telafi mantığı gerektirir |

Transfer kaydedildikten sonra `TransferCreated` olayı Kafka’ya gönderilebilir. Bildirim, raporlama ve analiz servisleri bu olayı ayrı ayrı tüketir. Kritik muhasebe işlemi ise güçlü tutarlılıkla korunur.

## Güvenlik ve gözlemlenebilirlik

TLS iletişimi şifreler; OAuth 2.0 ve kısa ömürlü belirteçler erişimi sınırlar. Biyometri tek başına yeterli değildir: cihaz bağlama, işlem imzalama, limit kontrolleri ve davranış analizi birlikte kullanılmalıdır.

Son olarak her istek bir korelasyon kimliğiyle izlenir. Loglar, metrikler ve dağıtık izler sayesinde ekipler transferin hangi serviste yavaşladığını görebilir. İyi bir dijital banka yalnızca parayı hızla taşımaz; işlemi kanıtlanabilir, tekrarlanamaz ve gerektiğinde saniye saniye açıklanabilir hâle getirir.
