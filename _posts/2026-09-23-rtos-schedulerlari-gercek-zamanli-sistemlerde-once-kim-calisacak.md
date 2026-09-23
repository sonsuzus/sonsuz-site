---
layout: post
title: "RTOS Scheduler’ları: Gerçek Zamanlı Sistemlerde Önce Kim Çalışacak?"
math: true
categories: 
  - Bilgi
tags: 
  - rtos
  - scheduler
  - gömülü sistemler
  - gerçek zamanlı programlama
  - edf
  - rms
toc: true
---

Bir mikrodenetleyicide sensör okumak, motor sürmek ve haberleşme paketlerini işlemek aynı anda gerekli olabilir. Ancak tek çekirdekli işlemci gerçekte aynı anda yalnızca bir işi yürütür. RTOS scheduler’ı, yani zamanlayıcı, tam bu noktada sahneye çıkar ve hazır görevlerden hangisinin işlemciyi kullanacağına karar verir. Kısacası scheduler, görevler arasındaki trafik polisidir; fakat yanlış kararında yalnızca korna sesi değil, kaçırılmış deadline’lar duyulur.
``

## Gerçek zamanlılık hız demek değildir

Gerçek zamanlı sistemlerde amaç her işi mümkün olan en yüksek hızda tamamlamak değil, belirlenen süre sınırları içinde **öngörülebilir** biçimde tamamlamaktır. Bir görevin temel zamanlama parametreleri şunlardır:

- $C_i$: Görevin en kötü durumdaki çalışma süresi
- $T_i$: Görevin periyodu
- $D_i$: Görevin deadline değeri
- $R_i$: Görevin ölçülen veya hesaplanan tepki süresi

Bir görevin başarılı sayılması için genellikle şu koşul aranır:

$$R_i \leq D_i$$

Örneğin hava yastığını 20 milisaniye yerine 2 saniyede açan bir sistem işlem sonucunu doğru üretse bile işlevsel olarak başarısızdır. Gerçek zamanlılık, doğru cevabı **doğru zamanda** üretmektir.

## Preemptive ve cooperative yaklaşım

Scheduler’lar görevlerin işlemciyi nasıl bırakacağı konusunda iki temel yaklaşım kullanır:

| Yaklaşım | İşlemci nasıl el değiştirir? | Avantaj | Risk |
|---|---|---|---|
| Preemptive | Yüksek öncelikli görev çalışan görevi kesebilir | Kritik olaylara hızlı tepki | Eşzamanlılık hataları artabilir |
| Cooperative | Görev işlemciyi gönüllü bırakır | Basit ve düşük ek yük | Kötü yazılmış görev sistemi kilitleyebilir |

Modern RTOS’ların çoğu preemptive zamanlama kullanır. Bir görev çalışırken daha yüksek öncelikli başka bir görev hazır duruma gelirse **context switch** gerçekleşir. İşlemci mevcut görevin register ve stack durumunu saklar, ardından diğer görevin bağlamını yükler. Bu işlem ücretsiz değildir; sık context switch, faydalı iş için kalan zamanı azaltır.

## Sabit öncelik ve Rate Monotonic Scheduling

Sabit öncelikli sistemlerde her göreve çalışma sırasında değişmeyen bir öncelik atanır. Rate Monotonic Scheduling, kısa periyotlu göreve daha yüksek öncelik verir. Mantık basittir: Daha sık gelmesi gereken iş daha acildir.

$n$ adet periyodik görev için klasik RMS kullanılabilirlik sınırı şöyledir:

$$U = \sum_{i=1}^{n}\frac{C_i}{T_i} \leq n(2^{1/n}-1)$$

Görev sayısı arttıkça bu sınır yaklaşık $0.693$ değerine yaklaşır. Sınır aşılırsa sistem kesinlikle başarısızdır denemez; yalnızca bu basit test başarının garantisini veremez. Daha ayrıntılı response-time analizi gerekebilir.

## EDF: Deadline en yakınsa mikrofon sende

Earliest Deadline First, dinamik öncelikli bir algoritmadır. Mutlak deadline’ı en yakın görev önce çalışır. İdeal, tek çekirdekli ve bağımsız periyodik görev modelinde EDF şu koşul altında sistemi zamanlayabilir:

$$\sum_{i=1}^{n}\frac{C_i}{T_i} \leq 1$$

| Algoritma | Öncelik türü | Teorik kullanım | Uygulama karmaşıklığı |
|---|---|---:|---|
| RMS | Sabit | Yaklaşık %69 garantili sınır | Düşük |
| EDF | Dinamik | %100’e kadar | Daha yüksek |
| Round Robin | Zaman dilimli | Deadline garantisi yok | Düşük |

EDF işlemciyi daha verimli kullanabilir; ancak görev sıralamasını sürekli güncellemek gerekir. Aşırı yük durumunda davranışı da sabit öncelikli sistemlere göre daha az öngörülebilir olabilir.

## Basitleştirilmiş scheduler örneği

Aşağıdaki C benzeri kod, hazır görevler arasından sayısal önceliği en yüksek olanı seçer:

```c
Task *select_next_task(Task tasks[], int count) {
    Task *selected = NULL;

    for (int i = 0; i < count; i++) {
        if (tasks[i].state != READY)
            continue;

        if (selected == NULL ||
            tasks[i].priority > selected->priority) {
            selected = &tasks[i];
        }
    }

    return selected;
}
```

Gerçek bir RTOS bu seçimi çoğunlukla ready queue, bitmap veya öncelik listeleriyle hızlandırır. Ayrıca kesmelerin güvenli yönetimi, tick mekanizması ve context switch kodu da devrededir.

## Öncelik terslenmesi sürprizi

Düşük öncelikli bir görev mutex’i tutarken yüksek öncelikli görev aynı mutex’i beklerse **priority inversion** oluşur. Araya orta öncelikli görevler de girerse kritik görev uzun süre engellenebilir. Priority inheritance protokolü, mutex’i tutan görevin önceliğini geçici olarak yükselterek bu sorunu azaltır.

Doğru scheduler seçimi yalnızca “en hızlı algoritma hangisi?” sorusuna bağlı değildir. Görev periyotları, deadline’lar, paylaşılan kaynaklar ve aşırı yük davranışı birlikte değerlendirilmelidir. Çünkü RTOS dünyasında kazanan, işlemciyi en çok kullanan değil; sözünü verdiği anda işi bitirendir.
