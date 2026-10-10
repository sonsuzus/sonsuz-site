---
layout: post
title: "Master Teorem ile Özyinelemeli Karmaşıklık Hesabı"
math: true
categories: 
  - Bilgi
tags: 
  - master teorem
  - algoritma
  - karmaşıklık
  - özyineleme
  - böl ve fethet
toc: true
image: /img/master-teorem-ile-29.png
---

Böl-fethet algoritmalarında kod birkaç satır görünebilir; fakat çalışma süresini hesaplamak bazen matematiksel bir bilmeceye dönüşür. Master Teorem, belirli biçimdeki özyineleme bağıntılarını uzun uzun açmadan sonuca ulaştıran pratik bir araçtır. Merge Sort, ikili arama ve benzeri algoritmaların karmaşıklığını bu yöntemle hızlıca sınıflandırabiliriz.
``
## Temel fikir: Problem nasıl parçalanıyor?

Bir böl-fethet algoritması genellikle üç adım uygular: problemi alt problemlere böler, bunları özyinelemeli biçimde çözer ve sonuçları birleştirir. Bu sürecin çalışma süresi şu bağıntıyla ifade edilir:

$$
T(n) = aT\left(\frac{n}{b}\right) + f(n)
$$

Buradaki değişkenlerin görevleri şöyledir:

| Sembol | Anlamı | Örnek |
|---|---|---|
| $a$ | Oluşturulan alt problem sayısı | Merge Sort için 2 |
| $b$ | Problem boyutunun küçülme oranı | Boyut yarıya iniyorsa 2 |
| $f(n)$ | Bölme ve birleştirme gibi özyineleme dışı işler | Merge Sort için $n$ |
| $T(n)$ | Toplam çalışma süresi | Aradığımız sonuç |

![master-teorem-ile-29](/img/master-teorem-ile-29.svg)


Teoremin merkezindeki karşılaştırma, $f(n)$ ile $n^{\log_b a}$ arasındadır. İkinci ifade, özyineleme ağacındaki alt problemlerin ürettiği temel iş yükünü temsil eder. Kısacası şu soruyu sorarız: Maliyeti alt problemler mi, her seviyede yapılan ek iş mi, yoksa ikisi birlikte mi büyütüyor?

## Master Teorem’in üç durumu

| Durum | Karşılaştırma | Sonuç | Baskın bölüm |
|---|---|---|---|
| 1 | $f(n)=O(n^{\log_b a-\varepsilon})$ | $\Theta(n^{\log_b a})$ | Alt problemler |
| 2 | $f(n)=\Theta(n^{\log_b a}\log^k n)$ | $\Theta(n^{\log_b a}\log^{k+1}n)$ | Dengeli |
| 3 | $f(n)=\Omega(n^{\log_b a+\varepsilon})$ | $\Theta(f(n))$ | Ek iş |

Buradaki $\varepsilon>0$, fonksiyonlar arasında polinom düzeyinde bir fark bulunduğunu belirtir. Üçüncü durumda ayrıca düzenlilik koşulu aranır: Yeterince büyük $n$ değerleri için $af(n/b)\leq cf(n)$ ve $c<1$ olmalıdır.

## Örnek: Merge Sort

Merge Sort diziyi iki eşit parçaya ayırır, iki parçayı ayrı ayrı sıralar ve doğrusal zamanda birleştirir:

$$
T(n)=2T(n/2)+n
$$

Buradan $a=2$, $b=2$ ve $f(n)=n$ elde edilir. Kritik terim:

$$
n^{\log_2 2}=n
$$

$f(n)$ ile kritik terim eşit büyüdüğü için ikinci durum geçerlidir. Sonuç:

$$
T(n)=\Theta(n\log n)
$$

Aşağıdaki Python kodu bu yapının algoritmadaki karşılığını gösterir:

```python
def merge_sort(items):
    if len(items) <= 1:
        return items

    middle = len(items) // 2
    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])
    return merge(left, right)
```

İki özyinelemeli çağrı $2T(n/2)$ terimini, `merge` işlemi ise doğrusal $n$ maliyetini oluşturur.

## İki kısa karşılaştırma

İkili aramada yalnızca bir yarı seçilir:

$$
T(n)=T(n/2)+1
$$

$a=1$, $b=2$ ve $f(n)=1$ olduğundan $n^{\log_2 1}=1$ bulunur. İkinci durum sonucunda karmaşıklık $\Theta(\log n)$ olur.

Şu bağıntıda ise birleştirme işi daha pahalıdır:

$$
T(n)=2T(n/2)+n^2
$$

Kritik terim $n$ iken $f(n)=n^2$ daha hızlı büyür. Düzenlilik koşulu da sağlandığından üçüncü durum uygulanır ve sonuç $\Theta(n^2)$ çıkar.

## Ne zaman kullanılamaz?

Master Teorem her özyineleme bağıntısına uymaz. Alt problemlerin eşit boyutta olmadığı $T(n)=T(n/3)+T(2n/3)+n$ veya boyutun sabit miktarda azaldığı $T(n)=T(n-1)+n$ biçimleri doğrudan kapsam dışındadır. Böyle durumlarda özyineleme ağacı, yerine koyma yöntemi ya da Akra–Bazzi teoremi tercih edilebilir.

Pratik reçete basittir: Önce $a$, $b$ ve $f(n)$ değerlerini çıkarın; ardından $n^{\log_b a}$ terimini hesaplayın ve $f(n)$ ile karşılaştırın. Üç durumdan doğru olanı seçtiğinizde, karmaşıklık hesabı korkutucu bir denklem olmaktan çıkıp kısa bir eşleştirme oyununa dönüşür.
