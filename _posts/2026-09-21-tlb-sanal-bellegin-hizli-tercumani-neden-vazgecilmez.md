---
layout: post
title: "TLB: Sanal Belleğin Hızlı Tercümanı Neden Vazgeçilmez?"
math: true
categories: 
  - Bilgi
tags: 
  - tlb
  - sanal bellek
  - işletim sistemleri
  - bellek yönetimi
  - işlemci mimarisi
  - performans
toc: true
image: /img/tlb-sanal-bellegin-66.png
---

Bir program bellekteki bir değişkene eriştiğinde işlemci çoğunlukla fiziksel adresi doğrudan kullanmaz. Önce sanal adresin fiziksel bellekte nereye karşılık geldiğini bulması gerekir. Bu çeviri her erişimde baştan yapılsaydı, ışık hızında çalışan işlemcimiz adres defterini karıştıran dalgın bir postacıya dönüşürdü. **Translation Lookaside Buffer**, yani TLB, yakın zamanda kullanılan adres çevirilerini saklayarak bu sorunu çözen küçük fakat kritik bir önbellektir.

``

## Sanal adres neden çevrilir?

İşletim sistemi her sürece kendisine aitmiş gibi görünen bir sanal adres alanı verir. Böylece süreçler birbirlerinin belleğine kolayca erişemez, fiziksel RAM daha esnek yönetilir ve kullanılmayan sayfalar diske taşınabilir.

Bir sanal adres genel olarak iki parçaya ayrılır:

$$SanalAdres = SanalSayfaNumarası + Ofset$$

Sanal sayfa numarası, **sayfa tablosu** aracılığıyla fiziksel çerçeve numarasına çevrilir. Ofset ise sayfa içindeki konumu gösterdiği için değişmeden kalır. Örneğin 4 KiB boyutlu sayfalarda son 12 bit ofsettir; çünkü $4\,KiB = 2^{12}$ bayttır.

| Bileşen | Görevi | Çeviri sırasında değişir mi? |
|---|---|---:|
| Sanal sayfa numarası | Sayfa tablosunda aranacak kimlik | Evet |
| Fiziksel çerçeve numarası | RAM’deki gerçek bölgeyi belirtir | Çeviri sonucudur |
| Ofset | Sayfa içindeki baytı seçer | Hayır |

## Sayfa tablosu neden tek başına yetmez?

Modern sistemlerde sayfa tabloları genellikle çok seviyelidir. Örneğin dört seviyeli bir tabloda tek bir sanal adresi çevirmek için dört ayrı tablo girdisinin okunması gerekebilir. Ardından asıl veriye erişilir. Yani tek bir yükleme komutu, perde arkasında beş bellek erişimine dönüşebilir.

TLB, sanal sayfa numarası ile fiziksel çerçeve numarası arasındaki son kullanılan eşleşmeleri işlemciye çok yakın bir yerde tutar. Aranan kayıt bulunursa buna **TLB hit**, bulunamazsa **TLB miss** denir.

| Durum | Yapılan işlem | Yaklaşık maliyet |
|---|---|---:|
| TLB hit | Çeviri doğrudan TLB’den alınır | Birkaç çevrim |
| TLB miss | Sayfa tablosu yürüyüşü yapılır | Onlarca veya yüzlerce çevrim |
| Page fault | Sayfa RAM’de değildir; işletim sistemi devreye girer | Çok daha yüksek |

Ortalama çeviri maliyeti basitleştirilmiş biçimde şöyle düşünülebilir:

$$EAT = h \times T_{hit} + (1-h) \times T_{miss}$$

Buradaki $h$, TLB isabet oranıdır. İsabet oranı yüzde 99 olsa bile kalan yüzde 1, özellikle yoğun bellek kullanan programlarda hissedilebilir. Bu nedenle TLB kapasitesi, gecikmesi ve değiştirme politikası işlemci tasarımında önemlidir.

## İşlemci erişimi nasıl gerçekleştirir?

Aşağıdaki sözde kod, çeviri sürecinin temel mantığını gösterir:

```text
function bellege_erisim(sanal_adres):
    sayfa, ofset = adresi_ayir(sanal_adres)

    if TLB.sayfayi_iceriyor(sayfa):
        cerceve = TLB.getir(sayfa)
    else:
        cerceve = sayfa_tablosunda_ara(sayfa)

        if cerceve RAM_de_degilse:
            page_fault_isle(sayfa)
            cerceve = sayfa_tablosunda_ara(sayfa)

        TLB.ekle(sayfa, cerceve)

    return fiziksel_bellek[cerceve + ofset]
```

Kod önce sanal adresi sayfa ve ofset parçalarına ayırır. TLB kaydı varsa pahalı tablo yürüyüşünü atlar. Kayıt yoksa sayfa tablosuna başvurur, sonucu TLB’ye ekler ve sonraki erişimleri hızlandırır.

## Yerellik TLB’nin gizli yakıtıdır

TLB’nin işe yaramasının temelinde **yerellik ilkesi** bulunur. Programlar yakın zamanda kullandıkları verilere tekrar erişme ve birbirine yakın adresleri kullanma eğilimindedir. Bir döngünün aynı dizi üzerinde ilerlemesi, tek bir TLB girdisinin binlerce baytlık sayfayı kapsamasını sağlar.

Buna karşılık çok büyük ve dağınık veri yapılarında TLB girdileri sık sık birbirini dışarı atabilir. Bu durum **TLB thrashing** olarak anılır. Daha büyük sayfalar kullanmak daha geniş bir alanı tek girdide kapsayabilir; ancak bellek israfı ve yönetim maliyeti oluşturabilir.

Kısacası TLB, sanal belleği mümkün kılan sayfa tabloları ile işlemcinin hız beklentisi arasındaki köprüdür. Küçük görünür, fakat o olmasaydı hemen her bellek erişimi pahalı bir adres çevirisi turuna çıkardı.

![tlb-sanal-bellegin-66](/img/tlb-sanal-bellegin-66.svg)

