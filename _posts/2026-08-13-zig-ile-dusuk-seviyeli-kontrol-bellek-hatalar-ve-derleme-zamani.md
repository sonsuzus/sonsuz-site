---
layout: post
title: "Zig ile Düşük Seviyeli Kontrol: Bellek, Hatalar ve Derleme Zamanı"
math: true
categories: 
  - Bilgi
tags: 
  - zig
  - sistem programlama
  - bellek yönetimi
  - compile time
image: /img/zig-ile-dusuk-22.png
---

![zig-ile-dusuk-22](/img/zig-ile-dusuk-22.svg)


C, onlarca yıldır işletim sistemlerinden gömülü cihazlara kadar düşük seviyeli yazılımın ortak diliydi. Zig ise C'nin performans ve donanıma yakınlık avantajlarını korurken, bellek yönetimini daha görünür, hata takibini daha disiplinli ve derleme zamanını daha üretken hâle getirmeyi amaçlar. Çöp toplayıcıya ihtiyaç duymadan güvenli alışkanlıklar kazandırması, onu özellikle sistem programlama meraklıları için ilginç bir seçenek yapar.

``

Zig'in temel felsefesi “gizli kontrol akışı yok” cümlesiyle özetlenebilir. Bir fonksiyon bellek ayırıyorsa, hata döndürebiliyorsa veya kaynak kapatıyorsa bunlar kodda açıkça görünür. Örneğin dilin varsayılan bir bellek ayırıcısı yoktur. Bu ilk bakışta zahmetli gelebilir; ancak programın hangi bellek stratejisini kullandığını mimari seviyede düşünmeye zorlar.

Bellek yönetiminde seçim tamamen geliştiriciye aittir. Kısa ömürlü işlemler için arena allocator, testler için genel amaçlı allocator veya gömülü sistemlerde sabit tampon tabanlı allocator tercih edilebilir. Bu yaklaşımın maliyeti ve getirisi şöyle karşılaştırılabilir:

| Yaklaşım | Avantaj | Dikkat edilmesi gereken nokta |
|---|---|---|
| Garbage collector | Kullanımı hızlıdır | Duraklamalar ve ek çalışma zamanı maliyeti olabilir |
| `malloc/free` | Esnek ve tanıdıktır | Sızıntı ve çift serbest bırakma riski taşır |
| Zig allocator | Strateji görünür ve değiştirilebilirdir | Ayırıcıyı fonksiyonlara taşımak gerekir |
| Sabit tampon | Öngörülebilir, hızlıdır | Kapasite sınırı dikkatle yönetilmelidir |

Aşağıdaki örnek, bir metni allocator kullanarak kopyalar. `errdefer`, fonksiyon hata ile çıkarsa ayrılmış kaynağı otomatik bırakır; başarılı durumda ise sahiplik çağırana devredilir.

```zig
const std = @import("std");

fn duplicate(allocator: std.mem.Allocator, text: []const u8) ![]u8 {
    const copy = try allocator.alloc(u8, text.len);
    errdefer allocator.free(copy);

    @memcpy(copy, text);
    return copy;
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    const allocator = gpa.allocator();
    const message = try duplicate(allocator, "Merhaba Zig");
    defer allocator.free(message);

    std.debug.print("{s}\n", .{message});
}
```

Burada `try`, hata oluşursa onu üst çağrıya iletir. Zig'de hatalar exception değildir; fonksiyonun dönüş türünün parçasıdır. Matematiksel olarak bir sonuç, kabaca $Result = Değer \cup Hata$ şeklinde düşünülebilir. Bu model, başarısız olabilecek işlemleri imzada görünür kılar. Örneğin dosya açma işlemi `!File` döndürüyorsa, çağıran taraf hatayı ele almak zorundadır.

Zig'i özel yapan diğer güç, derleme zamanı değerlendirmesidir. `comptime` ile türler, sabitler ve fonksiyon çağrıları derleme sırasında üretilebilir. Böylece C önişlemci makrolarının metin tabanlı ve kırılgan dünyası yerine, gerçek dil kurallarıyla çalışan bir metaprogramlama modeli elde edilir. Derleyici bazı hesaplamaları önceden yaparsa çalışma zamanı maliyeti yaklaşık olarak $T_{run} = T_{iş} - T_{comptime}$ kadar azalabilir.

```zig
const std = @import("std");

fn square(comptime T: type, value: T) T {
    return value * value;
}

pub fn main() void {
    const result = comptime square(i32, 12);
    std.debug.print("Sonuç: {}\n", .{result});
}
```

Bu örnekte `result` derleme aşamasında hesaplanabilir. Ancak `comptime` her problemi çözmek için kullanılmamalıdır: çok büyük veri üretimi derleme süresini uzatabilir. İyi denge, çalışma zamanındaki gerçek ihtiyacı ölçüp yalnızca sabit yapıdaki işleri derleyiciye taşımaktır.

Zig ayrıca C ile doğrudan etkileşim kurabilir; C başlıklarını içe aktarabilir ve C derleyicisi olarak kullanılabilir. Bu nedenle mevcut C kodunu bir gecede değiştirmek yerine, yeni modülleri Zig ile yazıp kademeli geçiş yapmak mümkündür. Sonuç olarak Zig, “daha az sihir, daha fazla niyet” yaklaşımıyla düşük seviyeli kontrol isteyen geliştiricilere modern ve güçlü bir alternatif sunar.
