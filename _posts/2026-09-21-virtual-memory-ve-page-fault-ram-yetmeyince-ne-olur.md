---
layout: post
title: "Virtual Memory ve Page Fault: RAM Yetmeyince Ne Olur?"
math: true
categories: 
  - Bilgi
tags: 
  - virtual memory
  - page fault
  - ram
  - işletim sistemi
  - bellek yönetimi
  - paging
toc: true
image: /img/virtual-memory-ve-80.png
---

![virtual-memory-ve-80](/img/virtual-memory-ve-80.svg)


Bir programın onlarca gigabayt bellek kullanıyormuş gibi davranabilmesi, bilgisayarınızda gerçekten o kadar RAM bulunduğu anlamına gelmez. İşletim sistemi, **virtual memory (sanal bellek)** adı verilen bir illüzyon kurar: Her süreç kendisine ait, düzenli ve geniş bir adres alanı görür. RAM yetersiz kaldığında ise disk, sayfa tabloları ve page fault mekanizması sahneye çıkar.

``

## Sanal bellek neden var?

Programların kullandığı adresler doğrudan fiziksel RAM adresleri değildir. İşlemci tarafından üretilen **sanal adres**, Memory Management Unit yani **MMU** aracılığıyla fiziksel adrese çevrilir. Bellek, genellikle 4 KiB gibi sabit boyutlu **page (sayfa)** parçalarına; RAM ise aynı boyuttaki **frame (çerçeve)** parçalarına ayrılır.

Bir sanal adresi basitleştirerek şöyle düşünebiliriz:

$$VA = p \times S + d$$

Burada $p$ sayfa numarası, $S$ sayfa boyutu, $d$ ise sayfa içindeki ofsettir. Sayfa tablosu, $p$ numaralı sanal sayfanın hangi fiziksel frame içinde bulunduğunu söyler.

| Kavram | Görevi | Nerede bulunur? |
|---|---|---|
| Page | Sanal belleğin sabit boyutlu parçası | Sanal adres alanı |
| Frame | Bir page'i taşıyan fiziksel alan | RAM |
| Page table | Page-frame eşleşmesini tutar | RAM ve işlemci önbellekleri |
| Swap | RAM'den çıkarılan verileri geçici saklar | SSD veya disk |
| TLB | Son adres çevirilerini hızlandırır | İşlemci |

## Page fault tam olarak nedir?

İşlemci bir sanal adrese erişmek istediğinde ilgili page RAM'de değilse **page fault** oluşur. Adı korkutucu olsa da bu her zaman hata veya çökme demek değildir. Daha çok işletim sistemine gönderilen “Aradığım sayfa burada yok!” bildirimidir.

İşletim sistemi sırasıyla şunları yapar:

1. Erişimin geçerli olup olmadığını kontrol eder. Adres sürece ait değilse segmentation fault oluşabilir.
2. Sayfa disk üzerindeki çalıştırılabilir dosyadan, eşlenmiş dosyadan veya swap alanından bulunur.
3. RAM'de boş frame varsa sayfa buraya yüklenir.
4. Boş frame yoksa bir **kurban sayfa** seçilir. Değiştirilmişse önce diske yazılır.
5. Sayfa tablosu ve gerekirse TLB güncellenir.
6. Kesilen komut yeniden çalıştırılır.

Bu süreç programa çoğunlukla görünmez; fakat disk erişimi RAM erişiminden binlerce kat yavaş olduğu için performansa görünür bir tokat atabilir.

## Minor ve major page fault farkı

| Tür | Disk erişimi | Tipik durum | Maliyet |
|---|---:|---|---:|
| Minor page fault | Gerekmez | Sayfa zaten bellektedir fakat eşleme eksiktir | Düşük |
| Major page fault | Gerekir | Sayfa diskten veya swap'ten okunur | Yüksek |
| Invalid access | Çözülemez | Yetkisiz ya da geçersiz adres | Program sonlandırılabilir |

Ortalama erişim süresi yaklaşık olarak şöyle modellenebilir:

$$EAT = (1-p) \times M + p \times F$$

Burada $p$ page fault olasılığı, $M$ normal bellek erişim süresi, $F$ ise fault çözme maliyetidir. $F$ çok büyük olduğundan küçücük bir $p$ artışı bile sistemi belirgin biçimde yavaşlatabilir.

## Sayfa değiştirme algoritmaları

İşletim sistemi hangi sayfayı RAM'den çıkaracağına karar vermelidir. FIFO en eski sayfayı seçer; LRU ise en uzun süredir kullanılmayanı hedefler. Gerçek sistemler çoğunlukla LRU'nun yaklaşık ve daha ekonomik varyasyonlarını kullanır.

Aşağıdaki Python kodu, FIFO yaklaşımını küçük bir RAM modeli üzerinde canlandırır:

```python
from collections import deque

requests = [1, 2, 3, 1, 4, 2, 5]
frames = deque(maxlen=3)
faults = 0

for page in requests:
    if page not in frames:
        faults += 1
        if len(frames) == frames.maxlen:
            frames.popleft()  # En eski sayfayı çıkarır
        frames.append(page)   # İstenen sayfayı RAM'e alır
    print(f"sayfa={page}, ram={list(frames)}")

print(f"page fault sayısı: {faults}")
```

## RAM gerçekten yetmezse

Çalışan süreçlerin aktif sayfaları RAM'e sığmadığında sistem sürekli sayfa çıkarıp geri yüklemeye başlayabilir. **Thrashing** denilen bu durumda işlemci iş yapmaktan çok page fault bekler; disk etkinliği yükselirken sistem adeta ağır çekime geçer.

Çözüm yalnızca swap alanını büyütmek değildir. Gereksiz süreçleri kapatmak, uygulamanın bellek sızıntılarını gidermek, verileri parçalar hâlinde işlemek ve gerektiğinde RAM artırmak daha etkilidir. Sanal bellek kapasiteyi sihirli biçimde çoğaltmaz; sınırlı RAM'i güvenli, düzenli ve mümkün olduğunca verimli kullanır.
