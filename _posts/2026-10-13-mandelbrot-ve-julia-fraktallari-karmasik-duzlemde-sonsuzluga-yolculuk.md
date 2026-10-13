---
layout: post
title: "Mandelbrot ve Julia Fraktalları: Karmaşık Düzlemde Sonsuzluğa Yolculuk"
math: true
categories: 
  - Bilgi
tags: 
  - fraktal
  - mandelbrot
  - julia
  - karmaşık-sayılar
  - python
  - matematik
toc: true
image: /img/mandelbrot-ve-julia-86.png
---

![mandelbrot-ve-julia-86](/img/mandelbrot-ve-julia-86.svg)


Bir deniz kabuğunun kıvrımlarını, eğrelti otunun yapraklarını veya uzaktan bakıldığında kıyı şeridinin bitmek bilmeyen girintilerini düşünün. Fraktallar, küçük parçaları bütüne benzeyen ve yakınlaştırıldıkça yeni ayrıntılar sunan geometrik yapılardır. Mandelbrot ve Julia kümeleri ise bu büyüleyici dünyayı yalnızca basit bir denklem, karmaşık sayılar ve bolca yineleme kullanarak bilgisayar ekranına taşır.

``

## Karmaşık düzlem ve yineleme

Karmaşık sayılar $z = x + yi$ biçiminde yazılır. Burada $x$ gerçek, $y$ sanal bileşendir ve $i^2 = -1$ eşitliği geçerlidir. Bu sayıları bir düzleme yerleştirdiğimizde yatay eksen gerçek, dikey eksen sanal kısmı temsil eder. Böylece her pikseli bir karmaşık sayıyla eşleştirebiliriz.

Mandelbrot ve Julia fraktallarının kalbinde şu şaşırtıcı derecede sade fonksiyon bulunur:

$$z_{n+1} = z_n^2 + c$$

Bir başlangıç değeri seçilir, denklem tekrar tekrar çalıştırılır ve oluşan dizinin davranışı gözlenir. Değerler sınırlı kalıyorsa ilgili nokta kümenin içinde, hızla büyüyorsa dışında kabul edilir. Karmaşık bir sayının büyüklüğü

$$\vert z\vert  = \sqrt{x^2 + y^2}$$

ile hesaplanır. Bu denklem için $\vert z\vert  > 2$ olduğunda dizinin sonsuza kaçacağı kesinleşir. Dolayısıyla bilgisayarın gerçekten sonsuza kadar hesap yapmasına gerek yoktur; aksi hâlde fraktalımız tamamlanana kadar birkaç çağ bekleyebilirdik.

## Mandelbrot ve Julia arasındaki fark

İki fraktal aynı fonksiyonu kullanır, ancak hangi değerin değişken tutulduğu konusunda ayrılır:

| Özellik | Mandelbrot Kümesi | Julia Kümesi |
|---|---|---|
| Başlangıç değeri | $z_0 = 0$ | Piksele göre değişir |
| $c$ değeri | Piksele göre değişir | Sabittir |
| Amaç | Hangi $c$ değerlerinin kararlı olduğunu bulmak | Belirli bir $c$ için başlangıçların davranışını görmek |
| Görsel karakter | Tek, bağlantılı ana yapı | $c$ değerine göre ada veya toz benzeri yapılar |

Bu nedenle Mandelbrot kümesi, Julia kümelerinin bir çeşit haritası gibi düşünülebilir. Mandelbrot kümesinin içinden seçilen $c$ değerleri çoğunlukla bağlantılı Julia kümeleri üretirken dışarıdan seçilenler parçalı desenlere yol açar.

## Kaçış zamanı algoritması

Bir noktanın kaçıp kaçmadığını anlamak için **kaçış zamanı algoritması** kullanılır. Her pikselde denklem belirli sayıda yinelenir. Nokta ne kadar geç kaçarsa sınıra o kadar yakındır. Renkler de kaçış turuna göre atanarak neon renkli kozmik brokoliler elde edilir.

Aşağıdaki Python programı Mandelbrot kümesini çizer:

```python
import numpy as np
import matplotlib.pyplot as plt

width, height = 800, 600
max_iter = 100

xs = np.linspace(-2.2, 1.0, width)
ys = np.linspace(-1.2, 1.2, height)
image = np.zeros((height, width))

for row, y in enumerate(ys):
    for col, x in enumerate(xs):
        c = complex(x, y)
        z = 0j

        for iteration in range(max_iter):
            z = z * z + c
            if abs(z) > 2:
                image[row, col] = iteration
                break
        else:
            image[row, col] = max_iter

plt.imshow(image, extent=[-2.2, 1.0, -1.2, 1.2],
           cmap="magma", origin="lower")
plt.axis("off")
plt.show()
```

Kod, düzlemdeki her pikseli $c$ olarak kullanır. `z` sıfırdan başlatılır; mutlak değer 2’yi geçtiğinde döngü durur ve kaçış turu görüntüye yazılır. `max_iter` yükseltildiğinde sınır bölgelerinde daha fazla detay görülür, fakat hesaplama süresi de artar.

## Julia kümesine dönüştürmek

Aynı kodu Julia üreticisine çevirmek için `c` sabitlenip `z` pikselden başlatılabilir:

```python
c = complex(-0.8, 0.156)
z = complex(x, y)
```

Geri kalan yineleme değişmez. Örneğin $c=-0.8+0.156i$ zarif ve kıvrımlı bir Julia kümesi oluşturur. Küçük bir parametre değişikliği bile görünümü dramatik biçimde dönüştürebilir.

Fraktalların asıl büyüsü, son derece basit kuralların öngörülmesi güç bir karmaşıklık üretmesidir. Yakınlaştırma yaptıkça ana şekle benzeyen fakat hiçbir zaman tamamen aynı olmayan yapılar belirir. Kısacası Mandelbrot ve Julia kümeleri, matematiğin yalnızca doğru cevaplar değil, sonsuz ayrıntılı sanat eserleri de üretebildiğinin renkli kanıtlarıdır.
