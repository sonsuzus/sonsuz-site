---
layout: post
title: "Branch Prediction’ın İç Dünyası: CPU Geleceği Nasıl Tahmin Ediyor?"
math: true
categories: 
  - Bilgi
tags: 
  - branch prediction
  - cpu
  - işlemci mimarisi
  - performans
  - pipeline
  - assembly
toc: true
image: /img/branch-predictionin-ic-50.png
---

![branch-predictionin-ic-50](/img/branch-predictionin-ic-50.svg)


Modern bir CPU, yalnızca komutları çalıştıran hızlı bir hesap makinesi değildir; aynı zamanda geleceği tahmin etmeye çalışan minik bir falcıdır. Programdaki `if`, `switch` ve döngü koşulları işlem akışını değiştirdiğinde CPU, sonucun hesaplanmasını beklemek yerine hangi yolun izleneceğini tahmin eder. Bu mekanizmaya **branch prediction**, yani dallanma tahmini denir.
``
## CPU neden tahmin yapmak zorunda?

İşlemciler komutları bir **pipeline** üzerinden geçirir. Basitleştirilmiş bir pipeline; komutu getirme, çözümleme, yürütme ve sonucu yazma aşamalarından oluşur. Üstelik modern CPU’lar aynı anda birçok komutu işleyebilir.

Bir koşullu dallanmayla karşılaşıldığında hangi komutun getirileceği henüz belli olmayabilir:

```c
if (sicaklik > 30) {
    klima_ac();
} else {
    pencereyi_ac();
}
```

CPU, `sicaklik > 30` sonucunu beklerse pipeline boş kalır. Bunun yerine bir yolu seçer ve komutları **spekülatif** olarak yürütmeye başlar. Tahmin doğruysa zaman kazanılır; yanlışsa yapılan işler iptal edilir ve pipeline doğru adresten yeniden doldurulur.

Ortalama maliyet kabaca şöyle modellenebilir:

$$
T = N \times C + M \times P
$$

Burada $N$ komut sayısını, $C$ komut başına temel maliyeti, $M$ yanlış tahmin sayısını ve $P$ yanlış tahmin cezasını gösterir. Modern işlemcilerde $P$, mimariye göre onlarca çevrime ulaşabilir.

## Statik ve dinamik tahmin

En basit yaklaşım **statik tahmindir**. Örneğin CPU, geriye doğru giden dalların döngü olduğunu varsayıp alınacağını tahmin edebilir. Ancak gerçek güç, geçmiş davranışları öğrenen dinamik tahmincilerden gelir.

| Yaklaşım | Kullandığı bilgi | Avantajı | Dezavantajı |
|---|---|---|---|
| Statik tahmin | Komutun yönü veya derleyici ipucu | Basit ve ucuz | Programa uyum sağlayamaz |
| 1 bit tahminci | Son dallanma sonucu | Hızlı öğrenir | Döngü sınırlarında kolay yanılır |
| 2 bit sayaç | Yakın geçmişteki eğilim | Tek sapmada fikrini değiştirmez | Karmaşık desenleri kaçırır |
| Global tahminci | Birden fazla dalın geçmişi | İlişkili koşulları öğrenebilir | Daha fazla donanım ister |

Yaygın 2 bit doygunluk sayacı dört durum taşır: güçlü alınmaz, zayıf alınmaz, zayıf alınır ve güçlü alınır. Sonuç alındıkça sayaç yükselir veya düşer. Böylece çoğunlukla çalışan bir koşul, tek istisna yüzünden hemen güven kaybetmez.

## Hedef adresi de tahmin etmek gerekir

Dallanmanın alınıp alınmayacağını bilmek tek başına yeterli değildir; CPU’nun gidilecek adresi de bulması gerekir. **Branch Target Buffer (BTB)**, daha önce görülen dalların hedeflerini saklayan bir önbellek gibi çalışır. Fonksiyon dönüşleri içinse çağrı adreslerini takip eden **Return Address Stack** kullanılabilir.

Dolaylı çağrılar daha zordur:

```cpp
// Hedef, çalışma anında seçildiği için tahmini daha güçtür.
handlers[event.type](event);
```

Bu tür kodlarda aynı çağrı noktası birçok farklı hedefe gidebilir. Sanal fonksiyonlar, callback’ler ve büyük `switch` yapıları bu nedenle tahminci üzerinde baskı oluşturabilir.

## Tahmin edilebilir kod neden hızlıdır?

Aşağıdaki döngüde veriler rastgele dağılmışsa koşulun sonucu sürekli değişebilir:

```c
long toplam = 0;
for (int i = 0; i < n; i++) {
    if (veri[i] >= esik) {
        toplam += veri[i]; // Yalnızca eşiği geçen değerleri toplar.
    }
}
```

Sıralı veya belirgin kümeler hâlindeki veriler, tahminci için daha kolaydır. Rastgele yüzde 50 dağılım ise adeta yazı tura gibidir. Bazı durumlarda kod, koşulsuz veya vektörleşmeye uygun biçimde yazılabilir:

```c
for (int i = 0; i < n; i++) {
    toplam += (veri[i] >= esik) ? veri[i] : 0;
}
```

Ancak üçlü operatörün mutlaka dalsız makine kodu üreteceği garanti değildir. Son kararı derleyici, optimizasyon seviyesi ve hedef mimari verir. Bu yüzden assembly çıktısını ve Linux’taki `perf stat` gibi araçların `branch-misses` sayacını incelemek en sağlıklı yöntemdir.

Kısacası branch prediction, CPU’nun pipeline’ı sürekli dolu tutmak için geçmişten örüntü öğrenmesidir. Başarılı olduğunda görünmezdir; başarısız olduğunda ise birkaç masum `if`, performans partisinin davetsiz misafirine dönüşebilir.
