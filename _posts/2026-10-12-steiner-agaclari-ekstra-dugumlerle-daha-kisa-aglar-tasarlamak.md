---
layout: post
title: "Steiner Ağaçları: Ekstra Düğümlerle Daha Kısa Ağlar Tasarlamak"
math: true
categories: 
  - Bilgi
tags: 
  - steiner ağacı
  - graf teorisi
  - optimizasyon
  - algoritma
  - python
  - hesaplamalı geometri
toc: true
image: /img/steiner-agaclari-ekstra-61.png
---

Bir grup şehri yollarla, bilgisayarı kablolarla veya elektronik bileşenleri iletken hatlarla bağlamak istediğinizi düşünün. İlk akla gelen çözüm, verilen noktalar arasında en kısa bağlantıları seçmektir. Steiner Ağacı Problemi ise daha yaratıcı davranır: Ağa yeni kavşaklar ekleyerek toplam uzunluğu daha da azaltabilir. Kısacası bazen hedefe daha kısa yoldan ulaşmak için önce yeni bir durak inşa etmek gerekir!

``

## Steiner Ağacı nedir?

Elimizde terminal adı verilen bir nokta kümesi olsun:

$$T = \{t_1, t_2, \ldots, t_n\}$$

Amaç, bütün terminalleri birbirine bağlayan ve toplam kenar uzunluğu minimum olan bir ağaç bulmaktır. Minimum Örten Ağaç (MST) yalnızca verilen noktaları kullanırken Steiner Ağacı, çözümü kısaltmak için **Steiner noktaları** denilen ekstra düğümler ekleyebilir.

Bir ağacın toplam maliyeti şöyle ifade edilir:

$$L(G) = \sum_{e \in E(G)} w(e)$$

Burada $E(G)$ ağacın kenarlarını, $w(e)$ ise ilgili kenarın uzunluğunu gösterir. Aradığımız çözüm, tüm terminalleri bağlayan ağaçlar arasında $L(G)$ değerini en aza indirendir.

| Özellik | Minimum Örten Ağaç | Steiner Ağacı |
|---|---|---|
| Kullanılan düğümler | Yalnızca verilen noktalar | Verilen ve eklenen noktalar |
| Çözüm kalitesi | Genellikle daha uzun | Eşit veya daha kısa |
| Hesaplama zorluğu | Polinom zamanda çözülebilir | Genel durumda NP-zor |
| Kullanım alanı | Basit ağ bağlantıları | Kablo, yol ve devre tasarımı |

![steiner-agaclari-ekstra-61](/img/steiner-agaclari-ekstra-61.svg)


## Neden 120 derece ortaya çıkar?

Öklid düzlemindeki ideal bir Steiner noktasına çoğunlukla üç kenar bağlanır ve bu kenarlar arasındaki açılar $120^\circ$ olur. Bunun nedeni kuvvet dengesi gibi düşünülebilir. Steiner noktasından çıkan üç birim yön vektörü $u_1$, $u_2$ ve $u_3$ için optimum durumda:

$$u_1 + u_2 + u_3 = 0$$

Üç eşit büyüklükte vektörün toplamının sıfır olması, aralarında $120^\circ$ bulunmasını gerektirir. Böylece düğümü herhangi bir yöne hareket ettirmek toplam mesafeyi ilk anda azaltmaz.

Üç terminal bir eşkenar üçgen oluşturuyorsa MST iki kenar kullanır ve toplam uzunluk $2a$ olur. Merkeze bir Steiner noktası eklendiğinde uzunluk $a\sqrt{3}$ değerine düşer. Çünkü $\sqrt{3} \approx 1{,}732$ olduğundan yeni kavşak gerçekten tasarruf sağlar.

## Basit bir sayısal yaklaşım

Aşağıdaki Python kodu, üç terminal için Steiner noktasını yaklaşık olarak arar. Bu yöntem matematiksel olarak en hızlı çözüm değildir; fakat toplam uzaklığın nasıl optimize edildiğini görmek için öğreticidir.

```python
import math

points = [(0, 0), (6, 0), (3, 5.2)]

def total_distance(x, y):
    return sum(math.hypot(x - px, y - py) for px, py in points)

x = sum(p[0] for p in points) / len(points)
y = sum(p[1] for p in points) / len(points)
step = 1.0

while step > 1e-5:
    candidates = [
        (x + dx, y + dy)
        for dx, dy in [(step, 0), (-step, 0),
                       (0, step), (0, -step)]
    ]
    best = min(candidates, key=lambda p: total_distance(*p))

    if total_distance(*best) < total_distance(x, y):
        x, y = best
    else:
        step /= 2

print('Steiner noktası:', round(x, 3), round(y, 3))
print('Toplam uzunluk:', round(total_distance(x, y), 3))
```

Kod önce terminallerin koordinat ortalamasından başlar. Dört yönde küçük hareketler deneyerek toplam uzaklığı azaltan konuma ilerler; iyileşme kalmadığında adım boyutunu küçültür. Bu, sezgisel bir yerel arama örneğidir.

## Gerçek dünyada neden önemlidir?

Steiner ağaçları telekomünikasyon hatlarında, çiplerin iletken yollarında, boru sistemlerinde ve ulaşım ağlarında kullanılabilir. Ancak problem NP-zor olduğu için büyük örneklerde kesin çözüm pahalıdır. Dinamik programlama, tamsayılı programlama, yaklaşım algoritmaları ve sezgisel yöntemler sıkça tercih edilir.

Steiner Ağacı Problemi bize önemli bir optimizasyon dersi verir: Sisteme yeni bir bileşen eklemek ilk bakışta maliyet gibi görünse de bütünün maliyetini azaltabilir. Bazen en iyi bağlantı, mevcut noktalar arasında değil, henüz var olmayan akıllıca seçilmiş bir kavşaktan geçer.
