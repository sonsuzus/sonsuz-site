---
layout: post
title: "Taşımacılık Problemi: En Düşük Maliyetli Dağıtımın Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - optimizasyon
  - taşımacılık problemi
  - yöneylem araştırması
  - doğrusal programlama
  - python
  - lojistik
toc: true
image: /img/tasimacilik-problemi-en-93.png
---

![tasimacilik-problemi-en-93](/img/tasimacilik-problemi-en-93.svg)


Bir fabrikanın ürünlerini farklı şehirlere göndermek kolay görünebilir: Kamyonları doldur, adresleri belirle ve yola çık! Fakat birden fazla üretim merkezi, değişen talepler ve farklı taşıma maliyetleri devreye girdiğinde işler hızla karmaşıklaşır. **Taşımacılık problemi**, kaynakların hedeflere ihtiyaçları karşılayacak biçimde ve mümkün olan en düşük toplam maliyetle dağıtılmasını sağlayan özel bir doğrusal programlama modelidir.
``

## Problemin temel bileşenleri

Modelde belirli miktarda ürüne sahip **kaynaklar** ve ürüne ihtiyaç duyan **hedefler** bulunur. Her kaynak-hedef çifti için birim taşıma maliyeti tanımlanır. Karar vermemiz gereken konu, hangi kaynaktan hangi hedefe kaç birim ürün gönderileceğidir.

Örneğin iki fabrika ve üç depo düşünelim:

| Kaynak | İstanbul | Ankara | İzmir | Kapasite |
|---|---:|---:|---:|---:|
| Fabrika A | 4 TL | 6 TL | 8 TL | 100 |
| Fabrika B | 5 TL | 3 TL | 7 TL | 150 |
| Talep | 80 | 90 | 80 | 250 |

Tablodaki sayılar bir birim ürünün taşıma maliyetidir. En ucuz hücreleri doğrudan seçmek her zaman doğru sonuç vermez; çünkü fabrika kapasiteleri ve depo talepleri birlikte değerlendirilmelidir. Ankara'ya fazla ürün gönderirsek İstanbul'un talebini karşılayacak yeterli kapasite kalmayabilir. Optimizasyonun sihri tam burada başlar.

## Matematiksel model

$i$ kaynakları, $j$ hedefleri temsil etsin. $x_{ij}$, $i$ kaynağından $j$ hedefine gönderilen ürün miktarı; $c_{ij}$ ise birim taşıma maliyeti olsun. Amaç fonksiyonu şöyledir:

$$
\min Z = \sum_{i=1}^{m}\sum_{j=1}^{n} c_{ij}x_{ij}
$$

Bu ifade, tüm rotalardaki miktar ile birim maliyet çarpımlarını toplar ve sonucu küçültmeye çalışır. Her kaynağın kapasitesini aşmamak için:

$$
\sum_{j=1}^{n}x_{ij} = a_i
$$

Her hedefin talebini karşılamak için de:

$$
\sum_{i=1}^{m}x_{ij} = b_j
$$

kısıtları kullanılır. Ayrıca negatif miktarda ürün gönderilemeyeceğinden $x_{ij} \geq 0$ olmalıdır.

## Dengeli ve dengesiz modeller

| Model | Koşul | Yapılacak işlem |
|---|---|---|
| Dengeli | Toplam arz = Toplam talep | Model doğrudan çözülür |
| Arz fazlası | Toplam arz > Toplam talep | Sahte hedef eklenir |
| Talep fazlası | Toplam arz < Toplam talep | Sahte kaynak eklenir |

Sahte kaynak veya hedefin taşıma maliyeti genellikle sıfır seçilir. Böylece matematiksel denge sağlanırken kullanılmayan kapasite ya da karşılanamayan talep görünür hâle gelir.

## Başlangıç çözümü ve iyileştirme

Taşımacılık problemlerinde başlangıç çözümü üretmek için **Kuzeybatı Köşe**, **En Düşük Maliyet** ve **Vogel Yaklaşım** yöntemleri kullanılabilir. Kuzeybatı Köşe yöntemi hızlıdır ancak maliyetleri dikkate almaz. En Düşük Maliyet yöntemi ucuz hücrelerden başlar. Vogel yöntemi ise satır ve sütunlardaki maliyet farklarını değerlendirerek çoğunlukla daha kaliteli bir başlangıç çözümü oluşturur.

| Yöntem | Hız | Başlangıç çözümü kalitesi |
|---|---|---|
| Kuzeybatı Köşe | Çok yüksek | Genellikle düşük |
| En Düşük Maliyet | Yüksek | Orta |
| Vogel | Orta | Genellikle yüksek |

Başlangıç çözümü daha sonra MODI veya Atlama Taşı yöntemiyle iyileştirilebilir. Günümüzde bu işlemler çoğunlukla optimizasyon kütüphanelerine bırakılır.

## Python ile çözüm

Aşağıdaki kod, örnek problemi SciPy'nin `linprog` fonksiyonuyla çözer:

```python
import numpy as np
from scipy.optimize import linprog

maliyet = np.array([4, 6, 8, 5, 3, 7])

# Her fabrikanın göndereceği toplam miktar
A_fabrika = np.array([
    [1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1]
])

# Her deponun alacağı toplam miktar
A_depo = np.array([
    [1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1]
])

A_eq = np.vstack([A_fabrika, A_depo])
b_eq = np.array([100, 150, 80, 90, 80])

sonuc = linprog(maliyet, A_eq=A_eq, b_eq=b_eq,
                bounds=(0, None), method="highs")

print("Dağıtım planı:", sonuc.x.reshape(2, 3))
print("Toplam maliyet:", sonuc.fun)
```

Kodda altı karar değişkeni iki fabrikanın üç depoya yapacağı sevkiyatları temsil eder. Eşitlik kısıtları kapasite ve talepleri sabitler; `bounds` ise negatif sevkiyatı engeller. Çözüm yalnızca ucuz rotaları değil, bütün sistemin toplam maliyetini dikkate alır.

Taşımacılık modeli; lojistik, personel atama, enerji dağıtımı ve veri merkezleri arasında iş yükü paylaşımı gibi pek çok alana uyarlanabilir. Kısacası mesele sadece kamyon göndermek değil, sınırlı kaynaklarla akıllıca yol almaktır.
