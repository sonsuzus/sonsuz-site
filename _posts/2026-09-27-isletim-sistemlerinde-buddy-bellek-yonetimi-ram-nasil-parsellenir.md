---
layout: post
title: "İşletim Sistemlerinde Buddy Bellek Yönetimi: RAM Nasıl Parsellenir?"
math: true
categories: 
  - Bilgi
tags: 
  - işletim sistemleri
  - bellek yönetimi
  - buddy allocator
  - ram
  - çekirdek
  - algoritma
toc: true
image: /img/isletim-sistemlerinde-buddy-91.png
---

![isletim-sistemlerinde-buddy-91](/img/isletim-sistemlerinde-buddy-91.svg)


Bir işletim sistemi çekirdeği için boş RAM, gelişigüzel dağıtılabilecek dev bir tarla değildir. Sürücüler, süreçler ve çekirdek veri yapıları sürekli farklı büyüklüklerde fiziksel bellek ister. Buddy bellek yönetimi, bu talepleri hızlı karşılamak için belleği ikinin kuvvetleri büyüklüğündeki bloklara ayırır; gerektiğinde blokları ikiye böler, serbest bırakıldıklarında ise yeniden birleştirir.
``

## Buddy sisteminin temel fikri

Buddy allocator, yönetilen bellek bölgesini genellikle büyüklüğü $2^N$ olan büyük bir blok olarak kabul eder. Bir istek geldiğinde, isteği karşılayabilecek en küçük ikinin kuvveti seçilir.

Örneğin 13 KB bellek isteniyorsa uygun blok büyüklüğü:

$$
2^{\lceil \log_2 13 \rceil} = 2^4 = 16\text{ KB}
$$

Sistemde yalnızca 64 KB'lık boş bir blok bulunduğunu düşünelim. Çekirdek bu bloğu sırasıyla böler:

- 64 KB → iki adet 32 KB
- Bir 32 KB → iki adet 16 KB
- 16 KB bloklardan biri isteğe verilir
- Kullanılmayan bloklar boş listelerde tutulur

Bir bloğun bölünmesiyle oluşan eşit büyüklükteki iki parçaya **buddy**, yani eş blok denir. Bu iki bloktan biri serbest bırakıldığında diğeri de boşsa tekrar birleşebilirler.

## Siparişler ve boş listeler

Her blok büyüklüğü bir **order** ile temsil edilir. Sayfa büyüklüğü 4 KB ise order 0 bir sayfa, order 1 iki sayfa taşır:

$$
\text{blok boyutu} = 2^{order} \times \text{sayfa boyutu}
$$

| Order | Sayfa sayısı | Blok büyüklüğü |
|---:|---:|---:|
| 0 | 1 | 4 KB |
| 1 | 2 | 8 KB |
| 2 | 4 | 16 KB |
| 3 | 8 | 32 KB |
| 4 | 16 | 64 KB |

Çekirdek, her order için ayrı bir boş blok listesi tutar. İstenen order boşsa daha üst order'lardan blok aranır. Bulunan büyük blok, hedef boyuta ulaşılıncaya kadar parçalanır. Böylece tüm RAM'i taramak yerine birkaç liste üzerinde işlem yapılır.

## Eş blok nasıl bulunur?

Buddy yaklaşımının en zarif numarası adres hesabıdır. Boyutu $2^k$ olan bir bloğun başlangıç adresi biliniyorsa buddy adresi şu şekilde hesaplanabilir:

$$
\text{buddy} = \text{adres} \oplus 2^k
$$

Buradaki $\oplus$ bit düzeyinde XOR işlemidir. İlgili boyut bitini değiştirmek, bloğun eşini doğrudan bulur. Böylece pahalı aramalar yerine hızlı bir adres hesabı yeterli olur.

```c
size_t buddy_address(size_t address, unsigned int order,
                     size_t page_size) {
    size_t block_size = page_size << order;
    return address ^ block_size;
}
```

Bu örnek, sayfa boyutunu `order` kadar sola kaydırarak blok büyüklüğünü hesaplar ve XOR ile eş bloğun adresini üretir. Gerçek çekirdeklerde fiziksel sayfa numaraları, bölgeler ve ek güvenlik kontrolleri de hesaba katılır.

## Bölme ve birleştirme döngüsü

Serbest bırakma sırasında allocator aynı order'daki buddy bloğu kontrol eder. Buddy boşsa iki blok birleşir ve bir üst order'a taşınır. Ardından yeni büyük bloğun buddy'si kontrol edilir. Bu işlem birleşme mümkün olmayana kadar sürer.

```text
free(block, order):
    while order < MAX_ORDER:
        buddy = find_buddy(block, order)
        if buddy kullanımda ise:
            break
        buddy'yi boş listesinden çıkar
        block = adresi daha küçük olan blok
        order = order + 1
    block'u ilgili boş listeye ekle
```

| Özellik | Buddy sistemi | Değişken boyutlu liste |
|---|---|---|
| Tahsis hızı | Yüksek | Aramaya göre değişir |
| Birleştirme | XOR ile kolay | Komşu aramak gerekebilir |
| İç parçalanma | Orta | Genellikle daha düşük |
| Dış parçalanma | Kontrollü | Daha belirgin olabilir |

Buddy sistemi parçalanmayı tamamen yok etmez. 17 KB'lık istek 32 KB blok kullanacağından 15 KB **iç parçalanma** oluşur. Buna karşılık standart blok boyutları ve hızlı birleşme, **dış parçalanmayı** azaltır. Linux gibi sistemler bu yöntemi küçük nesneler için kullanılan slab veya SLUB allocator'larla birlikte çalıştırır. Kısacası buddy allocator, RAM'i kusursuz değil; hızlı, öngörülebilir ve çekirdek için yönetilebilir biçimde parseller.
