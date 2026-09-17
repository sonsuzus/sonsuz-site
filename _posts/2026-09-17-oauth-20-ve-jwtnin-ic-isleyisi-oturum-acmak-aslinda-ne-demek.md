---
layout: post
title: "OAuth 2.0 ve JWT’nin İç İşleyişi: Oturum Açmak Aslında Ne Demek?"
math: true
categories: 
  - Bilgi
tags: 
  - oauth2
  - jwt
  - kimlik doğrulama
  - yetkilendirme
  - openid connect
  - web güvenliği
toc: true
---

Bir uygulamada “Google ile giriş yap” düğmesine bastığımızda birkaç saniye içinde hesabımıza ulaşırız. Perdenin arkasındaysa yönlendirmeler, izinler, kriptografik imzalar ve süreli anahtarlar çalışır. Üstelik OAuth 2.0 doğrudan bir oturum açma protokolü değildir! Gelin kimlik doğrulama ile yetkilendirme arasındaki sis perdesini kaldıralım.

``

## Oturum açmak hangi problemi çözer?

“Oturum açmak” günlük dilde tek işlem gibi görünse de üç ayrı kavram içerir:

| Kavram | Cevapladığı soru | Örnek |
|---|---|---|
| Kimlik doğrulama | Sen kimsin? | Parola, biyometri, OpenID Connect |
| Yetkilendirme | Neyi yapabilirsin? | Dosyaları okuma izni |
| Oturum yönetimi | Seni sonraki istekte nasıl tanırım? | Cookie veya erişim belirteci |

OAuth 2.0 esasen **yetkilendirme çerçevesidir**. Kullanıcının parolasını başka bir uygulamaya vermeden, belirli kaynaklara sınırlı erişim sağlatır. Kimliği standart biçimde öğrenmek için OAuth 2.0 üzerine kurulan **OpenID Connect (OIDC)** kullanılır.

Sistemde genellikle dört oyuncu bulunur: kullanıcı yani Resource Owner, erişim isteyen Client, izinleri yöneten Authorization Server ve verileri sunan Resource Server. Örneğin bir fotoğraf baskı uygulamasının Google Fotoğraflar’a erişmesi bu modele uyar.

## Authorization Code akışı

Modern web ve mobil uygulamalarda önerilen yöntem Authorization Code Flow ve PKCE birleşimidir:

1. İstemci rastgele bir `code_verifier` üretir.
2. Bunun özeti alınarak `code_challenge` oluşturulur.
3. Tarayıcı yetkilendirme sunucusuna yönlendirilir.
4. Kullanıcı kimliğini doğrular ve izin ekranını onaylar.
5. Sunucu istemciye kısa ömürlü, tek kullanımlık bir `code` yollar.
6. İstemci bu kodu ve `code_verifier` değerini token uç noktasında değiştirir.

PKCE ilişkisi basitleştirilmiş biçimde şöyledir:

$$code\_challenge = Base64URL(SHA256(code\_verifier))$$

Böylece yönlendirme sırasında kodu çalan saldırgan, gizli doğrulayıcıya sahip olmadığı için token alamaz.

```javascript
const response = await fetch("https://auth.example.com/token", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({
    grant_type: "authorization_code",
    code: authorizationCode,
    redirect_uri: "https://app.example.com/callback",
    client_id: "web-client",
    code_verifier: storedVerifier
  })
});

const tokens = await response.json();
```

Bu kod, alınan geçici yetkilendirme kodunu token setiyle değiştirir. Gerçek uygulamada HTTPS zorunlu olmalı; hata yanıtları ve `state` doğrulaması da mutlaka ele alınmalıdır.

## JWT nedir, ne değildir?

JWT, verileri taşımaya yarayan bir **belirteç biçimidir**; OAuth’un alternatifi değildir. Üç Base64URL bölümünden oluşur:

`header.payload.signature`

Payload içinde `sub` kullanıcıyı, `aud` hedef servisi, `iss` üreticiyi, `exp` ise sona erme zamanını gösterebilir. İmza genel olarak şu veriyi korur:

$$signature = Sign(key, Base64Url(header) + "." + Base64Url(payload))$$

JWT çoğunlukla **imzalıdır, şifreli değildir**. Payload herkes tarafından okunabilir; parola veya kredi kartı bilgisi buraya konmamalıdır. API yalnızca imzayı değil `iss`, `aud`, `exp` ve izinleri de doğrulamalıdır.

| Token | Amaç | Tipik ömür | Saklama yaklaşımı |
|---|---|---:|---|
| Access token | API çağırmak | Dakikalar | Mümkünse bellek |
| Refresh token | Yeni access token almak | Günler | Güvenli sunucu veya korumalı depolama |
| ID token | Kullanıcı kimliğini istemciye bildirmek | Kısa | OIDC istemcisi doğrular |

## Sonuç: Düğmenin arkasındaki anlaşma

Oturum açma, sunucunun “Bu istek aynı kullanıcıya mı ait?” sorusuna güvenli ve süreli bir cevap üretmesidir. OAuth 2.0 erişim yetkisini devreder, OIDC kimlik katmanını ekler, JWT ise bazı tokenların taşınma biçimi olabilir. Kısa token ömrü, PKCE, kesin yönlendirme adresleri, güvenli cookie seçenekleri ve doğru claim doğrulaması kullanıldığında o sıradan giriş düğmesi oldukça sağlam bir güvenlik protokolüne dönüşür.
