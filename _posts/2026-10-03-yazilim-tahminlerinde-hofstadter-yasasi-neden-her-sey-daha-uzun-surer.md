---
layout: post
title: "Yazılım Tahminlerinde Hofstadter Yasası: Neden Her Şey Daha Uzun Sürer?"
math: true
categories: 
  - Bilgi
tags: 
  - hofstadter yasası
  - yazılım tahmini
  - iyimserlik önyargısı
  - proje yönetimi
  - planlama yanılgısı
  - risk analizi
toc: true
image: /img/yazilim-tahminlerinde-hofstadter-88.png
---

![yazilim-tahminlerinde-hofstadter-88](/img/yazilim-tahminlerinde-hofstadter-88.svg)


Bir geliştiriciye “Bu özellik ne zaman biter?” diye sorduğunuzda genellikle net, umut dolu ve tehlikeli bir cevap alırsınız: “İki güne hazır.” İki gün sonra özellik büyük ölçüde tamamlanmıştır; yalnızca testler, hata düzeltmeleri, kod incelemesi, dokümantasyon ve daha önce kimsenin fark etmediği bir veri tabanı problemi kalmıştır. Yani iş bitmiştir, fakat aslında hiç bitmemiştir. Hofstadter Yasası tam olarak bu tanıdık çelişkiyi açıklar.

``

## Hofstadter Yasası nedir?

Bilişsel bilimci Douglas Hofstadter tarafından ortaya atılan yasa şöyle der:

> Hofstadter Yasası’nı hesaba katsanız bile, işler daima beklediğinizden uzun sürer.

Cümlenin eğlenceli tarafı, kendi önlemini de etkisiz hâle getirmesidir. Tahmininize fazladan süre ekleseniz bile beklenmeyen karmaşıklık bu tamponu tüketebilir. Çünkü yazılım geliştirme, aynı parçanın tekrar tekrar üretildiği mekanik bir süreç değildir. Gereksinimler değişir, bağımlılıklar bozulur ve küçük görünen kararlar yeni işler doğurur.

Basit bir tahmin modelini şöyle gösterebiliriz:

$$T_{gerçek} = T_{tahmin} \times (1 + b) + U$$

Burada $b$, iyimserlik önyargısından kaynaklanan hata oranını; $U$ ise bilinmeyen işleri temsil eder. Sorun, ekiplerin çoğunlukla $b = 0$ ve $U = 0$ varsayımıyla plan yapmasıdır. Gerçek dünya ise sıfırları pek sevmez.

## Beynimiz tahminleri neden sabote eder?

İyimserlik önyargısı, olumlu sonuçların gerçekleşme ihtimalini abartmamıza yol açar. Geliştirici görevin sorunsuz ilerleyen ideal sürümünü zihninde canlandırır. İnternet kesintisini, belirsiz kabul kriterlerini veya üçüncü taraf API’nin sürprizini tahmine katmaz.

Buna **planlama yanılgısı** da eşlik eder: Geçmişteki gecikmeleri incelemek yerine yeni görevin farklı ve daha kolay olacağına inanırız. Ayrıca yönetici baskısı, müşteriyi memnun etme arzusu ve deneyimli görünme isteği tahminleri aşağı çeker.

| Psikolojik tuzak | Tipik düşünce | Sonuç |
|---|---|---|
| İyimserlik önyargısı | “Bu kez sorun çıkmaz.” | Riskler yok sayılır |
| Planlama yanılgısı | “Önceki gecikme istisnaydı.” | Geçmiş veriler kullanılmaz |
| Çapa etkisi | “Yönetici üç gün dedi.” | Tahmin ilk sayıya yaklaşır |
| Kapsam ihmali | “Sadece bir buton ekleyeceğiz.” | Arka uç ve testler unutulur |
| Batık maliyet yanılgısı | “Bir gün daha verirsek biter.” | Sorunlu yaklaşım sürdürülür |

## Tek sayı yerine olasılık kullanın

“Beş gün sürer” demek, belirsizliği görünmez yapar. Bunun yerine iyimser, olası ve kötümser tahminler üretilebilir. PERT yaklaşımı beklenen süreyi şu şekilde hesaplar:

$$T_E = \frac{O + 4M + P}{6}$$

$O$ iyimser, $M$ en olası, $P$ kötümser süredir. Örneğin değerler 3, 6 ve 15 günse sonuç $7$ gündür. Bu yöntem kusursuz değildir; ancak ekibi tek bir sihirli sayıya bağlanmaktan kurtarır.

Belirsizliği görünür kılmak için küçük bir Monte Carlo simülasyonu da kullanılabilir:

```python
import random

sonuclar = []
for _ in range(10_000):
    analiz = random.triangular(1, 5, 2)
    gelistirme = random.triangular(3, 12, 6)
    test = random.triangular(1, 8, 3)
    sonuclar.append(analiz + gelistirme + test)

sonuclar.sort()
p85 = sonuclar[int(len(sonuclar) * 0.85)]
print(f"Yüzde 85 güvenle: {p85:.1f} gün")
```

Kod, her aşama için farklı süreler seçerek binlerce olası proje sonucu üretir. Böylece “kaç gün?” yerine “hangi güven düzeyinde kaç gün?” sorusu cevaplanır.

## Daha gerçekçi tahmin alışkanlıkları

Görevleri küçük parçalara bölün, benzer işlerin geçmiş çevrim sürelerini kaydedin ve tahmini işi yapacak kişilerin vermesini sağlayın. Kod incelemesi, test, dağıtım ve dokümantasyonu “sonradan yapılacak küçük işler” olarak değil, tamamlanma tanımının parçaları olarak görün.

Son olarak tahmin ile taahhüdü ayırın. Tahmin mevcut bilgilerle üretilen olasılıktır; taahhüt ise iş kararıdır. Hofstadter Yasası’nı yenmek mümkün olmayabilir, fakat belirsizliği dürüstçe yöneterek onun her sprintte aynı şakayı yapmasını engelleyebilirsiniz.
