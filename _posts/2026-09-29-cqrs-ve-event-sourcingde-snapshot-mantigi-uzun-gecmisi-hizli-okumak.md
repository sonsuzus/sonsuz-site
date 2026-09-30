---
layout: post
title: "CQRS ve Event Sourcing’de Snapshot Mantığı: Uzun Geçmişi Hızlı Okumak"
math: true
categories: 
  - Bilgi
tags: 
  - cqrs
  - event sourcing
  - snapshot
  - dağıtık sistemler
  - performans
  - yazılım mimarisi
toc: true
image: /img/cqrs-ve-event-51.png
---

![cqrs-ve-event-51](/img/cqrs-ve-event-51.svg)


Event Sourcing kullanan bir sistemde güncel durum doğrudan saklanmaz; geçmişte gerçekleşmiş olaylar sırayla uygulanarak yeniden oluşturulur. Bir siparişin yüzlerce, banka hesabının ise milyonlarca olayı varsa bu işlem zamanla ağırlaşabilir. Snapshot, olay günlüğünü çöpe atmadan belirli bir andaki durumu kaydeder ve sisteme adeta “Buradan devam et!” der.

``

## Önce temel fikir: Durum değil, olay saklamak

Klasik CRUD yaklaşımında veritabanındaki satır çoğunlukla nesnenin son durumunu temsil eder. Event Sourcing’de ise `HesapAcildi`, `ParaYatirildi` ve `ParaCekildi` gibi değişmez olaylar saklanır. Aggregate güncellenirken olaylar kronolojik biçimde uygulanır:

$$S_n = f(f(f(S_0, E_1), E_2), \ldots, E_n)$$

Burada $S_0$ başlangıç durumunu, $E_i$ olayları, $f$ ise olay uygulama fonksiyonunu temsil eder. Olay sayısı $n$ arttıkça aggregate yükleme maliyeti yaklaşık $O(n)$ olur. Snapshot bu geçmişin belirli bir noktaya kadar hesaplanmış sonucudur.

| Yaklaşım | Yükleme şekli | Avantaj | Dezavantaj |
|---|---|---|---|
| Tüm olayları oynatma | İlk olaydan başlanır | Basit ve eksiksizdir | Uzun akışlarda yavaştır |
| Snapshot kullanma | Snapshot ve sonraki olaylar okunur | Daha hızlı yüklenir | Ek sürümleme gerektirir |
| Yalnızca son durumu saklama | Güncel kayıt okunur | Çok hızlıdır | Olay geçmişi avantajları kaybolur |

## Snapshot nasıl çalışır?

Diyelim ki bir aggregate’in 10.000 olayı var ve her 1.000 olayda bir snapshot üretiyoruz. En güncel snapshot 9.000’inci olaydaysa sistem önce bu durumu yükler, ardından yalnızca kalan 1.000 olayı uygular:

$$S_{10000} = f(Snapshot_{9000}, E_{9001}, \ldots, E_{10000})$$

Snapshot genellikle aggregate kimliğini, durum verisini, olay sürümünü ve snapshot şema sürümünü içerir. Olay sürümü özellikle önemlidir; çünkü Event Store’dan hangi noktadan sonraki olayların isteneceğini belirler.

```csharp
public async Task<BankAccount> Load(Guid accountId)
{
    var snapshot = await snapshotStore.GetLatest(accountId);

    var account = snapshot is null
        ? BankAccount.Empty(accountId)
        : BankAccount.FromSnapshot(snapshot.State);

    var version = snapshot?.EventVersion ?? 0;
    var events = await eventStore.ReadAfter(accountId, version);

    foreach (var domainEvent in events)
        account.Apply(domainEvent);

    return account;
}
```

Bu kod önce en güncel snapshot’ı arar. Snapshot yoksa boş aggregate oluşturur; varsa kaydedilmiş durumu kullanır. Daha sonra sadece snapshot sürümünden sonraki olayları okuyarak güncel duruma ulaşır.

## Snapshot ne zaman alınmalı?

Her olaydan sonra snapshot oluşturmak genellikle kötü fikirdir; yazma maliyetini artırır ve Event Sourcing’i pahalı bir “son durum tablosuna” dönüştürür. Yaygın stratejiler şunlardır:

- Her 100 veya 1.000 olayda bir snapshot almak
- Aggregate yükleme süresi belirli bir eşiği aşınca snapshot üretmek
- Snapshot işlemini arka plan göreviyle gerçekleştirmek
- Yalnızca yoğun kullanılan aggregate’lerde snapshot kullanmak

En uygun aralık ölçümle bulunur. Ortalama yükleme maliyeti kabaca olay uygulama maliyeti $c$, snapshot aralığı $k$ olmak üzere $O(kc)$ seviyesine indirilebilir. Ancak snapshot yazma ve saklama maliyeti de hesaba katılmalıdır.

## CQRS tarafındaki önemli ayrım

Snapshot, çoğunlukla **write model aggregate’ini** hızlı yeniden oluşturmak için kullanılır. CQRS read model’i zaten sorgulara uygun, önceden hesaplanmış görünümler barındırır. Bu nedenle snapshot ile projection veya materialized view aynı şey değildir.

| Kavram | Amaç | Kaynak |
|---|---|---|
| Snapshot | Aggregate’i hızlı yüklemek | Aggregate durumu |
| Projection | Sorgulanabilir görünüm üretmek | Olay akışı |
| Event Store | Gerçeğin kalıcı kaynağını tutmak | Tüm olaylar |

## Sürümleme ve güvenlik ağı

Aggregate yapısı değiştiğinde eski snapshot’lar uyumsuz kalabilir. Snapshot’a `schemaVersion` eklemek, uyumsuz kayıtları görmezden gelip olaylardan yeniden üretmek güvenli bir yaklaşımdır. Snapshot hiçbir zaman gerçeğin ana kaynağı olmamalıdır; silinse bile sistem olay geçmişinden toparlanabilmelidir.

Kısacası snapshot, geçmişi budayan bir testere değil, uzun bir kitabın arasına konan ayraçtır. Doğru yere konulduğunda Event Sourcing’in denetlenebilirlik avantajını korurken aggregate yükleme sürelerini ciddi biçimde azaltır.
