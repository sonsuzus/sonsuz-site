---
layout: post
title: "Semaphore ve Mutex: Ortak Kaynakları Paylaşmanın İki Farklı Yolu"
math: true
categories: 
  - Bilgi
tags: 
  - semaphore
  - mutex
  - eşzamanlılık
  - thread
  - senkronizasyon
  - c++
toc: true
image: /img/semaphore-ve-mutex-16.png
---

Birden fazla thread aynı veriye, dosyaya veya bağlantıya aynı anda ulaşmak istediğinde küçük bir trafik kaosu doğar. Bu kaosu yönetmek için kullanılan en temel araçlardan ikisi **mutex** ve **semaphore**’dur. İkisi de erişimi sınırlar; ancak mutex tek anahtarlı bir oda kapısı gibi davranırken semaphore belirli sayıda araç kabul eden bir otoparka benzer.

![semaphore-ve-mutex-16](/img/semaphore-ve-mutex-16.svg)

``
## Önce problem: Race condition

Paylaşılan bir sayaç üzerinde şu işlemin yapıldığını düşünelim:

$$x = x + 1$$

Bu ifade tek adım gibi görünse de işlemci açısından genellikle üç aşamadır: değeri oku, artır ve geri yaz. İki thread aynı anda eski değeri okursa artışlardan biri kaybolabilir. Buna **race condition** denir.

Kritik bölgeye aynı anda girebilen thread sayısını $N$ ile gösterirsek mutex için temel kural şöyledir:

$$N \leq 1$$

Sayaçlı semaphore içinse başlangıç kapasitesi $K$ olmak üzere:

$$N \leq K$$

Yani mutex yalnızca tek bir yürütme akışına izin verirken semaphore kapasite kadar eş zamanlı erişim sağlayabilir.

## Mutex: Tek anahtar, tek sahip

**Mutex** kelimesi “mutual exclusion”, yani karşılıklı dışlama kavramından gelir. Bir thread mutex’i kilitlediğinde diğerleri kilit açılana kadar bekler. Ayrıca mutex’in önemli bir **sahiplik** kuralı vardır: Kilidi alan thread, kilidi açmalıdır.

Aşağıdaki C++ örneğinde sayaç güvenli biçimde artırılır:

```cpp
#include <iostream>
#include <mutex>
#include <thread>

std::mutex counterMutex;
int counter = 0;

void increment() {
    for (int i = 0; i < 1000; ++i) {
        std::lock_guard<std::mutex> lock(counterMutex);
        ++counter;
    } // lock_guard burada kilidi otomatik bırakır
}

int main() {
    std::thread first(increment);
    std::thread second(increment);

    first.join();
    second.join();
    std::cout << counter << '\n';
}
```

`std::lock_guard`, kapsam sona erdiğinde kilidi otomatik açar. Böylece hata, erken `return` veya exception durumlarında kilidin unutulması önlenir. Bu yaklaşım **RAII** adı verilen kaynak yönetimi tekniğine dayanır.

## Semaphore: Birden fazla geçiş kartı

**Semaphore**, kullanılabilir izinlerin sayısını tutan bir sayaçtır. Bir thread izin aldığında sayaç azalır; işi bitirip izin verdiğinde artar. Sayaç sıfırsa yeni gelenler bekler.

C++20 ile aynı anda en fazla üç işin bağlantı havuzunu kullanmasına şöyle izin verilebilir:

```cpp
#include <chrono>
#include <semaphore>
#include <thread>

std::counting_semaphore<3> connectionSlots(3);

void queryDatabase() {
    connectionSlots.acquire(); // Bir izin alır; yoksa bekler

    std::this_thread::sleep_for(
        std::chrono::milliseconds(200)
    ); // Veritabanı sorgusunu temsil eder

    connectionSlots.release(); // İzni havuza geri verir
}
```

Burada üç thread aynı anda ilerleyebilir. Dördüncü thread ise izinlerden biri iade edilene kadar bekler. Semaphore’u otopark görevlisi olarak düşünün: Hangi aracın çıktığıyla değil, boş yer sayısıyla ilgilenir.

## Aralarındaki temel farklar

| Özellik | Mutex | Semaphore |
|---|---|---|
| Temel amaç | Kritik bölgeyi korumak | Eş zamanlı erişim sayısını sınırlamak |
| Kapasite | Genellikle 1 | 1 veya daha fazla |
| Sahiplik | Kilitleyen açmalıdır | İzni farklı bir thread verebilir |
| Tipik kullanım | Paylaşılan veri, sayaç, nesne | Bağlantı havuzu, görev kuyruğu, hız sınırı |
| Sinyalleşme | Ana amacı değildir | Thread’ler arası sinyal için kullanılabilir |

Başlangıç değeri 1 olan **binary semaphore**, ilk bakışta mutex’e benzer. Fakat sahiplik garantisi taşımadığı için tamamen aynı araç değildir. Binary semaphore daha çok “olay gerçekleşti” sinyali vermek için kullanılabilir.

## Hangisini seçmeliyiz?

Tek bir veri yapısının tutarlılığını koruyorsanız çoğunlukla mutex doğru seçimdir. Elinizde $K$ adet aynı tür kaynak varsa sayaçlı semaphore daha doğal bir model sunar. Örneğin beş veritabanı bağlantısı için $K=5$ seçilebilir.

Her iki araçta da kilitleri gereğinden uzun tutmak performansı düşürür. Birden fazla kilidi farklı sıralarda almak ise **deadlock** oluşturabilir: Her thread diğerinin anahtarını bekler ve sistem dramatik bir sessizliğe gömülür. Kısacası mutex “bu kaynağa yalnızca bir kişi dokunsun”, semaphore ise “içeride en fazla şu kadar kişi bulunsun” demenin programlama dilindeki karşılığıdır.
