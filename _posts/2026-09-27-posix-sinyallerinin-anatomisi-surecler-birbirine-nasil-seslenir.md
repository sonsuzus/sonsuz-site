---
layout: post
title: "POSIX Sinyallerinin Anatomisi: Süreçler Birbirine Nasıl Seslenir?"
math: true
categories: 
  - Bilgi
tags: 
  - posix
  - sinyaller
  - linux
  - unix
  - c
  - işletim-sistemleri
toc: true
image: /img/posix-sinyallerinin-anatomisi-17.png
---

Bir terminalde çalışan programa `Ctrl+C` bastığınızda ekranda sihir gerçekleşmez; terminal sürücüsü, çekirdek ve hedef süreç arasında dikkatle düzenlenmiş bir mesajlaşma zinciri çalışır. POSIX sinyalleri, süreçlere “dur”, “devam et”, “çocuğun sona erdi” veya “hemen toparlan” gibi kısa bildirimler gönderen, veri taşımaktan çok olay duyurmaya odaklı mekanizmalardır.
``
## Sinyal gönderilince ne olur?

Bir sinyalin yaşam döngüsü üç temel aşamada düşünülebilir: **üretilme**, **bekleme** ve **teslim edilme**. Sinyal; donanım hatası, terminal olayı, zamanlayıcı veya başka bir sürecin sistem çağrısı nedeniyle üretilebilir.

Örneğin `kill(pid, SIGTERM)` çağrısı doğrudan hedefi öldürmez. İsmi biraz dramatiktir: Çekirdekten belirtilen sürece bir sinyal göndermesini ister. Çekirdek önce gönderen sürecin yetkilerini denetler, ardından sinyali hedef için bekleyenler kümesine ekler.

Bir sinyali matematiksel olarak süreç durumuna eklenen bir olay gibi gösterebiliriz:

$$P_{pending}' = P_{pending} \cup \{SIGINT\}$$

Sinyal engellenmemişse çekirdek, süreç yeniden kullanıcı moduna dönerken onu teslim eder. Standart sinyaller genellikle kuyruklanmaz; aynı sinyal teslim edilmeden üç kez gelirse süreç bunu tek bildirim olarak görebilir. POSIX gerçek zamanlı sinyalleri ise kuyruklanabilir ve sıralı teslim edilir.

| Özellik | Standart sinyaller | Gerçek zamanlı sinyaller |
|---|---|---|
| Kuyruklama | Genellikle birleşir | Her örnek kuyruklanır |
| Sıralama | Güçlü garanti yoktur | Sinyal numarasına göre önceliklidir |
| Ek veri | Sınırlı | `sigqueue()` ile değer taşıyabilir |
| Örnek | `SIGINT`, `SIGTERM` | `SIGRTMIN` ve sonrası |

![posix-sinyallerinin-anatomisi-17](/img/posix-sinyallerinin-anatomisi-17.svg)


## Ctrl+C aslında kime gider?

Terminal, ön plandaki bir **süreç grubunu** takip eder. `Ctrl+C` karakteri terminal sürücüsü tarafından yorumlandığında yalnızca tek sürece değil, ön plan süreç grubunun tamamına `SIGINT` gönderilir. Böylece `cat file | grep foo` gibi bir boru hattındaki süreçler birlikte uyarılır.

Kabuk bu grubun parçası değildir; işi yönetir ve genellikle arka planda bekler. Program `SIGINT` için özel davranış tanımlamamışsa varsayılan eylem sonlanmaktır.

| Sinyal | Tipik anlam | Varsayılan davranış | Yakalanabilir mi? |
|---|---|---|---|
| `SIGINT` | Etkileşimli kesme | Sonlandırma | Evet |
| `SIGTERM` | Nazik kapanma isteği | Sonlandırma | Evet |
| `SIGKILL` | Koşulsuz sonlandırma | Sonlandırma | Hayır |
| `SIGSTOP` | Koşulsuz durdurma | Durdurma | Hayır |
| `SIGCHLD` | Çocuk süreç değişti | Yok sayma | Evet |

## Sinyal nasıl yakalanır?

Modern POSIX kodunda eski `signal()` yerine davranışı daha açık olan `sigaction()` tercih edilir:

```c
#include <signal.h>
#include <unistd.h>

static volatile sig_atomic_t interrupted = 0;

static void handle_sigint(int signo) {
    (void)signo;
    interrupted = 1;
}

int main(void) {
    struct sigaction action = {0};
    action.sa_handler = handle_sigint;
    sigemptyset(&action.sa_mask);
    action.sa_flags = 0;

    sigaction(SIGINT, &action, NULL);

    while (!interrupted) {
        /* Programın normal işi burada yürütülür. */
    }

    const char message[] = "Guvenli kapanis yapiliyor...\n";
    write(STDOUT_FILENO, message, sizeof(message) - 1);
    return 0;
}
```

İşleyici yalnızca `sig_atomic_t` türündeki bayrağı değiştirir. Bunun nedeni sinyalin programı neredeyse herhangi bir noktada kesebilmesidir. `printf()`, `malloc()` veya kilit kullanan karmaşık fonksiyonlar o anda tutarsız durumda olabilir. İşleyici içinde yalnızca **async-signal-safe** fonksiyonlar kullanılmalıdır; `write()` bunlardan biridir.

## Neden SIGKILL yakalanamaz?

`SIGKILL` ve `SIGSTOP`, süreç tarafından yakalanamaz, engellenemez veya yok sayılamaz. Aksi hâlde bozulmuş ya da kötü niyetli bir süreç işletim sisteminin denetiminden kaçabilirdi. `SIGTERM` uygulamaya dosyalarını kapatma ve geçici kaynaklarını temizleme fırsatı verirken `SIGKILL` doğrudan çekirdeğin hükmüdür.

Bu yüzden iyi yönetim sırası önce `SIGTERM`, yeterli süre sonunda gerekirse `SIGKILL` göndermektir. Sinyaller konuşma balonları değil, çekirdeğin taşıdığı kısa kapı zilleridir: Mesajı duyunca ne yapılacağını süreç belirler—tabii zilin üzerinde `SIGKILL` yazmıyorsa!
