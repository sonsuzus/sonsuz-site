---
layout: post
title: "Prosedürel Zindan Üretimi: Hücresel Otomata mı, BSP mi?"
math: true
categories: 
  - Bilgi
tags: 
  - prosedürel üretim
  - hücresel otomata
  - bsp
  - oyun geliştirme
  - algoritma
  - zindan tasarımı
toc: true
image: /img/prosedurel-zindan-uretimi-30.png
---

Bir zindanı elle tasarlamak keyiflidir; yüzüncü zindanı tasarlamak ise insanı duvarlarla konuşmaya başlatabilir. Prosedürel üretim algoritmaları, belirli kurallardan yararlanarak her oyun oturumunda farklı haritalar oluşturur. Hücresel otomata doğal mağaralar üretirken Binary Space Partitioning, yani BSP, düzenli odalar ve koridorlar konusunda parlar. Peki projeniz için hangisini seçmelisiniz?

``

## Temel problem: Rastgelelik mi, oynanabilirlik mi?

Bir harita $W \times H$ boyutlarında hücrelerden oluşsun. En basit temsil şöyledir:

$$M(x,y) \in \{0,1\}$$

Burada $0$ yürünebilir zemini, $1$ ise duvarı gösterebilir. Algoritmanın görevi yalnızca hücreleri doldurmak değildir; bağlantılı, dengeli ve oyun mekaniğine uygun bir düzen üretmektir. Tam rastgele dağılım çoğunlukla kopuk odalar, erişilemeyen bölgeler ve anlamsız duvar kümeleri doğurur. Bu nedenle kontrollü rastgelelik gerekir.

## Hücresel otomata: Mağaraların mimarı

Hücresel otomata önce her hücreyi belirli bir olasılıkla duvar yapar. Ardından komşulara bakarak haritayı birkaç tur yumuşatır. Bir hücrenin sonraki durumu kabaca şöyle tanımlanabilir:

$$M_{t+1}(x,y)=\begin{cases}1, & N_t(x,y) \geq T \\ 0, & N_t(x,y)<T\end{cases}$$

$N_t$, çevredeki duvar sayısını; $T$ ise eşik değerini temsil eder. Örneğin sekiz komşudan en az beşi duvarsa merkez hücre de duvara dönüşür.

```python
import random

def cellular_step(grid, threshold=5):
    height, width = len(grid), len(grid[0])
    result = [[1] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            walls = sum(
                grid[y + dy][x + dx]
                for dy in (-1, 0, 1)
                for dx in (-1, 0, 1)
                if (dx, dy) != (0, 0)
            )
            result[y][x] = 1 if walls >= threshold else 0
    return result
```

Bu fonksiyon tek bir yumuşatma turu uygular. Üç ila altı tur genellikle organik boşluklar oluşturur. Ancak sonuçların bağlantılı olduğu garanti edilmez. Flood fill ile erişilemeyen bölgeleri tespit etmek ve küçük alanları kapatmak gerekebilir.

## BSP: Düzen seven zindan ustası

BSP, haritayı dikdörtgen bölgelere ayırır. Her bölge yeterince büyükse yatay veya dikey olarak ikiye bölünür. Yaprak bölgelerin içine odalar yerleştirilir; ardından kardeş bölgelerdeki odalar koridorlarla bağlanır.

Bir bölgenin alanı $A=w \cdot h$ olsun. Bölme işlemi, $A$ belirlenen minimum oda alanından büyük olduğu sürece devam eder. En-boy oranına bakmak aşırı ince bölgeleri önler.

```python
def split(rect, min_size=12):
    x, y, w, h = rect
    if w < min_size * 2 and h < min_size * 2:
        return [rect]

    if w > h and w >= min_size * 2:
        cut = random.randint(min_size, w - min_size)
        return [(x, y, cut, h), (x + cut, y, w - cut, h)]

    if h >= min_size * 2:
        cut = random.randint(min_size, h - min_size)
        return [(x, y, w, cut), (x, y + cut, w, h - cut)]

    return [rect]
```

Kod, tek bir dikdörtgeni güvenli ölçülerde iki parçaya ayırır. Gerçek üretimde fonksiyon yapraklara özyinelemeli uygulanır; odalar küçültülerek bölge sınırlarından pay bırakılır.

## Yöntemlerin karşılaştırması

| Özellik | Hücresel otomata | BSP |
|---|---|---|
| Görsel karakter | Organik ve mağaramsı | Geometrik ve mimari |
| Bağlantı garantisi | Doğrudan yok | Koridorlarla kolay |
| Parametreler | Duvar olasılığı, eşik, tur | Minimum boyut, bölme yönü |
| Oda kontrolü | Düşük | Yüksek |
| Uygun türler | Roguelike, hayatta kalma | RPG, taktik, klasik dungeon |
| Son işlem ihtiyacı | Genellikle yüksek | Genellikle orta |

![prosedurel-zindan-uretimi-30](/img/prosedurel-zindan-uretimi-30.svg)


## Hangisini seçmeli?

Doğal mağaralar, belirsiz görüş hatları ve keşif hissi istiyorsanız hücresel otomata güçlü bir tercihtir. Anahtar odaları, boss alanlarını ve görev rotalarını hassas biçimde konumlandırmanız gerekiyorsa BSP daha öngörülebilir davranır.

İki yöntemi birleştirmek de mümkündür: Önce BSP ile bağlantılı ana odaları kurabilir, ardından bazı bölgelerin içini hücresel otomata ile aşındırabilirsiniz. Böylece BSP’nin oynanabilirlik garantisi ile hücresel otomatanın organik görünümü birleşir. Kısacası en iyi algoritma evrensel değildir; oyununuzun mekânsal ihtiyaçlarını en az son işlemle karşılayan algoritmadır.
