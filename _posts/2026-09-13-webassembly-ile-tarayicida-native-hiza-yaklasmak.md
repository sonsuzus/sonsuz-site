---
layout: post
title: "WebAssembly ile Tarayıcıda Native Hıza Yaklaşmak"
math: true
categories: 
  - Bilgi
tags: 
  - webassembly
  - wasm
  - web performansı
toc: true
image: /img/webassembly-ile-tarayicida-90.png
---

Bir web sayfasının görüntü işlemek, fizik simülasyonu çalıştırmak veya milyonlarca veri noktasını analiz etmek için kullanılması geçmişte pek gerçekçi değildi. JavaScript motorları çok hızlandı; ancak C, C++ ve Rust gibi sistem dilleriyle geliştirilen ağır algoritmalar söz konusu olduğunda tarayıcıların yeni bir oyuncuya ihtiyacı vardı: **WebAssembly**, kısa adıyla WASM. Bu teknoloji, tarayıcıyı yalnızca belge gösteren bir uygulamadan yüksek performanslı bir çalışma platformuna dönüştürüyor.

``

## WebAssembly tam olarak nedir?

WebAssembly, işlemcinin doğrudan çalıştırdığı makine kodu değildir. Farklı dillerin derlenebildiği, taşınabilir ve düşük seviyeli bir **ikili komut formatıdır**. Tarayıcı WASM modülünü indirir, doğrular ve cihazın mimarisine uygun makine koduna dönüştürür.

Kabaca çalışma zinciri şöyledir:

$$\text{C/C++/Rust} \rightarrow \text{WASM bytecode} \rightarrow \text{JIT veya AOT} \rightarrow \text{Makine kodu}$$

Bu ara katman sayesinde aynı `.wasm` dosyası x86-64, ARM ve diğer mimarilerde çalışabilir. “Bir kere derle, tarayıcı olan her yerde koştur” fikrinin performans odaklı hâli diyebiliriz.

| Özellik | JavaScript | WebAssembly | Native uygulama |
|---|---|---|---|
| Çalışma ortamı | Tarayıcı motoru | WASM sanal makinesi | İşletim sistemi |
| Başlangıç kolaylığı | Çok yüksek | Derleme araçları gerekir | Platforma göre değişir |
| Sayısal performans | İyi | Native hıza yakın | Genellikle en yüksek |
| DOM erişimi | Doğrudan | JavaScript üzerinden | Bulunmaz |
| Güvenlik | Sandbox | Sandbox | Yetkilere bağlı |

## Neden hızlıdır?

JavaScript dinamik tiplidir. Motor, bir değişkenin sayı mı yoksa metin mi olduğunu çalışma sırasında takip edebilir. WebAssembly ise sayı türlerini önceden bilir. Örneğin `i32`, `i64`, `f32` ve `f64` gibi türler açıkça tanımlanır. Böylece motor daha az tahmin yapar ve daha kararlı optimizasyon uygular.

Bir algoritmanın toplam süresini basitleştirerek şöyle düşünebiliriz:

$$T_{toplam} = T_{indirme} + T_{derleme} + T_{çalıştırma} + T_{veri\ aktarımı}$$

WASM çoğunlukla $T_{çalıştırma}$ değerini düşürür. Buna karşılık JavaScript ile WASM arasında sürekli veri kopyalanırsa $T_{veri\ aktarımı}$ büyüyebilir. Bu nedenle küçük işler için WASM kullanmak, markete yarış arabasıyla gitmeye benzeyebilir.

## Rust ile küçük bir WASM fonksiyonu

Aşağıdaki Rust fonksiyonu, iki tam sayıyı toplar ve dışarıya çağrılabilir bir sembol olarak sunar:

```rust
#[no_mangle]
pub extern "C" fn topla(a: i32, b: i32) -> i32 {
    a + b
}
```

Kod uygun WASM hedefiyle derlendiğinde tarayıcı tarafından yüklenebilir. JavaScript tarafında modülü başlatıp dışa aktarılan fonksiyonu çağırabiliriz:

```javascript
const sonuc = await WebAssembly.instantiateStreaming(
  fetch("algoritma.wasm")
);

const toplam = sonuc.instance.exports.topla(20, 22);
console.log(toplam); // 42
```

`instantiateStreaming`, modül indirilirken derleme işleminin başlamasına imkân verir. Gerçek projelerde Rust için `wasm-bindgen`, C ve C++ içinse Emscripten gibi araçlar bellek yönetimi ve JavaScript bağlantısını kolaylaştırır.

## Hangi işlerde parlıyor?

WebAssembly özellikle görüntü ve video kodlama, CAD uygulamaları, oyun motorları, ses işleme, şifreleme, veri sıkıştırma, bilimsel simülasyon ve makine öğrenmesi çıkarımı gibi yoğun hesaplama gerektiren alanlarda etkilidir. SIMD komutları aynı anda birden fazla sayı üzerinde işlem yapılmasını sağlarken Web Workers ile birlikte kullanılan WASM thread’leri paralel hesaplamayı mümkün kılar.

Ancak WASM, JavaScript’in yerine geçen sihirli bir değnek değildir. DOM düğmelerini yönetmek, formları işlemek ve kullanıcı arayüzü oluşturmak için JavaScript hâlâ daha doğaldır. En verimli mimari genellikle hibrittir: JavaScript orkestrayı yönetir, WebAssembly ise ağır enstrümanları çalar.

Üstelik sandbox modeli sayesinde WASM modülleri belleğe, dosya sistemine veya cihaz kaynaklarına sınırsız biçimde erişemez. Sonuç olarak tarayıcının güvenlik sınırları korunurken performans sınırları ciddi biçimde genişler. Native hızın tamamı her zaman yakalanmasa da doğru algoritma ve iyi veri yönetimiyle aradaki fark şaşırtıcı ölçüde küçülebilir.

![webassembly-ile-tarayicida-90](/img/webassembly-ile-tarayicida-90.svg)

