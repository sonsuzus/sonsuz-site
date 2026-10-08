---
layout: post
title: "Görsel Bulmacalar Olmadan CAPTCHA: ALTCHA, Friendly Captcha ve mCaptcha"
math: true
categories: 
  - Program
tags: 
  - captcha
  - altcha
  - friendly-captcha
  - mcaptcha
  - web-güvenliği
  - proof-of-work
toc: true
image: /img/gorsel-bulmacalar-olmadan-80.png
---

Trafik ışığı seçmekten motosiklet aramaya kadar klasik CAPTCHA’lar kullanıcıları küçük bir sınava sokar. ALTCHA, Friendly Captcha ve mCaptcha ise “İnsan olduğunu kanıtla” yaklaşımını tersine çevirir: Kullanıcı yerine tarayıcı, arka planda küçük bir hesaplama yapar. Böylece erişilebilirlik, gizlilik ve kullanıcı deneyimi açısından daha dost canlısı bir savunma katmanı ortaya çıkar.

``

## Temel fikir: Proof of Work

Bu sistemlerin merkezinde **iş ispatı** veya benzeri görünmez doğrulama mekanizmaları bulunur. Sunucu, istemciye çözülmesi ölçülü miktarda işlem gerektiren bir problem verir. Tarayıcı çözümü bulur; sunucu ise sonucu çok daha düşük maliyetle doğrular.

Basitleştirilmiş bir problem şöyle düşünülebilir:

$$H(\text{challenge} \parallel n) < T$$

Burada $H$ bir özet fonksiyonu, $n$ tarayıcının aradığı sayı ve $T$ zorluk eşiğidir. Eşik küçüldükçe uygun sayı bulmak zorlaşır. Ortalama hesaplama maliyeti yaklaşık olarak:

$$E[\text{deneme}] \approx \frac{2^b}{T}$$

şeklinde yorumlanabilir. Meşru bir kullanıcı için birkaç yüz milisaniyelik iş önemsizdir; milyonlarca sahte istek gönderen bot açısından aynı maliyet çarpılarak büyür. Yine de bu yöntem botları sihirli biçimde yok etmez, yalnızca saldırının ekonomisini bozar.

## Üç çözümün karşılaştırması

| Özellik | ALTCHA | Friendly Captcha | mCaptcha |
|---|---|---|---|
| Ana yaklaşım | Proof of Work tabanlı challenge | Arka planda kriptografik puzzle | Uyarlanabilir Proof of Work |
| Kullanıcı etkileşimi | Genellikle tek kutu veya görünmez akış | Çoğunlukla görünmez | Görünmez doğrulama |
| Self-hosting | Güçlü ve esnek | Ürüne/plana göre değerlendirilir | Temel odak noktalarından biri |
| Entegrasyon tarzı | Açık kaynak kütüphane ve widget | Yönetilen servis ve SDK’lar | Açık kaynak sunucu kurulumu |
| Uygun senaryo | Kontrol isteyen geliştiriciler | Hızlı SaaS entegrasyonu | Tam bağımsız altyapı isteyenler |

**ALTCHA**, sade protokolü ve self-hosting seçeneğiyle uygulama mimarisine kolayca yerleşir. **Friendly Captcha**, operasyon yükünü azaltmak isteyen ekipler için yönetilen hizmet deneyimine odaklanır. **mCaptcha** ise açık kaynaklı, bağımsız ve uyarlanabilir bir CAPTCHA altyapısı kurmak isteyenler açısından dikkat çekicidir.

## ALTCHA ile örnek sunucu akışı

Aşağıdaki Express örneği bir challenge üretir ve tarayıcıdan gelen çözümü doğrular:

```js
import express from "express";
import { createChallenge, verifySolution } from "altcha-lib";

const app = express();
app.use(express.json());

const hmacKey = process.env.ALTCHA_HMAC_KEY;

app.get("/captcha/challenge", async (req, res) => {
  const challenge = await createChallenge({
    hmacKey,
    maxNumber: 100000
  });

  res.json(challenge);
});

app.post("/contact", async (req, res) => {
  const valid = await verifySolution(req.body.altcha, hmacKey);

  if (!valid) {
    return res.status(400).json({ error: "CAPTCHA doğrulanamadı" });
  }

  res.json({ success: true });
});

app.listen(3000);
```

`maxNumber`, istemcinin yapabileceği maksimum arama miktarını sınırlar. HMAC anahtarı challenge’ın sunucu tarafından üretildiğini kanıtlar; bu anahtar istemciye kesinlikle gönderilmemelidir. Kullanılan kütüphane sürümüne göre fonksiyon imzalarının kontrol edilmesi de önemlidir.

## Hangisini seçmeli?

Hızlı entegrasyon ve yönetilen altyapı istiyorsanız Friendly Captcha pratik olabilir. Veriyi, anahtarları ve doğrulama sürecini kendi sisteminizde tutmak istiyorsanız ALTCHA daha hafif bir seçenek sunar. Tamamen açık kaynak bir CAPTCHA servisini bağımsız çalıştırmak ve iş yükünü dinamik ayarlamak istiyorsanız mCaptcha güçlü bir adaydır.

Hiçbiri tek başına yeterli savunma değildir. CAPTCHA’yı **rate limiting**, IP ve hesap bazlı kota, tekrar saldırısı engelleme, kısa challenge süresi ve davranışsal sinyallerle destekleyin. Mobil cihazlarda aşırı zorluk pil tüketebilir; çok düşük zorluk ise bot maliyetini artırmaz. En iyi ayar, güvenlik ile gerçek kullanıcıların bekleme süresi arasındaki dengedir.

![gorsel-bulmacalar-olmadan-80](/img/gorsel-bulmacalar-olmadan-80.svg)

