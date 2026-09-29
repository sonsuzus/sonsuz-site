---
layout: post
title: "JWT Zafiyetleri: Algoritma Karmaşasından İmza Sahteciliğine"
math: true
categories: 
  - Bilgi
tags: 
  - jwt
  - web güvenliği
  - kimlik doğrulama
  - yetkilendirme
  - node.js
  - siber güvenlik
toc: true
image: /img/jwt-zafiyetleri-algoritma-49.png
---

JWT, kullanıcı oturumunu sunucuda saklamadan kimlik ve yetki bilgilerini taşıyabilen popüler bir standarttır. Ancak “durumsuz” olması, “kontrolsüz” olabileceği anlamına gelmez. Algoritma seçiminin istemciye bırakılması, imzasız token kabul edilmesi veya tahmin edilebilir gizli anahtar kullanılması; saldırganın başka bir kullanıcıya, hatta yöneticiye dönüşmesine yol açabilir.


![jwt-zafiyetleri-algoritma-49](/img/jwt-zafiyetleri-algoritma-49.svg)

``

## JWT gerçekte neyi garanti eder?

Bir JWT üç bölümden oluşur: `header.payload.signature`. Header kullanılan algoritmayı, payload ise `sub`, `role` ve `exp` gibi iddiaları taşır. Bu iki bölüm şifrelenmiş değildir; yalnızca Base64URL ile kodlanır. Dolayısıyla token içindeki bilgiler okunabilir.

İmza genel olarak şöyle modellenebilir:

$$S = Sign(K, Base64Url(H) + "." + Base64Url(P))$$

Burada $K$ anahtar, $H$ header ve $P$ payload’dur. Sunucu imzayı doğrulamadan payload’a güvenirse JWT, dijital kimlik kartı olmaktan çıkıp herkesin düzenleyebildiği bir not kâğıdına dönüşür.

| Özellik | Güvenli yaklaşım | Tehlikeli yaklaşım |
|---|---|---|
| Algoritma | Sunucu tarafından sabitlenir | Token header’ından körlemesine alınır |
| İmza | Her istekte doğrulanır | Sadece payload çözümlenir |
| Gizli anahtar | Uzun ve rastgele üretilir | Sözlük kelimesi kullanılır |
| Süre | Kısa `exp` değeri uygulanır | Süresiz token verilir |
| Anahtar yönetimi | Kasada tutulur ve döndürülür | Kaynak koda yazılır |

## `none` algoritması: İmza yoksa güven de yok

JWT standardında `alg: none`, imzasız token gerektiren sınırlı senaryolar için tanımlanmıştır. Geçmişte bazı kütüphaneler header içinde `none` gördüğünde doğrulamayı atlayabiliyordu. Saldırgan payload’daki `role` alanını değiştirip boş imzalı bir token gönderdiğinde uygulama bunu geçerli kabul edebiliyordu.

Sorun standardın varlığından çok, doğrulayıcının algoritma kararını güvenilmeyen token’a bırakmasıdır. Uygulama yalnızca önceden belirlediği algoritmaları kabul etmeli ve imzasız token’ları açıkça reddetmelidir.

## HS256 ve RS256 algoritma karmaşası

HS256 simetriktir: üretim ve doğrulama aynı gizli anahtarla yapılır. RS256 ise asimetriktir; özel anahtar imzalar, herkese açık anahtar doğrular.

| Algoritma | İmzalama | Doğrulama |
|---|---|---|
| HS256 | Gizli anahtar | Aynı gizli anahtar |
| RS256 | Özel anahtar | Açık anahtar |

Hatalı bir doğrulayıcı hem HS256 hem RS256 kabul eder ve anahtar türünü denetlemezse, RS256 açık anahtarını HS256 gizli anahtarı gibi yorumlayabilir. Böylece normalde yalnızca doğrulama için kullanılan açık veri, sahte imza üretiminde kullanılabilir. Savunma basittir: algoritmayı yapılandırmada sabitlemek, anahtar türünü doğrulamak ve farklı algoritmalar için ayrı doğrulama yolları kullanmak.

## Zayıf gizli anahtarlar

HS256 güvenliği gizli anahtarın tahmin edilememesine bağlıdır. `secret`, şirket adı veya kısa parola gibi anahtarlar çevrimdışı sözlük saldırılarıyla bulunabilir. Saniyede $R$ deneme yapılabiliyor ve anahtarın entropisi $H$ bit ise ortalama arama süresi kabaca:

$$T = 2^{H-1} / R$$

Bu nedenle yüksek entropili, kriptografik olarak rastgele üretilmiş anahtarlar kullanılmalıdır. Anahtarın sürüm kontrolüne eklenmesi de güçlü olmasını anlamsızlaştırır.

Aşağıdaki Node.js örneği, `jose` ile algoritmayı sabitleyerek token doğrular:

```js
import { jwtVerify } from "jose";

const secret = new TextEncoder().encode(process.env.JWT_SECRET);

export async function verifyAccessToken(token) {
  const { payload, protectedHeader } = await jwtVerify(token, secret, {
    algorithms: ["HS256"],
    issuer: "https://auth.example.com",
    audience: "api.example.com"
  });

  if (protectedHeader.alg !== "HS256") {
    throw new Error("Beklenmeyen JWT algoritması");
  }

  return payload;
}
```

Bu kod yalnızca imzayı değil, algoritma, issuer, audience ve süre iddialarını da denetler. Üretimde ayrıca kısa ömürlü erişim token’ları, güvenli yenileme token’ları, anahtar rotasyonu, `kid` değerinin kontrollü işlenmesi ve token iptal stratejileri kullanılmalıdır. JWT kullanmak güvenliği otomatikleştirmez; güvenlik, doğrulama politikasının ne kadar katı olduğuyla belirlenir.
