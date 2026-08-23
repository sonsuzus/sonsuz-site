---
layout: post
title: "Circuit Breaker Deseni: Zincirleme Hatalara Karşı Sistem Sigortası"
math: true
categories: 
  - Bilgi
tags: 
  - circuit breaker
  - mikroservisler
  - dayanıklılık
  - yazılım mimarisi
toc: true
---

Dağıtık sistemlerde bir servisin yavaşlaması, yalnızca o servisin problemi olarak kalmaz. Ödeme API’sini bekleyen sipariş servisi, sipariş servisini bekleyen sepet uygulaması ve en sonunda kullanıcı deneyimi etkilenir. Circuit Breaker (devre kesici) deseni, başarısız çağrıları sonsuza dek tekrarlamak yerine bağlantıyı geçici olarak keserek kaynakları koruyan bir dayanıklılık yaklaşımıdır. Elektrik sigortası nasıl aşırı yükte devreyi kapatıyorsa, yazılımsal devre kesici de sorunlu bağımlılığa yapılan çağrıları kontrollü biçimde durdurur.
``

## Neden yalnızca `try/catch` yeterli değildir?

`try/catch`, tek bir isteğin hatasını yakalar; fakat bağımlı sistemin kalıcı biçimde erişilemez olduğunu anlayıp gelecekteki çağrıları önlemez. Örneğin bir envanter servisi 10 saniye içinde yanıt veriyorsa, uygulama sunucusundaki yüzlerce istek bu süre boyunca bağlantı, iş parçacığı ve bellek tüketebilir. Buna **cascading failure** (zincirleme hata) denir.

Bir bağımlılığın başarısızlık oranını kabaca şöyle tanımlayabiliriz:

$$FailureRate = \frac{Başarısız\ İstek\ Sayısı}{Toplam\ İstek\ Sayısı} \times 100$$

Belirli bir zaman penceresinde bu oran eşik değeri geçerse devre açılır. Örneğin son 20 isteğin 12’si başarısızsa, $FailureRate = 60\%$ olur. Eşik %50 ise artık uzak servise gerçek istek göndermek yerine hızlıca alternatif yanıta dönmek daha sağlıklıdır.

## Devre kesicinin üç durumu

Circuit Breaker, basit bir `if` kontrolünden çok küçük bir durum makinesidir. Temel durumları aşağıdaki gibidir:

| Durum | Davranış | Amaç |
|---|---|---|
| **Closed (Kapalı)** | İstekler normal şekilde hedef servise gider. | Sistemin sağlıklı çalışmasına izin vermek. |
| **Open (Açık)** | İstekler hedefe gitmeden hemen reddedilir veya fallback çalışır. | Kaynak tüketimini ve hata yayılımını engellemek. |
| **Half-Open (Yarı Açık)** | Sınırlı sayıda test isteği hedefe gönderilir. | Servisin iyileşip iyileşmediğini ölçmek. |

Kapalı durumdaki hata sayısı eşiği aşınca devre açılır. Bir bekleme süresi sonunda yarı açık duruma geçilir. Deneme isteği başarılıysa devre tekrar kapanır; başarısızsa yeniden açılır. Bu akış, sistemin hem kendini korumasını hem de iyileşen bağımlılığı otomatik olarak yeniden kullanmasını sağlar.

## Basit bir TypeScript örneği

Aşağıdaki örnek, eğitim amaçlı sadeleştirilmiş bir devre kesici sınıfıdır. Gerçek projelerde Resilience4j, Polly veya opossum gibi olgun kütüphaneler tercih edilebilir.

```ts
class CircuitBreaker {
  private failures = 0;
  private state: "CLOSED" | "OPEN" = "CLOSED";
  private openedAt = 0;

  constructor(
    private readonly threshold = 3,
    private readonly resetTimeoutMs = 5000
  ) {}

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    const canRetry = Date.now() - this.openedAt > this.resetTimeoutMs;

    if (this.state === "OPEN" && !canRetry) {
      throw new Error("Circuit açık: fallback kullanılmalı");
    }

    try {
      const result = await operation();
      this.failures = 0;
      this.state = "CLOSED";
      return result;
    } catch (error) {
      this.failures++;
      if (this.failures >= this.threshold) {
        this.state = "OPEN";
        this.openedAt = Date.now();
      }
      throw error;
    }
  }
}
```

Bu kod, art arda üç hata sonrasında çağrıları beş saniye boyunca keser. Süre dolunca yeni bir istek gönderilmesine izin verir; başarılı olursa sayaç sıfırlanır. Üretimde buna yarı açık durum için sınırlı deneme sayısı da eklenmelidir.

## Fallback, timeout ve gözlemlenebilirlik

Circuit Breaker tek başına sihirli bir kalkan değildir. Özellikle timeout ile birlikte kullanılmalıdır; aksi halde devrenin hata sayması için isteklerin bitmesini uzun süre beklemek gerekir. Ayrıca fallback, her zaman “boş veri” demek değildir: önbellekteki son ürün fiyatını göstermek, isteği kuyruğa almak veya kullanıcıya açık bir bakım mesajı sunmak olabilir.

| Mekanizma | Çözdüğü problem | Örnek |
|---|---|---|
| Timeout | Sonsuz/yavaş bekleme | 2 saniye sonra isteği iptal etmek |
| Retry | Geçici ağ hatası | Kısa gecikmeyle 2 tekrar yapmak |
| Circuit Breaker | Sürekli arızalı bağımlılık | Çağrıları geçici olarak kesmek |
| Fallback | Kontrollü kullanıcı deneyimi | Önbellekten sonuç döndürmek |

Son olarak metrikleri izleyin: açık devre sayısı, hata oranı, fallback kullanım oranı ve gecikme süreleri mimarinin nabzını tutar. Doğru eşikler, kısa ama gerçekçi timeout’lar ve anlamlı fallback’lerle Circuit Breaker, dağıtık sisteminizin panik anında sakin kalmasını sağlar.
