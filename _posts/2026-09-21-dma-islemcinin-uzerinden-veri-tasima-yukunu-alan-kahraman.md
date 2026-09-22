---
layout: post
title: "DMA: İşlemcinin Üzerinden Veri Taşıma Yükünü Alan Kahraman"
math: true
categories: 
  - Bilgi
tags: 
  - dma
  - işlemci
  - bellek
  - donanım
  - gömülü sistemler
  - veri aktarımı
toc: true
image: /img/dma-islemcinin-uzerinden-35.png
---

Bir diskten belleğe megabaytlarca veri aktarırken işlemcinin her baytı tek tek taşıdığını düşünün. Bu, kargo şirketinin yöneticisinin kamyonu bırakıp bütün kutuları kendisinin taşımasına benzerdi. **Direct Memory Access (DMA)**, veri aktarımını özel bir denetleyiciye devrederek işlemciyi asıl işi olan komut yürütme için serbest bırakır. Ancak işlemci tamamen devre dışı kalmaz; aktarımı başlatır, sonucunu takip eder ve gerektiğinde hatalarla ilgilenir.

![dma-islemcinin-uzerinden-35](/img/dma-islemcinin-uzerinden-35.svg)

``

## DMA neden gereklidir?

DMA bulunmayan basit bir sistemde işlemci, çevre biriminden bir değer okur ve bunu belleğe yazar. Binlerce veri için aynı işlemler tekrarlandığından çok sayıda komut döngüsü harcanır. **Programmed I/O** adı verilen bu yaklaşım küçük aktarımlarda yeterli olsa da disk, ağ kartı, ses birimi ve kamera gibi yüksek hızlı aygıtlarda darboğaz oluşturur.

DMA kullanıldığında işlemci denetleyiciye temel olarak şu bilgileri verir:

1. Verinin alınacağı kaynak adresi,
2. Yazılacağı hedef adresi,
3. Aktarılacak veri miktarı,
4. Yön, veri genişliği ve çalışma modu.

DMA denetleyicisi aktarımı gerçekleştirir ve tamamlandığında genellikle bir **kesme** üretir. Böylece işlemci sürekli olarak “Bitti mi?” diye sormak yerine başka işler yapabilir.

| Özellik | Programmed I/O | DMA |
|---|---|---|
| Veriyi taşıyan | İşlemci | DMA denetleyicisi |
| İşlemci yükü | Yüksek | Düşük |
| Küçük veri maliyeti | Düşük | Kurulum nedeniyle daha yüksek |
| Büyük blok performansı | Zayıf | Güçlü |
| Tamamlanma bildirimi | Yoklama veya kesme | Genellikle kesme |

## Performansın teorik tarafı

Bir veri bloğunun işlemci tarafından taşınma süresini yaklaşık olarak

$$T_{CPU}=N\times t_{kelime}$$

şeklinde düşünebiliriz. Burada $N$ taşınacak kelime sayısı, $t_{kelime}$ ise okuma-yazma ve döngü komutlarının toplam süresidir. DMA tarafında yaklaşık maliyet şöyledir:

$$T_{DMA}=T_{kurulum}+T_{aktarım}+T_{kesme}$$

Küçük bir blokta $T_{kurulum}$ kazancı gölgeleyebilir. Veri büyüdükçe kurulum maliyeti toplam süre içinde önemsizleşir. DMA’nın asıl avantajı aktarımın her zaman daha kısa sürmesi değil, işlemcinin bu sırada başka komutları yürütebilmesidir.

DMA da belleğe erişmek için sistem veri yolunu kullanır. Bu nedenle işlemciyle kaynak paylaşımı gerekir. **Burst mode** modunda denetleyici veri yolunu alıp bir bloğu aralıksız taşır. **Cycle stealing** yaklaşımında ise arada tek veri yolu çevrimleri “ödünç alır”. İlki yüksek aktarım hızı, ikincisi daha dengeli işlemci erişimi sağlar.

## Basitleştirilmiş bir DMA kurulumu

Aşağıdaki C benzeri örnek, bellek eşlemeli DMA yazmaçlarının nasıl ayarlanabileceğini gösterir:

```c
#define DMA_SRC   (*(volatile unsigned int*)0x40000000)
#define DMA_DST   (*(volatile unsigned int*)0x40000004)
#define DMA_COUNT (*(volatile unsigned int*)0x40000008)
#define DMA_CTRL  (*(volatile unsigned int*)0x4000000C)

void dma_baslat(void* kaynak, void* hedef, unsigned int uzunluk) {
    DMA_SRC = (unsigned int)kaynak;
    DMA_DST = (unsigned int)hedef;
    DMA_COUNT = uzunluk;
    DMA_CTRL = 0x01; // Kanalı etkinleştir ve aktarımı başlat
}
```

`volatile`, derleyiciye bu adreslerin sıradan bellek olmadığını ve erişimlerin kaldırılmaması gerektiğini bildirir. Gerçek sistemlerde aktarım yönü, kanal önceliği, hata bitleri ve bellek bariyerleri de yapılandırılır.

## Önbellek ve güvenlik tuzakları

DMA doğrudan ana belleğe eriştiği için işlemci önbelleğiyle tutarsızlık oluşabilir. İşlemci değiştirdiği veriyi henüz RAM’e yazmamışsa DMA eski veriyi okuyabilir. Benzer biçimde DMA’nın yazdığı yeni veri işlemcinin önbelleğinde görünmeyebilir. Donanımsal **cache coherence** bulunmayan sistemlerde aktarım öncesi önbellek temizleme, sonrasında ise geçersiz kılma işlemleri gerekir.

Ayrıca sınırsız DMA erişimi güvenlik riski yaratır. Hatalı veya kötü niyetli bir aygıt, hassas bellek bölgelerini okuyabilir. **IOMMU**, aygıtların erişebileceği adresleri sınırlandırarak bu riski azaltır.

Kısacası DMA, işlemciyi kapatmaz; onu hamallıktan yöneticiliğe terfi ettirir. İşlemci işi planlar, DMA yükü taşır, kesme ise teslimat zilini çalar.
