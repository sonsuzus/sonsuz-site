---
layout: post
title: "Fintech API’leri: Bankalar ve Yazılımlar Birbirleriyle Nasıl Konuşuyor?"
math: true
categories: 
  - Bilgi
tags: 
  - fintech
  - api
  - açık-bankacılık
  - oauth
  - python
  - güvenlik
toc: true
image: /img/fintech-apileri-bankalar-88.png
---

Bir bütçe uygulaması banka bakiyenizi nasıl gösteriyor? Bir e-ticaret sitesi ödemenizin tamamlandığını nasıl anlıyor? Cevap, bankanın içinde klavyeye yetişmeye çalışan minik muhasebeciler değil: API’ler! Bu arayüzler, finansal sistemlerin belirli kurallar ve izinler çerçevesinde veri alışverişi yapmasını sağlıyor. Ancak para söz konusu olduğunda, sohbetin hem güvenli hem de tutarlı olması gerekiyor.

``

## API: Finans dünyasının ortak sözleşmesi

API, bir yazılımın başka bir yazılıma sunduğu programlama arayüzüdür. Bankacılıkta bu arayüz; hesapları listelemek, işlem geçmişini okumak veya ödeme başlatmak gibi yetenekler sunabilir.

Buradaki temel fikir **sözleşmedir**: Hangi adrese istek gönderileceği, hangi alanların beklendiği, kimlerin erişebileceği ve hataların nasıl bildirileceği önceden tanımlanır. API, bankanın veritabanına açılan sınırsız bir kapı değil, yetkileri sınırlandırılmış bir servis girişidir.

REST tabanlı sistemlerde HTTP yöntemleri yaygındır: `GET` veri okumak, `POST` ise ödeme talebi gibi yeni bir işlem oluşturmak için kullanılabilir. JSON, taşınan verinin sık kullanılan formatıdır; ancak bütün bankalar aynı uç noktaları veya alan isimlerini kullanmaz.

## Bir isteğin banka yolculuğu

Bir açık bankacılık uygulamasının hesap bilgilerini okuduğunu düşünelim:

1. **İzin:** Kullanıcı, hangi hesaplara ve verilere erişilebileceğini onaylar. Bu onay belirli bir süreyle sınırlandırılabilir.
2. **Yetkilendirme:** Uygulama, uygun akış üzerinden bir erişim belirteci alır. OAuth 2.0 burada sık kullanılan bir yetkilendirme çerçevesidir.
3. **İstek:** Uygulama, erişim belirtecini ekleyerek bankanın API’sine HTTPS üzerinden bağlanır.
4. **Kontrol:** Banka; uygulamanın yetkisini, iznin geçerliliğini ve istenen işlemin kapsamını denetler.
5. **Yanıt:** Banka, sözleşmeye uygun veriyi veya bir hata yanıtını döndürür.

OAuth 2.0, tek başına her durumda kullanıcı kimliğini doğrulayan bir protokol değildir. Kimlik doğrulama ile yetkilendirme ilişkili, fakat farklı kavramlardır. Ayrıca uygulamanın kullanıcıdan internet bankacılığı şifresini toplaması bu modelin gereği değildir.

## Anlık yanıt, tamamlanmış işlem demek değildir

Toplam yanıt süresini kabaca $T = T_a + T_k + T_i$ şeklinde düşünebiliriz. Burada $T_a$ ağ gecikmesini, $T_k$ güvenlik kontrollerini, $T_i$ ise işlem süresini temsil eder. Fakat bu süre yalnızca isteğin yanıtlanmasını anlatır; paranın kesin olarak alıcıya geçtiğini değil!

| İletişim biçimi | Kim başlatır? | Tipik kullanım |
|---|---|---|
| REST API isteği | Uygulama | Bakiye sorgulama, ödeme başlatma |
| Webhook bildirimi | Servis sağlayıcı | Ödeme durumunun değiştiğini haber verme |
| Toplu dosya aktarımı | Planlanmış süreç | Gün sonu raporu ve mutabakat |

Bunlar rakip değil, tamamlayıcı yöntemlerdir. Örneğin `202 Accepted`, isteğin işlenmek üzere kabul edildiğini belirtir; ödeme başarısı garantisi vermez. Kesin durum, sorgulama uç noktasından veya doğrulanmış bir webhook üzerinden öğrenilebilir.

## Python ile örnek ödeme isteği

Aşağıdaki örnek, `requests` kütüphanesiyle temsili bir API’ye ödeme talebi gönderir. Alanlar sağlayıcıya göre değişir; `API_ROOT` gerçek para hareketi olmayan test ortamına ayarlanmalıdır.

```python
import os
import requests

payment_key = os.environ["PAYMENT_KEY"]
response = requests.post(
    f'{os.environ["API_ROOT"]}/payments',
    headers={
        "Authorization": f'Bearer {os.environ["ACCESS_TOKEN"]}',
        "Idempotency-Key": payment_key,
    },
    json={
        "amount_minor": 1250,
        "currency": "TRY",
        "recipient_ref": "beneficiary_42",
    },
    timeout=(3, 10),
)
response.raise_for_status()
print(response.json()["status"])
```

Bu örnekte tutar, sözleşme gereği kuruş cinsindendir: 1250 kuruş, 12,50 TL eder. Tamsayı kullanımı, kayan noktalı sayıların hassasiyet sorunlarını önlemeye yardımcı olur. Bağlantı ve okuma zaman aşımı ayrı tanımlanmıştır; kod HTTP hatasında istisna üretir. Üretimde bu hatalar ayrıca ele alınmalıdır.

**Idempotency anahtarı**, sağlayıcı destekliyorsa, aynı mantıksal talebin tekrarında ikinci bir ödeme oluşmasını önlemeye yardımcı olur. Anahtar işlemle birlikte kalıcı saklanmalı, tekrar denemelerinde değiştirilmemelidir. Sağlayıcının saklama süresi ve tekrar davranışı mutlaka incelenmelidir.

## Güvenlik ve belirsizlikle yaşamak

HTTPS aktarımı korur; bazı entegrasyonlarda karşılıklı TLS ile uygulamanın sertifikası da doğrulanır. Erişim belirteçleri ve hesap bilgileri günlüklere gelişigüzel yazılmamalıdır. Webhook’larda sağlayıcının imza doğrulaması uygulanmalı, tekrar oynatılan veya yinelenen bildirimler hesaba katılmalıdır.

En kritik senaryo şudur: Banka ödemeyi kabul eder, fakat yanıt ağda kaybolur. Zaman aşımı, başarısız ödeme anlamına gelmez. Körlemesine yeni ödeme oluşturmak yerine mevcut işlem sorgulanmalı ve belgelenmiş tekrar mekanizması kullanılmalıdır. Hız sınırı yanıtlarında da sağlayıcının bekleme talimatlarına uyulmalıdır.

Son olarak **mutabakat**, uygulamanızdaki kayıtlarla bankanın kayıtlarını karşılaştırır. Çünkü sağlam fintech entegrasyonu yalnızca konuşabilen değil; yanlış anlayınca durabilen, tekrarları yönetebilen ve gün sonunda hesabını verebilen yazılımdır.

![fintech-apileri-bankalar-88](/img/fintech-apileri-bankalar-88.svg)

