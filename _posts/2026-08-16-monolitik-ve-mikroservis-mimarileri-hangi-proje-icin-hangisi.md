---
layout: post
title: "Monolitik ve Mikroservis Mimarileri: Hangi Proje İçin Hangisi?"
math: true
categories: 
  - Bilgi
tags: 
  - yazılım mimarisi
  - monolit
  - mikroservis
toc: true
image: /img/monolitik-ve-mikroservis-67.png
---

Bir yazılım projesi büyümeye başladığında en kritik sorulardan biri şudur: Uygulamayı tek parça hâlinde mi tutmalı, yoksa küçük ve bağımsız servisler olarak mı bölmeliyiz? Monolitik ve mikroservis mimarileri, yalnızca kodun klasör yapısını değil; ekip organizasyonunu, dağıtım süreçlerini, maliyeti ve hata yönetimini de belirler. Bu nedenle doğru seçim, modaya değil projenin gerçek ihtiyaçlarına dayanmalıdır.

``

## Temel fikir: Tek bina mı, şehir mi?

**Monolitik mimari**, kullanıcı arayüzü, iş kuralları ve veri erişimi gibi katmanların tek bir uygulama içinde paketlendiği yaklaşımdır. Örneğin bir e-ticaret sitesinin ürün, sepet, ödeme ve kullanıcı modülleri aynı kod deposunda çalışabilir ve tek paket olarak yayınlanabilir.

**Mikroservis mimarisi** ise sistemi iş alanlarına göre bağımsız servisler hâlinde böler. Ödeme servisi, sipariş servisi ve bildirim servisi kendi süreçlerinde çalışır; genellikle HTTP, gRPC veya mesaj kuyrukları üzerinden iletişim kurar. Bu yapı, tek binadan ziyade birbirine yollarla bağlı bir şehir gibidir.

Mimari karmaşıklığı kabaca şöyle düşünebiliriz:

$$C = C_{uygulama} + C_{dağıtım} + C_{iletişim} + C_{operasyon}$$

Monolitte $C_{iletişim}$ düşükken, mikroservislerde ağ iletişimi ve operasyon yükü nedeniyle artar. Buna karşılık çok büyük sistemlerde monolitin uygulama karmaşıklığı hızla yükselme eğilimindedir.

| Kriter | Monolitik Mimari | Mikroservis Mimari |
|---|---|---|
| Dağıtım | Tek paket, basit başlangıç | Her servis ayrı dağıtılır |
| Veri yönetimi | Genellikle ortak veritabanı | Servis başına veri sahipliği |
| Ölçekleme | Uygulamanın tamamı ölçeklenir | İhtiyaç duyan servis ölçeklenir |
| Hata etkisi | Hata tüm sistemi etkileyebilir | İzolasyon mümkündür, ancak zincirleme hata riski vardır |
| Operasyon | Daha az araç ve altyapı | Kubernetes, gözlemlenebilirlik, ağ yönetimi gerekebilir |

## Küçük projelerde monolitin gücü

MVP, yönetim paneli, küçük SaaS ürünü veya sınırlı ekiplerle geliştirilen projeler için monolit çoğu zaman en mantıklı başlangıçtır. Geliştirici uygulamayı yerelde tek komutla çalıştırabilir, hata ayıklama doğrudandır ve transaction yönetimi daha kolaydır. Özellikle ödeme sonrası sipariş oluşturma gibi işlemlerde tek veritabanı transaction'ı önemli bir rahatlık sağlar.

Örneğin basit bir sipariş akışı tek uygulamada şöyle yönetilebilir:

```python
# Sipariş ve stok işlemi aynı transaction içinde yürütülür.
def create_order(customer_id, product_id):
    product = db.products.get(product_id)
    if product.stock <= 0:
        raise ValueError("Stok yok")

    product.stock -= 1
    order = db.orders.create(customer_id=customer_id, product_id=product_id)
    db.commit()
    return order
```

Bu yaklaşımda tutarlılık güçlüdür. Ancak uygulama büyüdükçe bağımlılıklar artar; küçük bir ödeme değişikliği bile tüm paketin yeniden dağıtılmasını gerektirebilir.

## Büyük projelerde mikroservislerin esnekliği

Yüksek trafik alan, birçok ekip tarafından geliştirilen veya farklı ölçekleme ihtiyaçları bulunan sistemlerde mikroservisler avantaj sağlar. Örneğin bir kampanya sırasında katalog görüntüleme trafiği çok artarken ödeme servisi aynı oranda yük almayabilir. Bu durumda yalnızca katalog servisinin çoğaltılması maliyeti düşürebilir.

Ancak servisler arası iletişim yeni problemler doğurur: ağ gecikmesi, zaman aşımı, tekrar eden istekler ve dağıtık veri tutarlılığı. Monolitteki atomik transaction yerine çoğu zaman **eventual consistency** kullanılır. Sipariş oluşturulduktan sonra stok düşme işlemi bir olay aracılığıyla asenkron gerçekleşebilir.

```javascript
// Sipariş servisi, diğer servisleri doğrudan çağırmak yerine olay yayınlar.
await eventBus.publish("OrderCreated", {
  orderId: order.id,
  productId: order.productId
});
```

Bu kod servisleri gevşek bağlar; fakat olayın iki kez işlenmesi gibi durumlar için idempotent tüketiciler tasarlamak gerekir.

| Proje durumu | Önerilen başlangıç |
|---|---|
| 1-5 kişilik ekip, belirsiz ürün fikri | Modüler monolit |
| Tek veritabanı transaction'larına yoğun ihtiyaç | Monolit |
| Bağımsız ekipler ve farklı yayın takvimleri | Mikroservis |
| Çok yüksek, dengesiz trafik | Mikroservis veya hibrit yapı |
| DevOps ve izleme altyapısı sınırlı | Monolit |

## Son karar: Önce sınırları tasarlayın

Mikroservis, monolitin otomatik olarak "daha gelişmiş" versiyonu değildir; dağıtık sistem maliyetini bilinçli biçimde kabul etmektir. Çoğu ürün için iyi tasarlanmış bir **modüler monolit**, hızlı öğrenme ve düşük operasyon maliyeti sunar. İş alanları netleştiğinde, gerçekten bağımsız ölçeklenmesi veya ayrı ekiplerce yönetilmesi gereken modüller servisleştirilebilir. Kısacası: Önce basit kalın, sonra ölçerek bölünün.

![monolitik-ve-mikroservis-67](/img/monolitik-ve-mikroservis-67.svg)

