---
layout: post
title: "PREEMPT_RT ile Linux Gecikmesini Mikrosaniyelere İndirmek"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - preempt_rt
  - gerçek-zamanlı-sistemler
  - çekirdek
  - robotik
  - gömülü-sistemler
toc: true
image: /img/preempt_rt-ile-linux-88.png
---

Bir robot koluna “şimdi dur” dediğinizde komutun çekirdekte kahve molasına çıkmasını istemezsiniz. Standart Linux yüksek işlem hacmi ve adil kaynak paylaşımı için tasarlanırken endüstriyel kontrol sistemleri belirli bir işin öngörülebilir sürede tamamlanmasını ister. PREEMPT_RT, Linux çekirdeğinin uzun süre kesilemeyen bölgelerini azaltarak gecikmeyi yalnızca düşük değil, daha önemlisi **tahmin edilebilir** hâle getirir.

``

## Gerçek zamanlı olmak ne demektir?

Gerçek zamanlı sistem “çok hızlı bilgisayar” anlamına gelmez. Temel ölçüt, bir olay ile ona verilen tepki arasındaki en kötü sürenin belirlenen son tarihi aşmamasıdır. Basitleştirilmiş tepki süresi şöyle yazılabilir:

$$T_{tepki}=T_{kesme}+T_{zamanlama}+T_{çalışma}$$

Bir kontrol döngüsünün son tarihi $D$ ise güvenli çalışma koşulu şudur:

$$T_{tepki}^{max} \leq D$$

Ortalama gecikmenin $8\,\mu s$ olması etkileyici görünebilir; ancak sistem ara sıra $5\,ms$ bekliyorsa 1 kHz hızındaki robot kontrol döngüsü kaçırılabilir. Bu nedenle RT dünyasında ortalamadan çok **en kötü durum gecikmesi** önemlidir.

| Özellik | Standart Linux | PREEMPT_RT |
|---|---|---|
| Öncelik | İş hacmi ve adalet | Belirlenebilir tepki |
| Çekirdek öncelenmesi | Sınırlı | Çok daha kapsamlı |
| Kesme işleme | Çoğunlukla sert IRQ bağlamı | Büyük ölçüde iş parçacığı |
| Kilit davranışı | Beklerken dönebilir | Uyuyabilir, öncelik aktarabilir |
| Gecikme dağılımı | Sıçramalara açık | Daha dar ve öngörülebilir |

![preempt_rt-ile-linux-88](/img/preempt_rt-ile-linux-88.svg)


## Yama çekirdeğin içinde neyi değiştirir?

PREEMPT_RT’nin sihri tek bir zamanlayıcı ayarından gelmez. İlk önemli mekanizma, donanım kesmelerinin çoğunu **threaded IRQ** hâline getirmesidir. Böylece kesme işleyicileri zamanlayıcının yönettiği çekirdek iş parçacıkları olarak çalışır; kritik kontrol görevi, daha düşük öncelikli bir kesme iş parçacığını önleyebilir. Saat gibi bazı temel kesmeler yine sert IRQ bağlamında kalabilir.

İkinci değişiklik kilitlerdedir. Standart çekirdekteki birçok `spinlock_t`, RT yapılandırmasında uyuyabilen ve öncelik kalıtımı sağlayan `rtmutex` temelli kilitlere dönüşür. Düşük öncelikli görev bir kilidi tutarken yüksek öncelikli görev onu beklerse **öncelik terslenmesi** oluşur. Öncelik kalıtımı, kilit sahibini geçici olarak yüksek önceliğe taşıyarak bekleme süresini sınırlar.

Üçüncü unsur, kesilemeyen kritik bölgelerin küçültülmesidir. PREEMPT_RT çekirdek kodunun daha fazla noktasında zamanlayıcının devreye girmesine izin verir. Ancak bu bedava değildir: bağlam değiştirme ve kilit yönetimi ek maliyet oluşturabilir. Amaç en yüksek toplam performans değil, gecikme kuyruğundaki korkutucu sürprizleri temizlemektir.

## Yapılandırma ve görev önceliği

Uyumlu bir çekirdekte genellikle `CONFIG_PREEMPT_RT` etkinleştirilir. Gerçek zamanlı görevler `SCHED_FIFO` veya `SCHED_RR` politikasıyla çalıştırılabilir:

```bash
# Programı FIFO politikası ve 80 önceliğiyle başlatır
sudo chrt --fifo 80 ./robot-controller

# Kesme iş parçacıklarını incelemeye yardımcı olur
ps -eLo pid,cls,rtprio,comm | grep irq
```

`SCHED_FIFO` görevi gönüllü olarak bekleyene, işi bitene veya daha yüksek öncelikli görev gelene kadar çalışabilir. Hatalı bir sonsuz döngü sistemi kullanılmaz hâle getirebileceğinden CPU izolasyonu, watchdog ve güvenli öncelik planı şarttır.

## Gecikmeyi ölçmek

RT başarısı “sistem hızlı hissettiriyor” testiyle ölçülmez. `cyclictest`, periyodik uyanmaları zamanlayıp hedeflenen ve gerçek uyanma zamanı arasındaki farkı raporlar:

```bash
# Belleği kilitler, 1 ms aralıkla ölçer ve öncelik 90 kullanır
sudo cyclictest --mlockall --priority=90 --interval=1000 \
  --distance=0 --threads=1 --duration=10m
```

Test; ağ, disk, USB ve grafik yükü altında tekrarlanmalıdır. BIOS güç tasarrufu, CPU frekans değişimi, kötü sürücüler ve paylaşılan IRQ’lar sonuçları bozabilir. `mlockall()` ile belleğin kilitlenmesi de çalışma sırasında sayfa hatalarından doğan gecikmeleri azaltır.

PREEMPT_RT günümüzde ana akım Linux’a büyük ölçüde entegre olsa da tek başına deterministik fabrika garantisi değildir. Uygun donanım, RT uyumlu sürücüler, çekirdek ayarları, yük testleri ve ölçülmüş bir en kötü durum sınırı birlikte gerekir. Doğru mühendislikle Linux, masaüstü pengueninden mikrosaniyeleri ciddiye alan bir robot ustabaşına dönüşebilir.
