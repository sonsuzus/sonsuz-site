---
layout: post
title: "Flarum Forumlarında SPA Mimarisi: Mithril.js ile Yenilenmeden Akan Sayfalar"
math: true
categories: 
  - Bilgi
tags: 
  - flarum
  - spa
  - mithril.js
toc: true
---

Bir Flarum forumunda tartışmadan kullanıcı profiline geçtiğinizde tarayıcının klasik anlamda yeniden yüklenmediğini fark etmiş olabilirsiniz. Adres değişir, yeni içerik gelir, kaydırma davranışı düzenlenir; fakat sayfanın tamamı baştan kurulmaz. Bu akıcı deneyimin arkasında, Flarum’un Mithril.js tabanlı **Single Page Application (SPA)** mimarisi bulunur. Gelin bu yapının kaputunu açıp isteklerden bileşen yaşam döngüsüne kadar neler döndüğüne bakalım.
``

## SPA yaklaşımı neyi değiştiriyor?

Geleneksel çok sayfalı uygulamalarda her bağlantı, sunucudan yeni bir HTML belgesi ister. SPA mimarisinde ise ilk istekte uygulamanın ana kabuğu, JavaScript dosyaları ve temel stiller yüklenir. Sonraki gezinmelerde tarayıcı çoğunlukla JSON verisi alır; Mithril sanal DOM üzerinden yalnızca değişmesi gereken arayüz parçalarını günceller.

| Özellik | Geleneksel forum | Flarum SPA |
|---|---|---|
| Sayfa geçişi | Tam HTML yenilemesi | İstemci taraflı rota değişimi |
| Veri taşıma | HTML ağırlıklı | JSON:API yanıtları |
| Arayüz güncelleme | Belgenin tamamı | Değişen bileşenler |
| Kullanıcı hissi | Kesintili | Akıcı ve uygulama benzeri |

Basitleştirilmiş maliyet modelini şöyle ifade edebiliriz:

$$T_{klasik}=T_{HTML}+T_{CSS}+T_{JS}+T_{render}$$

$$T_{SPA}=T_{API}+T_{diff}+T_{patch}$$

İlk SPA yüklemesi pahalı olabilse de sonraki geçişlerde ortak kaynaklar yeniden indirilmediğinden toplam süre genellikle azalır.

## Mithril.js neden mimarinin merkezinde?

Mithril.js; yönlendirme, HTTP istekleri, bileşen sistemi ve sanal DOM özelliklerini küçük bir çekirdekte birleştirir. Flarum’un ön yüzü de `ForumApplication`, sayfalar, bileşenler ve modeller etrafında şekillenir. Bir rota değiştiğinde ilgili sayfa bileşeni oluşturulur, gerekli veri API’den alınır ve Mithril yeniden çizim sürecini yönetir.

Basit bir Mithril bileşeni şu şekilde düşünülebilir:

```javascript
const DiscussionSummary = {
  view(vnode) {
    const discussion = vnode.attrs.discussion;

    return m('button', {
      onclick: () => m.route.set('/d/' + discussion.id())
    }, discussion.title());
  }
};
```

Bu bileşen bir tartışma başlığı üretir. Tıklama sırasında klasik bağlantıyla tam yenileme yapmak yerine `m.route.set` istemci rotasını değiştirir. Flarum’un gerçek kodunda rota üretimi, model erişimi ve bağlantı bileşenleri daha kapsamlıdır; temel mantık ise aynıdır.

## Veri akışı: API’den modele, modelden ekrana

Flarum arka ucu verileri JSON:API biçiminde sunar. İstemci tarafındaki mağaza, gelen kayıtları model nesnelerine dönüştürür ve kimlikleri üzerinden saklar. Böylece aynı kullanıcı veya tartışma farklı bileşenlerde gerektiğinde mevcut model tekrar kullanılabilir.

Genel akış şöyledir:

1. Kullanıcı bir bağlantıya tıklar.
2. Mithril yönlendiricisi yeni rotayı çözümler.
3. Sayfa bileşeni gerekli kaynağı Flarum API’sinden ister.
4. Yanıt istemci mağazasına kaydedilir.
5. Mithril yeniden çizim yaparak görünümü günceller.

Bu yaklaşım ağ trafiğini tamamen ortadan kaldırmaz; onu daha hedefli hâle getirir. Örneğin bir tartışma açılırken tüm forum ana sayfası yerine tartışma, gönderiler ve ilişkili kullanıcılar alınabilir.

## Yaşam döngüsü ve yeniden çizim

Mithril bileşenleri `oninit`, `oncreate`, `onupdate` ve `onremove` gibi yaşam döngüsü metotlarına sahiptir. Flarum uzantıları bu noktalardan yararlanarak veri yükleyebilir veya üçüncü taraf arayüzlerini güvenli biçimde başlatabilir.

```javascript
const OnlineBadge = {
  oninit(vnode) {
    vnode.state.loading = true;
    app.store.find('users', vnode.attrs.userId)
      .finally(() => {
        vnode.state.loading = false;
        m.redraw();
      });
  },

  view(vnode) {
    return vnode.state.loading ? m('span', 'Kontrol ediliyor…') : m('span', 'Hazır');
  }
};
```

Burada veri isteği tamamlandığında `m.redraw()` görünümün güncellenmesini sağlar. Ancak gereksiz manuel yeniden çizimler performansı düşürebileceğinden, Mithril’in otomatik çizim davranışına öncelik verilmelidir.

## Güçlü taraflar ve mimari bedeller

SPA mimarisi hızlı geçişler, yeniden kullanılabilir bileşenler ve zengin etkileşimler sağlar. Buna karşılık durum yönetimi, geri tuşu davranışı, yükleniyor göstergeleri, hata senaryoları ve SEO daha dikkatli tasarlanmalıdır. Flarum bu karmaşıklığı rota sistemi, merkezi mağaza, JSON:API ve genişletilebilir bileşen yapısıyla dengeler.

Sonuç olarak Flarum, yalnızca sayfaları hızlandıran bir JavaScript katmanı kullanmaz; sunucu verisi ile istemci görünümünü birbirinden ayıran bütüncül bir mimari kurar. Mithril.js ise bu orkestrada rotaları, bileşenleri ve ekran güncellemelerini yöneten küçük ama etkili bir şeftir.
