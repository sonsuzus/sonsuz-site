---
layout: post
title: "Zig Dilinde comptime: Derleme Zamanı Kod Çalıştırmanın En Zarif Hali"
math: true
categories: 
  - Bilgi
tags: 
  - zig
  - comptime
  - derleme zamanı
  - metaprogramlama
  - sistem programlama
  - generics
toc: true
image: /img/zig-dilinde-comptime-26.png
---

C makrolarının metin değiştirme numaralarıyla, C++ şablonlarının hata mesajı destanları arasında kaybolduysanız Zig’in `comptime` özelliği ferah bir nefes gibi gelebilir. Zig, metaprogramlamayı ayrı ve gizemli bir alt dil olmaktan çıkarır: Normal Zig kodunu, uygun veriler biliniyorsa derleme sırasında çalıştırır. Böylece tür üretmekten matematiksel hesaplamalara kadar pek çok iş, çalışma zamanına yük bindirmeden yapılabilir.

![zig-dilinde-comptime-26](/img/zig-dilinde-comptime-26.svg)

``
## `comptime` tam olarak nedir?

`comptime`, bir değerin veya işlemin derleme sırasında bilinmesi gerektiğini belirtir. Derleyici bu kodu program çalışmadan önce değerlendirir ve ortaya çıkan sonucu üretilen makine koduna yerleştirir.

Basitçe iki farklı zaman dünyası düşünelim:

| Özellik | Derleme zamanı | Çalışma zamanı |
|---|---|---|
| Girdi kaynağı | Sabitler, türler, yapılandırmalar | Kullanıcı, dosya, ağ |
| Maliyet | Derleme süresine eklenir | Program çalışırken ödenir |
| Sonuç | Makine koduna gömülebilir | Bellekte hesaplanır |
| Hata yakalama | Derleme sırasında | Çalışma sırasında |

Bir işlemin maliyetini kabaca $T(n)$ ile gösterirsek, derleme zamanında hesaplanan sabit bir sonuç için çalışma zamanı maliyeti çoğu durumda

$$T_{runtime}(n) \approx O(1)$$

olur. Elbette hesaplama yok olmaz; maliyet yalnızca derleme aşamasına taşınır.

## Normal fonksiyon, sıra dışı zamanlama

Zig’de derleme zamanı hesabı yapmak için bambaşka bir sözdizimi öğrenmek gerekmez:

```zig
fn factorial(comptime n: u32) comptime_int {
    return if (n == 0) 1 else n * factorial(n - 1);
}

pub fn main() void {
    const result = factorial(10);
    _ = result;
}
```

Buradaki `n`, mutlaka derleme zamanında bilinmelidir. Derleyici fonksiyonu çalıştırır ve $10! = 3\,628\,800$ sonucunu programa sabit olarak yerleştirebilir. Aynı fonksiyona çalışma zamanında elde edilen rastgele bir değer verilirse derleme başarısız olur. Bu kısıtlama bir kusur değil, açık bir sözleşmedir.

## Türler de birer değerdir

`comptime` özelliğinin en güçlü taraflarından biri, Zig’de türlerin derleme zamanı değerleri olarak kullanılabilmesidir. Böylece jenerik fonksiyonlar şaşırtıcı ölçüde sade görünür:

```zig
fn maximum(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

const integer_max = maximum(i32, 12, 27);
const float_max = maximum(f64, 3.5, 8.2);
```

`T`, derleme sırasında verilen bir türdür. Derleyici her kullanım için uygun ve tür güvenli kodu üretir. Metinsel kopyalama yapılmadığından C makrolarındaki parantez tuzakları veya çift değerlendirme sorunları ortaya çıkmaz.

| Yaklaşım | Çalışma biçimi | Tür güvenliği | Ayrı metadil |
|---|---|---:|---:|
| C makrosu | Metin değiştirme | Zayıf | Evet, önişlemci |
| C++ şablonu | Şablon örnekleme | Güçlü | Büyük ölçüde evet |
| Zig `comptime` | Normal kodu değerlendirme | Güçlü | Hayır |

## Derleme zamanında tür üretmek

Fonksiyonlar yalnızca sayı değil, yeni bir tür de döndürebilir:

```zig
fn FixedBuffer(comptime T: type, comptime capacity: usize) type {
    return struct {
        items: [capacity]T = undefined,
        len: usize = 0,

        const Self = @This();

        pub fn push(self: *Self, value: T) !void {
            if (self.len == capacity) return error.Full;
            self.items[self.len] = value;
            self.len += 1;
        }
    };
}

const ByteBuffer = FixedBuffer(u8, 256);
```

Bu örnek, eleman türü ve kapasitesi derleme sırasında belirlenen özel bir tampon türü oluşturur. Kapasite sabit olduğundan dinamik bellek ayırmak gerekmez; derleyici `[256]u8` boyutunu doğrudan bilir.

## Ne zaman kullanılmalı?

`comptime`; jenerik veri yapıları, doğrulama, tablo üretimi, platform seçimi ve yansıma tabanlı serileştirme için idealdir. Ancak devasa hesaplamaları gelişigüzel biçimde derleme zamanına taşımak derlemeyi yavaşlatabilir. Altın kural şudur: Girdi önceden biliniyor ve sonuç programın yapısını etkiliyorsa `comptime` güçlü bir adaydır.

Zig’in asıl zarafeti yeni bir sihir icat etmesinde değil, sihri kaldırmasındadır. Döngüler yine döngü, fonksiyonlar yine fonksiyondur; yalnızca ne zaman çalışacakları bilinçli biçimde seçilir.
