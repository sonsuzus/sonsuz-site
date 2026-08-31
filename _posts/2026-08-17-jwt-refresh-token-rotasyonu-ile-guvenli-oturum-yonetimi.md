---
layout: post
title: "JWT Refresh Token Rotasyonu ile Güvenli Oturum Yönetimi"
math: true
categories: 
  - Bilgi
tags: 
  - jwt
  - refresh token
  - kimlik doğrulama
image: /img/jwt-refresh-token-38.png
---

JWT tabanlı kimlik doğrulama, stateless yapısı sayesinde ölçeklenebilir uygulamalarda oldukça popülerdir; ancak token çalınması, uzun oturumlar ve cihaz yönetimi gibi konular dikkatli tasarlanmadığında ciddi güvenlik açıkları doğurur. Bu noktada **kısa ömürlü access token** ve **rotasyona tabi refresh token** ikilisi, hem kullanıcı deneyimini hem de güvenlik seviyesini dengeler.
``

Temel fikir basittir: Access token, API çağrılarında kullanılan ve kısa süre geçerli olan JWT'dir. Refresh token ise access token süresi dolduğunda yeni bir ikili üretmek için kullanılır. Rotasyon stratejisinde her başarılı yenileme isteğinde eski refresh token geçersiz yapılır ve istemciye yeni bir refresh token verilir. Böylece ele geçirilmiş eski bir token'ın tekrar kullanılması saldırı sinyaline dönüşür.

Token sürelerini düşünürken güvenlik penceresini kabaca şu şekilde ifade edebiliriz:

$$Risk\ Penceresi \approx Token\ Yaşam\ Süresi \times Ele\ Geçirilme\ Olasılığı$$

Access token yaşam süresini kısa tutmak riski azaltır, fakat yenileme trafiğini artırır. Refresh token'ın daha uzun yaşaması kullanıcıyı sürekli yeniden girişten kurtarır; buna karşılık mutlaka sunucu tarafında izlenmeli ve iptal edilebilmelidir.

| Özellik | Access Token | Refresh Token |
|---|---|---|
| Ana kullanım | API yetkilendirmesi | Yeni token üretimi |
| Önerilen ömür | 5-15 dakika | Günler veya haftalar |
| Gönderim sıklığı | Her korumalı istek | Yalnızca yenileme isteği |
| Saklama yaklaşımı | Bellek, mümkünse kalıcı olmayan alan | `HttpOnly`, `Secure` cookie |
| Sunucuda takip | İsteğe bağlı | Kesinlikle önerilir |

## Rotasyonun güvenlik mantığı

Her refresh token için veritabanında bir kayıt veya oturum ailesi (*token family*) tutulabilir. Kayıtta token'ın hash'i, kullanıcı kimliği, cihaz bilgisi, son kullanma zamanı, oluşturulma zamanı ve varsa önceki token ilişkisi bulunur. Ham refresh token'ı veritabanına yazmak yerine parola saklar gibi hash'lemek kritik bir ayrıntıdır.

Yenileme akışı şöyledir:

1. İstemci `/auth/refresh` rotasına refresh token'ı gönderir.
2. Sunucu token hash'ini bulur, süresini ve iptal durumunu denetler.
3. Token geçerliyse eskisi `used` veya `revoked` olarak işaretlenir.
4. Yeni access token ve yeni refresh token oluşturulur.
5. Yeni refresh token aynı oturum ailesine bağlanarak kaydedilir.

Aynı eski refresh token yeniden gelirse bu durum **reuse detection** olarak değerlendirilir. Saldırgan mı yoksa kullanıcının iki sekmesi mi istek attı? Kesin cevap her zaman yoktur; yine de güvenli varsayım, ilgili token ailesindeki tüm oturumları iptal etmektir. Kullanıcı tekrar giriş yapar, saldırganın elindeki token da işe yaramaz.

```ts
async function rotateRefreshToken(rawToken: string) {
  const tokenHash = sha256(rawToken);
  const session = await sessions.findByTokenHash(tokenHash);

  if (!session || session.expiresAt < new Date()) {
    throw new UnauthorizedError("Geçersiz veya süresi dolmuş refresh token");
  }

  if (session.revokedAt) {
    await sessions.revokeFamily(session.familyId);
    throw new UnauthorizedError("Token tekrar kullanıldı; oturum kapatıldı");
  }

  await sessions.revoke(session.id);
  const refreshToken = crypto.randomUUID() + "." + crypto.randomUUID();
  await sessions.create({
    userId: session.userId,
    familyId: session.familyId,
    tokenHash: sha256(refreshToken),
    expiresAt: addDays(new Date(), 14)
  });

  return { accessToken: signAccessToken(session.userId), refreshToken };
}
```

Bu örnekte refresh token JWT olmak zorunda değildir; yüksek entropili rastgele, opak bir değer çoğu zaman daha iyi bir tercihtir. Çünkü sunucu oturum durumunu zaten veritabanından kontrol eder.

| Strateji | Avantaj | Risk / Maliyet |
|---|---|---|
| Sabit refresh token | Uygulaması kolay | Çalınırsa uzun süre kullanılabilir |
| Refresh token rotasyonu | Tekrar kullanımı algılar | Veri tabanı ve yarış durumu yönetimi gerekir |
| Tam stateless JWT | Hızlı doğrulama | Anlık iptal ve cihaz kontrolü zordur |

Son olarak cookie kullanılıyorsa `HttpOnly`, `Secure`, uygun `SameSite` politikası ve CSRF önlemi uygulanmalıdır. Mobil istemcilerde token'ı işletim sisteminin güvenli depolama alanında saklamak gerekir. Rotasyon, tek başına sihirli bir kalkan değildir; kısa access token ömrü, oturum iptali, cihaz görünürlüğü, hız sınırlama ve ayrıntılı güvenlik kayıtlarıyla birleştiğinde sağlam bir oturum mimarisine dönüşür.

![jwt-refresh-token-38](/img/jwt-refresh-token-38.svg)

