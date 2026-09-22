---
layout: post
title: "File Descriptor Mantığı: Linux Neden Dosya, Soket ve Pipe’a Aynı Gözle Bakar?"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - file-descriptor
  - sistem-programlama
  - soket
  - pipe
  - unix
toc: true
---

Linux dünyasında bir dosya açtığınızda, ağ bağlantısı kurduğunuzda veya iki süreç arasında pipe oluşturduğunuzda karşınıza küçük bir tamsayı çıkar: file descriptor, yani dosya tanımlayıcısı. İlk bakışta bir metin dosyasıyla ağ soketinin aynı sayı türüyle temsil edilmesi tuhaf görünebilir. Fakat bu yaklaşım, Unix felsefesinin en güçlü fikirlerinden birini uygular: Farklı kaynaklara ortak bir arayüz üzerinden erişmek.

``

## File descriptor gerçekte nedir?

File descriptor, kaynağın kendisi değildir. Sürece ait file descriptor tablosundaki bir girişin indeksidir. Örneğin `3` sayısı, kabaca “bu sürecin tablosundaki üçüncü kaynağa bak” anlamına gelir.

$$fd \in \{0,1,2,3,\ldots\}$$

Her süreç geleneksel olarak üç açık descriptor ile başlar:

| Descriptor | Sembolik ad | Varsayılan kaynak |
|---:|---|---|
| 0 | `stdin` | Standart giriş |
| 1 | `stdout` | Standart çıkış |
| 2 | `stderr` | Standart hata |

Kernel tarafında descriptor girdisi bir **open file description** yapısına bağlanır. Burada erişim modu, mevcut dosya konumu ve durum bayrakları gibi bilgiler tutulur. Bu yapı da dosya için inode’a, soket için ağ yapılarına, pipe için kernel tamponuna ulaşır.

Basitleştirilmiş ilişki şöyledir:

$$Süreç \rightarrow FD\ tablosu \rightarrow Açık\ kaynak\ açıklaması \rightarrow Kernel\ nesnesi$$

## Aynı görünmelerinin sırrı

Dosya, soket ve pipe fiziksel olarak aynı şey değildir. Aynı görünmelerinin nedeni, kernel’in bunlara benzer sistem çağrılarıyla erişilebilen ortak bir arayüz sunmasıdır.

| Kaynak | `read()` | `write()` | `lseek()` | Tipik kullanım |
|---|---:|---:|---:|---|
| Normal dosya | Evet | Evet | Evet | Kalıcı veri |
| Soket | Evet | Evet | Hayır | Ağ iletişimi |
| Pipe | Evet | Evet | Hayır | Süreçler arası iletişim |

Genel okuma işlemi şu biçimdedir:

```c
ssize_t n = read(fd, buffer, capacity);
```

`read()` çağrısı descriptor’ın arkasında ne bulunduğunu bilir. Normal dosyada disk veya önbellekten, sokette ağ tamponundan, pipe’da ise kernel’in pipe tamponundan veri getirir. Program aynı fonksiyonu çağırırken ayrıntılı işi kernel üstlenir.

Bu tasarım tam anlamıyla “her şey dosyadır” demek değildir. Daha doğru ifade şudur: **Birçok kernel kaynağı, dosya benzeri bir giriş/çıkış arayüzü sunar.** Örneğin bir sokete `lseek()` uygulamak mantıklı değildir ve çağrı hata verir.

## Pipe ile ortak arayüzü görmek

Aşağıdaki C kodu bir pipe oluşturur, yazma ucuna veri gönderir ve okuma ucundan aynı veriyi alır:

```c
#include <stdio.h>
#include <unistd.h>

int main(void) {
    int pipefd[2];
    char buffer[64] = {0};

    if (pipe(pipefd) == -1) {
        perror("pipe");
        return 1;
    }

    write(pipefd[1], "Merhaba kernel!", 15);
    read(pipefd[0], buffer, sizeof(buffer) - 1);
    printf("Okunan: %s\n", buffer);

    close(pipefd[0]);
    close(pipefd[1]);
    return 0;
}
```

`pipefd[0]` okuma, `pipefd[1]` yazma ucudur. Dikkat ederseniz burada özel bir `pipe_read()` fonksiyonu yoktur; bildiğimiz `read()` ve `write()` kullanılır.

## Yönlendirme neden bu kadar kolay?

Shell’deki şu komut, ortak descriptor modelinin pratik sonucudur:

```bash
cat access.log | grep "404" > errors.txt
```

Shell, `cat` çıktısını pipe’ın yazma ucuna; `grep` girişini pipe’ın okuma ucuna bağlar. Ardından `grep` çıktısını dosyaya yönlendirir. Programlar karşılarında terminal, pipe veya dosya olduğunu bilmek zorunda değildir.

`dup2()` gibi çağrılar descriptor’ları yeniden eşleyebilir. `fork()` sonrasında ebeveyn ve çocuk süreçlerin descriptor’ları aynı açık kaynak açıklamasını paylaşabildiği için dosya konumu da ortak ilerleyebilir.

Sonuç olarak file descriptor, kaynak türlerini ortadan kaldırmaz; farklı kaynakların ortak işlemlerle yönetilmesini sağlar. Bu küçük tamsayılar sayesinde yönlendirme, süreç zincirleri, ağ sunucuları ve olay döngüleri sade biçimde kurulabilir. Linux’un numarası her şeyi aynı yapmak değil, farklı şeylere konuşabilecekleri ortak bir dil vermektir.
