---
layout: post
title: "FUSE ile Python Kullanarak Kendi Sanal Dosya Sisteminizi Yazın"
math: true
categories: 
  - Proje
tags: 
  - fuse
  - python
  - dosya-sistemi
  - linux
  - sanal-dosya-sistemi
  - sistem-programlama
toc: true
image: /img/fuse-ile-python-34.png
---

Dosya sistemi yazmak denildiğinde akla çekirdek kodu, korkutucu C işaretçileri ve bilgisayarı yeniden başlatma ritüelleri gelebilir. FUSE sayesinde bunların çoğuna gerek kalmadan Python veya Go ile dosya işlemlerine kendi kurallarımızı uygulayabiliriz. Örneğin içeriğini çalışma anında üreten, buluttaki verileri dosya gibi gösteren ya da tüm yazılanları otomatik şifreleyen bir sistem geliştirebiliriz.
``
## FUSE tam olarak nedir?

FUSE, yani **Filesystem in Userspace**, dosya sistemi mantığının kullanıcı alanında çalışan normal bir program tarafından uygulanmasını sağlayan Linux altyapısıdır. Uygulamalar yine `open`, `read`, `write` ve `stat` gibi standart sistem çağrılarını kullanır. Çekirdekteki FUSE sürücüsü bu istekleri bizim sürecimize iletir, cevabı alır ve uygulamaya döndürür.

Akış kabaca şöyledir:

1. Kullanıcı `/mnt/ozel/merhaba.txt` dosyasını okur.
2. İşletim sistemi isteği FUSE sürücüsüne gönderir.
3. FUSE, Python programımızdaki `read()` metodunu çağırır.
4. Metodun ürettiği veri kullanıcıya teslim edilir.

Bir işlemin toplam gecikmesini basitçe $T = T_{kernel} + T_{iletisim} + T_{uygulama}$ şeklinde düşünebiliriz. Kullanıcı alanına geçiş ek maliyet oluşturduğu için FUSE her senaryoda yerel dosya sistemleri kadar hızlı değildir; fakat geliştirme kolaylığı çoğu özel proje için daha değerlidir.

| Özellik | Çekirdek dosya sistemi | FUSE dosya sistemi |
|---|---|---|
| Geliştirme dili | Genellikle C | Python, Go, Rust, C++ |
| Hata etkisi | Sistemi çökertebilir | Genellikle süreç kapanır |
| Performans | Çok yüksek | Ek iletişim maliyeti var |
| Geliştirme kolaylığı | Zor | Görece kolay |
| Kullanım alanı | Genel amaçlı depolama | Özel ve sanal sistemler |

## Python ile çalışan küçük bir örnek

Ubuntu tabanlı bir sistemde gerekli paketleri şu şekilde kurabiliriz:

```bash
sudo apt install fuse3 libfuse3-dev
python3 -m pip install fusepy
mkdir -p /tmp/benimfs
```

Aşağıdaki dosya sistemi yalnızca `merhaba.txt` isimli sanal bir dosya sunar. Dosyanın fiziksel diskte bulunması gerekmez; içerik Python tarafından anlık üretilir.

```python
from fuse import FUSE, Operations
import errno
import os

class BenimFS(Operations):
    mesaj = b"Merhaba, bu veri sanal dosya sisteminden geliyor!\n"

    def getattr(self, path, fh=None):
        if path == "/":
            return {
                "st_mode": 0o40555,
                "st_nlink": 2
            }

        if path == "/merhaba.txt":
            return {
                "st_mode": 0o100444,
                "st_nlink": 1,
                "st_size": len(self.mesaj)
            }

        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))

    def readdir(self, path, fh):
        return [".", "..", "merhaba.txt"]

    def open(self, path, flags):
        if path != "/merhaba.txt":
            raise OSError(errno.ENOENT, "Dosya bulunamadı")
        if flags & (os.O_WRONLY | os.O_RDWR):
            raise OSError(errno.EACCES, "Dosya salt okunur")
        return 0

    def read(self, path, size, offset, fh):
        return self.mesaj[offset:offset + size]

if __name__ == "__main__":
    FUSE(BenimFS(), "/tmp/benimfs", foreground=True)
```

`getattr()` dosyanın türünü, izinlerini ve boyutunu bildirir. `readdir()` dizin listesini üretir. `open()` erişim kurallarını denetlerken `read()` istenen aralıktaki baytları döndürür. Programı `python3 benimfs.py` ile çalıştırdıktan sonra başka bir terminalde `cat /tmp/benimfs/merhaba.txt` komutu kullanılabilir. Ayırmak için `fusermount3 -u /tmp/benimfs` yeterlidir.

## Tasarımda dikkat edilmesi gerekenler

Gerçek bir projede eşzamanlı erişim, önbellekleme, dosya tanıtıcıları, kullanıcı kimlikleri ve hata kodları hesaba katılmalıdır. `read()` metodunun tüm içeriği değil, yalnızca `offset` ile başlayan `size` baytı döndürmesi özellikle önemlidir. Aksi hâlde büyük dosyalarda beklenmedik sonuçlar oluşabilir.

| Amaç | Uygulanabilecek kural |
|---|---|
| Şifreli kasa | `write()` sırasında şifreleme |
| Bulut sürücüsü | `read()` sırasında API isteği |
| Denetim sistemi | Her erişimi günlüğe kaydetme |
| Dinamik rapor | Dosya açıldığında içerik üretme |

FUSE; prototipler, eğitim araçları, arşiv görüntüleyicileri ve uzak depolama istemcileri için güçlü bir oyun alanıdır. Çekirdeğe dalmadan işletim sisteminin dosya soyutlamasını kullanabilir, hatta bir REST API'yi klasör ve dosyalardan oluşan doğal bir arayüze dönüştürebilirsiniz.

![fuse-ile-python-34](/img/fuse-ile-python-34.svg)

