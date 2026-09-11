---
layout: post
title: "Arama Motorlarının Kronometresi: Core Web Vitals Metriklerinin Kodsal Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - core web vitals
  - web performansı
  - seo
toc: true
---

Modern arama motorları bir web sayfasını yalnızca anahtar kelimelerine göre değerlendirmiyor; kullanıcının sayfayı ne kadar hızlı gördüğünü, etkileşim sırasında ne kadar beklediğini ve içeriklerin ekranda zıplayıp zıplamadığını da ölçüyor. Google’ın Core Web Vitals yaklaşımı, soyut görünen “iyi kullanıcı deneyimini” LCP, INP ve CLS gibi sayısal göstergelere dönüştürüyor. Böylece performans optimizasyonu, “Bende hızlı açılıyor!” yorumundan çıkıp ölçülebilir bir yazılım kalitesi problemine dönüşüyor.
``

## Üç temel performans sinyali

Core Web Vitals ailesinin güncel üçlüsü **Largest Contentful Paint (LCP)**, **Interaction to Next Paint (INP)** ve **Cumulative Layout Shift (CLS)** metriklerinden oluşur. Eski kaynaklarda görülen FID, yalnızca ilk etkileşimin gecikmesini ölçüyordu; INP ise sayfanın yaşam döngüsündeki etkileşimleri inceleyerek daha kapsamlı bir tepki süresi sunar.

| Metrik | Ölçtüğü deneyim | İyi | Geliştirilmeli | Zayıf |
|---|---|---:|---:|---:|
| LCP | Ana içeriğin görünme süresi | ≤ 2,5 sn | ≤ 4 sn | > 4 sn |
| INP | Etkileşimden sonraki görsel tepki | ≤ 200 ms | ≤ 500 ms | > 500 ms |
| CLS | Beklenmeyen görsel kayma | ≤ 0,1 | ≤ 0,25 | > 0,25 |

LCP çoğunlukla büyük bir kahraman görseli, afiş veya başlık bloğu tarafından belirlenir. Değer kabaca kaynak edinme ve çizim aşamalarının toplamıdır:

$$LCP = TTFB + kaynak\ gecikmesi + indirme\ süresi + çizim\ gecikmesi$$

Bu nedenle yalnızca görseli sıkıştırmak yeterli olmayabilir. Sunucu yanıtı, önceliklendirme ve ana iş parçacığının yoğunluğu da sonucu etkiler.

## CLS neden boyutsuzdur?

CLS saniye değil, görsel kararsızlığı ifade eden boyutsuz bir puandır. Her beklenmeyen kayma için yaklaşık olarak şu ilişki kullanılır:

$$Kayma\ Puanı = Etki\ Oranı \times Mesafe\ Oranı$$

Boyutları belirtilmemiş bir görsel yüklendiğinde aşağıdaki içerik aşağı itilebilir. Tarayıcıya alanı önceden ayırmak basit ama etkili bir çözümdür:

```html
<img
  src='urun.webp'
  width='1200'
  height='675'
  loading='lazy'
  alt='Yeni ürünün tanıtım görseli'>
```

`width` ve `height`, görsel indirilmeden en-boy oranının hesaplanmasını sağlar. Reklam, gömülü video ve sonradan eklenen bildirim alanlarında da sabit alan veya `aspect-ratio` kullanılmalıdır.

## Metrikleri tarayıcıda yakalamak

`PerformanceObserver`, tarayıcının performans girdilerini uygulama içinde izlememize yardımcı olur. Aşağıdaki örnek LCP değerini ve oturumdaki beklenmeyen kaymaları toplar:

```javascript
let cls = 0;

new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries.at(-1);
  console.log('LCP:', lastEntry.startTime, 'ms');
}).observe({ type: 'largest-contentful-paint', buffered: true });

new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) cls += entry.value;
  }
  console.log('CLS:', cls.toFixed(3));
}).observe({ type: 'layout-shift', buffered: true });
```

`buffered: true`, gözlemci kurulmadan önce oluşmuş kayıtların da alınmasını sağlar. `hadRecentInput` kontrolü ise kullanıcının bilinçli eylemiyle meydana gelen kaymaları puan dışında bırakır.

## Yazılım kalitesini derecelendirmek

Metrikleri tek bir iç puana dönüştürmek, sürümler arasında karşılaştırma yapmayı kolaylaştırabilir. Ancak bu puan, arama motorunun resmî sıralama formülü değildir:

```javascript
function qualityScore({ lcp, inp, cls }) {
  const lcpScore = Math.max(0, 100 - (lcp / 2500) * 40);
  const inpScore = Math.max(0, 100 - (inp / 200) * 40);
  const clsScore = Math.max(0, 100 - (cls / 0.1) * 40);

  return Math.round(
    lcpScore * 0.4 + inpScore * 0.4 + clsScore * 0.2
  );
}
```

Ağırlıklar ürünün ihtiyaçlarına göre değiştirilebilir. Bir çizim uygulamasında INP, haber sitesinde ise LCP daha kritik olabilir.

Son olarak laboratuvar testleri ile gerçek kullanıcı verilerini ayırmak gerekir. Lighthouse kontrollü koşullarda teşhis sunarken Chrome User Experience Report gerçek ziyaretçilerin saha verilerini toplar. En sağlıklı süreç; saha verisiyle problemi bulmak, profil araçlarıyla nedenini araştırmak ve performans bütçesini CI/CD hattında otomatik denetlemektir. Hız artık sonradan sürülen cila değil, doğrudan mimari bir kalite özelliğidir.
