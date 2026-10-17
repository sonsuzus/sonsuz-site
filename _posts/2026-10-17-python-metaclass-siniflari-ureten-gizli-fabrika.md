---
layout: post
title: "Python Metaclass: Sınıfları Üreten Gizli Fabrika"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - metaclass
  - nesne-yönelimli-programlama
  - sınıflar
  - ileri-python
toc: true
image: /img/python-metaclass-siniflari-81.png
---

Python’da sınıfları genellikle nesne üreten şablonlar olarak düşünürüz. Peki sınıfların kendisini kim üretir? Cevap: **metaclass**. Metaclass kullanımı; sınıf oluşturulurken doğrulama yapmak, otomatik kayıt mekanizmaları kurmak ve sınıf yapısını değiştirmek gibi güçlü olanaklar sunar. Ancak bu güç, kodu küçük bir büyücülük gösterisine dönüştürebilecek kadar karmaşıktır.
``
## Önce temel model: Her şey bir nesnedir

Python’da sıradan bir nesne bir sınıftan, sınıf ise bir metaclass’tan oluşturulur. Varsayılan metaclass `type` sınıfıdır:

```python
class Robot:
    pass

r = Robot()

print(type(r))      # <class '__main__.Robot'>
print(type(Robot))  # <class 'type'>
```

Burada `r`, `Robot` sınıfının örneğidir; `Robot` ise `type` metaclass’ının örneğidir. İlişkiyi matematiksel biçimde şöyle gösterebiliriz:

$$
r \in Robot, \qquad Robot \in type
$$

Başka bir deyişle sınıflar, çalışma zamanında oluşturulan gerçek nesnelerdir. `type`, üç argümanla çağrıldığında dinamik olarak sınıf üretebilir:

```python
Robot = type(
    "Robot",
    (),
    {"selamla": lambda self: "Bip bip!"}
)

print(Robot().selamla())
```

Bu çağrıda ilk argüman sınıf adını, ikincisi temel sınıfları, üçüncüsü ise sınıfın isim alanını belirtir.

| Kavram | Ne üretir? | Varsayılan üretici |
|---|---|---|
| Sınıf | Nesne | Tanımlanan sınıf |
| Metaclass | Sınıf | `type` |
| Fonksiyon | Davranış | `def` veya `lambda` |

![python-metaclass-siniflari-81](/img/python-metaclass-siniflari-81.svg)


## Sınıf oluşturma süreci

Python bir `class` bloğuyla karşılaştığında kabaca isim alanını hazırlar, bloktaki ifadeleri çalıştırır ve ortaya çıkan sözlüğü metaclass’a gönderir. Temel model şu fonksiyon gibi düşünülebilir:

$$
C = M(n, B, D)
$$

Burada $M$ metaclass, $n$ sınıf adı, $B$ temel sınıflar ve $D$ sınıf sözlüğüdür. Metaclass’ın `__new__` metodu sınıf nesnesini oluşturur; `__init__` ise oluşturulan sınıfı yapılandırır.

```python
class AlanKontrolu(type):
    def __new__(mcls, name, bases, namespace):
        if name != "Model" and "tablo_adi" not in namespace:
            raise TypeError(f"{name} sınıfında tablo_adi bulunmalı")

        namespace["kaydet"] = lambda self: (
            f"{self.tablo_adi} tablosuna kaydedildi"
        )
        return super().__new__(mcls, name, bases, namespace)


class Model(metaclass=AlanKontrolu):
    pass


class Kullanici(Model):
    tablo_adi = "kullanicilar"


print(Kullanici().kaydet())
```

Bu örnek iki iş yapar: Alt sınıflarda `tablo_adi` alanını zorunlu tutar ve her sınıfa otomatik olarak `kaydet` metodu ekler. Böylece kurallar sınıf örneği oluşturulmadan uygulanır.

## Metaclass neden kullanılır?

Metaclass’lar özellikle framework geliştirirken değerlidir. ORM modellerinin sütunlarını toplamak, eklenti sınıflarını merkezi bir kayıt defterine eklemek, API sınıflarını doğrulamak veya deklaratif DSL yapıları kurmak yaygın örneklerdir.

| Yaklaşım | Güçlü yanı | Zayıf yanı |
|---|---|---|
| Decorator | Açık ve okunabilir | Kalıtım zincirini otomatik yönetmez |
| `__init_subclass__` | Alt sınıfları kolayca denetler | Oluşturma sürecine erişimi daha sınırlıdır |
| Metaclass | Sınıf üretimini tamamen kontrol eder | Hata ayıklaması ve birleşimi zordur |

## Karmaşıklığın karanlık tarafı

Bir sınıf birden fazla taban sınıftan kalıtım aldığında metaclass’lar uyumlu değilse **metaclass conflict** hatası oluşabilir. Ayrıca sınıfa görünmez biçimde metot eklemek, kodu okuyan kişinin davranışın kaynağını bulmasını zorlaştırır. Bu nedenle metaclass, “yapabiliyorum” diye değil, “başka temiz çözüm yok” denildiğinde seçilmelidir.

Çoğu uygulamada önce class decorator, descriptor veya `__init_subclass__` değerlendirilmelidir. Metaclass ise tekrar eden sınıf kurallarının merkezi olarak uygulanması ve sınıfın daha doğduğu anda dönüştürülmesi gerektiğinde parlar. Kısacası metaclass bir çekiç değil, hassas bir fabrika robotudur: doğru yerde üretimi hızlandırır; yanlış yerde bütün montaj hattını gizemli hâle getirir.
