---
layout: post
title: "WebAssembly (WASM) Nedir? Tarayıcıda Yerel Hıza Yaklaşmak"
math: true
categories: 
  - Bilgi
tags: 
  - WebAssembly
  - WASM
  - JavaScript
  - Performans
  - Tarayıcı
---

Web uygulamaları yıllarca JavaScript motorlarının omuzlarında yükseldi. Ancak görüntü işleme, 3B modelleme, oyun motorları ve bilimsel hesaplamalar gibi yoğun işlerde JavaScript tek başına her zaman ideal değildir. WebAssembly (WASM), derlenmiş kodun tarayıcı içinde güvenli biçimde, yerel uygulamalara yakın performansla çalışmasını sağlayan ikili bir komut formatıdır. Kısacası WASM, web platformuna takılmış küçük ama güçlü bir turbo motordur.

``

## WASM tam olarak ne yapar?

WebAssembly bir programlama dili değildir; düşük seviyeli, taşınabilir bir **derleme hedefidir**. C, C++, Rust, Go, AssemblyScript ve benzeri dillerle yazılmış kodlar `.wasm` uzantılı ikili modüllere dönüştürülebilir. Tarayıcı bu modülü doğrular, derler ve JavaScript ile birlikte çalıştırır.

Performans fikrini basitleştirelim. Bir görevin çalışma süresi kabaca şu şekilde düşünülebilir:

$$T_{toplam} = T_{hesaplama} + T_{bellek} + T_{veri\ transferi}$$

WASM özellikle $T_{hesaplama}$ yüksek olan algoritmalarda fark yaratır. Fakat JavaScript ile WASM arasında sürekli veri kopyalamak $T_{veri\ transferi}$ maliyetini yükseltebilir. Yani her problemi WASM'a çevirmek otomatik olarak roket hızı sağlamaz; doğru iş yükünü seçmek gerekir.

| Özellik | JavaScript | WebAssembly |
|---|---|---|
| Kaynak biçimi | İnsan tarafından okunabilir metin | Sıkıştırılmış ikili modül |
| Güçlü olduğu alan | Arayüz, DOM, hızlı geliştirme | Yoğun hesaplama, medya, oyun |
| DOM erişimi | Doğrudan | Genellikle JavaScript aracılığıyla |
| Çalışma ortamı | Tarayıcı ve Node.js | Tarayıcı, Node.js, WASI ortamları |
| Güvenlik modeli | Sandbox | Sandbox ve doğrulanmış modül |

## Tarayıcıda nasıl çalışır?

Bir WASM modülü doğrudan sayfadaki düğmelere veya DOM'a dokunmaz. Bunun yerine JavaScript bir köprü görevi görür: modülü yükler, fonksiyonlarını çağırır ve sonucu ekrana yansıtır. Bu ayrım aslında sağlıklıdır; kullanıcı arayüzü JavaScript'te, ağır matematik ise WASM'da kalır.

Aşağıdaki örnek, bir `.wasm` dosyasını indirip içindeki `topla` fonksiyonunu çağırır:

```javascript
async function wasmTopla(a, b) {
  const response = await fetch('/hesaplama.wasm');
  const bytes = await response.arrayBuffer();
  const { instance } = await WebAssembly.instantiate(bytes);

  return instance.exports.topla(a, b);
}

wasmTopla(20, 22).then(sonuc => {
  console.log(`Sonuç: ${sonuc}`); // 42
});
```

Bu kodun amacı modülü tarayıcıya yüklemek ve dışa aktarılan fonksiyona erişmektir. Gerçek projelerde `WebAssembly.instantiateStreaming()` tercih edilebilir; sunucu doğru `application/wasm` MIME türünü gönderiyorsa indirme sürerken derleme başlayabilir.

```javascript
const { instance } = await WebAssembly.instantiateStreaming(
  fetch('/hesaplama.wasm')
);

console.log(instance.exports.topla(5, 7));
```

## Ne zaman kullanmalısınız?

WASM, “sitem yavaş” cümlesinin sihirli cevabı değildir. Ağ gecikmesi, devasa görseller, kötü DOM işlemleri veya gereksiz React render'ları için önce klasik web performans tekniklerine bakılmalıdır. WASM'ın yıldızı, tekrar eden ve CPU tüketen hesaplarda parlar.

| Senaryo | WASM uygun mu? | Neden? |
|---|---:|---|
| Form doğrulama | Hayır | JavaScript daha basit ve yeterli |
| Görüntü filtreleme | Evet | Piksel bazlı yoğun hesaplama içerir |
| Video/ses kodlama | Evet | Mevcut yerel kütüphaneler kullanılabilir |
| DOM animasyonu | Genellikle hayır | Asıl darboğaz render hattı olabilir |
| CAD veya 3B görüntüleyici | Evet | Geometri ve fizik hesapları ağırdır |

Rust, bellek güvenliği ve güçlü WASM araç zinciri nedeniyle popüler bir seçimdir. Örneğin `wasm-pack`, Rust kodunu web projelerine uygun paketlere dönüştürür. C++ tarafında ise Emscripten, mevcut oyun veya grafik kütüphanelerini web'e taşımada sık kullanılır.

Sonuç olarak WebAssembly, JavaScript'in rakibi değil, onun performans odaklı ekip arkadaşıdır. Arayüz ve web API'leri için JavaScript'i; hesaplama yoğun çekirdekler için WASM'ı kullanmak, modern web uygulamalarında en dengeli mimarilerden birini oluşturur.
