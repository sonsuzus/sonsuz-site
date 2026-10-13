---
layout: post
title: "Paketleme Problemleri: Çemberleri ve Kareleri Alana Sığdırma Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - paketleme
  - geometri
  - optimizasyon
  - algoritma
  - python
  - matematik
toc: true
image: /img/paketleme-problemleri-cemberleri-47.png
---

Bir valize kıyafet, depoya kutu ya da işlemci üzerine transistör yerleştirirken aynı soruyla karşılaşırız: Sınırlı bir alanı nasıl daha verimli kullanabiliriz? Paketleme problemleri, basit görünen şekillerin şaşırtıcı derecede karmaşık düzenler oluşturduğu optimizasyon problemleridir. Özellikle çember ve kare paketleme; matematikten lojistiğe, üretimden bilgisayar bilimlerine kadar pek çok alanda karşımıza çıkar.
``

## Paketleme ve kaplama aynı şey mi?

İki kavram birbirine benzese de hedefleri farklıdır. **Paketleme**, şekilleri üst üste bindirmeden belirli bir bölgeye sığdırmaya çalışır. **Kaplama** ise bölgenin tamamını şekillerle örtmeyi amaçlar; şekillerin çakışmasına izin verilebilir.

| Problem | Temel hedef | Çakışma | Örnek |
|---|---|---|---|
| Paketleme | Alana en fazla şekli yerleştirmek | Yasak | Kutuların kamyona yüklenmesi |
| Kaplama | Alanın tamamını örtmek | Genellikle serbest | Sensörlerin bir bölgeyi izlemesi |
| Bölümleme | Boşluk ve çakışma bırakmamak | Yasak | Zeminin fayansla döşenmesi |

![paketleme-problemleri-cemberleri-47](/img/paketleme-problemleri-cemberleri-47.svg)


Paketleme verimliliği, şekillerin toplam alanının taşıyıcı bölgenin alanına oranıyla ölçülür:

$$
\eta = \frac{A_{şekiller}}{A_{bölge}}
$$

Burada $0 \leq \eta \leq 1$ olur. Oran büyüdükçe boş alan azalır.

## Çember paketlemenin geometrisi

Yarıçapı $r$ olan bir çemberin alanı $\pi r^2$ değerindedir. Çemberleri kare ızgara üzerinde dizersek her çember, kenarı $2r$ olan hayali bir hücrede bulunur. Bu düzenin yoğunluğu:

$$
\eta_{kare} = \frac{\pi r^2}{(2r)^2} = \frac{\pi}{4} \approx 0.785
$$

Ancak çemberleri bal peteğine benzeyen **altıgensel düzende** yerleştirmek daha verimlidir:

$$
\eta_{altıgen} = \frac{\pi}{2\sqrt{3}} \approx 0.907
$$

Yani sonsuz bir düzlemde alanın yaklaşık yüzde 90,7’si doldurulabilir. Portakal kasalarındaki çapraz dizilim tesadüf değildir! Bununla birlikte sonlu bir kutuda kenar etkileri ortaya çıkar. Kutunun sınırındaki çemberler ideal komşuluk düzenini sürdüremediği için en iyi teorik yoğunluğa her zaman ulaşılamaz.

## Kareler neden daha uysal?

Eş kareler, kenarları paralel yerleştirildiğinde boşluk bırakmadan düzlemi kaplayabilir. Bir karenin kenarı $a$ ise alanı $a^2$ olur ve uygun boyutlu dikdörtgenlerde $\eta=1$ elde edilebilir. Fakat taşıyıcı bölgenin ölçüleri $a$ değerinin tam katı değilse kenarlarda kullanılmayan şeritler kalır.

| Şekil | İdeal yoğunluk | Tipik dizilim | Temel zorluk |
|---|---:|---|---|
| Çember | Yaklaşık %90,7 | Altıgensel | Eğri sınırlar arasında boşluk |
| Kare | %100 | Izgara | Bölge boyutları ve döndürme |

Farklı boyutlarda kareler kullanıldığında problem hızla zorlaşır. Hangi karenin önce yerleştirileceği, döndürülüp döndürülmeyeceği ve kalan boşluğun nasıl değerlendirileceği kombinatoryal bir aramaya dönüşür.

## Bilgisayarla basit bir çember yerleştirme

Aşağıdaki Python kodu, dikdörtgen içine eş yarıçaplı çemberleri kare ızgara düzeninde yerleştirir. Her merkez, sınırlardan en az yarıçap kadar uzakta tutulur:

```python
def circle_grid(width, height, radius):
    centers = []
    diameter = 2 * radius
    y = radius

    while y <= height - radius:
        x = radius
        while x <= width - radius:
            centers.append((x, y))
            x += diameter
        y += diameter

    circle_area = len(centers) * 3.14159 * radius ** 2
    efficiency = circle_area / (width * height)
    return centers, efficiency

centers, ratio = circle_grid(20, 12, 1)
print(len(centers), round(ratio, 3))
```

Bu yöntem hızlıdır fakat her zaman en iyi sonucu vermez. Altıgensel yerleşim, satırları yatayda $r$ kadar kaydırarak daha fazla çember sığdırabilir. Daha karmaşık örneklerde açgözlü algoritmalar, geri izleme, benzetimli tavlama ve genetik algoritmalar kullanılabilir.

## Neden tek bir mükemmel algoritma yok?

Paketleme problemlerinde şekil boyutları, dönüş açıları ve taşıyıcı sınırları değiştikçe olası düzenlerin sayısı muazzam biçimde artar. Bu nedenle pratik uygulamalarda kesin çözüm yerine kısa sürede kaliteli sonuç üreten sezgisel yöntemler tercih edilir. Kısacası iyi paketleme, yalnızca boşluğu doldurmak değil; geometri, hesaplama maliyeti ve gerçek dünya kısıtları arasında akıllı bir denge kurmaktır.
