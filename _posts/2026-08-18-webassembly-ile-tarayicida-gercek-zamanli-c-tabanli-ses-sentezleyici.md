---
layout: post
title: "WebAssembly ile Tarayıcıda Gerçek Zamanlı C Tabanlı Ses Sentezleyici"
math: true
categories: 
  - Proje
tags: 
  - webassembly
  - c
  - web audio apı
image: /img/webassembly-ile-tarayicida-28.png
---

Tarayıcıda ses üretmek eskiden JavaScript döngülerine ve sınırlı performansa mahkûm bir iş gibi görünürdü. WebAssembly (WASM) sayesinde C ile yazılmış küçük, hızlı ve taşınabilir bir sentez motorunu doğrudan tarayıcıda çalıştırmak mümkün. Bu projede amaç, bir osilatörün ürettiği dalga formunu gerçek zamanlı olarak Web Audio API hattına aktararak temel ama genişletilebilir bir synthesizer oluşturmaktır.


![webassembly-ile-tarayicida-28](/img/webassembly-ile-tarayicida-28.svg)

``

Ses, saniyedeki örneklerden oluşan sayısal bir sinyaldir. Örnekleme hızı $f_s = 44100\,Hz$ ise tarayıcı her saniye 44.100 adet sayı bekler. Sinüs osilatörü için temel denklem şöyledir:

$$x[n] = A \sin\left(2\pi f \frac{n}{f_s}\right)$$

Burada $A$ genlik, $f$ frekans, $n$ ise örnek indeksidir. Ancak gerçek zamanlı sistemlerde mutlak örnek indeksi yerine **faz biriktirici** kullanmak daha pratiktir. Her örnekte fazı $\Delta \phi = f / f_s$ kadar artırır, faz 1'i geçtiğinde başa sararız. Bu yaklaşım, nota frekansı değişirken dalganın sürekliliğini korur.

| Kavram | JavaScript ile yaklaşım | C + WebAssembly yaklaşımı |
|---|---|---|
| Hesaplama maliyeti | JIT ve çöp toplayıcıdan etkilenebilir | Daha öngörülebilir sayısal çalışma |
| Kod paylaşımı | Web odaklıdır | DSP kodu masaüstü ve webde kullanılabilir |
| Bellek erişimi | JavaScript dizileri | WASM linear memory üzerinden tampon erişimi |
| Uygun kullanım | Prototip ve arayüz | Osilatör, filtre, efekt, miksaj |

İlk olarak C tarafında mono bir ses tamponunu dolduran fonksiyonumuzu yazalım. `phase` değişkeni statik tutulduğu için her çağrıda dalga formu kaldığı yerden devam eder. Bu ayrıntı yoksa tarayıcı her ses bloğunda dalgayı baştan başlatır ve rahatsız edici klik sesleri üretir.

```c
#include <math.h>
#include <stdint.h>

#define SAMPLE_RATE 44100.0f
static float phase = 0.0f;

void render(float *buffer, int frames, float frequency, float gain) {
    float phase_step = frequency / SAMPLE_RATE;

    for (int i = 0; i < frames; i++) {
        buffer[i] = gain * sinf(2.0f * M_PI * phase);
        phase += phase_step;
        if (phase >= 1.0f) phase -= 1.0f;
    }
}
```

Bu dosya Emscripten ile WASM'a dönüştürülebilir. `render` fonksiyonunu dışarı açmak ve belleği JavaScript'in okuyabilmesi için tipik derleme komutu şöyledir:

```bash
emcc synth.c -O3 -s WASM=1 \
  -s EXPORTED_FUNCTIONS='["_render","_malloc","_free"]' \
  -s EXPORTED_RUNTIME_METHODS='["HEAPF32"]' \
  -o synth.js
```

Tarayıcı tarafında ideal ses hattı `AudioWorklet`tir. Ana iş parçacığındaki `ScriptProcessorNode` eski bir çözümdür ve arayüz yoğunken kesintiye uğrayabilir. AudioWorklet ayrı bir ses iş parçacığında blok blok çalışır. Her blok çoğunlukla 128 kare içerir; dolayısıyla $44100 / 128 \approx 344$ kez çağrılır. Bu nedenle render fonksiyonunda bellek ayırmak, DOM'a erişmek veya ağır loglama yapmak yasaktır.

Aşağıdaki worklet örneği, WASM belleğinden gelen örnekleri çıkış kanalına kopyalama fikrini gösterir:

```js
class SynthProcessor extends AudioWorkletProcessor {
  process(inputs, outputs) {
    const output = outputs[0][0];
    const frames = output.length;

    // wasmRender, WASM tamponunu doldurur.
    const ptr = wasmRender(frames, 440, 0.15);
    const samples = new Float32Array(wasm.memory.buffer, ptr, frames);
    output.set(samples);
    return true;
  }
}
registerProcessor('synth-processor', SynthProcessor);
```

Genlik değerini genellikle $[-1, 1]$ aralığında tutun; daha büyük değerler kırpılmaya (clipping) yol açar. Güvenli bir başlangıç için `0.1` veya `0.2` gain iyi seçimdir. Ayrıca 440 Hz sabit değerini MIDI notalarına bağlamak için $f = 440 \times 2^{(m-69)/12}$ formülünü kullanabilirsiniz.

| Sonraki geliştirme | Kazandırdığı özellik |
|---|---|
| Kare ve testere dalgası | Daha karakterli tınılar |
| ADSR zarfı | Tuşa basma ve bırakma hissi |
| Low-pass filtre | Parlaklığı kontrol etme |
| Polyphony | Aynı anda birden fazla nota |

Bu mimarinin gücü, ses matematiğini C tarafında izole ederken klavye, arayüz ve MIDI etkileşimlerini JavaScript'e bırakmasından gelir. Böylece küçük bir sinüs osilatörü, zamanla tarayıcıda çalışan ciddi bir müzik aracına dönüşebilir.
