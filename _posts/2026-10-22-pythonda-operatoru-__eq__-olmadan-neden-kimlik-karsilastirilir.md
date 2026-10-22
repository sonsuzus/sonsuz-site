---
layout: post
title: "Python’da == Operatörü: __eq__ Olmadan Neden Kimlik Karşılaştırılır?"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - eşitlik
  - nesne yönelimli programlama
  - eq
  - kimlik karşılaştırması
toc: true
image: /img/pythonda-operatoru-__eq__-28.png
---

Python’da iki özel sınıf nesnesini `==` operatörüyle karşılaştırdığınızda, alanları tamamen aynı olsa bile sonucun `False` çıkması ilk bakışta şaşırtıcıdır. Bunun nedeni, sınıfta `__eq__` metodu tanımlanmadığında varsayılan eşitlik davranışının nesnelerin içeriklerine değil, pratikte kimliklerine dayanmasıdır. Başka bir ifadeyle Python, “Bu iki nesne aynı bilgiyi mi taşıyor?” yerine “Bunlar bellekteki aynı nesne mi?” sorusunu sorar.


![pythonda-operatoru-__eq__-28](/img/pythonda-operatoru-__eq__-28.svg)

``

## Eşitlik ve kimlik aynı şey değildir

Python’da `==` eşitlik, `is` ise kimlik karşılaştırması için kullanılır. Ancak özel bir sınıf kendi eşitlik kurallarını açıklamazsa bu iki karşılaştırmanın sonucu çoğunlukla aynı görünür.

```python
class Kullanici:
    def __init__(self, ad):
        self.ad = ad

kullanici_1 = Kullanici("Ada")
kullanici_2 = Kullanici("Ada")
kullanici_3 = kullanici_1

print(kullanici_1 == kullanici_2)  # False
print(kullanici_1 is kullanici_2)  # False
print(kullanici_1 == kullanici_3)  # True
print(kullanici_1 is kullanici_3)  # True
```

İlk iki nesnenin `ad` alanları aynıdır; fakat iki ayrı constructor çağrısıyla üretildikleri için kimlikleri farklıdır. Üçüncü değişken ise yeni bir nesne oluşturmaz, doğrudan ilk nesneyi gösterir.

| İfade | Sorduğu soru | Özel sınıftaki varsayılan sonuç |
|---|---|---|
| `a == b` | Nesneler eşit kabul ediliyor mu? | Aynı nesneyse `True` |
| `a is b` | Bellekte aynı nesne mi? | Aynı nesneyse `True` |
| `a.ad == b.ad` | Alan değerleri eşit mi? | Değerlere göre belirlenir |

## Perde arkasında `object.__eq__`

Bütün Python sınıfları, açıkça başka bir üst sınıf belirtilmese bile `object` sınıfından türetilir. Dolayısıyla tanımlamadığımız eşitlik davranışı `object.__eq__` üzerinden gelir.

Teknik açıdan `object.__eq__`, farklı nesneler için doğrudan her zaman `False` döndürmekten ziyade çoğu durumda `NotImplemented` sonucunu üretir. Python daha sonra karşı nesnenin yansıtılmış karşılaştırmasını denemeye ve uygun bir davranış bulunamazsa kimlik temelli sonuca ulaşmaya çalışır. Bu nedenle kullanıcı açısından gözlenen varsayılan davranış şu mantıkla özetlenebilir:

$$a == b \approx a\ is\ b$$

Buradaki $\approx$ işareti bilinçlidir: `==` ile `is` dil seviyesinde aynı işlem değildir; yalnızca `__eq__` özelleştirilmemiş sıradan nesnelerde sonuçları genellikle aynıdır.

Nesne kimliğini sayısal olarak incelemek için `id()` fonksiyonu kullanılabilir:

```python
print(id(kullanici_1))
print(id(kullanici_2))
print(id(kullanici_3))
```

`kullanici_1` ile `kullanici_3` aynı kimlik değerini verir. `id()` değeri uygulama çalışırken nesneyi benzersiz biçimde tanımlar; fakat kalıcı veri veya iş kuralı olarak kullanılmamalıdır.

## Değer eşitliği nasıl tanımlanır?

Nesnelerin alanlarına göre karşılaştırılmasını istiyorsak `__eq__` metodunu kendimiz yazabiliriz:

```python
class Kullanici:
    def __init__(self, ad):
        self.ad = ad

    def __eq__(self, diger):
        if not isinstance(diger, Kullanici):
            return NotImplemented
        return self.ad == diger.ad

kullanici_1 = Kullanici("Ada")
kullanici_2 = Kullanici("Ada")

print(kullanici_1 == kullanici_2)  # True
```

`isinstance` kontrolü, ilgisiz türlerin yanlışlıkla eşit kabul edilmesini önler. `False` yerine `NotImplemented` döndürmek ise Python’a diğer nesnenin karşılaştırma mekanizmasını deneme fırsatı verir.

| Yaklaşım | Avantaj | Kullanım alanı |
|---|---|---|
| Varsayılan kimlik davranışı | Basit ve güvenli | Benzersiz oturum veya bağlantı nesneleri |
| Özel `__eq__` | Alanlara göre anlamlı eşitlik | Kullanıcı, ürün ve koordinat modelleri |
| `@dataclass` | Daha az tekrar eden kod | Veri taşıyan sınıflar |

Örneğin `@dataclass`, varsayılan olarak alanları karşılaştıran bir `__eq__` üretebilir. Sonuç olarak her sınıfın değer eşitliğine ihtiyacı yoktur. Nesnenin kavramsal anlamı alanlarından geliyorsa `__eq__` tanımlamak mantıklıdır; benzersiz varlığı önemliyse varsayılan kimlik davranışı tam da istediğiniz şey olabilir.
