---
layout: post
title: "ABI Nedir? Derlenen Programların Görünmez Ortak Dili"
math: true
categories: 
  - Bilgi
tags: 
  - abi
  - derleyici
  - işletim sistemi
  - assembly
  - bağlayıcı
  - sistem programlama
toc: true
---

Bir C fonksiyonunu Rust’tan çağırdığınızda ya da işletim sistemi derlenmiş programınızı çalıştırdığında taraflar kaynak kodu tartışmaz. Bunun yerine; parametrelerin nereye konacağı, sonuçların nasıl döndürüleceği ve belleğin nasıl düzenleneceği gibi önceden belirlenmiş kurallara uyarlar. İşte bu görünmez anlaşmanın adı **ABI**, yani *Application Binary Interface*’tir.

``

## ABI tam olarak neyi tanımlar?

ABI, derlenmiş ikili bileşenlerin birbiriyle nasıl iletişim kuracağını belirleyen kurallar bütünüdür. Bir fonksiyon çağrısının makine seviyesinde gerçekleşebilmesi için yalnızca fonksiyon adını bilmek yetmez. İşlemcinin ve işletim sisteminin şu sorular üzerinde anlaşması gerekir:

- Parametreler hangi yazmaçlara veya yığına yerleştirilecek?
- Dönüş değeri nerede bulunacak?
- Hangi yazmaçları çağıran, hangilerini çağrılan fonksiyon koruyacak?
- Veri türlerinin boyutu ve hizalaması ne olacak?
- Semboller ikili dosyada nasıl adlandırılacak?
- Çalıştırılabilir dosya hangi biçimi kullanacak?

Örneğin bir veri yapısının bellekte kapladığı alan yalnızca alan boyutlarının toplamı değildir. Hizalama nedeniyle kabaca

$$
S = \sum_{i=1}^{n} s_i + P
$$

şeklinde düşünülebilir. Burada $s_i$ alanların boyutunu, $P$ ise derleyicinin eklediği dolgu baytlarını ifade eder. İki taraf farklı $P$ değerleri beklerse aynı bellek bölgesini farklı yorumlayabilir.

## API ile ABI aynı şey değildir

İsimleri benzer olsa da görev yaptıkları katmanlar farklıdır:

| Özellik | API | ABI |
|---|---|---|
| Açılım | Application Programming Interface | Application Binary Interface |
| Hedef | Kaynak kod | Derlenmiş makine kodu |
| Tanımladığı şey | Fonksiyonlar, sınıflar, sözleşmeler | Yazmaçlar, veri yerleşimi, çağrı kuralları |
| Uyumsuzluk sonucu | Derleme hatası | Bağlama hatası veya çalışma zamanı çökmesi |
| Kullanıcı | Programcı | Derleyici, bağlayıcı, işletim sistemi |

Bir kütüphanenin API’si değişmeden ABI’si bozulabilir. Örneğin herkese açık bir `struct` içine yeni alan eklemek, kaynak kod açısından masum görünse de yapının boyutunu ve alan ofsetlerini değiştirir. Eski sürüme göre derlenmiş uygulama artık yanlış adreslerden veri okuyabilir.

## Çağrı sözleşmesi: Fonksiyonların trafik kuralları

Aşağıdaki C fonksiyonunu düşünelim:

```c
int topla(int a, int b) {
    return a + b;
}
```

x86-64 System V ABI’de ilk iki tamsayı parametresi genellikle `RDI` ve `RSI` yazmaçlarına yerleştirilir; sonuç `RAX` üzerinden döndürülür. Basitleştirilmiş assembly karşılığı şöyledir:

```asm
topla:
    mov eax, edi     ; İlk parametreyi sonuç yazmacına al
    add eax, esi     ; İkinci parametreyi ekle
    ret              ; Sonucu EAX/RAX üzerinden döndür
```

Windows x64 ABI ise ilk parametreler için farklı yazmaçlar kullanır. Dolayısıyla aynı işlemci mimarisinde çalışmak, aynı ABI’yi kullanmak anlamına gelmez.

| Ortam | İlk tamsayı parametreleri | Tamsayı dönüş değeri |
|---|---|---|
| Linux x86-64 System V | RDI, RSI, RDX, RCX | RAX |
| Windows x64 | RCX, RDX, R8, R9 | RAX |
| AArch64 | X0–X7 | X0 |

## Dil uyumluluğunun gizli kahramanı

C’nin ABI’si görece sade ve kararlı olduğu için birçok dil ortak buluşma noktası olarak C arayüzünü kullanır. Rust’taki `extern "C"` ifadesi bunun açık bir örneğidir:

```rust
extern "C" {
    fn topla(a: i32, b: i32) -> i32;
}
```

Buradaki `"C"`, fonksiyonun C dilinde yazıldığını değil, **C çağrı sözleşmesine göre çağrılması gerektiğini** belirtir. Aksi hâlde derleyiciler parametreleri farklı yerlere koyabilir veya fonksiyon adını farklı biçimde kodlayabilir.

## ABI neden önemlidir?

Dinamik kütüphaneler, eklenti sistemleri, işletim sistemi çağrıları ve diller arası iletişim ABI sayesinde çalışır. Bir `.so` ya da `.dll` dosyasını güncellerken ABI uyumluluğunu korumak, uygulamaların yeniden derlenmeden çalışabilmesini sağlar.

Kısacası API, geliştiricilerin konuştuğu dilse ABI makinelerin lehçesidir. Görünmezdir; fakat kurallardan biri ihlal edildiğinde bağlayıcı hataları, bozuk veriler ve gizemli çökmelerle oldukça görünür hâle gelir.
