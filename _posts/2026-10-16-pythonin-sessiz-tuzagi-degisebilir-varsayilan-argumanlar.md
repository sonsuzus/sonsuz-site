---
layout: post
title: "Python’ın Sessiz Tuzağı: Değişebilir Varsayılan Argümanlar"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - fonksiyonlar
  - mutable
  - hata-ayıklama
  - yazılım-geliştirme
toc: true
image: /img/pythonin-sessiz-tuzagi-42.png
---

Python’da bir fonksiyonun varsayılan argümanına boş liste vermek son derece masum görünür. Ne yazık ki bu küçük kolaylık, farklı fonksiyon çağrılarının aynı listeyi paylaşmasına ve programın adeta önceki konuşmaları hiç unutmayan bir asistana dönüşmesine neden olabilir. Gelin bu sürpriz davranışın arkasındaki mantığı ve güvenli çözümünü inceleyelim.
``
## Sorun nerede başlıyor?

Aşağıdaki fonksiyon, aldığı ürünü bir sepete ekleyip sepeti döndürüyor:

```python
def sepete_ekle(urun, sepet=[]):
    sepet.append(urun)
    return sepet

print(sepete_ekle("Elma"))
print(sepete_ekle("Muz"))
```

İlk kez gören biri çıktının iki bağımsız liste olmasını bekleyebilir. Gerçek sonuç şöyledir:

```text
['Elma']
['Elma', 'Muz']
```

İkinci çağrıya açıkça bir sepet vermediğimiz hâlde `Elma` geri döndü. Çünkü Python, varsayılan argümanları fonksiyon **her çağrıldığında değil**, fonksiyon `def` ifadesi çalıştırıldığında yalnızca bir kez oluşturur.

Bunu basitçe şu modelle ifade edebiliriz:

$$D = \text{fonksiyon tanımlanırken oluşturulan varsayılan nesne}$$

Varsayılan değer kullanılınca her çağrı yeni bir nesne üretmek yerine aynı nesneye bağlanır:

$$C_1 \rightarrow D, \quad C_2 \rightarrow D, \quad C_3 \rightarrow D$$

Liste değiştirildiğinde aslında ortak $D$ nesnesi değiştirilmiş olur. Problem değişken adında değil, nesne kimliğindedir.

## Mutable ve immutable farkı

Python nesnelerini bu konu açısından iki gruba ayırabiliriz:

| Tür | Örnekler | Yerinde değişebilir mi? | Varsayılan argüman riski |
|---|---|---:|---:|
| Mutable | `list`, `dict`, `set` | Evet | Yüksek |
| Immutable | `int`, `str`, `tuple`, `None` | Hayır | Genellikle düşük |

![pythonin-sessiz-tuzagi-42](/img/pythonin-sessiz-tuzagi-42.svg)


Örneğin varsayılan değer `0` ise artırma işlemi mevcut tamsayıyı değiştirmez; yeni bir tamsayı nesnesi oluşturur. Ancak `liste.append()` aynı liste üzerinde işlem yapar. Sürprizin kaynağı tam olarak budur.

Nesnenin gerçekten paylaşıldığını `id()` ile gözlemleyebiliriz:

```python
def kaydet(deger, kayitlar=[]):
    print("Nesne kimliği:", id(kayitlar))
    kayitlar.append(deger)
    return kayitlar

kaydet("A")
kaydet("B")
```

Her iki çağrıda da aynı kimliğin yazdırılması, `kayitlar` listesinin yeniden oluşturulmadığını gösterir.

## Güvenli çözüm: `None` nöbetçisi

Yaygın çözüm, varsayılan argüman olarak immutable `None` kullanmak ve listeyi fonksiyon gövdesinde oluşturmaktır:

```python
def sepete_ekle(urun, sepet=None):
    if sepet is None:
        sepet = []  # Her bağımsız çağrı için yeni liste

    sepet.append(urun)
    return sepet

print(sepete_ekle("Elma"))
print(sepete_ekle("Muz"))
```

Bu kez sonuç `['Elma']` ve `['Muz']` olur. Kontrolde `sepet == None` yerine `sepet is None` tercih edilir; çünkü `None` özel bir tekil nesnedir ve burada kimlik kontrolü amaçlanır.

Ayrıca `if not sepet:` yazmak doğru bir alternatif değildir. Çağıran kişi bilinçli olarak boş bir liste gönderirse bu ifade listeyi yeni bir listeyle değiştirir. `is None`, “argüman verilmedi” durumu ile “boş koleksiyon verildi” durumunu birbirinden ayırır.

## Her zaman hata mı?

Paylaşılan varsayılan nesne bazen bilinçli biçimde önbellek oluşturmak için kullanılabilir:

```python
def kare(n, onbellek={}):
    if n not in onbellek:
        onbellek[n] = n ** 2
    return onbellek[n]
```

Burada sözlüğün çağrılar arasında korunması amaçlanmıştır. Yine de bu teknik gizli durum ürettiği için kodu okumayı, testleri ve eşzamanlı kullanımı zorlaştırabilir. `functools.lru_cache` gibi açık araçlar genellikle daha güvenlidir.

Kısacası varsayılan değer olarak `[]`, `{}` veya `set()` gördüğünüzde durup düşünün. Durumun paylaşılması özellikle istenmiyorsa `None` kullanın ve nesneyi fonksiyon içinde oluşturun. Python sizi kandırmaz; yalnızca verdiği sözü, beklediğinizden biraz daha uzun süre tutar!
