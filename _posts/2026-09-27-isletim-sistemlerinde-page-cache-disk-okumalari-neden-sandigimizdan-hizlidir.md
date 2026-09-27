---
layout: post
title: "İşletim Sistemlerinde Page Cache: Disk Okumaları Neden Sandığımızdan Hızlıdır?"
math: true
categories: 
  - Bilgi
tags: 
  - işletim sistemi
  - page cache
  - ram
  - disk
  - linux
  - performans
toc: true
image: /img/isletim-sistemlerinde-page-33.png
---

Bir dosyayı ilk kez açarken kısa bir bekleme yaşayıp ikinci açılışta şaşırtıcı bir hız görmüş olabilirsiniz. Dosya diskte durduğu hâlde bilgisayarınız nasıl bir anda hızlandı? Çoğu zaman cevap daha hızlı bir disk değil, işletim sisteminin boş RAM alanını akıllıca değerlendirdiği **page cache** mekanizmasıdır.

``

## Page cache nedir?

İşletim sistemi, depolama aygıtındaki dosyaları doğrudan uygulamaların yönetmesine izin vermez. Uygulama bir dosya istediğinde çekirdek, veriyi belirli büyüklükteki bellek sayfaları hâlinde okur. Okunan sayfalar yalnızca programa verilmez; aynı zamanda RAM içindeki page cache alanında tutulur.

Aynı dosya yeniden istendiğinde çekirdek önce önbelleği kontrol eder. Gerekli sayfalar RAM'deyse diske erişmeden sonucu döndürür. Buna **cache hit**, verinin bulunamayıp diskten okunmasına ise **cache miss** denir.

| Durum | Veri kaynağı | Yaklaşık gecikme | Sonuç |
|---|---|---:|---|
| Cache hit | RAM | nanosaniye–mikrosaniye | Çok hızlı okuma |
| SSD okuması | SSD | onlarca–yüzlerce mikrosaniye | Hızlı ama RAM'den yavaş |
| HDD okuması | Mekanik disk | milisaniye | Kafa hareketi nedeniyle yavaş |

![isletim-sistemlerinde-page-33](/img/isletim-sistemlerinde-page-33.svg)


Basitleştirilmiş toplam erişim süresi şöyle düşünülebilir:

$$T_{ortalama} = H \cdot T_{RAM} + (1-H) \cdot T_{disk}$$

Buradaki $H$, önbellek isabet oranıdır. $H$ değeri 1'e yaklaştıkça ortalama erişim süresi RAM hızına yaklaşır. Küçük görünen bir isabet oranı artışı bile yoğun dosya kullanan sunucularda büyük performans farkı yaratabilir.

## “Boş RAM” neden gerçekten boş değildir?

Görev yöneticisinde RAM'in büyük bölümünün kullanıldığını görmek her zaman sorun anlamına gelmez. Modern işletim sistemleri kullanılmayan belleği boş bırakmak yerine dosya önbelleği olarak değerlendirir. Çünkü kullanılmayan RAM, performans açısından kaçırılmış bir fırsattır.

Bir uygulama daha fazla belleğe ihtiyaç duyduğunda önbellekteki temiz sayfalar kolayca bırakılabilir. Bu nedenle page cache, uygulamaların belleğini “çalmaz”; ihtiyaç ortaya çıkana kadar boş kapasiteyi ödünç alır.

Linux çıktılarındaki `free`, `buff/cache` ve özellikle `available` değerleri bu yüzden birlikte değerlendirilmelidir:

```bash
# Belleğin uygulamalar ve önbellek arasında nasıl dağıldığını gösterir.
free -h

# Bir dosyayı okuyarak gerçek süreyi ölçer.
time cat buyuk-dosya.bin > /dev/null

# Aynı komut ikinci kez çalıştırıldığında veri büyük olasılıkla cache'tedir.
time cat buyuk-dosya.bin > /dev/null
```

İkinci çalıştırmanın daha hızlı olması, dosyanın değiştiği veya `cat` programının özel bir numara yaptığı anlamına gelmez. İlk komut dosya sayfalarını RAM'e taşımış, ikinci komut ise hazır bulunan sayfaları kullanmıştır. Dosya RAM kapasitesinden büyükse veya sistem yoğun bellek baskısı altındaysa fark azalabilir.

## Yazma işlemlerinde de görev alır mı?

Evet. Bir uygulama dosyaya yazdığında veri çoğu zaman önce bellekteki sayfalara aktarılır. Değiştirilmiş ve henüz diske gönderilmemiş sayfalara **dirty page** denir. Çekirdek bunları daha sonra toplu biçimde diske yazar. Böylece uygulama her küçük değişiklik için fiziksel disk işlemini beklemez.

| Sayfa türü | Anlamı | Bellekten hemen atılabilir mi? |
|---|---|---|
| Clean page | Diskteki kopyayla aynı | Evet |
| Dirty page | Henüz diske yazılmamış değişiklik içerir | Önce yazılmalıdır |

Bu yaklaşım performansı artırsa da elektrik kesintisi gibi durumlarda henüz kalıcı depolamaya ulaşmamış veriler kaybolabilir. Veritabanları bu nedenle `fsync` benzeri çağrılarla kritik verinin diske ulaştığından emin olur.

## Page cache her şeyi hızlandırır mı?

Page cache sihirli değildir. İlk okuma yine depolama aygıtının hızına bağlıdır. Çok büyük veri kümeleri önbelleğe sığmayabilir; başka uygulamalar da sık kullanılan sayfaları dışarı itebilir. Ayrıca bazı veritabanları ve özel uygulamalar, kendi önbelleklerini yönetmek için doğrudan I/O kullanabilir.

Yine de günlük kullanımda programların hızlı açılması, kaynak kodlarının çabuk derlenmesi ve aynı videonun tekrar akıcı oynatılması çoğunlukla bu görünmez yardımcı sayesinde gerçekleşir. Kısacası yüksek RAM kullanımı her zaman kötü değildir: İşletim sistemi belleği dosyalarla dolduruyorsa, RAM'iniz tembellik etmek yerine gelecekteki disk okumalarını hızlandırıyordur.
