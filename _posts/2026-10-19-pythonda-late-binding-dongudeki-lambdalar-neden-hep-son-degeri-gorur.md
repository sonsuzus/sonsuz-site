---
layout: post
title: "Python’da Late Binding: Döngüdeki Lambda’lar Neden Hep Son Değeri Görür?"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - lambda
  - closure
  - late-binding
  - fonksiyonel-programlama
toc: true
image: /img/pythonda-late-binding-15.png
---

Bir döngü içinde birkaç `lambda` oluşturup her birinin farklı değeri hatırlamasını beklersiniz. Ardından hepsi aynı sonucu döndürür ve Python masumca size bakar. Bu davranış bir hata değil; closure’ların değişkenleri nasıl bağladığıyla ilgili önemli bir Python kuralıdır.

``

## Şaşırtıcı örnek

Aşağıdaki kodun `0, 1, 2` yazdırmasını beklemek oldukça doğaldır:

```python
fonksiyonlar = []

for i in range(3):
    fonksiyonlar.append(lambda: i)

for fonksiyon in fonksiyonlar:
    print(fonksiyon())
```

Gerçek çıktı şöyledir:

```text
2
2
2
```

Çünkü `lambda`, oluşturulduğu anda `i` değişkeninin değerini kopyalamaz. Bunun yerine, çevresindeki kapsamda bulunan `i` değişkenine erişir. Fonksiyonlar çalıştırıldığında döngü çoktan bitmiştir ve `i` değişkeninin son değeri `2` olmuştur.

Bu davranış **late binding**, yani geç bağlama olarak adlandırılır. Bağlamanın fonksiyon tanımlanırken değil, fonksiyon çağrılırken gerçekleştiğini düşünebiliriz.

Matematiksel olarak üç fonksiyon oluşturduğumuzu varsayalım. Beklentimiz:

$$f_0() = 0, \quad f_1() = 1, \quad f_2() = 2$$

Fakat fonksiyonların tamamı aynı değişken hücresine başvurduğu için gerçekte:

$$f_i() = i_{son} = 2$$

olur.

## Closure tam olarak neyi saklar?

Closure, dış kapsamdaki değişkenlere erişebilen iç fonksiyondur. Önemli ayrıntı şudur: Python çoğu durumda değişkenin o anki değerini değil, değişkenin bulunduğu **hücreyi** saklar. Hücrenin içeriği sonradan değişirse closure yeni içeriği görür.

Python isimleri ararken kabaca **LEGB** sırasını kullanır:

| Kapsam | Anlamı | Örnek |
|---|---|---|
| Local | Fonksiyonun yerel alanı | Parametreler |
| Enclosing | Dış fonksiyonların alanı | Closure değişkenleri |
| Global | Modül seviyesi | Dosyada tanımlanan isimler |
| Built-in | Yerleşik isimler | `len`, `print` |

Döngüdeki `i`, lambda’nın yerel parametresi değildir. Bu nedenle çağrı sırasında dış kapsamdan okunur.

## En yaygın çözüm: varsayılan parametre

Değeri lambda oluşturulurken sabitlemek için varsayılan parametre kullanılabilir:

```python
fonksiyonlar = []

for i in range(3):
    fonksiyonlar.append(lambda i=i: i)

for fonksiyon in fonksiyonlar:
    print(fonksiyon())
```

Bu kez çıktı `0, 1, 2` olur. Çünkü varsayılan parametre ifadeleri fonksiyon **tanımlandığı anda** değerlendirilir. Sağ taraftaki `i`, mevcut döngü değerini alır; sol taraftaki `i` ise lambda’nın yerel parametresidir.

| Yaklaşım | Bağlanma zamanı | Sonuç |
|---|---|---|
| `lambda: i` | Çağrı anı | Son değer görülür |
| `lambda i=i: i` | Tanımlama anı | Her değer ayrı saklanır |

## Factory fonksiyonu kullanmak

Daha karmaşık işlemlerde varsayılan parametre numarası yerine açıklayıcı bir üretici fonksiyon tercih edilebilir:

```python
def carpani_uret(carpan):
    def carp(sayi):
        return sayi * carpan
    return carp

fonksiyonlar = [carpani_uret(i) for i in range(3)]

print([fonksiyon(10) for fonksiyon in fonksiyonlar])
# [0, 10, 20]
```

Her `carpani_uret` çağrısı yeni bir yerel kapsam oluşturur. Böylece her iç fonksiyon farklı bir `carpan` hücresine sahip olur. Bu yaklaşım daha uzun olsa da okunabilirliği yüksektir.

Alternatif olarak `functools.partial`, bir fonksiyonun belirli argümanlarını önceden bağlamak için kullanılabilir:

```python
from functools import partial

def carp(sayi, carpan):
    return sayi * carpan

fonksiyonlar = [partial(carp, carpan=i) for i in range(3)]
```

Late binding özellikle buton callback’lerinde, zamanlayıcılarda, olay dinleyicilerinde ve asenkron görevlerde ortaya çıkar. Kısa kural şudur: Döngü değişkenini daha sonra çalışacak bir fonksiyonda kullanıyorsanız, değeri varsayılan parametreyle, factory fonksiyonuyla veya `partial` ile açıkça bağlayın. Böylece lambda’lar sürpriz kutusu olmaktan çıkar.

![pythonda-late-binding-15](/img/pythonda-late-binding-15.svg)

