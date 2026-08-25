---
layout: post
title: "Lock-Free Veri Yapıları: Kilitsiz Eşzamanlılığın Temelleri"
math: true
categories: 
  - Bilgi
tags: 
  - lock-free
  - eşzamanlı programlama
  - atomik işlemler
---

Modern uygulamalarda birden fazla iş parçacığının aynı veriye erişmesi kaçınılmazdır. Geleneksel çözüm mutex gibi kilitlerdir; ancak bir iş parçacığı kilidi bırakmayı unutursa, askıya alınırsa veya uzun süre çalışırsa diğerleri beklemeye mahkûm olur. Lock-free veri yapıları, bu bekleme zincirini kırmak için atomik donanım işlemlerini kullanır. Amaç, tek tek iş parçacıklarının değil, sistemin bütünüyle her zaman ilerlemesidir.

``

## Lock-free tam olarak neyi garanti eder?

“Lock-free” ifadesi “hiç kimse beklemez” anlamına gelmez. Bir iş parçacığı, başka bir iş parçacığının sürekli araya girmesi nedeniyle kendi işlemini tekrar deneyebilir. Buna rağmen her başarısız deneme, başka bir iş parçacığının başarılı olduğu anlamına gelir. Yani sistem genelinde ilerleme vardır.

Eşzamanlılık literatüründeki ilerleme garantilerini şöyle karşılaştırabiliriz:

| Yaklaşım | İlerleme garantisi | Temel risk | Tipik kullanım |
|---|---|---|---|
| Mutex tabanlı | Kilidi alan iş parçacığına bağlı | Deadlock, priority inversion | Basit kritik bölgeler |
| Lock-free | Sistem genelinde en az bir işlem ilerler | Starvation, tekrar denemeler | Kuyruk, stack, sayaç |
| Wait-free | Her işlem sınırlı adımda biter | Yüksek algoritmik karmaşıklık | Gerçek zamanlı sistemler |

Bir algoritmanın lock-free olması için kritik araç genellikle **Compare-And-Swap** (CAS) işlemidir. CAS, bir bellek adresindeki değer beklenen değere eşitse onu yeni değerle atomik olarak değiştirir. Matematiksel olarak işlem şu şekilde özetlenebilir:

$$CAS(x, e, n) = \begin{cases} true & x=e \Rightarrow x\leftarrow n \\ false & x\neq e \end{cases}$$

Bu atomiklik sayesinde “kontrol et, sonra değiştir” adımları arasına başka bir iş parçacığının sızması engellenir.

## Örnek: CAS ile lock-free sayaç

Aşağıdaki Java örneğinde `AtomicInteger`, CPU’nun atomik talimatlarını sarmalar. Döngü, değer değişmişse güncel değerle yeniden deneme yapar:

```java
import java.util.concurrent.atomic.AtomicInteger;

public class LockFreeCounter {
    private final AtomicInteger value = new AtomicInteger(0);

    public int increment() {
        while (true) {
            int current = value.get();
            int next = current + 1;

            if (value.compareAndSet(current, next)) {
                return next;
            }
            // Başka bir thread değeri değiştirdi: yeniden dene.
        }
    }
}
```

Bu kodda iki thread aynı anda `current = 5` okuyabilir. İlki `5` değerini `6` yapar; ikincisinin CAS denemesi başarısız olur çünkü güncel değer artık `6`dır. İkinci thread tekrar okuyup `7`ye yükseltmeyi dener. Böylece kayıp güncelleme oluşmaz.

## Bellek görünürlüğü ve linearizability

Atomiklik tek başına yeterli değildir; yazılan verinin diğer çekirdeklerce doğru sırada görülmesi gerekir. Modern işlemciler performans için bellek işlemlerini yeniden sıralayabilir. Java’daki atomik sınıflar, C++ tarafındaki `std::atomic` ve uygun memory-order seçenekleri bu görünürlük problemini yönetir.

Bir diğer önemli kavram **linearizability**’dir. Eşzamanlı bir operasyon dışarıdan bakıldığında, çağrıldığı an ile tamamlandığı an arasında tek bir anda gerçekleşmiş gibi davranmalıdır. Stack’e ekleme işleminde başarılı CAS noktası çoğunlukla bu “doğrusallaşma noktası”dır.

## ABA problemi: Değer aynıysa gerçekten aynı mıdır?

CAS yalnızca değeri karşılaştırır. Bir pointer önce `A`, sonra `B`, ardından tekrar `A` olmuşsa CAS bunu değişiklik yokmuş gibi algılayabilir. Bu ABA problemidir. Özellikle lock-free bağlı listeler ve stack’lerde tehlikelidir.

| Sorun | Neden oluşur? | Yaygın çözüm |
|---|---|---|
| ABA | Değer A-B-A döngüsüne girer | Sürüm sayacı (tagged pointer) |
| Starvation | Aynı thread sürekli CAS kaybeder | Backoff, adil zamanlama |
| Bellek geri kazanımı | Silinen düğüm hâlâ okunuyor olabilir | Hazard pointer, epoch tabanlı bellek yönetimi |

Lock-free tasarım, mutex kaldırmaktan çok daha fazlasıdır: donanım atomikleri, bellek modeli, hata senaryoları ve bellek ömrü birlikte düşünülmelidir. Başlangıç için hazır atomik koleksiyonları tercih edin; özel bir lock-free yapı yazmadan önce ise ölçüm yapın. Çünkü doğru yazılmış sıradan bir mutex, yanlış yazılmış “hızlı” bir lock-free algoritmadan her zaman daha değerlidir.
