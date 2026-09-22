---
layout: post
title: "MMU ve Sanal Adresleme: CPU Gerçek Belleği Nasıl Buluyor?"
math: true
categories: 
  - Bilgi
tags: 
  - mmu
  - sanal bellek
  - işletim sistemi
  - cpu
  - sayfalama
  - tlb
toc: true
image: /img/mmu-ve-sanal-85.png
---

Bir program bellekteki `0x7FFF1234` adresine eriştiğinde CPU doğrudan RAM’in o noktasına koşmaz. Çünkü programın gördüğü adres, çoğunlukla fiziksel bir konum değil, işletim sistemi tarafından oluşturulmuş sanal bir adrestir. CPU içindeki **Bellek Yönetim Birimi (MMU)** bu adresi tercüme ederek gerçek RAM konumunu bulur. Kısacası MMU, belleğin simultane tercümanıdır; üstelik yanlış çeviri yaparsa program değil, bütün sistem homurdanabilir.

``

## Neden sanal adres kullanılıyor?

Her sürecin kendisine ait bağımsız bir adres alanı varmış gibi çalışması güvenlik ve kullanım kolaylığı sağlar. İki program aynı sanal adresi kullanabilir, ancak bu adresler farklı fiziksel sayfalara çevrilir. Böylece bir uygulama başka bir uygulamanın belleğini yanlışlıkla kurcalayamaz.

| Özellik | Sanal adres | Fiziksel adres |
|---|---|---|
| Kim üretir? | CPU’daki program komutları | MMU çevirisi |
| Kime özeldir? | Sürece | Sistemdeki RAM’e |
| Doğrudan RAM konumu mu? | Hayır | Evet |
| Koruma sağlar mı? | Sayfa izinleriyle sağlar | Tek başına sağlamaz |
| Diskle ilişkilendirilebilir mi? | Evet | Genellikle hayır |

![mmu-ve-sanal-85](/img/mmu-ve-sanal-85.svg)


Sanal bellek, sabit boyutlu **sayfalara** ayrılır. Fiziksel bellek tarafındaki eş boyutlu parçalara ise **sayfa çerçevesi** denir. Yaygın bir sayfa boyutu 4 KiB’dir:

$$4\text{ KiB} = 4096 = 2^{12}\text{ bayt}$$

Bu nedenle adresin son 12 biti sayfa içindeki konumu, yani **ofseti** belirtir. Kalan bitler sanal sayfa numarasıdır:

$$VA = VPN \times 2^{12} + offset$$

MMU, sanal sayfa numarasını fiziksel çerçeve numarasına dönüştürür; ofseti ise değiştirmez. Örneğin sanal sayfa 42, fiziksel çerçeve 9 ile eşleştirilmişse sayfa içindeki 100. baytın fiziksel adresi $9 \times 4096 + 100$ olur.

## Sayfa tablosu: Adreslerin rehberi

İşletim sistemi her süreç için bir **sayfa tablosu** yönetir. Bu tabloda fiziksel çerçeve numarasının yanında erişim izinleri ve durum bitleri bulunur.

| Bit veya alan | Görevi |
|---|---|
| Present | Sayfa şu anda RAM’de mi? |
| Read/Write | Yazmaya izin var mı? |
| User/Supervisor | Kullanıcı kodu erişebilir mi? |
| Executable | İçerik komut olarak çalıştırılabilir mi? |
| Dirty | Sayfa değiştirildi mi? |

Modern 64 bit sistemlerde tablo devasa olabileceği için çok seviyeli sayfa tabloları kullanılır. Sanal adres parçalara ayrılır; her parça bir sonraki tablodaki girdiyi seçer. CPU, işletim sisteminin belirlediği kök tablodan başlayarak adeta klasörler arasında gezinir. Bu işleme **page table walk** denir.

## TLB neden gerekli?

Her bellek erişiminde birkaç tablo okumak oldukça pahalıdır. Bu yüzden MMU içinde **Translation Lookaside Buffer (TLB)** adlı küçük ve hızlı bir önbellek bulunur. Yakın zamanda kullanılan VPN–çerçeve eşleşmeleri burada saklanır.

1. CPU sanal adres üretir.
2. MMU önce TLB’ye bakar.
3. Eşleşme varsa fiziksel adres hemen oluşturulur.
4. Yoksa sayfa tabloları yürünür.
5. Sayfa RAM’de değilse **page fault** oluşur.

Page fault her zaman hata değildir. İşletim sistemi ilgili sayfayı diskten RAM’e getirebilir, tabloyu güncelleyebilir ve komutu yeniden çalıştırabilir. Ancak geçersiz veya izinsiz erişim söz konusuysa süreç `segmentation fault` ile sonlandırılabilir.

Aşağıdaki Python kodu tek seviyeli basitleştirilmiş bir çeviriyi gösterir:

```python
PAGE_SIZE = 4096
page_table = {42: 9, 43: 15}

def translate(virtual_address):
    vpn = virtual_address // PAGE_SIZE
    offset = virtual_address % PAGE_SIZE

    if vpn not in page_table:
        raise MemoryError("Page fault!")

    frame = page_table[vpn]
    return frame * PAGE_SIZE + offset

virtual = 42 * PAGE_SIZE + 100
print(translate(virtual))  # 36964
```

Gerçek MMU’lar çok seviyeli tablolar, ayrıcalık kontrolleri, büyük sayfalar ve TLB politikalarıyla çok daha karmaşıktır. Fakat temel fikir değişmez: **sanal sayfayı bul, fiziksel çerçeveyle eşleştir, ofseti koru**. CPU’nun RAM’i bulma macerası, iyi düzenlenmiş bir adres defteri sayesinde nanosaniyeler içinde tamamlanır.
