---
layout: post
title: "APL ve BQN: Dizi Programlamada Tek Satırın Şaşırtıcı Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - apl
  - bqn
  - dizi-programlama
  - fonksiyonel-programlama
  - algoritma
  - programlama-dilleri
toc: true
---

Bir listedeki sayıları dönüştürmek, süzmek ve özetlemek için kaç satır kod gerekir? Geleneksel bir dilde döngü, sayaç ve geçici değişkenler devreye girebilir. APL ve onun modern akrabası BQN ise aynı problemi birkaç sembolle anlatır. İlk bakışta uzaylı alfabesine benzeyen bu yaklaşımın sırrı, tek tek elemanlarla değil dizilerin bütünüyle düşünmesidir.
``

## Dizi programlama nedir?

Dizi programlamada temel veri birimi yalnızca sayı değil; vektör, matris veya daha yüksek boyutlu bir dizidir. Bir işlem diziye uygulandığında çoğu zaman açık bir döngü yazmadan bütün elemanlar üzerinde çalışır.

Örneğin $x = [1,2,3,4]$ olsun. Matematiksel olarak her elemanın karesini şöyle tanımlarız:

$$y_i = x_i^2$$

Dizi dilleri bu ifadeyi neredeyse doğrudan kodlar. APL'de:

```apl
x ← 1 2 3 4
x * 2
```

Sonuç `1 4 9 16` olur. `*` fonksiyonu sağındaki üs değerini, solundaki dizinin her elemanına uygular. Döngü görünmez; çünkü eleman bazlı çalışma dilin doğal davranışıdır.

## APL ve BQN nasıl ayrılıyor?

APL, 1960'larda Kenneth E. Iverson'ın matematiksel gösteriminden doğdu. BQN ise aynı düşünce ailesini daha düzenli kurallar, güçlü fonksiyon birleştirme araçları ve modern bir uygulama ekosistemiyle sürdürür.

| Özellik | APL | BQN |
|---|---|---|
| Köken | Tarihsel ve köklü | Modern dizi dili |
| Gösterim | Yoğun APL sembolleri | Kendine özgü Unicode sembolleri |
| Değerlendirme | Genellikle sağdan sola | Basit ve tutarlı sözdizimi |
| Güçlü yanı | Olgun araçlar ve gelenek | Birleştiriciler ve düzenli semantik |
| İlk izlenim | Matematiksel hiyeroglif | Matematiksel hiyeroglifin yeni sürümü |

İki dilde de semboller süs değildir. Her biri tekrar kullanılan bir fikri sıkıştırır: toplama, katlama, sıralama, ters çevirme veya eksenler üzerinde çalışma.

## Tek satır neden güçlü?

Bir sayı dizisinin toplamını APL'de şöyle hesaplayabiliriz:

```apl
+/ 3 1 4 1 5
```

Buradaki `/`, toplama fonksiyonunu dizi boyunca **indirger**. İşlem aslında şudur:

$$3 + 1 + 4 + 1 + 5 = 14$$

BQN'de benzer indirgeme fikri `´` ile ifade edilir:

```bqn
+´ 3‿1‿4‿1‿5
```

Bu kod da diziyi toplama işlemiyle tek değere katlar. Kısalık, işlemlerin eksik yazılmasından değil, `for` döngüsü gibi mekanik ayrıntıların soyutlanmasından gelir.

Bir başka klasik işlem, ilk $n$ doğal sayıyı üretmektir. APL'nin `⍳` fonksiyonu indeks vektörü oluşturur:

```apl
⍳10
```

BQN'de aynı temel fikir `↕` ile karşılanır:

```bqn
↕10
```

BQN sıfır tabanlı olarak `0` ile `9` arasındaki değerleri üretir. APL'de başlangıç değeri çalışma alanındaki indeks başlangıcı ayarına bağlı olabilir.

## Okunabilirlik mi, sıkıştırma mı?

Tek satır her zaman iyi kod demek değildir. Dizi programlamanın amacı bir kod golfü yarışmasını kazanmak değil, problemi doğru soyutlama düzeyinde ifade etmektir.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Açık döngü | Yeni başlayan için tanıdık | Fazla mekanik ayrıntı |
| Yoğun tek satır | Matematiksel ve kısa | Sembol bilgisi gerektirir |
| Parçalara ayrılmış dizi kodu | Kısa ve test edilebilir | İyi isimlendirme ister |

Karmaşık ifadeleri adlandırılmış ara fonksiyonlara bölmek, sembollerin anlamını açıklamak ve örnek girdilerle test etmek önemlidir. Aksi hâlde bugünün zarif tek satırı, yarının dijital define haritasına dönüşebilir.

APL ve BQN, programcıya farklı bir zihinsel egzersiz sunar: “Bu eleman için ne yapmalıyım?” yerine “Bu dizinin tamamına hangi dönüşümü uygulamalıyım?” sorusunu sordurur. Sembolleri öğrenme eğrisi dik olsa da ödülü büyüktür; daha az mekanik kod, daha fazla matematiksel niyet ve bazen gerçekten büyüleyici tek satırlar.
