---
layout: post
title: "Oyunlarda Mantıksal Zaman ve Olay Döngüsü: FPS Değişse de Dünya Neden Aynı Hızda Akmalı?"
math: true
categories: 
  - Bilgi
tags: 
  - oyun programlama
  - asenkron programlama
  - game loop
---

Bir oyunda ekrandaki kare sayısı artınca karakterinizin daha hızlı koşması, fizik hesaplarının farklı bilgisayarlarda bambaşka sonuçlar üretmesi veya ağdaki oyuncuların zaman çizelgelerinin ayrışması klasik zamanlama hatalarıdır. Bu sorunların ortak kaynağı, fiziksel zaman ile oyunun mantıksal zamanını birbirine karıştırmaktır. Sağlam bir oyun döngüsü, işlemcinin o anki hızından bağımsız biçimde olayları düzenler; asenkron işler sürerken ana oyun dünyasının tutarlı kalmasını sağlar.
<!--more-->

## İki saat, iki farklı sorumluluk

**Fiziksel zaman**, işletim sisteminin yüksek çözünürlüklü saatinden alınan gerçek geçen süredir. Bir karenin başlangıcı ile sonu arasında 16 ms de geçebilir, 45 ms de. **Mantıksal zaman** ise oyun dünyasının ilerlemesi için motorun tanımladığı soyut saattir. Örneğin fizik motoru her adımda tam 20 ms ilerletilebilir.

Kareye bağlı hareket yaklaşımı ilk bakışta masumdur:

```csharp
// Hatalı: FPS yükseldikçe karakter daha fazla hareket eder.
position += direction * speed;
```

Burada `Update` saniyede 30 kez çalışırsa başka, 144 kez çalışırsa başka mesafe alınır. Değişken zaman adımıyla doğru temel formül şudur:

$$x_{yeni} = x_{eski} + v \cdot \Delta t$$

```csharp
// Görsel ve genel oyun mantığı için uygundur.
void Update(float deltaTime)
{
    position += direction * speed * deltaTime;
}
```

Ancak `deltaTime` aniden çok büyürse çarpışma hesapları nesnelerin duvarın içinden geçmesine yol açabilir. Bu nedenle fizik ve deterministik kurallar çoğunlukla sabit zaman adımında yürütülür.

| Yaklaşım | Zaman adımı | Güçlü yanı | Risk / kullanım alanı |
|---|---:|---|---|
| Değişken adım | Her karede farklı | Akıcı görsel güncellemeler | Fizikte büyük sıçramalar yaratabilir |
| Sabit adım | Örn. 0,02 saniye | Tekrarlanabilir fizik | Yavaş cihazda biriken güncellemeler |
| Hibrit döngü | İkisini birlikte kullanır | Görsel kalite ve tutarlılık | Biriktirici yönetimi gerekir |

## Biriktirici: gerçek zamanı mantıksal tiklere çevirmek

Hibrit modelde gerçek zaman önce bir **accumulator** içinde toplanır. Biriktirilen süre sabit adımı geçtikçe fizik güncellemesi çalışır. Böylece 60 FPS ve 120 FPS çalışan iki makine, aynı koşullarda aynı sayıda mantıksal tik üretebilir.

```csharp
const float fixedStep = 0.02f;
float accumulator = 0f;

void Frame(float realDelta)
{
    accumulator += Math.Min(realDelta, 0.1f); // Dev sıçramaları sınırla.

    while (accumulator >= fixedStep)
    {
        SimulatePhysics(fixedStep);
        ProcessScheduledEvents(gameTime + fixedStep);
        gameTime += fixedStep;
        accumulator -= fixedStep;
    }

    float alpha = accumulator / fixedStep;
    Render(Interpolate(previousState, currentState, alpha));
}
```

Kodda `Math.Min`, pencere taşındığında veya uygulama kısa süre durakladığında oluşabilecek devasa zaman farkını sınırlar. `Interpolate` ise iki fizik durumu arasında görsel geçiş yaparak, fizik 50 Hz iken ekranın 144 Hz’de pürüzsüz görünmesine yardım eder.

## Olay döngüsü ve asenkron görevler

Oyunlar yalnızca hareket hesaplamaz: dosya yükler, sunucudan veri bekler, yapay zekâ üretir ve ses hazırlar. Bunların ana döngüyü kilitlemesi kare düşüşü demektir. Çözüm, uzun süren işi asenkron başlatmak; fakat oyun dünyasını yalnızca ana iş parçacığında değiştirmektir.

```csharp
async Task LoadLevelAsync(string levelName)
{
    ShowLoadingScreen();
    var levelData = await fileService.ReadLevelAsync(levelName);
    eventQueue.Enqueue(() => SpawnLevel(levelData));
}

void ProcessEvents()
{
    while (eventQueue.TryDequeue(out var gameEvent))
        gameEvent(); // Dünya durumunu güvenli noktada değiştirir.
}
```

`await` dosya okuma sürerken oyun döngüsünün çizim yapmasına izin verir. Görev tamamlandığında sonuç doğrudan rastgele bir anda fizik dünyasına uygulanmaz; olay kuyruğuna eklenir. Kuyruk, her tikte kontrollü biçimde tüketildiğinden sıra, hata ayıklama ve tekrar üretilebilirlik daha iyi korunur.

Pratikte olaylara mantıksal zaman damgası da eklenebilir: `event.time <= gameTime` olduğunda işlenir. Bu yaklaşım özellikle çok oyunculu oyunlarda gecikmiş paketleri düzenlemek için değerlidir. Kısacası gerçek zaman performansın gerçeğidir; mantıksal zaman ise oyunun gerçeğidir. İyi bir motor, ikisini aynı saat sanmak yerine aralarında disiplinli bir köprü kurar.
