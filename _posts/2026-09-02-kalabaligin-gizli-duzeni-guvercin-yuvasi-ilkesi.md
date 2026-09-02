---
layout: post
title: "Kalabalığın Gizli Düzeni: Güvercin Yuvası İlkesi"
math: true
categories: 
  - Bilgi
tags: 
  - kombinatorik
  - matematiksel-ispat
  - algoritma
toc: true
---

Bazı matematik soruları uzun denklemler, karmaşık olasılıklar veya sayfalar dolusu hesaplama gerektiriyormuş gibi görünür. Oysa bazen çözüm, birkaç güvercini birkaç yuvaya yerleştirmekten ibarettir. Güvercin Yuvası İlkesi, şaşırtıcı derecede basit olmasına rağmen sayı teorisinden algoritmalara kadar pek çok alanda güçlü ispatlar kurmamızı sağlar.
``

## İlkenin temel fikri

Elimizde $n+1$ güvercin ve yalnızca $n$ yuva olduğunu düşünelim. Bütün güvercinleri yuvalara yerleştirirsek en az bir yuvada birden fazla güvercin bulunmak zorundadır. Çünkü her yuvaya en fazla bir güvercin koyabilseydik toplam kapasite yalnızca $n$ olurdu.

İlkenin en sade matematiksel ifadesi şöyledir:

$$
N > K \Rightarrow \text{en az bir yuvada iki veya daha fazla nesne vardır.}
$$

Burada $N$ nesne sayısını, $K$ ise sınıf ya da yuva sayısını temsil eder. Genelleştirilmiş biçimde, en az bir yuvada bulunması garanti edilen nesne sayısı:

$$
\left\lceil \frac{N}{K} \right\rceil
$$

kadardır. Örneğin 25 öğrenciyi 7 haftanın günlerine doğum günlerine göre dağıtırsak, en az bir günde doğmuş öğrenci sayısı $\lceil 25/7 \rceil=4$ olur.

## Güvercin ve yuva nasıl seçilir?

Soruların zor kısmı bölme işlemi değil, neyin “güvercin” ve neyin “yuva” olduğunu fark etmektir. Aynı problem farklı biçimlerde gizlenebilir.

| Problemde görünen unsur | Güvercin | Yuva |
|---|---|---|
| Öğrencilerin doğum ayları | Öğrenciler | 12 ay |
| Tam sayıların kalanları | Tam sayılar | Olası kalanlar |
| Dosyaların sunuculara dağıtılması | Dosyalar | Sunucular |
| İnsanlar arasındaki ortak özellik | İnsanlar | Özellik sınıfları |

Örneğin 13 kişinin bulunduğu bir odada en az iki kişinin aynı ayda doğduğunu garanti edebiliriz. On üç kişi güvercin, 12 ay ise yuvadır. Hangi ayın tekrarlandığını bulamayız; fakat bir tekrarın mutlaka var olduğunu ispatlarız. İlke çoğunlukla sonucu inşa etmekten ziyade sonucun kaçınılmazlığını gösterir.

## Kalanlar üzerinden klasik bir örnek

Herhangi 6 tam sayı seçelim. Bu sayıları 5 ile böldüğümüzde elde edilebilecek kalanlar yalnızca şunlardır:

$$0,1,2,3,4$$

Altı sayı, beş kalan sınıfına dağıtılır. Dolayısıyla en az iki sayı aynı kalanı verir. Bu iki sayıya $a$ ve $b$ dersek:

$$a \equiv b \pmod 5$$

olur. Buradan $a-b$ farkının 5 ile tam bölündüğü sonucuna ulaşırız. Sayıların kendilerini bilmeden onlar hakkında kesin bir özellik elde ettik; ilkenin büyüsü tam olarak budur.

## Programlamada nasıl karşımıza çıkar?

Güvercin Yuvası İlkesi, veri yapılarındaki çakışmaları anlamak için de kullanılır. Bir hash tablosunda olası anahtar sayısı, indeks sayısından fazlaysa çakışma kaçınılmazdır.

```python
def pigeonhole(values, bucket_count):
    buckets = [[] for _ in range(bucket_count)]

    for value in values:
        index = value % bucket_count
        buckets[index].append(value)

    return [bucket for bucket in buckets if len(bucket) > 1]

print(pigeonhole([7, 12, 18, 23, 29, 34], 5))
```

Bu kod, sayıları 5 ile bölümden kalanlarına göre kovalara ayırır ve birden fazla eleman içeren kovaları döndürür. Altı değer yalnızca beş kovaya dağıtıldığı için sonuç listesinin boş olması mümkün değildir.

## Benzer yöntemlerle farkı

| Yöntem | Temel soru | Sağladığı sonuç |
|---|---|---|
| Güvercin Yuvası | Yeterli yer var mı? | Bir tekrarın varlığını kanıtlar |
| Tümevarım | Önerme tüm adımlarda sürüyor mu? | Sonsuz durum ailesini kanıtlar |
| Çelişki | Tersi doğru kabul edilirse ne olur? | İmkânsızlık üzerinden ispatlar |
| Sayma | Kaç farklı düzenleme vardır? | Kesin bir adet hesaplar |

Bir soruda “mutlaka”, “en az iki”, “aynı kalan” veya “ortak özellik” ifadeleri geçiyorsa güvercinleri saymaya başlamak iyi bir reflekstir. Karmaşık görünen tablonun altında çoğu zaman basit bir kapasite problemi vardır: Misafir çok, sandalye azsa birileri kesinlikle sıkışacaktır.
