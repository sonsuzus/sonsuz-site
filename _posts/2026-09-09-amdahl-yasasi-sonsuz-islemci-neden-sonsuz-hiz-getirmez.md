---
layout: post
title: "Amdahl Yasası: Sonsuz İşlemci Neden Sonsuz Hız Getirmez?"
math: true
categories: 
  - Bilgi
tags: 
  - amdahl yasası
  - paralel programlama
  - yüksek performanslı hesaplama
toc: true
---

Bir programı hızlandırmak için sisteme daha fazla işlemci eklemek ilk bakışta kusursuz bir plan gibi görünür. İki işlemci iki kat, bin işlemci bin kat hız sağlamalı, değil mi? Ne yazık ki gerçek sistemlerde bazı işler paralel yürütülemez. Amdahl Yasası, programın bu seri bölümünün toplam hızlanmaya nasıl kaçınılmaz bir tavan koyduğunu matematiksel olarak açıklar.
``

## Temel fikir: Her iş bölüşülemez

Bir programın toplam çalışma süresini iki parçaya ayıralım:

- **Seri bölüm:** Yalnızca tek işlemci üzerinde yürütülebilen işlemler.
- **Paralel bölüm:** Birden fazla işlemci arasında paylaştırılabilen işlemler.

Programın seri oranını $s$, paralel oranını ise $p$ ile gösterirsek:

$$s + p = 1$$

Paralel bölümün $N$ işlemciye kusursuz biçimde dağıtıldığını varsayalım. Seri bölüm aynı sürede tamamlanırken paralel bölümün süresi yaklaşık $N$ kat azalır. Buna göre Amdahl Yasası şöyle yazılır:

$$S(N) = \frac{1}{s + \frac{p}{N}}$$

Buradaki $S(N)$, programın $N$ işlemci kullanıldığında tek işlemcili çalışmaya göre kaç kat hızlandığını belirtir.

Örneğin bir programın yüzde 90'ı paralel, yüzde 10'u seri olsun. On işlemci kullanıldığında:

$$S(10) = \frac{1}{0.10 + \frac{0.90}{10}} \approx 5.26$$

Yani on işlemci, on kat değil yalnızca yaklaşık **5,26 kat** hızlanma sağlar. İşlemcilerden bazıları zaman zaman seri bölümün bitmesini bekler; pahalı donanımın küçük bir kahve molası verdiğini düşünebiliriz.

## Sonsuz işlemcide ne olur?

İşlemci sayısını sonsuza yaklaştırdığımızda $p/N$ sıfıra yaklaşır:

$$S_{max} = \lim_{N \to \infty} S(N) = \frac{1}{s}$$

Programın yüzde 10'u seri ise teorik maksimum hızlanma yalnızca $1/0.10 = 10$ kattır. Milyonlarca işlemci eklemek bile bu sınırı aşamaz.

| Seri oran | Paralel oran | Teorik maksimum hızlanma |
|---:|---:|---:|
| %50 | %50 | 2 kat |
| %20 | %80 | 5 kat |
| %10 | %90 | 10 kat |
| %5 | %95 | 20 kat |
| %1 | %99 | 100 kat |

Tablo önemli bir gerçeği gösterir: Büyük performans kazanımları için yalnızca işlemci sayısını artırmak değil, seri kısmı küçültmek gerekir.

## Python ile hızlanmayı hesaplamak

Aşağıdaki kod, farklı işlemci sayılarında teorik hızlanmayı hesaplar:

```python
def amdahl_speedup(serial_ratio, processor_count):
    parallel_ratio = 1 - serial_ratio
    return 1 / (
        serial_ratio + parallel_ratio / processor_count
    )

serial_ratio = 0.10

for processors in [1, 2, 4, 8, 16, 64, 1024]:
    speedup = amdahl_speedup(serial_ratio, processors)
    print(f"{processors:4} işlemci: {speedup:.2f} kat")
```

Fonksiyon önce paralel oranı bulur, ardından Amdahl formülünü uygular. İşlemci sayısı büyüdükçe sonuç 10 kata yaklaşır; ancak hiçbir zaman onu geçmez.

## Teori ile gerçek sistem arasındaki fark

Amdahl Yasası ideal paralelleştirme varsayar. Gerçek uygulamalarda işlemciler arasında veri aktarımı, görev oluşturma, senkronizasyon, kilit bekleme ve bellek erişimi gibi ek maliyetler vardır.

| Teorik varsayım | Gerçek dünyadaki durum |
|---|---|
| İşler eşit bölünür | Görev süreleri farklı olabilir |
| İletişim ücretsizdir | Veri aktarımı zaman alır |
| İşlemciler sürekli çalışır | Senkronizasyon beklemeleri oluşur |
| Bellek sınırsızdır | Bant genişliği darboğaz olabilir |

Bu nedenle ölçülen hızlanma çoğunlukla Amdahl Yasası'nın tahmininden daha düşüktür. Yasa bir performans garantisi değil, ideal koşullardaki üst sınırdır.

## Performans mühendisliği açısından ders

Daha fazla çekirdek satın almadan önce profil çıkarma araçlarıyla seri darboğazlar belirlenmelidir. Algoritmayı değiştirmek, kritik bölümleri küçültmek, kilit kullanımını azaltmak veya veri bağımlılıklarını yeniden düzenlemek donanım eklemekten daha etkili olabilir.

Kısacası Amdahl Yasası, yüksek performanslı hesaplamanın nazik ama acımasız uyarısıdır: Bir programın küçük seri bölümü bile devasa bir paralel sistemin hızını belirleyebilir. Sonsuz işlemciniz olsa dahi algoritmanızın tek başına yürümekte ısrar eden kısmını ikna etmeden sonsuz performansa ulaşamazsınız.
