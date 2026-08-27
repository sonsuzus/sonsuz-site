---
layout: post
title: "Clean Architecture Prensipleri: Test Edilebilir ve Uzun Ömürlü Yazılımlar"
math: true
categories: 
  - Bilgi
tags: 
  - Clean Architecture
  - Yazılım Mimarisi
  - Test Edilebilirlik
---

Bir yazılım projesinin en pahalı kısmı çoğu zaman ilk sürümünü geliştirmek değildir; asıl maliyet, değişen iş kurallarına ve yeni ihtiyaçlara yıllar boyunca uyum sağlamaktır. Clean Architecture, kodu yalnızca bugün çalışacak şekilde değil, yarın değiştirilebilecek şekilde tasarlamayı hedefler. Temel fikir basittir: İş kuralları; veritabanı, arayüz, framework veya dış servis gibi ayrıntılara bağımlı olmamalıdır.
``

Clean Architecture yaklaşımı Robert C. Martin tarafından yaygınlaştırılmıştır. Soğan, Hexagonal Architecture ve Ports-and-Adapters gibi mimari yaklaşımlarla akrabadır. Hepsinin ortak hedefi, bağımlılıkların merkezdeki iş kurallarına doğru akmasıdır. Böylece bir web framework'ünü değiştirmek, PostgreSQL yerine başka bir veritabanına geçmek ya da komut satırı arayüzü eklemek, domain mantığını altüst etmez.

## Bağımlılık Kuralı: Oklar Her Zaman İçeri

Mimarinin kalbinde **Dependency Rule** bulunur: Kaynak kod bağımlılıkları dış katmandan iç katmana yönelmelidir. İç katmanlar dışarıdaki araçlardan haberdar olmaz. Bu yaklaşımı katmanlar üzerinden inceleyelim:

| Katman | Sorumluluk | Bilmemesi Gerekenler |
|---|---|---|
| Entities | En temel iş kuralları | HTTP, SQL, framework |
| Use Cases | Uygulama senaryoları | React, ORM, REST ayrıntıları |
| Interface Adapters | Veri dönüşümü, controller ve presenter | Altyapı implementasyonları |
| Frameworks & Drivers | Veritabanı, web sunucusu, UI | Domain kararları |

Bu ilişkiyi basitçe $D_{outer} \rightarrow D_{inner}$ şeklinde düşünebiliriz. Dış katman iç katmana bağımlıdır; tersi yasaktır. Değişim maliyeti kabaca bağımlı modül sayısıyla artar: $C \propto n$. Bu nedenle merkezdeki modüllerin bağımlılık sayısını düşük tutmak, bakım maliyetini doğrudan azaltır.

## Interface ile Ayrıntıyı Tersine Çevirmek

Bir sipariş oluşturma senaryosunun veritabanına doğrudan bağlandığını düşünelim. Use case, `PostgresOrderRepository` sınıfını oluşturursa PostgreSQL artık iş akışının vazgeçilmez parçası olur. Bunun yerine use case bir soyutlamaya bağımlı olmalıdır:

```ts
interface OrderRepository {
  save(order: Order): Promise<void>;
}

class CreateOrder {
  constructor(private readonly repository: OrderRepository) {}

  async execute(customerId: string, total: number) {
    if (total <= 0) throw new Error("Tutar pozitif olmalı");

    const order = new Order(customerId, total);
    await this.repository.save(order);
    return order;
  }
}
```

Burada `CreateOrder`, siparişin **nasıl** saklandığını bilmez; yalnızca saklanmasını ister. Gerçek uygulamada PostgreSQL adaptörü, testte ise bellek içi bir repository verilebilir. Bu, Dependency Inversion Principle'ın pratik karşılığıdır: Yüksek seviye politika, düşük seviye detaya değil; ikisi de soyutlamaya bağımlıdır.

## Testler Neden Kolaylaşır?

Dış sistemlerden bağımsız use case'ler hızlı, kararlı ve odaklı birim testlerine izin verir. Ağ, veritabanı ve zaman gibi kontrol edilmesi zor unsurlar testin merkezinden çıkar.

```ts
class InMemoryOrderRepository implements OrderRepository {
  public orders: Order[] = [];
  async save(order: Order) { this.orders.push(order); }
}

const repo = new InMemoryOrderRepository();
const useCase = new CreateOrder(repo);
await useCase.execute("customer-42", 250);
console.assert(repo.orders.length === 1);
```

| Yaklaşım | Test Hızı | Dış Bağımlılık | Değişime Dayanıklılık |
|---|---:|---|---|
| Doğrudan ORM kullanan servis | Düşük | Yüksek | Düşük |
| Port ve adapter kullanan use case | Yüksek | Düşük | Yüksek |

Elbette Clean Architecture her küçük proje için zorunlu değildir. Basit bir prototipte katmanlar gereksiz tören yaratabilir. Ancak iş kuralları büyüyor, ekip genişliyor ve teknoloji kararlarının değişmesi bekleniyorsa bu ayrım erken dönemde büyük bir sigortaya dönüşür. Amaç daha çok dosya üretmek değil; değişimin en sık yaşandığı yerleri, en değerli iş kurallarından uzak tutmaktır.
