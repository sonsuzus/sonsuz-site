---
layout: post
title: "Immutable Infrastructure: Sunucuyu Yamalamak Yerine Baştan Yaratmak"
math: true
categories: 
  - Bilgi
tags: 
  - immutable infrastructure
  - devops
  - cloud
  - otomasyon
  - packer
  - terraform
toc: true
image: /img/immutable-infrastructure-sunucuyu-25.png
---

Bir sunucu yıllarca çalıştıkça üzerine yamalar, geçici ayarlar ve “şimdilik böyle kalsın” çözümleri birikir. Sonunda kimsenin dokunmaya cesaret edemediği dijital bir antikaya dönüşür. Immutable Infrastructure, yani değişmez altyapı yaklaşımı, bu sorunu radikal bir kuralla çözer: Çalışan sunucuyu güncelleme; yeni sürümü içeren temiz bir imaj üret, yeni sunucuları başlat ve eskilerini çöpe at.
``

## Değişmezlik tam olarak ne demek?

Buradaki “değişmez” ifadesi sunucunun hiçbir veriyi değiştiremeyeceği anlamına gelmez. Temel fikir, sunucunun işletim sistemi, uygulama sürümü ve sistem paketleri gibi tanımlayıcı bileşenlerinin canlı ortamda değiştirilmemesidir. Kalıcı veriler veritabanı, nesne depolama veya yönetilen disk gibi haricî sistemlerde tutulur.

Klasik modelde bir sunucuya bağlanıp şu işlemleri yapabiliriz:

```bash
sudo apt update
sudo apt install uygulama-v2
sudo systemctl restart uygulama
```

Bu komutlar basit görünür; ancak yüz sunucunun doksan dokuzunda başarılı olup birinde başarısız olabilir. O tek sunucu artık diğerlerinden farklıdır. Buna **configuration drift**, yani yapılandırma kayması denir.

| Yaklaşım | Güncelleme biçimi | Geri dönüş | Yapılandırma kayması |
|---|---|---|---|
| Mutable | Çalışan sunucu yamalanır | Eski paket yeniden kurulur | Yüksek |
| Immutable | Yeni imaj ve sunucu oluşturulur | Eski sunucu grubuna dönülür | Düşük |
| Konteyner tabanlı | Yeni container imajı dağıtılır | Önceki etiket çalıştırılır | Çok düşük |

## Güvenilirliğin matematiği

Her manuel güncellemenin hata olasılığı $p$, güncellenen sunucu sayısı $n$ olsun. Tüm işlemlerin kusursuz tamamlanma olasılığı yaklaşık olarak şöyledir:

$$P(başarı) = (1-p)^n$$

Örneğin hata ihtimali yalnızca $p=0.01$ ve sunucu sayısı $n=100$ olduğunda bütün sunucuların doğru güncellenme olasılığı $(0.99)^{100} \approx 0.366$ olur. Otomatik imaj üretiminde ise değişiklik bir kez uygulanır, test edilir ve aynı çıktı her makineye dağıtılır. Böylece yüz farklı güncelleme süreci yerine doğrulanmış tek bir artefakt kullanılır.

## İmaj üretme hattı

Değişmez altyapının kalbinde “golden image” bulunur. Bu imaj; işletim sistemini, güvenlik yamalarını, çalışma ortamını ve uygulamayı içerir. Packer ile basitleştirilmiş bir AWS imajı şöyle tanımlanabilir:

```hcl
source "amazon-ebs" "app" {
  instance_type = "t3.micro"
  source_ami    = var.base_ami
  ssh_username  = "ubuntu"
  ami_name      = "uygulama-${var.version}"
}

build {
  sources = ["source.amazon-ebs.app"]

  provisioner "shell" {
    script = "scripts/install-app.sh"
  }
}
```

Bu yapılandırma temel bir makine açar, kurulum betiğini çalıştırır ve sürümlenmiş bir AMI üretir. Oluşan imaj güvenlik taramalarından ve entegrasyon testlerinden geçtikten sonra dağıtıma hazırdır.

Dağıtım genellikle blue-green yöntemiyle yapılır. “Blue” mevcut sistem, “green” ise yeni imajla oluşturulan gruptur. Green makineler sağlık kontrollerini geçtiğinde yük dengeleyicinin trafiği kademeli olarak onlara yönlendirilir. Sorun çıkarsa trafik blue grubuna çevrilir; gece yarısı paket kaldırma operasyonuna gerek kalmaz.

## Bedelsiz sihir değil

Immutable Infrastructure güçlüdür fakat hazırlık ister. İmaj üretimi uzun sürebilir, depolama maliyeti oluşturabilir ve veritabanı şema değişiklikleri dikkatle tasarlanmalıdır. Yeni uygulama sürümü eski şemayla bir süre çalışabilmeli; önce geriye uyumlu şema genişletilmeli, ardından kullanılmayan alanlar kaldırılmalıdır.

Ayrıca sunucunun yerel diskine yazılan dosyalar makine silindiğinde kaybolur. Loglar merkezî bir sisteme gönderilmeli, kullanıcı yüklemeleri nesne depolamada ve oturum bilgileri Redis benzeri haricî servislerde saklanmalıdır.

## Sunucular evcil hayvan değil, sürüdür

Geleneksel sunucular isim verilen, özenle iyileştirilen evcil hayvanlara benzer. Değişmez sunucular ise aynı özelliklere sahip bir sürüdür; biri bozulursa tedavi edilmez, yenisi oluşturulur. Bu zihniyet sürüm izlenebilirliği, hızlı geri dönüş, tutarlı ortamlar ve daha küçük saldırı yüzeyi sağlar. Kısacası güvenilirliğin kaynağı kusursuz sunucular değil, sunucuları güvenle ve tekrar tekrar üretebilen otomasyondur.

![immutable-infrastructure-sunucuyu-25](/img/immutable-infrastructure-sunucuyu-25.svg)

