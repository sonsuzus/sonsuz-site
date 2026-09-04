---
layout: post
title: "Yazılım Testlerinde Mutasyon Analizi: Testlerinizi Bilinçli Hatalarla Sınayın"
math: true
categories: 
  - Bilgi
tags: 
  - mutasyon testi
  - yazılım testi
  - test kalitesi
toc: true
---

Kod kapsamınız yüzde 100 olabilir; ancak bu, testlerinizin gerçekten hata yakaladığı anlamına gelmez. Belki testler yalnızca satırları çalıştırıyor, sonuçları ise yeterince sorgulamıyordur. Mutasyon analizi, kaynak kodda kontrollü ve küçük hatalar oluşturarak test takımına şu eğlenceli soruyu sorar: “Bunu da yakalayabilecek misin?”

``

## Mutasyon analizi nasıl çalışır?

Mutasyon testi aracı, çalışan kaynak kodun farklı kopyalarını üretir. Her kopyada tek bir küçük değişiklik bulunur ve bu değiştirilmiş sürüme **mutant** denir. Ardından mevcut test takımı her mutant üzerinde çalıştırılır.

Testlerden en az biri başarısız olursa mutant **öldürülmüş** kabul edilir. Testlerin tamamı geçerse mutant **hayatta kalmıştır**. Hayatta kalan mutantlar genellikle eksik doğrulamaları, zayıf sınır testlerini veya hiç test edilmeyen davranışları gösterir.

Örneğin araç şu değişiklikleri yapabilir:

| Orijinal ifade | Mutasyon | Olası hata |
|---|---|---|
| `age >= 18` | `age > 18` | Sınır değeri hatası |
| `price + tax` | `price - tax` | Aritmetik hata |
| `isActive` | `!isActive` | Mantıksal tersine çevirme |
| `return true` | `return false` | Sabit dönüş değişimi |
| `a && b` | `a || b` | Koşul operatörü hatası |

Bu değişiklikler rastgele kod bozma işlemleri değildir. Gerçek geliştirici hatalarını taklit eden, önceden tanımlanmış **mutasyon operatörleri** tarafından uygulanır.

## Mutasyon skoru

Test takımının başarısı çoğunlukla mutasyon skoru ile ölçülür:

$$
M = \frac{K}{T - E} \times 100
$$

Burada $K$ öldürülen mutant sayısını, $T$ toplam mutant sayısını, $E$ ise eşdeğer mutantları temsil eder. Örneğin 120 mutantın 90’ı öldürülmüş ve 10’u eşdeğer kabul edilmişse skor:

$$
M = \frac{90}{120 - 10} \times 100 \approx 81.8\%
$$

**Eşdeğer mutant**, kodu değiştirmesine rağmen gözlemlenebilir davranışı değiştirmeyen mutanttır. Örneğin pozitif sayılarla çalışan belirli bir bağlamda `x * 1` ifadesinin `x / 1` yapılması aynı sonucu üretebilir. Böyle bir mutantı hiçbir test öldüremez; bu nedenle sonuçlar yorumlanırken ayrıca incelenmelidir.

## Küçük bir örnek

Aşağıdaki JavaScript fonksiyonu yetişkinlik kontrolü yapıyor:

```javascript
function isAdult(age) {
  return age >= 18;
}
```

Yalnızca aşağıdaki testin bulunduğunu düşünelim:

```javascript
test("20 yaşındaki kişi yetişkindir", () => {
  expect(isAdult(20)).toBe(true);
});
```

Mutasyon aracı `>=` operatörünü `>` olarak değiştirirse test hâlâ geçer. Mutant hayatta kalır; çünkü test sınır değeri olan 18’i hiç denememiştir. Eksikliği gidermek için şu test eklenebilir:

```javascript
test("18 yaşındaki kişi yetişkindir", () => {
  expect(isAdult(18)).toBe(true);
});
```

Artık `age > 18` mutasyonu başarısız olur ve mutant öldürülür. Böylece mutasyon analizi yalnızca bir puan vermekle kalmaz, hangi davranışın eksik sınandığını da gösterir.

## Kod kapsamından farkı nedir?

| Ölçüm | Yanıtladığı soru | Zayıf yönü |
|---|---|---|
| Satır kapsamı | Hangi satırlar çalıştı? | Sonuçların doğrulandığını göstermez |
| Dal kapsamı | Hangi karar yolları çalıştı? | Doğrulamaların gücünü ölçmez |
| Mutasyon skoru | Testler davranış değişimini yakaladı mı? | Çalıştırma maliyeti yüksektir |

Kod kapsamı haritayı gösterirken mutasyon analizi alarm sistemini dener. Bu iki ölçüm rakip değil, tamamlayıcıdır.

## Pratik kullanım önerileri

Mutasyon testleri normal testlerden çok daha yavaş olabilir; çünkü her mutant için testlerin yeniden çalıştırılması gerekir. Bu yüzden önce değişen dosyalarda çalıştırmak, paralel yürütme kullanmak ve anlamsız operatörleri kapatmak faydalıdır. Java için PIT, JavaScript ve TypeScript için Stryker, .NET için Stryker.NET tercih edilebilir.

Hedef körü körüne yüzde 100 skor değildir. Kritik iş kurallarındaki hayatta kalan mutantları incelemek daha değerlidir. Çünkü iyi bir test takımı yalnızca kodu gezmez; kod yanlış davrandığında yüksek sesle itiraz eder.
