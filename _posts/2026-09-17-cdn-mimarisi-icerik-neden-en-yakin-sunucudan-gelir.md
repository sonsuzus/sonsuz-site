---
layout: post
title: "CDN Mimarisi: İçerik Neden En Yakın Sunucudan Gelir?"
math: true
categories: 
  - Bilgi
tags: 
  - cdn
  - web performansı
  - ağ mimarisi
  - önbellekleme
  - dns
  - anycast
toc: true
image: /img/cdn-mimarisi-icerik-74.png
---

Bir web sitesini açtığınızda görsellerin, videoların ve JavaScript dosyalarının kıtalar arası uzun bir yolculuğa çıkmasını istemezsiniz. CDN, yani İçerik Dağıtım Ağı, popüler içerikleri dünyanın farklı bölgelerindeki sunuculara kopyalayarak kullanıcıya yakın bir noktadan teslim eder. Ancak buradaki “yakınlık” yalnızca kilometre hesabı değildir; ağ gecikmesi, yönlendirme kalitesi, sunucu yükü ve erişilebilirlik de seçimi etkiler.


![cdn-mimarisi-icerik-74](/img/cdn-mimarisi-icerik-74.svg)

``

## CDN hangi problemi çözer?

Ana sunucunuzun İstanbul’da, ziyaretçinizin ise Tokyo’da olduğunu düşünün. CDN kullanılmadığında istek çok sayıda yönlendiriciden geçerek İstanbul’a ulaşır ve cevap aynı ağ yolundan geri döner. Her durak küçük bir gecikme ekler. Üstelik okyanus geçmek, ışık hızında bile sıfır zaman almaz.

Yaklaşık aktarım süresini şöyle modelleyebiliriz:

$$
T_{toplam} = T_{RTT} + T_{sunucu} + T_{aktarım}
$$

Burada $T_{RTT}$ isteğin hedefe gidip ilk cevabın geri gelme süresi, $T_{sunucu}$ içeriğin hazırlanma süresi, $T_{aktarım}$ ise verinin indirilme süresidir. CDN özellikle $T_{RTT}$ değerini düşürür ve önbellek sayesinde sunucu işlem süresini azaltabilir.

| Özellik | Doğrudan ana sunucu | CDN üzerinden |
|---|---|---|
| Fiziksel mesafe | Genellikle daha uzun | Çoğunlukla daha kısa |
| Gecikme | Bölgeye göre yüksek | Daha düşük ve dengeli |
| Ana sunucu yükü | Tüm istekleri karşılar | İsteklerin çoğu dağıtılır |
| Trafik sıçramaları | Risk oluşturabilir | Birçok noktaya yayılır |
| Arıza dayanıklılığı | Tek merkeze bağımlı | Alternatif noktalar bulunabilir |

## “En yakın” sunucu nasıl seçilir?

CDN sağlayıcıları dünya çapındaki veri merkezlerinde **PoP** (Point of Presence) adı verilen erişim noktaları çalıştırır. Kullanıcının isteği genellikle iki yöntemden biriyle uygun PoP’a yönlendirilir.

**GeoDNS**, kullanıcının DNS sorgusunu inceleyerek tahmini konuma uygun bir IP adresi döndürür. Örneğin Ankara’daki kullanıcı Avrupa veya Türkiye’deki bir noktaya, Sydney’deki kullanıcı Avustralya’daki bir noktaya yönlendirilebilir.

**Anycast** yönteminde ise birçok veri merkezi aynı IP adresini duyurur. İnternetin yönlendirme protokolü BGP, isteği ağ açısından en uygun rotaya taşır. Böylece kullanıcı aynı IP’ye bağlandığını düşünürken trafik farklı şehirlerdeki sunuculara ulaşabilir.

Bu nedenle en yakın sunucu her zaman coğrafi olarak en yakın değildir. Yan binadaki veri merkezinin bağlantısı yoğunken 300 kilometre uzaktaki bir PoP daha hızlı olabilir. CDN sistemi gecikme ölçümleri, paket kaybı, kapasite ve sağlık kontrolleriyle kararını günceller.

## Cache hit ve cache miss

İstek seçilen PoP’a ulaştığında içerik önbellekte aranır. Dosya bulunursa buna **cache hit** denir ve cevap hemen kullanıcıya gönderilir. Bulunamazsa **cache miss** oluşur; PoP dosyayı origin adı verilen ana sunucudan alır, kullanıcıya iletir ve sonraki istekler için saklar.

$$
Hit\ Ratio = \frac{Cache\ Hit}{Toplam\ İstek} \times 100
$$

Yüksek hit oranı genellikle daha hızlı yanıt ve daha düşük origin maliyeti anlamına gelir. Önbellek davranışı HTTP başlıklarıyla yönetilebilir:

```http
Cache-Control: public, max-age=3600, s-maxage=86400
```

Bu örnek, tarayıcının içeriği bir saat; paylaşımlı CDN önbelleğinin ise bir gün saklayabileceğini belirtir. Sık değişen HTML sayfalarında daha kısa, sürümlenmiş görsellerde ve JavaScript dosyalarında daha uzun süreler kullanılabilir.

## CDN yalnızca hız değildir

Modern CDN’ler TLS sonlandırma, DDoS koruması, bot filtreleme, görsel optimizasyonu ve edge computing gibi görevler de üstlenir. Dinamik içerik tamamen önbelleğe alınamasa bile bağlantının kullanıcıya yakın noktada kurulması ve origin’e optimize edilmiş hatların kullanılması performansı artırabilir.

Kısacası CDN, internetin stratejik noktalara yerleştirilmiş mahalle depoları gibidir. Ürün uzaktaki fabrikadan her siparişte yeniden gelmez; yakındaki depoda varsa hızla teslim edilir. Sonuç daha düşük gecikme, daha az ana sunucu yükü ve yoğun trafikte bile daha mutlu kullanıcılardır.
