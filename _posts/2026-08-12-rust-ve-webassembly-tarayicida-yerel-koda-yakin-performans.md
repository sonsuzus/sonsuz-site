---
layout: post
title: "Rust ve WebAssembly: Tarayıcıda Yerel Koda Yakın Performans"
math: true
categories: 
  - Bilgi
tags: 
  - rust
  - webassembly
  - wasm
  - frontend
  - performans
image: /img/rust-ve-webassembly-18.png
---

Web uygulamalarında JavaScript hâlâ merkezdedir; ancak yoğun hesaplama, görüntü işleme, fizik simülasyonu ve sıkıştırma gibi görevlerde tek başına ideal olmayabilir. Rust ile WebAssembly (WASM) ikilisi, tarayıcı içinde güvenli bellek yönetimi ve yerel koda yakın çalışma hızı sunarak bu açığı kapatır. Buradaki amaç JavaScript’i tamamen kovmak değil; arayüzü JavaScript’e, hesaplama motorunu ise Rust’a vermektir.

``

## WASM neden hızlıdır?

WebAssembly, tarayıcıların çalıştırabildiği ikili bir komut biçimidir. Rust kaynak kodu doğrudan WASM dosyasına derlenir; tarayıcı da bu dosyayı doğrular, derler ve JavaScript tarafından çağrılabilir hâle getirir. WASM, donanımın makine kodu değildir; güvenli bir sanal makinede çalışır. Buna rağmen önceden tanımlı, düşük seviyeli komutları ve doğrulanabilir yapısı sayesinde yorumlanan kod yükünü azaltır.

Performansı kabaca şu şekilde düşünebiliriz:

$$T_{toplam} = T_{hesaplama} + T_{veri\ transferi} + T_{başlatma}$$

Rust tarafında $T_{hesaplama}$ ciddi ölçüde azalabilir. Fakat büyük dizileri JavaScript ile WASM arasında sürekli kopyalamak, $T_{veri\ transferi}$ maliyetini büyütebilir. Bu nedenle WASM’a küçük küçük iş vermek yerine, büyük hesaplama paketleri göndermek daha verimlidir.

| Özellik | JavaScript | Rust + WASM |
|---|---|---|
| Başlangıç maliyeti | Genellikle düşüktür | WASM indirme ve başlatma maliyeti vardır |
| Yoğun sayısal işlemler | Motor optimizasyonuna bağlıdır | Daha öngörülebilir ve hızlı olabilir |
| DOM erişimi | Doğrudan ve pratiktir | Genellikle JavaScript köprüsü gerekir |
| Bellek güvenliği | Dinamik çalışma zamanı kuralları | Rust sahiplik modeliyle derleme zamanında güçlüdür |
| Uygun kullanım | Arayüz ve olay yönetimi | Algoritma, medya, kripto, simülasyon |

## Gerekli araç zinciri

Başlamak için Rust’ın yanı sıra `wasm-pack` aracı gerekir. `wasm-pack`, Rust crate’ini WASM’a derler, JavaScript paketini üretir ve `wasm-bindgen` köprüsünü yapılandırır.

```bash
cargo install wasm-pack
cargo new --lib hizli-hesaplayici
cd hizli-hesaplayici
```

`Cargo.toml` dosyasında kütüphanenin hem Rust hem WASM hedefi için üretilebilmesini belirtelim:

```toml
[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen = "0.2"
```

Ardından `src/lib.rs` içine JavaScript’in çağıracağı basit ama hesaplama odaklı bir fonksiyon yazabiliriz. Aşağıdaki örnek, bir dizideki değerlerin kareleri toplamını hesaplar:

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn kareler_toplami(sayilar: &[f64]) -> f64 {
    sayilar.iter().map(|sayi| sayi * sayi).sum()
}
```

`#[wasm_bindgen]` özniteliği, fonksiyonun JavaScript dünyasına açılmasını sağlar. Rust dilim türü olan `&[f64]`, köprü tarafından uygun WASM bellek gösterimine dönüştürülür. Gerçek projelerde çok büyük verilerde kopyalama davranışını ölçmek önemlidir.

Paketi web hedefiyle üretmek için şu komut yeterlidir:

```bash
wasm-pack build --target web
```

Bu işlem sonunda `pkg` klasöründe `.wasm` dosyası, JavaScript sarmalayıcısı ve TypeScript tür tanımları oluşur. Tarayıcı tarafında modülü asenkron başlatırız:

```javascript
import init, { kareler_toplami } from "./pkg/hizli_hesaplayici.js";

await init();
const sonuc = kareler_toplami(new Float64Array([2, 3, 4]));
console.log(sonuc); // 29
```

## Performansın gizli düşmanı: sınır geçişleri

WASM her problem için sihirli hız iksiri değildir. DOM güncellemek, buton olaylarını dinlemek veya birkaç sayıyı toplamak için Rust’a geçmek çoğu zaman gereksizdir. JavaScript-WASM çağrılarının da bir maliyeti vardır. Binlerce küçük çağrı yerine tek çağrıda binlerce eleman işlemek daha mantıklıdır.

| Senaryo | Önerilen yaklaşım |
|---|---|
| Form, menü, DOM animasyonu | JavaScript veya TypeScript |
| Görsel filtreleme | Rust + WASM |
| Oyun fiziği | Rust + WASM, çizim için Web API’leri |
| CSV ayrıştırma ve analiz | Veri büyüklüğüne göre hibrit yapı |
| Kriptografik veya sıkıştırma işlemleri | Rust + WASM |

Sonuç olarak Rust ve WASM, frontend’in yerine geçen değil, onu güçlendiren bir ikilidir. Ölçüm yapmadan optimizasyon kararı vermeyin: önce tarayıcı profil aracında darboğazı bulun, sonra hesaplama yoğun bölümü WASM’a taşıyın. Böylece hem JavaScript’in çevikliğini hem de Rust’ın disiplinli performansını aynı uygulamada kullanabilirsiniz.

![rust-ve-webassembly-18](/img/rust-ve-webassembly-18.svg)

