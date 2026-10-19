---
layout: post
title: "Python’da Sığ Kopya Tuzağı: copy ve deepcopy Arasındaki Kritik Fark"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - deepcopy
  - copy
  - veri-yapıları
  - referanslar
  - bellek-yönetimi
toc: true
image: /img/pythonda-sig-kopya-28.png
---

Python’da bir listeyi kopyaladığınızı düşünüp orijinal verinin de değiştiğini görmek, küçük çaplı bir yazılım korku filmidir. Özellikle listeler, sözlükler veya nesneler iç içe geçtiğinde `copy()` ile `deepcopy()` arasındaki fark kolayca gözden kaçar. Çünkü ekranda birbirinin aynısı görünen iki değer, bellekte aynı alt nesneleri paylaşmaya devam ediyor olabilir.

``

## Değer değil, referans kopyalanır

Python değişkenleri nesnelerin kendisini değil, nesnelere giden referansları tutar. Basit bir atama yeni nesne oluşturmaz:

```python
orijinal = [[1, 2], [3, 4]]
takma_ad = orijinal

takma_ad[0].append(99)
print(orijinal)  # [[1, 2, 99], [3, 4]]
```

Burada iki değişken de aynı dış listeyi gösterir. Bunu matematiksel olarak bir referans eşlemesiyle düşünebiliriz. Bir değişkenin gösterdiği nesneyi $R(x)$ ile ifade edersek:

$$R(orijinal) = R(takma\_ad)$$

Dolayısıyla birinden yapılan değişiklik diğerinde de görünür. Kopyalama işlemleri bu ortaklığı belirli seviyelerde kırar.

## Sığ kopya nasıl çalışır?

`copy.copy()` veya bir listenin `copy()` metodu yalnızca en dıştaki kapsayıcıyı yeniden oluşturur. İçindeki nesnelerin referansları ise paylaşılır.

```python
import copy

orijinal = {
    'kullanici': {'ad': 'Ada', 'roller': ['admin']},
    'aktif': True
}

sig = copy.copy(orijinal)
sig['kullanici']['roller'].append('editor')

print(orijinal['kullanici']['roller'])
# ['admin', 'editor']
```

Yeni bir sözlük oluşturulmuştur; ancak `'kullanici'` anahtarının gösterdiği iç sözlük hâlâ aynıdır. Yani dış kabuk yeni, iç mobilyalar ortaktır.

| İşlem | Dış nesne | İç nesneler | Değişiklik riski |
|---|---|---|---|
| Atama (`=`) | Paylaşılır | Paylaşılır | Çok yüksek |
| Sığ kopya (`copy`) | Yeniden oluşturulur | Paylaşılır | İç yapılarda yüksek |
| Derin kopya (`deepcopy`) | Yeniden oluşturulur | Genellikle yeniden oluşturulur | Düşük |

![pythonda-sig-kopya-28](/img/pythonda-sig-kopya-28.svg)


Nesne kimlikleriyle durumu doğrulayabiliriz:

```python
print(orijinal is sig)  # False
print(orijinal['kullanici'] is sig['kullanici'])  # True
```

## Derin kopya neyi değiştirir?

`copy.deepcopy()` veri yapısını özyinelemeli biçimde dolaşır ve eriştiği iç nesneleri de kopyalar:

```python
derin = copy.deepcopy(orijinal)
derin['kullanici']['roller'].append('tester')

print(derin['kullanici']['roller'])
# ['admin', 'editor', 'tester']

print(orijinal['kullanici']['roller'])
# ['admin', 'editor']
```

Bu kez iç liste bağımsızdır. Yaklaşık $n$ adet nesnenin ziyaret edildiği bir yapı için zaman ve ek bellek maliyeti çoğunlukla $O(n)$ olarak düşünülebilir. Sığ kopya ise yalnızca dış kapsayıcının $k$ eleman referansını aktarır ve yaklaşık $O(k)$ maliyet taşır.

## Her durumda deepcopy mi?

Hayır. `deepcopy()` güvenli görünse de büyük yapılarda pahalıdır. Ayrıca dosya bağlantıları, ağ soketleri veya özel sınıflar gibi kaynakların anlamlı biçimde kopyalanması mümkün olmayabilir. Python, döngüsel referanslarda sonsuz özyinelemeyi önlemek için daha önce kopyalanan nesneleri bir `memo` tablosunda izler.

| Senaryo | Tercih |
|---|---|
| Düz, tek seviyeli liste | `copy()` veya dilimleme |
| İç içe ve bağımsız değişecek veri | `deepcopy()` |
| Salt okunur ortak alt nesneler | `copy()` |
| Çok büyük veri yapısı | Yalnızca gereken dalları kopyalama |
| Özel sınıflar | Kontrollü kopyalama metotları |

En sık yapılan hata, yalnızca dış nesnenin farklı olduğunu kontrol etmektir. İç içe yapılarda birkaç seviyede `is` karşılaştırması yapmak, problemi erkenden yakalar. Kısacası `copy()` yeni bir kap üretir; `deepcopy()` ise kabı, içindekileri ve mümkün olduğunca onların içindekileri de çoğaltır. Kopyalama kararını verirken sadece verinin bugünkü görünümünü değil, hangi seviyelerinin daha sonra değiştirileceğini düşünmek gerekir.
