---
layout: post
title: "Haskell ile Saf Fonksiyonel Programlama: Doğruluk İçin Yan Etkisiz Tasarım"
math: true
categories: 
  - Bilgi
tags: 
  - haskell
  - fonksiyonel programlama
  - saf fonksiyonlar
  - tembel değerlendirme
---

Bir programın doğru çalıştığından emin olmak çoğu zaman yalnızca test yazmakla bitmez. Değişkenlerin beklenmedik biçimde güncellenmesi, dosya işlemleri, ağ çağrıları ve zaman bağımlılığı gibi etkiler kodun davranışını zorlaştırır. Haskell, **saf fonksiyonel programlama** yaklaşımıyla bu karmaşıklığı azaltmayı hedefler: Fonksiyonlar mümkün olduğunca yalnızca girdilerine bağlı sonuç üretir; yan etkiler ise açıkça modellenir.
``

Saflığın temel kavramı **referanssal şeffaflık**tır. Bir ifade her yerde aynı değerle değiştirilebiliyorsa referanssal olarak şeffaftır. Matematikteki $f(x) = x^2$ fonksiyonu bunun ideal örneğidir: $f(4)$ her koşulda $16$ eder. Haskell'de saf fonksiyonlar da aynı sözleşmeye sahiptir. Böylece bir fonksiyonun sonucunu anlamak için uygulamanın küresel durumunu, çağrılma sırasını veya gizli değişkenleri takip etmek gerekmez.

| Özellik | Saf fonksiyon | Yan etkili fonksiyon |
|---|---|---|
| Sonuç | Sadece parametrelere bağlıdır | Ortam, zaman veya küresel duruma bağlı olabilir |
| Test | Girdi-çıktı örnekleriyle kolaydır | Hazırlık, temizleme ve mock gerektirebilir |
| Çağrı sırası | Genellikle önemsizdir | Davranışı değiştirebilir |
| Yeniden kullanım | Yüksektir | Dış bağımlılıklarla sınırlanabilir |

Örneğin aşağıdaki `indirimliToplam` fonksiyonu hiçbir dış veriye erişmez ve herhangi bir değeri değiştirmez. Aynı `fiyatlar` ve `oran` ile her çağrıda aynı sonucu verir. Bu özellik, fonksiyonu hem birim testleri hem de cebirsel düşünme açısından güvenilir kılar.

```haskell
indirimliToplam :: [Double] -> Double -> Double
indirimliToplam fiyatlar oran =
  sum (map (\fiyat -> fiyat * (1 - oran)) fiyatlar)

ornekToplam :: Double
ornekToplam = indirimliToplam [100, 250, 80] 0.20
```

Burada `map`, listedeki her fiyatı dönüştürür; `sum` ise dönüştürülmüş değerleri toplar. Fonksiyonun doğruluğu parçalar üzerinden incelenebilir. Örneğin $0 \leq oran \leq 1$ ise, negatif olmayan her fiyat için indirimli fiyatın da negatif olmayacağı söylenebilir. Bu tür kurallar, property-based testing araçlarıyla otomatik olarak sınanabilir.

Haskell'in ikinci güçlü aracı **tembel değerlendirme**dir (lazy evaluation). Bir ifade, sonucu gerçekten gerekene kadar hesaplanmaz. Bu yaklaşım sonsuz veri yapılarını pratik hale getirir. Örneğin doğal sayıları baştan oluşturmak yerine, ihtiyaç oldukça üretebiliriz:

```haskell
dogalSayilar :: [Integer]
dogalSayilar = [0..]

ilkBesKare :: [Integer]
ilkBesKare = take 5 (map (\n -> n * n) dogalSayilar)
```

`dogalSayilar` teorik olarak sonsuzdur; fakat `take 5`, yalnızca gerekli ilk beş değerin hesaplanmasını ister. Sonuç `[0,1,4,9,16]` olur. Eager, yani istekli değerlendirme kullanan bir sistemde sonsuz listenin tamamını üretmeye çalışmak programı kilitlerdi.

| Değerlendirme biçimi | Hesaplama zamanı | Avantaj | Dikkat edilmesi gereken |
|---|---|---|---|
| İstekli değerlendirme | Fonksiyon çağrılır çağrılmaz | Akış daha doğrudan görünebilir | Gereksiz hesaplama yapabilir |
| Tembel değerlendirme | Sonuç gerektiğinde | Sonsuz listeler ve zincirleme dönüşümler | Bellekte bekleyen ifadeler birikebilir |

Saflık ve tembellik birlikte özellikle güçlüdür. Saf bir ifade ertelenebilir, tekrar hesaplanabilir veya derleyici tarafından optimize edilebilir; çünkü bu işlemler programın gözlemlenebilir davranışını değiştirmez. Yan etkili bir `print` ya da dosya yazma işlemi ertelenirse sırası değişebilir ve sonuç tehlikeli hale gelir. Haskell bu nedenle etkileri `IO` tipiyle ayırır: saf hesaplama ile dış dünya etkileşimi aynı şeymiş gibi görünmez.

Sonuç olarak Haskell, program doğruluğunu sihirli biçimde garanti etmez; ancak hataya açık alanları görünür yapar. Saf fonksiyonlar küçük, tahmin edilebilir ve kanıtlanabilir bileşenler sunar. Tembel değerlendirme ise yalnızca gerekli işi yaparak zarif veri akışları kurar. Bu ikili, özellikle iş kuralları, veri dönüşümü ve algoritmik hesaplamalarda daha güvenilir yazılımlar tasarlamak için güçlü bir zihinsel modeldir.
