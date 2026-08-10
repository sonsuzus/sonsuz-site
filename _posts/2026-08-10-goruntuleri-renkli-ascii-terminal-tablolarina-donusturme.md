---
layout: post
title: "Görüntüleri Renkli ASCII Terminal Tablolarına Dönüştürme"
math: true
categories: 
  - Proje
tags: 
  - Python
  - ASCII Art
  - Terminal
  - Pillow
  - ANSI
---

Bir fotoğrafı terminalde yalnızca karakterler ve renklerle yeniden üretmek, nostaljik görünen ama oldukça öğretici bir görüntü işleme projesidir. Temel fikir basittir: Görüntüdeki her küçük piksel bölgesini, parlaklığı temsil eden bir ASCII karakterine ve o bölgenin rengini taşıyan ANSI kaçış koduna dönüştürürüz. Sonuç, terminal penceresinde çalışan mini bir renkli mozaiktir.
``
Bu dönüşümde en önemli kavram **örnekleme**dir. Modern fotoğraflar binlerce piksel genişliğinde olabilir; terminal ise sınırlı sayıda karakter hücresine sahiptir. Bu nedenle resmi önce hedef genişliğe küçültürüz. Her terminal karakteri yaklaşık olarak kare değil, dikeyde daha uzundur. Dolayısıyla görüntü yüksekliğini doğrudan orantılamak resmi gereğinden uzun gösterir. Pratik bir düzeltme formülü şöyledir:

$$h_{yeni} = h_{eski} \times \frac{w_{yeni}}{w_{eski}} \times k$$

Buradaki $k$ terminal yazı tipine bağlı en-boy düzeltme katsayısıdır; çoğu terminal için $0.45$ ile $0.60$ arası iyi bir başlangıçtır.

Karakter seçimi ise parlaklık üzerinden yapılır. RGB pikselini önce algısal parlaklığa indirgeriz. İnsan gözü yeşile kırmızı ve maviden daha duyarlı olduğundan basit ortalama yerine ağırlıklı yöntem daha iyi sonuç verir:

$$Y = 0.2126R + 0.7152G + 0.0722B$$

$Y$ değeri $0$ ile $255$ arasındadır. Koyu pikseller yoğun karakterlerle (`@`, `#`, `M`), açık pikseller ise seyrek karakterlerle (`.`, boşluk) temsil edilir. Böylece karakterin kapladığı mürekkep alanı görüntünün gölgelerini taklit eder.

| Aşama | Girdi | Çıktı | Amaç |
|---|---|---|---|
| Yeniden boyutlandırma | Büyük görsel | Terminal ölçekli görsel | Karakter sayısını yönetmek |
| Parlaklık hesabı | RGB piksel | $Y$ değeri | Uygun ASCII karakterini seçmek |
| Renk kodlama | RGB piksel | ANSI `38;2` kodu | Gerçek renge yakın görünüm |
| Satır üretimi | Karakterler | Terminal metni | Görüntüyü ekrana çizmek |

Aşağıdaki Python örneği, Pillow kütüphanesiyle bir görüntüyü True Color destekleyen terminaller için dönüştürür. `38;2;r;g;b` dizisi ön plan rengini RGB olarak belirler; ardından karakter yazılır ve renk sıfırlanır.

```python
from PIL import Image

PALETTE = "@%#*+=-:. "
RESET = "\033[0m"

def pixel_to_char(r, g, b):
    brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
    index = int(brightness / 255 * (len(PALETTE) - 1))
    return PALETTE[index]

def image_to_ascii(path, width=80):
    image = Image.open(path).convert("RGB")
    old_width, old_height = image.size
    height = int(old_height * width / old_width * 0.5)
    image = image.resize((width, max(1, height)))

    for y in range(image.height):
        line = []
        for x in range(image.width):
            r, g, b = image.getpixel((x, y))
            char = pixel_to_char(r, g, b)
            line.append(f"\033[38;2;{r};{g};{b}m{char}")
        print("".join(line) + RESET)

image_to_ascii("manzara.jpg", width=100)
```

Kodun karakter paleti koyudan açığa sıralıdır. Bu sıralama ters olursa negatif fotoğraf benzeri bir etki elde edilir. Ayrıca her piksel için ANSI kodu üretmek, özellikle geniş görsellerde terminal çıktısını büyütür. Aynı renkte art arda gelen karakterlerde rengi tekrar yazmamak küçük bir optimizasyondur.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Gri tonlu ASCII | Hızlı, her terminalde okunur | Renk bilgisi kaybolur |
| 16 renk ANSI | Eski terminallerle uyumlu | Renkler kaba görünür |
| 24-bit True Color | Fotoğrafa yakın sonuç | Terminal desteği gerekir |

Projeyi geliştirmek için kontrast ayarı, kenar algılama veya piksel yerine küçük blokların ortalama rengini alma eklenebilir. En etkileyici sonuçlar, belirgin ışık-gölge farkı bulunan portreler ve manzara fotoğraflarında ortaya çıkar. Terminaliniz bir tuval olmayabilir; ama doğru karakterler seçildiğinde şaşırtıcı derecede iyi bir ressamdır.
