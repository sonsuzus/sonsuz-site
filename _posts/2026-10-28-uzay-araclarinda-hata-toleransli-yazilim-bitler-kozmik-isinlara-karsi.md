---
layout: post
title: "Uzay Araçlarında Hata Toleranslı Yazılım: Bitler Kozmik Işınlara Karşı"
math: true
categories: 
  - Bilgi
tags: 
  - uzay yazılımı
  - hata toleransı
  - üçlü modüler yedeklilik
  - gömülü sistemler
  - kozmik radyasyon
  - tüm
toc: true
image: /img/uzay-araclarinda-hata-70.png
---

Dünya’daki bir uygulama çöktüğünde yeniden başlatma düğmesine basabiliriz. Milyonlarca kilometre uzaktaki bir uzay aracında ise fiziksel müdahale pek mümkün değildir. Üstelik yüksek enerjili parçacıklar elektronik devrelere çarparak bellekteki tek bir biti değiştirebilir. Bu nedenle uzay yazılımı yalnızca doğru çalışmakla kalmamalı; hata yaptığını fark etmeli, hasarı sınırlamalı ve görevine devam edebilmelidir.


![uzay-araclarinda-hata-70](/img/uzay-araclarinda-hata-70.svg)

``

## Kozmik radyasyon bir biti nasıl değiştirir?

Güneş’ten ve galaksinin uzak bölgelerinden gelen yüksek enerjili parçacıklar, bir yarı iletkenin içinden geçerken elektrik yükü oluşturabilir. Bu geçici yük, bellekte saklanan `0` değerini `1` yapabilir veya tersini gerçekleştirebilir. Donanım fiziksel olarak bozulmadığı hâlde verinin değiştiği bu olay **Single Event Upset (SEU)** olarak adlandırılır.

Bir bitin belirli sürede hata yaşama olasılığı yaklaşık olarak parçacık akısı ile hassas kesitin çarpımına bağlıdır:

$$R_{SEU} = \Phi \times \sigma \times N$$

Burada $\Phi$ parçacık akısını, $\sigma$ devrenin radyasyona duyarlı kesitini, $N$ ise korunması gereken bit sayısını temsil eder. Bellek büyüdükçe hedef alan da büyür; yani daha fazla kapasite, daha fazla olası hata noktası demektir.

| Sorun | Etkisi | Yaygın savunma |
|---|---|---|
| Tek bit değişimi | Veri veya komut bozulur | ECC, bellek tarama |
| İşlemci kilitlenmesi | Görev döngüsü durur | Watchdog ve yeniden başlatma |
| Sensör sapması | Yanlış yönelim kararı çıkar | Çoğunluk oylaması |
| Kalıcı donanım arızası | Bir modül kullanılamaz | Yedek bilgisayara geçiş |

## Üçlü Modüler Yedeklilik nasıl çalışır?

**Triple Modular Redundancy (TMR)** yaklaşımında aynı hesaplama üç bağımsız modülde yürütülür. Sonuçlar bir oylayıcıya gönderilir ve çoğunluğun ürettiği değer kabul edilir. Modüllerin çıktıları $A$, $B$ ve $C$ ise oylama mantığı şöyle yazılabilir:

$$Y = AB + AC + BC$$

Örneğin çıktılar `1, 1, 0` olduğunda sonuç `1` olur. Kozmik parçacık yalnızca üçüncü modülü şaşırtmışsa sistem doğru karar vermeyi sürdürür. Ancak aynı tasarım hatasının üç kopyada da bulunması TMR ile çözülemez. Bu yüzden bağımsız geliştirme, farklı algoritmalar ve fiziksel ayrım önemlidir.

```python
def majority_vote(values):
    """Üç modülün sonucundan çoğunluk değerini seçer."""
    if len(values) != 3:
        raise ValueError("TMR tam olarak üç sonuç gerektirir")

    zeros = values.count(0)
    ones = values.count(1)
    return 1 if ones > zeros else 0

sensor_results = [1, 1, 0]
command = majority_vote(sensor_results)
print(command)  # 1
```

Bu örnek yöntemin özünü gösterir; gerçek uçuş yazılımı ayrıca hangi modülün azınlıkta kaldığını kaydeder. Aynı modül sürekli farklı sonuç veriyorsa sistem onu arızalı ilan ederek yedek birime geçebilir.

## TMR tek başına yeterli mi?

Hayır. Oylayıcının kendisi hata yapabilir ve eş zamanlı iki modül bozulabilir. Bu nedenle savunma katmanlı kurulur.

| Teknik | Güçlü yanı | Bedeli |
|---|---|---|
| TMR | Tek modül hatasını anında maskeler | Güç, alan ve işlem maliyeti |
| ECC bellek | Bit hatalarını düzeltir | Ek kontrol bitleri |
| Watchdog | Kilitlenen sistemi sıfırlar | Durum kaybı yaşanabilir |
| Checkpoint | Güvenli duruma dönüş sağlar | Depolama ve zaman maliyeti |
| Safe mode | Aracı hayatta tutar | Bilimsel görevler geçici olarak durur |

Bellek tarama, diğer adıyla **scrubbing**, ECC ile düzeltilen verileri düzenli olarak yeniden yazar. Böylece ikinci hata gelmeden ilk bozulma temizlenir. Watchdog zamanlayıcısı yazılımdan periyodik bir yaşam sinyali bekler; sinyal kesilirse işlemciyi veya ilgili görevi yeniden başlatır.

## Güvenilirlik bir mimari özelliktir

Uzay yazılımında hata toleransı sonradan eklenen bir yama değildir. Telemetri kayıtları, zaman aşımı kuralları, güvenli mod, yedek bilgisayarlar ve doğrulanabilir durum makineleri birlikte tasarlanır. Amaç bütün hataları engellemek değil, kaçınılmaz hataların felakete dönüşmesini önlemektir. Kısacası uzay aracı, kozmik zarların her zaman lehine gelmeyeceğini bilir ve yazılımını buna göre oynar.
