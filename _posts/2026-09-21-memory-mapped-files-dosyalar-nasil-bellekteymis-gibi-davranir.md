---
layout: post
title: "Memory-Mapped Files: Dosyalar Nasıl Bellekteymiş Gibi Davranır?"
math: true
categories: 
  - Bilgi
tags: 
  - memory-mapped-files
  - sanal-bellek
  - işletim-sistemleri
  - mmap
  - performans
  - dosya-girdisi-çıktısı
toc: true
---

Büyük bir dosyanın içeriğine erişmek için genellikle `read()` çağrıları, tamponlar ve döngüler düşünürüz. Memory-mapped file yaklaşımıysa dosyanın belirli bir bölümünü sürecin sanal adres alanına bağlar. Böylece program, dosyayı gerçekten RAM’e bütünüyle yüklemeden ona sıradan bir bellek dizisiymiş gibi erişebilir. İşin arkasındaki sihir değil; sanal bellek, sayfa tabloları ve işletim sisteminin sayfa önbelleğidir.

``

## Temel fikir: Adres ile veriyi birbirinden ayırmak

Bir işaretçinin gösterdiği adres, fiziksel RAM’deki doğrudan konum değildir. Modern işletim sistemlerinde süreçler **sanal adresler** kullanır. İşlemcinin bellek yönetim birimi, yani MMU, bu adresleri sayfa tabloları yardımıyla fiziksel bellek sayfalarına dönüştürür.

Bir dosya eşlendiğinde işletim sistemi kabaca şunu söyler:

> “Bu sanal adres aralığına erişilirse karşılık gelen veriyi şu dosyadan getir.”

Program eşlenen bölgeye ilk kez dokunduğunda ilgili sayfa henüz RAM’de bulunmayabilir. İşlemci bu durumda bir **page fault** üretir. İşletim sistemi dosyanın gerekli kısmını diskten okuyarak RAM’deki bir sayfaya yerleştirir, sayfa tablosunu günceller ve program kaldığı yerden devam eder.

Sayfa boyutu $P$, erişilen dosya konumu $x$ ise gereken sayfanın başlangıcı yaklaşık olarak şöyle bulunur:

$$
\text{sayfaBaşlangıcı} = \left\lfloor \frac{x}{P} \right\rfloor P
$$

Örneğin $P=4096$ bayt olduğunda 5000. bayta erişmek, 4096’dan başlayan sayfanın yüklenmesini gerektirir. Yani disk erişimi çoğunlukla tek tek baytlarla değil, sayfalarla gerçekleşir.

## Klasik okuma ile karşılaştırma

| Özellik | `read()` yaklaşımı | Memory mapping |
|---|---|---|
| Veri erişimi | Sistem çağrısı ve kullanıcı tamponu | İşaretçi veya indeks |
| Yükleme zamanı | Program açıkça ister | Sayfa hatasıyla ihtiyaç anında |
| Kopyalama | Çoğu senaryoda tampona kopyalanır | Sayfa önbelleği doğrudan eşlenebilir |
| Rastgele erişim | Konumlandırma ve okuma gerekir | Dizi erişimine benzer |
| Hata modeli | Dönüş kodları | Erişim sırasında sinyal oluşabilir |
| Uygun kullanım | Akışsal ve küçük okumalar | Büyük dosyalar, rastgele erişim |

Memory mapping her zaman daha hızlı değildir. Sıralı okunan küçük bir dosyada `read()` oldukça verimli olabilir. Buna karşılık devasa bir veritabanı indeksinin yalnızca birkaç bölümüne erişiliyorsa bütün dosyayı okumamak önemli avantaj sağlar.

## C ile küçük bir örnek

Aşağıdaki kod, dosyayı salt okunur biçimde eşler ve ilk baytı görüntüler:

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

int main(void) {
    int fd = open("veri.bin", O_RDONLY);
    struct stat bilgi;
    fstat(fd, &bilgi);

    unsigned char *veri = mmap(
        NULL,
        bilgi.st_size,
        PROT_READ,
        MAP_PRIVATE,
        fd,
        0
    );

    if (veri == MAP_FAILED) return 1;

    printf("İlk bayt: %u\n", veri[0]);

    munmap(veri, bilgi.st_size);
    close(fd);
    return 0;
}
```

`mmap()` hemen bütün dosyayı RAM’e taşımaz; yalnızca sanal adres eşlemesini kurar. `veri[0]` ifadesi çalıştığında gerekli sayfa talep üzerine yüklenir. `MAP_PRIVATE`, değişikliklerin dosyaya yazılmadığı özel bir kopya görünümü sağlar. Paylaşılan ve yazılabilir bir eşleme için `MAP_SHARED` ile uygun koruma bayrakları kullanılabilir.

## Yazma, paylaşım ve riskler

Yazılabilir eşlemede değiştirilen sayfalar **dirty page** olarak işaretlenir. İşletim sistemi bunları daha sonra dosyaya aktarabilir; `msync()` belirli eşlemelerin senkronizasyonunu istemek için kullanılır. Ancak bu çağrı tek başına uygulama seviyesinde işlem bütünlüğü sağlamaz. Çökme güvenliği gereken sistemlerde günlükleme, atomik güncellemeler ve `fsync()` gibi mekanizmalar ayrıca düşünülmelidir.

Dosya eşliyken başka bir süreç dosyayı küçültürse artık geçerli olmayan bölgeye erişmek hata veya `SIGBUS` doğurabilir. Ayrıca rastgele erişim çok sayıda page fault üreterek performansı düşürebilir.

Kısacası dosya gerçekten bir RAM dizisine dönüşmez. İşletim sistemi, sanal adresleri dosya destekli sayfalarla ilişkilendirir ve yalnızca ihtiyaç duyulan parçaları belleğe getirir. Programın gördüğü sade bir işaretçi, perde arkasında ise MMU, sayfa önbelleği ve dosya sistemi birlikte çalışan kalabalık bir ekip vardır.
