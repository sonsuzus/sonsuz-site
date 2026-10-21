---
layout: post
title: "df ve du Neden Farklı Sonuç Gösterir? Disk Kullanımının İki Yüzü"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - shell
  - df
  - du
  - disk-kullanımı
  - sistem-yönetimi
toc: true
image: /img/df-ve-du-10.png
---

Linux sunucunuz “Disk doldu!” diye alarm verirken `du` ile yaptığınız kontrolde hâlâ bolca yer görünmesi kafa karıştırıcı olabilir. Aslında `df` ve `du` aynı şeyi hatalı biçimde ölçmez; disk kullanımına farklı katmanlardan bakar. Biri dosya sisteminin muhasebe kayıtlarını, diğeri erişilebilen dosya ve dizinleri inceler.

``

## Temel fark: dosya sistemi ve dosyalar

`df`, adını “disk free” ifadesinden alır. Bağlı dosya sistemlerinin toplam, kullanılmış ve boş blok sayılarını çekirdek üzerinden sorgular:

```bash
df -h
```

Buradaki `-h`, değerleri GiB ve MiB gibi okunabilir birimlerle gösterir. Basitleştirilmiş biçimde `df` hesabı şöyledir:

$$
Kullanılan\ Alan = Toplam\ Bloklar - Boş\ Bloklar
$$

`du` ise “disk usage” anlamına gelir ve belirtilen yoldaki dosya ağacını dolaşır. Bulabildiği dosyaların kapladığı blokları toplar:

```bash
du -sh /var
```

`-s` yalnızca toplam sonucu, `-h` ise okunabilir birimleri verir. Yaklaşık hesap şu şekilde düşünülebilir:

$$
du(D) = \sum_{f \in D} Ayrılan\ Bloklar(f)
$$

Dolayısıyla `df` bütün dosya sistemini, `du` ise seçilen dizin ağacında erişebildiği girdileri raporlar.

| Özellik | `df` | `du` |
|---|---|---|
| Veri kaynağı | Dosya sistemi metadata bilgileri | Dizin ve dosya ağacı |
| Temel soru | Bölümde ne kadar yer kaldı? | Bu dizin ne kadar yer kaplıyor? |
| Silinmiş açık dosyaları görür mü? | Evet, kullanılan alana dahil eder | Hayır |
| Yetki sorunlarından etkilenir mi? | Genellikle hayır | Evet |
| Bağlama noktalarından etkilenir mi? | Her dosya sistemini ayrı gösterir | Başka dosya sistemlerine geçebilir |
| Çalışma maliyeti | Genellikle çok hızlı | Büyük ağaçlarda yavaş olabilir |

## En yaygın fark: silinmiş ama açık dosyalar

Bir uygulama büyük bir log dosyasını açık tutarken dosya `rm` ile silinirse dizin girdisi kaldırılır. Ancak süreç dosya tanımlayıcısını kapatıncaya kadar veri blokları serbest bırakılmaz. Bu durumda `du` dosyayı bulamaz, fakat `df` blokları hâlâ kullanımda görür.

Bu hayalet dosyaları bulmak için:

```bash
sudo lsof +L1
```

Çıktıda büyük bir dosya görürseniz ilgili servisi kontrollü biçimde yeniden başlatmak genellikle alanı serbest bırakır:

```bash
sudo systemctl restart uygulama-servisi
```

Üretim ortamında süreci doğrudan öldürmek yerine önce servis etkisini ve log yapılandırmasını incelemek daha güvenlidir.

## Diğer ayrışma nedenleri

Dosya sistemleri, normal kullanıcıların diski tamamen doldurmasını engellemek için ayrılmış bloklara sahip olabilir. Örneğin ext4 üzerinde yüzde 5 rezerv varsa normal kullanıcı boş alan göremezken `root` bu alanı kullanabilir. `df` çıktısındaki “available” değeri bu nedenle basit boş blok sayısından farklı olabilir.

Sparse, yani seyrek dosyalar da ayrı bir tuzaktır. Dosyanın mantıksal boyutu 10 GB olduğu hâlde diskte yalnızca birkaç MB blok ayrılmış olabilir:

```bash
truncate -s 10G seyrek.img
ls -lh seyrek.img
du -h seyrek.img
du --apparent-size -h seyrek.img
```

`ls` ve `du --apparent-size` mantıksal boyutu, standart `du` ise gerçekten ayrılmış alanı gösterir.

Ayrıca `du /` komutu `/mnt` veya `/proc` gibi alt bağlama noktalarına geçebilir. Yalnızca kök dosya sistemini incelemek için `-x` kullanmak daha doğru bir karşılaştırma sağlar:

```bash
sudo du -xsh /
df -h /
```

## Pratik teşhis sırası

Önce `df -hT` ile dolu dosya sistemini ve türünü belirleyin. Ardından aynı bağlama noktasında `du -x` kullanın. Sonuçlar ciddi ölçüde farklıysa `lsof +L1` ile silinmiş açık dosyaları, `df -i` ile inode tükenmesini ve bağlama noktalarını kontrol edin.

Kısacası `df` diskin muhasebecisi, `du` ise klasörleri tek tek gezen envanter görevlisidir. Raporların farklı çıkması çoğu zaman hata değil, iki aracın farklı sorulara cevap vermesidir.

![df-ve-du-10](/img/df-ve-du-10.svg)

