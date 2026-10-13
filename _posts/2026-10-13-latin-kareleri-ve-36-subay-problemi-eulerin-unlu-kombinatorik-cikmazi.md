---
layout: post
title: "Latin Kareleri ve 36 Subay Problemi: Euler’in Ünlü Kombinatorik Çıkmazı"
math: true
categories: 
  - Bilgi
tags: 
  - latin kareleri
  - kombinatorik
  - euler
  - 36 subay problemi
  - ortogonal kareler
  - matematik
toc: true
image: /img/latin-kareleri-ve-93.png
---

Bir orduda altı farklı rütbeden ve altı farklı alaydan toplam 36 subay bulunduğunu düşünün. Euler’in sorusu ilk bakışta masumdur: Bu subaylar, her satırda ve sütunda her rütbe ile her alay tam bir kez görünecek biçimde $6 \times 6$ bir kareye yerleştirilebilir mi? Küçük bir sudoku havası taşıyan bu soru, kombinatoriğin en ünlü çıkmazlarından birine dönüşmüştür.

``

## Latin karesi nedir?

$n$ farklı sembolün, her satırda ve her sütunda tam bir kez yer aldığı $n \times n$ tabloya **Latin karesi** denir. Adı, ilk örneklerde sembol olarak Latin harflerinin kullanılmasından gelir.

Örneğin üçüncü dereceden bir Latin karesi şöyledir:

|   | 1. sütun | 2. sütun | 3. sütun |
|---|---|---|---|
| 1. satır | A | B | C |
| 2. satır | B | C | A |
| 3. satır | C | A | B |

![latin-kareleri-ve-93](/img/latin-kareleri-ve-93.svg)


Bu yapının döngüsel örneği matematiksel olarak

$$L(i,j)=(i+j)\bmod n$$

formülüyle üretilebilir. Burada hücredeki sembol, satır ve sütun indislerinin modüler toplamıdır. Böylece hiçbir sembol aynı satırda veya sütunda tekrarlanmaz.

## İki kare neden gerekiyor?

36 Subay Problemi’nde yalnızca rütbeleri düzgün yerleştirmek yetmez; alayların da aynı koşulu sağlaması gerekir. Dolayısıyla biri rütbeleri, diğeri alayları gösteren iki Latin karesine ihtiyaç vardır. Üstelik bu kareler üst üste getirildiğinde her sıralı ikili tam bir kez görünmelidir.

Bu özelliğe sahip karelere **ortogonal Latin kareleri** denir. $L_1$ ve $L_2$ kareleri için bütün

$$(L_1(i,j),L_2(i,j))$$

çiftleri birbirinden farklı olmalıdır. Altıncı derecede toplam $6^2=36$ hücre bulunduğundan, altı rütbe ve altı alayın oluşturduğu 36 olası eşleşmenin her biri tam bir hücreye düşmelidir.

| Kavram | Satır ve sütun koşulu | Hücre çiftleri koşulu |
|---|---|---|
| Latin karesi | Her sembol bir kez görünür | Uygulanmaz |
| Ortogonal Latin kareleri | İki kare de Latin karesidir | Her ikili yalnızca bir kez görünür |
| 36 Subay düzeni | Rütbe ve alaylar tekrarlanmaz | 36 eşleşmenin tamamı kullanılır |

## Euler’in tahmini ve şaşırtıcı sonuç

Euler, $n \equiv 2 \pmod 4$ olan derecelerde ortogonal Latin karelerinin bulunmadığını düşündü. Buna göre $n=2,6,10,14,\ldots$ değerlerinin tamamı sorunlu olmalıydı. Altıncı derece için çözüm bulamaması da bu düşünceyi güçlendirdi.

Ancak burada matematiğin sevdiği bir ters köşe vardır. Gaston Tarry, 1900 civarında bütün olasılıkları sistematik biçimde inceleyerek $n=6$ için çözüm bulunmadığını kanıtladı. Buna karşılık Bose, Shrikhande ve Parker, 1959–1960 yıllarında Euler’in genel tahminini çürüttü: $n=2$ ve $n=6$ dışında her $n$ için bir çift ortogonal Latin karesi vardır. Yani 36 subay gerçekten çıkmazdadır, fakat daha büyük “$4k+2$” orduları aynı kaderi paylaşmaz.

## Bir çözüm adayını kodla denetlemek

Aşağıdaki Python fonksiyonu iki tablonun Latin karesi olup olmadığını ve üst üste bindirilen çiftlerin tekrarlanıp tekrarlanmadığını kontrol eder:

```python
def ortogonal_mi(a, b):
    n = len(a)
    semboller = set(range(n))

    for kare in (a, b):
        for satir in kare:
            if set(satir) != semboller:
                return False
        for sutun in zip(*kare):
            if set(sutun) != semboller:
                return False

    ciftler = {
        (a[i][j], b[i][j])
        for i in range(n)
        for j in range(n)
    }
    return len(ciftler) == n * n
```

Kod önce her satır ve sütunun tam sembol kümesini içerdiğini doğrular. Ardından hücre çiftlerini bir kümeye ekler. Kümenin büyüklüğü $n^2$ ise bütün eşleşmeler benzersizdir. Elbette fonksiyon $n=6$ için ne kadar hevesli aday verirsek verelim `True` döndürecek bir çift bulamaz; sorun programda değil, matematiğin kendisindedir.

Latin kareleri bugün deney tasarımı, hata düzelten kodlar, turnuva planlama ve kriptografi gibi alanlarda kullanılır. Euler’in çözemediği bulmaca ise önemli bir ders bırakır: Bir örnek için başarısız olmak genel bir kural önermeye yetebilir, fakat o kuralı kanıtlamaya yetmez.
