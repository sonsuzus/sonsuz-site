---
layout: post
title: "Hücresel Otomata ile Kentsel Büyüme Modellemesi"
math: true
categories: 
  - Proje
tags: 
  - hücresel otomata
  - kentsel büyüme
  - python
  - simülasyon
  - modelleme
  - şehir planlama
toc: true
image: /img/hucresel-otomata-ile-80.png
---

Şehirler bazen planlı caddelerle, bazen de “Şuraya da bir bina konduralım!” yaklaşımıyla büyür. Gerçek kentsel gelişim ekonomi, ulaşım, nüfus ve coğrafya gibi pek çok değişkene bağlıdır. Yine de yalnızca karelerden ve birkaç komşuluk kuralından yararlanarak şaşırtıcı derecede gerçekçi büyüme desenleri üretebiliriz. Bunun için kullanacağımız araç, hücresel otomata modelidir.
``

## Hücresel otomata nedir?

Hücresel otomata, uzayı hücrelerden oluşan bir ızgaraya bölen ayrık bir modeldir. Her hücre belirli bir durumda bulunur ve bir sonraki zaman adımındaki durumu, kendi mevcut durumuna ve komşularına göre hesaplanır.

Kentsel büyüme modelinde hücreler arazi parçalarını temsil edebilir:

| Hücre değeri | Arazi türü | Büyüyebilir mi? |
|---:|---|---|
| 0 | Boş arazi | Evet |
| 1 | Kentsel alan | Zaten gelişmiş |
| 2 | Su veya koruma alanı | Hayır |

En yaygın iki komşuluk yaklaşımı şunlardır:

| Komşuluk | Hücre sayısı | Özellik |
|---|---:|---|
| Von Neumann | 4 | Yalnızca yatay ve dikey komşular |
| Moore | 8 | Çapraz hücreler dâhil tüm çevre |

Moore komşuluğu, şehrin daha yuvarlak ve yaygın biçimde büyümesine izin verir. Von Neumann komşuluğu ise daha köşeli desenler oluşturabilir.

## Büyüme kuralını kurmak

Boş bir hücrenin kentleşme olasılığını, çevresindeki kentsel hücrelerin oranıyla ilişkilendirebiliriz. Hücrenin sekiz komşusundan $n$ tanesi kentleşmişse temel olasılık şöyle tanımlanabilir:

$$P = b + w(n / 8)$$

Burada $b$ kendiliğinden büyüme olasılığı, $w$ ise komşuluk etkisinin ağırlığıdır. Örneğin $b=0.01$ ve $w=0.6$ olduğunda, mevcut şehre yakın araziler daha hızlı yapılaşırken uzakta küçük uydu yerleşimler de doğabilir. Olasılığın 1'i aşmaması için $P = min(1, P)$ kullanılır.

Bu basit denklem önemli bir fikri yakalar: Kentsel alanlar altyapı, ulaşım ve hizmetlere yakınlık nedeniyle çoğunlukla mevcut yerleşimlerin çevresinde gelişir.

## Python ile küçük bir simülasyon

Aşağıdaki kod, 50x50 hücrelik bir haritada Moore komşuluğunu kullanarak büyümeyi simüle eder:

```python
import numpy as np
import matplotlib.pyplot as plt

size = 50
city = np.zeros((size, size), dtype=int)
city[24:27, 24:27] = 1  # Başlangıçtaki kent merkezi

base_probability = 0.01
neighbor_weight = 0.60

def step(grid):
    new_grid = grid.copy()

    for row in range(1, size - 1):
        for col in range(1, size - 1):
            if grid[row, col] != 0:
                continue

            neighborhood = grid[row-1:row+2, col-1:col+2]
            urban_neighbors = np.count_nonzero(neighborhood == 1)
            probability = min(1, base_probability +
                              neighbor_weight * urban_neighbors / 8)

            if np.random.random() < probability:
                new_grid[row, col] = 1

    return new_grid

for _ in range(30):
    city = step(city)

plt.imshow(city, cmap='Greys', interpolation='nearest')
plt.title('30 Adım Sonra Kentsel Yayılım')
plt.axis('off')
plt.show()
```

`step` fonksiyonu her boş araziyi inceler, kentleşmiş komşuları sayar ve hesaplanan olasılığa göre hücrenin durumunu değiştirir. Güncelleme sırasında ayrı bir kopya kullanılması kritiktir; aksi hâlde aynı turda yeni kentleşen hücreler hemen komşularını etkiler ve zaman mantığı bozulur.

## Modeli daha gerçekçi yapmak

Basit modeli yükselti, yol ve koruma alanı katmanlarıyla geliştirebiliriz. Bir hücrenin toplam uygunluğu örneğin $S = 0.5N + 0.3R - 0.2E$ biçiminde hesaplanabilir. Burada $N$ komşuluk etkisini, $R$ yola yakınlığı, $E$ ise eğim maliyetini temsil eder.

Farklı parametrelerle çok sayıda deney yapmak, tek bir kesin gelecek üretmekten daha değerlidir. Çünkü model bir kehanet makinesi değil, “Bu kurallar geçerliyse ne olabilir?” sorusuna cevap veren bir düşünme laboratuvarıdır. Birkaç satırlık kodla plansız yayılımı, uydu kentleri veya koruma politikalarının etkisini karşılaştırabilir; şehirlerin karmaşık görünümünün basit yerel kararlardan nasıl doğabildiğini gözlemleyebilirsiniz.

![hucresel-otomata-ile-80](/img/hucresel-otomata-ile-80.svg)

