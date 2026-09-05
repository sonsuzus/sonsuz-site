---
layout: post
title: "Bellek Sızıntılarını Profilleme: Sunucudaki Görünmez Tüketimi Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - bellek sızıntısı
  - profiling
  - sunucu performansı
toc: true
---

Uzun süre çalışan bir sunucu uygulaması başlangıçta uslu bir ev arkadaşı gibi davranıp günler sonra bütün belleği işgal edebilir. Trafik sabitken RAM kullanımının sürekli yükselmesi, gecikmelerin artması ve sonunda sürecin işletim sistemi tarafından sonlandırılması tipik belirtilerdir. Neyse ki Linux ve popüler çalışma zamanlarının yerleşik araçları, uygulamayı hemen durdurmadan bu gizli tüketimi izlememizi sağlar.

``

## Sızıntı nedir, ne değildir?

Bellek sızıntısı, artık işe yaramayan nesnelerin veya bölgelerin hâlâ erişilebilir görünmesi nedeniyle serbest bırakılamamasıdır. Çöp toplayıcılı dillerde unutulmuş bir koleksiyon, olay dinleyicisi ya da önbellek; C ve C++ tarafında ise karşılığı verilmeyen bir `malloc` çağrısı buna yol açabilir.

Her büyüme sızıntı değildir. İşletim sistemi dosya önbelleği tutabilir, çalışma zamanı belleği tekrar kullanmak üzere kendisine ayırabilir veya uygulama gerçekten daha fazla aktif veri taşıyor olabilir. Basitçe:

$$M_{surec}=M_{aktif}+M_{bos\ fakat\ ayrilmis}+M_{yerel}+M_{esleme}$$

Bir sızıntıda uzun dönemli eğilim yaklaşık olarak $\frac{dM}{dt}>0$ kalır ve yük azaldığında anlamlı biçimde gerilemez.

| Gözlem | Muhtemel neden | Kontrol yöntemi |
|---|---|---|
| RSS sürekli artıyor | Yerel veya yönetilen bellek | `/proc`, çalışma zamanı sayaçları |
| Heap artıyor, GC düşüremiyor | Erişilebilir nesneler birikiyor | Heap dökümü karşılaştırması |
| Heap sabit, RSS artıyor | Yerel tahsis veya parçalanma | `pmap`, native profiler |
| Yük azalınca bellek düşüyor | Normal çalışma kümesi | Zaman serisi izleme |

## Önce süreci dışarıdan gözlemleyin

Linux üzerinde ilk durak `/proc` dosya sistemidir. Aşağıdaki döngü, sürecin RSS ve sanal bellek değerlerini her on saniyede kaydeder:

```bash
PID=1234
while true; do
  date
  grep -E 'VmRSS|VmSize|RssAnon|RssFile' /proc/$PID/status
  sleep 10
done
```

`VmRSS` fiziksel bellekte bulunan toplamı, `RssAnon` ise çoğunlukla heap ve anonim tahsisleri gösterir. Dosya eşlemelerinin ayrıntısı için `pmap -x 1234` kullanılabilir. Aynı komutu farklı zamanlarda çalıştırıp çıktıları karşılaştırmak, büyüyen bölgenin anonim bellek mi yoksa eşlenmiş dosya mı olduğunu ortaya çıkarır.

## Çalışma zamanına içeriden bakın

Yönetilen uygulamalarda yalnızca RSS izlemek yeterli değildir. Java için JDK ile gelen araçlar oldukça güçlüdür:

```bash
jcmd 1234 GC.heap_info
jcmd 1234 GC.class_histogram > histogram-ilk.txt
sleep 600
jcmd 1234 GC.class_histogram > histogram-son.txt
```

Histogramlar sınıf başına nesne sayısını ve kaplanan alanı gösterir. İki ölçüm arasında sürekli büyüyen `HashMap`, oturum veya mesaj sınıfları şüphelidir. Daha ayrıntılı inceleme gerektiğinde `jcmd 1234 GC.heap_dump /tmp/heap.hprof` ile heap dökümü alınabilir; ancak büyük heap’lerde kısa duraklama ve yoğun disk kullanımı yaşanabileceği unutulmamalıdır.

.NET uygulamalarında `dotnet-counters monitor --process-id 1234` ile GC heap boyutu, tahsis hızı ve koleksiyon sayıları canlı izlenebilir. `dotnet-gcdump collect -p 1234` ise nesne türlerinin dağılımını kaydeder. Python’da standart kütüphanedeki `tracemalloc` iki anlık görüntüyü karşılaştırabilir:

```python
import tracemalloc

tracemalloc.start(25)
baslangic = tracemalloc.take_snapshot()
# Sunucu bir süre normal trafik işler.
son = tracemalloc.take_snapshot()

for kayit in son.compare_to(baslangic, "lineno")[:10]:
    print(kayit)
```

Bu kod, bellek artışını kaynak dosyası ve satır numarasıyla ilişkilendirir. Böylece yalnızca “bellek yükseliyor” demek yerine hangi kod yolunun tahsis ürettiği görülebilir.

## Güvenilir profilleme stratejisi

Tek bir ölçüme güvenmeyin. Önce düşük maliyetli sayaçlarla eğilimi doğrulayın, ardından aynı yük altında en az iki histogram veya snapshot alın. Ölçümleri istek sayısına göre normalize etmek de önemlidir:

$$Sizinti\ orani=\frac{M_2-M_1}{Istek_2-Istek_1}$$

Düzeltmeden sonra aynı senaryoyu yeniden çalıştırıp bu oranın sıfıra yaklaşmasını bekleyin. Profil araçları dedektif büyüteci gibidir: Suçluyu tek başına tutuklamazlar, fakat doğru zaman karşılaştırmasıyla parmak izlerini görünür hâle getirirler.
