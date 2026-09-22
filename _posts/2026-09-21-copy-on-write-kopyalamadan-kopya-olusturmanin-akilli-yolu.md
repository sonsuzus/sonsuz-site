---
layout: post
title: "Copy-on-Write: Kopyalamadan Kopya Oluşturmanın Akıllı Yolu"
math: true
categories: 
  - Bilgi
tags: 
  - copy-on-write
  - bellek
  - işletim-sistemleri
  - performans
  - c
  - veri-yapıları
toc: true
image: /img/copy-on-write-82.png
---

Bir nesnenin kopyasını çıkarmak çoğu zaman masum görünür: bellekte yeni bir alan ayır, verileri taşı ve devam et. Ancak yüzlerce megabaytlık verilerle çalışıyorsak bu işlem hem zaman hem bellek tüketir. Copy-on-Write, kısaca **CoW**, “Gerçekten değiştirmeyeceksen neden kopyalıyorsun?” diyerek iki kopyanın aynı belleği geçici olarak paylaşmasını sağlar.
``
## Temel fikir: Kopyayı ihtiyaç anına ertelemek

Normal, yani eager copy yaklaşımında bir veri kopyalandığı anda yeni bellek ayrılır. Copy-on-Write yaklaşımında ise yalnızca yeni bir referans oluşturulur. Asıl kopyalama, taraflardan biri veriyi değiştirmek istediğinde gerçekleşir.

| Özellik | Geleneksel kopyalama | Copy-on-Write |
|---|---|---|
| İlk kopyalama maliyeti | Yüksek | Çok düşük |
| Başlangıçtaki bellek tüketimi | Artar | Değişmez veya az artar |
| Yazma maliyeti | Normal | İlk yazmada ek maliyet vardır |
| Değiştirilmeyen kopyalarda verim | Düşük | Çok yüksek |
| Uygulama karmaşıklığı | Basit | Referans takibi gerektirir |

Bir veri bloğunun boyutu $n$ olsun. Geleneksel kopyalamanın zaman maliyeti yaklaşık

$$T_{copy}(n)=O(n)$$

iken CoW ile ilk kopyalama yalnızca bir referans sayacını artırdığı için yaklaşık $O(1)$ maliyetindedir. Değişiklik yapılırsa ertelenmiş $O(n)$ maliyeti o anda ödenir. Başka bir deyişle CoW maliyeti yok etmez; **yalnızca gerekene kadar erteler ve bazen tamamen önler**.

## Referans sayacı nasıl çalışır?

Paylaşılan veri bloğunun yanında kaç nesnenin bu bloğu kullandığını belirten bir sayaç tutulabilir. Sayaç $r=1$ ise verinin tek sahibi vardır ve doğrudan değişiklik yapılabilir. Eğer $r>1$ ise yazma öncesinde özel bir kopya oluşturulmalıdır.

Aşağıdaki sadeleştirilmiş C kodu bu karar mekanizmasını gösterir:

```c
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    size_t size;
    int refs;
} Buffer;

Buffer *clone(Buffer *source) {
    source->refs++;
    return source; // Veri henüz kopyalanmadı
}

Buffer *prepare_write(Buffer *buffer) {
    if (buffer->refs == 1)
        return buffer; // Tek sahip: güvenle değiştir

    Buffer *copy = malloc(sizeof(Buffer));
    copy->size = buffer->size;
    copy->data = malloc(copy->size);
    memcpy(copy->data, buffer->data, copy->size);
    copy->refs = 1;

    buffer->refs--;
    return copy;
}
```

`clone` fonksiyonu yalnızca sahip sayısını artırır. `prepare_write` ise paylaşım varsa bağımsız bir tampon üretir. Gerçek projelerde bellek serbest bırakma, hata kontrolü ve eşzamanlı erişim için atomik sayaçlar da gerekir; yani örnek, mekanizmanın iskeletidir.

## İşletim sistemlerinde CoW

CoW’un en ünlü kullanım alanlarından biri Unix benzeri sistemlerdeki `fork()` çağrısıdır. Yeni süreç oluşturulduğunda ebeveyn sürecin bütün belleğini hemen kopyalamak pahalı olur. Bunun yerine iki süreç aynı fiziksel sayfaları paylaşır ve sayfalar salt okunur olarak işaretlenir.

Süreçlerden biri yazmaya çalıştığında işlemci bir **page fault** üretir. İşletim sistemi ilgili sayfayı kopyalar, yazma iznini açar ve programı kaldığı yerden sürdürür. Uygulama açısından her süreç bağımsız belleğe sahipmiş gibi görünür; perde arkasında ise yalnızca değiştirilen sayfalar çoğaltılır.

## Ne zaman iyi bir seçimdir?

CoW; büyük metinler, resimler, koleksiyonlar ve sık kopyalanıp nadiren değiştirilen değerler için idealdir. Buna karşılık her kopyanın hemen değiştirildiği senaryolarda yalnızca maliyeti erteleyip ek kontrol yükü oluşturabilir. Çok iş parçacıklı uygulamalarda referans sayacı ve yazma anı yarış koşullarına karşı korunmalıdır.

Özetle Copy-on-Write, “önce paylaş, gerekirse ayır” ilkesidir. Kopyaların çoğu hiç değiştirilmezse ciddi performans ve bellek kazancı sağlar. Değişiklik geldiğinde ise illüzyon bozulur, özel kopya oluşturulur ve herkes kendi verisiyle yoluna devam eder.

![copy-on-write-82](/img/copy-on-write-82.svg)

