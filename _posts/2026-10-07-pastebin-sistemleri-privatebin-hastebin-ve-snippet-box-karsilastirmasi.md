---
layout: post
title: "Pastebin Sistemleri: PrivateBin, Hastebin ve Snippet Box Karşılaştırması"
math: true
categories: 
  - Proje
tags: 
  - pastebin
  - privatebin
  - hastebin
  - snippet-box
  - güvenlik
  - web-geliştirme
toc: true
image: /img/pastebin-sistemleri-privatebin-51.png
---

![pastebin-sistemleri-privatebin-51](/img/pastebin-sistemleri-privatebin-51.svg)


Kod, hata çıktısı veya kısa bir yapılandırma dosyası paylaşmak istediğinizde mesajlaşma uygulamasına yüzlerce satır yapıştırmak pek zarif değildir. Pastebin sistemleri, metni sunucuda saklayıp paylaşılabilir bir bağlantıya dönüştürür. Ancak PrivateBin, Hastebin ve Snippet Box aynı ihtiyacı farklı güvenlik, hız ve kullanım kolaylığı tercihleriyle çözer.

``

## Pastebin mantığı nasıl çalışır?

Temel bir pastebin uygulamasında istemci metni sunucuya gönderir. Sunucu içeriği bir kimlikle ilişkilendirerek veritabanına veya dosya sistemine kaydeder ve kullanıcıya `/abc123` benzeri bir adres döndürür. Bu yapı üç ana bileşenden oluşur:

1. Metni kabul eden bir HTTP API,
2. İçeriği saklayan depolama katmanı,
3. Paste'i görüntüleyen kullanıcı arayüzü.

Kimliklerin tahmin edilmesi istenmiyorsa yeterli rastgelelik kullanılmalıdır. $n$ karakterli ve her karakter için $a$ olasılıklı bir alfabenin teorik kombinasyon sayısı şöyledir:

$$N = a^n$$

Örneğin 62 karakterlik alfabeyle üretilen 10 karakterli bir kimlik, $62^{10}$ farklı olasılık sağlar. Yine de rastgele adresler, erişim kontrolünün yerine geçmez; yalnızca bağlantının keşfedilmesini zorlaştırır.

## Üç yaklaşımın karşılaştırması

| Sistem | Temel yaklaşım | Güçlü tarafı | Dikkat edilmesi gereken |
|---|---|---|---|
| PrivateBin | Tarayıcı tarafında şifreleme | Sunucu düz metni göremez | Bağlantı kaybolursa içerik kurtarılamaz |
| Hastebin | Hızlı ve sade paylaşım | Minimal arayüz ve kolay API | Varsayılan kurulumlar hassas veri için uygun olmayabilir |
| Snippet Box | Düzenli snippet yönetimi | Etiketleme ve kişisel arşiv | Kullanıcı hesabı ve yetkilendirme gerektirebilir |

**PrivateBin**, sıfır bilgi yaklaşımına yakın bir model kullanır. İçerik tarayıcıda şifrelenir; şifreleme anahtarı genellikle URL parçasında tutulur ve sunucuya gönderilmez. Sunucu yalnızca anlamsız şifreli veriyi saklar. Böylece sunucu yöneticisi bile içeriği doğrudan okuyamaz.

**Hastebin**, “yapıştır, kaydet, bağlantıyı al” felsefesine odaklanır. Kod paylaşımı ve terminal çıktıları için oldukça pratiktir. Basit mimarisi sayesinde ekip içi sunucuya kolayca kurulabilir. Fakat gizli anahtar, parola veya müşteri verisi paylaşılacaksa ek kimlik doğrulama ve şifreleme gerekir.

**Snippet Box** yaklaşımı ise geçici paylaşımdan çok kişisel kod arşivine yakındır. Başlıklar, etiketler, programlama dili seçimi ve arama özellikleri sayesinde tekrar kullanılan SQL sorguları, Docker komutları veya yapılandırma parçaları düzenli biçimde tutulabilir.

## Basit bir paste API'si

Aşağıdaki Express örneği, metni bellekte saklayan küçük bir servis oluşturur. `crypto.randomBytes`, tahmin edilmesi zor kimlik üretir; süre dolduğunda paste otomatik olarak silinir.

```js
import express from "express";
import crypto from "crypto";

const app = express();
const pastes = new Map();

app.use(express.json({ limit: "100kb" }));

app.post("/pastes", (req, res) => {
  const text = String(req.body.text ?? "");
  const ttl = Math.min(req.body.ttl ?? 3600, 86400);

  if (!text.trim()) {
    return res.status(400).json({ error: "Metin gerekli" });
  }

  const id = crypto.randomBytes(8).toString("hex");
  pastes.set(id, { text, expiresAt: Date.now() + ttl * 1000 });

  setTimeout(() => pastes.delete(id), ttl * 1000);
  res.status(201).json({ url: `/pastes/${id}` });
});

app.get("/pastes/:id", (req, res) => {
  const paste = pastes.get(req.params.id);
  if (!paste || paste.expiresAt < Date.now()) {
    return res.sendStatus(404);
  }
  res.type("text/plain").send(paste.text);
});

app.listen(3000);
```

Bu örnek öğreticidir; üretimde Redis veya PostgreSQL, hız sınırlama, içerik boyutu denetimi, güvenli başlıklar ve kötüye kullanım bildirimi eklenmelidir. Bellek içi kayıtlar uygulama yeniden başladığında kaybolur.

## Hangisini seçmelisiniz?

Hassas ve geçici metinler için **PrivateBin**, hızlı ekip içi kod paylaşımı için **Hastebin**, uzun vadeli ve aranabilir kişisel koleksiyonlar için **Snippet Box** daha uygundur. Ayrıca tek kullanımlık görüntüleme ve otomatik silme seçenekleri riski azaltır. Kısacası en iyi sistem, en çok özelliği sunan değil; verinin gizlilik düzeyine ve yaşam süresine en doğru cevabı verendir.
