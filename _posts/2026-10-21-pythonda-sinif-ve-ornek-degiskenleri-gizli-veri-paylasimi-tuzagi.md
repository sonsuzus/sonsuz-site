---
layout: post
title: "Python’da Sınıf ve Örnek Değişkenleri: Gizli Veri Paylaşımı Tuzağı"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - sınıflar
  - oop
  - değişkenler
  - hata ayıklama
toc: true
image: /img/pythonda-sinif-ve-54.png
---

Python’da nesne yönelimli programlama yaparken sınıf değişkenleri ile örnek değişkenleri arasındaki küçük görünen fark, beklenmedik sonuçlara yol açabilir. Özellikle liste veya sözlük gibi değiştirilebilir bir nesne sınıf değişkeni olarak tanımlandığında, bir örnekte yapılan değişiklik diğer örneklerde de ortaya çıkar. Böylece birbirinden bağımsız olması beklenen nesneler, farkında olmadan aynı veriyi paylaşmaya başlar.


![pythonda-sinif-ve-54](/img/pythonda-sinif-ve-54.svg)

``

## Sınıf değişkeni nedir?

Sınıf değişkeni, sınıf gövdesinde tanımlanır ve sınıfın bütün örnekleri tarafından paylaşılır. Bir sınıftan $n$ adet nesne üretilse bile ilgili sınıf değişkeni için genellikle tek bir ortak nesne bulunur:

$$\text{paylaşılan veri sayısı} = 1$$

Örnek değişkeni ise çoğunlukla `__init__` içinde `self` üzerinden oluşturulur. Her örnek kendi değerini taşır:

$$\text{bağımsız veri sayısı} = n$$

Temel farkı şöyle özetleyebiliriz:

| Özellik | Sınıf değişkeni | Örnek değişkeni |
|---|---|---|
| Tanımlandığı yer | Sınıf gövdesi | Genellikle `__init__` metodu |
| Erişim | `Sinif.deger` veya `nesne.deger` | `nesne.deger` |
| Paylaşım | Bütün örneklerde ortak | Her örneğe özel |
| Uygun kullanım | Sabitler, sayaçlar, ortak ayarlar | Kullanıcı adı, bakiye, kişisel liste |

## Tehlikeli örnek: Ortak liste

Aşağıdaki sınıfta `gorevler`, sınıf seviyesinde tanımlanmıştır:

```python
class Kullanici:
    gorevler = []

    def __init__(self, ad):
        self.ad = ad

    def gorev_ekle(self, gorev):
        self.gorevler.append(gorev)

ayse = Kullanici('Ayşe')
mehmet = Kullanici('Mehmet')

ayse.gorev_ekle('Raporu hazırla')

print(ayse.gorevler)
print(mehmet.gorevler)
```

Her iki çıktı da `['Raporu hazırla']` olur. Mehmet rapor hazırlamak istememişti; ancak Python onu projeye gönüllü yazdı! Bunun nedeni, `ayse.gorevler` ile `mehmet.gorevler` ifadelerinin aynı listeyi bulmasıdır.

Bunu kimlik kontrolüyle doğrulayabiliriz:

```python
print(ayse.gorevler is mehmet.gorevler)  # True
print(id(ayse.gorevler) == id(mehmet.gorevler))  # True
```

Python bir niteliği ararken önce örneğin kendi alanına, ardından sınıfa bakar. `gorevler` örneklerin içinde bulunmadığı için sınıftaki ortak listeye ulaşılır. `append`, yeni bir liste atamak yerine mevcut listeyi yerinde değiştirir.

## Doğru çözüm: Listeyi örnekte oluşturmak

Her kullanıcının bağımsız görev listesine sahip olması için liste `__init__` içinde tanımlanmalıdır:

```python
class Kullanici:
    def __init__(self, ad):
        self.ad = ad
        self.gorevler = []

    def gorev_ekle(self, gorev):
        self.gorevler.append(gorev)

ayse = Kullanici('Ayşe')
mehmet = Kullanici('Mehmet')

ayse.gorev_ekle('Raporu hazırla')

print(ayse.gorevler)    # ['Raporu hazırla']
print(mehmet.gorevler)  # []
```

Artık her `Kullanici` oluşturulduğunda bellekte yeni bir liste üretilir. Dolayısıyla kimlik karşılaştırması `False` sonucunu verir.

## Her sınıf değişkeni kötü müdür?

Hayır. Değişmez veya gerçekten ortak olması gereken bilgiler için sınıf değişkenleri oldukça kullanışlıdır:

```python
class Kullanici:
    uygulama_adi = 'Görev Ustası'
    kullanici_sayisi = 0

    def __init__(self, ad):
        self.ad = ad
        self.gorevler = []
        Kullanici.kullanici_sayisi += 1
```

Burada `uygulama_adi` bütün kullanıcılar için ortaktır. `kullanici_sayisi` ise oluşturulan toplam örnek sayısını izler. Buna karşılık `ad` ve `gorevler`, kullanıcıya özgüdür.

## Atama ile değiştirme arasındaki ince fark

`nesne.gorevler = []` yazmak, örnek üzerinde yeni bir nitelik oluşturabilir ve sınıf değişkenini gölgeleyebilir. Fakat `nesne.gorevler.append(...)` ortak nesneyi doğrudan değiştirir. Bu nedenle yalnızca çıktıya bakmak yerine verinin nerede tanımlandığını sorgulamak önemlidir.

Pratik kural şudur: Bir değer nesneye özgüyse `self` ile oluşturun. Liste, sözlük veya küme gibi değiştirilebilir yapıları sınıf gövdesine koymadan önce mutlaka “Bunun bütün örneklerce paylaşılmasını gerçekten istiyor muyum?” diye sorun. Cevap hayırsa doğru adres `__init__` metodudur.
