---
layout: post
title: "CDN Çalışma Mantığı: İçeriği Dünyaya Yakınlaştıran Ağ"
math: true
categories: 
  - Bilgi
tags: 
  - cdn
  - web performansı
  - ağ teknolojileri
toc: true
image: /img/cdn-calisma-mantigi-51.png
---

Bir web sitesi yalnızca güzel tasarımdan ibaret değildir; ziyaretçi Tokyo'dayken sunucunuz İstanbul'da bulunuyorsa, aradaki fiziksel mesafe sayfanın açılışını yavaşlatır. CDN (Content Delivery Network / İçerik Dağıtım Ağı), görsel, JavaScript, CSS, video ve hatta önbelleğe alınabilir API yanıtlarını kullanıcıya en yakın noktadan ulaştıran küresel bir sunucu ağıdır. Temel hedef basittir: veriyi uzun bir kıtalararası yolculuğa çıkarmak yerine, ona mahalleden servis yapmaktır.
``

CDN'in arkasındaki ana fikir **edge computing** yaklaşımının hafif bir versiyonudur. Asıl içeriğin bulunduğu merkezi sunucuya **origin** denir. CDN sağlayıcısının farklı şehir ve ülkelerde konumlanan sunucuları ise **edge** ya da PoP (Point of Presence) olarak adlandırılır. Bir kullanıcı sayfayı istediğinde DNS yönlendirmesi, Anycast ağ yapısı ve gecikme ölçümleri birlikte çalışarak en uygun edge noktasını seçer.

Gecikmenin kaba modeli şu şekilde düşünülebilir:

$$T_{toplam} = T_{DNS} + T_{bağlantı} + T_{sunucu} + T_{aktarim}$$

Burada en pahalı kalem çoğu zaman uzak sunucuya gidiş-dönüş süresidir (RTT). Fiber kablodaki sinyal ışık hızına yakın ilerlese bile yönlendirme cihazları, yoğunluk ve fiziksel mesafe ek süre üretir. CDN, özellikle $T_{bağlantı}$ ve RTT kısmını küçülterek kullanıcı deneyimini iyileştirir.

## İstek geldiğinde neler olur?

Örneğin tarayıcı `site.com/logo.png` için istek gönderir. Alan adı CDN'e yönlendirilmişse edge sunucu önce kendi önbelleğine bakar. Dosya varsa buna **cache hit** denir ve dosya hemen döner. Yoksa **cache miss** gerçekleşir; edge, origin sunucudan dosyayı alır, belirlenen kurallara göre önbelleğe yazar ve kullanıcıya iletir. Sonraki yakın kullanıcılar aynı dosyayı çok daha hızlı alır.

| Durum | İsteğin kaynağı | Sonuç |
|---|---|---|
| Cache hit | Yakındaki edge sunucu | Düşük gecikme, origin yükü azalır |
| Cache miss | Origin sunucu | İlk istek daha yavaş, içerik edge'e kaydedilir |
| Expired cache | Origin veya doğrulama isteği | Güncel içerik kontrol edilir |

Önbelleğin ne kadar yaşayacağını genellikle HTTP başlıkları belirler. Örneğin aşağıdaki ayar, tarayıcı ve CDN'in görseli bir yıl saklamasına izin verir:

```http
Cache-Control: public, max-age=31536000, immutable
ETag: "logo-v42"
```

`max-age` saniye cinsinden ömrü tanımlar. `immutable`, dosyanın bu süre boyunca değişmeyeceğini söyler. Bu nedenle sürüm numaralı dosya adları (`app.8f3a.js` gibi) CDN stratejilerinde çok değerlidir: Yeni sürüm yeni URL ile gelir, eski sürüm ise güvenle uzun süre saklanabilir.

## CDN yalnızca hız değildir

CDN origin sunucunun üzerindeki trafik baskısını azaltır. Binlerce kişi aynı kampanya görselini açtığında, origin yerine yüzlerce edge noktası cevap verir. Bu dağıtım DDoS saldırılarının emilmesine, TLS bağlantılarının kullanıcıya yakın noktada sonlandırılmasına ve Web Application Firewall kurallarının uygulanmasına da yardımcı olur.

| Özellik | CDN olmadan | CDN ile |
|---|---|---|
| Statik dosya gecikmesi | Kullanıcı-origin mesafesine bağlı | En yakın edge üzerinden daha düşük |
| Origin yükü | Her istekte artar | Önbellek hit'leriyle azalır |
| Trafik patlaması | Tek merkez zorlanabilir | Küresel ağ paylaşır |
| Güvenlik katmanı | Uygulama önünde sınırlı | WAF, rate limit, DDoS koruması eklenebilir |

Ancak her şey otomatik değildir. Giriş yapmış kullanıcıya özel sayfaları yanlışlıkla önbelleğe almak güvenlik sorununa yol açabilir. `Set-Cookie` içeren cevaplar, kişisel API verileri ve yönetim ekranları çoğunlukla `private` veya `no-store` politikasıyla CDN önbelleğinin dışında tutulmalıdır.

Özetle CDN bir dosya deposu değil, akıllı bir dağıtım ve önbellekleme katmanıdır. Doğru cache başlıkları, sürümlenmiş statik dosyalar ve dikkatli dinamik içerik kurallarıyla, siteniz ziyaretçiye nerede olursa olsun daha yakın hissedilir.

![cdn-calisma-mantigi-51](/img/cdn-calisma-mantigi-51.svg)

