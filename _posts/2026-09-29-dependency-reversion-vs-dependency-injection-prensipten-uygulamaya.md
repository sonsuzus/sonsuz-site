---
layout: post
title: "Dependency Reversion vs Dependency Injection: Prensipten Uygulamaya"
math: true
categories: 
  - Bilgi
tags: 
  - dependency inversion
  - dependency injection
  - solid
  - yazılım mimarisi
  - tasarım kalıpları
  - csharp
toc: true
image: /img/dependency-reversion-vs-32.png
---

![dependency-reversion-vs-32](/img/dependency-reversion-vs-32.svg)


Bir yazılım geliştiricinin araç çantasında birbirine benzeyen ama aynı işi yapmayan iki önemli kavram bulunur: Dependency Inversion Principle (DIP) ve Dependency Injection (DI). Başlıkta “Dependency Reversion” olarak anılsa da prensibin literatürdeki adı **Dependency Inversion**, yani Bağımlılıkların Tersine Çevrilmesi Prensibi'dir. DIP mimari yönü belirleyen bir pusula, DI ise o yönde ilerlemeyi kolaylaştıran pratik bir araçtır.

``

## Önce bağımlılık nedir?

Bir sınıf görevini tamamlamak için başka bir sınıfa ihtiyaç duyuyorsa aralarında bağımlılık vardır. Örneğin `OrderService`, sipariş onayından sonra doğrudan `EmailSender` oluşturabilir. Bu durumda servis yalnızca bildirim gönderme fikrine değil, e-posta teknolojisinin somut ayrıntılarına da bağlanır.

Bağımlılık sayısını kabaca $D$, bir değişikliğin yayılma maliyetini de $C$ ile gösterirsek sıkı bağlı bir yapıda genellikle şu eğilim görülür:

$$C \propto D \times K$$

Buradaki $K$, bağımlılıklar arasındaki sıkılık katsayısıdır. DIP'nin hedefi bütün bağımlılıkları yok etmek değil, $K$ değerini arayüzler ve doğru sınırlar yardımıyla küçültmektir.

## Dependency Inversion ne söyler?

SOLID'in “D” harfi olan DIP iki temel öneride bulunur:

1. Üst seviye modüller alt seviye modüllere doğrudan bağlı olmamalıdır; ikisi de soyutlamalara bağlanmalıdır.
2. Soyutlamalar ayrıntılara değil, ayrıntılar soyutlamalara bağlı olmalıdır.

Örneğin sipariş politikası üst seviye bir iş kuralıdır. SMTP ile e-posta göndermek ise teknik ayrıntıdır. `OrderService` doğrudan SMTP sınıfını tanırsa mimari okun ters yönüne bakar. Araya `INotificationSender` koyulduğunda iş kuralı bir teknolojiye değil, ihtiyaç duyduğu davranış sözleşmesine bağlanır.

## Dependency Injection ne yapar?

DI, bir nesnenin ihtiyaç duyduğu bağımlılıkları kendi içinde oluşturmak yerine dışarıdan almasıdır. Constructor injection en yaygın ve güvenli yöntemdir:

```csharp
public interface INotificationSender
{
    Task SendAsync(string message);
}

public sealed class OrderService
{
    private readonly INotificationSender _sender;

    public OrderService(INotificationSender sender)
    {
        _sender = sender;
    }

    public Task ConfirmAsync(int orderId)
    {
        return _sender.SendAsync($"Sipariş {orderId} onaylandı.");
    }
}
```

Bu kodda arayüz, bildirimin nasıl gönderileceğini değil hangi davranışın gerektiğini açıklar. Constructor ise bağımlılığı görünür ve zorunlu hâle getirir. `OrderService`, `EmailSender` nesnesini üretmediği için test sırasında sahte bir gönderici kullanılabilir.

Bir DI container bu bağlantıyı otomatik kurabilir:

```csharp
services.AddScoped<INotificationSender, EmailSender>();
services.AddScoped<OrderService>();
```

Container faydalıdır ancak DI'nin kendisi değildir. Aynı nesneleri `new OrderService(new EmailSender())` ile elle birleştirmek de dependency injection'dır.

## Farklar tek tabloda

| Boyut | Dependency Inversion | Dependency Injection |
|---|---|---|
| Türü | Mimari prensip | Uygulama tekniği veya kalıbı |
| Ana soru | Kod hangi yöne bağımlı olmalı? | Bağımlılık nesneye nasıl verilmeli? |
| Arayüz şart mı? | Genellikle anlamlı soyutlama gerekir | Hayır, somut nesne de enjekte edilebilir |
| Container şart mı? | Hayır | Hayır |
| Temel kazanç | Mimari esneklik ve ayrıntılardan bağımsızlık | Nesne üretimini ayırma ve test kolaylığı |

## Kesişim ve sık yapılan hata

DI kullanmak otomatik olarak DIP uygulamak anlamına gelmez. Aşağıdaki constructor enjeksiyondur, fakat üst seviye servis hâlâ somut SMTP ayrıntısına bağımlıdır:

```csharp
public OrderService(SmtpEmailSender sender)
{
    _sender = sender;
}
```

Tersine, DIP'ye uygun bir tasarım DI container olmadan da kurulabilir. Uygulamanın başlangıç noktası nesneleri elle üretip arayüzler üzerinden bağlayabilir. Önemli olan, iş kurallarının teknik ayrıntılara değil kendi tanımladığı kararlı sözleşmelere dayanmasıdır.

Kısacası DIP “bağımlılıkların yönünü düzelt” der; DI ise “bu bağımlılıkları dışarıdan ver” der. Birlikte kullanıldıklarında test edilebilir, değiştirilebilir ve bakımı daha huzurlu sistemler ortaya çıkar. Pusula ile tornavidayı karıştırmayın: Biri yönü gösterir, diğeri sistemi kurmanıza yardım eder.
