---
layout: post
title: "C# ile Multithreading: TPL, Task ve async/await Rehberi"
math: true
categories: 
  - Program
tags: 
  - csharp
  - multithreading
  - tpl
  - async
  - await
  - paralel-programlama
toc: true
image: /img/c-ile-multithreading-31.png
---

Bir uygulamanın aynı anda birden fazla iş yapabilmesi kulağa sihir gibi gelebilir; ancak C# dünyasında bu sihrin arkasında iş parçacıkları, görevler ve dikkatli bir zamanlama mekanizması bulunur. Task Parallel Library (TPL) CPU ağırlıklı işleri paralelleştirirken `async/await`, özellikle dosya, ağ ve veritabanı gibi beklemeli işlemlerde iş parçacıklarını gereksiz yere meşgul etmeden ölçeklenebilir uygulamalar kurmamızı sağlar.
``
## Eşzamanlılık ve paralellik aynı şey değildir

Eşzamanlılık, birden fazla işin zaman aralıkları iç içe geçecek şekilde ilerlemesidir. Paralellik ise bu işlerin gerçekten aynı anda, örneğin farklı işlemci çekirdeklerinde çalışmasıdır.

| Kavram | Temel amaç | Uygun iş türü | C# aracı |
|---|---|---|---|
| Eşzamanlılık | Beklerken başka işe geçmek | Ağ, dosya, veritabanı | `async/await` |
| Paralellik | Hesabı çekirdeklere dağıtmak | Görüntü işleme, hesaplama | `Parallel`, TPL |
| İş parçacığı | Çalıştırma kaynağı sağlamak | Düşük seviyeli kontrol | `Thread` |
| Görev | Yapılacak işi temsil etmek | Modern iş akışları | `Task` |

Bir işin tek çekirdekte tamamlanma süresi $T_1$, $p$ çekirdekteki süresi $T_p$ ise teorik hızlanma şöyle ifade edilir:

$$S_p = \frac{T_1}{T_p}$$

İdeal durumda $S_p \approx p$ beklenir. Gerçekte görev oluşturma maliyeti, senkronizasyon ve paylaşılan kaynaklar nedeniyle bu değere nadiren ulaşılır.

## TPL ile CPU ağırlıklı işleri çalıştırmak

TPL, görevlerin uygun iş parçacıklarına dağıtılmasını `ThreadPool` üzerinden yönetir. Böylece her iş için elle `Thread` oluşturmak gerekmez.

```csharp
using System;
using System.Linq;
using System.Threading.Tasks;

int[] sayilar = Enumerable.Range(1, 8).ToArray();

Parallel.ForEach(sayilar, sayi =>
{
    double sonuc = Math.Sqrt(sayi) * Math.Pow(sayi, 3);
    Console.WriteLine($"{sayi}: {sonuc} - Thread: {Environment.CurrentManagedThreadId}");
});
```

`Parallel.ForEach`, koleksiyondaki hesaplamaları mümkün olduğunda farklı iş parçacıklarında yürütür. Ancak çok küçük işlemleri paralelleştirmek, yönetim maliyeti yüzünden normal bir döngüden daha yavaş olabilir. Önce ölçmek, sonra paralelleştirmek altın kuraldır.

Bağımsız görevleri başlatıp hepsinin bitmesini beklemek için `Task.WhenAll` kullanılabilir:

```csharp
Task<int> hesap1 = Task.Run(() => Enumerable.Range(1, 1_000_000).Sum());
Task<int> hesap2 = Task.Run(() => Enumerable.Range(1, 500_000).Sum());

int[] sonuclar = await Task.WhenAll(hesap1, hesap2);
Console.WriteLine($"Toplam: {sonuclar.Sum()}");
```

`Task.Run`, CPU ağırlıklı senkron kodu ThreadPool üzerinde çalıştırır. Buna karşılık zaten asenkron olan HTTP veya veritabanı çağrılarını ayrıca `Task.Run` içine koymak genellikle gereksizdir.

## async/await ile beklerken kaynak tüketmemek

`async`, metodun asenkron işlem içerebildiğini; `await` ise işlem tamamlanana kadar kontrolün çağırana geri verilebileceğini belirtir. Bu sırada iş parçacığının bloklanması gerekmez.

```csharp
using System.Net.Http;

static async Task<int> SayfaBoyutuAsync(
    string adres,
    CancellationToken iptal)
{
    using HttpClient istemci = new();
    string icerik = await istemci.GetStringAsync(adres, iptal);
    return icerik.Length;
}

using CancellationTokenSource kaynak = new();
kaynak.CancelAfter(TimeSpan.FromSeconds(5));

try
{
    int boyut = await SayfaBoyutuAsync("https://example.com", kaynak.Token);
    Console.WriteLine($"İndirilen karakter: {boyut}");
}
catch (OperationCanceledException)
{
    Console.WriteLine("İşlem iptal edildi.");
}
```

Buradaki `CancellationToken`, uzun süren işlemin kontrollü biçimde durdurulmasını sağlar. `await` edilen görev hata üretirse istisna normal bir senkron metottaki gibi `try/catch` ile yakalanabilir.

## Paylaşılan veriler ve yarış durumları

Birden fazla görev aynı değişkeni değiştirirse sonuç öngörülemez olabilir. Örneğin `sayac++` atomik değildir; okuma, artırma ve yazma adımlarından oluşur. Güvenli artırma için `Interlocked.Increment(ref sayac)` veya daha karmaşık kritik bölgelerde `lock` kullanılmalıdır.

Modern C# kodunda temel yaklaşım basittir: I/O ağırlıklı işlemlerde doğal asenkron API’leri `await` edin, CPU ağırlıklı ve bağımsız hesaplamalarda TPL kullanın, paylaşılan durumu azaltın ve performans kararlarını mutlaka ölçümlerle doğrulayın.

![c-ile-multithreading-31](/img/c-ile-multithreading-31.svg)

