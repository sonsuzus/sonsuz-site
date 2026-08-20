---
layout: post
title: "OAuth 2.0 ile Güvenli Yetkilendirme Akışları: Anahtarı Vermeden Kapıyı Açmak"
math: true
categories: 
  - Bilgi
tags: 
  - oauth 2.0
  - kimlik doğrulama
  - apı güvenliği
image: /img/oauth-20-ile-41.png
---

Bir uygulamanın kullanıcı adına Google Drive dosyalarına erişmesi, GitHub depolarını listelemesi veya Spotify çalma listesi oluşturması sık rastlanan bir ihtiyaçtır. Ancak uygulamanın kullanıcının parolasını istemesi hem tehlikeli hem de gereksizdir. OAuth 2.0, parolayı paylaşmadan, sınırlı ve süreli erişim izinleri vermeyi sağlayan yetkilendirme çerçevesidir. Kısacası uygulamaya evinizin anahtarını değil, yalnızca belirli odalara girebilen ve süresi dolan bir ziyaretçi kartı verirsiniz.
``
OAuth 2.0 öncelikle bir **kimlik doğrulama** protokolü değil, bir **yetkilendirme** standardıdır. Kimlik doğrulama, “Bu kişi kim?” sorusunu; yetkilendirme ise “Bu kişi veya uygulama ne yapabilir?” sorusunu yanıtlar. Kullanıcı kimliğini standart biçimde almak için OAuth 2.0’ın üzerine inşa edilen **OpenID Connect (OIDC)** kullanılır.

| Kavram | Görevi | Örnek |
|---|---|---|
| Resource Owner | Verinin sahibi olan kullanıcı | Ayşe |
| Client | Erişim isteyen uygulama | Fotoğraf düzenleme uygulaması |
| Authorization Server | İzin veren ve token üreten sunucu | Google OAuth sunucusu |
| Resource Server | Korunan API/veri sunucusu | Google Drive API |
| Access Token | API çağrılarında taşınan kısa ömürlü izin belgesi | `Bearer eyJ...` |

![oauth-20-ile-41](/img/oauth-20-ile-41.svg)


Sistemin merkezinde **access token** bulunur. Bu token çoğunlukla kısa ömürlüdür; örneğin bir saat geçerli olabilir. Süre dolduğunda, uygun koşullarda **refresh token** kullanılarak yeni bir access token alınır. Süreli token yaklaşımı, bir sızıntının etkisini azaltır. Basitçe token geçerliliğini şöyle düşünebiliriz:

$$T_{etkili} = \min(T_{token}, T_{izin}, T_{oturum})$$

Yani token teknik olarak geçerli olsa bile kullanıcı izni kaldırmış veya oturum sonlanmışsa erişim kesilmelidir.

## En güvenli tercih: Authorization Code Flow + PKCE

Web, mobil ve masaüstü uygulamalarında güncel öneri **Authorization Code Flow with PKCE** akışıdır. PKCE (Proof Key for Code Exchange), yetkilendirme kodu ele geçirilse dahi saldırganın onu token’a dönüştürmesini zorlaştırır.

Akış sırasıyla şöyledir:

1. İstemci rastgele bir `code_verifier` üretir.
2. Bunun SHA-256 özetiyle `code_challenge` oluşturur.
3. Kullanıcı tarayıcı üzerinden yetkilendirme sunucusuna yönlendirilir.
4. Kullanıcı izin verdikten sonra uygulamanın `redirect_uri` adresine kısa ömürlü bir `code` gelir.
5. Uygulama, `code` ile birlikte orijinal `code_verifier` değerini token uç noktasına gönderir.
6. Sunucu doğrulama yapar ve access token döndürür.

```javascript
import crypto from "node:crypto";

const verifier = crypto.randomBytes(32).toString("base64url");
const challenge = crypto
  .createHash("sha256")
  .update(verifier)
  .digest("base64url");

const params = new URLSearchParams({
  client_id: process.env.CLIENT_ID,
  redirect_uri: "http://localhost:3000/callback",
  response_type: "code",
  scope: "read_profile read_files",
  code_challenge: challenge,
  code_challenge_method: "S256",
  state: crypto.randomBytes(16).toString("hex")
});

console.log(`https://auth.example.com/authorize?${params}`);
```

Bu kod, yönlendirme adresini üretir. `state` parametresi özellikle önemlidir: İsteği başlatan tarayıcı oturumu ile dönüş isteğini eşleştirerek CSRF saldırılarına karşı koruma sağlar. Gerçek uygulamada `state` değeri sunucu tarafındaki oturumda saklanmalı ve callback sırasında mutlaka doğrulanmalıdır.

| Akış | Uygun kullanım | Dikkat edilmesi gereken |
|---|---|---|
| Authorization Code + PKCE | SPA, mobil, geleneksel web | Önerilen varsayılan seçimdir |
| Client Credentials | Sunucudan sunucuya API erişimi | Kullanıcı verisi için kullanılmaz |
| Device Authorization | TV, CLI, giriş ekranı zayıf cihazlar | Kullanıcı ikinci cihazda onay verir |
| Implicit Flow | Eski tarayıcı tabanlı uygulamalar | Güncel projelerde kaçınılmalıdır |

## Güvenlik kontrol listesi

Token’ları URL’ye, loglara veya tarayıcı `localStorage` alanına gelişigüzel yazmayın. Sunucu taraflı uygulamalarda `HttpOnly`, `Secure` ve `SameSite` nitelikli çerezler daha güvenli bir seçenek olabilir. Her zaman HTTPS kullanın, izinleri en az ayrıcalık ilkesiyle (`scope`) sınırlandırın ve yönlendirme URI’lerini yetkilendirme sunucusunda tam eşleşecek biçimde kaydedin.

Son olarak, `client_secret` yalnızca gizli sunucu ortamlarında korunabilir; SPA ve mobil uygulamalarda gerçekten sır değildir. Bu yüzden bu tür istemcilerde PKCE kritik önemdedir. OAuth 2.0 doğru uygulandığında, kullanıcı deneyimini bozmadan uygulamalara kontrollü erişim verir: parola paylaşılmaz, izinler görünür olur ve erişim gerektiğinde geri alınabilir.
