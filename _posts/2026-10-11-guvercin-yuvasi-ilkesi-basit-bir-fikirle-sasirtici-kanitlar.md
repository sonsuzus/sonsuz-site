---
layout: post
title: "Güvercin Yuvası İlkesi: Basit Bir Fikirle Şaşırtıcı Kanıtlar"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - güvercin-yuvası-ilkesi
  - algoritma
  - kombinatorik
  - ispat
  - python
toc: true
image: /img/guvercin-yuvasi-ilkesi-57.png
---

Bir kümesteki yuvalardan daha fazla güvercin varsa en az bir yuvayı paylaşmak zorunda kalırlar. Kulağa çocuk oyuncağı gibi gelen bu gözlem; sayı teorisinden çizge kuramına, algoritma analizinden günlük yaşam problemlerine kadar şaşırtıcı derecede güçlü sonuçlar üretir. Matematikte buna **Güvercin Yuvası İlkesi** denir ve çoğu zaman aranan nesneyi göstermeden, yalnızca onun var olmak zorunda olduğunu kanıtlar.


![guvercin-yuvasi-ilkesi-57](/img/guvercin-yuvasi-ilkesi-57.svg)

``

## İlkenin matematiksel temeli

Elimizde $n$ adet yuva ve bu yuvalara dağıtılan $n+1$ adet güvercin olsun. Her yuvada en fazla bir güvercin bulunduğunu varsayarsak yerleştirilebilecek toplam güvercin sayısı en fazla $n$ olur. Oysa elimizde $n+1$ güvercin vardır. Varsayımımız çelişkiye ulaştığı için en az bir yuvada iki veya daha fazla güvercin bulunmalıdır.

İlkenin genelleştirilmiş biçimi daha kullanışlıdır: $N$ nesne $k$ kutuya dağıtılırsa kutulardan en az biri en az

$$
ceil(N/k)
$$

nesne içerir. Buradaki $ceil(x)$, sonucu yukarıdaki en yakın tam sayıya yuvarlar. Örneğin 100 dosya 9 sunucuya dağıtılırsa en az bir sunucuda en az $ceil(100/9)=12$ dosya bulunur.

| Durum | Güvercinler | Yuvalar | Zorunlu sonuç |
|---|---:|---:|---|
| Klasik ilke | $n+1$ | $n$ | Bir yuvada en az 2 nesne |
| Genelleştirilmiş ilke | $N$ | $k$ | Bir yuvada en az $ceil(N/k)$ nesne |
| Ters bakış | En fazla $r$ nesne/yuvada | $k$ | Toplam en fazla $rk$ nesne |

## Doğum günü örneği

Bir okulda 367 öğrenci olduğunu düşünelim. Yılın 366 gün sürebileceğini hesaba katsak bile en az iki öğrencinin doğum günü aynıdır. Öğrenciler güvercin, takvim günleri ise yuva rolündedir.

Daha güçlü bir soru soralım: 100 öğrenciden kaçının aynı ayda doğmuş olması garanti edilir? Aylar 12 yuva olduğuna göre:

$$
ceil(100/12)=9
$$

Dolayısıyla hangi aylarda doğduklarını bilmeden, en az 9 öğrencinin aynı doğum ayını paylaştığını söyleyebiliriz. İlkenin büyüsü burada ortaya çıkar: Dağılımı hesaplamaz, kaçınılmaz sonucu yakalarız.

## Sayı teorisinden şaşırtıcı bir kanıt

Herhangi $n+1$ tam sayı seçelim. Bu sayıları $n$ ile böldüğümüzde kalanlar yalnızca

$$
0,1,2,...,n-1
$$

olabilir. Yani $n$ farklı kalan yuvası vardır. Ancak $n+1$ sayı bulunduğu için iki sayı aynı kalanı verir. Bu sayılara $a$ ve $b$ dersek:

$$
a mod n = b mod n
$$

Buradan $a-b$ farkının $n$ ile tam bölündüğü sonucu çıkar. Sayıların değerlerini hiç bilmeden, aralarında $n$'nin katı olan bir fark bulunacağını kanıtladık.

## Bilgisayar bilimindeki karşılığı

Hash tablolarında çok sayıda anahtar, sınırlı sayıdaki indekse eşlenir. Anahtar sayısı indeks sayısından fazlaysa çakışma kaçınılmazdır. İyi bir hash fonksiyonu çakışmayı yok etmez; dengeli dağıtmaya çalışır.

```python
def pigeonhole_groups(values, bucket_count):
    # Sayıları kalanlarına göre sınıflandırır.
    buckets = [[] for _ in range(bucket_count)]

    for value in values:
        index = value % bucket_count
        buckets[index].append(value)

    return max(buckets, key=len)

numbers = [14, 27, 35, 42, 58, 63]
print(pigeonhole_groups(numbers, 5))
```

Kod, sayıları beş kalan sınıfına yerleştirir ve en kalabalık sınıfı döndürür. Altı sayı beş sınıfa dağıtıldığı için sınıflardan birinde en az iki sayı bulunacağı daha program çalışmadan garantidir.

| Matematiksel kavram | Programlamadaki karşılığı |
|---|---|
| Güvercin | Anahtar, veri veya istek |
| Yuva | Hash indeksi, sunucu veya bellek bölgesi |
| Aynı yuvaya düşme | Çakışma ya da kaynak paylaşımı |
| Genelleştirilmiş sınır | En kötü durum yükü |

## Kanıtlarda nasıl fark edilir?

Bir problemde “en az iki tanesi”, “mutlaka aynı”, “garanti edilen minimum” veya “kaçınılmaz çakışma” ifadeleri geçiyorsa güvercin yuvası ilkesini düşünmek yararlıdır. Asıl ustalık, güvercinleri ve yuvaları doğru seçmektir. Bazen yuvalar aylar, bazen kalan sınıfları, bazen de geometrik bölgelerdir.

Bu ilke bize önemli bir matematiksel alışkanlık kazandırır: Her şeyi tek tek bulmak zorunda değiliz. Kapasite ile nesne sayısını karşılaştırmak, karmaşık görünen bir varlık kanıtını birkaç satırlık kaçınılmazlık argümanına dönüştürebilir.
