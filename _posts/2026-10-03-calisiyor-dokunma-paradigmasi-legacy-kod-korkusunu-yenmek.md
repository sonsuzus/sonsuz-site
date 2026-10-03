---
layout: post
title: "Çalışıyor, Dokunma! Paradigması: Legacy Kod Korkusunu Yenmek"
math: true
categories: 
  - Bilgi
tags: 
  - legacy kod
  - teknik borç
  - yazılım testi
  - refactoring
  - risk yönetimi
  - yazılım mimarisi
toc: true
image: /img/calisiyor-dokunma-paradigmasi-44.png
---

![calisiyor-dokunma-paradigmasi-44](/img/calisiyor-dokunma-paradigmasi-44.svg)


Bir şirketin en kritik sistemi bazen modern bulut servislerinde değil, kimsenin tam olarak anlamadığı eski bir sunucuda yaşar. Faturaları hesaplar, siparişleri işler ve maaşları yatırır; fakat ona dokunmak yasaktır. Çünkü kodu yazan ekip çoktan ayrılmış, belgeler kaybolmuş ve testler hiç yazılmamıştır. Sistem çalışıyordur ama bu huzur değil, sessizce biriken teknik risktir.

``

## Legacy kod gerçekten nedir?

Legacy kod yalnızca yaşlı kod değildir. On yıllık, iyi belgelenmiş ve kapsamlı testlerle korunan bir uygulama güvenle geliştirilebilir. Buna karşılık geçen ay yazılmış fakat kimsenin davranışını doğrulayamadığı bir servis de legacy sayılabilir.

Pratik bir tanım şudur: **Güvenle değiştirilemeyen kod, legacy koddur.** Sorunun merkezinde kullanılan programlama dilinden çok geri bildirim eksikliği bulunur. Bir değişikliğin sistemi bozup bozmadığını hızla öğrenemiyorsak geliştirme süreci tahmine dönüşür.

Riski basitleştirilmiş biçimde şöyle düşünebiliriz:

$$R = P(Hata) \times E(Hata)$$

Burada $P(Hata)$ değişikliğin hata üretme olasılığını, $E(Hata)$ ise oluşacak etkinin maliyetini gösterir. Test eksikliği ilk değeri, sistemin şirket için kritik olması ise ikinci değeri büyütür. Sonuç: Küçücük bir değişiklik bile yöneticilerin kahvesini soğutabilir.

| Durum | Kısa vadeli sonuç | Uzun vadeli sonuç |
|---|---|---|
| Koda hiç dokunmamak | Kesinti ihtimali azalır | Güvenlik açıkları ve bağımlılıklar büyür |
| Büyük yeniden yazım | Temiz başlangıç hissi verir | Bilinmeyen iş kuralları kaybolabilir |
| Kontrollü iyileştirme | Başlangıçta yavaş ilerler | Değişiklik güveni düzenli biçimde artar |

## Donukluğun görünmeyen faturası

“Dokunma” kararı sistemi koruyor gibi görünürken şirketi hareketsiz bırakır. Yeni kampanya kuralları uygulanamaz, mevzuat değişiklikleri gecikir ve artık desteklenmeyen kütüphaneler güvenlik açığına dönüşür. Ayrıca bilgi birkaç deneyimli çalışanın zihninde toplanır. Bu kişilerin ayrılmasıyla ortaya çıkan **otobüs faktörü**, yani kaç kişinin kaybının projeyi durduracağı, tehlikeli biçimde $1$ olabilir.

Teknik borcun büyümesi bileşik faize benzer. Yaklaşık maliyet modeli şu şekilde ifade edilebilir:

$$M(t) = M_0(1+r)^t$$

$M_0$ bugünkü bakım maliyeti, $r$ karmaşıklığın artış oranı ve $t$ geçen dönemdir. Bugün ertelenen küçük düzenleme, birkaç yıl sonra pahalı bir kurtarma operasyonuna dönüşebilir.

## Kodu uyandırmadan önce nabzını ölçmek

İlk adım doğrudan refactoring yapmak değil, mevcut davranışı kaydetmektir. **Karakterizasyon testleri**, sistemin ideal olarak ne yapması gerektiğini değil, şu anda ne yaptığını belgeler. Tuhaf görünen bir sonuç bile müşterilerin alıştığı bir iş kuralı olabilir.

```python
def test_eski_indirim_davranisi():
    # Mevcut çıktıyı güvenlik ağı olarak sabitler.
    sonuc = eski_sistem.fiyat_hesapla(tutar=1000, musteri_yasi=6)
    assert sonuc == 870
```

Bu test, `870` değerinin doğru tasarım olduğunu iddia etmez. Değişiklik sırasında davranışın yanlışlıkla farklılaşmasını görünür kılar. Ardından loglar, üretim metrikleri ve gerçek kullanım örnekleri incelenerek bu sonucun korunmasına veya bilinçli biçimde değiştirilmesine karar verilir.

## Güvenli modernizasyon rotası

Başarılı ekipler sistemi tek gecede yeniden yazmaya çalışmaz. Önce kritik akışları belirler, gözlemlenebilirlik ekler ve küçük test adaları oluştururlar. Sonra bağımlılıkları arayüzlerin arkasına alıp parçaları kademeli değiştirirler. Bu yaklaşım **Strangler Fig** deseni olarak bilinir: Yeni sistem, eskisinin işlevlerini azar azar devralır.

1. İş açısından en kritik senaryoları listele.
2. Log, metrik ve alarm mekanizmaları kur.
3. Karakterizasyon ve entegrasyon testleri ekle.
4. Küçük, geri alınabilir değişiklikler yayınla.
5. Her dağıtım için geri dönüş planı hazırla.

Amaç eski kodu estetik uğruna güzelleştirmek değildir. Amaç, şirketin yeniden güvenle hareket edebilmesini sağlamaktır. “Çalışıyor, dokunma” yerine daha sağlıklı cümle şudur: **“Nasıl çalıştığını ölç, testle koru ve küçük adımlarla iyileştir.”**
