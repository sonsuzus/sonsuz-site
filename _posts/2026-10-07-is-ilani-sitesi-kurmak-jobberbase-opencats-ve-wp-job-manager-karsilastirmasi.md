---
layout: post
title: "İş İlanı Sitesi Kurmak: Jobberbase, OpenCATS ve WP Job Manager Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - iş ilanı sitesi
  - jobberbase
  - opencats
  - wordpress
  - wp job manager
  - açık kaynak
toc: true
image: /img/is-ilani-sitesi-83.png
---

Bir iş ilanı sitesi kurmak, yalnızca ilan başlığı ve “Başvur” düğmesi yerleştirmekten ibaret değildir. İşveren yönetimi, aday takibi, arama, yetkilendirme ve veri güvenliği gibi parçalar da sistemin omurgasını oluşturur. Bu noktada Jobberbase, OpenCATS ve WP Job Manager farklı ihtiyaçlara hitap eden üç güçlü seçenek olarak karşımıza çıkar.

``

## Önce temel modeli anlayalım

İş ilanı platformlarında genellikle üç ana aktör bulunur: ziyaretçi, aday ve işveren. Daha kapsamlı sistemlerde bunlara insan kaynakları uzmanı ile yönetici rolleri de eklenir. En basit veri ilişkisi şöyle ifade edilebilir:

$$
İşveren \rightarrow İlan \rightarrow Başvuru \leftarrow Aday
$$

Bir platformun gerçek maliyetini hesaplarken yalnızca kurulum ücretine bakmak yanıltıcıdır. Daha doğru bir yaklaşım şudur:

$$
TCO = K + Ö + B + E
$$

Burada $TCO$ toplam sahip olma maliyetini, $K$ kurulum ve geliştirmeyi, $Ö$ özelleştirmeyi, $B$ bakımı, $E$ ise eklenti ve altyapı giderlerini temsil eder. “Ücretsiz yazılım” bazen bolca geliştirici kahvesi gerektirebilir!

## Üç çözümün kısa karşılaştırması

| Özellik | Jobberbase | OpenCATS | WP Job Manager |
|---|---|---|---|
| Temel amaç | Sade iş ilanı panosu | Aday takip sistemi | WordPress tabanlı ilan sitesi |
| Kurulum kolaylığı | Orta | Orta-zor | Kolay |
| Aday takibi | Sınırlı | Güçlü | Eklentilere bağlı |
| Tema ve tasarım | Eski, özelleştirilebilir | Yönetim odaklı | Çok geniş seçenek |
| Ekosistem | Küçük | Niş | Çok büyük |
| Uygun kullanıcı | Teknik ekip | İK departmanı | Girişimci ve ajans |

## Jobberbase: Sadelik arayanlara

Jobberbase, klasik bir açık kaynak iş ilanı panosudur. İlan yayınlama, kategori oluşturma ve konuma göre listeleme gibi temel işlevleri sunar. Kod tabanı üzerinde çalışabilen bir geliştiriciniz varsa yalın bir ürün ortaya çıkarabilirsiniz.

Ancak projenin yaşı önemli bir dezavantajdır. Modern PHP sürümleri, güvenlik beklentileri ve mobil tasarım için ek çalışma gerekebilir. Jobberbase’i hazır bir ürün yerine geliştirilecek bir başlangıç iskeleti olarak değerlendirmek daha gerçekçidir.

## OpenCATS: İlan sitesinden fazlası

OpenCATS, doğrudan ilan panosundan çok bir **ATS**, yani Applicant Tracking System’dır. Adayların özgeçmişlerini saklama, görüşme süreçlerini izleme, not ekleme ve pozisyonlarla adayları eşleştirme özellikleri sunar.

Bu nedenle amaç yalnızca halka açık ilan yayınlamaksa arayüzü gereğinden karmaşık gelebilir. Buna karşılık işe alım ekibiniz onlarca pozisyon ve yüzlerce aday yönetiyorsa OpenCATS çok daha anlamlıdır. Kısacası Jobberbase vitrinken OpenCATS mutfaktır; tabakların nerede olduğunu bile takip eder.

## WP Job Manager: WordPress gücü

WP Job Manager, mevcut bir WordPress sitesine iş ilanı özellikleri ekleyen modüler bir eklentidir. Kısa kodlar ve bloklar sayesinde ilan listeleri, gönderim formları ve işveren panelleri hazırlanabilir.

Örneğin ilan listesini bir sayfaya eklemek oldukça kolaydır:

```text
[jobs location="İstanbul" keywords="PHP"]
```

Bu kısa kod, İstanbul konumundaki ve PHP anahtar kelimesiyle ilişkili ilanları filtreleyerek gösterir. Özgeçmiş yönetimi, ücretli ilanlar ve başvuru akışları için ek eklentiler gerekebilir. Bu durum maliyeti artırsa da WordPress’in tema, SEO ve ödeme altyapısı seçenekleri büyük esneklik sağlar.

## Hangisini seçmelisiniz?

- Minimal, geliştirici kontrolünde bir ilan panosu istiyorsanız **Jobberbase** düşünülebilir.
- Şirket içi işe alım ve aday süreçleri öncelikliyse **OpenCATS** daha uygundur.
- Hızlı kurulum, modern tasarım, SEO ve gelir modeli hedefleniyorsa **WP Job Manager** öne çıkar.

Yeni başlayacak çoğu proje için WP Job Manager en pratik seçimdir. OpenCATS operasyonel derinlik, Jobberbase ise kod üzerinde tam kontrol isteyen ekipler için değerlidir. Son karardan önce bakım sıklığını, güvenlik güncellemelerini ve ihtiyaç duyacağınız eklentileri test ortamında incelemek, ileride “Bu başvuru nereye kayboldu?” gizemlerini önemli ölçüde azaltır.

![is-ilani-sitesi-83](/img/is-ilani-sitesi-83.svg)

