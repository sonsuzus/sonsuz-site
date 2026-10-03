---
layout: post
title: "1 GB RAM’lik Sunucularda Hayatta Kalma Rehberi: OOM Killer’ı Evcilleştirmek"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - oom-killer
  - bellek-yönetimi
  - swap
  - sunucu-optimizasyonu
  - devops
toc: true
image: /img/1-gb-ramlik-24.png
---

![1-gb-ramlik-24](/img/1-gb-ramlik-24.svg)


1 GB RAM’li bir sanal sunucu, doğru yönetildiğinde küçük web siteleri, API’ler ve otomasyon servisleri için şaşırtıcı derecede yeteneklidir. Ancak kontrolsüz bir uygulama, birkaç Docker konteyneri veya coşkulu bir veritabanı sorgusu belleği tükettiğinde Linux’un OOM Killer mekanizması sahneye çıkar. Bu rehberde amacımız OOM Killer’ı tamamen devre dışı bırakmak değil; belleği ölçmek, patlamaları sınırlamak ve çekirdeğe kimi feda edeceğini daha bilinçli biçimde anlatmaktır.

``

## OOM Killer neden ortaya çıkar?

Linux, fiziksel RAM’i süreçler, çekirdek önbellekleri ve dosya cache’i arasında paylaştırır. Bir sistemin kabaca kullanılabilir bellek kapasitesi şöyle düşünülebilir:

$$M_{toplam} = M_{RAM} + M_{swap}$$

Fakat `free` çıktısındaki boş RAM’in az olması tek başına kriz değildir. Linux kullanılmayan belleği disk cache’i olarak değerlendirir ve gerektiğinde geri alabilir. Asıl tehlike, süreçlerin aktif bellek taleplerinin karşılanamamasıdır. Çekirdek yeterli sayfa boşaltamazsa OOM Killer, sistemi tamamen kilitlemek yerine bir süreci sonlandırır.

| Kavram | Anlamı | Neden önemli? |
|---|---|---|
| RSS | Sürecin fiziksel RAM’de tuttuğu alan | Gerçek baskıyı gösterir |
| VSZ | Ayrılmış sanal adres alanı | Tek başına RAM tüketimi değildir |
| Available | Yeni işler için kullanılabilecek tahmini bellek | `free` değerinden daha anlamlıdır |
| Swap | Disk veya sıkıştırılmış RAM desteği | Ani sıçramalara zaman kazandırır |

## Önce ölç, sonra buda

Bellek sorunlarını tahminlerle çözmek, karanlıkta sinek avlamaya benzer. Aşağıdaki komutlar en çok RAM kullanan süreçleri ve genel durumu gösterir:

```bash
free -h
ps aux --sort=-%mem | head -n 10
vmstat 1
journalctl -k | grep -i -E 'oom|killed process'
```

`vmstat` çıktısındaki `si` ve `so`, swap giriş-çıkışını gösterir. Bu değerler sürekli hareketliyse sunucu yalnızca swap kullanmıyor, adeta disk üzerinde yaşamaya çalışıyordur. `journalctl` ise hangi sürecin OOM tarafından öldürüldüğünü doğrulamanızı sağlar.

## Uygulamaya bellek sınırı koymak

Bir uygulamanın bütün RAM’i sahiplenmesini önlemenin en temiz yolu cgroup sınırlarıdır. Systemd servisine aşağıdaki ayarlar eklenebilir:

```ini
[Service]
MemoryHigh=600M
MemoryMax=750M
OOMScoreAdjust=200
Restart=on-failure
```

`MemoryHigh`, süreçleri yavaşlatan yumuşak bir baskı noktasıdır. `MemoryMax` ise aşılmaması gereken sert tavandır. `OOMScoreAdjust=200`, çekirdeğe bu servisin kritik sistem süreçlerinden önce feda edilebileceğini söyler. Değişiklikten sonra yapılandırmayı etkinleştirin:

```bash
sudo systemctl daemon-reload
sudo systemctl restart uygulamam.service
```

Docker kullanıyorsanız aynı yaklaşım `--memory=600m --memory-swap=900m` seçenekleriyle uygulanabilir. Limitsiz konteyner, küçük VPS’in açık büfesine bırakılmış aç bir canavar gibidir.

## Swap: can simidi, sürat teknesi değil

Swap, RAM’in yerine geçmez; kısa süreli bellek sıçramalarında OOM kararını geciktirir. SSD üzerinde 1–2 GB swap, 1 GB RAM’li sunucular için genellikle makul bir güvenlik katmanıdır.

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Kalıcı olması için `/etc/fstab` dosyasına `/swapfile none swap sw 0 0` satırı eklenir. Swap kullanım isteği `vm.swappiness` ile ayarlanır:

```bash
sudo sysctl vm.swappiness=20
```

| Değer | Davranış |
|---|---|
| 1–10 | Swap’a oldukça geç yönelir |
| 20–40 | Küçük sunucular için dengeli olabilir |
| 60+ | Daha istekli swap kullanır |

Disk erişimi pahalıysa zram da değerlendirilebilir. Zram, verileri RAM içinde sıkıştırır; işlemci harcayarak daha fazla etkili bellek sağlar.

## OOM önceliğini dikkatle değiştirin

Bir sürecin OOM puanı `/proc/PID/oom_score` üzerinden görülebilir. `oom_score_adj` değeri $-1000$ ile $1000$ arasındadır. Yüksek değer öldürülme ihtimalini artırır; `-1000` ise süreci neredeyse dokunulmaz yapar.

```bash
cat /proc/$(pidof nginx)/oom_score
sudo sh -c 'echo -200 > /proc/$(pidof nginx)/oom_score_adj'
```

Her servisi korumaya çalışmayın. Herkes VIP olursa çekirdek kimi dışarı atacağını bilemez. SSH, izleme ve ters proxy gibi erişim için gerekli servisleri koruyup yeniden üretilebilir worker süreçlerini daha feda edilebilir bırakın.

Son olarak uygulama önbelleklerini sınırlayın, gereksiz servisleri kapatın, veritabanı buffer ayarlarını küçültün ve bellek metriklerine alarm ekleyin. Küçük sunucularda başarı, RAM’i hiç doldurmamak değil; dolduğunda sistemin kontrollü ve öngörülebilir davranmasını sağlamaktır.
