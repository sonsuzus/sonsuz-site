---
layout: post
title: "Circuit Breaker Deseni: Mikroservislerde Arızayı İzole Etmenin Akıllı Yolu"
math: true
categories: 
  - Bilgi
tags: 
  - mikroservisler
  - design patterns
  - circuit breaker
image: /img/circuit-breaker-deseni-24.png
---

![circuit-breaker-deseni-24](/img/circuit-breaker-deseni-24.svg)


Dağıtık sistemlerde en tehlikeli hata, tek bir servisin yavaşlamasının veya çökmesinin domino taşı gibi tüm uygulamayı devirmesidir. Circuit Breaker deseni, sorunlu bir bağımlılığa yapılan çağrıları geçici olarak keserek kaynak tüketimini sınırlar, hatayı izole eder ve sistemin geri kalanının nefes almasını sağlar.
``
Bir e-ticaret uygulamasını düşünelim: Sipariş servisi, ödeme sağlayıcısına istek gönderiyor. Ödeme API'si yavaşladığında sipariş servisindeki istekler bekler, thread havuzu dolar ve sonunda ürün kataloğu gibi tamamen alakasız görünen uçlar bile cevap veremez. Buna **cascading failure** yani zincirleme arıza denir. Circuit Breaker, belirli hata eşiği aşıldığında ödeme API'sine yeni istek göndermeyi bırakır. Böylece başarısız olmaya mahkûm çağrılar sistemi tüketmez.

Desen, elektrik sigortasına benzer biçimde üç durumla çalışır: **Closed**, **Open** ve **Half-Open**. Closed durumunda çağrılar normal biçimde hedef servise gider. Hata oranı veya ardışık hata sayısı eşik değerini aşarsa devre Open olur. Bu aşamada çağrı daha hedefe ulaşmadan hızlıca reddedilir; buna *fail fast* yaklaşımı denir. Belirli bir bekleme süresinden sonra Half-Open durumuna geçilir ve sınırlı sayıda deneme isteği gönderilir. Denemeler başarılıysa devre tekrar Closed olur; başarısızsa Open durumuna geri döner.

| Durum | İstek davranışı | Geçiş koşulu | Amaç |
|---|---|---|---|
| Closed | İstek hedef servise gönderilir | Hata eşiği aşılırsa Open | Normal çalışma |
| Open | İstek anında reddedilir veya fallback döner | Bekleme süresi bitince Half-Open | Kaynakları korumak |
| Half-Open | Kontrollü deneme istekleri gönderilir | Başarıda Closed, hatada Open | Servisin iyileşmesini ölçmek |

Devrenin açılma kararını yalnızca hata adediyle vermek her zaman doğru değildir. Hata oranı, gecikme ve gözlem penceresi birlikte değerlendirilmelidir. Basit bir hata oranı şöyle ifade edilir:

$$Hata\ Oranı = \frac{başarısız\ istek\ sayısı}{toplam\ istek\ sayısı} \times 100$$

Örneğin son 30 saniyede en az 20 istek geldiyse ve hata oranı %50'yi geçtiyse devreyi açmak mantıklı olabilir. Ancak bu değerler evrensel değildir: kritik ödeme işlemleri ile öneri motorunun hata toleransı aynı olmaz. Eşikler, servis sözleşmesine ve gözlemlenen üretim verilerine göre ayarlanmalıdır.

Java ekosisteminde Resilience4j bu deseni uygulanabilir hale getirir. Aşağıdaki örnek, uzak ödeme çağrısını korur ve hata oluştuğunda yerel bir fallback üretir:

```java
CircuitBreaker breaker = CircuitBreaker.ofDefaults("paymentService");

Supplier<String> protectedCall = CircuitBreaker.decorateSupplier(
    breaker,
    () -> paymentClient.charge(orderId)
);

try {
    return protectedCall.get();
} catch (CallNotPermittedException ex) {
    return "Ödeme sistemi geçici olarak erişilemez.";
} catch (Exception ex) {
    return "Ödeme doğrulanamadı; sipariş beklemeye alındı.";
}
```

Burada `decorateSupplier`, uzak çağrıyı devre kesiciyle sarar. Devre açıksa `CallNotPermittedException` hızlıca fırlatılır; ağda boşuna zaman kaybedilmez. Fallback ise rastgele bir başarı mesajı olmamalıdır. Siparişi beklemeye almak, önbellekten son bilinen veriyi döndürmek veya kullanıcıya yeniden deneme seçeneği sunmak gibi **iş kurallarına uygun** bir yanıt vermelidir.

Circuit Breaker, retry, timeout ve bulkhead ile birlikte daha güçlüdür. Timeout olmayan bir devre kesici, çok geç hata alabilir; sınırsız retry ise arızalı servise yük bindirir. Bulkhead ise her bağımlılığın kaynak havuzunu ayırarak bir servisin tüm thread'leri tüketmesini önler.

| Teknik | Çözdüğü temel problem | Circuit Breaker ile ilişkisi |
|---|---|---|
| Timeout | Sonsuza yakın bekleme | Hataların hızlı algılanmasını sağlar |
| Retry | Geçici ağ hataları | Sınırlı kullanılmalıdır; aksi halde yükü artırır |
| Bulkhead | Kaynakların ortaklaşa tükenmesi | Arıza izolasyonunu kaynak seviyesine taşır |
| Fallback | Kullanıcı deneyiminin bozulması | Devre açıkken anlamlı yanıt üretir |

Son olarak metrikleri izleyin: açık devre sayısı, başarısız çağrı oranı, Half-Open başarıları ve fallback kullanım oranı alarm üretmelidir. Circuit Breaker bir hatayı gizleme aracı değil, arızayı kontrollü biçimde görünür kılan ve yayılmasını engelleyen bir dayanıklılık mekanizmasıdır.
