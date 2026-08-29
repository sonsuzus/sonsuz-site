---
layout: post
title: "DDD ile Karmaşık İş Problemlerini Yazılım Modeline Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - domain-driven design
  - ddd
  - yazılım mimarisi
---

Karmaşık bir iş alanını yazılıma aktarmak, veritabanına birkaç tablo eklemekten çok daha fazlasıdır. Sigorta poliçeleri, kargo rotaları veya kampanya kuralları gibi alanlarda asıl zorluk; kodun iş dilinden kopmasıdır. Domain-Driven Design (DDD), yazılımın merkezine teknik ayrıntıları değil, işletmenin gerçek kurallarını koyar. Amaç, uzmanların anlattığı dünyayı geliştiricilerin sürdürülebilir biçimde modelleyebilmesidir.
``

DDD'nin temel varsayımı şudur: En değerli karmaşıklık, **domain** yani problem alanındadır. Bir e-ticaret sisteminde ürün listelemek teknik bir ayrıntı olabilir; ancak iade hakkının hangi koşullarda doğduğu iş kuralıdır. Bu ayrımı iyi yapmak gerekir. Basitçe model kalitesi şöyle düşünülebilir:

$$\text{Model Değeri} = \text{İş Kuralını İfade Etme Gücü} - \text{Gereksiz Teknik Karmaşıklık}$$

İlk araç **ubiquitous language** (ortak dil) yaklaşımıdır. Yazılımcılar, ürün yöneticileri ve alan uzmanları aynı kavramları aynı anlamda kullanmalıdır. Örneğin “sipariş” kelimesi bazen ödeme bekleyen sepeti, bazen kargolanmış paketi ifade ediyorsa model sislenir. Bu nedenle kavramlar konuşmalarda, testlerde, sınıf adlarında ve API uçlarında tutarlı biçimde yer almalıdır.

| Belirsiz ifade | Ortak dilde daha iyi karşılık | Model etkisi |
|---|---|---|
| Aktif müşteri | Son 90 günde alışveriş yapan müşteri | Kural ölçülebilir olur |
| Sipariş tamamlandı | Ödeme alındı ve stok rezerve edildi | Durum geçişi netleşir |
| İndirim uygulanır | Uygun kampanya indirimi hesaplanır | Hesaplama ayrı modellenir |

DDD'de sistemi tek bir dev model olarak tasarlamak yerine **bounded context** sınırları çizilir. Örneğin Katalog bağlamındaki `Product`, ürünün açıklaması ve kategorisiyle ilgilenir. Sipariş bağlamındaki `Product` ise fiyat anındaki adı, birim fiyatı ve miktarı temsil eden bir satır olabilir. Aynı kelime, farklı bağlamlarda farklı nesnedir; bu bir hata değil, kontrollü bir tasarım kararıdır.

| Kavram | Katalog bağlamı | Sipariş bağlamı |
|---|---|---|
| Ürün | Tanım, görsel, kategori | Satın alma anındaki fiyat bilgisi |
| Müşteri | Profil ve tercih | Teslimat ve fatura sahibi |
| Stok | Mevcut adet | Rezerve edilmiş adet |

Modelin yapı taşlarından **Entity**, kimliğiyle anlam kazanır; `Customer` adı değişse bile aynı müşteridir. **Value Object** ise değerleriyle tanımlanır; iki `Money(100, "TRY")` aynı değeri temsil eder. **Aggregate**, tutarlılık sınırıdır: dış dünya bir aggregate'ın iç nesnelerini doğrudan değiştirmemelidir. Bu sınır, özellikle eşzamanlı işlemlerde kuralları korur.

Aşağıdaki örnekte `Order`, toplam tutarın negatif olamayacağı kuralını kendi içinde koruyan bir aggregate root'tur:

```typescript
class Money {
  constructor(readonly amount: number, readonly currency: string) {
    if (amount < 0) throw new Error("Tutar negatif olamaz");
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) throw new Error("Para birimi uyuşmuyor");
    return new Money(this.amount + other.amount, this.currency);
  }
}

class Order {
  private total = new Money(0, "TRY");

  addItem(unitPrice: Money, quantity: number) {
    if (quantity <= 0) throw new Error("Miktar pozitif olmalı");
    this.total = this.total.add(new Money(unitPrice.amount * quantity, unitPrice.currency));
  }
}
```

Burada `Money`, para birimi uyumunu ve negatif tutarı engelleyerek primitive değerlerin dağınıklığını azaltır. `Order.addItem` ise iş dilini doğrudan konuşur; `setTotal` gibi kuralları delecek genel amaçlı bir metot sunmaz.

DDD her projede ağır katmanlar kurmak demek değildir. Önce en pahalı hataların yaşandığı, kuralı bol alanları belirleyin. Alan uzmanıyla örnek olayları konuşun, terimleri yazın, sınırları çizin ve davranışı testlerle sabitleyin. Teknik mimari zamanla değişebilir; fakat iyi kurulmuş bir domain modeli, iş değiştikçe ekibin yönünü koruyan pusula olur.
