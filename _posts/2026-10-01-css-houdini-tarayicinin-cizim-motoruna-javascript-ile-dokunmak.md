---
layout: post
title: "CSS Houdini: Tarayıcının Çizim Motoruna JavaScript ile Dokunmak"
math: true
categories: 
  - Bilgi
tags: 
  - css
  - javascript
  - houdini
  - paint-api
  - typed-om
  - web-performans
toc: true
image: /img/css-houdini-tarayicinin-31.png
---

![css-houdini-tarayicinin-31](/img/css-houdini-tarayicinin-31.svg)


CSS güçlüdür; ancak standartlara eklenmemiş bir görsel efekt veya yerleşim davranışı istediğimizde çoğunlukla JavaScript ile DOM elemanları üretmeye başlarız. CSS Houdini ise sihirbaz şapkasından tavşan değil, tarayıcının işleme sürecine kontrollü kancalar çıkarır. Böylece geliştiriciler özel CSS özellikleri tanımlayabilir, görseller çizebilir ve deneysel olarak yeni yerleşim algoritmaları geliştirebilir.
``

## Houdini aslında nedir?

Tarayıcı bir sayfayı kabaca şu sırayla işler: CSS kurallarını ayrıştırır, stil değerlerini hesaplar, elemanların geometrisini belirler ve pikselleri çizer. Bu süreç şu zincirle özetlenebilir:

$$\text{CSSOM} \rightarrow \text{Style} \rightarrow \text{Layout} \rightarrow \text{Paint} \rightarrow \text{Composite}$$

Geleneksel JavaScript çoğunlukla zincirin dışından DOM'u değiştirir. Houdini API'leri ise belirli aşamalara daha yakın çalışır. Amaç tarayıcı motorunu baştan programlamak değil; motorun izin verdiği güvenli genişletme noktalarını kullanmaktır.

| API | Görevi | Tipik kullanım |
|---|---|---|
| Properties and Values API | Özel CSS değişkenlerine tür kazandırır | Animasyonlu renk, açı ve uzunluk |
| Paint API | Bir elemanın arka planını JavaScript ile çizer | Desenler, rozetler, dekorasyonlar |
| Typed OM | CSS değerlerini metin yerine nesne olarak işler | Birim güvenli stil hesaplama |
| Layout API | Özel yerleşim algoritmaları tanımlar | Deneysel masonry veya özel grid |
| Animation Worklet | Animasyon hesaplarını iş parçacığına yaklaştırır | Kaydırmaya bağlı akıcı hareketler |

API'lerin destek düzeyleri aynı değildir. Özellikle Layout API ve Animation Worklet deneysel kalabilir; üretimde kullanmadan önce tarayıcı uyumluluğu kontrol edilmelidir.

## Türü belli özel CSS özellikleri

Normal bir CSS değişkeni metinsel bir değerdir. `CSS.registerProperty()` ile değişkenin renk, uzunluk veya sayı olduğunu tarayıcıya bildirebiliriz:

```js
CSS.registerProperty({
  name: "--vurgu",
  syntax: "<color>",
  inherits: false,
  initialValue: "#7c3aed"
});
```

Bunun ardından tarayıcı iki renk arasındaki geçişi anlayarak değişkeni akıcı biçimde animasyonlayabilir:

```css
.kart {
  --vurgu: #7c3aed;
  background: var(--vurgu);
  transition: --vurgu 400ms ease;
}

.kart:hover {
  --vurgu: #06b6d4;
}
```

Tür bilgisi olmadan tarayıcı başlangıç ve bitiş değerlerini yalnızca iki metin gibi görebilir. Tür tanımlandığında ara değer yaklaşık olarak $C(t)=(1-t)C_0+tC_1$ biçiminde hesaplanabilir.

## Paint API ile kendi fırçamızı yapmak

Paint API, Canvas benzeri bir çizim bağlamını CSS arka planında kullanmamızı sağlar. Önce worklet dosyasını kaydederiz:

```js
CSS.paintWorklet.addModule("nokta-deseni.js");
```

Worklet içinde tekrar eden noktalar çizen sınıfımızı oluştururuz:

```js
registerPaint("noktalar", class {
  static get inputProperties() {
    return ["--nokta-rengi", "--nokta-araligi"];
  }

  paint(ctx, size, properties) {
    const color = properties.get("--nokta-rengi").toString();
    const gap = parseFloat(properties.get("--nokta-araligi")) || 20;

    ctx.fillStyle = color;
    for (let x = gap / 2; x < size.width; x += gap) {
      for (let y = gap / 2; y < size.height; y += gap) {
        ctx.beginPath();
        ctx.arc(x, y, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }
});
```

Sonra çizimi sıradan bir CSS görseli gibi kullanırız:

```css
.hero {
  --nokta-rengi: rgba(255, 255, 255, 0.45);
  --nokta-araligi: 24;
  background-image: paint(noktalar);
}
```

Yaklaşık nokta sayısı $N=(w/g)(h/g)$ olduğundan aralık küçüldükçe çizim maliyeti hızla artar. Bu nedenle worklet kodu kısa tutulmalı, DOM erişimi beklenmemeli ve pahalı hesaplamalardan kaçınılmalıdır.

## Houdini ne zaman kullanılmalı?

Houdini; dinamik desenler, tasarım sistemi değişkenleri ve CSS ile bütünleşen özel görseller için etkileyicidir. Buna karşılık basit gradyanları JavaScript ile yeniden çizmek gereksiz karmaşıklık yaratır. En sağlıklı yaklaşım özellik desteğini `CSS.supports()` ile denetlemek, normal CSS ile bir yedek görünüm sunmak ve Houdini'yi aşamalı geliştirme olarak kullanmaktır. Kısacası Houdini, CSS'in yerine geçen bir büyü değil; tarayıcının fırçasını kontrollü biçimde ödünç aldığımız güçlü bir araç kutusudur.
