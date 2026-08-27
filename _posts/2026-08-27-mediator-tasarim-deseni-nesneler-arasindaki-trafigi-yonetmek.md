---
layout: post
title: "Mediator Tasarım Deseni: Nesneler Arasındaki Trafiği Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - Design Patterns
  - Mediator
  - Nesne Yönelimli Programlama
---

Bir sınıfın diğer beş sınıfı doğrudan tanıdığı bir uygulama, küçükken masum görünür; büyüdükçe ise kabloları birbirine dolanmış bir sunucu odasına dönüşür. **Mediator (Arabulucu)** tasarım deseni, nesnelerin birbirleriyle doğrudan konuşması yerine merkezi bir arabulucu üzerinden iletişim kurmasını sağlar. Böylece sınıflar arası bağımlılık azalır, iletişim kuralları tek bir noktada toplanır ve sistemi değiştirmek daha güvenli hale gelir.
``

Mediator deseninin temel problemi, özellikle kullanıcı arayüzleri, sohbet sistemleri, uçuş kontrolü veya sipariş akışları gibi alanlarda ortaya çıkar. Örneğin bir formdaki `Kayıt Ol` düğmesi; e-posta kutusunun geçerliliğini, şifre alanının durumunu ve hata mesajı etiketini doğrudan yönetirse her bileşen diğerlerini tanımaya başlar. Yeni bir alan eklemek, mevcut bileşenlerin çoğunu değiştirmeyi gerektirebilir.

Desende iki ana rol bulunur: **Colleague (işbirlikçi)** nesneler olay üretir veya olaydan etkilenir; **Mediator** ise bu olayları yorumlar ve uygun nesnelere komut verir. Colleague nesnesi diğer colleague'ları değil, yalnızca arabulucuyu bilir. İletişim akışı kabaca şöyledir:

$$Colleague_A \rightarrow Mediator \rightarrow Colleague_B, Colleague_C$$

Bu yapı, nesneler arasındaki bağlantı sayısını azaltır. $n$ nesnenin herkesle doğrudan konuştuğu bir modelde olası ilişki sayısı yaklaşık $n(n-1)$ iken, merkezi arabulucuda her nesne çoğunlukla tek bir mediator referansı taşır. Elbette bu matematiksel sadeleşmenin bedeli, arabulucunun daha fazla karar vermesidir.

| Özellik | Doğrudan iletişim | Mediator ile iletişim |
|---|---|---|
| Bağımlılık | Nesneler birbirini tanır | Nesneler mediator'ı tanır |
| İş kuralı konumu | Birçok sınıfa dağılır | Merkezi noktada toplanır |
| Yeni bileşen ekleme | Mevcut sınıfları etkileyebilir | Genellikle mediator güncellenir |
| Temel risk | Sıkı bağlılık | Aşırı büyümüş mediator |

Aşağıdaki C# örneğinde bir sohbet odası mediator görevini üstlenir. Kullanıcılar birbirlerinin referansını bilmeden mesaj gönderebilir:

```csharp
using System;
using System.Collections.Generic;

interface IChatMediator
{
    void Send(string message, User sender);
    void AddUser(User user);
}

class ChatRoom : IChatMediator
{
    private readonly List<User> users = new();

    public void AddUser(User user) => users.Add(user);

    public void Send(string message, User sender)
    {
        foreach (var user in users)
        {
            if (user != sender)
                user.Receive($"{sender.Name}: {message}");
        }
    }
}

class User
{
    private readonly IChatMediator mediator;
    public string Name { get; }

    public User(string name, IChatMediator mediator)
    {
        Name = name;
        this.mediator = mediator;
    }

    public void Send(string message) => mediator.Send(message, this);
    public void Receive(string message) => Console.WriteLine(message);
}
```

Burada `User.Send`, hedef kullanıcıları dolaşmaz. Bu sorumluluk `ChatRoom.Send` içindedir. Örneğin daha sonra engelleme, mesaj filtreleme, çevrim içi durumu veya loglama eklemek isterseniz kullanıcı sınıfını değiştirmek zorunda kalmadan arabulucuya davranış ekleyebilirsiniz. Bu, **Single Responsibility Principle** açısından da avantajdır: kullanıcı mesaj üretir, oda ise dağıtım politikasını yönetir.

Ancak Mediator her derde deva değildir. Çok fazla iş kuralı tek bir sınıfa eklenirse ortaya “god object” adı verilen dev, anlaşılması zor bir merkez çıkabilir. Bu durumda arabulucuyu daha küçük senaryo arabulucularına bölmek, olay tabanlı mimariye geçmek veya kuralları ayrı servislerle desteklemek mantıklıdır.

| Mediator tercih edin | Dikkatli olun |
|---|---|
| Karmaşık UI bileşenleri birbirini tetikliyorsa | Nesneler zaten doğal ve basit bir hiyerarşideyse |
| İletişim kuralları sık değişiyorsa | Mediator yüzlerce alakasız kural taşıyorsa |
| Bileşenleri bağımsız test etmek istiyorsanız | Basit bir metot çağrısı yeterliyse |

Özetle Mediator, nesneleri sessizleştirmez; onların konuşma biçimini düzenler. Merkezi trafik kontrolü sayesinde bileşenler daha az şey bilir, daha kolay test edilir ve değişime karşı daha dayanıklı olur.
