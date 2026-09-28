---
layout: post
title: "UEFI Boot Sürecinin Anatomisi: Eski BIOS'un Karanlığından Çıkış"
math: true
categories: 
  - Bilgi
tags: 
  - uefi
  - bios
  - önyükleme
  - işletim-sistemleri
  - donanım
  - güvenlik
toc: true
image: /img/uefi-boot-surecinin-47.png
---

Bilgisayarın güç düğmesine bastığınızda ekranda logo görünmeden önce oldukça hareketli bir dünya uyanır. Eski BIOS, diskin ilk sektöründeki birkaç yüz bayta bel bağlayan bir kapıcıyken UEFI; dosya sistemi okuyabilen, uygulama çalıştırabilen ve güvenlik politikaları uygulayabilen küçük bir işletim sistemi gibidir. Gelin işlemcinin ilk komutundan işletim sistemi çekirdeğine kadar uzanan bu görünmez yolculuğu parçalarına ayıralım.

``

## BIOS neden artık yeterli değildi?

Klasik BIOS, açılışta POST işlemini gerçekleştirir, önyükleme sırasındaki diski seçer ve diskin ilk 512 baytlık sektörünü belleğe yüklerdi. Bu sektör MBR olarak adlandırılır. MBR içinde hem bölüm tablosu hem de minicik bir önyükleme kodu bulunur. Kullanılabilir kod alanının yaklaşık 446 bayt olması, modern sistemler için pek ferah sayılmaz.

MBR ayrıca 32 bitlik sektör adresleri kullanır. Sektör boyutu 512 bayt olduğunda erişilebilen teorik kapasite:

$$2^{32} \times 512 \approx 2\ \text{TiB}$$

Dolayısıyla büyük diskler, gelişmiş güvenlik beklentileri ve daha esnek açılış senaryoları BIOS–MBR ikilisini emekliliğe yaklaştırdı.

| Özellik | Klasik BIOS | UEFI |
|---|---|---|
| Önyükleme kaynağı | Diskin ilk sektörü | EFI dosyaları |
| Bölümleme | MBR | Genellikle GPT |
| Çalışma modu | 16 bit | 32 veya 64 bit |
| Büyük disk desteği | Yaklaşık 2 TiB | Çok daha yüksek |
| Güvenlik | Yerleşik doğrulama yok | Secure Boot mevcut |
| Arayüz | Temel metin ekranı | Grafik, fare ve ağ desteği olabilir |

## UEFI açılış zinciri

Güç verildiğinde işlemci firmware içindeki başlangıç adresinden çalışmaya başlar. UEFI önce işlemciyi, belleği ve anakart bileşenlerini hazırlar. Bu süreç kabaca SEC, PEI ve DXE aşamalarına ayrılır. SEC güvenli bir başlangıç ortamı kurar; PEI belleği hazırlar; DXE ise sürücüleri yükleyerek donanımları kullanılabilir hâle getirir.

Ardından Boot Device Selection aşaması devreye girer. Firmware, kalıcı NVRAM içinde tutulan `BootOrder` ve `Boot####` değişkenlerini inceler. Seçilen kayıt, genellikle GPT ile biçimlendirilmiş diskteki EFI System Partition üzerinde bulunan bir `.efi` uygulamasını gösterir.

Tipik dosya yolları şöyledir:

```text
EFI/
├── Microsoft/Boot/bootmgfw.efi
├── ubuntu/shimx64.efi
└── Boot/bootx64.efi
```

Buradaki programlar ham sektörlere sıkışmış kod parçaları değildir. PE/COFF biçimindeki gerçek yürütülebilir dosyalardır. UEFI bunları çoğunlukla FAT32 olan bölüme girerek normal bir dosya gibi bulur ve çalıştırır. `EFI/Boot/bootx64.efi` yolu ise özellikle çıkarılabilir aygıtlar için kullanılan varsayılan kaçış kapısıdır.

## Boot manager'dan çekirdeğe

Çalıştırılan EFI programı Windows Boot Manager, GRUB, systemd-boot veya doğrudan UEFI uyumlu bir çekirdek olabilir. Bir Linux sisteminde GRUB yapılandırmayı okur, kullanıcıya menü sunar, çekirdeği ve initramfs dosyasını belleğe taşır. Sonra kontrolü çekirdeğe devreder.

UEFI uygulamaları bu sırada firmware servislerinden yararlanabilir. Ancak işletim sistemi hazır olduğunda `ExitBootServices()` çağrılır. Bu çağrı, “Teşekkürler firmware, direksiyonu artık ben alıyorum” demektir. Boot Services kapanır; yalnızca saat ve NVRAM erişimi gibi sınırlı Runtime Services kalabilir.

Linux altında UEFI kayıtlarını görmek için şu komut kullanılabilir:

```bash
sudo efibootmgr -v
```

Komut; açılış sırasını, etkin kayıtları ve bunların hangi EFI dosyasına yöneldiğini gösterir. Kayıtları değiştirirken dikkat gerekir; yanlış bir sıra sistemi bozmasa bile açılışı küçük bir hazine avına çevirebilir.

## Secure Boot neyi güvenceye alır?

Secure Boot, çalıştırılacak EFI dosyasının güvenilir bir anahtarla imzalanıp imzalanmadığını denetler. Basitleştirilmiş doğrulama mantığı şöyledir:

$$\operatorname{Verify}(K_{pub},\ signature,\ H(file)) = true$$

Sonuç doğruysa uygulama çalıştırılır; değilse zincir durdurulur. Secure Boot tek başına tüm zararlı yazılımları engellemez, fakat firmware ile çekirdek arasındaki önyükleme zincirinin izinsiz değiştirilmesini zorlaştırır.

Özetle UEFI, BIOS'un yalnızca daha renkli sürümü değildir. Dosya sistemi, sürücüler, uygulamalar, değişkenler ve kriptografik doğrulama sağlayan modüler bir platformdur. Modern bilgisayar açılırken ilk sektörün karanlığında el yordamıyla ilerlemek yerine düzenli, denetlenebilir ve genişletilebilir bir yol haritası izler.

![uefi-boot-surecinin-47](/img/uefi-boot-surecinin-47.svg)

