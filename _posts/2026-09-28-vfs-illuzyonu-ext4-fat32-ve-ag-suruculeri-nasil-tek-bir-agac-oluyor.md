---
layout: post
title: "VFS İllüzyonu: Ext4, FAT32 ve Ağ Sürücüleri Nasıl Tek Bir Ağaç Oluyor?"
math: true
categories: 
  - Bilgi
tags: 
  - vfs
  - linux
  - dosya sistemleri
  - ext4
  - fat32
  - kernel
  - sistem programlama
toc: true
image: /img/vfs-illuzyonu-ext4-39.png
---

Bir Linux programı `/home/ada/notlar.txt` dosyasını açarken diskin Ext4, FAT32, NFS veya başka bir dosya sistemiyle biçimlendirilmiş olup olmadığını genellikle bilmez. Program yalnızca yol, dosya ve dizin kavramlarını görür. Bu etkileyici illüzyonu oluşturan katman, çekirdekteki **VFS (Virtual File System)** yapısıdır. VFS, farklı kurallara sahip depolama sistemlerini ortak bir arayüzün arkasında buluşturan evrensel bir tercüman gibi çalışır.
``
## Neden bir soyutlama katmanı gerekiyor?

Ext4; Unix izinleri, sembolik bağlantılar ve günlükleme gibi özellikleri doğal olarak destekler. FAT32 ise daha basit bir yapıya sahiptir; Unix tarzı sahiplik bilgilerini diskte aynı biçimde saklamaz. NFS gibi ağ dosya sistemlerinde veriye ulaşmak için fiziksel diske değil, ağ üzerinden başka bir makineye istek gönderilir.

Buna rağmen kullanıcı programları çoğunlukla aynı sistem çağrılarını kullanır:

```c
int fd = open("/mnt/veri/rapor.txt", O_RDONLY);
char buffer[128];
ssize_t n = read(fd, buffer, sizeof(buffer));
close(fd);
```

Bu kod, dosyanın türünü sorgulamadan onu açar, okur ve kapatır. `open()` çağrısını karşılayan çekirdek, yolun hangi bağlama noktasına ait olduğunu bulur; ardından işlemi ilgili dosya sistemi sürücüsüne yönlendirir.

| Özellik | Ext4 | FAT32 | NFS | VFS'nin sunduğu görünüm |
|---|---|---|---|---|
| Veri konumu | Yerel disk | Yerel/çıkarılabilir disk | Uzak sunucu | Dosya yolu |
| Unix izinleri | Doğal | Sınırlı/türetilmiş | Sunucuya bağlı | Ortak izin API'si |
| Sembolik bağlantı | Var | Doğal olarak yok | Genellikle var | Destekleniyorsa standart işlem |
| Erişim yöntemi | Blok aygıtı | Blok aygıtı | Ağ protokolü | `open`, `read`, `write` |

## VFS'nin temel nesneleri

VFS, her şeyi tek bir dev nesneye dönüştürmez. Bunun yerine birkaç çekirdek veri yapısı arasında görev dağıtır:

- **Superblock:** Bağlanmış dosya sisteminin genel bilgisini temsil eder.
- **Inode:** Bir dosyanın türü, izinleri, sahibi ve boyutu gibi metadata bilgisini taşır.
- **Dentry:** Dosya adlarını inode'larla ilişkilendirir ve yol çözümlemeyi hızlandırır.
- **File:** Açılmış dosyanın süreç açısından durumunu, konumunu ve bayraklarını tutar.

Basitleştirilmiş olarak bir yol çözümleme maliyeti şöyle düşünülebilir:

$$T_{erişim} = T_{yol} + T_{VFS} + T_{sürücü} + T_{depolama}$$

Yerel Ext4 kullanımında son terim disk veya önbellek gecikmesidir. NFS kullanımında ise buna ağ gecikmesi de eklenir. VFS aynı arayüzü sağlasa da bütün dosya sistemlerini aynı hızda veya aynı yeteneklerde yapmaz.

## İşlem yönlendirme nasıl gerçekleşiyor?

Her dosya sistemi, VFS'nin beklediği operasyon tablolarını doldurur. Mantık kabaca şöyledir:

```c
struct file_operations ornek_islemler = {
    .read  = ornek_read,
    .write = ornek_write,
    .open  = ornek_open,
    .release = ornek_close
};
```

Bu yapı temsili bir örnektir. VFS, genel `read()` isteğini aldığında açık dosyayla ilişkili operasyon tablosundaki uygun fonksiyonu çağırır. Böylece Ext4 kendi blok eşleme mantığını, NFS ise ağ isteği oluşturma mekanizmasını çalıştırabilir.

## Tek ağaç illüzyonu

Windows dünyasındaki ayrı sürücü harflerinin aksine Linux, dosya sistemlerini tek bir kök ağaca bağlar:

```bash
mount /dev/sdb1 /mnt/fat32
mount -t nfs sunucu:/paylasim /mnt/ag
```

Bu komutlardan sonra `/mnt/fat32` ve `/mnt/ag`, `/` ile başlayan aynı ağacın dalları gibi görünür. Bağlama noktası geçildiğinde VFS, yol çözümlemeye başka bir superblock üzerinden devam eder. Kullanıcı açısından yalnızca dizin değiştirilmiştir; çekirdek açısından ise bambaşka bir depolama dünyasına geçilmiştir.

VFS'nin asıl başarısı farklılıkları yok etmek değil, onları **kontrollü biçimde saklamaktır**. FAT32'de bulunmayan izinlerin bağlama seçenekleriyle taklit edilmesi veya ağ bağlantısı kopunca NFS işleminin hata vermesi bunun sınırlarını gösterir. Yine de programcıya sunulan homojen dosya ağacı, işletim sistemlerinin en güçlü soyutlamalarından biridir: Alt katta türlü motorlar çalışırken üst katta herkes aynı direksiyonu kullanır.

![vfs-illuzyonu-ext4-39](/img/vfs-illuzyonu-ext4-39.svg)

