---
layout: post
title: "Conway Yasası: Şirket Şeması Nasıl Yazılım Mimarisine Dönüşür?"
math: true
categories: 
  - Bilgi
tags: 
  - conway yasası
  - yazılım mimarisi
  - organizasyon tasarımı
toc: true
---

Bir yazılım sisteminin mimari diyagramına bakarak onu geliştiren şirketin organizasyon şemasını tahmin edebilir misiniz? Conway Yasası’na göre çoğu zaman evet! Ekipler arasındaki iletişim sınırları; servislerin, modüllerin ve API’lerin sınırlarına dönüşür. Başka bir deyişle şirket yalnızca yazılım üretmez, kendi iletişim biçiminin dijital bir kopyasını da üretir.
``

## Conway Yasası nedir?

Bilgisayar bilimci Melvin Conway, 1967 yılında şu gözlemi ortaya koydu: Bir sistem tasarlayan organizasyonlar, kendi iletişim yapılarını yansıtan tasarımlar üretmeye eğilimlidir. Buradaki “iletişim yapısı” yalnızca kimin kime e-posta gönderdiği değildir. Ekiplerin sorumlulukları, yöneticiler arasındaki sınırlar, toplantı alışkanlıkları ve hatta farklı ofislerin saat dilimleri bile mimariyi etkiler.

Bu ilişkiyi basitleştirerek şöyle gösterebiliriz:

$$
M \approx f(O, I, S)
$$

Burada $M$ yazılım mimarisini, $O$ organizasyon yapısını, $I$ ekipler arasındaki iletişim yoğunluğunu, $S$ ise sorumluluk sınırlarını temsil eder. İletişimi güçlü ekiplerin geliştirdiği parçalar daha sıkı bütünleşirken, nadiren konuşan ekiplerin bileşenleri belirgin arayüzlerle ayrılma eğilimindedir.

Örneğin kullanıcı arayüzü, ödeme ve lojistik ekiplerinden oluşan bir e-ticaret şirketi düşünelim. Bu yapı zamanla üç ayrı servise dönüşebilir. Bu mutlaka kötü değildir; ancak servis sınırları teknik ihtiyaçlardan çok departman sınırlarına göre çizildiyse gereksiz ağ çağrıları ve veri tutarsızlıkları ortaya çıkabilir.

| Organizasyon yapısı | Muhtemel mimari sonucu | Olası risk |
|---|---|---|
| Tek, büyük geliştirme ekibi | Monolitik uygulama | Sıkı bağımlılık |
| Bağımsız ürün ekipleri | Mikroservisler | Servis ve operasyon yükü |
| Frontend ve backend ayrımı | Katmanlı mimari | Teslimat için ekipler arası bekleme |
| Coğrafi olarak dağınık ekipler | Mesajlaşma ve asenkron süreçler | Gecikmeli geri bildirim |

## Kodda organizasyon izleri

Bir sipariş servisinin ödeme ekibine ait servisi HTTP üzerinden çağırdığını düşünelim:

```javascript
async function siparisOlustur(sepet) {
  const odeme = await fetch("http://odeme-servisi/tahsilat", {
    method: "POST",
    body: JSON.stringify({ tutar: sepet.toplam })
  });

  if (!odeme.ok) throw new Error("Ödeme tamamlanamadı");
  return siparisDeposu.kaydet(sepet);
}
```

Bu kod yalnızca teknik bir tercih değildir. Sipariş ve ödeme sorumluluklarının farklı ekiplerde bulunduğunu da ima eder. HTTP arayüzü, iki ekip arasındaki iletişim sözleşmesinin çalışan karşılığıdır. Ödeme ekibi API’yi haber vermeden değiştirirse yalnızca kod değil, ekipler arası güven de kırılır.

## Conway Yasası neden “kaçınılmaz” görünür?

Bir geliştirici, başka bir ekibin koduna kolayca katkıda bulunamıyorsa kendi kontrolünde yeni bir bileşen oluşturmayı tercih eder. Yönetim bütçeyi departmanlara göre dağıtıyorsa teknik sahiplik de aynı çizgileri izler. Böylece organizasyonel mesafe arttıkça bileşenler arasındaki mesafe de büyür.

Bunu sezgisel olarak şöyle ifade edebiliriz:

$$
Bileşen\ Ayrılığı \propto İletişim\ Maliyeti
$$

İletişim maliyeti yükseldikçe ortak modül geliştirmek zorlaşır; ekipler API, kuyruk veya ayrı veri tabanı gibi daha sert sınırlar kurar.

## Ters Conway manevrası

Conway Yasası yalnızca teşhis aracı değildir. “Ters Conway manevrası”, hedeflenen mimariye uygun ekip yapısını bilinçli biçimde tasarlamaktır. Bağımsız mikroservisler isteniyorsa ekiplerin de geliştirme, test, dağıtım ve gözlemleme yetkilerine sahip olması gerekir. Aksi hâlde “bağımsız servisler”, dağıtım için beş farklı departmandan onay bekler.

İyi bir yaklaşım, ekipleri teknik katmanlar yerine iş yetenekleri etrafında kurmaktır. Örneğin ayrı frontend, backend ve veri tabanı ekipleri yerine ödeme deneyiminin tamamından sorumlu çapraz fonksiyonlu bir ekip oluşturulabilir.

Sonuç olarak mimari kararlar yalnızca teknoloji seçimi değildir. İletişim kanalları, yetki sınırları ve ekip sahipliği de sistem tasarımının parçalarıdır. Bir sonraki mimari problemi incelerken yalnızca kod deposuna değil, toplantı takvimine de bakın; hatanın kaynağı bazen sınıflarda değil, organizasyon şemasındadır.
