---
layout: post
title: "Event Sourcing: Sistemin Geçmişini Yeniden Oynatmak"
math: true
categories: 
  - Bilgi
tags: 
  - event-sourcing
  - veritabanı
  - yazılım-mimarisi
toc: true
---

Bir banka hesabındaki bakiyenin 1.250 TL olduğunu bilmek faydalıdır; ancak bu bakiyeye **nasıl ulaşıldığını** bilmek çok daha güçlüdür. Event Sourcing, yalnızca güncel durumu saklamak yerine, durumu meydana getiren bütün olayları değiştirilemez bir günlükte tutar. Böylece sistemin geçmişi silinmez; gerektiğinde baştan oynatılarak herhangi bir andaki durum yeniden oluşturulabilir.

``

## Event Sourcing’in temel fikri

Geleneksel sistemlerde bir kayıt her işlemden sonra güncellenir. Kullanıcının adresi değiştiğinde eski adresin üzerine yenisi yazılır. Event Sourcing yaklaşımında ise `AdresDegistirildi` adında yeni bir olay eklenir; geçmiş kayıt değiştirilmez.

Bir varlığın belirli bir andaki durumunu matematiksel olarak şöyle ifade edebiliriz:

$$S_n = f(S_{n-1}, E_n)$$

Burada $S_n$ yeni durumu, $S_{n-1}$ önceki durumu ve $E_n$ gerçekleşen olayı temsil eder. Bütün geçmişi yeniden oynatmak istediğimizde başlangıç durumuna olayları sırayla uygularız:

$$S_n = E_n(E_{n-1}(\dots E_2(E_1(S_0))))$$

Kısacası son durum, olayların sıralı biçimde katlanmasının sonucudur. Bir video oyununun kayıt dosyası yerine oyuncunun bütün hareketlerini sakladığınızı düşünün: doğru sırayla oynatıldığında aynı sahne yeniden oluşur.

## Geleneksel yaklaşım ile karşılaştırma

| Özellik | Durum tabanlı kayıt | Event Sourcing |
|---|---|---|
| Saklanan veri | Yalnızca güncel durum | Gerçekleşen bütün olaylar |
| Geçmişi inceleme | Ek denetim tablosu gerekir | Doğal olarak mümkündür |
| Hata ayıklama | Sonuç görülür | Sonuca götüren adımlar görülür |
| Veri düzeltme | Kayıt güncellenir | Düzeltici yeni olay eklenir |
| Güncel duruma erişim | Genellikle hızlıdır | Olay oynatma veya projeksiyon gerekir |

Event Store içindeki olaylar genellikle kimlik, olay türü, zaman, sürüm ve veri alanlarından oluşur. Aynı varlığa ait olayların sırası kritik olduğundan sürüm numarası kullanılır.

## Küçük bir uygulama örneği

Aşağıdaki C# örneği, banka hesabına ait olayları çalıştırarak bakiyeyi yeniden hesaplar:

```csharp
public interface IAccountEvent { }

public record MoneyDeposited(decimal Amount) : IAccountEvent;
public record MoneyWithdrawn(decimal Amount) : IAccountEvent;

public class BankAccount
{
    public decimal Balance { get; private set; }

    public void Apply(IAccountEvent accountEvent)
    {
        switch (accountEvent)
        {
            case MoneyDeposited deposited:
                Balance += deposited.Amount;
                break;
            case MoneyWithdrawn withdrawn:
                Balance -= withdrawn.Amount;
                break;
        }
    }
}

var history = new IAccountEvent[]
{
    new MoneyDeposited(1000),
    new MoneyWithdrawn(200),
    new MoneyDeposited(450)
};

var account = new BankAccount();
foreach (var accountEvent in history)
    account.Apply(accountEvent);

Console.WriteLine(account.Balance); // 1250
```

Buradaki `Apply` metodu dış dünyada yeni bir işlem gerçekleştirmez; yalnızca olayın durum üzerindeki etkisini uygular. Bu ayrım önemlidir. Geçmiş yeniden oynatılırken müşteriye tekrar e-posta göndermek veya ödeme çekmek istemeyiz!

## Snapshot ve projeksiyonlar

Milyonlarca olayı her sorguda baştan çalıştırmak pahalı olabilir. Bu sorunu çözmek için belirli aralıklarla **snapshot** alınır. Snapshot, örneğin ilk 100.000 olayın oluşturduğu durumu saklar; sistem daha sonra yalnızca kalan olayları uygular.

Okuma işlemleri için de olaylardan türetilen **projeksiyonlar** kullanılır. Bir projeksiyon, olay akışını kullanıcı arayüzünün ihtiyaç duyduğu tabloya dönüştürebilir. Bu yapı sıklıkla CQRS ile birlikte kullanılır: komutlar olay üretirken sorgular optimize edilmiş okuma modellerinden cevaplanır.

## Güçlü ama bedelsiz değil

Event Sourcing; finans, sipariş, stok, denetim ve zaman yolculuğu gerektiren sistemlerde oldukça değerlidir. Buna karşılık olay şemalarının sürümlenmesi, projeksiyonların güncel tutulması ve kişisel verilerin silinmesi gibi konular ek tasarım ister. Olayların değiştirilemez olması, hatalı olayların silinmesi yerine telafi edici olaylarla düzeltilmesini gerektirir.

Bu yaklaşım her CRUD uygulaması için sihirli bir değnek değildir. Fakat sistemde “Ne oldu, neden oldu ve geçen salı saat 14.32’de durum neydi?” soruları önemliyse Event Sourcing, yazılımınıza oldukça güvenilir bir hafıza kazandırır.
