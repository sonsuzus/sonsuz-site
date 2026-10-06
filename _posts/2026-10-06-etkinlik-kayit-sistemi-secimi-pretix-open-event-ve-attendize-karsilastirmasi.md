---
layout: post
title: "Etkinlik Kayıt Sistemi Seçimi: Pretix, Open Event ve Attendize Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - etkinlik
  - pretix
  - open-event
  - attendize
  - açık-kaynak
  - biletleme
toc: true
image: /img/etkinlik-kayit-sistemi-42.png
---

Bir etkinlik düzenlemek dışarıdan bakıldığında birkaç konuşmacı, biraz kahve ve bolca yaka kartından ibaret görünebilir. Ancak kayıtlar başladığında kapasite yönetimi, bilet türleri, ödemeler, QR kodları ve iptaller sahne arkasında küçük bir yazılım orkestrasına dönüşür. Pretix, Open Event ve Attendize bu orkestrayı yönetmek için kullanılabilecek açık kaynak ağırlıklı üç güçlü alternatiftir.
``
## Etkinlik kayıt sisteminin temel mantığı

Bir kayıt sistemi yalnızca ad ve e-posta saklayan bir form değildir. Temel veri modeli genellikle **etkinlik**, **bilet türü**, **sipariş**, **katılımcı**, **ödeme** ve **check-in** varlıklarından oluşur. Bir sipariş birden fazla katılımcı içerebilir; her katılımcının ise farklı bir bileti veya oturumu olabilir.

Kapasite hesabını en basit biçimiyle şöyle gösterebiliriz:

$$Kalan\ Kapasite = Toplam\ Kapasite - Onaylı\ Biletler - Rezerve\ Biletler$$

Talep yoğunluğunu ölçmek için de doluluk oranı kullanılabilir:

$$Doluluk\ Oranı = \frac{Satılan\ Bilet}{Toplam\ Kapasite} \times 100$$

Bu formüldeki “rezerve” kavramı önemlidir. Kullanıcı ödeme ekranındayken koltuğu kısa süreliğine ayırmazsanız aynı son bileti iki kişiye satabilirsiniz. Dağıtık sistemlerin klasik yarış koşulu, konferans kapısında tatsız bir sürprize dönüşür.

## Üç platformun karakteri

| Özellik | Pretix | Open Event | Attendize |
|---|---|---|---|
| Temel yaklaşım | Biletleme ve ödeme odaklı | Etkinlik programı ve topluluk odaklı | Sade, kendi sunucunda biletleme |
| Teknoloji ekosistemi | Python/Django | API merkezli modern yapı | PHP/Laravel |
| Çoklu etkinlik | Güçlü | Güçlü | Temel ihtiyaçlara uygun |
| Check-in | Mobil ve çevrim dışı senaryolara uygun | Etkinlik uygulamalarıyla bütünleşebilir | QR kod tabanlı kullanım |
| Özelleştirme | Eklenti ve API seçenekleri geniş | API ve istemci uygulamaları güçlü | Laravel bilenler için erişilebilir |
| En uygun senaryo | Profesyonel bilet satışı | Konferans, program ve konuşmacı yönetimi | Küçük veya orta ölçekli organizasyon |

### Pretix

Pretix, karmaşık bilet türleri, kuponlar, vergi kuralları, bekleme listeleri ve ödeme sağlayıcıları gereken projelerde öne çıkar. Birden fazla organizatörün veya etkinliğin yönetileceği yapılarda güçlüdür. Buna karşılık seçenek sayısının fazla olması ilk kurulum ekranlarını biraz “uçak kokpiti” gibi hissettirebilir.

### Open Event

FOSSASIA ekosistemindeki Open Event, yalnızca bilet satmaya değil; konuşmacı, oturum, salon ve etkinlik programı yönetmeye de odaklanır. Özellikle konferans veya festival gibi program akışının bilet kadar önemli olduğu projelerde anlamlıdır. API merkezli yaklaşımı, özel web ya da mobil istemci geliştirecek ekiplerin işini kolaylaştırır.

### Attendize

Attendize, Laravel tabanlı ve daha sade bir kendi sunucunda barındırma deneyimi sunar. PHP ekosistemine hâkim ekipler kodu uyarlamakta rahat edebilir. Bununla birlikte üretime geçmeden önce kullanılan sürümün güncelliği, topluluk etkinliği, güvenlik yamaları ve ödeme entegrasyonlarının bölgesel uyumluluğu mutlaka incelenmelidir.

## Webhook ile kaydı başka sisteme aktarmak

Kayıt tamamlandığında CRM, e-posta servisi veya yaka kartı uygulaması bilgilendirilebilir. Aşağıdaki Python örneği, gelen webhook isteğinin imzasını doğrular:

```python
import hashlib
import hmac

SECRET = b"super-secret-key"

def verify_webhook(raw_body: bytes, received_signature: str) -> bool:
    expected = hmac.new(
        SECRET,
        raw_body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, received_signature)
```

Burada HMAC, isteğin gerçekten güvendiğimiz sistemden geldiğini kontrol eder. `compare_digest` kullanılması zamanlama saldırılarına karşı normal metin karşılaştırmasından daha güvenlidir. Doğrulama sonrasında işlem mümkünse kuyruğa aktarılmalı; webhook’a hızlıca başarılı yanıt verilmelidir.

## Hangisini seçmeli?

Ödeme, vergi, kupon ve gelişmiş biletleme öncelikliyse **Pretix**; konuşmacı ve program yönetimi merkezdeyse **Open Event**; sade arayüz ve Laravel ile özelleştirme isteniyorsa **Attendize** mantıklı adaydır. Son kararı vermeden önce KVKK süreçleri, yedekleme, e-posta teslimatı, ödeme komisyonları, güncelleme politikası ve yoğunluk testi değerlendirilmelidir. Çünkü iyi bir kayıt sistemi yalnızca bilet satmaz; etkinlik sabahı oluşabilecek kuyruğu da daha oluşmadan yönetir.

![etkinlik-kayit-sistemi-42](/img/etkinlik-kayit-sistemi-42.svg)

