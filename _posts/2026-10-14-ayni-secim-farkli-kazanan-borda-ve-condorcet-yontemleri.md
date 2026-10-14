---
layout: post
title: "Aynı Seçim, Farklı Kazanan: Borda ve Condorcet Yöntemleri"
math: true
categories: 
  - Bilgi
tags: 
  - oylama
  - borda
  - condorcet
  - sosyal-seçim
  - algoritma
  - matematik
toc: true
image: /img/ayni-secim-farkli-60.png
---

Bir seçimde en çok oyu alan adayın kazanacağını düşünmek doğaldır. Ancak seçmenler yalnızca tek aday belirtmek yerine adayları tercih sırasına koyduğunda işler değişir. Oyları nasıl puanladığımız veya adayları nasıl karşılaştırdığımız, aynı tercihlerden farklı kazananlar çıkarabilir. Borda ve Condorcet yöntemleri, bu şaşırtıcı durumun en güzel örneklerindendir.

``

## Tercihli oylamanın temel fikri

Üç adayımız olsun: Ada, Bora ve Ceren. Seçmenlerden adayları en beğendiklerinden en az beğendiklerine doğru sıralamalarını isteyelim. Sonuçlar şöyle olsun:

| Seçmen sayısı | 1. tercih | 2. tercih | 3. tercih |
|---:|---|---|---|
| 4 | Ada | Bora | Ceren |
| 3 | Bora | Ceren | Ada |
| 2 | Ceren | Bora | Ada |

![ayni-secim-farkli-60](/img/ayni-secim-farkli-60.svg)


Burada yalnızca birinci tercihlere bakarsak Ada 4, Bora 3, Ceren 2 oy alır. Basit çoğulluk yöntemi Ada'yı kazanan ilan eder. Fakat sıralamanın geri kalanını da hesaba katarsak sonuç değişebilir.

## Borda sayımı: Her sıraya puan

Borda yönteminde adaylar bulundukları sıraya göre puan kazanır. $m$ aday varsa birinci sıraya $m-1$, ikinci sıraya $m-2$ ve son sıraya $0$ puan verilebilir. Üç aday için puanlar sırasıyla $2$, $1$ ve $0$ olur.

Bir adayın toplam Borda puanı şu şekilde ifade edilir:

$$B(a)=\sum_{i=1}^{n} p_i(a)$$

Burada $p_i(a)$, $i$ numaralı seçmenin $a$ adayına verdiği sıra puanıdır. Örneğimizde puanlar şöyledir:

| Aday | Puan hesabı | Toplam |
|---|---|---:|
| Ada | $4\times2+3\times0+2\times0$ | 8 |
| Bora | $4\times1+3\times2+2\times1$ | 12 |
| Ceren | $4\times0+3\times1+2\times2$ | 7 |

Borda kazananı Bora'dır. Ada daha fazla seçmenin ilk tercihi olmasına rağmen birçok seçmen tarafından son sıraya konmuştur. Bora ise geniş bir uzlaşma sağlamıştır. Borda, güçlü sevgiyi ödüllendirirken genel kabulü de önemser.

## Condorcet: Bire bir düello

Condorcet yaklaşımı puan toplamak yerine adayları ikili karşılaştırır. Bir aday, diğer bütün adayları bire bir seçimlerde yeniyorsa **Condorcet kazananı** olur.

Örneğin Bora ile Ada karşılaştırıldığında ilk gruptaki 4 seçmen Ada'yı, diğer 5 seçmen Bora'yı üstün tutar. Bora, Ada'yı $5$–$4$ yener. Bora ile Ceren karşılaşmasında ise ilk iki grup, yani 7 seçmen Bora'yı Ceren'in önüne koyar. Böylece Bora yine kazanır ve Condorcet kazananı olur.

| Yöntem | Neye odaklanır? | Bu örnekte kazanan |
|---|---|---|
| Basit çoğulluk | Birinci tercihler | Ada |
| Borda | Tüm sıraların puanı | Bora |
| Condorcet | İkili karşılaşmalar | Bora |

Borda ve Condorcet her zaman aynı sonucu vermez. Ayrıca Condorcet kazananı bulunmayabilir: Ada Bora'yı, Bora Ceren'i, Ceren de Ada'yı yenebilir. Bu duruma **Condorcet döngüsü** denir; tercihler taş-kâğıt-makas oyununa dönüşür.

## Küçük bir Python uygulaması

Aşağıdaki kod, sıralı oyların Borda puanlarını hesaplar:

```python
from collections import defaultdict

oylar = [
    (4, ["Ada", "Bora", "Ceren"]),
    (3, ["Bora", "Ceren", "Ada"]),
    (2, ["Ceren", "Bora", "Ada"]),
]

puanlar = defaultdict(int)
aday_sayisi = len(oylar[0][1])

for secmen, siralama in oylar:
    for sira, aday in enumerate(siralama):
        puanlar[aday] += secmen * (aday_sayisi - sira - 1)

print(dict(puanlar))
print("Kazanan:", max(puanlar, key=puanlar.get))
```

Döngü, her adayın sıra puanını o tercihi paylaşan seçmen sayısıyla çarpar. Çıktıda Bora 12 puanla kazanır.

Sonuç olarak seçim yöntemi tarafsız bir ayrıntı değil, sonucun parçasıdır. Basit çoğulluk güçlü birinci tercihleri, Borda genel memnuniyeti, Condorcet ise bire bir üstünlüğü ölçer. Bu nedenle “Kim kazandı?” sorusundan önce “Oyları hangi kuralla saydık?” diye sormak gerekir.
