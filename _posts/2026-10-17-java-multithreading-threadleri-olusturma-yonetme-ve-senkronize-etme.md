---
layout: post
title: "Java Multithreading: Thread’leri Oluşturma, Yönetme ve Senkronize Etme"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - multithreading
  - thread
  - eşzamanlılık
  - senkronizasyon
  - concurrency
toc: true
image: /img/java-multithreading-threadleri-19.png
---

Bir uygulamanın aynı anda dosya indirip kullanıcı arayüzünü canlı tutması veya binlerce isteğe cevap vermesi gerekiyorsa sahneye çok iş parçacıklı programlama çıkar. Java, `Thread` sınıfından modern `ExecutorService` araçlarına kadar bu konuda güçlü seçenekler sunar. Ancak birden fazla iş parçacığı aynı veriye dokunduğunda işler, aynı buzdolabındaki son tatlıya uzanan iki el gibi hızla karışabilir.

``

## İş parçacığı nedir?

Bir **process**, çalışan uygulamanın kendisidir; **thread** ise o uygulama içindeki bağımsız yürütme akışıdır. Aynı process içindeki thread’ler heap belleğini paylaşır, fakat kendi çağrı yığınlarına sahiptir.

Eşzamanlılık ile paralellik de aynı şey değildir:

| Kavram | Açıklama | Örnek |
|---|---|---|
| Concurrency | İşlerin zaman dilimleriyle ilerlemesi | Tek çekirdekte iki görevin sırayla çalışması |
| Parallelism | İşlerin fiziksel olarak aynı anda çalışması | İki çekirdekte iki hesaplama |
| Asenkronluk | Sonucu beklemeden başka işe geçilmesi | Ağ isteğinin arka planda tamamlanması |

Bir işlem tek başına $T$ sürede bitiyorsa, teorik olarak $n$ çekirdekle süre $T/n$ olabilir. Gerçekte seri bölümler ve koordinasyon maliyeti nedeniyle bu ideale ulaşılamaz. Amdahl Yasası bunu şöyle özetler:

$$S(n)=\frac{1}{(1-p)+\frac{p}{n}}$$

Burada $p$, paralelleştirilebilen bölümün oranıdır. Kodun yalnızca yüzde 50’si paralelse yüz çekirdek bile sonsuz hız sağlamaz.

## Thread oluşturmanın modern yolu

Doğrudan `Thread` oluşturmak mümkündür; fakat üretim kodunda görevleri thread yönetiminden ayıran `ExecutorService` daha kullanışlıdır:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class WorkerDemo {
    public static void main(String[] args) {
        ExecutorService pool = Executors.newFixedThreadPool(3);

        for (int i = 1; i <= 5; i++) {
            int taskId = i;
            pool.submit(() -> {
                String name = Thread.currentThread().getName();
                System.out.println(taskId + " görevi: " + name);
            });
        }

        pool.shutdown();
    }
}
```

Bu örnekte beş görev, üç iş parçacıklı bir havuza gönderilir. Havuz thread’leri tekrar kullandığı için her görevde yeni bir thread oluşturma maliyeti doğmaz. `shutdown()` mevcut görevlerin tamamlanmasına izin verirken yeni görev kabulünü kapatır.

## Race condition ve senkronizasyon

Paylaşılan bir sayacı artıran `counter++` ifadesi atomik değildir. Aslında okuma, artırma ve yazma adımlarından oluşur. İki thread aynı değeri okuyup üzerine yazarsa bir artış kaybolabilir; buna **race condition** denir.

```java
class SafeCounter {
    private int value = 0;

    public synchronized void increment() {
        value++;
    }

    public synchronized int getValue() {
        return value;
    }
}
```

`synchronized`, aynı nesnenin kilidini aynı anda yalnızca bir thread’in almasını sağlar. Ayrıca bir thread’in yaptığı değişikliklerin diğerleri tarafından görünür olmasına yardım eder. Basit sayaçlar için `AtomicInteger` daha hafif bir alternatiftir:

```java
import java.util.concurrent.atomic.AtomicInteger;

AtomicInteger counter = new AtomicInteger();
counter.incrementAndGet();
```

| Araç | Uygun kullanım | Dikkat edilmesi gereken |
|---|---|---|
| `synchronized` | Birden çok adımlı kritik bölge | Uzun kilitler performansı düşürür |
| `AtomicInteger` | Atomik sayaç işlemleri | Karmaşık durumları tek başına çözmez |
| `ReentrantLock` | Zaman aşımı ve esnek kilitleme | Kilit `finally` içinde bırakılmalıdır |
| `ConcurrentHashMap` | Eşzamanlı anahtar-değer erişimi | Bileşik işlemler ayrıca düşünülmelidir |

## Deadlock tuzağı

İki thread birbirinin tuttuğu kilidi beklerse **deadlock** oluşur. Bunu önlemek için kilitleri daima aynı sırayla almak, kritik bölgeleri kısa tutmak ve mümkünse değişmez nesneler kullanmak gerekir. Thread sayısını gelişigüzel artırmak da çözüm değildir; fazla thread, context switching maliyetini yükseltir.

Özetle iyi bir multithreading tasarımı, işleri küçük görevlere böler, thread havuzlarını kullanır ve paylaşılan değiştirilebilir veriyi azaltır. Amaç en fazla thread’i üretmek değil, doğru işleri güvenli biçimde eşzamanlı çalıştırmaktır.

![java-multithreading-threadleri-19](/img/java-multithreading-threadleri-19.svg)

