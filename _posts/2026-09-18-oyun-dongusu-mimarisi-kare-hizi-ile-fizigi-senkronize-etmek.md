---
layout: post
title: "Oyun Döngüsü Mimarisi: Kare Hızı ile Fiziği Senkronize Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - oyun geliştirme
  - game loop
  - fizik motoru
  - delta time
  - kare hızı
  - mimari
toc: true
image: /img/oyun-dongusu-mimarisi-26.png
---

Bir oyun çalışırken ekrandaki karakterler hareket eder, fizik hesaplanır, oyuncu girdileri okunur ve görüntü yeniden çizilir. Bütün bu işleri durmaksızın yöneten yapıya **oyun döngüsü**, yani *game loop* denir. Ancak ekran kartı saniyede 144 kare üretirken fiziğin aynı hızda güncellenmesi oyunu farklı bilgisayarlarda tutarsızlaştırabilir. Sağlam bir mimarinin sırrı, görüntüleme ile simülasyonu birbirinden ayırmaktır.


![oyun-dongusu-mimarisi-26](/img/oyun-dongusu-mimarisi-26.svg)

``

## Bir oyun döngüsünde neler olur?

En temel oyun döngüsü üç aşamadan oluşur:

1. Klavye, fare veya gamepad girdilerini oku.
2. Oyun durumunu ve fiziği güncelle.
3. Güncel durumu ekrana çiz.

Saf bir uygulama şöyle görünebilir:

```csharp
while (gameIsRunning)
{
    ProcessInput();
    Update();
    Render();
}
```

Buradaki problem `Update()` metodunun bilgisayarın hızına bağlı çalışmasıdır. Güçlü bir cihaz döngüyü daha sık tamamlar; dolayısıyla karakterler daha hızlı hareket edebilir. Oyun mantığı “her karede 2 metre ilerle” diyorsa kare hızı doğrudan oyun hızına dönüşür.

## Delta time yaklaşımı

İlk çözüm, önceki kareden beri geçen süreyi ölçmektir. Bu süreye **delta time** denir ve genellikle saniye cinsinden tutulur. Hareket denklemi şöyle yazılır:

$$x_{yeni} = x_{eski} + v \cdot \Delta t$$

Burada $v$ saniyedeki hız, $\Delta t$ ise iki kare arasındaki süredir. Örneğin hız $5\,m/s$ ve delta time $0.02$ saniyeyse nesne o karede $0.1$ metre ilerler.

```csharp
float deltaTime = timer.ElapsedSeconds;
timer.Restart();

player.Position += player.Velocity * deltaTime;
```

Bu yöntem animasyonlar ve kamera hareketleri için uygundur. Fakat değişken zaman adımı fizik simülasyonlarında kararsızlık yaratabilir. Kare aniden geciktiğinde büyük bir $\Delta t$ oluşur; çarpışmalar atlanabilir veya yay sistemleri patlamış mısır gibi sağa sola sıçrayabilir.

| Yaklaşım | Avantaj | Dezavantaj | Uygun kullanım |
|---|---|---|---|
| Kareye bağlı | Çok basit | Donanıma göre oyun hızı değişir | Prototip |
| Değişken delta time | Akıcı ve kolay | Fizik kararsızlaşabilir | Kamera, animasyon |
| Sabit zaman adımı | Tutarlı ve deterministik | Ek mimari gerektirir | Fizik, oyun kuralları |

## Sabit zaman adımı ve accumulator

Fiziği örneğin saniyede 60 kez çalıştırabiliriz. Bu durumda sabit adım:

$$dt = \frac{1}{60} \approx 0.01667\ saniye$$

Ekran ister 30 ister 165 FPS üretsin, fizik aynı büyüklükte adımlarla ilerler. Her gerçek karede geçen süre bir **accumulator** içinde biriktirilir. Birikmiş süre sabit adıma ulaştığında fizik güncellenir.

```csharp
double fixedDt = 1.0 / 60.0;
double accumulator = 0.0;
double previousTime = GetTime();

while (gameIsRunning)
{
    double currentTime = GetTime();
    double frameTime = currentTime - previousTime;
    previousTime = currentTime;

    // Donma sonrası yüzlerce fizik adımı oluşmasını engeller.
    frameTime = Math.Min(frameTime, 0.25);
    accumulator += frameTime;

    ProcessInput();

    while (accumulator >= fixedDt)
    {
        PreviousState = CurrentState;
        SimulatePhysics(fixedDt);
        accumulator -= fixedDt;
    }

    double alpha = accumulator / fixedDt;
    Render(Interpolate(PreviousState, CurrentState, alpha));
}
```

Kodda fizik yalnızca `fixedDt` ile ilerler. `frameTime` sınırı, pencere sürüklendiğinde veya hata ayıklayıcı durduğunda **ölüm spirali** oluşmasını önler. Ölüm spirali, gecikmeyi kapatmak için daha fazla güncelleme yapılması ve bu güncellemelerin daha da fazla gecikme üretmesidir.

## Enterpolasyon neden gerekli?

Fizik 60 Hz, ekran 144 Hz çalışıyorsa bazı görüntü kareleri arasında yeni fizik durumu bulunmaz. Doğrudan son durum çizilirse hareket küçük sıçramalarla görünür. Enterpolasyon, önceki ve mevcut fizik durumları arasında görsel bir ara nokta üretir:

$$x_{görsel} = (1-\alpha)x_{önceki} + \alpha x_{mevcut}$$

Bu işlem fiziği değiştirmez; yalnızca çizilen konumu yumuşatır. Böylece simülasyonun güvenilirliği ile yüksek yenileme hızlı monitörlerin akıcılığı aynı anda korunur.

## Pratik mimari önerisi

Girdi toplama ve çizim her karede, fizik ile kritik oyun kuralları sabit adımda çalışmalıdır. Ağ tabanlı veya tekrar oynatma özelliğine sahip projelerde sabit adım ayrıca deterministik sonuçları kolaylaştırır. Maksimum fizik güncellemesi sınırlandırılmalı, ağır işlemler profillenmeli ve render sistemi fizik durumunu doğrudan değiştirmemelidir.

Kısacası render “ne kadar hızlı yapabiliyorsan çiz”, fizik ise “daima aynı zaman adımıyla ilerle” ilkesini izlemelidir. Bu ayrım yapıldığında oyun, hem eski dizüstünde hem de ışıklı oyuncu bilgisayarında aynı kurallarla çalışır.
