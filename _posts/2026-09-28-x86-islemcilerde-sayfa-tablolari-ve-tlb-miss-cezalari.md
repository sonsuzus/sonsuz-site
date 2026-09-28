---
layout: post
title: "x86 İşlemcilerde Sayfa Tabloları ve TLB Miss Cezaları"
math: true
categories: 
  - Bilgi
tags: 
  - x86
  - sanal bellek
  - sayfa tabloları
  - tlb
  - işletim sistemleri
  - bellek yönetimi
toc: true
image: /img/x86-islemcilerde-sayfa-96.png
---

![x86-islemcilerde-sayfa-96](/img/x86-islemcilerde-sayfa-96.svg)


Bir program `0x7fff...` gibi bir adres kullandığında RAM üzerinde doğrudan o noktaya gitmez. Gördüğü adres sanaldır; fiziksel bellekteki karşılığını işlemcinin Bellek Yönetim Birimi, yani MMU bulur. İşletim sistemi sayfa tablolarını kurar, donanım bu tabloları yürür ve TLB sık kullanılan sonuçları saklar. Bu ekip çalışması hızlıysa her şey yolundadır; TLB ıskaladığında ise işlemci küçük ama pahalı bir hazine avına çıkar.
``

## Sayfalara bölünmüş iki dünya

x86-64 sistemlerde sanal ve fiziksel bellek sabit boyutlu sayfalara ayrılır. En yaygın sayfa boyutu 4 KiB'dir. Sanal adresin alt 12 biti sayfa içindeki konumu belirtir, çünkü:

$$4\ \text{KiB} = 4096 = 2^{12}$$

Geri kalan bitler sanal sayfa numarasını oluşturur. Çeviri sonucunda fiziksel çerçeve numarası bulunur ve ofset değiştirilmeden sona eklenir:

$$\text{Fiziksel Adres} = \text{Çerçeve Numarası} \times 4096 + \text{Ofset}$$

Her sanal sayfa için devasa, düz bir tablo tutmak çok fazla bellek harcardı. Bu nedenle x86-64, tabloları ağaç benzeri katmanlara böler. Yaygın dört seviyeli düzende adres; PML4, PDPT, PD ve PT indisleriyle yürünür. Her indis 9 bittir ve 512 girdiden birini seçer.

| Bölüm | Bit sayısı | Görevi |
|---|---:|---|
| PML4 indisi | 9 | En üst tabloyu seçer |
| PDPT indisi | 9 | Alt dizini seçer |
| PD indisi | 9 | Sayfa dizinini seçer |
| PT indisi | 9 | Son sayfa girdisini seçer |
| Ofset | 12 | Sayfa içindeki baytı seçer |

Beş seviyeli sayfalama etkinse ağacın tepesine PML5 eklenir ve kullanılabilir sanal adres alanı büyür.

## Sayfa yürüyüşü nasıl gerçekleşir?

`CR3` yazmacı, geçerli adres uzayının üst seviye tablosunun fiziksel adresini taşır. İşlemci her seviyedeki girdiyi okuyarak sonraki tablonun adresine ulaşır. Son PTE girdisi fiziksel çerçeveyi ve erişim kurallarını içerir.

```text
virtual_address -> PML4 -> PDPT -> PD -> PT -> physical_frame
```

Bu şema, dört seviyeli bir donanımsal sayfa yürüyüşünü özetler. Girdilerde `Present`, `Read/Write`, `User/Supervisor`, `Accessed`, `Dirty` ve `NX` gibi bayraklar bulunur. Örneğin `NX`, ilgili sayfadan komut çalıştırılmasını engelleyerek veri bölgelerini saldırılara karşı güçlendirir.

Burada önemli ayrım şudur: Çekirdek her bellek erişiminde çeviriyi yazılımla yapmaz. Çekirdek tabloları oluşturur ve izinleri yönetir; normal çeviriyi MMU gerçekleştirir.

## TLB neden bu kadar önemli?

Translation Lookaside Buffer, yakın zamanda kullanılan sanal sayfa-fiziksel çerçeve eşleşmelerini saklayan küçük ve hızlı bir önbellektir.

| Durum | Gerçekleşen işlem | Yaklaşık sonuç |
|---|---|---|
| TLB hit | Çeviri önbellekten alınır | Çok düşük gecikme |
| TLB miss | Sayfa tabloları yürünür | Birden fazla bellek erişimi |
| Page fault | Geçerli eşleme yoktur | Çekirdek devreye girer; çok pahalıdır |

TLB miss, page fault değildir. Sayfa RAM'de ve geçerli olabilir; yalnızca çevirisi TLB'de bulunmamıştır. Dört seviyeli yürüyüş teorik olarak dört tablo okuması gerektirir. Bu okumalar önbelleklerde değilse ceza yüzlerce çevrime yaklaşabilir. İşlemciler page-walk cache gibi ek önbelleklerle ara seviyeleri saklayarak bu maliyeti azaltır.

## Performansı iyileştiren yöntemler

2 MiB veya 1 GiB büyük sayfalar, tek TLB girdisinin daha geniş alanı kapsamasını sağlar. Böylece TLB erişim kapsamı artar:

$$\text{TLB Reach} = \text{Girdi Sayısı} \times \text{Sayfa Boyutu}$$

Ancak büyük sayfalar iç parçalanmayı artırabilir. Ayrıca bağlam değişimlerinde TLB girdilerini tamamen temizlemek pahalıdır. PCID özelliği, farklı süreçlere ait girdileri etiketleyerek gereksiz temizlemeleri azaltır. Çekirdek belirli bir eşlemeyi değiştirdiğinde ise hedefli geçersizleştirme kullanabilir:

```asm
invlpg [rax]   ; RAX'ın işaret ettiği sanal sayfanın TLB girdisini geçersizleştirir
```

Özetle sayfa tabloları esneklik ve koruma, TLB ise hız sağlar. Biri şehrin ayrıntılı haritasıysa diğeri sık gidilen adreslerin cep notudur; not kaybolduğunda haritaya dönmek mümkündür, fakat işlemci çevrimleri bunun faturasını mutlaka keser.
