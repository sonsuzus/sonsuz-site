---
layout: post
title: "Kimlik Doğrulamada FIDO2 ve WebAuthn: Parolasız Geleceğin Altyapısı"
math: true
categories: 
  - Bilgi
tags: 
  - fido2
  - webauthn
  - siber güvenlik
  - parolasız giriş
  - kriptografi
  - javascript
toc: true
image: /img/kimlik-dogrulamada-fido2-16.png
---

Parolalar uzun yıllardır dijital dünyanın kapı anahtarlarıydı; ne var ki unutuluyor, tekrar kullanılıyor, oltalama sitelerine yazılıyor ve veri tabanlarından çalınıyorlar. FIDO2 ve WebAuthn ise kullanıcıdan ezberlenebilir bir sır istemek yerine cihazdaki güvenli donanımı ve açık anahtarlı kriptografiyi kullanıyor. Böylece parmak izi, yüz tanıma veya PIN ile onaylanan giriş işlemi sırasında sunucuya biyometrik veri değil, alan adına bağlı kriptografik bir kanıt gönderiliyor.
``

## FIDO2 hangi parçalardan oluşur?

FIDO2, tek bir protokolün adı olmaktan çok iki temel bileşenin oluşturduğu bir ekosistemdir:

- **WebAuthn:** Tarayıcı ile web uygulaması arasındaki standart JavaScript API’sidir.
- **CTAP2:** Bilgisayar veya telefon ile güvenlik anahtarı gibi harici bir doğrulayıcı arasındaki iletişimi tanımlar.

Doğrulayıcı, cihazın güvenli çipi, telefonun ekran kilidi altyapısı veya USB/NFC güvenlik anahtarı olabilir. Parmak izi burada özel anahtarın kullanılmasına izin veren yerel kilittir. Biyometrik şablon normal şartlarda cihazdan çıkmaz.

| Özellik | Parola | FIDO2/WebAuthn |
|---|---|---|
| Sunucuda tutulan veri | Parola özeti | Açık anahtar |
| Kullanıcının hatırladığı sır | Gerekli | Genellikle gereksiz |
| Oltalama direnci | Düşük | Yüksek, alan adına bağlı |
| Veri sızıntısının etkisi | Çevrimdışı tahmin mümkün | Açık anahtar tek başına kullanılamaz |
| Giriş kanıtı | Paylaşılan sır | Sayısal imza |

## Kayıt töreni nasıl çalışır?

Sunucu önce rastgele ve tek kullanımlık bir `challenge` üretir. Tarayıcı bunu doğrulayıcıya iletir. Doğrulayıcı, ilgili siteyi temsil eden RP kimliği için yeni bir anahtar çifti oluşturur:

$$K_{özel} \rightarrow \text{cihazda kalır}, \qquad K_{açık} \rightarrow \text{sunucuya gider}$$

Sunucu açık anahtarı kullanıcı hesabıyla ilişkilendirir. Özel anahtar dışarı aktarılmadığı için sunucu veri tabanı ele geçirilse bile saldırgan giriş imzası üretemez. Attestation adı verilen isteğe bağlı mekanizma, anahtarın hangi doğrulayıcı türünde üretildiği hakkında ayrıca kanıt sağlayabilir; ancak gizlilik gereksinimleri nedeniyle her projede zorunlu tutulmaz.

Tarayıcı tarafında kayıt isteği kabaca şöyledir:

```javascript
const credential = await navigator.credentials.create({
  publicKey: {
    challenge: challengeFromServer,
    rp: { name: "Örnek Uygulama", id: "example.com" },
    user: {
      id: userIdBytes,
      name: "ada@example.com",
      displayName: "Ada"
    },
    pubKeyCredParams: [{ type: "public-key", alg: -7 }],
    authenticatorSelection: {
      residentKey: "preferred",
      userVerification: "required"
    }
  }
});
```

Bu kod anahtarı doğrudan üretmez; işlemi tarayıcı ve doğrulayıcıya devreder. Gerçek uygulamada ikili alanlar Base64URL biçimine dönüştürülerek sunucuya gönderilir ve kayıt yanıtı mutlaka sunucuda doğrulanır.

## Giriş sırasında ne imzalanır?

Girişte sunucu yeni bir challenge yollar. Doğrulayıcı kullanıcı onayından sonra challenge, origin ve diğer bağlam verilerini kapsayan içeriği özel anahtarla imzalar:

$$\sigma = \operatorname{Sign}_{K_{özel}}(H(\text{authenticatorData} \parallel \text{clientDataJSON}))$$

Sunucu da kayıtlı açık anahtarla $\operatorname{Verify}_{K_{açık}}(m,\sigma)$ işlemini gerçekleştirir. Challenge’ın tek kullanımlık olması tekrar saldırılarını; origin ve RP ID denetimleri ise kimlik avını engellemeye yardımcı olur. Sahte site, gerçek alan adına bağlı anahtardan geçerli imza isteyemez.

```javascript
const assertion = await navigator.credentials.get({
  publicKey: {
    challenge: challengeFromServer,
    rpId: "example.com",
    userVerification: "required"
  }
});
```

Sunucu; challenge, origin, RP ID özeti, imza ve kullanıcı doğrulama bayraklarını kontrol etmelidir. Yalnızca tarayıcıdan “başarılı” yanıt gelmesine güvenmek ciddi bir güvenlik hatasıdır.

## Passkey bunun neresinde?

Passkey, WebAuthn kimlik bilgilerinin kullanıcı dostu ve gerektiğinde uçtan uca şifreli biçimde cihazlar arasında eşitlenebilen yorumudur. Cihaz kaybına karşı kurtarma kolaylığı sağlar. Yine de hesap kurtarma kanalları, oturum çerezleri ve sunucu güvenliği saldırıya açık kalabilir. FIDO2 sihirli değnek değildir; fakat parolayı ve oltalanabilir paylaşılan sır modelini ortadan kaldırarak kimlik doğrulamanın en kırılgan halkasını güçlü biçimde değiştirir.

![kimlik-dogrulamada-fido2-16](/img/kimlik-dogrulamada-fido2-16.svg)

