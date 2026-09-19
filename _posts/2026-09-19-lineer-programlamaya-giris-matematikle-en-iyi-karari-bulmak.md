---
layout: post
title: "Lineer Programlamaya Giriş: Matematikle En İyi Kararı Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - lineer programlama
  - optimizasyon
  - matematik
  - python
  - yöneylem araştırması
toc: true
---

Bir fabrikanın hangi üründen kaç tane üretmesi gerektiğini, bir kargo şirketinin araçlarını nasıl dağıtacağını veya sınırlı bütçenin projeler arasında nasıl paylaştırılacağını düşünün. Bütün bu soruların ortak noktası, belirli kısıtlar altında **en iyi kararı** aramalarıdır. Lineer programlama, matematiği adeta bir karar verme pusulasına dönüştürerek bu tür optimizasyon problemlerini sistematik biçimde çözmemizi sağlar.

``

## Lineer programlama nedir?

Lineer programlama; bir amaç fonksiyonunu, doğrusal eşitlik veya eşitsizliklerle tanımlanan kısıtlar altında en büyük ya da en küçük yapma yöntemidir. Buradaki “programlama” sözcüğü kod yazmaktan çok **planlama** anlamına gelir.

Bir lineer programlama modeli üç temel bileşenden oluşur:

| Bileşen | Görevi | Örnek |
|---|---|---|
| Karar değişkenleri | Kontrol edilecek miktarları gösterir | Üretilecek masa ve sandalye sayısı |
| Amaç fonksiyonu | Optimize edilmek istenen sonucu tanımlar | Toplam kârı büyütmek |
| Kısıtlar | Kaynak ve iş kurallarını ifade eder | Ahşap, süre veya bütçe sınırı |

Karar değişkenlerini $x_1, x_2, \ldots, x_n$ ile gösterirsek genel bir maksimizasyon modeli şöyledir:

$$
\max Z = c_1x_1 + c_2x_2 + \cdots + c_nx_n
$$

Kısıtlar ise matris gösterimiyle kısaca aşağıdaki biçimde yazılabilir:

$$
Ax \le b, \qquad x \ge 0
$$

Burada $c$ katkı veya maliyet katsayılarını, $A$ kaynak kullanım oranlarını, $b$ mevcut kaynakları temsil eder. $x \ge 0$ koşulu, negatif üç masa üretmek gibi matematiksel fakat gerçek hayatta biraz tuhaf sonuçları engeller.

## Küçük bir üretim modeli

Bir atölye masa ve sandalye üretsin. Bir masa 60 TL, bir sandalye 40 TL kâr sağlıyor olsun. Masa için 4 saat, sandalye için 2 saat işçilik gerekiyor ve toplam 40 saat mevcut. Ayrıca en fazla 12 ürün üretilebiliyor.

$x$: masa sayısı, $y$: sandalye sayısı olsun. Modelimiz:

$$
\max Z = 60x + 40y
$$

$$
4x + 2y \le 40
$$

$$
x + y \le 12
$$

$$
x,y \ge 0
$$

İki değişkenli modeller grafik yöntemiyle çözülebilir. Her kısıt düzlemde bir doğru oluşturur; bütün koşulları sağlayan ortak bölgeye **uygun çözüm bölgesi** denir. Lineer amaç fonksiyonu optimum değerine bu bölgenin köşe noktalarından en az birinde ulaşır. Bu özellik, yüzlerce değişkenli problemlerde kullanılan Simpleks algoritmasının da temel sezgisidir.

| Yöntem | Güçlü yanı | Uygun olduğu durum |
|---|---|---|
| Grafik yöntemi | Görsel ve öğreticidir | İki karar değişkeni |
| Simpleks | Köşe noktaları arasında ilerler | Orta ve büyük modeller |
| İç nokta yöntemleri | Büyük sistemlerde verimlidir | Çok sayıda değişken ve kısıt |

## Python ile modeli çözelim

PuLP kütüphanesi, matematiksel modeli okunabilir biçimde koda aktarmamızı sağlar:

```python
from pulp import LpMaximize, LpProblem, LpVariable, value

model = LpProblem("Atolye_Plani", LpMaximize)

x = LpVariable("masa", lowBound=0)
y = LpVariable("sandalye", lowBound=0)

model += 60 * x + 40 * y       # Toplam kâr
model += 4 * x + 2 * y <= 40   # İşçilik sınırı
model += x + y <= 12           # Kapasite sınırı

model.solve()

print("Masa:", x.value())
print("Sandalye:", y.value())
print("Kâr:", value(model.objective))
```

Çözüm $x=8$, $y=4$ ve $Z=640$ verir. Yani kaynakları en kârlı kullanan plan sekiz masa ve dört sandalye üretmektir. Değişkenlerin tam sayı olması zorunluysa `cat="Integer"` parametresi eklenebilir; bu durumda model artık tamsayılı lineer programlama sınıfına girer.

## Her problem lineer midir?

Bir modelin lineer olabilmesi için değişkenler birbirleriyle çarpılmamalı, üsleri bir olmalı ve katsayılar sabit kalmalıdır. Örneğin $3x+2y$ lineerken, $xy$, $x^2$ ve değişken faiz oranları doğrusal değildir.

Lineer programlama yalnızca bir formül koleksiyonu değil, karmaşık kararları açık varsayımlara dönüştüren bir düşünme biçimidir. Değişkenleri doğru seçmek, kısıtları eksiksiz kurmak ve sonucu gerçek hayat açısından yorumlamak; çoğu zaman algoritmayı çalıştırmaktan daha önemlidir.
