---
layout: post
title: "Mutation Testing: Testleriniz Gerçekten Güçlü mü, Yoksa Sadece Yeşil mi?"
math: true
categories: 
  - Bilgi
tags: 
  - mutation testing
  - yazılım testi
  - test kalitesi
  - unit test
  - javascript
  - jest
toc: true
---

Test ekranındaki bütün işaretlerin yeşil olması insana huzur verir. Fakat yeşil testler, kodun doğru çalıştığını kanıtlamaktan çok mevcut beklentilerin karşılandığını söyler. Peki testlerimiz kritik bir hata karşısında gerçekten kırılıyor mu? Mutation testing, yani mutasyon testi, üretim koduna kontrollü küçük hatalar ekleyerek bu soruya oldukça eğlenceli ve zaman zaman acımasız bir cevap verir.

``

## Mutasyon testinin temel fikri

Mutasyon aracı kaynak kodun farklı kopyalarını oluşturur ve her kopyada küçük bir değişiklik yapar. Bu değiştirilmiş sürümlere **mutant** denir. Örneğin `>` operatörü `>=` yapılabilir, `true` değeri `false` ile değiştirilebilir veya matematiksel bir işlem kaldırılabilir.

Ardından test paketi her mutant için yeniden çalıştırılır:

- En az bir test başarısız olursa mutant **öldürülmüş** kabul edilir.
- Bütün testler geçerse mutant **hayatta kalır**.
- Davranışı değiştirmeyen bir mutant oluşursa buna **eşdeğer mutant** denir.

Mutasyon puanı genel olarak şöyle hesaplanır:

$$
MutationScore = \frac{Öldürülen\ Mutantlar}{Toplam\ Mutantlar - Eşdeğer\ Mutantlar} \times 100
$$

Örneğin 100 mutantın 80'i öldürülmüş, 10'u eşdeğer kabul edilmişse puan yaklaşık $88{,}9\%$ olur. Ancak yüksek puan tek başına kusursuz test paketi anlamına gelmez; önemli olan hayatta kalan mutantların neden yaşadığını incelemektir.

## Kod kapsamı ile aynı şey mi?

Hayır. Kod kapsamı ve mutasyon testi birbirini tamamlayan iki farklı ölçümdür.

| Ölçüm | Sorduğu soru | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Kod kapsamı | Bu satır çalıştırıldı mı? | Test edilmeyen bölgeleri gösterir | Sonuçların doğru doğrulandığını söylemez |
| Mutasyon testi | Kod bozulursa test fark eder mi? | Assertion kalitesini ölçer | Çalıştırılması maliyetlidir |
| Başarılı test sayısı | Kaç test geçti? | Hızlı geri bildirim verir | Testlerin anlamlı olduğunu kanıtlamaz |

Bir satır yüzde yüz kapsanabilir ama sonucu doğrulayan bir assertion bulunmayabilir. Mutasyon testi tam olarak bu rahat bölgeyi hedef alır.

## Küçük bir örnek

Aşağıdaki JavaScript fonksiyonu, belirli bir tutardan itibaren müşteriye indirim uyguluyor:

```javascript
function calculatePrice(total) {
  if (total >= 100) {
    return total * 0.9;
  }

  return total;
}
```

Yalnızca `calculatePrice(200)` sonucunun `180` olduğunu doğrulayan bir test yazdığımızı düşünelim. Mutasyon aracı `>=` operatörünü `>` olarak değiştirirse test yine geçer. Çünkü sınır değeri olan `100` hiç denenmemiştir.

```javascript
test('100 birimlik alışverişe indirim uygular', () => {
  expect(calculatePrice(100)).toBe(90);
});

test('sınırın altındaki tutarı değiştirmez', () => {
  expect(calculatePrice(99)).toBe(99);
});
```

Bu iki test yalnızca satırları çalıştırmakla kalmaz; iş kuralının sınırlarını da tarif eder. Artık `>=` operatörünü `>` yapan mutant öldürülecektir. Mutantın cenaze törenine çiçek göndermeniz gerekmez.

## Hangi araçlar kullanılabilir?

Ekosisteme göre yaygın seçenekler şunlardır:

| Platform | Araç |
|---|---|
| JavaScript / TypeScript | StrykerJS |
| Java | PIT |
| .NET | Stryker.NET |
| Python | mutmut, cosmic-ray |

Örneğin StrykerJS, `npx stryker run` komutuyla çalıştırılabilir. Araç; öldürülen, hayatta kalan, zaman aşımına uğrayan ve kapsanmayan mutantları raporlar.

## Mutasyon testi nasıl verimli kullanılır?

Mutasyon testini her dosyada ve her commit'te çalıştırmak pahalı olabilir. Çünkü $m$ mutant ve yaklaşık $t$ süreli bir test paketi için kaba maliyet $O(m \times t)$ seviyesine çıkabilir. Bu yüzden önce kritik iş kurallarına, para hesaplarına, yetkilendirme kodlarına ve geçmişte hata üreten modüllere odaklanın.

Hayatta kalan her mutant için hemen yeni test yazmak da doğru değildir. Önce mutantın gerçek davranış farkı oluşturup oluşturmadığını kontrol edin. Ardından eksik assertion, denenmemiş sınır değeri veya gereksiz üretim kodu ihtimallerini değerlendirin.

Sonuç olarak mutation testing, “Kaç testimiz var?” sorusunu “Testlerimiz hangi hataları yakalayabiliyor?” sorusuna dönüştürür. Yeşil ekran güzeldir; fakat bazen kaliteli bir test paketine ulaşmanın yolu, kodu kontrollü biçimde bozup testlerin alarm verip vermediğini dinlemekten geçer.
