---
layout: post
title: "Condition Variable: Thread’ler Birbirini Nasıl Bekler?"
math: true
categories: 
  - Bilgi
tags: 
  - condition-variable
  - thread
  - eşzamanlılık
  - cpp
  - mutex
  - senkronizasyon
toc: true
---

Bir thread’in sürekli “Hazır mı? Hazır mı? Şimdi hazır mı?” diye kontrol yapması, işlemciyi gereksiz yere meşgul eden dijital bir sabırsızlıktır. **Condition variable**, thread’lerin belirli bir koşul gerçekleşene kadar verimli biçimde uyumasını ve koşul değiştiğinde yeniden çalışmasını sağlayan bir senkronizasyon aracıdır.
``
## Temel problem: Beklerken ne yapmalıyız?

Bir üretici thread’in veri hazırladığını, tüketici thread’in ise bu veriyi işlediğini düşünelim. Tüketici, veri hazır değilken aşağıdaki gibi sürekli kontrol yapabilir:

```cpp
while (!veri_hazir) {
    // Kontrol etmeye devam et
}
```

Bu yönteme **busy waiting** denir. Thread çalışmayı bırakmadığı için CPU zamanı tüketir. Condition variable kullanıldığında ise tüketici uyutulur; böylece işlemci başka işler yapabilir.

Kabaca işlem maliyetini şöyle ifade edebiliriz:

$$
Maliyet_{busy} \approx kontrol\_sayisi \times kontrol\_maliyeti
$$

Condition variable yaklaşımında maliyet daha çok uyutma ve uyandırma işlemlerine bağlıdır:

$$
Maliyet_{cv} \approx uyutma + uyandirma + kilitleme
$$

Uzun veya belirsiz bekleme sürelerinde ikinci yaklaşım genellikle çok daha verimlidir.

| Yaklaşım | CPU kullanımı | Tepki süresi | Kullanım alanı |
|---|---:|---:|---|
| Busy waiting | Yüksek | Çok düşük olabilir | Çok kısa beklemeler |
| Condition variable | Düşük | Zamanlayıcıya bağlı | Kuyruklar ve iş parçacığı havuzları |
| Sabit süre uyuma | Düşük | Gereksiz gecikmeli | Basit ama hassas olmayan işler |

## Üçlü ekip: Durum, mutex ve condition variable

Condition variable tek başına bir koşulu saklamaz. “Veri hazır mı?” bilgisini ayrı bir değişken tutar. Bu paylaşılan durumu korumak için **mutex**, değişikliği bekleyen thread’leri yönetmek için de **condition variable** kullanılır.

Bekleyen thread’in yaptığı işlem atomik bir mantığa sahiptir:

1. Mutex’i kilitler.
2. Koşulu kontrol eder.
3. Koşul yanlışsa mutex’i bırakıp uyur.
4. Uyandırıldığında mutex’i tekrar kilitler.
5. Koşulu yeniden kontrol eder.

Mutex’in bekleme sırasında bırakılması kritiktir. Aksi hâlde üretici kilidi alamaz, durumu değiştiremez ve herkes sonsuza kadar bekler: tam bir senkronizasyon trajedisi!

## C++ ile üretici-tüketici örneği

```cpp
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>

std::queue<int> kuyruk;
std::mutex mtx;
std::condition_variable cv;
bool tamamlandi = false;

void uretici() {
    for (int i = 1; i <= 5; ++i) {
        {
            std::lock_guard<std::mutex> kilit(mtx);
            kuyruk.push(i);
        }
        cv.notify_one(); // Bir tüketiciyi uyandırır
    }

    {
        std::lock_guard<std::mutex> kilit(mtx);
        tamamlandi = true;
    }
    cv.notify_all(); // Bekleyen herkes durumu tekrar kontrol eder
}

void tuketici() {
    while (true) {
        std::unique_lock<std::mutex> kilit(mtx);

        cv.wait(kilit, [] {
            return !kuyruk.empty() || tamamlandi;
        });

        if (kuyruk.empty() && tamamlandi)
            break;

        int veri = kuyruk.front();
        kuyruk.pop();
        kilit.unlock();

        std::cout << "İşlenen veri: " << veri << '\n';
    }
}
```

`wait`, koşul yanlışken mutex’i bırakıp thread’i uyutur. Uyandırıldığında mutex’i yeniden edinir ve lambda ifadesini tekrar çalıştırır. `unique_lock` kullanılmasının nedeni, condition variable’ın kilidi geçici olarak açıp yeniden kapatabilmesidir.

## Neden koşul tekrar kontrol edilir?

Bir thread bildirim gelmeden de uyanabilir. Buna **spurious wakeup**, yani sahte uyanma denir. Ayrıca birden fazla tüketici uyandığında veriyi ilk davranan thread almış olabilir. Bu nedenle bekleme mantığı `if` değil, kavramsal olarak `while` olmalıdır:

```cpp
while (!kosul) {
    cv.wait(kilit);
}
```

Predicate alan `wait` sürümü bu döngüyü bizim için gerçekleştirir.

## `notify_one` mı, `notify_all` mı?

| Fonksiyon | Davranış | Tercih nedeni |
|---|---|---|
| `notify_one()` | Tek bir thread’i uyandırır | Tek iş veya tek kaynak hazırsa |
| `notify_all()` | Tüm bekleyenleri uyandırır | Kapanış ya da herkesi ilgilendiren durum değişiminde |

Özetle condition variable bir “olay oldu” mesajından çok, “durum değişmiş olabilir, tekrar kontrol et” zilidir. Doğru koşul değişkeni, mutex ve predicate birleşimi; yarış koşullarını önlerken CPU’nun boş yere maraton koşmasına da engel olur.
