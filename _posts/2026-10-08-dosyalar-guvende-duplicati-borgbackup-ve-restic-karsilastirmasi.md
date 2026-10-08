---
layout: post
title: "Dosyalar Güvende: Duplicati, BorgBackup ve Restic Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - yedekleme
  - duplicati
  - borgbackup
  - restic
  - veri güvenliği
  - linux
toc: true
image: /img/dosyalar-guvende-duplicati-70.png
---

Bir diskin bozulması, yanlışlıkla çalıştırılan bir silme komutu veya fidye yazılımı, yılların verisini saniyeler içinde erişilemez hâle getirebilir. Neyse ki Duplicati, BorgBackup ve Restic; şifreleme, sıkıştırma ve artımlı yedekleme gibi modern özelliklerle “Keşke yedek alsaydım!” cümlesini tarihe gömmeyi amaçlıyor.
``

## Sağlam bir yedekleme sisteminin mantığı

Yedekleme, dosyaları başka bir klasöre kopyalamaktan ibaret değildir. Güvenilir bir plan için yaygın **3-2-1 kuralı** uygulanabilir:

- Verinin en az **3 kopyası** bulunmalı.
- Kopyalar **2 farklı ortamda** tutulmalı.
- Kopyalardan **1 tanesi uzak konumda** olmalı.

Depolama ihtiyacını azaltmak için üç araç da artımlı yedekleme yaklaşımından yararlanır. İlk çalıştırmada tüm veri saklanırken sonraki çalıştırmalarda yalnızca değişiklikler gönderilir. Basitleştirilmiş depolama hesabı şöyledir:

$$S = F + \sum_{i=1}^{n} \Delta_i$$

Burada $F$ ilk tam yedeğin boyutunu, $\Delta_i$ ise her çalıştırmada değişen veri miktarını temsil eder. Tekilleştirme sayesinde aynı veri bloklarının tekrar saklanması önlenebilir. Örneğin 10 GB’lık bir dosyanın yalnızca küçük bir bölümü değiştiğinde yeniden 10 GB göndermek gerekmez.

## Üç aracın karşılaştırması

| Özellik | Duplicati | BorgBackup | Restic |
|---|---|---|---|
| Kullanım biçimi | Web arayüzü ve CLI | Komut satırı | Komut satırı |
| İşletim sistemi | Windows, Linux, macOS | Özellikle Linux/macOS | Windows, Linux, macOS |
| Tekilleştirme | Var | Çok güçlü | Var |
| Şifreleme | AES-256 | Yerleşik | Yerleşik |
| Uzak depolama | Çok sayıda bulut servisi | Genellikle SSH | S3, SFTP ve çeşitli servisler |
| İdeal kullanıcı | Görsel arayüz isteyenler | Performans odaklı Linux kullanıcıları | Taşınabilirlik isteyenler |

**Duplicati**, tarayıcıdan yönetilen arayüzü sayesinde zamanlama, hedef seçimi ve geri yükleme işlemlerini kolaylaştırır. Google Drive, OneDrive ve S3 gibi hedeflere doğrudan bağlanabilmesi önemli bir avantajdır. Buna karşılık büyük yedek kümelerinde veritabanı bakımı gerekebilir.

**BorgBackup**, içerik tanımlı parçalama ve güçlü tekilleştirme özellikleriyle özellikle Linux sunucularında parlar. Depoların SSH üzerinden kullanılabilmesi güvenli ve hızlı bir yapı sunar. Ancak grafik arayüz bekleyen kullanıcılar için biraz fazla terminal kokabilir.

**Restic** ise sade komutları, tek dosyalık kurulumu ve platformlar arası desteğiyle öne çıkar. Şifreleme varsayılan tasarımın parçasıdır; yedek deposu ele geçirilse bile parola olmadan içerik okunamaz.

## BorgBackup ile örnek yedekleme

Önce şifreli bir depo oluşturulur, ardından proje dizini arşivlenir:

```bash
borg init --encryption=repokey-blake2 /mnt/backup/borg-repo
borg create --stats /mnt/backup/borg-repo::proje-{now} ~/projeler
```

İlk komut şifreli depoyu hazırlar. İkinci komut, tarih bilgisini taşıyan yeni bir anlık görüntü oluşturur. Eski yedekleri kontrollü biçimde temizlemek için şu politika uygulanabilir:

```bash
borg prune --list /mnt/backup/borg-repo \
  --keep-daily=7 --keep-weekly=4 --keep-monthly=6
```

Bu komut son yedi günlük, dört haftalık ve altı aylık yedeği korur.

## Restic ile uzak hedef kullanımı

Restic deposu SFTP üzerinde hazırlanabilir:

```bash
export RESTIC_REPOSITORY=sftp:user@sunucu:/yedekler/restic
restic init
restic backup ~/Belgeler ~/Fotoğraflar
restic check
```

`backup` verileri şifreleyerek gönderirken `check`, depo bütünlüğünü denetler. Parola otomasyon sırasında açıkça yazılmamalı; izinleri sınırlandırılmış bir parola dosyası veya güvenli sır yönetim sistemi kullanılmalıdır.

## Hangisini seçmeli?

Masaüstünde kolay yönetim ve bulut bağlantıları için **Duplicati**, Linux sunucusunda yüksek verimlilik için **BorgBackup**, farklı sistemlerde sade ve güvenli kullanım için **Restic** güçlü adaydır. Hangi araç seçilirse seçilsin, yalnızca yedek almak yeterli değildir. Düzenli geri yükleme testi yapılmayan bir yedek, açılana kadar Schrödinger’in yedeğidir: Hem vardır hem yoktur!

![dosyalar-guvende-duplicati-70](/img/dosyalar-guvende-duplicati-70.svg)

