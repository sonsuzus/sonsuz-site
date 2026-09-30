---
layout: post
title: "Bounded Context Sınırlarını Çizmek: Mikroservisler Nereden Bölünmeli?"
math: true
categories: 
  - Bilgi
tags: 
  - mikroservisler
  - bounded-context
  - domain-driven-design
  - yazılım-mimarisi
  - ddd
  - dağıtık-sistemler
toc: true
image: /img/bounded-context-sinirlarini-85.png
---

Mikroservis mimarisine geçerken ilk refleks çoğu zaman şudur: Kullanıcı tablosu için bir servis, sipariş tablosu için bir servis, ürün tablosu için de başka bir servis… Tebrikler, artık basit bir veritabanına ağ gecikmesi, dağıtık transaction ve hata ayıklama zorluğu eklediniz! Sağlıklı servis sınırları teknik yapılara göre değil, domain içindeki iş yetenekleri ve anlamsal bütünlük dikkate alınarak çizilmelidir.

![bounded-context-sinirlarini-85](/img/bounded-context-sinirlarini-85.svg)

``

## Küçük olmak tek başına erdem değildir

Bir mikroservisin amacı mümkün olan en az satır kodu barındırmak değildir. Amaç, belirli bir iş sorumluluğunu bağımsız şekilde yerine getirebilen ve kendi kararlarını verebilen bir bileşen oluşturmaktır. Buradaki kritik kavram **yüksek iç tutarlılık**, yani cohesion’dır.

Bir servisteki davranışların birbiriyle ilişkisini $C$, diğer servislere bağımlılığını ise $D$ olarak düşünelim. Basitleştirilmiş bir sınır kalitesi şöyle ifade edilebilir:

$$Q = \frac{C}{D + 1}$$

İyi bir servis sınırında $C$ yüksek, $D$ düşük olmalıdır. Her tabloyu ayrı servise dönüştürmek genellikle $D$ değerini büyütür; çünkü tek bir iş akışı için çok sayıda ağ çağrısı gerekir.

| Bölme yaklaşımı | Örnek | Muhtemel sonuç |
|---|---|---|
| Veritabanı tablosuna göre | MüşteriServisi, AdresServisi | Yoğun senkron iletişim |
| Teknik katmana göre | ValidasyonServisi, E-postaServisi | Domain bilgisinin parçalanması |
| İş yeteneğine göre | Sipariş Yönetimi, Faturalama | Daha bağımsız modeller |
| Değişim hızına göre | Kampanya Motoru | Bağımsız geliştirme ve dağıtım |

## Bounded Context neyi korur?

Domain-Driven Design içindeki **Bounded Context**, belirli bir modelin ve kullandığı dilin geçerli olduğu açık sınırdır. Aynı kelime farklı context’lerde farklı anlamlara gelebilir. Örneğin “müşteri”, satış context’inde indirim seviyesi olan bir alıcıyken faturalama context’inde vergi numarası ve ödeme adresi bulunan hukuki taraftır.

Bu iki context aynı `Customer` sınıfını paylaşırsa zamanla devasa, her ihtiyacı karşılamaya çalışan bir model oluşur. Bunun yerine her context kendi modeline sahip olmalı ve diğer context’lerle açık sözleşmeler üzerinden konuşmalıdır.

```typescript
// Sipariş context'i yalnızca kendi kararları için gereken modeli tutar.
type Buyer = {
  id: string;
  discountTier: "standard" | "gold";
};

class Order {
  constructor(
    private buyer: Buyer,
    private total: number
  ) {}

  calculatePayableAmount(): number {
    return this.buyer.discountTier === "gold"
      ? this.total * 0.9
      : this.total;
  }
}
```

Bu modelde müşterinin vergi numarası bulunmaz; çünkü siparişin indirim hesabı için gerekli değildir. Faturalama context’i aynı kişiyi farklı bir modelle temsil edebilir.

## Sınırları bulmak için sorulacak sorular

Servisleri ayırmadan önce ekipçe şu soruların yanıtları aranmalıdır:

1. Bu davranışlar aynı iş kuralını mı koruyor?
2. Veriler birlikte ve atomik olarak mı değişmeli?
3. Kavramlar aynı ekip tarafından mı yönetiliyor?
4. Bileşenler farklı hızlarda mı değişiyor?
5. Bir bölüm çalışmadığında diğerinin çalışması anlamlı mı?

Örneğin sipariş oluşturma ile stok rezervasyonu farklı iş yetenekleri olabilir. Ancak güçlü tutarlılık zorunluysa bunları erkenden iki servise ayırmak, Saga ve telafi işlemleri gibi önemli operasyonel maliyetler doğurur. Önce modüler monolit içinde ayrı modüller tasarlamak, sınırlar doğrulandıktan sonra servis çıkarmak çoğu zaman daha güvenlidir.

## Servis değil, anlam sınırı tasarlayın

Her Bounded Context mutlaka ayrı mikroservis olmak zorunda değildir. Bounded Context mantıksal bir sınırdır; mikroservis ise dağıtım kararıdır. Birden fazla context aynı uygulamada bağımsız modüller olarak yaşayabilir.

İyi bir sınır çizildiğinde servis, başka bir servisin tablosunu okumaya çalışmaz; ihtiyaç duyduğu bilgiyi API, olay veya açık bir sözleşme aracılığıyla alır. Sonuç olarak doğru soru “Bu sistemi kaç parçaya bölebiliriz?” değil, “Hangi iş kuralları birlikte anlamlı ve tutarlı kalmalıdır?” olmalıdır. Mikroservislerin gücü küçüklükten değil, doğru yerde duran özerklikten gelir.
