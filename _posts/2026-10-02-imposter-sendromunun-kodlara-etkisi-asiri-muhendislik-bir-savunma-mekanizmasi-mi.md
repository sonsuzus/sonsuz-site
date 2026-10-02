---
layout: post
title: "İmposter Sendromunun Kodlara Etkisi: Aşırı Mühendislik Bir Savunma Mekanizması mı?"
math: true
categories: 
  - Bilgi
tags: 
  - imposter sendromu
  - aşırı mühendislik
  - yazılım psikolojisi
  - temiz kod
  - yazılım mimarisi
  - tasarım kalıpları
toc: true
image: /img/imposter-sendromunun-kodlara-26.png
---

Basit bir kullanıcı ayarı kaydetmek için neden üç arayüz, iki fabrika, bir strateji deseni ve gelecekte kurulabilecek uzay kolonilerine hazır bir eklenti sistemi yazdık? Yanıt her zaman teknik gereksinimler değildir. Bazen yazılımcı, yeterliliğini kanıtlamak veya eleştiriden korunmak için çözümü bilinçsizce karmaşıklaştırır. İmposter sendromu ile aşırı mühendislik arasındaki ilişki tam da bu noktada ortaya çıkar.

![imposter-sendromunun-kodlara-26](/img/imposter-sendromunun-kodlara-26.svg)

``
## İmposter sendromu kod yazabilir mi?

İmposter sendromu, kişinin başarısını bilgi ve emeği yerine şansa bağlaması; çevresindekilerin ise yakında onun aslında yeterince iyi olmadığını keşfedeceğini düşünmesidir. Bu bir klinik tanıdan çok, tekrarlayan bir düşünce ve duygu örüntüsüdür.

Yazılım geliştirme bu örüntüyü beslemeye oldukça uygundur. Teknolojiler sürekli değişir, internette herkes uzman görünür ve kod incelemeleri doğrudan ürettiğimiz işe dokunur. Böyle bir ortamda karmaşık kod, psikolojik bir zırha dönüşebilir:

- Çok desen kullanırsam deneyimli görünürüm.
- Her ihtimali kapsarsam hata yaptığım söylenemez.
- Soyutlama katmanlarını artırırsam çözümüm sıradan görünmez.
- Geleceği tahmin edersem değerimi kanıtlarım.

Sorun, mühendisliğin risk yönetiminden gösteri yönetimine dönüşmesidir.

## Sağlam tasarım ile aşırı mühendislik arasındaki çizgi

Her soyutlama gereksiz değildir. Tasarım kalıpları gerçek ve tekrar eden problemlere verilmiş isimli çözümlerdir. Belirleyici soru şudur: Karmaşıklık mevcut bir ihtiyeti mi çözüyor, yoksa olası eleştirilere karşı güvence mi sağlıyor?

| Sağlam mühendislik | Aşırı mühendislik |
|---|---|
| Mevcut gereksinime dayanır | Hayalî gelecek senaryolarına dayanır |
| Karmaşıklığı azaltır | Karmaşıklığı katmanlar arasında saklar |
| Test ve bakım maliyetini düşürür | Küçük değişiklikleri pahalılaştırır |
| Takım tarafından kolayca açıklanabilir | Yazarının sürekli açıklamasına ihtiyaç duyar |
| Gerektiğinde genişletilir | En baştan her şeye hazır olmaya çalışır |

Bunu kabaca bir karar modeliyle ifade edebiliriz:

$$D = V - (K + B + R)$$

Burada $D$ tasarımın net değeri, $V$ sağladığı gerçek fayda, $K$ geliştirme karmaşıklığı, $B$ bakım maliyeti ve $R$ yanlış varsayım riskidir. Sonuç negatifse mimari etkileyici görünse bile ekonomik değildir.

## Bir buton için kurulan küçük imparatorluk

Aşağıdaki çözüm, yalnızca tema adını kaydetmek için gereksiz soyutlamalar oluşturur:

```javascript
class ThemeStorageStrategy {
  save(theme) {
    throw new Error('Uygulanmalı');
  }
}

class LocalThemeStorage extends ThemeStorageStrategy {
  save(theme) {
    localStorage.setItem('theme', theme);
  }
}

class ThemeStorageFactory {
  static create() {
    return new LocalThemeStorage();
  }
}

ThemeStorageFactory.create().save('dark');
```

Bu yapı, gerçekten birden fazla depolama yöntemi seçilecekse anlamlı olabilir. Tek gereksinim tarayıcıya değer yazmaksa aşağıdaki kod daha dürüsttür:

```javascript
function saveTheme(theme) {
  localStorage.setItem('theme', theme);
}

saveTheme('dark');
```

İkinci sürüm daha az “mimar” görünse de okunması, test edilmesi ve değiştirilmesi kolaydır. Basitlik bilgi eksikliği değil, seçenekler arasından bilinçli seçim yapabilme becerisidir.

## Savunma mekanizmasını nasıl fark ederiz?

Kodlamaya başlamadan önce şu sorular yararlıdır:

1. Bu katman bugün hangi somut problemi çözüyor?
2. Kaldırırsam sistemin hangi gereksinimi bozulur?
3. Yeni ekip arkadaşı çözümü on dakikada anlayabilir mi?
4. Tasarımı teknik ihtiyaç nedeniyle mi, profesyonel görünmek için mi seçiyorum?
5. Daha basit sürüm başarısız olursa geri dönüş maliyeti nedir?

Ayrıca kod incelemelerinde “Buna neden ihtiyaç var?” sorusunu saldırı gibi değil, maliyet analizi gibi ele almak gerekir. Küçük deneyler, zaman kutulu prototipler ve YAGNI ilkesi — “İhtiyacın olmayacak” — geleceği tamamen reddetmez; geleceğin faturasını bugünden ödemeyi reddeder.

İmposter hissinin panzehiri daha fazla desen kullanmak değil, kararları görünür gerekçelere bağlamaktır. İyi yazılımcı bütün kalıpları aynı dosyada sergileyen kişi değil; hangi kalıbı neden kullanmayacağını da bilen kişidir. Bazen en olgun mimari karar, yeni bir sınıf eklemek yerine iki satırlık fonksiyon yazıp kahveye dönmektir.
