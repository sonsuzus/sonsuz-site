---
layout: post
title: "Epoll vs Kqueue: C10K Çağında Olay Dinleme Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - epoll
  - kqueue
  - c10k
  - asenkron
  - linux
  - bsd
  - ağ-programlama
toc: true
image: /img/epoll-vs-kqueue-15.png
---

Bir web sunucusunun aynı anda on binlerce bağlantıya cevap vermesi, yalnızca hızlı bir işlemciye sahip olmakla çözülmez. Asıl mesele, çoğu zaman hiçbir şey yapmadan veri bekleyen bağlantıları düşük maliyetle yönetebilmektir. Linux dünyasındaki **epoll** ve BSD/macOS tarafındaki **kqueue**, işletim sistemine “Hazır olanı bana haber ver, diğerleriyle beni uğraştırma” diyerek yüksek eşzamanlılığın kapısını açar.

![epoll-vs-kqueue-15](/img/epoll-vs-kqueue-15.svg)

``
## C10K problemi neden ortaya çıktı?

Klasik yaklaşımda her bağlantı için ayrı süreç veya iş parçacığı oluşturulurdu. Bu model anlaşılır olsa da bağlantı sayısı yükseldiğinde bellek tüketimi, bağlam değiştirme ve zamanlayıcı yükü büyür. Yaklaşık maliyeti şöyle düşünebiliriz:

$$M \approx N \times S$$

Burada $N$ bağlantı sayısını, $S$ ise her iş parçacığının yığın ve yönetim maliyetini temsil eder. Her iş parçacığı yalnızca 1 MB yığın ayırsa 10.000 bağlantı teorik olarak 10 GB adres alanı isteyebilir. Üstelik işlemci, iş yapanlardan çok bekleyen iş parçacıkları arasında dolaşabilir.

`select` ve `poll` daha az iş parçacığıyla çalışmayı mümkün kılsa da her çağrıda izlenen tanımlayıcıların taranması gerekir. Bu davranış kabaca $O(N)$ maliyetlidir. epoll ve kqueue ise yalnızca durumu değişen olayları döndürerek maliyeti pratikte hazır olay sayısına, yani $O(K)$ düzeyine yaklaştırır.

## epoll ve kqueue karşılaştırması

| Özellik | epoll | kqueue |
|---|---|---|
| Platform | Linux | FreeBSD, OpenBSD, NetBSD, macOS |
| Temel nesne | Dosya tanımlayıcısı olayları | Genel amaçlı kernel olayları |
| Çalışma biçimi | İlgi listesi ve hazır listesi | Filtre tabanlı olay kuyruğu |
| Ağ dışı olaylar | Daha sınırlı, ek API gerekebilir | Sinyal, süreç, zamanlayıcı ve dosya sistemi filtreleri |
| Tetikleme | Level veya edge-triggered | Varsayılan level, `EV_CLEAR` ile edge benzeri |
| Güncelleme | `epoll_ctl` | `kevent` değişiklik listesi |

**Level-triggered** kullanımda veri okunabilir kaldığı sürece bildirim tekrar gelir. Bu, unutkan programcılar için daha güvenlidir. **Edge-triggered** kullanımda ise yalnızca durum değişiminde bildirim alınır. Daha az uyarı üretir ancak soketin `EAGAIN` sonucuna kadar tamamen boşaltılması gerekir; aksi hâlde veri kuyrukta sessizce bekleyebilir.

## Linux üzerinde epoll akışı

Aşağıdaki C kodu, bir epoll örneği oluşturup dinleme soketini takip listesine ekler:

```c
int epfd = epoll_create1(EPOLL_CLOEXEC);

struct epoll_event ev = {0};
ev.events = EPOLLIN | EPOLLET;
ev.data.fd = server_fd;

epoll_ctl(epfd, EPOLL_CTL_ADD, server_fd, &ev);

struct epoll_event events[256];
int count = epoll_wait(epfd, events, 256, -1);

for (int i = 0; i < count; i++) {
    handle_event(events[i].data.fd, events[i].events);
}
```

`EPOLLIN`, okunabilir veri bulunduğunu; `EPOLLET` ise edge-triggered çalışma istendiğini belirtir. Gerçek bir sunucuda soketler non-blocking yapılmalı, `accept` ve `read` işlemleri `EAGAIN` görülene kadar döngüyle sürdürülmelidir.

## BSD tarafında kqueue

kqueue aynı fikri filtrelerle daha genel hâle getirir:

```c
int kq = kqueue();
struct kevent change;

EV_SET(&change, server_fd, EVFILT_READ,
       EV_ADD | EV_ENABLE, 0, 0, NULL);
kevent(kq, &change, 1, NULL, 0, NULL);

struct kevent events[256];
int count = kevent(kq, NULL, 0, events, 256, NULL);

for (int i = 0; i < count; i++) {
    handle_event((int)events[i].ident, events[i].filter);
}
```

`EVFILT_READ` okunabilirliği izler. Aynı mekanizma `EVFILT_TIMER` ile zamanlayıcıları, `EVFILT_SIGNAL` ile sinyalleri ve `EVFILT_PROC` ile süreç değişimlerini de takip edebilir. Bu bütünlük, kqueue’nun en şık tarafıdır.

## Hangisini seçmeli?

Seçim çoğunlukla performanstan önce platform tarafından yapılır: Linux’ta epoll, BSD ve macOS’ta kqueue doğal tercihtir. Nginx, libuv, Tokio ve benzeri sistemler bu ayrıntıları soyutlayabilir. Yine de sihirli değnek yoktur; yavaş istemciler, geri basınç, zaman aşımı, bağlantı başına bellek ve adil görev dağıtımı ayrıca tasarlanmalıdır.

Sonuçta C10K’yı aşmanın sırrı, her bağlantıya çalışan tahsis etmek değil, **hazır olana çalışacak zaman vermektir**. epoll ve kqueue farklı lehçelerde konuşsa da aynı cümleyi kurar: Boşta bekleme, olay gelince harekete geç!
