---
layout: post
title: "Linux initramfs'in Sırrı: Kök Dosya Sisteminden Önceki Minik Dünya"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - initramfs
  - kernel
  - önyükleme
  - sistem-yönetimi
  - ramdisk
toc: true
image: /img/linux-initramfsin-sirri-12.png
---

![linux-initramfsin-sirri-12](/img/linux-initramfsin-sirri-12.svg)


Bilgisayarın güç düğmesine bastığınızda Linux doğrudan `/` dizinine koşmaz. Çekirdek belleğe yüklense bile gerçek kök dosya sistemine ulaşmak için disk denetleyicisi, dosya sistemi, RAID, LVM veya şifreleme sürücülerine ihtiyaç duyabilir. İşte **initramfs**, bu tavuk-yumurta problemini çözen, RAM üzerinde kurulmuş geçici ve küçük bir kullanıcı alanıdır.
``
## Açılış zincirindeki yeri

Modern bir Linux açılışı kabaca şu sırayı izler:

1. BIOS veya UEFI donanımı hazırlar.
2. GRUB gibi önyükleyici çekirdeği ve initramfs arşivini RAM'e taşır.
3. Çekirdek donanımı algılar ve initramfs'i geçici kök olarak açar.
4. Initramfs içindeki `/init` programı gerekli hazırlıkları yapar.
5. Gerçek kök dosya sistemi bağlanır.
6. `switch_root` sonrasında systemd veya başka bir init sistemi başlatılır.

Toplam açılış süresini basitleştirerek şöyle düşünebiliriz:

$$T_{boot} = T_{firmware} + T_{loader} + T_{kernel} + T_{initramfs} + T_{userspace}$$

Initramfs aşaması küçük görünür; ancak şifreli diskin parolasını bekliyorsa veya kayıp bir depolama aygıtını arıyorsa $T_{initramfs}$ ciddi biçimde büyüyebilir.

## Initramfs gerçekte nedir?

Initramfs genellikle `cpio` biçiminde paketlenmiş ve gzip, xz ya da zstd ile sıkıştırılmış bir arşivdir. Önyükleyici bu arşivi RAM'e yükler; çekirdek de arşivi kendi sağladığı geçici `rootfs` üzerine açar. Dolayısıyla klasik anlamda biçimlendirilmiş bir RAM diski olmak zorunda değildir.

| Özellik | initramfs | Gerçek kök dosya sistemi |
|---|---|---|
| Konum | RAM | SSD, HDD, ağ veya başka depolama |
| Ömür | Açılışın erken aşaması | Sistem kapanana kadar |
| İçerik | Araçlar, betikler, modüller | Tam Linux kullanıcı alanı |
| Temel görev | Gerçek kökü erişilebilir yapmak | Uygulamaları ve hizmetleri çalıştırmak |
| Boyut | Genellikle onlarca MB | GB veya TB düzeyi |

Bu ortamda BusyBox, `udev`, `cryptsetup`, LVM araçları, dosya sistemi yardımcıları ve çekirdek modülleri bulunabilir. Amaç masaüstü açmak değil, ana sisteme giden köprüyü kurmaktır.

## Çekirdek neden tek başına yetmiyor?

Çekirdek bazı sürücüleri doğrudan içine gömülü taşıyabilir. Fakat her sürücüyü çekirdeğe kalıcı olarak eklemek onu büyütür ve esnekliği azaltır. Modüler yaklaşımda gerekli `.ko` dosyaları initramfs'e yerleştirilir. Örneğin kök bölümünüz NVMe üzerinde ve ext4 biçimindeyse NVMe denetleyicisi ile ext4 desteğinin gerçek köke ulaşılmadan önce hazır olması gerekir.

Şifreli bir LVM düzeninde süreç daha eğlencelidir: initramfs önce disk sürücüsünü yükler, ardından LUKS kapsayıcısını `cryptsetup` ile açar, LVM mantıksal birimlerini etkinleştirir ve ancak bundan sonra kök dosya sistemini bağlar. Ağ üzerinden NFS kökü kullanılıyorsa ağ kartı sürücüsü, IP yapılandırması ve NFS desteği de bu minik çantaya eklenir.

## İçeriği nasıl inceleriz?

Dağıtıma göre dosya adı değişse de mevcut arşivi listelemek kolaydır:

```bash
# Çalışan çekirdeğe ait initramfs içeriğini listeler.
lsinitramfs /boot/initrd.img-$(uname -r) | less
```

Fedora ve RHEL ailesinde benzer inceleme `lsinitrd` ile yapılır. Debian veya Ubuntu üzerinde initramfs'i yeniden üretmek için:

```bash
# Kurulu tüm çekirdeklerin initramfs dosyalarını günceller.
sudo update-initramfs -u -k all
```

Dracut kullanan sistemlerde karşılığı çoğunlukla şöyledir:

```bash
# Mevcut çekirdek için initramfs'i zorla yeniden oluşturur.
sudo dracut --force
```

Bu komutlar özellikle yeni depolama sürücüsü eklediğinizde, kök bölüm yapısını değiştirdiğinizde veya açılışta gerekli modül arşive girmediğinde önemlidir.

## Hata olduğunda ne görürüz?

Initramfs gerçek kökü bulamazsa sistem acil durum kabuğuna düşebilir; `unable to find root device`, `ALERT! UUID does not exist` veya LUKS aygıtına ilişkin hatalar görülebilir. Bu noktada `cat /proc/cmdline`, `blkid`, `ls /dev` ve `dmesg` komutları güçlü dedektif araçlarıdır. Yanlış UUID, eksik modül ya da hatalı çekirdek parametresi genellikle suçludur.

Kısacası initramfs, Linux açılışının sahne arkasındaki teknik ekip gibidir: dekoru kurar, kapıları açar, gerçek kökü sahneye çıkarır ve işi bittiğinde sessizce ortadan kaybolur.
