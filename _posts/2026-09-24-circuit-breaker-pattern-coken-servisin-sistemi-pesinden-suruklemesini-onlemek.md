---
layout: post
title: "Circuit Breaker Pattern: Çöken Servisin Sistemi Peşinden Sürüklemesini Önlemek"
math: true
categories: 
  - Bilgi
tags: 
  - circuit breaker
  - mikroservis
  - dağıtık sistemler
  - dayanıklılık
  - hata yönetimi
  - javascript
toc: true
image: /img/circuit-breaker-pattern-70.png
---

Bir mikroservis çöktüğünde sorun çoğu zaman yalnızca o servisle sınırlı kalmaz. Ona istek gönderen uygulamalar yanıt bekler, bağlantı havuzları dolar, iş parçacıkları tükenir ve masum servisler de domino taşları gibi devrilmeye başlar. **Circuit Breaker Pattern**, elektrik sigortasına benzeyen bir koruma mekanizması kurarak bu zincirleme felaketi durdurur.
``
## Circuit Breaker neyi çözer?

Bir sipariş servisinin ödeme servisini çağırdığını düşünelim. Ödeme servisi yanıt veremiyorsa her isteği tekrar tekrar ona göndermek problemi çözmez; aksine ağ trafiğini ve kaynak tüketimini artırır. Circuit Breaker, belirli sayıdaki başarısızlıktan sonra çağrıları geçici olarak engeller ve hızlı hata döndürür.

Bir çağrının ortalama bekleme süresi $T$, eş zamanlı istek sayısı $N$ ise bloke edilen toplam kaynak baskısını kabaca şöyle düşünebiliriz:

$$Yuk = N \times T$$

Örneğin 500 istek 10 saniye boyunca beklerse sistemde $5000$ istek-saniyelik baskı oluşur. Devre açıkken çağrının 10 milisaniyede reddedilmesi bu maliyeti dramatik biçimde azaltır.

## Üç temel durum

Circuit Breaker küçük bir durum makinesi olarak çalışır:

| Durum | Davranış | Geçiş koşulu |
|---|---|---|
| **Closed** | İstekler hedef servise gider | Hata eşiği aşılırsa Open |
| **Open** | İstekler gönderilmeden reddedilir | Bekleme süresi dolunca Half-Open |
| **Half-Open** | Sınırlı sayıda deneme yapılır | Başarılıysa Closed, hatalıysa Open |

![circuit-breaker-pattern-70](/img/circuit-breaker-pattern-70.svg)


İsimler ilk bakışta ters gelebilir. Elektrik devresinde **closed**, akımın geçtiği; **open** ise akımın kesildiği durumdur. Burada “akım”, servis çağrılarıdır.

Hata oranı $E$, başarısız çağrı sayısı $F$ ve toplam çağrı sayısı $R$ ile hesaplanabilir:

$$E = \frac{F}{R} \times 100$$

Son 20 çağrının 12’si başarısızsa hata oranı yüzde 60’tır. Eşik yüzde 50 olarak ayarlanmışsa devre açılabilir. Ancak yalnızca oran kullanmak risklidir: İki çağrıdan birinin başarısız olması da yüzde 50 eder. Bu nedenle minimum örnek sayısı belirlemek önemlidir.

## JavaScript ile sade bir uygulama

Aşağıdaki sınıf, art arda gelen hataları sayar; eşik aşılınca çağrıları durdurur ve belirlenen sürenin ardından kontrollü bir denemeye izin verir:

```javascript
class CircuitBreaker {
  constructor(action, threshold = 3, resetTime = 5000) {
    this.action = action;
    this.threshold = threshold;
    this.resetTime = resetTime;
    this.failures = 0;
    this.state = "CLOSED";
    this.openedAt = null;
  }

  async execute(...args) {
    if (this.state === "OPEN") {
      const elapsed = Date.now() - this.openedAt;
      if (elapsed < this.resetTime) {
        throw new Error("Devre açık: çağrı engellendi");
      }
      this.state = "HALF_OPEN";
    }

    try {
      const result = await this.action(...args);
      this.failures = 0;
      this.state = "CLOSED";
      return result;
    } catch (error) {
      this.failures++;
      if (this.state === "HALF_OPEN" || this.failures >= this.threshold) {
        this.state = "OPEN";
        this.openedAt = Date.now();
      }
      throw error;
    }
  }
}
```

Sınıf gerçek projelerde zaman aşımı, kayan pencere, eş zamanlı Half-Open denemelerini sınırlama ve metrik toplama gibi özelliklerle genişletilmelidir. Hazır çözümler için Java ekosisteminde Resilience4j, .NET tarafında Polly kullanılabilir.

## Retry ile aynı şey mi?

| Yaklaşım | Temel amaç | Hatalı kullanım riski |
|---|---|---|
| Retry | Geçici hatada çağrıyı yinelemek | Çöken servise daha fazla yük bindirmek |
| Timeout | Sonsuz beklemeyi engellemek | Çok kısa sürede geçerli çağrıları kesmek |
| Circuit Breaker | Arızalı hedefe trafiği durdurmak | Yanlış eşikle devreyi gereksiz açmak |
| Fallback | Alternatif yanıt üretmek | Eski veya eksik veri sunmak |

Bu desenler rakip değil, ekip arkadaşıdır. İyi bir akışta önce timeout uygulanır, yalnızca geçici hatalar dikkatli biçimde retry edilir, hata yoğunluğu artarsa devre açılır ve mümkünse önbellekten fallback yanıtı sunulur.

## Sonuç

Circuit Breaker bozuk servisi tamir etmez; sistemin geri kalanına nefes alacak alan kazandırır. Başarı için eşikleri trafik karakterine göre ayarlamak, devre durumlarını izlemek ve alarm üretmek gerekir. Çünkü dağıtık sistemlerde soru “Bir servis çöker mi?” değil, “Çöktüğünde sistem ne kadar zarif davranır?” olmalıdır.
