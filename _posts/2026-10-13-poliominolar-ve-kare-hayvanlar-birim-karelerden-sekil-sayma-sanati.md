---
layout: post
title: "Poliominolar ve Kare Hayvanlar: Birim Karelerden Şekil Sayma Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - poliomino
  - kombinatorik
  - algoritma
  - matematik
  - python
  - ızgara
toc: true
image: /img/poliominolar-ve-kare-16.png
---

![poliominolar-ve-kare-16](/img/poliominolar-ve-kare-16.svg)


Bir avuç birim kareyi kenarlarından birleştirerek kaç farklı şekil oluşturabilirsiniz? İlk bakışta çocuk oyuncağı gibi görünen bu soru, kombinatorik ve algoritma dünyasında şaşırtıcı derecede derin bir probleme dönüşür. Poliominolar, diğer adıyla kare hayvanlar, basit kurallardan karmaşık sayma problemlerinin nasıl doğduğunu gösteren harika matematiksel canlılardır.
``

## Poliominonun anatomisi

Bir **poliomino**, kenarları boyunca birbirine bağlı birim karelerin birleşimidir. Yalnızca köşeden temas eden kareler bağlı sayılmaz. Kare sayısı $n$ ise şekle $n$-omino denir: $n=1$ monomino, $n=2$ domino, $n=3$ tromino ve $n=4$ tetrominodur.

Bir şekli koordinat kümesiyle ifade edebiliriz. Örneğin L-tromino:

$$P = \{(0,0), (1,0), (0,1)\}$$

Bu temsil, çizimleri bilgisayarın karşılaştırabileceği verilere dönüştürür. Ancak “farklı” kelimesinin anlamını belirlemeden saymaya başlayamayız.

| Sayma türü | Öteleme | Döndürme | Yansıtma |
|---|---:|---:|---:|
| Sabit poliomino | Aynı kabul edilir | Farklı | Farklı |
| Tek yüzlü poliomino | Aynı | Aynı | Farklı |
| Serbest poliomino | Aynı | Aynı | Aynı |

Örneğin serbest tetrominoların sayısı 5’tir; bunlar Tetris’ten tanıdığımız I, O, T, L ve S aileleridir. Sabit sayımda farklı yönelimler ayrı tutulduğu için sonuç daha büyüktür.

## Sistematik üretim fikri

En güvenilir yaklaşım, $n$ kareli her şekilden komşu boş hücrelere bir kare ekleyerek $n+1$ kareli adaylar üretmektir. Bir hücrenin dört kenar komşusu

$$N(x,y)=\{(x+1,y),(x-1,y),(x,y+1),(x,y-1)\}$$

kümesiyle verilir. Sorun, aynı şeklin farklı büyüme yollarıyla defalarca oluşmasıdır. Çözüm **kanonikleştirme** işlemidir.

Önce şekil, en küçük $x$ ve $y$ koordinatları sıfır olacak biçimde ötelenir. Serbest poliominolar sayılıyorsa sekiz simetri—dört döndürme ve bunların yansımaları—üretilir. Her temsil sıralanır; sözlük sırasına göre en küçük olan şeklin kimliği seçilir.

```python
def normalize(cells):
    min_x = min(x for x, y in cells)
    min_y = min(y for x, y in cells)
    return tuple(sorted((x - min_x, y - min_y) for x, y in cells))

def transforms(cells):
    variants = []
    current = list(cells)
    for _ in range(4):
        variants.append(normalize(current))
        variants.append(normalize([(-x, y) for x, y in current]))
        current = [(-y, x) for x, y in current]
    return variants

def canonical(cells):
    return min(transforms(cells))
```

Bu kod, bir şeklin döndürülmüş veya aynalanmış kopyalarını aynı anahtara indirger. Böylece adayları bir `set` içinde saklamak tekrarları otomatik olarak eler.

## Büyüterek sayma

```python
def generate(n):
    shapes = {canonical({(0, 0)})}
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for size in range(1, n):
        new_shapes = set()
        for shape in shapes:
            cells = set(shape)
            for x, y in cells:
                for dx, dy in directions:
                    candidate = (x + dx, y + dy)
                    if candidate not in cells:
                        new_shapes.add(canonical(cells | {candidate}))
        shapes = new_shapes
    return shapes
```

Algoritma anlaşılırdır fakat $n$ büyüdükçe aday sayısı hızla artar. Serbest poliomino sayıları $1,1,2,5,12,35,108,369,1285,4655,\ldots$ şeklinde ilerler. Genel kapalı formül bilinmez; yaklaşık büyüme $a_n \approx C\mu^n n^{-\theta}$ biçiminde incelenir.

Daha büyük örneklerde Redelmeier algoritması, sınır hücrelerini kontrollü biçimde gezerek tekrar üretimini azaltır. Simetri sayımında Burnside Lemması da kullanılabilir:

$$\vert X/G\vert =\frac{1}{\vert G\vert }\sum_{g\in G}\vert \mathrm{Fix}(g)\vert $$

Kısacası kare hayvanlar; koordinat modelleme, grafik bağlantısı, simetri grupları ve verimli arama tekniklerini aynı oyun alanında buluşturur. Birkaç kareyle başlayan macera, bilgisayarların bile dikkatle saymak zorunda olduğu gerçek bir algoritma safarisidir.
