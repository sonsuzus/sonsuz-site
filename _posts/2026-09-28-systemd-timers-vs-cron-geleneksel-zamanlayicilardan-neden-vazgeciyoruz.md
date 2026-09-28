---
layout: post
title: "Systemd Timers vs Cron: Geleneksel Zamanlayıcılardan Neden Vazgeçiyoruz?"
math: true
categories: 
  - Bilgi
tags: 
  - systemd
  - cron
  - linux
  - otomasyon
  - devops
  - zamanlayıcı
toc: true
image: /img/systemd-timers-vs-51.png
---

Cron, Unix dünyasının yıllara meydan okuyan çalar saatidir: Belirlenen zamanda çalar, komutu çalıştırır ve fazla soru sormaz. Ancak modern Linux sistemlerinde görevlerin yalnızca “saat 03.00’te çalışması” yetmiyor. Ağın hazır olması, önceki işlemin tamamlanması, kaçırılan görevlerin telafi edilmesi ve çıktıların merkezi biçimde izlenmesi gerekiyor. İşte systemd timer birimleri, klasik zamanlamayı servis yönetimiyle birleştirerek Cron’un bıraktığı boşlukları dolduruyor.
``

## İki farklı zamanlama yaklaşımı

Cron, satır tabanlı ve bağımsız bir zamanlayıcıdır. Her kayıt, zaman ifadesi ile çalıştırılacak komutu eşleştirir. Systemd ise zamanlamayı iki parçaya ayırır: `.timer` birimi **ne zaman**, `.service` birimi ise **ne çalışacağını** tanımlar. Bu ayrım ilk bakışta fazladan dosya gibi görünse de bağımlılık, güvenlik ve kaynak yönetimi açısından büyük esneklik sağlar.

Periyodik bir görevin ideal çalışma anını basitçe şöyle düşünebiliriz:

$$t_n = t_0 + nP$$

Burada $t_0$ başlangıç anını, $P$ periyodu ve $n$ çalıştırma sırasını temsil eder. Cron çoğunlukla takvimdeki sabit anları hedeflerken systemd, bu modele açılıştan sonra geçen süre veya son çalıştırmadan itibaren geçen süre gibi monoton zaman ölçümlerini de ekler.

| Özellik | Cron | Systemd Timer |
|---|---|---|
| Zaman hassasiyeti | Genellikle dakika | Saniye ve daha ince aralıklar |
| Bağımlılık yönetimi | Yerleşik değil | Birimler arasında desteklenir |
| Kaçırılan görev | Genellikle çalışmaz | `Persistent=true` ile telafi edilir |
| Loglama | E-posta, dosya veya syslog ayarı gerekir | `journalctl` ile bütünleşiktir |
| Kaynak sınırlama | Harici araç gerekir | CPU, bellek ve süreç sınırları uygulanabilir |
| Rastgele gecikme | Ek betik gerekir | `RandomizedDelaySec` kullanılabilir |

## Cron ile geleneksel örnek

Her gece 03.00’te yedek almak için crontab satırı oldukça kısadır:

```cron
0 3 * * * /usr/local/bin/backup.sh
```

Bu sadelik Cron’un en büyük gücüdür. Fakat makine 03.00’te kapalıysa görev kaçar. Betiğin hangi ortam değişkenleriyle çalıştığı veya çıktısının nereye gittiği de ayrıca yönetilmelidir.

## Aynı görevi systemd ile kurmak

Önce işlemi tanımlayan `/etc/systemd/system/backup.service` dosyasını oluştururuz:

```ini
[Unit]
Description=Gece yedeklemesini çalıştır
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
User=backup
```

`After` ve `Wants`, görevin ağ hazırlandıktan sonra başlamasını sağlar. `Type=oneshot`, komut tamamlanınca servisin bitmiş sayılacağını belirtir. Ardından `/etc/systemd/system/backup.timer` zamanlamayı üstlenir:

```ini
[Unit]
Description=Gece yedekleme zamanlayıcısı

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
RandomizedDelaySec=10m
Unit=backup.service

[Install]
WantedBy=timers.target
```

`Persistent=true`, bilgisayar kapalıyken kaçırılan çalıştırmayı açılış sonrasında gerçekleştirir. `RandomizedDelaySec=10m` ise görevi on dakikalık pencereye dağıtır. Yüz sunucunun aynı saniyede yedekleme başlatıp depolama sistemine küçük çaplı bir trafik kıyameti yaşatmasını böylece önleyebiliriz.

Yapılandırmayı etkinleştirmek ve kontrol etmek için:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
systemctl list-timers
journalctl -u backup.service
```

Son komut, ayrı log dosyası tasarlamadan servisin standart çıktısını ve hatalarını gösterir.

## Cron tamamen öldü mü?

Hayır. Tek kullanıcılı makinelerdeki basit, dakika tabanlı görevler için Cron hâlâ anlaşılır ve taşınabilir bir çözümdür. Systemd timer ise modern Linux sunucularında gözlemlenebilirlik, kaçırılan görevlerin telafisi, güvenlik seçenekleri ve servis bağımlılıkları gerektiğinde öne çıkar.

Kısacası Cron bir alarm saatiyse systemd timer; alarmı, görev yöneticisi ve kayıt defteri bulunan akıllı bir asistandır. Birkaç satır daha fazla yapılandırma ister, ancak üretim ortamında “Görev neden çalışmadı?” sorusuna çok daha hızlı cevap verir.

![systemd-timers-vs-51](/img/systemd-timers-vs-51.svg)

