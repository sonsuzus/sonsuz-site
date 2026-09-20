---
layout: post
title: "Inclusion-Exclusion Principle: Üst Üste Binen Kümeleri Doğru Saymak"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - kombinatorik
  - kümeler
  - algoritma
  - python
toc: true
---

Bir etkinliğe katılanların 30’u Python, 25’i JavaScript biliyorsa toplam 55 yazılımcımız olduğunu düşünebiliriz. Fakat iki dili de bilenler varsa aynı kişileri iki kez saymış oluruz. Inclusion-Exclusion Principle, Türkçesiyle **Dahil Etme–Hariç Tutma İlkesi**, tam olarak bu tür üst üste binmeleri düzeltmek için kullanılan zarif bir sayma yöntemidir.
``

## Temel fikir: Ekle, çakışmayı çıkar

İki sonlu küme düşünelim: $A$ ve $B$. Önce $\vert A\vert +\vert B\vert $ hesaplanır. Ancak $A \cap B$ içindeki elemanlar iki defa sayıldığı için kesişimin büyüklüğü bir kez çıkarılır:

$$
\vert A \cup B\vert  = \vert A\vert  + \vert B\vert  - \vert A \cap B\vert 
$$

Örneğin 30 kişi Python, 25 kişi JavaScript biliyor ve 10 kişi iki dili de kullanıyorsa:

$$
\vert P \cup J\vert  = 30 + 25 - 10 = 45
$$

Yani en az bir dili bilen 45 kişi vardır. Buradaki önemli fikir, kesişimdeki kişileri tamamen silmek değil, fazladan yapılan sayımı telafi etmektir.

| Yaklaşım | İşlem | Sonuç | Sorun |
|---|---:|---:|---|
| Saf toplama | $30+25$ | 55 | Ortak kişiler iki kez sayılır |
| Dahil etme–hariç tutma | $30+25-10$ | 45 | Doğru sonuç elde edilir |
| Sadece kesişimi sayma | $10$ | 10 | Yalnızca iki dili bilenleri verir |

## Üç kümede neden işler karışıyor?

Üç küme olduğunda önce tekil kümeleri ekler, sonra ikili kesişimleri çıkarırız. Fakat üç kümenin ortak bölgesi başlangıçta üç kez eklenmiş, ikili kesişimler çıkarılırken de üç kez çıkarılmıştır. Böylece hiç sayılmamış olur. Onu yeniden bir kez eklemeliyiz:

$$
\vert A \cup B \cup C\vert  = \vert A\vert +\vert B\vert +\vert C\vert 
-\vert A \cap B\vert -\vert A \cap C\vert -\vert B \cap C\vert 
+\vert A \cap B \cap C\vert 
$$

İşaretlerin sırayla artı ve eksi olması tesadüf değildir:

| Seçilen kesişim düzeyi | İşaret |
|---|---:|
| Tek kümeler | $+$ |
| İkili kesişimler | $-$ |
| Üçlü kesişimler | $+$ |
| Dörtlü kesişimler | $-$ |

Genel olarak $n$ küme için bütün boş olmayan alt küme kombinasyonları değerlendirilir. Tek sayıda kümenin kesişimi eklenir, çift sayıda kümenin kesişimi çıkarılır:

$$
\left\vert \bigcup_{i=1}^{n} A_i\right\vert 
= \sum_{\emptyset \ne S \subseteq \{1,\ldots,n\}}
(-1)^{\vert S\vert +1}\left\vert \bigcap_{i \in S} A_i\right\vert 
$$

Bu formül biraz ürkütücü görünse de aslında “bir elemanı kaç kez saydım?” sorusunun sistematik cevabıdır.

## Sayılarla pratik örnek

1 ile 100 arasındaki sayılardan 2’ye veya 3’e bölünen kaç sayı vardır? 2’ye bölünen 50, 3’e bölünen 33 sayı bulunur. Her ikisine bölünenler, yani $\operatorname{lcm}(2,3)=6$ ile bölünen 16 sayı, iki kez sayılmıştır:

$$
50+33-16=67
$$

Aşağıdaki Python fonksiyonu aynı hesabı herhangi iki bölen için yapar:

```python
def divisible_by_either(limit, a, b):
    count_a = limit // a
    count_b = limit // b

    gcd = __import__('math').gcd(a, b)
    lcm = a * b // gcd
    count_both = limit // lcm

    return count_a + count_b - count_both

print(divisible_by_either(100, 2, 3))  # 67
```

Fonksiyon, önce her bölenin katlarını sayar. Ardından ortak katların sayısını, iki sayının en küçük ortak katı üzerinden bulup çıkarır. Böylece tüm sayıları tek tek dolaşmadan $O(1)$ zamanda sonuç üretir.

## Nerelerde kullanılır?

Bu ilke yalnızca ders kitaplarında yaşamaz. Olasılık hesaplarında, veritabanı sorgularında, bit maskeli dinamik programlamada, ağ güvenliğinde ve kısıtları ihlal eden durumları saymada kullanılır. Özellikle “en az bir koşulu sağlayan” nesneleri sayarken güçlüdür.

Akılda tutulacak kısa tarif şudur: **Tekleri ekle, çiftleri çıkar, üçlüleri yeniden ekle ve işaretleri dönüşümlü sürdür.** Kümeler üst üste bindikçe paniklemek yerine, her elemanın toplamda tam bir kez sayılmasını hedefleyin.
