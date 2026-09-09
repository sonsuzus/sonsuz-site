---
layout: post
title: "JWT Çalındığında Ne Olur? Sunucu Taraflı Oturum Yönetiminin Gizli Tuzakları"
math: true
categories: 
  - Bilgi
tags: 
  - jwt
  - apı güvenliği
  - oturum yönetimi
toc: true
---

JWT, modern API’lerin kimlik doğrulama dünyasındaki hızlı geçiş kartıdır: İmzayı kontrol et, kullanıcıyı tanı ve isteği içeri al. Ancak kart çalındığında sistem çoğu zaman kapıyı açmaya devam eder. Güvenli bir mimari; yalnızca belirtecin geçerli olup olmadığını değil, ilişkili oturumun hâlâ güvenilir olup olmadığını da sorgulamalıdır.
``
## JWT neden tek başına oturum değildir?

JWT’nin temel avantajı, sunucunun her istekte merkezi oturum kaydı aramadan doğrulama yapabilmesidir. Bir belirteç kabaca şu alanları taşır:

```json
{
  "sub": "user-42",
  "jti": "token-abc",
  "iat": 1750000000,
  "exp": 1750000900
}
```

İmza, içeriğin değiştirilmediğini kanıtlar; belirtecin çalınmadığını veya kullanıcının oturumu kapatmadığını kanıtlamaz. Geçerlilik koşulu basitleştirilirse:

$$
Valid(T)=SignatureOK(T) \land now < exp(T)
$$

Gerçek bir uygulamada denklem daha kapsamlı olmalıdır:

$$
Accept(T)=Valid(T) \land SessionActive(T) \land \neg Revoked(T)
$$

Bu fark önemlidir. Saldırgan geçerli bir access token ele geçirirse parola değişikliği, çıkış işlemi veya hesap kilitleme uygulanmasına rağmen token süresi dolana kadar API’ye erişebilir.

## Sık karşılaşılan gizli açıklar

| Yaklaşım | Gizli risk | Daha güvenli çözüm |
|---|---|---|
| Uzun ömürlü access token | Çalınan token saatlerce kullanılabilir | 5–15 dakikalık ömür |
| Sadece istemcide çıkış | Sunucudaki token geçerliliğini korur | Oturumu sunucuda iptal etme |
| Değişmeyen refresh token | Kopyası sınırsız yenileme yapabilir | Refresh token rotasyonu |
| Token’ı veritabanında düz saklama | Veritabanı sızıntısı doğrudan erişim sağlar | Token özetini saklama |
| Yalnızca `exp` kontrolü | Hesap kapatma kararını görmez | Oturum sürümü veya denylist |

Saat farkı da küçük ama etkili bir tuzaktır. Sunucuların saatleri senkron değilse yeni token “henüz geçerli değil” sayılabilir veya süresi dolmuş token kısa süre daha kabul edilebilir. NTP senkronizasyonu kullanılmalı; tolerans mümkünse 30–60 saniyeyi aşmamalıdır.

## Hibrit oturum modeli

Pratik bir tasarımda access token kısa ömürlü, refresh token ise rastgele ve tek kullanımlık olur. Sunucu refresh token’ın kendisini değil, kriptografik özetini saklar. Oturum kaydı; kullanıcı kimliği, cihaz bilgisi, sona erme zamanı ve iptal durumunu içerir.

```js
import crypto from 'node:crypto';

const digest = token =>
  crypto.createHash('sha256').update(token).digest('hex');

async function rotateRefreshToken(rawToken) {
  const hash = digest(rawToken);
  const session = await db.sessions.findByRefreshHashForUpdate(hash);

  if (!session || session.revokedAt || session.expiresAt < new Date()) {
    throw new Error('Oturum geçersiz');
  }

  const nextToken = crypto.randomBytes(32).toString('base64url');
  await db.sessions.replaceRefreshHash(session.id, digest(nextToken));
  return nextToken;
}
```

Bu örnek, token’ı özetleyerek arar ve işlem sırasında kaydı kilitler. Kilit veya atomik güncelleme önemlidir; aksi hâlde aynı refresh token ile eşzamanlı iki yenileme yapılabilir. Kullanılmış token yeniden görülürse bu durum olası hırsızlık olarak değerlendirilip ilgili token ailesinin tamamı iptal edilmelidir.

## Çalınmaya karşı savunma katmanları

Tarayıcı uygulamalarında refresh token, JavaScript’in okuyamadığı `HttpOnly`, `Secure` ve uygun `SameSite` ayarlarına sahip çerezde tutulmalıdır. Access token’ı `localStorage` içinde saklamak, bir XSS açığını doğrudan hesap ele geçirmeye dönüştürebilir. Çerez kullanıldığında ise CSRF koruması unutulmamalıdır.

Her token için `iss`, `aud`, `exp`, `nbf`, algoritma ve imza anahtarı doğrulanmalıdır. Sunucu, token başlığındaki algoritmayı körü körüne kabul etmemeli; izin verilen algoritmaları sabit bir listeyle sınırlandırmalıdır. Anahtar rotasyonu yapılırken eski anahtarlar yalnızca mevcut kısa ömürlü token’lar bitene kadar tutulmalıdır.

Son olarak parola değişikliği, şüpheli konum, cihaz kaybı veya yönetici müdahalesi bütün oturumları kapatabilmelidir. Kısa ömürlü JWT performans sağlar; sunucu taraflı oturum kaydı ise acil durum frenidir. Güvenli API, bu iki yaklaşımı rakip değil, birbirini tamamlayan katmanlar olarak kullanır.
