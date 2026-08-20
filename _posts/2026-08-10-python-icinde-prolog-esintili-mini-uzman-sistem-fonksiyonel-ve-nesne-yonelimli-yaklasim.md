---
layout: post
title: "Python İçinde Prolog Esintili Mini Uzman Sistem: Fonksiyonel ve Nesne Yönelimli Yaklaşım"
math: true
categories: 
  - Proje
tags: 
  - python
  - prolog
  - uzman sistemler
image: /img/python-icinde-prolog-48.png
---

![python-icinde-prolog-48](/img/python-icinde-prolog-48.svg)


Bir uzman sistem, belirli bir alandaki bilgileri kurallar hâlinde saklar ve bu bilgilerden yeni sonuçlar üretir. Bu projede Python'ın nesne yönelimli yapısını bilgi temsili için, fonksiyonel yaklaşımını ise sorgu sonuçlarını akış hâlinde üretmek için birleştiriyoruz. Ortaya çıkan yapı tam bir Prolog yorumlayıcısı değildir; ancak `ebeveyn(ali, ayse)` gibi olgular ve `buyukebeveyn(X, Z) :- ebeveyn(X, Y), ebeveyn(Y, Z)` benzeri kurallarla mantıksal çıkarım yapabilen, Python içine gömülü küçük ama öğretici bir motor olacaktır.
``

## Neden iki paradigma?

Prolog'un merkezinde **bildirimsel programlama** bulunur: “Nasıl yapacağını” değil, “neyin doğru olduğunu” tanımlarsınız. Python ise çoğu zaman yordamlarla çalışır. İkisini birleştirmenin püf noktası, kuralları nesneler olarak modellemek; çözüm uzayını ise `yield` ile tembel biçimde gezmektir.

| Yaklaşım | Sistemdeki rolü | Avantajı |
|---|---|---|
| Nesne yönelimli | `Atom` ve `Kural` veri modelleri | Bilgiyi açık ve genişletilebilir temsil eder |
| Fonksiyonel/jeneratör | Geri izlemeli sorgu çözümü | Birden fazla cevabı sırayla üretir |
| Bildirimsel mantık | Olgu ve kural yazımı | Alan bilgisini Python kontrol akışından ayırır |

Mantıksal çıkarımın temel işlemi **birleştirme**dir (unification). İki terim uyumluysa değişkenlere değer bağlanır. Örneğin `ebeveyn(X, ayse)` ile `ebeveyn(ali, ayse)` eşleştiğinde $X = ali$ elde edilir. Bir kural gövdesindeki tüm hedefler doğruysa kuralın başı doğrudur:

$$
(A \land B) \Rightarrow C
$$

Burada motorumuz derinlik öncelikli arama uygular. Bu yaklaşım basittir; ancak özyinelemeli veya döngüsel kurallarda kontrol mekanizması gerektirebilir.

## Veri modeli ve birleştirme

Aşağıdaki kod, atomları, kuralları ve değişken bağlamlarını temsil eder. Büyük harfle başlayan değerleri değişken kabul ediyoruz.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Atom:
    ad: str
    args: tuple

@dataclass(frozen=True)
class Kural:
    bas: Atom
    govde: tuple

def degisken_mi(x):
    return isinstance(x, str) and x[:1].isupper()

def cozumle(x, baglam):
    while degisken_mi(x) and x in baglam:
        x = baglam[x]
    return x

def birlestir(a, b, baglam):
    a, b = cozumle(a, baglam), cozumle(b, baglam)
    if a == b:
        return baglam
    if degisken_mi(a):
        return {**baglam, a: b}
    if degisken_mi(b):
        return {**baglam, b: a}
    return None
```

`birlestir`, mevcut sözlüğü değiştirmek yerine yeni bir sözlük döndürür. Bu küçük ayrıntı önemlidir: geri izleme sırasında bir dalın yaptığı değişiklik diğer dallara sızmaz. Yani fonksiyonel veri akışı, mantıksal aramanın güvenlik kemeri olur.

## Geri izlemeli çıkarım motoru

Şimdi olgularla kuralları tarayan motoru yazalım. `coz` bir jeneratördür; bu nedenle ilk cevapta durabilir veya tüm cevapları gezebilirsiniz.

```python
class Motor:
    def __init__(self, olgular, kurallar):
        self.olgular = olgular
        self.kurallar = kurallar

    def atom_birlestir(self, hedef, aday, baglam):
        if hedef.ad != aday.ad or len(hedef.args) != len(aday.args):
            return None
        for x, y in zip(hedef.args, aday.args):
            baglam = birlestir(x, y, baglam)
            if baglam is None:
                return None
        return baglam

    def coz(self, hedefler, baglam=None):
        baglam = {} if baglam is None else baglam
        if not hedefler:
            yield baglam
            return
        ilk, *kalan = hedefler
        for aday in self.olgular:
            yeni = self.atom_birlestir(ilk, aday, baglam)
            if yeni is not None:
                yield from self.coz(kalan, yeni)
```

Bu sürüm doğrudan olguları çözer. Kuralları eklemek için her `Kural` nesnesinin `bas` kısmını hedefle birleştirip, ardından `govde + kalan` hedeflerini çözmek yeterlidir. Böylece Prolog'daki geri zincirleme davranışına yaklaşırız.

Örneğin `ebeveyn(ali, ayse)` ve `ebeveyn(ayse, can)` olgularından `buyukebeveyn(ali, can)` türetilebilir. Çıkarım maliyeti kabaca aday sayısı ve hedef derinliğiyle büyür: $O(b^d)$. Bu nedenle gerçek projelerde indeksleme, maksimum derinlik ve döngü algılama eklemek akıllıcadır. Mini motorun güzelliği ise şurada: Python'dan ayrılmadan, kurallarla düşünebilen bir sistem inşa etmiş olursunuz.
