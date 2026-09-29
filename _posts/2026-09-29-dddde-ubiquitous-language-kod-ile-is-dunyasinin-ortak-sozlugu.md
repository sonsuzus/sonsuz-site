---
layout: post
title: "DDD’de Ubiquitous Language: Kod ile İş Dünyasının Ortak Sözlüğü"
math: true
categories: 
  - Bilgi
tags: 
  - ddd
  - ubiquitous-language
  - yazılım-mimarisi
  - domain-driven-design
  - temiz-kod
toc: true
image: /img/dddde-ubiquitous-language-89.png
---

![dddde-ubiquitous-language-89](/img/dddde-ubiquitous-language-89.svg)


Bir yazılımcı “müşteri kaydını güncelledim” derken satış ekibi bunun yeni bir müşteri oluşturmak anlamına geldiğini düşünüyorsa, ortada teknik değil dilsel bir hata vardır. Domain-Driven Design’ın Ubiquitous Language, yani Her Yerde Geçerli Dil yaklaşımı; toplantılarda, belgelerde, testlerde ve kaynak kodda aynı iş terimlerinin aynı anlamla kullanılmasını amaçlar. Böylece kod yalnızca bilgisayarın çalıştırdığı talimatlar olmaktan çıkar, iş sürecinin okunabilir bir modeline dönüşür.

``

## Ubiquitous Language nedir?

DDD’ye göre bir yazılımın merkezinde veritabanı tabloları veya kullandığı framework değil, çözmeye çalıştığı **domain problemi** bulunur. Ubiquitous Language; domain uzmanlarıyla geliştiricilerin birlikte oluşturduğu, sınırları ve anlamları açık ortak sözlüktür.

Örneğin e-ticaret ekibi müşterinin ürünleri geçici olarak ayırması işlemine “rezervasyon” diyorsa kodda buna `HoldItems`, `LockStock` veya `TemporaryBasketOperation` demek gereksiz çeviri yükü oluşturur. Sınıfın `StockReservation`, metodun ise `reserve()` olması beklenir.

İletişimdeki yaklaşık belirsizliği basitçe şöyle düşünebiliriz:

$$B = T \times Y \times A$$

Burada $T$ farklı terim sayısını, $Y$ yanlış yorumlama olasılığını, $A$ ise iletişim adımı sayısını temsil eder. Ortak dil, özellikle $T$ ve $Y$ değerlerini azaltarak toplam belirsizliği düşürür. Bu matematiksel bir proje metriğinden çok, dil karmaşasının ekip büyüdükçe neden katlandığını anlatan zihinsel modeldir.

## Teknik dil ile domain dili arasındaki fark

| Teknik veya belirsiz ad | Domain odaklı ad | Kazanım |
|---|---|---|
| `DataManager` | `OrderRepository` | Hangi veriyi yönettiği anlaşılır |
| `process()` | `approvePayment()` | Gerçek iş kararı görünür olur |
| `status = 3` | `OrderStatus.Shipped` | Gizli anlam ortadan kalkar |
| `User` | `Subscriber` | Bağlama özgü rol tanımlanır |

Her şeyi iş terimine dönüştürmek de doğru değildir. `HashMap`, HTTP veya veritabanı bağlantısı gibi altyapı kavramları teknik isimlerini koruyabilir. Önemli olan, **iş davranışlarının altyapı ayrıntıları arasında kaybolmamasıdır**.

## Kod iş sürecini anlatsın

Aşağıdaki C# örneğinde sipariş iptali, genel amaçlı metotlar yerine domain kurallarıyla ifade edilir:

```csharp
public sealed class Order
{
    public OrderStatus Status { get; private set; }
    public DateTime CreatedAt { get; }

    public void CancelByCustomer(DateTime now)
    {
        if (Status == OrderStatus.Shipped)
            throw new DomainException("Gönderilmiş sipariş iptal edilemez.");

        if (now - CreatedAt > TimeSpan.FromHours(24))
            throw new DomainException("Müşteri iptal süresi doldu.");

        Status = OrderStatus.Cancelled;
    }
}
```

`updateStatus(4)` yazmak teknik olarak daha kısa olabilirdi; ancak `CancelByCustomer` hem niyeti hem de işlemi yapan rolü açıklar. Kurallar nesnenin içinde bulunduğu için başka bir servis siparişi yanlışlıkla geçersiz duruma taşıyamaz. Kod incelemesine katılan domain uzmanı C# bilmeyebilir, fakat “gönderilmiş sipariş iptal edilemez” kuralını doğrulayabilir.

## Ortak dil nasıl oluşturulur?

İlk adım, geliştiricilerin toplantılarda yalnızca dinleyip sonra terimleri “teknik dile çevirmemesi”dir. Bilinmeyen ifadeler anında sorulmalıdır: “İptal ile iade aynı şey mi?”, “Müşteri ne zaman abone olur?” veya “Onay kesinleşme anlamına mı geliyor?” gibi sorular modelin sınırlarını ortaya çıkarır.

Ekip şu pratikleri uygulayabilir:

- Domain terimleri için yaşayan bir sözlük hazırlamak.
- Event Storming oturumlarında iş olaylarını geçmiş zamanla adlandırmak: `PaymentReceived` gibi.
- Sınıf, metot, API ve test adlarında aynı kelimeleri kullanmak.
- Anlamı değişen terimleri kodla birlikte güncellemek.
- Aynı kelimenin farklı bağlamlardaki anlamlarını ayırmak.

Son madde kritiktir. “Müşteri”, satış bağlamında potansiyel alıcıyken faturalama bağlamında ödeme yükümlüsü olabilir. DDD bunu tek ve devasa bir modelle çözmeye çalışmaz; **Bounded Context** sınırları içinde farklı ama tutarlı diller kullanılmasına izin verir.

Ubiquitous Language yalnızca güzel sınıf isimleri seçme tekniği değildir. İş bilgisini kodun yapısına taşıyan sürekli bir ekip alışkanlığıdır. Yazılımcı ile iş birimi aynı kelimeyi aynı anlamda kullandığında toplantılar kısalır, hatalı varsayımlar azalır ve kaynak kod yaşayan bir iş dokümanına dönüşür.
