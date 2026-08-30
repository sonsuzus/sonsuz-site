---
layout: post
title: "OAuth 2.0 Akışı: Modern Yetkilendirmenin Perde Arkası"
math: true
categories: 
  - Bilgi
tags: 
  - oauth 2.0
  - kimlik doğrulama
  - apı güvenliği
---

Bir uygulamanın kullanıcı parolasını hiç görmeden Google Drive dosyalarına erişebilmesi nasıl mümkün olur? OAuth 2.0, tam da bu problemi çözen bir **yetkilendirme çerçevesidir**. Kullanıcı, bir uygulamaya belirli ve sınırlı izinler verir; uygulama ise bu izinleri temsil eden token'larla API çağrıları yapar. Böylece parola paylaşımı yerine kontrollü, süreli ve gerektiğinde geri alınabilir erişim sağlanır.

``

Önce önemli bir ayrımı netleştirelim: OAuth 2.0 tek başına bir **kimlik doğrulama (authentication)** protokolü değildir. Yani teorik olarak “Bu kullanıcı gerçekten Ayşe mi?” sorusunu çözmekten çok, “Bu uygulama Ayşe adına hangi kaynağa ne kadar süreyle erişebilir?” sorusuna odaklanır. Kullanıcı bilgilerini standart biçimde almak için OAuth 2.0 üzerine kurulu **OpenID Connect (OIDC)** tercih edilir.

| Kavram | Sorduğu soru | Örnek |
|---|---|---|
| Authentication | Sen kimsin? | Kullanıcının Google hesabıyla oturum açması |
| Authorization | Ne yapabilirsin? | Uygulamanın takvimi okuyabilmesi |
| OAuth 2.0 | İzni nasıl devrederiz? | Uygulamaya sınırlı erişim token'ı verme |
| OpenID Connect | Kimlik bilgisini nasıl taşırız? | `id_token` ile kullanıcı kimliği alma |

OAuth evreninde dört temel oyuncu vardır: **Resource Owner** kullanıcıdır; **Client** erişim isteyen uygulamadır; **Authorization Server** kullanıcının iznini alıp token üretir; **Resource Server** ise korunmuş API'yi barındırır. Örneğin bir takvim uygulamasında kullanıcı kaynak sahibidir, mobil uygulama client'tır, Google yetkilendirme sunucusudur ve Google Calendar API kaynak sunucusudur.

En güvenli ve güncel tarayıcı/mobil senaryolarında kullanılan yöntem **Authorization Code Flow with PKCE** akışıdır. Adımlar şöyledir:

1. Uygulama rastgele bir `state`, `code_verifier` ve bunun özetinden oluşan `code_challenge` üretir.
2. Kullanıcı, yetkilendirme sunucusunun giriş ve izin ekranına yönlendirilir.
3. Kullanıcı istenen kapsamları (`scope`) onaylar.
4. Sunucu uygulamanın geri dönüş adresine kısa ömürlü bir `authorization_code` gönderir.
5. Uygulama bu kodu, `code_verifier` ile birlikte token uç noktasına iletir.
6. Sunucu doğrulama sonrası `access_token`, gerekirse `refresh_token` ve OIDC kullanılıyorsa `id_token` döner.

PKCE'nin mantığı basit ama güçlüdür. Saldırgan yönlendirme sırasında authorization code'u ele geçirse bile gizli doğrulayıcıyı bilmeden token alamaz. Özet ilişkiyi şöyle düşünebiliriz:

$$code\_challenge = BASE64URL(SHA256(code\_verifier))$$

`state` parametresi ise CSRF saldırılarına karşı istemci tarafından üretilen ve dönüşte doğrulanan bir bağlam değeridir. Bu iki parametre “küçük ayrıntı” değil, akışın güvenlik kemeridir.

Aşağıdaki örnek, kullanıcıyı yetkilendirme ekranına göndermek için JavaScript ile URL üretir:

```javascript
const params = new URLSearchParams({
  response_type: "code",
  client_id: "calendar-web-client",
  redirect_uri: "https://app.example.com/callback",
  scope: "openid profile calendar.readonly",
  state: crypto.randomUUID(),
  code_challenge: generatedChallenge,
  code_challenge_method: "S256"
});

window.location.href = `https://auth.example.com/authorize?${params}`;
```

Bu kodun görevi token almak değil, kullanıcıyı güvenilir yetkilendirme sunucusuna yönlendirmektir. Dönüşte gelen `code`, tarayıcıda uzun süre saklanmamalı; mümkünse sunucu tarafında token ile değiştirilmelidir.

Token'ların ömrü ve kapsamı güvenlik dengesini belirler. Risk kabaca token gücü, kapsamı ve geçerlilik süresiyle artar: $Risk \propto Scope \times Lifetime$. Bu nedenle `calendar.readonly` gibi en dar kapsamları istemek, saatlerce yaşayan access token'lar yerine kısa ömürlü token kullanmak gerekir.

| Token türü | Amaç | Güvenlik notu |
|---|---|---|
| Access Token | API çağrısı yapmak | Kısa ömürlü tutulmalıdır |
| Refresh Token | Yeni access token almak | Çok dikkatli saklanmalıdır |
| ID Token | Kullanıcı kimliği bilgisini taşımak | API erişimi için kullanılmamalıdır |

Son olarak, `redirect_uri` değerini tam eşleşmeyle doğrulayın, token'ları URL sorgu parametrelerine koymayın, HTTPS zorunlu kullanın ve erişim token'ını JWT diye körü körüne güvenilir kabul etmeyin. OAuth 2.0 doğru kurulduğunda kullanıcı deneyimini kolaylaştırır; yanlış kurulduğunda ise anahtarı kapının üzerinde bırakmaya benzer.
