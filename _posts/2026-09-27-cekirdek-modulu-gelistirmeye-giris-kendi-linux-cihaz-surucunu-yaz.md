---
layout: post
title: "Çekirdek Modülü Geliştirmeye Giriş: Kendi Linux Cihaz Sürücünü Yaz"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - kernel
  - çekirdek-modülü
  - cihaz-sürücüsü
  - c
  - sistem-programlama
toc: true
image: /img/cekirdek-modulu-gelistirmeye-69.png
---

Linux çekirdeği devasa bir monolitik yapı olsa da her özelliği kalıcı olarak çekirdeğe gömmek zorunda değildir. Yüklenebilir Çekirdek Modülleri (Loadable Kernel Modules veya LKM), çalışan sistemi yeniden başlatmadan sürücü, dosya sistemi ya da ağ özelliği eklememizi sağlar. Bu yazıda küçük bir karakter cihazı geliştirerek modül mimarisini güvenli biçimde keşfedeceğiz.

``

## Modül mimarisi nasıl çalışır?

Bir çekirdek modülü, kullanıcı alanındaki sıradan uygulamalardan farklı olarak **kernel space** içinde çalışır. İşletim sisteminin belleğine ve donanım kaynaklarına doğrudan erişebildiği için küçük bir hata bile tüm sistemi durdurabilir. Bu nedenle geliştirmeyi sanal makinede yapmak akıllıcadır.

Modül çekirdeğe yüklendiğinde sembolleri bağlanır, başlangıç fonksiyonu çalıştırılır ve gerekli kaynaklar kaydedilir. Kaldırılırken kaynakların ters sırada serbest bırakılması gerekir. Basitleştirilmiş yaşam döngüsü şöyledir:

$$Kaynak\ Durumu = Tahsis\ Edilenler - Serbest\ Bırakılanlar$$

Sağlıklı bir kaldırma işleminde sonucun $0$ olması beklenir. Aksi durumda bellek sızıntıları, kullanımda kalan cihazlar veya çökmeler ortaya çıkabilir.

| Özellik | Kullanıcı alanı programı | Çekirdek modülü |
|---|---|---|
| Çalışma alanı | User space | Kernel space |
| Standart kütüphane | Genellikle kullanılabilir | Kullanılamaz |
| Hata sonucu | Süreç kapanabilir | Sistem çökebilir |
| Çıktı yöntemi | `printf()` | `pr_info()` / `printk()` |
| Yükleme | Programı çalıştırma | `insmod` veya `modprobe` |

![cekirdek-modulu-gelistirmeye-69](/img/cekirdek-modulu-gelistirmeye-69.svg)


## Basit bir karakter cihazı

Aşağıdaki modül, `/dev/minidriver` adında bir karakter cihazı oluşturur. Kullanıcı cihazı okuduğunda çekirdekten kısa bir mesaj alır. `miscdevice` arabirimi, ana cihaz numarasını otomatik seçerek örneği sade tutar.

```c
#include <linux/module.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

static const char message[] = "Merhaba, çekirdek!\n";

static ssize_t mini_read(struct file *file, char __user *buffer,
                         size_t length, loff_t *offset)
{
    return simple_read_from_buffer(buffer, length, offset,
                                   message, sizeof(message) - 1);
}

static const struct file_operations mini_fops = {
    .owner = THIS_MODULE,
    .read = mini_read,
};

static struct miscdevice mini_device = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "minidriver",
    .fops = &mini_fops,
    .mode = 0444,
};

static int __init mini_init(void)
{
    int result = misc_register(&mini_device);

    if (result)
        pr_err("minidriver kaydedilemedi: %d\n", result);
    else
        pr_info("minidriver yüklendi\n");

    return result;
}

static void __exit mini_exit(void)
{
    misc_deregister(&mini_device);
    pr_info("minidriver kaldırıldı\n");
}

module_init(mini_init);
module_exit(mini_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Örnek Geliştirici");
MODULE_DESCRIPTION("Basit karakter cihazı modülü");
```

`file_operations`, sistem çağrıları ile sürücü fonksiyonları arasındaki köprüdür. Kullanıcı `read()` çağırdığında çekirdek `mini_read()` fonksiyonuna yönelir. `simple_read_from_buffer()` ise çekirdek belleğindeki veriyi kullanıcı belleğine kontrollü şekilde aktarır; doğrudan işaretçi kopyalamaktan daha güvenlidir.

## Derleme ve deneme

Modülü derlemek için aynı dizine şu `Makefile` dosyasını ekleyin:

```makefile
obj-m += minidriver.o

all:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

Ardından geliştirme başlıklarının kurulu olduğundan emin olarak komutları çalıştırın:

```bash
make
sudo insmod minidriver.ko
cat /dev/minidriver
sudo rmmod minidriver
dmesg | tail
```

`insmod` modülü doğrudan yüklerken `modprobe` bağımlılıkları da çözer. Üretim sistemlerinde Secure Boot imzasız modülleri reddedebilir; ayrıca çekirdek API’leri sürümler arasında değişebilir.

## Güvenli geliştirme alışkanlıkları

Her tahsisin karşılığında bir temizleme işlemi yazın, kullanıcıdan gelen uzunluk ve adreslere güvenmeyin, kilit gerektiren ortak verileri koruyun ve günlükleri `dmesg` üzerinden izleyin. Gerçek donanım sürücülerinde kesmeler, DMA, aygıt ağacı ve platform veri yolları devreye girer. Ancak temel ritim değişmez: **kaydet, isteği işle, kaynakları eksiksiz bırak ve modülü kaldır**.
