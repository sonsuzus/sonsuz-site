---
layout: post
title: "JWT ile Oturum Yönetimi: Stateless Kimlik Doğrulamanın Mantığı"
math: true
categories: 
  - Bilgi
tags: 
  - JWT
  - Kimlik Doğrulama
  - Web Güvenliği
---

Modern web uygulamalarında kullanıcı oturumunu yönetmenin iki temel yolu vardır: sunucuda oturum bilgisi saklamak veya bu bilgiyi istemcinin taşıdığı imzalı bir belirtece emanet etmek. JSON Web Token (JWT), ikinci yaklaşımın popüler temsilcisidir. Kullanıcı giriş yaptığında sunucu, kimliği ve yetkileri içeren imzalı bir token üretir; sonraki isteklerde token gönderilir ve sunucu imzayı doğrulayarak kullanıcıyı tanır. Böylece her istekte veritabanına ya da merkezi bir oturum deposuna bakmak zorunda kalmazsınız.
``

## JWT'nin anatomisi

JWT, noktalarla ayrılan üç Base64URL kodlu bölümden oluşur:

$$JWT = Base64URL(Header).Base64URL(Payload).Base64URL(Signature)$$

`Header`, token türünü ve imzalama algoritmasını belirtir. `Payload`, kullanıcıya ilişkin claim adı verilen alanları taşır. `Signature` ise token'ın yolda değiştirilmediğini kanıtlayan kriptografik imzadır. Önemli ayrım şudur: Base64URL **şifreleme değildir**. Payload içeriği kolayca okunabilir; bu nedenle parola, kredi kartı numarası veya gizli profil verisi token içine konulmamalıdır.

| Bölüm | Örnek içerik | Görevi | Gizli mi? |
|---|---|---|---|
| Header | `alg: HS256` | İmza algoritmasını tanımlar | Hayır |
| Payload | `sub`, `role`, `exp` | Kimlik ve yetki claim'lerini taşır | Hayır |
| Signature | Kriptografik çıktı | Bütünlüğü doğrular | Taklit edilmemeli |

Bir HMAC tabanlı imzada genel mantık şöyledir:

$$signature = HMAC_{SHA-256}(secret, encodedHeader + "." + encodedPayload)$$

Sunucu aynı gizli anahtarla imzayı yeniden üretir. Sonuç eşleşmiyorsa token reddedilir. RSA veya ECDSA gibi asimetrik yöntemlerde ise imzalama özel anahtarla, doğrulama açık anahtarla yapılır; bu yapı mikroservisler için özellikle kullanışlıdır.

## Girişten korumalı rotaya akış

Aşağıdaki Express örneği, girişte kısa ömürlü bir access token üretir ve korumalı rotada doğrular. Gerçek projede kullanıcı kontrolü mutlaka veritabanı ve güvenli parola hash'i ile yapılmalıdır.

```js
import express from "express";
import jwt from "jsonwebtoken";

const app = express();
app.use(express.json());
const secret = process.env.JWT_SECRET;

app.post("/login", (req, res) => {
  const user = { id: "42", role: "editor" }; // Örnek doğrulanmış kullanıcı
  const token = jwt.sign(
    { sub: user.id, role: user.role },
    secret,
    { expiresIn: "15m", issuer: "ornek-uygulama" }
  );
  res.json({ accessToken: token });
});

function authenticate(req, res, next) {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (!token) return res.sendStatus(401);

  try {
    req.user = jwt.verify(token, secret, { issuer: "ornek-uygulama" });
    next();
  } catch {
    res.status(401).json({ message: "Geçersiz veya süresi dolmuş token" });
  }
}

app.get("/profile", authenticate, (req, res) => {
  res.json({ userId: req.user.sub, role: req.user.role });
});
```

Bu örnekte `sub` kullanıcı kimliğini, `exp` token'ın son kullanma zamanını temsil eder. `jwt.verify` sadece imzayı değil, süre gibi standart claim'leri de denetler. Yetki kontrolü ise ayrı bir adımdır: Token geçerli diye her kaynağa erişim verilmez; `role` veya izin claim'leri rota gereksinimleriyle karşılaştırılır.

## Stateless olmanın bedeli

JWT'nin cazibesi yatay ölçeklemededir: Her sunucu imzayı doğrulayabildiği için ortak session tablosu zorunlu değildir. Ancak token çalınırsa, süresi bitene kadar geçerli kalabilir. Bu yüzden access token'lar kısa ömürlü tutulur; daha uzun oturumlar için güvenli, rotasyonu yapılan refresh token'lar kullanılır.

| Yaklaşım | Avantaj | Dikkat edilmesi gereken |
|---|---|---|
| Sunucu oturumu | Anında iptal kolaylığı | Paylaşımlı session deposu ihtiyacı |
| JWT access token | Ölçeklenebilir, hızlı doğrulama | İptal ve token hırsızlığı riski |
| Refresh token | Uzun süreli deneyim | Güvenli saklama ve rotasyon gerekir |

Token'ı tarayıcıda saklarken XSS ve CSRF tehditlerini düşünün. `HttpOnly`, `Secure`, `SameSite` özellikli çerezler JavaScript erişimini sınırlar; Authorization başlığı kullanımı ise CSRF dinamiğini değiştirir ama XSS riskini tamamen çözmez. Son olarak algoritmayı sunucuda sabitleyin, `none` gibi beklenmeyen algoritmaları kabul etmeyin, güçlü anahtarlar kullanın ve HTTPS'i zorunlu tutun. JWT sihirli bir güvenlik kalkanı değil; doğru süre, doğru claim ve doğru saklama stratejisiyle güçlü bir oturum aracıdır.
