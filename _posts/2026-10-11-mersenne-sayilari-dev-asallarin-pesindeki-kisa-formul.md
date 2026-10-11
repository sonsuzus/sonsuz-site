---
layout: post
title: "Mersenne Sayıları: Dev Asalların Peşindeki Kısa Formül"
math: true
categories: 
  - Bilgi
tags: 
  - mersenne
  - asal sayılar
  - sayı teorisi
  - python
  - algoritma
  - matematik
toc: true
image: /img/mersenne-sayilari-dev-74.png
---

Bir sayının milyonlarca basamağı varsa onun asal olup olmadığını nasıl anlarsınız? Bütün bölenleri sırayla denemek, evrendeki sabrı tüketebilecek kadar pahalıdır. Neyse ki Mersenne sayıları, özel biçimleri sayesinde büyük asal arayışını ulaşılabilir hâle getirir. Üstelik bu arayış, sayı teorisinden dağıtık hesaplamaya uzanan heyecanlı bir maceradır.
``

## Mersenne sayısı nedir?

Bir Mersenne sayısı, pozitif bir $p$ tam sayısı için şu biçimde tanımlanır:

$$M_p = 2^p - 1$$

Örneğin $p=5$ seçilirse $M_5=2^5-1=31$ elde edilir ve 31 asaldır. Ancak formüle uyan her sayı asal değildir. $p=11$ için sonuç $2047$ olur; kulağa iddialı gelse de $2047=23 \times 89$ olduğundan bileşiktir.

Mersenne sayısının asal olabilmesi için $p$ değerinin asal olması zorunludur. Çünkü $p=ab$ biçiminde bileşikse:

$$2^{ab}-1=(2^a-1)(2^{a(b-1)}+2^{a(b-2)}+...+1)$$

Bu çarpanlara ayırma, $M_p$ sayısının da bileşik olduğunu gösterir. Fakat dikkat: $p$ değerinin asal olması yeterli değil, yalnızca gerekli bir koşuldur.

| Üs $p$ | $M_p$ | Sonuç |
|---:|---:|---|
| 2 | 3 | Asal |
| 3 | 7 | Asal |
| 5 | 31 | Asal |
| 7 | 127 | Asal |
| 11 | 2047 | Bileşik |
| 13 | 8191 | Asal |

![mersenne-sayilari-dev-74](/img/mersenne-sayilari-dev-74.svg)


## Neden asallık testlerinde özeller?

Genel amaçlı asallık testleri her tam sayıyla ilgilenmek zorundadır. Mersenne sayılarıysa ikilik sistemde yalnızca birlerden oluşur. Örneğin $31$, ikilik sistemde `11111` biçimindedir. Bu düzenli yapı, modüler işlemlerin daha verimli uygulanmasını sağlar.

En önemli avantaj, **Lucas–Lehmer testi** adlı deterministik algoritmadır. $p>2$ asal olmak üzere önce $s_0=4$ alınır ve şu yineleme $p-2$ kez çalıştırılır:

$$s_n=s_{n-1}^2-2 \pmod {M_p}$$

Son değer sıfırsa $M_p$ asaldır; değilse bileşiktir. Olasılıksal testlerin aksine sonuç “muhtemelen asal” değil, kesindir.

| Yaklaşım | Uygulandığı sayılar | Sonuç | Büyük sayılardaki durum |
|---|---|---|---|
| Deneme bölmesi | Her sayı | Kesin | Çok yavaş |
| Miller–Rabin | Her sayı | Genellikle olasılıksal | Oldukça hızlı |
| Lucas–Lehmer | Mersenne adayları | Kesin | Son derece uygun |

## Python ile Lucas–Lehmer testi

Aşağıdaki fonksiyon, verilen asal üs için Mersenne adayını oluşturur ve yinelemeyi gerçekleştirir:

```python
def lucas_lehmer(p):
    """2^p - 1 sayısının Mersenne asalı olup olmadığını test eder."""
    if p == 2:
        return True

    mersenne = (1 << p) - 1
    s = 4

    for _ in range(p - 2):
        s = (s * s - 2) % mersenne

    return s == 0

for p in [2, 3, 5, 7, 11, 13, 17]:
    print(p, lucas_lehmer(p))
```

Buradaki `1 << p` işlemi, ikilik düzende 1 sayısını $p$ basamak sola kaydırarak $2^p$ üretir. Her adımda mod alınması da ara değerlerin gereksiz biçimde büyümesini engeller. Yine de milyonlarca basamaklı adaylarda hızlı büyük tam sayı çarpımı ve dikkatli bellek yönetimi gerekir.

## Dev asallar neden aranıyor?

Mersenne asallarının doğrudan günlük şifrelemede kullanılması şart değildir. Asıl değerleri; hızlı aritmetik algoritmalarını sınamak, donanım hatalarını yakalamak ve sayı teorisini ilerletmektir. Ayrıca her Mersenne asalı, Öklid–Euler teoremi sayesinde bir çift mükemmel sayı üretir:

$$N=2^{p-1}(2^p-1)$$

Bu arayışın en ünlü aktörlerinden biri GIMPS projesidir. Dünyanın dört bir yanındaki gönüllü bilgisayarlar aday üsleri paylaşarak test eder. Böylece tek bir makinenin yıllar sürecek işi, dev bir dijital define avına dönüşür. Kısacık $2^p-1$ formülü, matematiğin en büyük sayısal keşiflerinden bazılarına açılan şaşırtıcı derecede güçlü bir kapıdır.
