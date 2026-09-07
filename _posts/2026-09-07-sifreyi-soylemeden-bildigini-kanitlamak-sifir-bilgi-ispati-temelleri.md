---
layout: post
title: "Şifreyi Söylemeden Bildiğini Kanıtlamak: Sıfır Bilgi İspatı Temelleri"
math: true
categories: 
  - Bilgi
tags: 
  - sıfır bilgi ispatı
  - kriptografi
  - kimlik doğrulama
toc: true
---

Bir kapının önündesiniz ve içerideki görevliye gizli parolayı bildiğinizi kanıtlamanız gerekiyor. Ancak parolayı söylerseniz görevli de onu öğrenmiş olacak! Sıfır Bilgi İspatı, yani **Zero-Knowledge Proof (ZKP)**, tam olarak bu bilmeceyi matematik yardımıyla çözer: Gizli bilginin kendisini paylaşmadan ona sahip olduğunuzu kanıtlarsınız.
``
## Sıfır bilgi ne anlama gelir?

Bir ZKP protokolünde iki taraf bulunur:

- **Kanıtlayıcı (Prover):** Gizli bilgiyi bildiğini iddia eder.
- **Doğrulayıcı (Verifier):** Bu iddiayı kontrol eder.

Başarılı bir protokol üç temel özelliğe sahip olmalıdır:

| Özellik | Anlamı | Basit yorum |
|---|---|---|
| Tamlık | Dürüst kanıtlayıcı kabul edilir | Şifre doğruysa kapı açılır |
| Sağlamlık | Sahtekârın başarı ihtimali çok düşüktür | Bilmeyen kişi kolayca blöf yapamaz |
| Sıfır bilgi | Gizli veri hakkında ek bilgi sızmaz | Kapı açılır ama şifre duyulmaz |

Buradaki “sıfır”, iletişim kurulmadığı anlamına gelmez. Doğrulayıcı bir **transkript** görür; fakat bu transkript, gizli anahtarı öğrenmesine yardımcı olmamalıdır.

## Schnorr protokolüyle matematiksel sezgi

Klasik bir örnek olan Schnorr kimlik doğrulamasında büyük bir asal mertebeli grup seçilir. $g$ grubun üreteci, $q$ grup mertebesi ve $x$ gizli anahtar olsun. Sunucu yalnızca şu açık değeri bilir:

$$y = g^x$$

Kanıtlayıcı rastgele bir $r$ seçip $t=g^r$ değerini gönderir. Sunucu rastgele bir meydan okuma $c$ üretir. Kanıtlayıcı ise şu yanıtı hesaplar:

$$s = r + cx \pmod q$$

Sunucu aşağıdaki eşitliği kontrol eder:

$$g^s \stackrel{?}{=} t\cdot y^c$$

Eşitliğin çalışması tesadüf değildir:

$$g^s=g^{r+cx}=g^r(g^x)^c=t\cdot y^c$$

Gizli $x$ hiç gönderilmediği hâlde doğru yanıt üretmek için ona ihtiyaç vardır. Her oturumda yeni $r$ kullanılması kritiktir; aynı rastgele değer tekrar kullanılırsa iki farklı yanıttan gizli anahtar hesaplanabilir.

## Oyuncak bir Python gösterimi

Aşağıdaki kod gerçek güvenlik sağlamayan küçük sayılarla protokol akışını gösterir:

```python
import secrets

p, q, g = 23, 11, 2       # g, q mertebeli alt grubun üreteci
x = 7                      # Kanıtlayıcının gizli anahtarı
y = pow(g, x, p)           # Sunucunun sakladığı açık değer

r = secrets.randbelow(q)   # Her oturum için yeni rastgele sayı
t = pow(g, r, p)           # Taahhüt

c = secrets.randbelow(q)   # Sunucunun meydan okuması
s = (r + c * x) % q        # Kanıtlayıcının yanıtı

left = pow(g, s, p)
right = (t * pow(y, c, p)) % p
print("Kanıt geçerli mi?", left == right)
```

Gerçek sistemlerde yüzlerce bitlik güvenli gruplar, standart eğriler ve dikkatle incelenmiş kütüphaneler kullanılır. Kriptografiyi üretim ortamında “kendin yazmak”, yangın tüpünü kartondan yapmak gibidir.

## Peki şifre doğrudan $x$ olabilir mi?

Kısa cevap: Olmamalı. İnsan şifreleri düşük entropilidir. Sunucuda $y=g^x$ tutulursa saldırgan olası şifreleri deneyip karşılık gelen açık değerleri karşılaştırabilir. Bu, çevrimdışı sözlük saldırısına dönüşür.

| Yaklaşım | Risk | Daha doğru seçenek |
|---|---|---|
| Şifreyi sunucuya gönderme | Ağ veya sunucu sızıntısı | Güvenli kimlik doğrulama protokolü |
| Şifreyi doğrudan üs yapma | Sözlük saldırısı | KDF ve özel protokol |
| Ev yapımı ZKP | Uygulama hataları | Denetlenmiş standartlar |

Parola tabanlı uygulamalarda **OPAQUE** gibi artırılmış PAKE protokolleri tercih edilir. ZKP’ler ayrıca anonim kimlik, blokzincir gizliliği ve yaşın 18’den büyük olduğunu doğum tarihini açıklamadan kanıtlama gibi alanlarda kullanılır. Ana fikir büyülüdür ama sihir değildir: Bilginin kendisini değil, yalnızca onunla üretilebilecek matematiksel bir kanıtı paylaşırsınız.
