---
layout: post
title: "Cron Çalışıyor Ama Script Çalışmıyor: PATH ve Ortam Değişkenleri Tuzağı"
math: true
categories: 
  - Bilgi
tags: 
  - cron
  - shell
  - linux
  - path
  - bash
  - hata ayıklama
toc: true
image: /img/cron-calisiyor-ama-55.png
---

Terminalde kusursuz çalışan bir script’in cron tarafından başlatıldığında hata vermesi, Linux dünyasının klasik “ama benim makinemde çalışıyordu” vakalarındandır. Suç çoğu zaman cron’da değil; interaktif shell ile cron job’ının farklı `PATH`, çalışma dizini ve ortam değişkenleri kullanmasındadır.
``
## Aynı kullanıcı, neden farklı sonuç?

Terminal açtığımızda Bash genellikle `.bashrc`, `.profile` veya `.bash_profile` gibi başlangıç dosyalarını okuyabilir. Bu dosyalar `PATH`, dil ayarları, alias’lar ve uygulamalara özel değişkenler tanımlar. Cron ise öngörülebilir olmak amacıyla oldukça sade bir ortam oluşturur ve interaktif shell yapılandırmasını kendiliğinden yüklemez.

| Özellik | İnteraktif shell | Cron ortamı |
|---|---|---|
| `PATH` | Genellikle genişletilmiş | Kısa ve sistem odaklı |
| Başlangıç dosyaları | Çoğunlukla okunur | Genellikle okunmaz |
| Çalışma dizini | Kullanıcının seçtiği dizin | Çoğu zaman kullanıcının ev dizini |
| Alias ve fonksiyonlar | Kullanılabilir | Genellikle tanımsız |
| TTY | Vardır | Yoktur |
| Dil değişkenleri | Kullanıcı ayarlarından gelir | Eksik veya farklı olabilir |

![cron-calisiyor-ama-55](/img/cron-calisiyor-ama-55.svg)


Shell bir komutun içinde `/` görmezse çalıştırılabilir dosyayı `PATH` dizinlerinde sırayla arar. Bunu basitçe şöyle düşünebiliriz:

$$
\text{komut yolu} = \min\{d_i/komut \mid d_i \in PATH,\; çalıştırılabilir\}
$$

Örneğin terminalinizde `/usr/local/bin` mevcutken cron’un `PATH` değerinde bu dizin yoksa `node`, `python`, `docker` veya özel bir CLI bulunamayabilir. Sonuç genellikle `command not found` olur; çıktı yönlendirilmediyse hatayı görmeyebilirsiniz bile.

## Güvenilir çözüm: ortamı açıkça tanımlamak

Crontab içinde ihtiyaç duyulan shell ve `PATH` değerlerini belirtmek ilk savunma hattıdır:

```cron
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

*/10 * * * * /home/ada/scripts/rapor.sh >> /home/ada/logs/rapor.log 2>&1
```

Buradaki `2>&1`, standart hata akışını standart çıktıyla aynı log dosyasına gönderir. Böylece cron’un sessizliğini bozup gerçek hatayı yakalayabilirsiniz. Ancak `SHELL=/bin/bash` yazmak Bash’i otomatik olarak login veya interaktif shell yapmaz; `.bashrc` dosyasının okunacağı anlamına gelmez.

Script içinde kritik komutlar için mutlak yollar kullanmak daha da sağlamdır:

```bash
#!/usr/bin/env bash
set -euo pipefail

DATE=/usr/bin/date
PG_DUMP=/usr/bin/pg_dump
GZIP=/usr/bin/gzip

backup="/var/backups/app-$($DATE +%F).sql.gz"
$PG_DUMP appdb \vert  $GZIP > "$backup"
```

Bu script, hangi programların çalışacağını belirsiz `PATH` aramasına bırakmaz. `set -euo pipefail` ise başarısız komutları, tanımsız değişkenleri ve boru hattı hatalarını görünür kılar.

## Göreli yolların gizli tehlikesi

Script’in `./config.json` dosyasını okuması, cron’un doğru dizinde başladığını garanti etmez. Önce script dizinine geçmek güvenlidir:

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

/usr/bin/python3 generate_report.py --config ./config.json
```

Böylece script nereden çağrılırsa çağrılsın dosya yolları tutarlı kalır.

## Ortamı karşılaştırarak hata ayıklama

Cron’un gördüğü ortamı dosyaya yazdırabilirsiniz:

```cron
* * * * * /usr/bin/env | /usr/bin/sort > /tmp/cron-env.txt 2>&1
```

Terminalde de `env | sort > /tmp/shell-env.txt` çalıştırıp iki dosyayı `diff` ile karşılaştırın. Ayrıca `command -v python3`, `command -v node` gibi komutlarla gerçek çalıştırılabilir yolları bulun.

`.bashrc` dosyasını zorla yüklemek kısa vadede işe yarayabilir, fakat interaktif terminale özel komutlar cron altında yeni sorunlar çıkarabilir. En iyi yaklaşım; bağımlılıkları, yolları, çalışma dizinini ve loglamayı açıkça tanımlayan, kendi ortamını bilen bağımsız script’ler yazmaktır. Cron sürpriz yapmaz; yalnızca bizim terminalde fark etmeden taşıdığımız görünmez bagajı yanında getirmez.
