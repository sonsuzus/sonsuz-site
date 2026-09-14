---
layout: post
title: "SSA Formu: Derleyiciler Kodumuzu Neden Yeniden Yazar?"
math: true
categories: 
  - Bilgi
tags: 
  - ssa
  - derleyiciler
  - optimizasyon
  - ara temsil
  - algoritmalar
toc: true
---

Yazdığımız kod derleyiciye ulaştığında değişmez bir kutsal metin gibi korunmaz. Tam tersine; parçalanır, sadeleştirilir ve analiz edilmesi daha kolay biçimlere dönüştürülür. Bu dönüşümlerin en önemlilerinden biri **Static Single Assignment**, kısaca SSA formudur. SSA sayesinde derleyici, her değerin nerede üretildiğini daha rahat görür ve kod üzerinde güvenli optimizasyonlar yapabilir.

``

## SSA’nın temel fikri

SSA formundaki ana kural son derece basittir: **Her değişken yalnızca bir kez atanır.** Kaynak programda aynı değişkene defalarca değer verebiliriz:

```c
int x = 4;
x = x + 2;
x = x * 3;
```

Derleyici bunu SSA biçiminde her atamaya farklı bir sürüm vererek temsil eder:

```text
x1 = 4
x2 = x1 + 2
x3 = x2 * 3
```

Burada `x1`, `x2` ve `x3` birbirinden farklı değerlerdir. Matematiksel olarak her tanım ile kullanım arasında açık bir ilişki oluşur:

$$
x_1 = 4, \qquad x_2 = x_1 + 2, \qquad x_3 = 3x_2
$$

Böylece derleyici “Bu `x` hangi atamadan geliyor?” diye dedektiflik yapmak zorunda kalmaz. Her kullanımın tek bir tanımı vardır. Bu ilişki genellikle **use-def zinciri** olarak adlandırılır.

| Özellik | Normal ara temsil | SSA formu |
|---|---|---|
| Değişkene atama | Birden fazla olabilir | Her sürüme yalnızca bir kez |
| Değerin kaynağını bulma | Geriye doğru analiz gerekebilir | Doğrudan görülebilir |
| Sabit yayılımı | Daha karmaşık | Daha kolay |
| Ölü kod tespiti | Ek veri akışı analizi ister | Kullanılmayan tanımlar açıktır |
| Kontrol akışı birleşimi | Belirsizlik oluşturabilir | `phi` fonksiyonu kullanılır |

## Yol ayrımında phi fonksiyonu

Tek atama kuralı, `if` gibi kontrol akışı yapılarında ilginç bir sorun doğurur:

```c
int x;
if (score > 50)
    x = 10;
else
    x = 20;
return x;
```

İki farklı yürütme yolu, dönüş noktasına farklı `x` değerleri getirir. SSA bu birleşimi **phi ($\phi$) fonksiyonu** ile gösterir:

```text
if score > 50:
    x1 = 10
else:
    x2 = 20

x3 = phi(x1, x2)
return x3
```

$\phi$ fonksiyonu çalışma zamanında çağrılan sıradan bir fonksiyon değildir. “Kontrol hangi bloktan geldiyse o blokta üretilen değeri seç” anlamına gelen ara temsil talimatıdır:

$$
x_3 = \phi(x_1, x_2)
$$

Döngülerde de aynı fikir kullanılır. Sayaç değişkeninin başlangıç değeri ile önceki iterasyondan gelen değeri bir `phi` düğümünde birleşir. Bu yapı, döngü değişmezlerini ve tümevarım değişkenlerini fark etmeyi kolaylaştırır.

## Derleyici bundan ne kazanır?

SSA yalnızca değişkenlerin sonuna numara ekleyen kozmetik bir işlem değildir. Pek çok optimizasyonun altyapısını hazırlar:

- **Sabit yayılımı:** `a1 = 5` biliniyorsa `b1 = a1 + 3`, doğrudan `b1 = 8` olabilir.
- **Ölü kod eleme:** Bir SSA değeri hiç kullanılmıyorsa onu üreten işlem kaldırılabilir.
- **Ortak alt ifade eleme:** Aynı girdilerle tekrarlanan hesaplamalar paylaşılabilir.
- **Kopya yayılımı:** Yalnızca başka bir değeri kopyalayan gereksiz tanımlar temizlenebilir.
- **Aralık analizi:** Bir değerin mümkün olan alt ve üst sınırları daha kolay izlenebilir.

Örneğin:

```text
a1 = 6
b1 = a1 * 2
c1 = a1 * 2
result1 = b1 + c1
```

Derleyici, `b1` ile `c1` hesaplarının aynı olduğunu görerek ikinci çarpma işlemini kaldırabilir. Ardından sabit yayılımıyla sonuç tamamen hesaplanabilir.

## SSA nasıl oluşturulur?

Derleyici önce programı **kontrol akışı grafiğine** böler. Ardından hangi blokların diğer bloklara hükmettiğini belirleyen **dominance** ilişkisini hesaplar. Bir tanımın birden fazla akış yolunda birleştiği uygun noktalara `phi` düğümleri yerleştirilir ve değişkenler sürümlere ayrılarak yeniden adlandırılır.

Makine kodunda sonsuz sayıda SSA değişkeni bulunmaz; işlemcinin sınırlı sayıda yazmacı vardır. Bu yüzden optimizasyonlardan sonra SSA formu çözülür, `phi` düğümleri kopyalama işlemlerine dönüştürülür ve değerler yazmaçlara ya da belleğe atanır.

Kısacası derleyici kodumuzu yeniden yazar çünkü insan dostu sözdizimi, güçlü analizler için her zaman uygun değildir. SSA; değerlerin geçmişini görünür kılan, optimizasyonları güvenli hâle getiren ve modern derleyicilerin karmaşık kod üzerinde daha az tahminle çalışmasını sağlayan düzenli bir hesap haritasıdır.
