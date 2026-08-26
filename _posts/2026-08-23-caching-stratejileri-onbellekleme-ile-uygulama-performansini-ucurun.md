---
layout: post
title: "Caching Stratejileri: Önbellekleme ile Uygulama Performansını Uçurun"
math: true
categories: 
  - Bilgi
tags: 
  - caching
  - performans
  - redis
  - backend
  - web geliştirme
toc: true
---

Bir uygulama yavaşsa suçlu her zaman veritabanı değildir; bazen aynı veriyi yüzlerce kez hesaplayan veya uzak bir servisten tekrar tekrar isteyen kodlardır. Önbellekleme (caching), sık kullanılan ve üretimi maliyetli sonuçları daha hızlı erişilebilen bir katmanda saklama tekniğidir. Doğru tasarlandığında gecikmeyi azaltır, altyapı maliyetini düşürür ve sistemin yoğun trafik altında daha sakin kalmasını sağlar. Ancak cache, “ekle ve unut” düğmesi değildir: veri güncelliği, bellek sınırları ve tutarlılık dikkatle yönetilmelidir.
``

Temel fikir basittir: Bir isteğin maliyetini $C_{kaynak}$, cache üzerinden cevaplama maliyetini $C_{cache}$ olarak düşünelim. Cache hit oranı $h$ ise ortalama maliyet yaklaşık olarak şöyle hesaplanabilir:

$$C_{ortalama} = h \cdot C_{cache} + (1-h) \cdot C_{kaynak}$$

Örneğin veritabanından ürün getirmek 100 ms, Redis'ten getirmek 2 ms sürsün. Hit oranı %90 olduğunda ortalama süre $0.9 \cdot 2 + 0.1 \cdot 100 = 11.8$ ms olur. Küçük görünen bu fark, saniyede binlerce istekte devasa bir rahatlama yaratır.

## Cache Nerede Konumlanır?

Önbellek tek bir teknoloji değil, uygulamanın farklı katmanlarında uygulanabilen bir yaklaşımdır. Tarayıcı cache'i statik dosyaları tekrar indirmeyi önlerken, CDN kullanıcıya coğrafi olarak yakın noktadan içerik sunar. Sunucu tarafında ise uygulama belleği veya Redis gibi dağıtık çözümler devreye girer.

| Katman | İdeal kullanım | Avantaj | Dikkat edilmesi gereken |
|---|---|---|---|
| Tarayıcı | CSS, JS, görseller | Ağ isteğini azaltır | Dosya sürümleme gerekir |
| CDN | Statik içerik, medya | Küresel düşük gecikme | Dinamik içerik kuralları |
| Uygulama belleği | Küçük, sık erişilen veri | Çok hızlıdır | Çoklu sunucuda tutarsızlık |
| Redis/Memcached | Oturum, sorgu sonucu | Paylaşımlı ve ölçeklenebilir | TTL ve bellek yönetimi |
| Veritabanı cache'i | Tekrarlanan sorgular | Uygulamaya şeffaf olabilir | Her problemi çözmez |

## En Yaygın Stratejiler

**Cache-aside**, en sık kullanılan modeldir. Uygulama önce cache'e bakar; veri yoksa veritabanından okur ve sonucu cache'e yazar. Okuma ağırlıklı kataloglar için harikadır. Dezavantajı, ilk isteğin cache miss yaşamasıdır.

**Write-through** yaklaşımında veri yazılırken hem ana veri kaynağı hem cache güncellenir. Okumalar güvenilir biçimde güncel kalır; fakat yazma işlemi yavaşlayabilir. **Write-behind** ise önce cache'e yazar, kalıcı depoya daha sonra asenkron aktarır. Hızlıdır ama elektrikler metaforik olarak kesilirse veri kaybı riski taşır.

| Strateji | Okuma performansı | Yazma maliyeti | Uygun senaryo |
|---|---:|---:|---|
| Cache-aside | Yüksek | Düşük | Ürün listeleri, raporlar |
| Write-through | Yüksek | Orta | Fiyat ve stok gibi güncel veri |
| Write-behind | Çok yüksek | Düşük | Telemetri, sayaçlar |
| Read-through | Yüksek | Düşük | Merkezi cache katmanları |

## TTL, Geçersiz Kılma ve Cache Stampede

Cache'te her veri sonsuza dek yaşamamalıdır. TTL (time-to-live), anahtarın geçerlilik süresini belirler. Haber akışı için 30 saniye makul olabilirken, ülke listesi saatlerce saklanabilir. Kritik nokta şudur: Veri değiştiğinde sadece TTL'nin dolmasını beklemek bazen kabul edilemez. Bu durumda ilgili anahtarı silmek veya güncellemek gerekir.

Aşağıdaki örnek, Node.js ve Redis ile cache-aside desenini gösterir. Kod, ürün bulunamadığında veritabanına gider ve sonucu 60 saniyeliğine saklar:

```javascript
async function getProduct(productId) {
  const key = `product:${productId}`;
  const cached = await redis.get(key);

  if (cached) {
    return JSON.parse(cached);
  }

  const product = await db.products.findById(productId);
  if (!product) return null;

  await redis.set(key, JSON.stringify(product), { EX: 60 });
  return product;
}
```

Bir anahtarın süresi dolduğunda çok sayıda istek aynı anda veritabanına hücum edebilir; buna **cache stampede** denir. Çözüm olarak kilitleme, tekil istek birleştirme (request coalescing) veya TTL'ye rastgele küçük bir sapma ekleme kullanılabilir. Örneğin 60 saniye yerine $60 + random(0, 10)$ saniye vermek, tüm anahtarların aynı anda ölmesini engeller.

Son olarak ölçmeden optimizasyon yapmayın. Hit ratio, p95 gecikme, Redis bellek tüketimi ve veritabanı sorgu sayısı düzenli izlenmelidir. Hedef sadece cache eklemek değil; doğru veriyi, doğru süreyle, doğru katmanda saklayarak uygulamanın hem hızlı hem güvenilir kalmasını sağlamaktır.
