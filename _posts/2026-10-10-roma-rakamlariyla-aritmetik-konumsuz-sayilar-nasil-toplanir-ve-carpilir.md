---
layout: post
title: "Roma Rakamlarıyla Aritmetik: Konumsuz Sayılar Nasıl Toplanır ve Çarpılır?"
math: true
categories: 
  - Bilgi
tags: 
  - roma rakamları
  - algoritma
  - aritmetik
  - sayı sistemleri
  - python
toc: true
image: /img/roma-rakamlariyla-aritmetik-33.png
---

Roma rakamları denince çoğumuzun aklına saat kadranları, tarihî yapılar ve film jeneriklerindeki gizemli tarihler gelir. Oysa `I`, `V`, `X`, `L`, `C`, `D` ve `M` sembolleriyle aritmetik yapmak da mümkündür. Üstelik bunun için sayıları mutlaka onluk sisteme çevirmek gerekmez. Biraz sembol birleştirme, biraz sadeleştirme ve bolca düzenleme yeterlidir.

``

## Pozisyonel Olmamak Ne Demektir?

Onluk sistem pozisyoneldir: `325` sayısındaki `3`, yüzler basamağında olduğu için $3 \times 100$ değerindedir. Roma sisteminde ise sembollerin temel değerleri konumlarından bağımsızdır.

| Roma sembolü | Değeri | Beşli karşılığı |
|---|---:|---|
| I | 1 | V = 5I |
| X | 10 | L = 5X |
| C | 100 | D = 5C |
| M | 1000 | — |

![roma-rakamlariyla-aritmetik-33](/img/roma-rakamlariyla-aritmetik-33.svg)


Bir Roma dizisinin değeri, çıkarma gösterimi yok sayıldığında sembol değerlerinin toplamıdır:

$$V(s)=\sum_{i=1}^{n} V(s_i)$$

Örneğin `VIII`, $5+1+1+1=8$ eder. Ancak `IV` gibi çıkarımlı yazımlarda küçük sembol büyük sembolden önce gelirse çıkarılır: $5-1=4$. Aritmetik algoritmalarında bu istisnayı azaltmak için önce genişletilmiş toplamsal biçim kullanmak oldukça pratiktir. Böylece `IV`, geçici olarak `IIII`; `IX` ise `VIIII` biçiminde düşünülebilir.

## Roma Rakamlarıyla Toplama

`XXVII + XVIII` işlemini ele alalım. Önce sembolleri toplamsal biçimde yan yana getiririz:

```text
XXVII + XVIII
= XXVIIXVIII
= XXXVVIIII
```

Ardından aynı sembolleri gruplayıp dönüşüm kurallarını uygularız:

- `IIIII → V`
- `VV → X`
- `XXXXX → L`
- `LL → C`
- `CCCCC → D`
- `DD → M`

`XXXVVIIII` ifadesinde iki `V`, bir `X` olur. Sonuç `XXXXV`, yani standart yazımla `XLV` olur. Gerçekten de $27+18=45$.

| Aşama | Gösterim | Amaç |
|---|---|---|
| Birleştirme | `XXVIIXVIII` | Sembolleri aynı havuzda toplamak |
| Sıralama | `XXXVVIIII` | Eş sembolleri yan yana getirmek |
| Sadeleştirme | `XXXXV` | Grupları büyük sembollere çevirmek |
| Normalleştirme | `XLV` | Standart çıkarımlı yazımı üretmek |

Bu yaklaşım, elde taşımalı toplamanın Roma usulü kuzenidir. Tek fark, basamaklar yerine sembol paketleri taşınmasıdır.

## Çarpma: Tekrarlı Toplamadan Dağıtmaya

En basit yöntem, çarpılan sayıyı tekrar tekrar toplamaktır. Örneğin `XII × III`, üç tane `XII` sembol grubunun birleşimidir:

$$XII \times III = XII + XII + XII = XXXIIIIII$$

Altı `I`, `VI` olarak sadeleşir ve sonuç `XXXVI` olur. Yani $12 \times 3=36$.

Büyük sayılarda tekrarlı toplama verimsizdir. Bunun yerine çarpanı Roma sembollerinin değerlerine ayırabiliriz. `XIV × VI` işlemi, dağılım özelliğiyle şöyle ele alınır:

$$14 \times 6 = 14 \times (5+1)$$

Roma mantığında bu, `XIV` sayısının beş katı ile bir kopyasını birleştirmek demektir. Sonuç $70+14=84$, yani `LXXXIV` olur.

## Python ile Sembol Tabanlı Toplama

Aşağıdaki kod, çıkarımlı biçimi önce toplamsal biçime genişletir; sembolleri sayar ve ardından değeri standart Roma gösterimine dönüştürür:

```python
values = {
    "I": 1, "V": 5, "X": 10, "L": 50,
    "C": 100, "D": 500, "M": 1000
}

expansions = {
    "IV": "IIII", "IX": "VIIII",
    "XL": "XXXX", "XC": "LXXXX",
    "CD": "CCCC", "CM": "DCCCC"
}

def expand(roman):
    for short, long_form in expansions.items():
        roman = roman.replace(short, long_form)
    return roman

def roman_add(a, b):
    pool = expand(a) + expand(b)
    total = sum(values[symbol] for symbol in pool)
    return to_roman(total)

def to_roman(number):
    table = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    result = ""
    for value, symbol in table:
        count, number = divmod(number, value)
        result += symbol * count
    return result

print(roman_add("XXVII", "XVIII"))  # XLV
```

Roma aritmetiği, bilgisayarların kullandığı modern sayı sistemleri kadar verimli değildir; sıfır ve basamak değeri bulunmaması işleri zorlaştırır. Yine de bu algoritmalar önemli bir fikri gösterir: Aritmetik, yalnızca rakamların biçimine değil, temsil kurallarına dayanır. Kuralları doğru tanımladığınızda, antik bir saat kadranı bile küçük bir hesap makinesine dönüşebilir.
