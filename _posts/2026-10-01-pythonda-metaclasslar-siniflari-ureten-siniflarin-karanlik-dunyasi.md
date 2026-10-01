---
layout: post
title: "Python'da Metaclass'lar: Sınıfları Üreten Sınıfların Karanlık Dünyası"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - metaclass
  - oop
  - django
  - sqlalchemy
  - orm
toc: true
image: /img/pythonda-metaclasslar-siniflari-27.png
---

Python'da her şeyin bir nesne olduğunu duymuşsunuzdur; buna sınıflar da dahildir. Bir sınıf örnekleri üretirken, metaclass da sınıfları üretir. Kulağa programlama dünyasının matruşka bebeği gibi geliyor: nesnenin arkasında sınıf, sınıfın arkasında ise metaclass vardır. Genellikle “ihtiyacın olduğunu düşünüyorsan muhtemelen yoktur” uyarısıyla anılsalar da metaclass'lar, Django ve SQLAlchemy gibi araçların etkileyici otomasyonlarının temel parçalarındandır.

![pythonda-metaclasslar-siniflari-27](/img/pythonda-metaclasslar-siniflari-27.svg)

``
## Sınıf da Bir Nesnedir

Normal bir sınıf tanımladığımızda Python yalnızca kaynak kodunu kaydetmez; bellekte çağrılabilir bir sınıf nesnesi oluşturur:

```python
class Robot:
    enerji = 100

    def selamla(self):
        return "Bip bip!"

print(type(Robot))    # <class 'type'>
print(type(Robot()))  # <class '__main__.Robot'>
```

`Robot()` çağrısı bir örnek üretirken `Robot` sınıfının kendisi de `type` isimli metaclass'ın örneğidir. İlişkiyi sembolik olarak şöyle gösterebiliriz:

$$
Robot() \xrightarrow{instance\ of} Robot \xrightarrow{instance\ of} type
$$

Başka bir ifadeyle, $C$ bir sınıf ve $x$ onun nesnesiyse $type(x)=C$ ve çoğu durumda $type(C)=type$ olur.

| Katman | Ürettiği şey | Tipik çağrı |
|---|---|---|
| Fonksiyon | Değer | `hesapla()` |
| Sınıf | Nesne örneği | `Robot()` |
| Metaclass | Sınıf | `type(...)` |

## `type` ile Dinamik Sınıf Üretmek

Üç parametreyle çağrılan `type`, doğrudan sınıf fabrikası gibi çalışır. Parametreleri sınıf adı, üst sınıflar demeti ve sınıf sözlüğüdür:

```python
def selamla(self):
    return f"Merhaba, ben {self.ad}!"

Robot = type(
    "Robot",
    (object,),
    {"ad": "T-800", "selamla": selamla}
)

print(Robot().selamla())
```

Bu kod, `class Robot:` yazarak oluşturacağımız yapının dinamik karşılığıdır. Python bir `class` bloğuyla karşılaşınca gövdeyi çalıştırır, ortaya çıkan isim alanını toplar ve uygun metaclass'a teslim eder.

## Kendi Metaclass'ımızı Yazalım

Metaclass oluşturmak için çoğunlukla `type` sınıfından miras alınır. `__new__`, sınıf nesnesi henüz yaratılmadan önce isim alanını inceleyip değiştirebilir:

```python
class OtomatikKayitMeta(type):
    kayitlar = {}

    def __new__(mcls, ad, tabanlar, alanlar):
        alanlar["sinif_kimligi"] = ad.lower()
        yeni_sinif = super().__new__(mcls, ad, tabanlar, alanlar)

        if ad != "Eklenti":
            mcls.kayitlar[ad] = yeni_sinif

        return yeni_sinif

class Eklenti(metaclass=OtomatikKayitMeta):
    pass

class Raporlayici(Eklenti):
    pass

print(Raporlayici.sinif_kimligi)       # raporlayici
print(OtomatikKayitMeta.kayitlar)      # Otomatik kayıt
```

Burada her alt sınıfa otomatik bir nitelik ekleniyor ve sınıf merkezi kayıt tablosuna yerleştiriliyor. Eklenti sistemlerinde bu yaklaşım, geliştiricinin ayrıca `register()` çağırmasını gereksiz kılabilir.

| Metaclass metodu | Çalıştığı an | Görevi |
|---|---|---|
| `__prepare__` | Sınıf gövdesinden önce | İsim alanını hazırlar |
| `__new__` | Sınıf yaratılırken | Sınıfı oluşturur veya dönüştürür |
| `__init__` | Sınıf yaratıldıktan sonra | Oluşturulan sınıfı yapılandırır |
| `__call__` | Sınıftan örnek alınırken | Örnek üretimini denetler |

## ORM'lerdeki Büyü Nerede?

Bir ORM modelinde yazılan alanlar ilk bakışta sıradan sınıf nitelikleridir:

```python
class Kullanici(Model):
    ad = StringField(max_length=100)
    yas = IntegerField()
```

ORM'nin metaclass'ı sınıf oluşturulurken bu `Field` nesnelerini keşfeder; sütun adlarını, veri tiplerini ve doğrulama kurallarını metadata yapısına dönüştürür. Böylece sınıf tanımı aynı anda hem Python API'si hem de veritabanı şeması olur. Kabaca $Model\ Class \rightarrow Metadata \rightarrow SQL$ dönüşümü gerçekleşir.

## Ne Zaman Uzak Durmalı?

Metaclass'lar güçlüdür fakat sınıf yaratma sürecini görünmez hâle getirerek hata ayıklamayı zorlaştırabilir. Yalnızca alt sınıfları kaydetmek veya küçük kontroller yapmak istiyorsanız sınıf dekoratörleri ve `__init_subclass__` daha okunabilir seçeneklerdir.

Metaclass; birçok sınıfa merkezi kurallar uygulamak, deklaratif API tasarlamak veya sınıf tanımını çalışma anında dönüştürmek gerektiğinde anlamlıdır. Yani karanlık büyü yasak değildir; yalnızca basit bir ampulü yakmak için ejderha çağırmamak gerekir.
