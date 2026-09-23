---
layout: post
title: "Bloom Filter: Bir Şeyin Kesinlikle Olmadığını Ucuza Söylemek"
math: true
categories: 
  - Bilgi
tags: 
  - bloom-filter
  - veri-yapıları
  - algoritmalar
  - olasılık
  - python
  - performans
toc: true
image: /img/bloom-filter-bir-14.png
---

Bir kullanıcı adının daha önce alınıp alınmadığını, bir URL’nin taranıp taranmadığını veya önbellekte belirli bir anahtarın bulunup bulunmadığını kontrol ettiğinizi düşünün. Milyarlarca kayıt arasında sürekli arama yapmak pahalıdır. Bloom Filter burada ilginç bir pazarlık önerir: Çok az bellek kullanır, bir elemanın **kesinlikle bulunmadığını** söyler; fakat bazen bulunmayan bir elemana “belki var” diyebilir.


![bloom-filter-bir-14](/img/bloom-filter-bir-14.svg)

``

## Temel fikir: Cevaplar eşit derecede kesin değil

Bloom Filter, olasılıksal bir veri yapısıdır. Elinde başlangıçta tamamı sıfır olan $m$ bitlik bir dizi ve birbirinden bağımsızmış gibi davranan $k$ adet hash fonksiyonu bulunur.

Bir eleman eklenirken hash fonksiyonları çalıştırılır. Her fonksiyon, bit dizisinde bir konum üretir ve ilgili bit $1$ yapılır. Sorgulama sırasında aynı konumlara bakılır:

- Bitlerden en az biri $0$ ise eleman **kesinlikle yoktur**.
- Bütün bitler $1$ ise eleman **muhtemelen vardır**.

Çünkü bu bitleri sorgulanan eleman değil, daha önce eklenen başka elemanlar da açmış olabilir. Buna **yanlış pozitif** denir. Standart Bloom Filter yanlış negatif üretmez: Eklenmiş bir eleman için “yok” cevabı vermez.

| Özellik | Bloom Filter | Hash Set |
|---|---|---|
| Bellek kullanımı | Çok düşük | Görece yüksek |
| “Yok” cevabı | Kesin | Kesin |
| “Var” cevabı | Olasılıksal | Kesin |
| Elemanları listeleme | Mümkün değil | Mümkün |
| Standart yapıda silme | Güvenli değil | Kolay |

## Yanlış pozitif ihtimali

Filtreye $n$ eleman eklendiğinde yanlış pozitif olasılığı yaklaşık olarak şöyledir:

$$
p \approx \left(1-e^{-kn/m}\right)^k
$$

Burada $m$ bit sayısı, $n$ eklenen eleman sayısı ve $k$ hash fonksiyonu sayısıdır. Sabit bir $m$ ve $n$ için uygun hash sayısı yaklaşık olarak:

$$
k_{opt} \approx \frac{m}{n}\ln 2
$$

Daha fazla hash fonksiyonu kullanmak her zaman daha iyi değildir. Çok az hash, yeterince kontrol yapmaz; çok fazla hash ise bit dizisini hızla doldurur. Bloom Filter’ın dengesi biraz asansöre fazla kişi bindirmemeye benzer: Kapasite aşılırsa herkes birbirine benzemeye başlar.

## Python ile küçük bir uygulama

Aşağıdaki örnek, iki temel hash değerinden farklı konumlar türetir. Böylece gerçekten $k$ ayrı hash algoritması çalıştırmak yerine “double hashing” yaklaşımı kullanılır.

```python
import hashlib

class BloomFilter:
    def __init__(self, size=10_000, hash_count=5):
        self.size = size
        self.hash_count = hash_count
        self.bits = bytearray(size)

    def _positions(self, value):
        data = value.encode("utf-8")
        h1 = int(hashlib.md5(data).hexdigest(), 16)
        h2 = int(hashlib.sha1(data).hexdigest(), 16)

        for i in range(self.hash_count):
            yield (h1 + i * h2) % self.size

    def add(self, value):
        for position in self._positions(value):
            self.bits[position] = 1

    def might_contain(self, value):
        return all(self.bits[p] for p in self._positions(value))

filter = BloomFilter()
filter.add("kahve")

print(filter.might_contain("kahve"))   # Muhtemelen var
print(filter.might_contain("çay"))     # Kesinlikle yok olabilir
```

Bu öğretici örnekte her konum bir bayt kaplar. Gerçek uygulamalarda bit dizisi kullanılarak bellek tüketimi yaklaşık sekiz kat azaltılabilir. Ayrıca MD5 burada güvenlik amacıyla değil, hızlı ve tutarlı konum üretmek için kullanılmıştır.

## Nerelerde işe yarar?

Bloom Filter genellikle pahalı bir işlemin ön kapısında bekler. Filtre “yok” derse veritabanı, disk veya ağ sorgusu tamamen atlanır. “Belki var” derse kesin sonucu öğrenmek için asıl veri kaynağına gidilir.

Tipik kullanım alanları şunlardır:

- Veritabanında gereksiz disk okumalarını engellemek
- Web tarayıcılarında daha önce ziyaret edilen URL’leri kontrol etmek
- Önbellek kaçırmalarını hızlıca belirlemek
- Dağıtık sistemlerde kayıt varlığına ön kontrol yapmak
- Kötü amaçlı adres veya parola listelerini süzmek

Silme gerekiyorsa standart yapı uygun değildir; bir biti sıfırlamak başka elemanları da etkileyebilir. Bunun yerine bitler değil sayaçlar kullanan **Counting Bloom Filter** tercih edilir. Özetle Bloom Filter, “var mı?” sorusuna her zaman kesin cevap vermez; fakat “yok mu?” sorusunu şaşırtıcı derecede hızlı, küçük ve ekonomik biçimde çözer.
