---
layout: post
title: "PWA ve Service Worker ile Çevrimdışı Önbellek Stratejileri"
math: true
categories: 
  - Bilgi
tags: 
  - pwa
  - service-worker
  - önbellek
  - javascript
  - çevrimdışı
  - web-performansı
toc: true
image: /img/pwa-ve-service-57.png
---

Bir web sitesini uçakta, metroda veya internetin naz yaptığı bir kafede açtığınızı düşünün. Normalde tarayıcı üzgün bir hata sayfası gösterirken Progressive Web App, yani PWA, daha önce kaydedilmiş kaynakları kullanarak çalışmaya devam edebilir. Bu küçük sihrin arkasında, tarayıcı ile ağ arasında görev yapan **Service Worker** bulunur.

``

## PWA ve Service Worker mantığı

PWA; web teknolojileriyle geliştirilen, kurulabilen, hızlı açılan ve çevrimdışı deneyim sunabilen uygulamadır. Manifest dosyası uygulamanın adı, simgesi ve görünümü gibi bilgileri tanımlarken Service Worker ağ isteklerini yönetir.

Service Worker, sayfanın JavaScript sürecinden ayrı çalışan olay tabanlı bir arka plan betiğidir. DOM'a doğrudan erişemez; ancak `fetch`, `install`, `activate` ve bildirim olaylarını dinleyebilir. Güvenlik nedeniyle HTTPS gerektirir; geliştirme sırasında `localhost` istisnadır.

Temel yaşam döngüsü şöyledir:

1. **Register:** Sayfa Service Worker dosyasını kaydeder.
2. **Install:** Statik kaynaklar önbelleğe alınır.
3. **Activate:** Eski önbellek sürümleri temizlenir.
4. **Fetch:** İsteklerin ağdan mı, önbellekten mi karşılanacağı belirlenir.

Bir kaynağın ortalama yanıt süresini kabaca şöyle modelleyebiliriz:

$$T_{ortalama} = p_c T_{cache} + (1-p_c)T_{network}$$

Burada $p_c$ önbellekte bulunma olasılığıdır. $T_{cache}$ çoğunlukla ağ süresinden küçük olduğu için isabet oranı yükseldikçe uygulama hızlanır.

## Stratejiler karşı karşıya

| Strateji | Öncelik | Avantaj | Uygun kullanım |
|---|---|---|---|
| Cache First | Önbellek | Çok hızlı ve çevrimdışı çalışır | Logo, font, CSS |
| Network First | Ağ | Güncel veri sunar | Haberler, kullanıcı paneli |
| Stale-While-Revalidate | Önbellek + arka plan güncelleme | Hız ve güncellik dengesi | Ürün listeleri, avatarlar |
| Cache Only | Yalnız önbellek | Ağ isteği oluşturmaz | Uygulama kabuğu |
| Network Only | Yalnız ağ | Daima sunucuya gider | Ödeme ve anlık işlemler |

![pwa-ve-service-57](/img/pwa-ve-service-57.svg)


**Cache First**, önce depoya bakar; kaynak yoksa ağa gider. Dosya adlarında içerik karması kullanılan `app.a81f.css` gibi statik varlıklar için idealdir. **Network First** önce sunucuyu dener, bağlantı başarısızsa önbelleğe döner. Güncelliğin önemli olduğu içeriklerde daha güvenlidir.

**Stale-While-Revalidate** ise kullanıcıya önbellekteki sürümü hemen verirken ağdan yeni sürümü indirip sonraki ziyaret için saklar. Kullanıcı beklemez, içerik de zamanla tazelenir. Adındaki “stale”, gösterilen verinin kısa süreliğine eski olabileceğini anlatır.

## Uygulamalı Service Worker

Önce Service Worker'ı sayfada kaydedelim:

```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

Ardından `sw.js` içinde Stale-While-Revalidate stratejisini kurabiliriz:

```javascript
const CACHE = 'site-v1';

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.open(CACHE).then(async cache => {
      const cached = await cache.match(event.request);

      const update = fetch(event.request).then(response => {
        if (response.ok && event.request.method === 'GET') {
          cache.put(event.request, response.clone());
        }
        return response;
      });

      return cached || update;
    })
  );
});
```

Kod önce eşleşen kaynağı arar. Önbellek kaydı varsa onu anında döndürür; `fetch` işlemi arka planda güncel yanıtı getirerek depolar. `response.clone()` gereklidir, çünkü yanıt gövdesi yalnızca bir kez okunabilen bir akıştır.

## Dikkat edilmesi gerekenler

Önbelleği sınırsız büyütmek yerine sürümleme ve temizleme uygulanmalıdır. HTML için Network First, görseller için Stale-While-Revalidate, parmak izi eklenmiş statik dosyalar için Cache First tercih edilebilir. Hassas API yanıtlarını ve kişisel verileri gelişigüzel saklamak ciddi güvenlik sorunları doğurur.

Sonuç olarak tek bir “en iyi” strateji yoktur. Başarılı bir PWA, her kaynak türünün güncellik, hız ve çevrimdışı erişim ihtiyacını değerlendirir. Service Worker doğru kurgulandığında web sitesi yalnızca hızlı görünmez; internet ortadan kaybolduğunda bile işini sürdüren dayanıklı bir uygulamaya dönüşür.
