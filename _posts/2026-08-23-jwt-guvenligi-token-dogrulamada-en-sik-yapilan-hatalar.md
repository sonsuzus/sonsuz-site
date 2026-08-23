---
layout: post
title: "JWT Güvenliği: Token Doğrulamada En Sık Yapılan Hatalar"
math: true
categories: 
  - Bilgi
tags: 
  - JWT
  - Web Güvenliği
  - Kimlik Doğrulama
---

JWT’ler (JSON Web Token), oturum bilgisini sunucu yerine imzalı bir belirteçte taşıyarak ölçeklenebilir kimlik doğrulama sağlar. Ancak “imzalı” olması, token’ın otomatik olarak güvenli olduğu anlamına gelmez. Güvenlik; imza algoritması, anahtar yönetimi, claim doğrulaması, tarayıcıda saklama biçimi ve token yaşam döngüsünün birlikte doğru tasarlanmasına bağlıdır.
``

Bir JWT üç parçadan oluşur: `header.payload.signature`. İlk iki bölüm Base64URL ile **kodlanır**, şifrelenmez; dolayısıyla payload içindeki e-posta, kullanıcı kimliği veya rol gibi bilgiler okunabilir. İmza ise token’ın yetkili sunucu tarafından üretildiğini ve sonradan değiştirilmediğini doğrular:

$$signature = HMAC_{SHA-256}(base64url(header) + "." + base64url(payload), secret)$$

Bu nedenle JWT payload’ına parola, erişim anahtarı, kişisel sağlık verisi ya da gizli iş verisi koymak ciddi bir tasarım hatasıdır. Gizlilik gerekiyorsa JWE kullanımı veya hassas verinin sunucuda tutulması değerlendirilmelidir.

## İmza doğrulaması: Algoritmaya körü körüne güvenmeyin

En tehlikeli hatalardan biri, token header’ındaki `alg` alanını doğrudan kabul etmektir. Saldırganlar geçmişte `alg: none` veya algoritma karmaşası üzerinden imza kontrolünü atlatabilmiştir. Uygulama yalnızca beklediği algoritmaları allowlist ile kabul etmelidir. Örneğin RS256 kullanan bir sistemin HS256 token kabul etmesi, genel anahtarın yanlışlıkla HMAC sırrı gibi kullanılmasına kapı açabilir.

| Hatalı yaklaşım | Risk | Doğru yaklaşım |
|---|---|---|
| Header’daki `alg` değerini kabul etmek | Algoritma karışıklığı | Sunucuda sabit algoritma allowlist’i |
| Sadece decode etmek | Sahte token kabulü | Kriptografik imzayı doğrulamak |
| Tek, kısa secret kullanmak | Brute-force riski | Yüksek entropili anahtar ve rotasyon |
| `exp` kontrolünü atlamak | Süresiz erişim | Zorunlu zaman claim denetimi |

Node.js tarafında doğrulama mantığı şu türde olmalıdır:

```js
import jwt from "jsonwebtoken";

export function verifyAccessToken(token) {
  return jwt.verify(token, process.env.JWT_PUBLIC_KEY, {
    algorithms: ["RS256"],
    issuer: "https://auth.ornek.com",
    audience: "ornek-api",
    clockTolerance: 5
  });
}
```

Bu kod yalnızca `RS256` kabul eder; ayrıca token’ı üreten tarafı (`issuer`) ve token’ın hedef API’sini (`audience`) denetler. `clockTolerance`, küçük sunucu saati farklarının meşru istekleri reddetmesini engeller; gereğinden büyük tutulmamalıdır.

## Claim’ler yetki değildir, doğrulanmış bağlamdır

`exp`, `nbf`, `iat`, `iss`, `aud`, `sub` claim’leri yalnızca token içinde bulunuyor diye güvenilir sayılmaz; imza doğrulamasından **sonra** anlam kazanırlar. Özellikle `exp` kontrol edilmezse çalınan bir token yıllarca geçerli kalabilir. Kısa ömürlü access token ve yenilenebilir refresh token modeli yaygındır:

$$T_{access} \ll T_{refresh}$$

Örneğin access token 10–15 dakika, refresh token ise günler mertebesinde olabilir. Refresh token kullanıldığında rotasyon uygulanmalı; her yenilemede yeni token üretilmeli ve eskisi geçersizleştirilmelidir. Böylece çalınmış bir refresh token’ın tekrar kullanımı tespit edilebilir.

## Tarayıcıda saklama ve XSS/CSRF dengesi

`localStorage` kullanımı pratik görünür, fakat başarılı bir XSS saldırısında JavaScript token’ı okuyup dışarı gönderebilir. `HttpOnly`, `Secure`, uygun `SameSite` niteliğine sahip cookie ise JavaScript erişimini engeller. Buna karşılık cookie tabanlı akışta CSRF tehdidi düşünülmelidir.

| Saklama yöntemi | Güçlü yanı | Dikkat edilmesi gereken |
|---|---|---|
| `localStorage` | Kolay API kullanımı | XSS ile token sızıntısı |
| HttpOnly cookie | JavaScript okuyamaz | CSRF koruması gerekir |
| Bellek içi saklama | Kalıcı XSS etkisini azaltır | Sayfa yenilemede oturum akışı gerekir |

Cookie tercihinde `SameSite=Lax` veya ihtiyaca göre `Strict`, state değiştiren isteklerde CSRF tokenı ve origin kontrolleri iyi bir başlangıçtır. Her durumda HTTPS zorunludur; aksi hâlde ağdaki biri bearer token’ı ele geçirebilir.

Son olarak JWT iptal listesi gerektirmez sözü mutlak değildir. Parola değişikliği, hesap kapatma veya şüpheli oturum durumlarında `jti` tabanlı denylist, kullanıcı için token-geçerlilik-zamanı kaydı ya da refresh token oturum tablosu gerekir. JWT’yi “durumsuz sihir” değil, açık kuralları olan imzalı bir yetki taşıyıcısı olarak tasarlamak en güvenli yaklaşımdır.
