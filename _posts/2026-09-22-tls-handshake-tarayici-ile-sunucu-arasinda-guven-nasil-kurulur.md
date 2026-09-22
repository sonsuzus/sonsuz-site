---
layout: post
title: "TLS Handshake: Tarayıcı ile Sunucu Arasında Güven Nasıl Kurulur?"
math: true
categories: 
  - Bilgi
tags: 
  - tls
  - https
  - şifreleme
  - siber güvenlik
  - sertifika
  - web
toc: true
---

Adres çubuğundaki küçük kilit simgesi, tarayıcınız ile sunucu arasında görünmez ama oldukça hareketli bir tanışma gerçekleştiğini gösterir. TLS handshake adı verilen bu süreçte taraflar kullanılacak şifreleme yöntemini belirler, sunucu kimliğini kanıtlar ve oturuma özel anahtarlar üretir. Üstelik bütün bunlar çoğunlukla birkaç ağ turunda, siz daha sayfanın açılmasını beklerken tamamlanır.

``

## TLS neyi çözmeye çalışıyor?

Şifrelenmemiş HTTP trafiği, araya giren biri tarafından okunabilir veya değiştirilebilir. TLS ise üç temel güvenlik özelliği sağlar:

| Özellik | Sağladığı güvence | Günlük hayattaki benzetme |
|---|---|---|
| Gizlilik | Veriyi yalnızca taraflar okuyabilir | Kilitli zarf |
| Bütünlük | Veride değişiklik yapıldığı anlaşılır | Mühür |
| Kimlik doğrulama | Bağlanılan sunucunun kimliği denetlenir | Resmî kimlik kartı |

Buradaki önemli ayrıntı şudur: TLS, sunucunun “iyi niyetli” olduğunu kanıtlamaz. Yalnızca alan adının kontrolünü sertifikayla ilişkilendirir ve iletişim kanalını korur. Dolandırıcılık sitesi de kendi alan adı için geçerli bir TLS sertifikası alabilir.

## İlk merhaba: ClientHello

Tarayıcı bağlantıyı başlatırken sunucuya bir **ClientHello** mesajı gönderir. Bu mesaj desteklenen TLS sürümlerini, şifre takımlarını, rastgele bir değeri ve TLS 1.3 kullanılıyorsa anahtar paylaşımı için geçici açık anahtar bilgisini içerir.

Sunucu buna **ServerHello** ile karşılık verir. Kullanılacak TLS sürümünü ve kriptografik seçenekleri seçer, kendi anahtar paylaşımını gönderir. Modern TLS 1.3 bağlantılarında çoğunlukla ECDHE kullanılır. İki taraf, gizli anahtarı ağ üzerinden doğrudan göndermeden aynı ortak sırrı hesaplar.

Basitleştirilmiş biçimde ortak sır şu fikirle gösterilebilir:

$$S = ECDH(k_{istemci}, P_{sunucu}) = ECDH(k_{sunucu}, P_{istemci})$$

Ardından oturum anahtarları, bu sırdan ve handshake özetinden türetilir:

$$K = HKDF(S, handshake\_hash)$$

Bu yaklaşım **forward secrecy** sağlar. Sunucunun uzun süreli özel anahtarı gelecekte ele geçirilse bile kaydedilmiş eski oturumların kolayca çözülememesi hedeflenir.

## Tarayıcı sertifikaya neden inanıyor?

Sunucu, alan adını ve açık anahtarını içeren sertifika zincirini gönderir. Tarayıcı zinciri kökten başlayarak doğrulamaz; sunucu sertifikasından yukarı doğru ilerleyip kendi güven deposunda bulunan kök sertifika otoritesine ulaşmaya çalışır.

Tarayıcı başlıca şu kontrolleri yapar:

1. Sertifikanın imzası geçerli mi?
2. Sertifika süresi dolmuş mu veya henüz başlamamış mı?
3. Ziyaret edilen alan adı, sertifikadaki SAN alanıyla eşleşiyor mu?
4. Zincirdeki ara sertifikalar doğru mu?
5. Sertifika iptal edilmiş görünüyor mu?

Örneğin `api.example.com` sertifikası otomatik olarak `example.net` için kullanılamaz. Joker sertifika olan `*.example.com` ise genellikle `shop.example.com` adresini kapsar; fakat `a.shop.example.com` için yeterli değildir.

## İmzalar ve Finished mesajı

Sertifikanın geçerli olması tek başına yeterli değildir. Sunucu, sertifikadaki açık anahtara karşılık gelen özel anahtara gerçekten sahip olduğunu dijital imzayla kanıtlar. Tarayıcı bu imzayı doğrular.

Son aşamada iki taraf da şimdiye kadarki handshake mesajlarından bir özet üretip **Finished** mesajı yollar. Özetler uyuşursa görüşmenin değiştirilmediği anlaşılır. Bundan sonra HTTP istekleri, türetilen simetrik anahtarlarla şifrelenir. Simetrik şifreleme, büyük miktarda veri için açık anahtarlı yöntemlerden daha hızlıdır.

| Aşama | Kullanılan yaklaşım | Amaç |
|---|---|---|
| Sertifika doğrulama | Dijital imza | Sunucu kimliğini doğrulamak |
| Anahtar anlaşması | ECDHE | Ortak sır üretmek |
| Veri aktarımı | AES-GCM veya ChaCha20-Poly1305 | Hızlı ve güvenli iletişim |

## Handshake’i terminalden izlemek

Bir sunucunun sunduğu sertifika zincirini OpenSSL ile inceleyebilirsiniz:

```bash
openssl s_client \
  -connect example.com:443 \
  -servername example.com \
  -showcerts
```

Buradaki `-servername` seçeneği SNI bilgisini gönderir. Aynı IP adresinde birden fazla site barındırılıyorsa sunucunun doğru sertifikayı seçmesini sağlar. Çıktıdaki `Protocol`, `Cipher` ve `Verify return code` alanları sırasıyla TLS sürümünü, seçilen şifre takımını ve doğrulama sonucunu gösterir.

Kısacası TLS handshake, “bir sertifika gönder ve şifrelemeye başla” işleminden daha fazlasıdır. Tarayıcı güven zincirini denetler, sunucu özel anahtara sahip olduğunu kanıtlar, taraflar geçici bir ortak sır üretir ve tüm görüşmenin bütünlüğünü doğrular. Kilit simgesinin arkasında küçük ama disiplinli bir kriptografi orkestrası çalışır.
