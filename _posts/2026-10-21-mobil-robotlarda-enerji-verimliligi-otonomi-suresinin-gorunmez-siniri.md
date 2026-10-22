---
layout: post
title: "Mobil Robotlarda Enerji Verimliliği: Otonomi Süresinin Görünmez Sınırı"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - enerji verimliliği
  - mobil robotlar
  - otonomi
  - batarya
  - gömülü sistemler
toc: true
image: /img/mobil-robotlarda-enerji-81.png
---

Bir mobil robot ne kadar akıllı olursa olsun, bataryası tükendiğinde pahalı bir dekorasyona dönüşür. Haritalama, engelden kaçınma ve yapay zekâ gibi yetenekler robotun görev başarısını belirlerken enerji verimliliği, bu yeteneklerin ne kadar süre kullanılabileceğini belirler. Dolayısıyla otonomi yalnızca yazılımsal bağımsızlık değil, aynı zamanda robotun şarj istasyonuna ihtiyaç duymadan çalışabildiği süredir.

``

## Otonomi süresinin temel denklemi

İdeal koşullarda çalışma süresi, bataryada depolanan enerji ile robotun ortalama güç tüketimi arasındaki oranla hesaplanabilir:

$$
t = \frac{E_{batarya}}{P_{ortalama}}
$$

Burada $t$ çalışma süresini, $E_{batarya}$ watt-saat cinsinden kullanılabilir enerjiyi, $P_{ortalama}$ ise watt cinsinden ortalama tüketimi temsil eder. Örneğin 240 Wh kullanılabilir enerjiye sahip ve ortalama 60 W tüketen bir robot teorik olarak dört saat çalışabilir.

Ancak gerçek dünya; sürtünme, batarya yaşlanması, sıcaklık ve dönüşüm kayıplarıyla denkleme küçük sürprizler ekler. Daha gerçekçi bir model şöyledir:

$$
t = \frac{E_{nominal} \cdot \eta_{batarya} \cdot DoD}{P_{hareket}+P_{bilgisayar}+P_{sensör}+P_{diğer}}
$$

$\eta_{batarya}$ enerji aktarım verimini, $DoD$ ise güvenli deşarj oranını gösterir. Bataryayı sürekli yüzde sıfıra indirmek daha uzun tek seferlik çalışma sağlayabilir; fakat batarya ömrünü hızla azaltır.

## Enerji nereye gidiyor?

Mobil robotlarda motorlar genellikle en büyük tüketicidir. Yine de yüksek performanslı işlemciler, LiDAR, kameralar ve kablosuz haberleşme de küçümsenmemelidir.

| Alt sistem | Tipik tüketim etkisi | Verimlilik yaklaşımı |
|---|---:|---|
| Tahrik motorları | Çok yüksek | Hafif gövde, uygun hız ve doğru redüksiyon |
| Ana bilgisayar | Orta-yüksek | Dinamik frekans ayarı, uyku modları |
| LiDAR ve kameralar | Orta | Gerektiğinde örnekleme, sensör birleştirme |
| Haberleşme | Düşük-orta | Veri paketleme, gönderim sıklığını azaltma |
| Yardımcı elektronik | Düşük | Verimli regülatör ve güç kapılama |

Hız konusu özellikle ilginçtir. Çok yavaş hareket etmek görevi uzatarak bilgisayar ve sensörlerin daha uzun süre açık kalmasına neden olur. Aşırı hızlanmak ise motor akımını ve mekanik kayıpları artırır. Bu yüzden en verimli hız her zaman en düşük hız değildir; sistemin toplam enerjisini en aza indiren çalışma noktasıdır.

## Yazılım da enerji tüketir

Kötü planlanan bir rota yalnızca zaman değil, doğrudan enerji kaybettirir. Gereksiz dönüşler, sert hızlanmalar ve sürekli yeniden planlama tüketimi artırır. Enerji farkındalığına sahip bir maliyet fonksiyonu şu şekilde kurulabilir:

$$
J = \alpha d + \beta E + \gamma R
$$

Burada $d$ mesafe, $E$ tahmini enerji tüketimi, $R$ ise çarpışma veya zorlu zemin riski olabilir. Katsayılar görevin önceliklerini belirler. Böylece robot yalnızca en kısa yolu değil, yokuşları ve zemin koşullarını hesaba katan ekonomik yolu seçebilir.

Aşağıdaki Python fonksiyonu, basitleştirilmiş bir görev süresi tahmini yapar:

```python
def otonomi_hesapla(kapasite_wh, ortalama_guc_w,
                     batarya_verimi=0.9, guvenli_desarj=0.8):
    kullanilabilir_enerji = (
        kapasite_wh * batarya_verimi * guvenli_desarj
    )
    return kullanilabilir_enerji / ortalama_guc_w

saat = otonomi_hesapla(240, 60)
print(f"Tahmini otonomi: {saat:.2f} saat")
```

Fonksiyon, nominal kapasitenin tamamını erişilebilir kabul etmek yerine verim ve güvenli deşarj katsayılarını uygular. Yine de ivmelenme, yük değişimi ve sıcaklık gibi dinamik etkiler için gerçek robottan telemetri toplanmalıdır.

## Daha uzun görevler için tasarım ilkeleri

| Verimsiz yaklaşım | Enerji dostu karşılığı |
|---|---|
| Sürekli en yüksek işlemci frekansı | İş yüküne göre frekans ölçekleme |
| Ani hızlanma ve frenleme | Yumuşak hız profilleri |
| Tüm sensörleri sürekli çalıştırma | Göreve bağlı sensör etkinleştirme |
| Yalnızca en kısa rotayı seçme | Enerji maliyetli rota planlama |

Sonuç olarak büyük batarya eklemek tek çözüm değildir; çünkü batarya büyüdükçe ağırlık ve motor tüketimi de artar. Başarılı bir mobil robot tasarımı mekanik, elektronik ve yazılım optimizasyonunu birlikte ele alır. Enerji bütçesi tasarımın sonunda kontrol edilen bir ayrıntı değil, ilk günden itibaren yönetilen temel bir kaynak olmalıdır.

![mobil-robotlarda-enerji-81](/img/mobil-robotlarda-enerji-81.svg)

