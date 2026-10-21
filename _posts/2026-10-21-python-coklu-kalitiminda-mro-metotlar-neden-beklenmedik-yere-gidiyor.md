---
layout: post
title: "Python Çoklu Kalıtımında MRO: Metotlar Neden Beklenmedik Yere Gidiyor?"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - mro
  - çoklu-kalıtım
  - oop
  - c3-doğrusallaştırma
  - super
toc: true
image: /img/python-coklu-kalitiminda-68.png
---

Python’da çoklu kalıtım ilk bakışta oldukça masum görünür: Bir sınıf, birden fazla sınıftan özellik kazanır ve herkes mutlu olur. Ancak aynı isimli metotlar, elmas biçimli kalıtım zincirleri ve `super()` çağrıları devreye girdiğinde Python’ın hangi metodu çalıştırdığı şaşırtıcı olabilir. Bu karar rastgele verilmez; arka planda Method Resolution Order, yani MRO adı verilen kesin bir sıralama bulunur.
``
## MRO tam olarak nedir?

MRO, bir özellik veya metot aranırken sınıfların hangi sırayla ziyaret edileceğini belirtir. Python 3 bu sırayı oluşturmak için **C3 doğrusallaştırma** algoritmasını kullanır. Amaç; çocuk sınıfları ebeveynlerden önce tutmak, sınıf bildirimindeki soldan sağa önceliği korumak ve kalıtım ağında tutarlı bir sıra üretmektir.

Bir `C` sınıfı, `B1, B2, ..., Bn` sınıflarından türetiliyorsa sıralama kabaca şöyle ifade edilir:

$$
L(C) = [C] + merge(L(B_1), L(B_2), \ldots, L(B_n), [B_1, B_2, \ldots, B_n])
$$

Buradaki `merge`, başka listelerin kuyruklarında bulunmayan uygun bir baş elemanı seçer. Bu kural, bir sınıfın kendi alt sınıfından önce aranmasını engeller.

| Yaklaşım | Arama mantığı | Olası sonuç |
|---|---|---|
| Tekli kalıtım | Çocuktan ebeveyne doğru | Genellikle tahmin edilebilir |
| Basit çoklu kalıtım | Soldaki ebeveyn önce | Aynı adlı metot gölgelenebilir |
| Elmas kalıtım | C3 MRO sırası izlenir | Ortak ata yalnızca bir kez işlenir |
| Doğrudan sınıf çağrısı | Belirtilen sınıf zorla kullanılır | Zincir ve diğer sınıflar atlanabilir |

![python-coklu-kalitiminda-68](/img/python-coklu-kalitiminda-68.svg)


## Beklenmedik davranış örneği

Aşağıdaki örnekte iki ara sınıf aynı metodu değiştirir:

```python
class Temel:
    def mesaj(self):
        return "Temel"

class A(Temel):
    def mesaj(self):
        return "A -> " + super().mesaj()

class B(Temel):
    def mesaj(self):
        return "B -> " + super().mesaj()

class C(A, B):
    pass

nesne = C()
print(nesne.mesaj())
print(C.mro())
```

Çıktı şu yapıdadır:

```text
A -> B -> Temel
[C, A, B, Temel, object]
```

Şaşırtıcı nokta, `A` içindeki `super()` çağrısının doğrudan `Temel` sınıfına gitmemesidir. `super()`, “ebeveynimi çağır” anlamına gelmez; **mevcut MRO’da benden sonraki sınıfa geç** demektir. Dolayısıyla `C(A, B)` için `A` sonrasında `B` çalışır.

Ebeveynlerin sırasını değiştirirsek sonuç da değişir:

```python
class D(B, A):
    pass

print(D().mesaj())
# B -> A -> Temel
```

Yalnızca sınıf bildirimindeki sıra değişmesine rağmen davranış tersine dönmüştür. Özellikle mixin kullanılan büyük projelerde bu durum sessiz ve zor bulunan hatalar doğurabilir.

## `super()` zinciri nasıl güvenli kurulur?

İşbirlikçi çoklu kalıtımda zincire katılan bütün sınıflar uyumlu davranmalıdır. Her sınıf `super()` çağırmalı, metot imzaları birbiriyle çelişmemeli ve zincir doğrudan sınıf adıyla kesilmemelidir.

```python
class KayitMixin:
    def kaydet(self, **kwargs):
        print("Kayıt günlüğü oluşturuldu")
        return super().kaydet(**kwargs)

class DogrulamaMixin:
    def kaydet(self, **kwargs):
        if not kwargs.get("ad"):
            raise ValueError("ad gerekli")
        return super().kaydet(**kwargs)

class Depo:
    def kaydet(self, **kwargs):
        return f"Kaydedildi: {kwargs['ad']}"

class Servis(KayitMixin, DogrulamaMixin, Depo):
    pass
```

Bu tasarımda her katman yalnızca kendi görevini yapar ve kontrolü sıradaki sınıfa bırakır. `Servis.mro()` çağrısı, gerçek yürütme yolunu incelemenin en pratik yöntemidir.

## Akılda tutulması gerekenler

MRO’yu bir soy ağacından çok, Python’ın önceden hazırladığı bir ziyaret listesi gibi düşünün. `super()` bu listede tek adım ilerler. Beklenmedik bir sonuçla karşılaştığınızda `Sinif.__mro__` veya `Sinif.mro()` çıktısını kontrol edin; ebeveyn sırasını bilinçli belirleyin ve doğrudan `A.metot(self)` çağrılarından kaçının. Çoklu kalıtım güçlüdür, fakat MRO okunmadan kullanıldığında kod tabanına küçük bir labirent yerleştirebilir.
