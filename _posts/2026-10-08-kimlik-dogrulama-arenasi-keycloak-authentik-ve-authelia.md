---
layout: post
title: "Kimlik Doğrulama Arenası: Keycloak, Authentik ve Authelia"
math: true
categories: 
  - Bilgi
tags: 
  - kimlik doğrulama
  - keycloak
  - authentik
  - authelia
  - openid connect
  - siber güvenlik
toc: true
image: /img/kimlik-dogrulama-arenasi-17.png
---

Birden fazla uygulama kullanan ekiplerde her servis için ayrı kullanıcı adı ve parola yönetmek kısa sürede dijital bir anahtarlık kâbusuna dönüşür. Keycloak, Authentik ve Authelia bu sorunu merkezi kimlik doğrulama, tek oturum açma ve erişim politikalarıyla çözer. Ancak üçü de aynı kapıyı korusa da farklı anahtarlar ve farklı güvenlik yaklaşımları kullanır.

![kimlik-dogrulama-arenasi-17](/img/kimlik-dogrulama-arenasi-17.svg)

``
## Önce temel kavramlar

**Kimlik doğrulama** (authentication), kullanıcının kim olduğunu kanıtlamasıdır. **Yetkilendirme** (authorization) ise doğrulanan kullanıcının hangi kaynaklara erişebileceğini belirler. Kısaca ilk soru “Sen kimsin?”, ikinci soru “Burada ne yapabilirsin?” şeklindedir.

Modern sistemlerde parola her uygulamaya gönderilmez. Kullanıcı bir **Kimlik Sağlayıcıya** (Identity Provider veya IdP) yönlendirilir. Başarılı girişten sonra uygulamaya imzalı bir token verilir. Basitleştirilmiş güven modeli şöyle ifade edilebilir:

$$
Güven = Kimlik\ Doğrulama + Token\ Bütünlüğü + Erişim\ Politikası
$$

Token içinde kullanıcı kimliği, roller ve geçerlilik süresi gibi talepler bulunur. Bir tokenın kullanılabilirliği kabaca şu koşula bağlıdır:

$$
Geçerli = İmzaDoğru \land (şimdi < sonKullanma) \land doğruHedef
$$

OpenID Connect (OIDC) kimlik bilgisini OAuth 2.0 üzerine ekler. SAML daha çok kurumsal ve eski sistemlerde görülürken LDAP merkezi kullanıcı dizini görevi üstlenir.

## Üç adayın karşılaştırması

| Özellik | Keycloak | Authentik | Authelia |
|---|---|---|---|
| Temel rol | Tam kapsamlı IdP | Modern ve görsel IdP | Ters proxy odaklı erişim katmanı |
| OIDC / OAuth 2.0 | Çok güçlü | Güçlü | Destekliyor |
| SAML | Gelişmiş | Destekliyor | Sınırlı senaryolar |
| Yönetim arayüzü | Ayrıntılı fakat yoğun | Kullanıcı dostu | Yapılandırma dosyası ağırlıklı |
| Kaynak ihtiyacı | Görece yüksek | Orta | Düşük |
| İdeal kullanım | Kurumsal sistemler | Self-hosted ve orta ölçek | Mevcut web servislerini koruma |

**Keycloak**, realm, client, rol, grup ve identity brokering özellikleriyle adeta kimlik yönetiminin İsviçre çakısıdır. Büyük organizasyonlar ve karmaşık rol modelleri için güçlüdür; buna karşılık kurulumu ve işletimi daha fazla dikkat ister.

**Authentik**, akış tabanlı yaklaşımı ve modern arayüzüyle daha yumuşak bir öğrenme eğrisi sunar. OIDC, SAML, LDAP ve proxy provider seçeneklerini aynı merkezde toplar. Ev laboratuvarları ile büyüyen ekipler arasında güzel bir köprü kurar.

**Authelia** ise özellikle Nginx, Traefik veya Caddy arkasındaki uygulamalara giriş ekranı ve çok faktörlü doğrulama eklemek için hafif bir çözümdür. Tam teşekküllü kurumsal IdP yerine güvenlik kapısı gibi düşünülmelidir.

## Basit bir OIDC istemcisi

Bir uygulamanın sağlayıcıyı keşfetmesi çoğunlukla standart bir adres üzerinden gerçekleşir:

```javascript
const issuer = "https://kimlik.example.com/realms/ekip";

const oidcConfig = {
  authority: issuer,
  client_id: "blog-paneli",
  redirect_uri: "https://panel.example.com/callback",
  response_type: "code",
  scope: "openid profile email"
};
```

Bu yapılandırma uygulamanın hangi IdP’ye bağlanacağını, dönüş adresini ve talep ettiği kullanıcı bilgilerini belirtir. `authorization code` akışı kullanılmalı; tarayıcı tabanlı istemcilerde ayrıca **PKCE** etkinleştirilmelidir. Böylece ele geçirilen yetkilendirme kodunun başka bir istemci tarafından kullanılması zorlaşır.

## Güvenli kurulum kontrol listesi

- Yönetici hesabında çok faktörlü doğrulamayı etkinleştirin.
- Yalnızca HTTPS kullanın ve yönlendirme adreslerini kesin tanımlayın.
- Token ömrünü gereksiz yere uzun tutmayın.
- Servis hesaplarına en az ayrıcalık ilkesini uygulayın.
- Veritabanı, anahtarlar ve yapılandırmalar için düzenli yedek alın.
- Giriş denemelerini ve yönetici işlemlerini merkezi olarak kaydedin.

Sonuç olarak karmaşık kurumsal federasyon için **Keycloak**, modern arayüz ve esnek self-hosted deneyim için **Authentik**, ters proxy arkasındaki servisleri hızlıca korumak için **Authelia** öne çıkar. En iyi ürün, en uzun özellik listesine sahip olan değil; ekibinizin güvenle işletebildiği ve düzenli güncelleyebildiği üründür.
