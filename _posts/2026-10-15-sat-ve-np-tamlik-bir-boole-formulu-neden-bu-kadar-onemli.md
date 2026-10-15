---
layout: post
title: "SAT ve NP-Tamlık: Bir Boole Formülü Neden Bu Kadar Önemli?"
math: true
categories: 
  - Bilgi
tags: 
  - sat
  - np-tamlık
  - algoritmalar
  - karmaşıklık-teorisi
  - boole-mantığı
  - python
toc: true
image: /img/sat-ve-np-60.png
---

Bir bulmacanın çözümünü kontrol etmek kolayken çözümü sıfırdan bulmak son derece zor olabilir mi? Mantıksal Sağlanabilirlik Problemi, yani SAT, tam olarak bu ayrımın peşine düşer. Basit görünen Boole formüllerinden doğan SAT; algoritma tasarımından donanım doğrulamaya, yapay zekâdan çizelgelemeye kadar uzanan etkisiyle hesaplama karmaşıklığı teorisinin merkezinde yer alır.

![sat-ve-np-60](/img/sat-ve-np-60.svg)

``

## SAT problemi nedir?

Bir Boole formülü; `doğru` veya `yanlış` değerlerini alabilen değişkenlerden ve AND ($\land$), OR ($\lor$), NOT ($\neg$) gibi bağlaçlardan oluşur. SAT problemi şu soruyu sorar:

> Formülü doğru yapan en az bir değişken ataması var mı?

Örneğin

$$
F=(x \lor y) \land (\neg x \lor z)
$$

formülü için $x=1$, $y=0$ ve $z=1$ seçildiğinde iki parantez de doğru olur. Dolayısıyla $F$ sağlanabilirdir. Buna karşılık

$$
G=x \land \neg x
$$

hiçbir atamayla doğru yapılamaz; bu formül sağlanamazdır.

$n$ değişkenli bir formül için toplam $2^n$ olası atama vardır. Kaba kuvvet algoritması bunların tamamını dener. Bu yaklaşımın çalışma süresi yaklaşık olarak

$$
T(n)=O(2^n \cdot \vert F\vert )
$$

olur. Üstel büyüme yüzünden birkaç yüz değişken bile bilgisayarı ciddi biçimde terletebilir.

## P, NP ve NP-tamlık bağlantısı

SAT'ın önemini anlamak için temel karmaşıklık sınıflarını karşılaştıralım:

| Sınıf | Temel fikir | SAT ile ilişkisi |
|---|---|---|
| P | Çözüm polinom zamanda bulunabilir | SAT'ın P'de olup olmadığı bilinmiyor |
| NP | Verilen çözüm polinom zamanda doğrulanabilir | Bir atama kolayca kontrol edildiği için SAT, NP'dedir |
| NP-zor | NP'deki her problem buna indirgenebilir | SAT, NP-zordur |
| NP-tam | Hem NP'de hem NP-zordur | SAT, ilk kanıtlanan NP-tam problemdir |

Birisi bize değişken atamasını sertifika olarak verirse formülü doğrusal ya da polinoma yakın sürede değerlendirebiliriz. Zor olan, bu sertifikayı bulmaktır.

1971 tarihli **Cook–Levin Teoremi**, SAT'ın NP-tam olduğunu gösterdi. Teoremin özündeki fikir şudur: NP'deki herhangi bir problemin polinom zamanlı hesaplama adımları, bir Boole formülüyle temsil edilebilir. Oluşturulan formül ancak ve ancak özgün problem örneğinin geçerli bir çözümü varsa sağlanabilir.

Bu dönüşüme **polinom zamanlı indirgeme** denir:

$$
A \leq_p SAT
$$

Buradaki ifade, $A$ probleminin örneklerini polinom zamanda SAT örneklerine çevirebildiğimizi anlatır. Bu nedenle SAT için polinom zamanlı bir algoritma bulunursa NP'deki bütün problemler polinom zamanda çözülebilir ve $P=NP$ sonucu elde edilir.

## CNF ve 3-SAT neden sık kullanılır?

SAT formülleri çoğunlukla **Konjonktif Normal Form** ile yazılır. CNF, OR ile bağlanan değişmezlerin oluşturduğu tümcelerin AND ile birleştirilmesidir:

$$
(x \lor \neg y \lor z) \land (y \lor w) \land (\neg x \lor \neg w)
$$

Her tümcede tam üç değişmez bulunan özel sürüme **3-SAT** denir. Kısıtlı görünmesine rağmen 3-SAT da NP-tamdır. Bu düzenli yapı, başka problemlerin SAT'a veya SAT'tan başka problemlere indirgenmesini kolaylaştırır.

## Küçük bir SAT çözücüsü

Aşağıdaki Python kodu bütün atamaları deneyerek verilen CNF formülünü çözer. Her tümce `(değişken, negatif_mi)` çiftlerinden oluşur:

```python
from itertools import product

def solve_sat(variables, clauses):
    for values in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))

        def literal_value(literal):
            variable, is_negative = literal
            value = assignment[variable]
            return not value if is_negative else value

        if all(any(literal_value(lit) for lit in clause)
               for clause in clauses):
            return assignment
    return None

clauses = [
    [("x", False), ("y", False)],
    [("x", True), ("z", False)]
]

print(solve_sat(["x", "y", "z"], clauses))
```

Kod öğretici olsa da üstel sayıda atama dener. Gerçek SAT çözücüleri DPLL, birim yayılımı, geri izleme ve CDCL gibi tekniklerle arama uzayının büyük bölümlerini eler. En kötü durum hâlâ üstel olabilir; ancak modern çözücüler milyonlarca değişken içeren pratik örneklerde şaşırtıcı derecede başarılıdır.

SAT'ın büyüsü burada yatar: Sorusu küçücük, sonuçları devasa! Devre doğrulama, paket bağımlılıkları, Sudoku, görev planlama ve yazılım testi gibi problemler Boole kısıtlarına çevrilebilir. Bu yüzden SAT yalnızca teorik bir bilmece değil, hem $P$ ile $NP$ arasındaki gizemin kapısı hem de güçlü bir mühendislik aracıdır.
