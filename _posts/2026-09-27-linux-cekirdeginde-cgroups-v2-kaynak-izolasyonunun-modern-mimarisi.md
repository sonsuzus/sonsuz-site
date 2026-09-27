---
layout: post
title: "Linux Çekirdeğinde Cgroups v2: Kaynak İzolasyonunun Modern Mimarisi"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - cgroups
  - docker
  - konteyner
  - çekirdek
  - devops
toc: true
image: /img/linux-cekirdeginde-cgroups-17.png
---

Bir konteynere “en fazla 512 MB bellek kullan” veya “işlemcinin yalnızca yarısını tüket” dediğimizde bu kuralları Docker’ın sihirli değneği değil, Linux çekirdeğinin **control groups** mekanizması uygular. Cgroups v2, ilk sürümün yıllar içinde karmaşıklaşan yapısını tek bir hiyerarşide birleştirerek kaynak yönetimini daha tutarlı, güvenli ve öngörülebilir hâle getirir.
``
## Cgroups neyi çözer?

Cgroups, süreçleri gruplandırır ve CPU, bellek, disk G/Ç ya da süreç sayısı gibi kaynakları bu gruplar üzerinden denetler. Namespace’ler bir konteynerin *neyi görebildiğini*, cgroups ise *ne kadar tüketebildiğini* belirler. Dolayısıyla ikisi tamamlayıcıdır: namespace izolasyon perdesiyken cgroups kaynak bütçesidir.

Bir grubun CPU kullanım oranı basitçe

$$
R = \frac{Q}{P}
$$

ile düşünülebilir. Burada $Q$ izin verilen CPU süresi, $P$ ise periyottur. Örneğin `cpu.max` dosyasına `50000 100000` yazılması, grubun her 100 milisaniyede en fazla 50 milisaniye CPU kullanabilmesi, yani yaklaşık $R=0.5$ CPU kapasitesi anlamına gelir.

## v1 neden yorucuydu?

Cgroups v1’de her denetleyici bağımsız bir hiyerarşiye bağlanabiliyordu. Aynı süreç CPU ağacında bir grupta, bellek ağacında başka bir grupta bulunabiliyordu. Esneklik gibi görünen bu model; Docker, systemd ve Kubernetes gibi araçlar aynı makinede çalıştığında yönetim karmaşasına, belirsiz yetki devrine ve tutarsız kaynak davranışlarına yol açıyordu.

| Özellik | Cgroups v1 | Cgroups v2 |
|---|---|---|
| Hiyerarşi | Denetleyici başına ayrı olabilir | Tek ve birleşik |
| Süreç organizasyonu | Farklı ağaçlarda farklı üyelik | Tek cgroup üyeliği |
| Yetki devri | Karmaşık ve riskli | Kontrollü delegation |
| Bellek denetimi | Daha parçalı davranış | Tutarlı limit ve basınç modeli |
| Arayüz | Denetleyiciler arasında düzensiz | Standartlaştırılmış dosyalar |

## Birleşik hiyerarşi nasıl çalışır?

v2 çoğunlukla `/sys/fs/cgroup` altında tek bir ağaç sunar. Bir sürecin kimliği `cgroup.procs`, kullanılabilir denetleyiciler `cgroup.controllers`, alt gruplara aktarılacak denetleyiciler ise `cgroup.subtree_control` üzerinden yönetilir.

```bash
# Sistemde etkin olan v2 denetleyicilerini gösterir.
cat /sys/fs/cgroup/cgroup.controllers

# Yeni bir uygulama grubu oluşturur.
sudo mkdir /sys/fs/cgroup/demo

# Kabuğun PID'sini gruba taşır.
echo $$ | sudo tee /sys/fs/cgroup/demo/cgroup.procs
```

v2’nin önemli kurallarından biri **no internal process constraint** ilkesidir. Kaynak denetleyicileri alt gruplara dağıtan bir cgroup, normalde aynı anda doğrudan süreç barındırmaz. Başka bir deyişle dallar organizasyon, yapraklar iş yükü içindir. Bu kural, ebeveyn ve çocuk gruplar arasında kaynak hesabının bulanıklaşmasını önler.

## Bellek, CPU ve süreç sınırları

Bellek tarafında `memory.max` kesin tavanı, `memory.high` ise çekirdeğin agresif geri kazanım uygulamaya başlayacağı yumuşak eşiği ifade eder. Böylece uygulamayı anında öldürmeden önce baskı oluşturmak mümkündür. `memory.current` mevcut tüketimi gösterirken `memory.events`, OOM gibi olayları sayar.

```bash
# Kesin bellek limitini 512 MiB yapar.
echo 536870912 | sudo tee /sys/fs/cgroup/demo/memory.max

# Yaklaşık yarım CPU ve en fazla 100 süreç tanımlar.
echo '50000 100000' | sudo tee /sys/fs/cgroup/demo/cpu.max
echo 100 | sudo tee /sys/fs/cgroup/demo/pids.max
```

CPU paylaşım önceliği için v1’deki `cpu.shares` yerine daha anlaşılır bir aralığa sahip `cpu.weight` kullanılır. G/Ç denetimi de `io.max` ve `io.weight` gibi tutarlı adlarla sunulur.

## Docker açısından anlamı

Docker’daki `--memory`, `--cpus` ve `--pids-limit` seçenekleri sonuçta bu dosyalara dönüştürülür. Modern systemd sürümleri de servisleri cgroup ağacında doğal olarak düzenler. Tek hiyerarşi sayesinde orkestratör, çalışma zamanı ve init sistemi aynı kaynak ağacını paylaşabilir; “bu süreci aslında kim yönetiyor?” bilmecesi büyük ölçüde ortadan kalkar.

Cgroups v2 yalnızca temizlenmiş bir arayüz değildir. Tutarlı muhasebe, güvenli yetki devri, gelişmiş bellek baskısı ve sade hiyerarşi sayesinde konteyner izolasyonunu daha sağlam bir çekirdek sözleşmesine dönüştürür. Kısacası v1 kaynaklara ayrı ayrı kilit vuruyordu; v2 ise bütün binaya düzenli bir erişim planı çiziyor.

![linux-cekirdeginde-cgroups-17](/img/linux-cekirdeginde-cgroups-17.svg)

