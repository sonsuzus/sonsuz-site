---
layout: post
title: "Ekleme-Çıkarma İlkesi: Kesişen Kümeleri Hatasız Sayma"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - kombinatorik
  - kümeler
  - sayma
  - algoritma
  - python
toc: true
image: /img/ekleme-cikarma-ilkesi-26.png
---

Bir etkinliğe katılanların kaçının kahve veya çay içtiğini bulmak kulağa kolay gelir: Kahve içenlerle çay içenleri topla! Fakat bazı kişiler ikisini de içiyorsa onları iki kez saymış oluruz. Ekleme-Çıkarma İlkesi, diğer adıyla Dahil Etme-Hariç Tutma İlkesi, tam olarak bu tür çakışmaları düzeltmek için kullanılan güçlü bir sayma yöntemidir.


![ekleme-cikarma-ilkesi-26](/img/ekleme-cikarma-ilkesi-26.svg)

``

## Temel fikir: Önce ekle, sonra fazlalığı çıkar

İki sonlu küme düşünelim: $A$ ve $B$. Bu kümelerin birleşimi, en az birine ait olan elemanlardan oluşur. Yalnızca $\vert A\vert +\vert B\vert $ işlemini yaparsak $A \cap B$ kesişimindeki elemanları iki defa sayarız. Bu fazlalığı gidermek için kesişimin eleman sayısını bir kez çıkarmamız gerekir:

$$
\vert A \cup B\vert  = \vert A\vert  + \vert B\vert  - \vert A \cap B\vert 
$$

Buradaki dikey çizgiler kümenin eleman sayısını ifade eder. İlkenin mantığı küçük bir muhasebe işlemine benzer: Her şeyi kasaya ekler, yanlışlıkla iki kez kaydedilenleri geri çıkarırız.

| Bölge | İlk toplamada sayılma sayısı | Düzeltme sonrası |
|---|---:|---:|
| Yalnızca $A$ | 1 | 1 |
| Yalnızca $B$ | 1 | 1 |
| $A \cap B$ | 2 | 1 |
| İki kümenin de dışında | 0 | 0 |

## İki kümeli örnek

Bir sınıfta 24 öğrenci Python, 18 öğrenci JavaScript biliyor olsun. Her iki dili bilen 9 öğrenci varsa en az bir dili bilenlerin sayısı şöyledir:

$$
\vert P \cup J\vert  = 24 + 18 - 9 = 33
$$

Burada $24+18=42$ demek hatalıdır; çünkü iki dili bilen 9 öğrenci toplamın içinde iki kez görünür. Bu öğrencileri bir kez çıkardığımızda doğru sonuç olan 33'e ulaşırız.

Hiçbir dili bilmeyenlerin sayısı sorulursa evrensel kümeden yararlanabiliriz. Sınıfta toplam 40 öğrenci varsa:

$$
40-\vert P \cup J\vert =40-33=7
$$

Dolayısıyla 7 öğrenci iki dilden hiçbirini bilmemektedir.

## Üç kümede neden yeniden ekleme yapıyoruz?

Üç küme söz konusu olduğunda önce tekil kümeler eklenir, ardından tüm ikili kesişimler çıkarılır. Ancak üç kümenin ortak bölgesi başlangıçta üç kez eklenmiş, ikili kesişimler çıkarılırken de üç kez çıkarılmış olur. Böylece hiç sayılmamış hale gelir. Onu bir kez yeniden eklemeliyiz:

$$
\vert A \cup B \cup C\vert  = \vert A\vert +\vert B\vert +\vert C\vert 
-\vert A \cap B\vert -\vert A \cap C\vert -\vert B \cap C\vert 
+\vert A \cap B \cap C\vert 
$$

| Aşama | İşaret | Amaç |
|---|---:|---|
| Tek kümeler | $+$ | Bütün adayları saymak |
| İkili kesişimler | $-$ | Çift sayımları düzeltmek |
| Üçlü kesişim | $+$ | Fazla çıkarılan ortak bölgeyi geri eklemek |

İşaretlerin sırayla artı ve eksi olması tesadüf değildir. Genel durumda tek sayıda kümenin kesişimleri eklenir, çift sayıda kümenin kesişimleri çıkarılır.

## Python ile hesaplama

Aşağıdaki fonksiyon, üç kümenin birleşim büyüklüğünü gerçek küme işlemleriyle hesaplar ve formül sonucuyla karşılaştırır:

```python
def birlesim_sayisi(a, b, c):
    formule_gore = (
        len(a) + len(b) + len(c)
        - len(a & b) - len(a & c) - len(b & c)
        + len(a & b & c)
    )
    dogrudan = len(a | b | c)
    return formule_gore, dogrudan

A = {1, 2, 3, 4}
B = {3, 4, 5}
C = {4, 5, 6}

print(birlesim_sayisi(A, B, C))  # (6, 6)
```

`&` kesişimi, `|` ise birleşimi temsil eder. İki sonucun eşit çıkması, formülün aynı elemanı tekrar tekrar saymadan çalıştığını gösterir.

## Sık yapılan hatalar

En yaygın hata, kesişimleri hiç çıkarmamaktır. Bir diğer hata ise “yalnızca iki kümeye ait olanlar” ile “iki kümenin kesişimi” ifadelerini aynı sanmaktır. Örneğin $A \cap B$, aksi belirtilmedikçe $C$'de bulunan ortak elemanları da kapsar. Ayrıca “en az biri” birleşimi, “hepsi” kesişimi, “hiçbiri” ise birleşimin tümleyenini işaret eder.

Ekleme-Çıkarma İlkesi; anketlerden olasılığa, sayıların bölünebilirliğinden algoritma analizine kadar pek çok alanda kullanılır. Ana strateji basittir: Çakışmaları belirle, kaç kez sayıldıklarını izle ve artı-eksi düzeltmelerini sırayla uygula.
