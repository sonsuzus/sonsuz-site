---
layout: post
title: "Sihirli Kareler ve Küpler: Sayıların Dengeli Dansı"
math: true
categories: 
  - Bilgi
tags: 
  - sihirli kare
  - sihirli küp
  - algoritma
  - python
  - matematik
  - kombinatorik
toc: true
image: /img/sihirli-kareler-ve-51.png
---

![sihirli-kareler-ve-51](/img/sihirli-kareler-ve-51.svg)


Bir sayı tablosunun bütün satırları, sütunları ve köşegenleri aynı toplamı veriyorsa ortada matematiksel bir sihir var demektir. Ancak tavşan da şapka da yok: Sihirli kareler ve onların üç boyutlu akrabaları olan sihirli küpler, kombinatorik düzenleme algoritmalarına dayanır. Bu yapılar; algoritmik düşünme, arama yöntemleri ve kısıt programlama için oldukça eğlenceli çalışma alanlarıdır.
``

## Sihirli toplam nereden gelir?

$n \times n$ boyutlu normal bir sihirli kare, $1$ ile $n^2$ arasındaki sayıları tam olarak birer kez içerir. Bütün satırların, sütunların ve iki ana köşegenin toplamı aynı olmalıdır.

Karedeki sayıların toplamı:

$$
1+2+\cdots+n^2=\frac{n^2(n^2+1)}{2}
$$

Bu toplam $n$ satıra eşit biçimde dağıldığı için sihirli sabit şöyledir:

$$
M_2=\frac{n(n^2+1)}{2}
$$

Örneğin $n=3$ için $M_2=15$ olur.

| Boyut | Kullanılan sayılar | Sihirli toplam |
|---|---:|---:|
| $3 \times 3$ | 1–9 | 15 |
| $4 \times 4$ | 1–16 | 34 |
| $5 \times 5$ | 1–25 | 65 |

## Tek dereceli kareler: Siyam yöntemi

$n$ tek olduğunda en meşhur oluşturma tekniği **Siyam yöntemi**dir. Önce 1 sayısı üst satırın ortasına yerleştirilir. Her yeni sayı için bir satır yukarı ve bir sütun sağa gidilir. Tahtanın dışına çıkılırsa karşı kenardan devam edilir. Hedef hücre doluysa son konumdan bir satır aşağı inilir.

```python
def magic_square(n):
    if n % 2 == 0:
        raise ValueError("Bu yöntem yalnızca tek boyutlarda çalışır.")

    square = [[0] * n for _ in range(n)]
    row, col = 0, n // 2

    for number in range(1, n * n + 1):
        square[row][col] = number
        next_row = (row - 1) % n
        next_col = (col + 1) % n

        if square[next_row][next_col] != 0:
            row = (row + 1) % n
        else:
            row, col = next_row, next_col

    return square

for line in magic_square(3):
    print(line, "toplam:", sum(line))
```

Modulo (`%`) işlemi burada tahtanın kenarlarını birer geçit hâline getirir. Böylece yukarıdan çıkan konum aşağıdan, sağdan çıkan konum soldan geri döner. Algoritmanın çalışma süresi $O(n^2)$, bellek kullanımı da oluşturulan tablo nedeniyle $O(n^2)$ seviyesindedir.

## Her kare aynı yöntemle mi oluşturulur?

Hayır. Kareler boyutlarına göre farklı ailelere ayrılır:

| Kare türü | Koşul | Yaygın yaklaşım |
|---|---|---|
| Tek dereceli | $n \bmod 2=1$ | Siyam yöntemi |
| Çift-çift | $n \bmod 4=0$ | Tamamlama ve tersleme |
| Tek-çift | $n \bmod 4=2$ | Alt kareleri birleştirme |

Örneğin $4 \times 4$ karelerde sayılar sırayla yazılıp belirli köşegen desenlerindeki değerler $n^2+1-x$ dönüşümüyle terslenebilir. Buna karşılık $6 \times 6$ gibi tek-çift boyutlar daha zahmetlidir; kare genellikle tek dereceli alt karelere bölünür ve seçilmiş sütunlar yer değiştirilir.

## Üçüncü boyuta geçiş: Sihirli küpler

$n \times n \times n$ sihirli küp, $1$ ile $n^3$ arasındaki sayıları içerir. Her eksene paralel doğru aynı toplamı verir. Kusursuz türlerde uzay köşegenleri de bu kurala katılır. Sihirli sabit:

$$
M_3=\frac{n(n^3+1)}{2}
$$

| Özellik | Sihirli kare | Sihirli küp |
|---|---|---|
| Hücre sayısı | $n^2$ | $n^3$ |
| Temel yönler | satır, sütun | $x$, $y$, $z$ eksenleri |
| Arama uzayı | $(n^2)!$ | $(n^3)!$ |
| Doğrulama | çizgiler ve köşegenler | düzlemsel ve uzaysal çizgiler |

Küplerde doğrudan deneme yapmak hızla imkânsızlaşır. Bu nedenle **geri izleme**, kısıt yayılımı ve simetri azaltma kullanılır. Bir hücreye sayı yerleştirildiğinde ilgili çizginin toplamı sihirli sabiti aşarsa dal hemen budanır. Ayrıca küpü döndürerek elde edilen eş değer çözümlerden yalnızca biri aranır.

Sihirli düzenlerin asıl numarası sonuç değil, kısıtları akıllıca yönetmektir. Karelerde yapıcı formüller çoğu zaman yeterliyken küpler, programcıyı sezgisel arama ve optimizasyon teknikleriyle tanıştırır. Sayılar aynı toplamda buluşurken algoritmalar da matematikle el sıkışır.
