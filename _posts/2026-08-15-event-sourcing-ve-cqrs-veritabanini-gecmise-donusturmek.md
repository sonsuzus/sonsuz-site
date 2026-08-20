---
layout: post
title: "Event Sourcing ve CQRS: Veritabanını Geçmişe Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - event sourcing
  - cqrs
  - mikroservisler
---

Geleneksel uygulamalar genellikle bir müşterinin mevcut bakiyesini, siparişin son durumunu veya kullanıcının güncel profilini saklar. Event Sourcing ise daha meraklı bir yaklaşım benimser: “Bu durum nasıl oluştu?” sorusunun cevabını da saklar. Sistem durumu, değişmez olayların kronolojik dizisinden yeniden üretilir. CQRS (Command Query Responsibility Segregation) bu fikri, yazma ve okuma modellerini ayırarak tamamlar. İkili birlikte kullanıldığında ilk bakışta karmaşık görünse de denetlenebilir, ölçeklenebilir ve geçmişi güçlü sistemler kurmayı sağlar.

``

## Temel fikir: Durum değil, değişim saklanır

Klasik bir banka hesabında tabloya `balance = 1200` yazılabilir. Event Sourcing yaklaşımında ise şu olaylar tutulur: `AccountOpened`, `MoneyDeposited`, `MoneyWithdrawn`. Güncel bakiye, olaylar baştan sona uygulanarak hesaplanır. Matematiksel olarak hesap durumunu şöyle düşünebiliriz:

$$S_n = reduce(apply, S_0, [e_1, e_2, ..., e_n])$$

Burada $S_0$ başlangıç durumu, $e_i$ olaylar, `apply` ise bir olayın durumu nasıl değiştirdiğini tanımlayan saf fonksiyondur. Para yatırma olayının etkisi örneğin $B_{yeni} = B_{eski} + miktar$ şeklindedir.

| Özellik | Geleneksel CRUD | Event Sourcing |
|---|---|---|
| Saklanan veri | Son durum | Durumu oluşturan olaylar |
| Geçmişi inceleme | Ek log/audit gerekir | Doğal olarak vardır |
| Hatalı işlemi düzeltme | Kaydı güncelleme | Telafi olayı üretme |
| Okuma performansı | Genellikle doğrudan | Projeksiyon gerektirebilir |
| Şema değişimi | Tablo migrasyonu | Olay sürümleme gerekir |

Olaylar geçmişin gerçeğidir; bu nedenle ideal olarak değiştirilemezler. “Ödeme silindi” demek yerine `PaymentRefunded` gibi yeni bir olay eklenir. Bu yaklaşım muhasebe, lojistik, rezervasyon ve finans gibi izlenebilirliğin kritik olduğu alanlarda özellikle değerlidir.

## CQRS sahneye çıkıyor

CQRS, komutları sorgulardan ayırır. Komut (command) sistemi değiştirmek ister; sorgu (query) ise yalnızca bilgi ister. Bir komut, iş kurallarını kontrol eder ve başarılıysa olayı event store'a yazar. Sorgular ise çoğu zaman olaylardan türetilmiş, okumaya özel projeksiyonları kullanır.

| Katman | Sorumluluk | Örnek |
|---|---|---|
| Command modeli | Kural doğrulama ve olay üretme | `WithdrawMoney` |
| Event store | Olayları sıralı saklama | `MoneyWithdrawn` |
| Projection | Olaylardan okuma modeli üretme | Hesap özeti tablosu |
| Query modeli | Hızlı veri sunma | “Son 10 hareket” API'si |

Aşağıdaki TypeScript örneği, bir aggregate'in komutu olaya dönüştürmesini gösterir:

```ts
type Event =
  | { type: "MoneyDeposited"; amount: number }
  | { type: "MoneyWithdrawn"; amount: number };

class BankAccount {
  private balance = 0;

  apply(event: Event) {
    this.balance += event.type === "MoneyDeposited"
      ? event.amount
      : -event.amount;
  }

  withdraw(amount: number): Event {
    if (amount <= 0 || amount > this.balance) {
      throw new Error("Yetersiz bakiye veya geçersiz tutar");
    }
    return { type: "MoneyWithdrawn", amount };
  }
}
```

Burada `withdraw` doğrudan veritabanını güncellemez; önce üretilecek olayı belirler. Olay kalıcı olarak yazıldıktan sonra hem aggregate'e uygulanır hem de projeksiyon tüketicilerine iletilir. Böylece sipariş ekranı, raporlama servisi ve bildirim sistemi aynı olaydan kendi ihtiyaçlarına uygun modeller yaratabilir.

## Dikkat edilmesi gerekenler

Bu mimari her CRUD ekranı için sihirli değnek değildir. Olay sayısı büyüdükçe aggregate'i baştan kurmak maliyetli olabilir; çözüm olarak belirli aralıklarda snapshot alınır. Ayrıca projeksiyonlar asenkron güncellendiğinden kullanıcı kısa süreliğine eski veriyi görebilir. Buna eventual consistency denir.

Olay adlarını geçmiş zamanla ve iş dilinde yazmak iyi bir pratiktir: `OrderPlaced`, `InventoryReserved`, `ShipmentDelivered`. Teknik ayrıntılar yerine işte gerçekleşen anlamlı değişimi anlatan olaylar, sistemi yıllar sonra bile okunabilir tutar. Kısacası Event Sourcing geçmişi veri modelinin merkezine alır; CQRS ise bu geçmişten hem güvenli yazma akışları hem de hızlı okuma deneyimleri üretir.
