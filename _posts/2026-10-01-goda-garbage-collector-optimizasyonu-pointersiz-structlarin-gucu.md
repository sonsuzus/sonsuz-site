---
layout: post
title: "Go'da Garbage Collector Optimizasyonu: Pointersız Struct'ların Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - go
  - golang
  - garbage-collector
  - bellek-optimizasyonu
  - performans
  - struct
toc: true
image: /img/goda-garbage-collector-91.png
---

![goda-garbage-collector-91](/img/goda-garbage-collector-91.svg)


Go’nun Garbage Collector’ı geliştiriciyi manuel bellek yönetiminden kurtarır; ancak milyonlarca nesneyle çalışan servislerde bu konforun küçük bir faturası vardır: GC, canlı işaretçileri bulmak için heap üzerindeki nesneleri tarar. Struct’larımızı işaretçi içermeyecek biçimde tasarladığımızda Go çalışma zamanı bu nesneleri **noscan** olarak sınıflandırabilir. Böylece nesnelerin kapladığı bellek hâlâ yönetilirken içlerinin pointer aramak amacıyla taranmasına gerek kalmaz.
``
## GC neden pointer peşinde koşar?

Go GC, eşzamanlı çalışan üç renkli işaretleme yaklaşımını kullanır. Basitleştirirsek nesneler beyaz, gri ve siyah kümelerde düşünülür. Köklerden erişilebilen nesneler keşfedilir; içlerinde bulunan pointer’lar başka nesnelere ulaşmak için takip edilir. Tarama maliyetini kabaca şöyle modelleyebiliriz:

$$T_{scan} \approx N_p \times C_p$$

Burada $N_p$ incelenen pointer alanlarının sayısını, $C_p$ ise her alanı işleme maliyetini temsil eder. Pointersız bir nesne için $N_p=0$ olduğundan nesnenin **iç tarama maliyeti** sıfıra yaklaşır. Bu, tüm GC maliyetinin veya duraklama süresinin sıfır olacağı anlamına gelmez; tahsis, işaretleme altyapısı ve sweep işlemleri devam eder.

| Veri alanı | Pointer içerir mi? | GC taraması |
|---|---:|---|
| `uint64`, `int32`, `bool` | Hayır | İçerik taranmaz |
| Sabit uzunluklu sayı dizisi | Hayır | İçerik taranmaz |
| `string` | Evet | Veri adresi izlenir |
| `slice` | Evet | Arka dizi adresi izlenir |
| `map`, pointer, interface | Evet | İlgili referanslar izlenir |

## Pointer ağırlıklı model

Aşağıdaki kayıt okunaklıdır fakat `string` ve slice alanları nedeniyle pointer barındırır:

```go
type Event struct {
    ID      uint64
    User    string
    Payload []byte
    Active  bool
}
```

Her `Event`, kullanıcı adı ve payload verisini başka bellek bölgelerine bağlar. Milyonlarca kayıt bellekte tutulduğunda GC yalnızca kayıtları değil, bu bağlantıları da değerlendirmek zorundadır.

## Pointersız alternatif

Verilerin üst sınırları biliniyorsa sabit boyutlu diziler ve uzunluk alanları kullanılabilir:

```go
type Event struct {
    ID         uint64
    User       [32]byte
    Payload    [256]byte
    UserLen    uint8
    PayloadLen uint16
    Active     bool
}

func (e *Event) SetUser(name string) {
    e.UserLen = uint8(copy(e.User[:], name))
}

func (e Event) UserString() string {
    return string(e.User[:e.UserLen])
}
```

Struct’ın alanları sayı, boolean ve sabit byte dizilerinden oluşur. `SetUser`, gelen metni struct içindeki diziye kopyalar. `UserString` ise gerektiğinde metin üretir; fakat bu dönüşüm yeni tahsis oluşturabileceğinden sıcak döngülerde doğrudan byte görünümüyle çalışmak daha avantajlıdır.

Bu yaklaşım bedava değildir. Her olay 256 byte payload taşımasa bile struct içinde o alan ayrılır. Yaklaşık bellek tüketimi şu şekilde düşünülebilir:

$$M \approx N \times sizeof(Event)$$

Dolayısıyla pointersız tasarım, GC taramasını azaltırken veri seyrekse toplam belleği artırabilir.

## Kimliklerle referans kurmak

Nesneleri pointer ile birbirine bağlamak yerine sayısal kimlikler ve merkezi diziler kullanılabilir:

```go
type Node struct {
    Value int64
    Next  uint32 // Pointer değil, dizideki indeks
}

type Graph struct {
    Nodes []Node
}
```

`Node` tamamen pointersızdır. `Graph` içindeki slice ise pointer taşır, ancak GC milyonlarca düğümde bağlantı aramak yerine yalnızca üst düzey slice bilgisini tarar. İndeks kullanımı ayrıca verileri ardışık tutarak CPU önbelleği açısından kazanç sağlayabilir.

## Ölçmeden optimize etmeyin

Kararı tahminle değil benchmark ve GC izleriyle verin:

```bash
go test -bench=. -benchmem
GODEBUG=gctrace=1 go run .
go tool pprof -http=:8080 heap.out
```

`-benchmem` tahsis sayılarını, `gctrace` GC davranışını, heap profili ise belleği hangi tiplerin tuttuğunu gösterir. Pointersız struct’lar özellikle önbellekler, telemetri tamponları, oyun dünyaları ve büyük indekslerde güçlüdür. Buna karşılık değişken uzunluklu verilerde sabit diziler ciddi israf yaratabilir. En iyi sonuç; pointer sayısını azaltmak, nesne ömrünü kontrol etmek, toplu veri düzeni kullanmak ve her değişikliği gerçek trafik altında ölçmekle gelir.
