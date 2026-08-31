---
layout: post
title: "Yazılım Mimarisinde Katmanlı Tasarım: Sorumlulukları Doğru Ayırmak"
math: true
categories: 
  - Bilgi
tags: 
  - yazılım mimarisi
  - katmanlı tasarım
  - clean code
toc: true
image: /img/yazilim-mimarisinde-katmanli-47.png
---

![yazilim-mimarisinde-katmanli-47](/img/yazilim-mimarisinde-katmanli-47.svg)


Katmanlı tasarım, büyük ve küçük ölçekli uygulamalarda kodun bir "spagetti tabağına" dönüşmesini engelleyen mimari yaklaşımlardan biridir. Temel fikir basittir: Kullanıcıyla konuşan kod, iş kurallarını uygulayan kod ve veriyi saklayan kod aynı sorumluluğu paylaşmamalıdır. Böylece bir veritabanı değişikliği ekranları, bir arayüz yenilemesi de kritik hesaplama kurallarını doğrudan etkilemez.

``

Bu yaklaşım genellikle üç ana katmanla anlatılır: **sunum (presentation)**, **iş mantığı (business/application)** ve **veri erişim (data access)**. Her katmanın kendine ait bir görevi, bağımlılık yönü ve sınırı vardır. Katmanları departmanlar gibi düşünebilirsiniz: Resepsiyon müşteriyi karşılar, mutfak yemeği hazırlar, depo malzemeyi yönetir. Resepsiyonun depodaki stok tablosunu doğrudan değiştirmesi nasıl kaosa yol açarsa, arayüzün SQL sorgusu çalıştırması da benzer bir mimari alarmdır.

## Katmanların görev dağılımı

| Katman | Temel sorumluluk | Bilmemesi gereken detay |
|---|---|---|
| Sunum | HTTP isteği, form doğrulama, ekran/API yanıtı | SQL, tablo şeması, karmaşık iş kuralı |
| İş mantığı | Kuralları uygulama, süreçleri yönetme | HTML, framework ekran bileşenleri |
| Veri erişim | Sorgu, kayıt, güncelleme, silme işlemleri | Kullanıcının ekran akışı |

**Sunum katmanı**, REST API controller'ları, web sayfaları veya mobil arayüzler olabilir. Bu katman isteği alır, basit biçimsel kontroller yapar ve sonucu kullanıcıya uygun formata dönüştürür. Örneğin e-posta alanının boş olup olmadığını kontrol etmek sunumda yapılabilir; ancak kullanıcının aynı gün içinde en fazla üç sipariş verebilmesi iş mantığının konusudur.

**İş mantığı katmanı**, sistemin asıl karakteridir. İndirim hesaplama, yetki kontrolü, sipariş onayı ve bakiye doğrulama gibi kurallar burada yaşar. Bir siparişin toplamı örneğin şu şekilde ifade edilebilir:

$$Toplam = \sum_{i=1}^{n}(BirimFiyat_i \times Adet_i) - İndirim + Kargo$$

Bu formülün nereden çağrıldığı önemli değildir. Web sitesi, mobil uygulama veya komut satırı aracı aynı iş servisini kullanabilir. İşte katmanlı tasarımın tekrar kullanılabilirlik hediyesi burada ortaya çıkar.

**Veri erişim katmanı** ise kalıcılık işlerini üstlenir. Repository veya DAO desenleriyle veritabanı ayrıntılarını saklar. İş katmanı, `SELECT` cümlelerini bilmek yerine anlamlı metotlar çağırır: `findById`, `save` ya da `findActiveOrders` gibi.

```typescript
// Veri erişim katmanı: verinin nereden geldiğini gizler
interface ProductRepository {
  findById(id: string): Promise<Product | null>;
}

// İş mantığı katmanı: kuralı uygular
class OrderService {
  constructor(private products: ProductRepository) {}

  async addItem(productId: string, quantity: number) {
    const product = await this.products.findById(productId);
    if (!product) throw new Error("Ürün bulunamadı");
    if (product.stock < quantity) throw new Error("Yetersiz stok");

    return { productId, quantity, subtotal: product.price * quantity };
  }
}
```

Bu örnekte servis, ürünün PostgreSQL, MongoDB ya da bellek içi bir koleksiyondan gelmesiyle ilgilenmez. Bu ayrım test yazmayı da kolaylaştırır: Gerçek veritabanı yerine sahte bir `ProductRepository` vererek stok kuralını hızlıca sınayabilirsiniz.

## Bağımlılık yönünü korumak

Klasik katmanlı modelde çağrı yönü şöyledir:

$$Sunum \rightarrow İş\ Mantığı \rightarrow Veri\ Erişim$$

Ters yönlü bağımlılıklar tehlikelidir. Örneğin repository'nin controller çağırması veya servis kodunun doğrudan `req.body` kullanması katman sınırlarını bozar. Daha esnek sistemlerde bağımlılık tersine çevrilir: İş katmanı bir arayüz tanımlar, veri erişim katmanı bu arayüzü uygular. Böylece iş kuralları altyapıdan bağımsız kalır.

Katmanlı tasarım her dosyayı üç klasöre taşımaktan fazlasıdır; sorumlulukları bilinçli biçimde ayırma disiplinidir. Küçük projelerde bile bu disiplin, büyüme başladığında "Bu SQL sorgusu neden buton bileşeninde?" sorusunu sormak zorunda kalmanızı büyük ölçüde önler.
