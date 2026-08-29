---
layout: post
title: "Mobil Uygulamalarda OAuth 2.0 ve OpenID Connect: Authorization Code + PKCE Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - oauth 2.0
  - openıd connect
  - pkce
toc: true
---

Mobil uygulamalar için oturum açma tasarlarken en riskli fikirlerden biri, kullanıcı parolasını doğrudan uygulamaya toplatmak veya istemci sırrını APK/IPA içine gömmektir. Mobil paketler tersine mühendisliğe açıktır; bu nedenle uygulamanız bir **public client** olarak düşünülmelidir. Güvenli yaklaşım, kimlik sağlayıcının tarayıcı tabanlı oturumunu kullanan OAuth 2.0 Authorization Code akışı ile OpenID Connect (OIDC) katmanını, PKCE korumasıyla birleştirmektir.

``

Önce rollerin dilini netleştirelim. OAuth 2.0, bir uygulamanın kullanıcı adına API erişim yetkisi almasını sağlar; yani temel sorusu “Bu uygulama hangi kaynağa erişebilir?”dir. OIDC ise OAuth 2.0 üzerine kimlik doğrulama ekler ve “Kullanıcı kim?” sorusunu yanıtlar. Bu yanıt çoğunlukla imzalı bir JWT olan `id_token` içinde gelir.

| Kavram | OAuth 2.0 | OpenID Connect |
|---|---|---|
| Ana amaç | Yetkilendirme | Kimlik doğrulama + yetkilendirme |
| Temel çıktı | `access_token` | `id_token`, `access_token` |
| Örnek scope | `api.read` | `openid`, `profile`, `email` |
| Kullanım alanı | API çağrısı | Kullanıcı oturumu ve profil |

## 1. Kimlik sağlayıcıyı ve yönlendirmeyi kaydedin

Kimlik sağlayıcıda mobil istemcinizi kaydedin; `client_id` üretin ve platforma özel callback adresleri tanımlayın. Tercihen claimed HTTPS redirect (`https://uygulama.example.com/callback`) veya Android App Links / iOS Universal Links kullanın. Özel şema (`myapp://callback`) mümkündür, ancak başka uygulamaların şemayı kapma riski nedeniyle daha dikkatli ele alınmalıdır.

Buradaki kritik kural şudur: Mobil uygulamaya `client_secret` koymayın. Sır, cihazdaki dosyada saklansa bile bir gün çıkarılır. Güvenlik modeli bunun yerine PKCE ile kod değişimini bağlar.

## 2. PKCE değerlerini üretin

PKCE, yakalanmış bir authorization code’un saldırgan tarafından token’a çevrilmesini engeller. Uygulama rastgele bir `code_verifier` üretir; sonra onun SHA-256 özeti olan `code_challenge` değerini gönderir:

$$code\_challenge = BASE64URL(SHA256(code\_verifier))$$

`code_verifier`, 43–128 karakter uzunluğunda, kriptografik olarak güvenli rastgele bir dize olmalıdır. `S256` yöntemini kullanın; `plain` yöntemi modern istemciler için uygun değildir.

```kotlin
val verifier = secureRandomUrlSafeString(64)
val challenge = base64UrlNoPadding(
    MessageDigest.getInstance("SHA-256")
        .digest(verifier.toByteArray(Charsets.US_ASCII))
)
```

Bu kod, Android tarafında doğrulayıcıyı ve sağlayıcıya gönderilecek meydan okumayı üretir. `verifier` değerini yalnızca geçici olarak, uygulamanın güvenli depolamasında tutun.

## 3. Authorization isteğini sistem tarayıcısında başlatın

Uygulama içi WebView yerine sistem tarayıcısı veya platformun yetkilendirme sekmesini kullanın. Böylece kullanıcı, gerçek sağlayıcının alan adını görür; SSO çerezleri çalışır ve uygulamanız parolaya erişmez. İsteğe `response_type=code`, `client_id`, `redirect_uri`, `scope=openid profile`, `code_challenge`, `code_challenge_method=S256` ve tahmin edilemez `state` ekleyin. OIDC için ayrıca `nonce` üretin.

| Parametre | Güvenlik işlevi |
|---|---|
| `state` | CSRF ve yanlış callback eşlemesini önler |
| `nonce` | `id_token` yeniden oynatma riskini azaltır |
| `code_challenge` | Kod ele geçirilse bile token alınmasını zorlaştırır |
| `redirect_uri` | Yanıtın yalnızca kayıtlı hedefe dönmesini sağlar |

## 4. Callback’i doğrulayın ve kodu token’a çevirin

Callback geldiğinde önce dönen `state` ile saklanan değeri sabit zamanlı karşılaştırın. Ardından authorization code’u token endpoint’ine, aynı `redirect_uri` ve özgün `code_verifier` ile gönderin. Sağlayıcı challenge ile verifier uyuşmuyorsa isteği reddeder.

OIDC kullanıyorsanız `id_token` içindeki imzayı sağlayıcının JWKS anahtarlarıyla doğrulayın; ayrıca `iss`, `aud`, `exp` ve `nonce` claim’lerini kontrol edin. Sadece JWT’nin decode edilmesi doğrulama değildir: imza kontrolü yapılmadan token’a güvenilmez.

## 5. Token yaşam döngüsünü yönetin

`access_token` kısa ömürlü olmalı; API çağrılarında `Authorization: Bearer` başlığıyla kullanılmalıdır. Yenileme token’ı veriliyorsa onu iOS Keychain veya Android Keystore destekli güvenli depoda saklayın. Token’ları loglamayın, panoya kopyalamayın ve analitik olaylarına eklemeyin. Çıkışta yerel token’ları silin; sağlayıcı destekliyorsa revocation endpoint’ini de çağırın.

Sonuçta formül basittir: tarayıcıda yetkilendir, PKCE ile kodu bağla, callback ve token claim’lerini doğrula, sırları değil kısa ömürlü token’ları yönet. Bu yapı hem kullanıcı deneyimini hem de mobil güvenlik sınırlarını ciddi biçimde iyileştirir.
