---
layout: post
title: "Python’da `is` ve `==`: Küçük Tam Sayı Önbelleğinin Kurduğu Tuzak"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - operatörler
  - bellek
  - cpython
  - hata ayıklama
  - nesne kimliği
toc: true
image: /img/pythonda-is-ve-17.png
---

![pythonda-is-ve-17](/img/pythonda-is-ve-17.svg)


Python öğrenirken `is` ve `==` bazen aynı sonucu veriyormuş gibi görünür. Özellikle küçük tam sayılarla yapılan denemelerde iki operatörün de `True` döndürmesi, aralarında gerçek bir fark olmadığı yanılgısını doğurabilir. Oysa biri değerleri, diğeri nesnelerin kimliğini karşılaştırır; küçük tam sayı önbelleklemesi ise bu farkı geçici olarak gizleyen küçük bir illüzyondur.

``

## Eşitlik ve kimlik aynı şey değildir

`==` operatörü iki nesnenin **değer bakımından eşit** olup olmadığını denetler. Bu işlem çoğunlukla nesnenin `__eq__` metodu üzerinden gerçekleştirilir. `is` ise iki değişkenin bellekteki **aynı nesneye referans verip vermediğine** bakar ve özelleştirilemez.

| Operatör | Sorduğu soru | Temel mekanizma | Tipik kullanım |
|---|---|---|---|
| `==` | Değerler eşit mi? | `__eq__` | Sayı, metin ve koleksiyon karşılaştırma |
| `is` | Aynı nesne mi? | Nesne kimliği | `None`, sentinel ve tekil nesneler |

Tam sayılar açısından ilişkiyi kabaca şöyle gösterebiliriz:

$$a \text{ is } b \Rightarrow a == b$$

Ancak ters yön garanti değildir:

$$a == b \not\Rightarrow a \text{ is } b$$

Yani aynı değere sahip iki farklı nesne bulunabilir. İki ayrı kâğıda `1000` yazılması, kâğıtları aynı kâğıt yapmaz.

## Küçük tam sayı önbelleği

Yaygın Python uygulaması CPython, sık kullanılan küçük tam sayı nesnelerini tekrar tekrar üretmemek için önceden hazır tutar. Tipik olarak $-5$ ile $256$ arasındaki tam sayılar önbelleğe alınır. Bu sınırlar CPython uygulama ayrıntısıdır; dil tarafından bütün Python uygulamaları için garanti edilmez.

```python
a = 100
b = 100

print(a == b)  # True: değerler eşit
print(a is b)  # CPython'da çoğunlukla True: aynı önbellek nesnesi
```

Burada `is` sonucunun `True` olması, sayısal karşılaştırma için doğru operatörü kullandığımız anlamına gelmez. Yalnızca `a` ve `b`, CPython tarafından paylaşılmış aynı `100` nesnesine bağlanmıştır.

Daha büyük değerlerde maske düşebilir:

```python
a = int("1000")
b = int("1000")

print(a == b)  # True
print(a is b)  # Genellikle False
print(id(a), id(b))
```

`int` çağrıları çalışma anında eşit değerli fakat ayrı nesneler oluşturabilir. `id()` çıktılarının farklı olması, değişkenlerin aynı nesneyi göstermediğini açıklar.

## Neden bazı testler yine şaşırtır?

Aynı kod bloğunda yazılan sabitler, derleyici optimizasyonları nedeniyle paylaşılabilir. Metinlerde interning, sabit katlama ve etkileşimli kabuğun çalışma biçimi de sonuçları etkileyebilir. Bu nedenle `257 is 257` benzeri deneyler farklı Python sürümlerinde, REPL’de veya bir dosya içinde farklı davranabilir. Ayrıca modern Python sürümleri, bir literal ile `is` kullanılınca `SyntaxWarning` gösterebilir.

| Senaryo | Doğru tercih | Neden? |
|---|---|---|
| `puan` değeri 100 mü? | `puan == 100` | Değer karşılaştırılır |
| Sonuç `None` mı? | `sonuc is None` | `None` tekil nesnedir |
| İki liste aynı içeriğe mi sahip? | `liste1 == liste2` | Elemanlar karşılaştırılır |
| İki ad aynı listeyi mi gösteriyor? | `liste1 is liste2` | Nesne kimliği araştırılır |

## Güvenli kullanım kuralı

Sayıları, metinleri ve koleksiyon içeriklerini karşılaştırırken `==` kullanın. `is` operatörünü başta `None` olmak üzere kimliği özellikle önemli olan tekil nesnelere ayırın:

```python
def kullaniciyi_bul(kimlik):
    kullanici = veritabaninda_ara(kimlik)

    if kullanici is None:
        return "Kullanıcı bulunamadı"

    if kullanici.yas == 18:
        return "Kullanıcı tam 18 yaşında"

    return "Kullanıcı bulundu"
```

İlk koşul özel `None` nesnesinin kimliğini, ikinci koşul ise sayısal değeri denetler. Kısacası önbelleğe güvenerek yazılan `is` karşılaştırması tesadüfen çalışabilir; doğru semantiğe dayanan `==` ise niyetinizi açık, taşınabilir ve güvenilir biçimde ifade eder.
