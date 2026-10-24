---
layout: post
title: "Mars Rover’larında Otonom Karar Verme: Gecikmeye Rağmen Güvenli Keşif"
math: true
categories: 
  - Bilgi
tags: 
  - mars
  - otonom sistemler
  - yapay zeka
  - rota planlama
  - robotik
  - bilgisayarlı görü
toc: true
image: /img/mars-roverlarinda-otonom-71.png
---

Mars yüzeyinde ilerleyen bir rover, Dünya’dan verilen her komutu anında uygulayan uzaktan kumandalı bir araba değildir. Gezegenlerin konumuna bağlı olarak tek yönlü iletişim yaklaşık 4–24 dakika sürebilir. Rover bir kayaya yaklaşırken operatörün “Sola dön!” komutunu bekleseydi cevap gelene kadar çoktan kuma saplanmış olabilirdi. Bu nedenle araç; çevresini algılayan, riskleri hesaplayan ve güvenli rotayı kendi başına seçen küçük bir robot kâşif gibi davranır.
``

## Neden otonomi gerekli?

Bir komutun Dünya’dan Mars’a gidip sonucunun geri dönmesi için gereken yaklaşık süre şöyle düşünülebilir:

$$T_{toplam} = 2 \times \frac{d}{c} + T_{işleme}$$

Burada $d$ gezegenler arasındaki mesafe, $c$ ışık hızı ve $T_{işleme}$ görev merkezindeki değerlendirme süresidir. Radyo sinyalleri ışık hızında ilerlese bile mesafe ortadan kalkmaz. Üstelik bant genişliği sınırlıdır; rover sürekli yüksek çözünürlüklü görüntü gönderemez.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Dünya’dan doğrudan kontrol | İnsan uzmanlığı yüksektir | Gecikme nedeniyle anlık tepki veremez |
| Tam otonom hareket | Hızlı karar alır | Hatalı algılama riski taşır |
| Karma yaklaşım | Güvenlik ve esnekliği dengeler | Karmaşık yazılım ve test gerektirir |

![mars-roverlarinda-otonom-71](/img/mars-roverlarinda-otonom-71.svg)


Güncel görevlerde çoğunlukla karma yaklaşım kullanılır. Bilim insanları hedef bölgeyi belirler; rover ise birkaç metrelik hareket sırasında taşlardan, çukurlardan ve tehlikeli eğimlerden kaçınır.

## Rover çevresini nasıl görüyor?

Otonom sürüşün ilk aşaması **algılama**dır. Stereo kameralar aynı sahneyi iki farklı noktadan görüntüler. İnsan gözlerindeki derinlik algısına benzeyen bu yöntemle pikseller arasındaki kayma, yani disparity, ölçülür. Basitleştirilmiş derinlik bağıntısı şöyledir:

$$Z = \frac{fB}{\Delta x}$$

$Z$ engele olan uzaklığı, $f$ kameranın odak uzaklığını, $B$ iki kamera arasındaki mesafeyi ve $\Delta x$ görüntülerdeki piksel farkını gösterir. Rover bu verilerden üç boyutlu bir nokta bulutu ve yerel arazi haritası üretir.

Her arazi parçasına bir maliyet atanabilir:

$$C = w_1E + w_2S + w_3R + w_4D$$

Burada $E$ eğim, $S$ zeminin gevşekliği, $R$ kaya riski ve $D$ hedefe olan uzaklıktır. Ağırlıklar görev önceliklerine göre ayarlanır. Böylece en kısa rota yerine en güvenli ve enerji açısından uygun rota seçilebilir.

## Rota planlama nasıl çalışıyor?

Harita hücrelere veya düğümlere ayrıldıktan sonra A*, Dijkstra ya da örnekleme tabanlı algoritmalar kullanılabilir. A* algoritmasının temel değerlendirmesi şöyledir:

$$f(n) = g(n) + h(n)$$

$g(n)$ başlangıçtan mevcut noktaya kadar gerçek maliyeti, $h(n)$ ise hedefe kalan tahmini maliyeti temsil eder.

```python
from heapq import heappush, heappop

def guvenli_adimlar(baslangic, hedef, komsular):
    kuyruk = [(0, baslangic, [])]
    ziyaret = set()

    while kuyruk:
        maliyet, konum, yol = heappop(kuyruk)
        if konum == hedef:
            return yol + [konum]
        if konum in ziyaret:
            continue

        ziyaret.add(konum)
        for yeni, arazi_riski in komsular(konum):
            if yeni not in ziyaret:
                heappush(kuyruk, (
                    maliyet + arazi_riski,
                    yeni,
                    yol + [konum]
                ))
    return None
```

Bu sade örnek, komşu konumları arazi riskine göre kuyruğa ekler. Gerçek rover yazılımı tekerlek kaymasını, enerji tüketimini, gövde yüksekliğini ve iletişim fırsatlarını da hesaba katar.

## Karar vermek yalnızca ilerlemek değildir

Rover risk yükseldiğinde durabilir, yeni fotoğraflar çekebilir veya farklı bir rota hesaplayabilir. Tekerleklerin dönüşüyle beklenen hareket karşılaştırılarak kayma tahmin edilir. Motorlar çalıştığı hâlde konum değişmiyorsa sistem gevşek kum ihtimalini fark eder.

| Durum | Otonom tepki |
|---|---|
| Büyük kaya | Yanal kaçış rotası oluşturma |
| Dik eğim | Maliyeti artırma veya rotayı reddetme |
| Tekerlek kayması | Hızı azaltma ve yeniden planlama |
| Belirsiz görüntü | Durup ek görüntü toplama |
| Kritik hata | Güvenli moda geçme |

Mars’ta başarılı otonomi, rover’ın “zekice cesur” değil, ölçülü biçimde temkinli olmasıdır. Çünkü milyonlarca kilometre uzaktaki bir robot için en iyi karar bazen yeni bir keşfe koşmak değil, durup Dünya’daki ekibin talimatını beklemektir.
