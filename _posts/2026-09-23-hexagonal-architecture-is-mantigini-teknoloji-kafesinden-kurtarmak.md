---
layout: post
title: "Hexagonal Architecture: İş Mantığını Teknoloji Kafesinden Kurtarmak"
math: true
categories: 
  - Bilgi
tags: 
  - hexagonal architecture
  - yazılım mimarisi
  - domain driven design
  - clean code
  - typescript
  - test
toc: true
image: /img/hexagonal-architecture-is-29.png
---

![hexagonal-architecture-is-29](/img/hexagonal-architecture-is-29.svg)


Bir uygulamanın iş kuralları; veritabanı, web framework’ü veya mesaj kuyruğu değiştiğinde neden yeniden yazılmak zorunda kalsın? Hexagonal Architecture, diğer adıyla Ports and Adapters, tam olarak bu soruya itiraz eder. Amaç teknolojiyi yok etmek değil, onu iş mantığının patronu olmaktan çıkarıp değiştirilebilir bir yardımcıya dönüştürmektir.

``

## Merkezde teknoloji değil, domain vardır

Alistair Cockburn tarafından ortaya konan Hexagonal Architecture, uygulamayı iç ve dış dünya olarak iki temel bölgeye ayırır. İçeride kullanım senaryoları ve iş kuralları, dışarıda ise HTTP, PostgreSQL, Kafka, dosya sistemi veya üçüncü taraf servisler bulunur.

Bağımlılıkların yönü dışarıdan içeriye doğrudur. Domain katmanı teknolojik detayları tanımaz. Bu fikri basitçe şöyle gösterebiliriz:

$$
\text{Adapter} \rightarrow \text{Port} \rightarrow \text{Application Core}
$$

Buradaki önemli koşul şudur:

$$
D(\text{Domain}, \text{Framework}) = 0
$$

Yani domain’in framework’e doğrudan bağımlılığı sıfır olmalıdır. Express uygulamanızı çalıştırabilir; ancak indirim oranınızı hesaplamamalıdır!

## Port ve adapter nedir?

**Port**, uygulama çekirdeğinin dış dünyayla nasıl konuşacağını belirleyen sözleşmedir. **Adapter** ise bu sözleşmenin belirli bir teknolojiyle uygulanmasıdır. Port prizi tarif eder, adapter ise elinizdeki cihazı o prize bağlar.

| Kavram | Görevi | Örnek |
|---|---|---|
| Domain | İş kurallarını taşır | Sipariş, fiyat, indirim |
| Inbound port | Uygulamaya sunulan işlemi tanımlar | `CreateOrderUseCase` |
| Outbound port | Çekirdeğin ihtiyaç duyduğu servisi tanımlar | `OrderRepository` |
| Inbound adapter | Dış girdiyi kullanım senaryosuna iletir | REST controller, CLI |
| Outbound adapter | Dış teknolojiyi porta uyarlar | PostgreSQL repository |

Geleneksel katmanlı mimaride iş mantığı çoğu zaman ORM modellerine sızar. Hexagonal yaklaşımda ise veritabanı yalnızca adapter’dır.

## TypeScript ile küçük bir örnek

Önce domain’in ihtiyaç duyduğu çıkış portunu tanımlayalım:

```typescript
interface OrderRepository {
  save(order: Order): Promise<void>;
}

class Order {
  constructor(
    public readonly productId: string,
    public readonly quantity: number
  ) {
    if (quantity <= 0) {
      throw new Error("Adet pozitif olmalıdır");
    }
  }
}
```

`Order`, PostgreSQL tablosu veya ORM dekoratörü bilmez. Yalnızca kendi geçerlilik kuralını korur. Kullanım senaryosu da somut veritabanına değil, porta bağımlıdır:

```typescript
class CreateOrderService {
  constructor(private readonly repository: OrderRepository) {}

  async execute(productId: string, quantity: number): Promise<void> {
    const order = new Order(productId, quantity);
    await this.repository.save(order);
  }
}
```

Şimdi aynı portu bellek içi bir adapter ile uygulayabiliriz:

```typescript
class InMemoryOrderRepository implements OrderRepository {
  public orders: Order[] = [];

  async save(order: Order): Promise<void> {
    this.orders.push(order);
  }
}
```

Bu adapter özellikle testlerde kullanışlıdır. Gerçek veritabanı başlatmadan kullanım senaryosu sınanabilir:

```typescript
const repository = new InMemoryOrderRepository();
const service = new CreateOrderService(repository);

await service.execute("kitap-42", 2);
console.assert(repository.orders.length === 1);
```

## Neyi kazanırız, bedeli nedir?

| Özellik | Doğrudan framework bağımlılığı | Hexagonal Architecture |
|---|---|---|
| Teknoloji değiştirme | Zor ve riskli | Adapter değiştirilir |
| Birim testi | Altyapı gerektirebilir | Bellek içi adapter yeterlidir |
| İş kurallarının görünürlüğü | Dağınık olabilir | Merkezde ve belirgindir |
| Başlangıç maliyeti | Daha düşük | Daha fazla arayüz ve dosya |
| Büyük projede bakım | Zorlaşabilir | Sınırlar sayesinde kolaylaşır |

Elbette her küçük uygulamanın onlarca port ve adapter’a ihtiyacı yoktur. Üç ekranlı basit bir yönetim panelinde bu yapı gereksiz tören yaratabilir. Fakat uzun ömürlü, sık entegrasyon değiştiren veya karmaşık kurallara sahip sistemlerde yatırım karşılığını hızla verir.

## Sonuç

Hexagonal Architecture’ın özü altıgen çizmek değil, bağımlılıkları bilinçli yönetmektir. İş mantığı içeride güvenli biçimde kalır; HTTP, veritabanı ve mesajlaşma sistemleri dışarıdan takılıp çıkarılabilir. Böylece teknoloji değiştiğinde uygulamanın kalbi ameliyat edilmez, yalnızca uygun adapter yenilenir.
