---
layout: post
title: "Mutex vs Spinlock: Beklemek mi, Boşuna Dönmek mi Daha Maliyetli?"
math: true
categories: 
  - Bilgi
tags: 
  - mutex
  - spinlock
  - eşzamanlılık
  - çok çekirdekli programlama
  - performans
  - c++
toc: true
image: /img/mutex-vs-spinlock-63.png
---

Çok çekirdekli bir sistemde iki iş parçacığı aynı veriye uzandığında küçük bir trafik kavşağı oluşur. Mutex kırmızı ışıkta motoru kapatıp beklemeye, spinlock ise ışık yeşile dönene kadar gaza basmadan motoru çalıştırmaya benzer. Hangisinin daha hızlı olduğu, kilidin ne kadar süre tutulduğuna ve işletim sisteminin bekletme maliyetine bağlıdır.

``

## Temel fark: Uyku mu, aktif bekleme mi?

Bir **mutex** alınamıyorsa bekleyen iş parçacığı çoğunlukla işletim sistemi tarafından uyutulur. Böylece işlemci başka işler çalıştırabilir. Ancak uyutma ve yeniden uyandırma; sistem çağrıları, zamanlayıcı müdahalesi ve bağlam değişimi gibi maliyetler doğurur.

Bir **spinlock** ise iş parçacığını uyutmaz. İş parçacığı kilidi tekrar tekrar kontrol ederek işlemci üzerinde aktif kalır. Kilit birkaç nanosaniye sonra açılacaksa bu yaklaşım oldukça hızlıdır. Bekleme uzarsa işlemci zamanı ve enerji boşa harcanır.

| Özellik | Mutex | Spinlock |
|---|---|---|
| Bekleme biçimi | İş parçacığını uyutabilir | Aktif döngüde bekler |
| CPU tüketimi | Beklerken düşüktür | Beklerken yüksektir |
| Kısa kritik bölüm | Ek yük oluşturabilir | Genellikle avantajlıdır |
| Uzun kritik bölüm | Genellikle avantajlıdır | Oldukça maliyetlidir |
| Tek çekirdekli sistem | Kullanılabilir | Çoğu durumda anlamsızdır |
| Kesme bağlamı | Genellikle uygun değildir | Çekirdek kodunda kullanılabilir |

![mutex-vs-spinlock-63](/img/mutex-vs-spinlock-63.svg)


## Maliyetin matematiği

Spinlock seçiminin mantıklı olması için bekleme maliyetinin uyutma maliyetinden küçük olması beklenir. Basitleştirilmiş karar koşulu şöyledir:

$$T_{bekleme} < T_{uyutma} + T_{uyandırma}$$

Kilit ortalama $T_k$ süre tutuluyor ve kilidi dolu bulma olasılığı $P_c$ ise spinlock için yaklaşık bekleme maliyeti $P_c \times T_k$ olarak düşünülebilir. Mutex tarafında ise bağlam değiştirme maliyeti devreye girer. Modern sistemlerde bu değerler sabit değildir; çekirdek sayısı, önbellek mimarisi ve sistem yükü sonucu değiştirir.

Spinlock yalnızca döngü maliyeti de değildir. Kilit değişkeninin farklı çekirdeklerin önbellekleri arasında taşınması **cache coherence** trafiği oluşturur. Çok sayıda çekirdek aynı bellek satırını izliyorsa küçücük bir atomik değişken, sistemin en popüler dedikodu konusu hâline gelebilir.

## C++ ile iki yaklaşım

Aşağıdaki basit spinlock, `atomic_flag` kullanarak kilidi atomik biçimde almaya çalışır. `yield`, işletim sistemine başka bir iş parçacığını çalıştırabileceğini söyler; fakat kilidi gerçek anlamda uyuyan bir mutex hâline getirmez.

```cpp
#include <atomic>
#include <thread>

class SpinLock {
    std::atomic_flag locked = ATOMIC_FLAG_INIT;

public:
    void lock() {
        while (locked.test_and_set(std::memory_order_acquire)) {
            std::this_thread::yield();
        }
    }

    void unlock() {
        locked.clear(std::memory_order_release);
    }
};
```

Aynı kritik bölüm standart mutex ile daha güvenli ve okunaklı biçimde korunabilir:

```cpp
#include <mutex>

std::mutex mutex;
int counter = 0;

void increment() {
    std::lock_guard<std::mutex> guard(mutex);
    ++counter; // Paylaşılan veriyi güvenle günceller.
}
```

`std::lock_guard`, fonksiyondan istisnayla çıkılsa bile mutex kilidini otomatik bırakır. Üretim kodunda bu RAII yaklaşımı, elle `lock` ve `unlock` çağırmaktan daha güvenlidir.

## Hangisini ne zaman seçmeli?

Kritik bölüm birkaç atomik işlem kadar kısaysa, çekirdek sayısı yeterliyse ve çakışma düşükse spinlock avantaj sağlayabilir. İşlem bloklayıcı G/Ç yapıyor, bellek ayırıyor veya süresi öngörülemeyen başka kodlar çağırıyorsa mutex daha doğru seçimdir. Spinlock tutulurken uyumak ise performans felaketinin davetiyesidir.

Modern mutex uygulamalarının önce kısa süre dönüp sonra uyuyan **adaptif** stratejiler kullanabildiğini de unutmayın. Dolayısıyla teorik tahmin tek başına yeterli değildir. Gerçek iş yükünü benchmark ve profiler ile ölçün. En hızlı kilit bazen spinlock, bazen mutex; çoğu zamansa paylaşılan veriyi azaltarak hiç ihtiyaç duymadığınız kilittir.
