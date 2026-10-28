---
layout: post
title: "Saniyelerle Yarışmak: Speedrun Kültürü ve Glitch Ustalığı"
math: true
categories: 
  - Bilgi
tags: 
  - speedrun
  - glitch
  - oyun geliştirme
  - oyun kültürü
  - algoritma
  - performans
toc: true
image: /img/saniyelerle-yarismak-speedrun-44.png
---

Bir oyunu bitirmek çoğu oyuncu için hikâyeyi keşfetmek, görevleri tamamlamak ve son düşmanı yenmek demektir. Speedrunner içinse oyun; ölçülebilen, parçalarına ayrılabilen ve mümkün olan en kısa sürede çözülebilen dev bir optimizasyon problemidir. Duvarların içinden geçmek, ara sahneleri atlamak veya fizik motorunu şaşırtmak hile gibi görünebilir; fakat speedrun topluluklarında bunlar çoğu zaman yıllarca araştırılan teknik becerilerdir.

``

## Speedrun yalnızca hızlı oynamak değildir

Speedrun, belirlenmiş kurallar altında bir oyunu ya da oyun bölümünü en kısa sürede tamamlama yarışıdır. Oyuncular rotalarını tekrar tekrar deneyerek hareketleri, kaynak kullanımını ve savaşları optimize eder. Bu süreç matematiksel olarak bir maliyet minimizasyonuna benzetilebilir:

$$T_{toplam} = T_{hareket} + T_{savaş} + T_{yükleme} + T_{hata}$$

Amaç, toplam süreyi küçültmektir. Bir kısayol hareket süresini 20 saniye azaltırken başarısız olma riski nedeniyle ortalama 30 saniye kaybettiriyorsa rekor denemesi için uygun olmayabilir. Bu nedenle oyuncular yalnızca tekniğin teorik kazancını değil, başarı olasılığını da değerlendirir:

$$E(T) = p \cdot T_{başarılı} + (1-p) \cdot T_{başarısız}$$

Buradaki $p$, hareketin başarı ihtimalidir. Dünya rekoru peşindeki oyuncu düşük olasılıklı bir yöntemi seçebilirken maraton yayınındaki oyuncu daha güvenli bir rota kullanabilir.

## Glitch nasıl keşfedilir?

Glitch, oyunun kodu ile oyuncunun eylemleri arasındaki beklenmeyen etkileşimdir. Keşif bazen tesadüfen gerçekleşir: Oyuncu zıplarken menüyü açar ve karakter bir kapının arkasına ışınlanır. Topluluk daha sonra olayı yeniden üretmeye çalışır, gerekli koşulları belirler ve bulguları kare kare inceler.

Bir glitch’in geliştirilmesi genellikle şu aşamalardan geçer:

1. **Gözlem:** Beklenmeyen davranış fark edilir.
2. **Yeniden üretim:** Aynı sonucun hangi girdilerle oluştuğu aranır.
3. **Modelleme:** Kamera, çarpışma ve bellek gibi sistemlerin rolü incelenir.
4. **Optimizasyon:** Daha hızlı ve güvenilir uygulama geliştirilir.
5. **Belgeleme:** Video, zaman damgası ve rehber toplulukla paylaşılır.

Yani meşhur kısayol, çoğunlukla tek bir kişinin şans eseri bulduğu numaradan ziyade kolektif bir araştırma ürünüdür.

| Teknik | Temel fikir | Olası kazanç | Risk |
|---|---|---:|---|
| Duvar geçişi | Çarpışma sınırını aşmak | Yüksek | Bölüm dışında kalmak |
| Menü atlaması | Oyun durumlarını yanlış sırada tetiklemek | Orta | Kaydın bozulması |
| Hız depolama | Fizik değerini sonraki harekete taşımak | Yüksek | Hassas zamanlama |
| Güvenli rota | Glitch kullanmadan optimize yürümek | Düşük | Genellikle az |

## Kareler, girdiler ve ölçüm

60 FPS çalışan bir oyunda tek kare yaklaşık olarak $1/60$ saniye, yani 16,67 milisaniyedir. Bir hareket yalnızca iki karelik pencerede yapılabiliyorsa oyuncunun doğru girdiyi yaklaşık 33 milisaniyelik aralıkta vermesi gerekir. Bu yüzden speedrunner’lar kayıtlarını analiz eden küçük araçlar kullanır.

```python
splitler = [42.18, 39.72, 41.05, 38.91]
hedef = 40.00

for bolum, sure in enumerate(splitler, start=1):
    fark = sure - hedef
    durum = "yavaş" if fark > 0 else "hızlı"
    print(f"Bölüm {bolum}: {abs(fark):.2f} sn {durum}")
```

Bu Python örneği, bölüm sürelerini hedef değerle karşılaştırır. Gerçek analiz araçları aynı mantığı kişisel en iyi dereceler, ortalamalar ve rota alternatifleri üzerinde uygular.

## Glitch kullanmak hile midir?

Cevap kategoriye bağlıdır. **Any%** kategorisi oyunu izin verilen her yöntemle bitirmeyi hedefler. **Glitchless** kategorisi belirli hataları yasaklar. **100%** ise tanımlanan tüm içeriklerin tamamlanmasını ister. Kuralları topluluk belirler; emülatör, mod, makro veya dışarıdan kod müdahalesi çoğunlukla yasaktır.

Speedrun kültürünü ilginç yapan şey, oyuncuların oyunu bozarken aslında onu olağanüstü ayrıntılı biçimde öğrenmesidir. Geliştiricinin kurduğu dünya bir laboratuvara, kontrolcü deney aracına, her başarısız deneme de yeni bir veri noktasına dönüşür. Ekranda birkaç saniyelik kısayol görünür; arkasında ise yüzlerce saatlik merak, iş birliği ve ustalık vardır.

![saniyelerle-yarismak-speedrun-44](/img/saniyelerle-yarismak-speedrun-44.svg)

