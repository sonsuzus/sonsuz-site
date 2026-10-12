---
layout: post
title: "Armstrong Sayıları: Basamaklardan Doğan Matematiksel Sihir"
math: true
categories: 
  - Program
tags: 
  - armstrong sayıları
  - python
  - algoritma
  - matematik
  - basamak işlemleri
  - özel sayılar
toc: true
image: /img/armstrong-sayilari-basamaklardan-27.png
---

Bazı sayılar sıradan görünürken basamaklarına ayrıldıklarında küçük bir matematik gösterisi yapar. Armstrong sayıları da tam olarak bu gruptadır: Her basamağın belirli bir kuvvetini alıp topladığımızda sayının kendisine geri döneriz. Bu özellik hem basamak işlemlerini öğrenmek hem de döngü, fonksiyon ve algoritma karmaşıklığı pratiği yapmak için harika bir bahanedir.
``
Bir sayının Armstrong sayısı olup olmadığını anlamadan önce tanımı netleştirelim. Pozitif bir $n$ sayısının basamak sayısı $k$ ve basamakları $d_1,d_2,\ldots,d_k$ olsun. Eğer

$$
n = \sum_{i=1}^{k} d_i^k
$$

eşitliği sağlanıyorsa bu sayı bir Armstrong sayısıdır. Bu sayılara **narsistik sayılar** da denir. Buradaki önemli ayrıntı, her basamağın kuvvetinin sayının toplam basamak sayısına eşit olmasıdır.

Örneğin $153$ üç basamaklıdır. Dolayısıyla her basamağın üçüncü kuvveti alınır:

$$
1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153
$$

Sonuç yine $153$ olduğundan sayı Armstrong özelliği taşır. Buna karşılık $123$ için aynı işlem $1+8+27=36$ sonucunu verir; yani sihir gerçekleşmez.

| Sayı | Basamak sayısı | Kuvvetler toplamı | Armstrong mı? |
|---:|---:|---:|:---:|
| 153 | 3 | $1^3+5^3+3^3=153$ | Evet |
| 370 | 3 | $3^3+7^3+0^3=370$ | Evet |
| 9474 | 4 | $9^4+4^4+7^4+4^4=9474$ | Evet |
| 123 | 3 | $1^3+2^3+3^3=36$ | Hayır |

## Python ile tek sayı kontrolü

Sayıyı metne dönüştürmek, basamaklara erişmenin en okunabilir yollarından biridir:

```python
def armstrong_mu(sayi):
    basamaklar = str(sayi)
    kuvvet = len(basamaklar)

    toplam = sum(int(basamak) ** kuvvet
                 for basamak in basamaklar)
    return toplam == sayi

for sayi in [153, 123, 370, 9474]:
    print(sayi, armstrong_mu(sayi))
```

Fonksiyon önce basamak sayısını belirler. Ardından her karakteri tekrar tam sayıya çevirir, uygun kuvveti hesaplar ve sonuçları toplar. Son satırda toplam ile başlangıçtaki sayı karşılaştırılır. Böylece kontrol mantığı yeniden kullanılabilir küçük bir fonksiyona dönüşür.

Metin dönüşümü kullanmadan, yalnızca aritmetik işlemlerle de basamakları ayırabiliriz. $n \bmod 10$ son basamağı verirken, $n // 10$ son basamağı sayıdan çıkarır:

```python
def aralikta_armstrong(baslangic, bitis):
    bulunanlar = []

    for sayi in range(baslangic, bitis + 1):
        kuvvet = len(str(sayi))
        gecici = sayi
        toplam = 0

        while gecici > 0:
            basamak = gecici % 10
            toplam += basamak ** kuvvet
            gecici //= 10

        if toplam == sayi:
            bulunanlar.append(sayi)

    return bulunanlar

print(aralikta_armstrong(1, 10000))
```

Burada `gecici` değişkeni önemlidir; doğrudan `sayi` üzerinde bölme yapsaydık karşılaştıracağımız özgün değeri kaybederdik. Algoritma, verilen aralıktaki her sayıyı tek tek inceler.

## Karmaşıklık ve optimizasyon

Üst sınır $N$, sayıların ortalama basamak sayısı da $k$ ise yaklaşık zaman karmaşıklığı $O(Nk)$ olur. Küçük aralıklarda bu son derece yeterlidir. Daha büyük aramalarda $0^k$ ile $9^k$ arasındaki sonuçları önceden bir tabloda saklamak, aynı kuvvet hesaplarını tekrar yapmayı önler.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Metne dönüştürme | Kısa ve okunabilir | Karakter dönüşümü yapar |
| Mod ve bölme | Sayısal mantığı öğretir | Biraz daha uzun kodlanır |
| Kuvvetleri önbellekleme | Büyük aralıklarda hız kazandırır | Ek hazırlık ve bellek ister |

Aynı şablon; mutlu sayılar, mükemmel sayılar ve rakamları toplamına bölünebilen Harshad sayıları gibi özel sayı problemlerine de uyarlanabilir. Değişen şey çoğunlukla basamaklara uygulanan kuraldır. Kısacası Armstrong sayıları yalnızca matematiksel bir merak değil, problemi parçalama ve temiz fonksiyon tasarlama konusunda eğlenceli bir algoritma laboratuvarıdır.

![armstrong-sayilari-basamaklardan-27](/img/armstrong-sayilari-basamaklardan-27.svg)

