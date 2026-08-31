---
layout: post
title: "1 GB RAM’li Linux Sunucularda Swap Alanı Yapılandırma ve Optimizasyon Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - swap
  - sunucu optimizasyonu
toc: true
---

Yalnızca 1 GB RAM’e sahip bir Linux sunucu; küçük web siteleri, kişisel projeler ve düşük trafikli API’ler için yeterli olabilir. Ancak veritabanı, PHP-FPM veya Docker gibi servisler aynı anda belleğe yüklendiğinde RAM hızla tükenebilir. Swap alanı, tam bu noktada devreye girerek sunucunun ani bellek krizlerinde çökmesi yerine biraz yavaşlayarak çalışmaya devam etmesini sağlar.

``

## Swap Nedir ve Nasıl Çalışır?

Swap, diskin RAM yetersiz kaldığında geçici bellek olarak kullanılan bölümüdür. Linux çekirdeği, uzun süredir kullanılmayan bellek sayfalarını RAM’den swap alanına taşıyarak aktif işlemler için yer açar.

Toplam kullanılabilir sanal bellek kabaca şöyle düşünülebilir:

$$M_{sanal} = M_{RAM} + M_{swap}$$

1 GB RAM ve 2 GB swap bulunan bir sunucuda teorik sanal bellek 3 GB’dır. Bununla birlikte swap, gerçek RAM’in doğrudan alternatifi değildir. RAM nanosaniye düzeyinde erişim sağlarken disk erişimi çok daha yavaştır. Özellikle klasik HDD üzerinde yoğun swap kullanımı sunucuyu adeta ağır çekime alabilir.

| Özellik | RAM | Swap |
|---|---|---|
| Hız | Çok yüksek | Daha düşük |
| Kullanılan donanım | Bellek modülü | SSD veya HDD |
| Amaç | Aktif verileri çalıştırmak | Bellek baskısını azaltmak |
| Dolduğunda sonuç | OOM riski oluşur | Sistem ciddi biçimde yavaşlar |

Swap bulunmadığında RAM tamamen dolarsa Linux’un **OOM Killer** mekanizması devreye girer. Bu mekanizma, sistemi kurtarmak için yüksek bellek tüketen süreçlerden birini sonlandırır. Kurban bazen önemsiz bir işlem, bazen de veritabanınız olabilir; yani OOM Killer biraz huysuz bir trafik polisi gibidir.

## Ne Kadar Swap Ayrılmalı?

1 GB RAM’e sahip genel amaçlı bir sunucu için 1-2 GB swap çoğunlukla yeterlidir. Hazırda bekletme kullanılmayan sunucularda swap alanının RAM’in iki katı olması zorunlu bir kural değildir.

| Sunucu iş yükü | Önerilen swap |
|---|---:|
| Hafif web sitesi | 1 GB |
| WordPress ve veritabanı | 1-2 GB |
| Docker veya derleme işleri | 2-4 GB |
| Sürekli yüksek bellek kullanımı | RAM yükseltmek daha doğru |

## Swap Dosyası Oluşturma

Önce mevcut durumu kontrol edin:

```bash
free -h
swapon --show
```

Aşağıdaki komutlar 2 GB boyutunda bir swap dosyası oluşturur:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

`chmod 600`, diğer kullanıcıların swap dosyasına erişmesini engeller. `mkswap` dosyayı takas alanı biçimine dönüştürür, `swapon` ise yeniden başlatma beklemeden etkinleştirir.

Ayarın kalıcı olması için `/etc/fstab` dosyasına şu satırı ekleyin:

```text
/swapfile none swap sw 0 0
```

Ardından yapılandırmayı doğrulayın:

```bash
sudo swapon --show
free -h
```

## Swappiness Değerini Optimize Etme

`vm.swappiness`, Linux’un swap kullanmaya ne kadar istekli olduğunu belirleyen 0-100 arası bir değerdir. Yüksek değer erken, düşük değer ise daha geç swap kullanımı anlamına gelir.

```bash
cat /proc/sys/vm/swappiness
sudo sysctl vm.swappiness=10
```

1 GB’lık web sunucularında `10` veya `20`, genellikle iyi bir başlangıçtır. Ayarı kalıcı yapmak için `/etc/sysctl.d/99-swap.conf` dosyasını oluşturun:

```bash
vm.swappiness=10
vm.vfs_cache_pressure=50
```

Sonrasında ayarları yükleyin:

```bash
sudo sysctl --system
```

`vfs_cache_pressure=50`, inode ve dizin önbelleklerinin daha uzun süre korunmasına yardım eder. Ancak sihirli bir sayı yoktur; gerçek sonuç iş yüküne göre ölçülmelidir.

## İzleme ve Son Tavsiyeler

Swap kullanımını `free -h`, `vmstat 1` ve `htop` ile takip edebilirsiniz. `vmstat` çıktısındaki `si` ve `so` değerlerinin sürekli yüksek olması, swap giriş-çıkışının yoğunlaştığını gösterir.

Swap, kısa süreli bellek sıçramalarına karşı güvenlik ağıdır; yetersiz RAM sorununu sonsuza kadar çözmez. Sunucu devamlı swap kullanıyor, yanıt süreleri yükseliyor ve OOM kayıtları oluşuyorsa uygulama servislerini sınırlandırmak, gereksiz süreçleri kapatmak veya RAM’i yükseltmek gerekir. İyi ayarlanmış swap paraşüttür; motor değildir.
