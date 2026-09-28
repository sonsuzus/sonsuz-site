---
layout: post
title: "NUMA Mimarilerinde Bellek Yerelliği: Yanlış RAM Yuvası Sistemi Nasıl Yavaşlatır?"
math: true
categories: 
  - Bilgi
tags: 
  - numa
  - bellek
  - linux
  - performans
  - sunucu
  - işlemci
toc: true
image: /img/numa-mimarilerinde-bellek-42.png
---

Çok soketli bir sunucuya RAM eklemek, ilk bakışta bütün işlemcilerin eşit hızda kullanabileceği büyük bir bellek havuzu oluşturmak gibi görünür. NUMA mimarisinde ise RAM’in hangi işlemciye yakın olduğu önemlidir. Program doğru çekirdekte çalışsa bile verisi uzak NUMA düğümündeyse, her bellek erişiminde küçük ama milyonlarca kez tekrarlandığında pahalı bir yolculuk başlar.


![numa-mimarilerinde-bellek-42](/img/numa-mimarilerinde-bellek-42.svg)

``

## NUMA tam olarak nedir?

NUMA, yani **Non-Uniform Memory Access**, bellek erişim süresinin konuma göre değiştiği mimaridir. Her işlemci soketi; belirli çekirdekler, bellek denetleyicileri ve RAM kanallarıyla birlikte bir **NUMA düğümü** oluşturur. Bir çekirdek kendi düğümündeki RAM’e doğrudan erişirken diğer sokete bağlı RAM’e işlemciler arası bağlantı üzerinden ulaşır.

Basitleştirilmiş erişim maliyeti şöyle modellenebilir:

$$
T_{ortalama} = p \cdot T_{yerel} + (1-p) \cdot T_{uzak}
$$

Burada $p$, erişimlerin yerel belleğe gitme oranıdır. Yerel gecikme 90 ns, uzak gecikme 150 ns ve yerellik oranı $p=0.7$ ise:

$$
T_{ortalama} = 0.7(90) + 0.3(150) = 108\text{ ns}
$$

Tek erişimdeki 18 nanosaniyelik fark önemsiz görünebilir. Ancak büyük veri tabanları, sanal makineler ve analitik uygulamalar saniyede milyarlarca erişim yapabilir.

| Özellik | Yerel bellek | Uzak bellek |
|---|---:|---:|
| Gecikme | Daha düşük | Daha yüksek |
| Bant genişliği | Genellikle yüksek | Bağlantıyla sınırlı |
| Trafik yolu | Bellek denetleyicisine doğrudan | Soketler arası bağlantı üzerinden |
| Tercih | İş parçacığına yakın veri | Mecbur kalındığında |

## Yanlış RAM yuvası neden sorun çıkarır?

RAM modülleri soketlere dengesiz dağıtılırsa bir işlemci yeterli yerel belleğe sahipken diğeri sürekli uzak belleğe başvurabilir. Ayrıca bellek kanallarının eksik doldurulması bant genişliğini azaltır. Bu nedenle sunucu üreticisinin yuva sıralaması yalnızca estetik bir öneri değildir; kanalların ve NUMA düğümlerinin dengeli çalışmasını sağlar.

İşletim sistemleri çoğunlukla **first-touch** politikası kullanır: Bir bellek sayfası, ona ilk yazan iş parçacığının NUMA düğümünde fiziksel olarak ayrılır. Ana iş parçacığı bütün diziyi başlatıp ardından işi diğer soketlere dağıtırsa veri tek düğümde toplanabilir. Çalışanlar da hesap yapmak yerine adeta soketler arası kargo bekler.

## Linux üzerinde topolojiyi incelemek

Aşağıdaki komutlar düğümleri, işlemcileri ve erişim istatistiklerini gösterir:

```bash
lscpu | grep -i numa
numactl --hardware
numastat -p <PID>
```

`numactl --hardware`, hangi CPU’ların ve ne kadar belleğin her düğüme ait olduğunu açıklar. `numastat` çıktısındaki `numa_miss` ve `numa_foreign` değerlerinin yükselmesi, uzak yerleşim şüphesini güçlendirir.

Bir uygulamayı belirli çekirdek ve bellek düğümüne bağlamak mümkündür:

```bash
numactl --cpunodebind=0 --membind=0 ./uygulama
```

Bu komut hem işlemci çalışmasını hem bellek tahsisini düğüm 0 ile sınırlar. Kesin bağlama kapasiteyi daraltabileceğinden üretimde ölçüm yapmadan uygulanmamalıdır. Daha esnek bir seçenek olan `--interleave=all`, sayfaları düğümler arasında dönüşümlü dağıtarak büyük ve paralel iş yüklerinde bant genişliğini dengeleyebilir.

| Strateji | Avantaj | Risk |
|---|---|---|
| Yerel bağlama | Düşük gecikme | Düğüm belleği tükenebilir |
| Interleave | Dengeli bant genişliği | Her erişim yerel olmaz |
| Otomatik NUMA dengeleme | Kolay yönetim | Sayfa taşıma maliyeti oluşur |
| Uygulama kontrollü tahsis | En iyi yerellik potansiyeli | Kod karmaşıklığı artar |

## Programlar nasıl NUMA dostu olur?

Paralel uygulamalar veriyi tek iş parçacığında hazırlamak yerine her parçayı onu kullanacak iş parçacığında başlatmalıdır. İş parçacığı sabitleme, çekirdekler arasında gereksiz göçü önler. Veri bölümlendirme de iş ile belleği aynı düğümde tutar. Java JVM, veri tabanları ve konteyner platformlarında CPU sınırı koyarken bellek politikasını unutmak, optimizasyonun yarısını çöpe atmak demektir.

Sonuç olarak NUMA performansı yalnızca daha hızlı RAM satın alma meselesi değildir. DIMM’leri üretici şemasına göre dengeli yerleştirmek, topolojiyi gözlemlemek, first-touch davranışını anlamak ve gerçek iş yüküyle ölçüm yapmak gerekir. NUMA’da temel kural basittir: Hesabı veriye götürmek, veriyi soketler arasında sürekli gezdirmekten ucuzdur.
