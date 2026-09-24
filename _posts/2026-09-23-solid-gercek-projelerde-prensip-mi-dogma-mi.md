---
layout: post
title: "SOLID Gerçek Projelerde: Prensip mi, Dogma mı?"
math: true
categories: 
  - Bilgi
tags: 
  - solid
  - yazılım-mimarisi
  - temiz-kod
  - nesne-yönelimli-programlama
  - refactoring
  - tasarım-prensipleri
toc: true
image: /img/solid-gercek-projelerde-75.png
---

SOLID, yazılım ekiplerinin toplantılarda ciddi yüz ifadeleriyle andığı; kod incelemelerinde ise bazen kılıç gibi kullandığı beş tasarım prensibidir. Doğru uygulandığında değişime dayanıklı kod üretir, yanlış yorumlandığında üç satırlık işlem için on iki arayüz ve yirmi sınıf doğurabilir. Dolayısıyla asıl soru “SOLID kullanmalı mıyız?” değil, “Hangi maliyet karşılığında ve hangi problem için kullanmalıyız?” olmalıdır.


![solid-gercek-projelerde-75](/img/solid-gercek-projelerde-75.svg)

``

## SOLID neyi çözmeye çalışır?

SOLID’in temel hedefi kodu mümkün olduğunca parçalamak değil, değişikliklerin etkisini sınırlamaktır. Bir modüldeki değişiklik tüm sistemi titretiyorsa tasarımın bağımlılık yapısı sorunludur. Bunu kabaca şöyle ifade edebiliriz:

$$Risk \approx Değişiklik\ Olasılığı \times Değişiklik\ Etkisi$$

SOLID çoğunlukla ikinci çarpanı küçültmeye çalışır. Ancak bunun karşılığında soyutlama, dosya sayısı ve zihinsel yük artabilir.

| Prensip | Sağladığı fayda | Dogmaya dönüşme belirtisi |
|---|---|---|
| SRP | Değişiklik nedenlerini ayırır | Her metot için ayrı sınıf açmak |
| OCP | Yeni davranışları mevcut kodu bozmadan ekletir | Hiç oluşmamış senaryolar için eklenti sistemi kurmak |
| LSP | Alt türlerin güvenle kullanılmasını sağlar | Kalıtımı tamamen yasaklamak |
| ISP | İstemciyi gereksiz metotlardan korur | Tek metotlu onlarca anlamsız arayüz üretmek |
| DIP | Yüksek seviyeli politikayı ayrıntılardan ayırır | Her sınıfın önüne arayüz koymak |

## Gerçek projede SRP sınavı

Tek Sorumluluk Prensibi, “bir sınıf yalnızca tek iş yapsın” şeklinde eksik anlatılır. Daha doğru tanım, sınıfın **tek bir değişiklik nedeni** olmasıdır. Örneğin sipariş toplamını hesaplayan kod ile PDF faturası oluşturan kod farklı iş kuralları nedeniyle değişir.

```csharp
public class OrderService
{
    public decimal CalculateTotal(Order order)
        => order.Items.Sum(x => x.Price * x.Quantity);

    public void Save(Order order)
    {
        // Veritabanına kaydetme ayrıntıları
    }

    public byte[] CreatePdf(Order order)
    {
        // PDF kütüphanesine bağlı çıktı üretimi
        return Array.Empty<byte>();
    }
}
```

Bu sınıf hesaplama, kalıcılık ve sunum katmanlarını aynı yerde toplar. Proje büyüyorsa bunları `OrderCalculator`, `OrderRepository` ve `InvoiceRenderer` olarak ayırmak mantıklıdır. Fakat iki günlük bir prototipte aynı ayrım, geliştirme hızını gereksiz yere düşürebilir.

## OCP ve DIP: Her yere arayüz mü?

Ödeme yöntemleri sık sık genişliyorsa bir soyutlama değerlidir:

```csharp
public interface IPaymentProcessor
{
    Task ProcessAsync(decimal amount);
}

public class CardPaymentProcessor : IPaymentProcessor
{
    public Task ProcessAsync(decimal amount)
    {
        // Kart sağlayıcısının API çağrısını gerçekleştirir.
        return Task.CompletedTask;
    }
}
```

Bu yapı, kart ödemesinin yanına havale veya dijital cüzdan eklemeyi kolaylaştırır. Buna karşılık yalnızca uygulama sürümünü döndüren ve değişmesi beklenmeyen bir `VersionService` için `IVersionService` üretmek çoğu zaman törensel programlamadır.

Kararı şu basit sezgiyle değerlendirebiliriz:

$$Soyutlama\ Değeri = Beklenen\ Değişim\ Maliyeti - Ek\ Karmaşıklık$$

Sonuç negatifse soyutlama henüz kendini ödemiyor olabilir. “Şimdilik doğrudan yaz, ihtiyaç oluşunca yeniden düzenle” yaklaşımı dikkatsizlik değil; testler varsa kontrollü bir stratejidir.

## LSP ve ISP neden sessizce bozulur?

Liskov Yerine Geçme Prensibi, alt sınıfın üst sınıfın sözleşmesini bozmamasını ister. `Penguin`, `Bird` sınıfından türeyip `Fly()` çağrısında hata fırlatıyorsa biyolojik sınıflandırma doğru, davranışsal model yanlıştır. Çözüm `FlyingBird` gibi yetenek odaklı soyutlamalar olabilir.

ISP ise özellikle büyük servis arayüzlerinde önemlidir. Bir raporlama bileşeni yalnızca veri okuyorsa ona `DeleteCustomer()` bağımlılığı vermek gereksizdir. Ancak arayüzleri aşırı küçültmek de sistemi keşfetmeyi zorlaştırır. Birlikte değişen ve aynı istemcilerce kullanılan operasyonlar birlikte kalabilir.

## Prensipleri pusula olarak kullanın

SOLID bir uygunluk kontrol listesi değil, tasarım konuşmalarında kullanılan ortak dildir. Kod incelemesinde “DIP ihlali!” demek yerine şu sorular daha üretkendir:

- Bu bağımlılığın değişme ihtimali nedir?
- Değişirse kaç modül etkilenecek?
- Soyutlama testi veya okunabilirliği gerçekten iyileştiriyor mu?
- Bugünkü karmaşıklık, gelecekteki olası kazanca değer mi?

İyi mimari, bütün prensiplere yüzde yüz uyan mimari değildir. Ekibin rahatça anlayabildiği, test edebildiği ve değiştirebildiği mimaridir. SOLID bu yolculukta pusuladır; pusulaya bakmak faydalıdır, fakat uçurumun kenarında hâlâ haritaya göre yürümek pek akıllıca değildir.
