---
layout: post
title: "Flarum İçin Kapsamlı SEO: JavaScript Tabanlı Forum İçeriklerini Eksiksiz İndeksletme"
math: true
categories: 
  - Bilgi
tags: 
  - flarum
  - seo
  - javascript
toc: true
---

Flarum hızlı, modern ve kullanıcı dostu bir forum altyapısıdır; ancak JavaScript ağırlıklı çalışma modeli SEO tarafında bazı soru işaretleri oluşturabilir. Arama motoru botu sayfaya geldiğinde yalnızca boş bir uygulama kabuğu görüyorsa tartışmalarınız, kullanıcı yanıtları ve kategori açıklamalarınız indekslenmeden kalabilir. Neyse ki sunucu tarafı çıktı, doğru meta etiketleri ve kontrollü ön oluşturma stratejileriyle botlara eksiksiz içerik sunmak mümkündür.

``

## JavaScript tabanlı indeksleme nasıl çalışır?

Googlebot gibi gelişmiş tarayıcılar JavaScript çalıştırabilir; fakat tarama ve render işlemleri çoğunlukla iki aşamalıdır. İlk aşamada sunucunun döndürdüğü HTML incelenir, ikinci aşamada sayfa render kuyruğuna alınarak JavaScript çalıştırılır. Bu gecikme, özellikle binlerce tartışmaya sahip forumlarda tarama bütçesini verimsiz kullanabilir.

Basitleştirilmiş indekslenebilirlik puanını şöyle düşünebiliriz:

$$I = C \times R \times A$$

Burada $C$ içerik bütünlüğünü, $R$ render başarısını, $A$ ise botun sayfaya erişebilmesini temsil eder. Değerlerden biri sıfıra yaklaşırsa toplam indeksleme başarısı da dramatik biçimde düşer. Yani mükemmel içerik, hatalı render yüzünden görünmez olabilir.

| Yaklaşım | Avantaj | Dezavantaj | Önerilen kullanım |
|---|---|---|---|
| İstemci tarafı render | Hızlı etkileşim, kolay geliştirme | Bot render kuyruğuna bağımlıdır | Kullanıcı paneli |
| Sunucu tarafı render | HTML içinde hazır içerik | Sunucu yükünü artırır | Tartışma ve etiket sayfaları |
| Dinamik render | Botlara önceden oluşturulmuş çıktı | Bakım ve önbellek gerektirir | SSR uygulanamayan kurulumlar |
| Statik üretim | Çok hızlı ve güvenilir | Sık değişen yanıtlarda güncelleme zordur | Kurallar ve bilgi sayfaları |

## Önce sunucudan gelen HTML’yi kontrol edin

Bir tartışma URL’sini `curl` ile çağırarak botun başlangıçta ne gördüğünü inceleyin:

```bash
curl -A "Googlebot" -L https://forum.example.com/d/42-ornek-konu
```

Çıktıda konu başlığı, ilk mesaj ve canonical etiketi bulunmalıdır. Yalnızca uygulama kökü ve JavaScript dosyaları görünüyorsa sunucu tarafı render veya ön oluşturma katmanı düşünülmelidir. Rendertron benzeri eski çözümler yerine güncel Chromium tabanlı Playwright servisleri kullanılabilir.

Aşağıdaki örnek, Playwright ile sayfanın render edilmesini ve oluşan HTML’nin alınmasını gösterir:

```javascript
import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto(process.argv[2], { waitUntil: "networkidle" });
console.log(await page.content());
await browser.close();
```

Bu çıktı Nginx veya bir uygulama ara katmanında önbelleğe alınabilir. Ancak kullanıcıya başka, bota başka içerik göstermeyin. Dinamik render yalnızca aynı içeriğin çalıştırılmış HTML sürümünü üretmelidir; aksi hâlde cloaking riski doğar.

## Teknik SEO temelini sağlamlaştırın

Her tartışma için benzersiz `<title>`, açıklama, canonical URL ve Open Graph etiketleri üretin. Sayfalama kullanılıyorsa her sayfa erişilebilir bir URL taşımalı; sonsuz kaydırma tek erişim yöntemi olmamalıdır. Silinen veya taşınan konular doğru `404`, `410` ya da `301` yanıtını vermelidir.

Forum içeriği için `DiscussionForumPosting` yapılandırılmış verisi oldukça değerlidir:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "DiscussionForumPosting",
  "headline": "Örnek tartışma",
  "datePublished": "2026-08-14T10:00:00Z",
  "author": { "@type": "Person", "name": "Ada" }
}
</script>
```

XML site haritasına yalnızca indekslenebilir tartışmaları ekleyin ve `lastmod` değerini yeni yanıt geldiğinde güncelleyin. Düşük kaliteli profil, arama sonucu ve yinelenen filtre sayfalarını `noindex` ile sınırlandırarak tarama bütçesini asıl içeriklere yönlendirin.

Son olarak Google Search Console URL Denetimi, Rich Results Test ve log analiziyle gerçek Googlebot davranışını izleyin. SEO’yu tek seferlik eklenti kurulumu değil; render süresi, indekslenen URL oranı ve organik trafik üzerinden sürekli ölçülen bir performans süreci olarak ele alın.
