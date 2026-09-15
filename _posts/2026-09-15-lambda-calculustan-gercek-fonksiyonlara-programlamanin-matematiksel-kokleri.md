---
layout: post
title: "Lambda Calculus’tan Gerçek Fonksiyonlara: Programlamanın Matematiksel Kökleri"
math: true
categories: 
  - Bilgi
tags: 
  - lambda-calculus
  - fonksiyonel-programlama
  - matematik
  - programlama
  - algoritma
  - bilgisayar-bilimi
toc: true
---

Bir programlama dilinde fonksiyon yazarken aslında 1930’larda ortaya atılmış matematiksel bir modelin izlerini takip ederiz. Parametreler, dönüş değerleri, anonim fonksiyonlar ve closure gibi modern araçların kökünde **lambda calculus** bulunur. Üstelik bu model, bilgisayarların henüz oda büyüklüğünde bile olmadığı bir dönemde geliştirilmiştir!

``

## Lambda calculus nedir?

Lambda calculus, Alonzo Church tarafından hesaplanabilirliği incelemek amacıyla geliştirilen küçük fakat güçlü bir biçimsel sistemdir. Yalnızca üç temel yapıdan oluşur:

1. **Değişken:** $x$
2. **Fonksiyon tanımı:** $\lambda x.M$
3. **Fonksiyon uygulaması:** $M\ N$

Örneğin kendisine verilen değeri değiştirmeden döndüren özdeşlik fonksiyonu şöyledir:

$$
\lambda x.x
$$

Bu fonksiyona $5$ uygularsak ifade $(\lambda x.x)\ 5$ olur ve sonuç $5$ çıkar. Burada gerçekleşen işleme **beta indirgeme** denir:

$$
(\lambda x.M)\ N \rightarrow M[x := N]
$$

Sözel olarak: Fonksiyon gövdesindeki $x$ değişkenlerini, verilen $N$ değeriyle değiştir. Yani beta indirgeme, matematik dünyasının fonksiyon çağrısıdır.

## Matematikten koda geçiş

Lambda ifadelerinin modern dillerdeki karşılıkları şaşırtıcı derecede açıktır:

| Lambda calculus | Programlama karşılığı | Örnek |
|---|---|---|
| $\lambda x.x$ | Anonim fonksiyon | `x => x` |
| Fonksiyon uygulaması | Fonksiyon çağrısı | `f(5)` |
| Beta indirgeme | Parametre yerleştirme | `x` yerine `5` |
| Serbest değişken | Closure tarafından yakalanan değer | Dış kapsamdaki değişken |
| İç içe fonksiyon | Currying | `f(a)(b)` |

JavaScript ile iki sayıyı toplayan curried bir fonksiyon yazalım:

```javascript
const topla = x => y => x + y;

const onaEkle = topla(10);
console.log(onaEkle(7)); // 17
```

`topla(10)` çağrısı hemen bir sayı üretmez; `x` değerini hatırlayan yeni bir fonksiyon döndürür. `onaEkle`, dış kapsamındaki `10` değerini koruduğu için bir **closure** örneğidir. Lambda calculus açısından ifade şöyledir:

$$
\lambda x.\lambda y.x+y
$$

Birden fazla parametre alıyor gibi görünen fonksiyonların tek parametreli fonksiyon zincirine dönüştürülmesine **currying** denir.

## Sayılar bile fonksiyon olabilir

Saf lambda calculus içinde sayı sabitleri yoktur. Buna rağmen sayılar, fonksiyonların kaç kez uygulanacağını belirten yapılarla temsil edilebilir. Bunlara **Church sayıları** adı verilir:

$$
0 = \lambda f.\lambda x.x
$$

$$
1 = \lambda f.\lambda x.f(x)
$$

$$
2 = \lambda f.\lambda x.f(f(x))
$$

İki sayısı, `f` fonksiyonunu başlangıç değerine iki defa uygular. Python’da bu fikri çalıştırabiliriz:

```python
church_iki = lambda f: lambda x: f(f(x))
artir = lambda n: n + 1

sonuc = church_iki(artir)(0)
print(sonuc)  # 2
```

Bu kod günlük kullanım için pratik değildir; ancak veri ile davranış arasındaki sınırın düşündüğümüz kadar keskin olmadığını gösterir. Yeterince güçlü fonksiyonlarla sayıları, mantıksal değerleri ve veri yapılarını modellemek mümkündür.

## Saf fonksiyonların önemi

Lambda calculus, durum değiştirmek yerine ifadeleri dönüştürür. Bu yaklaşım modern fonksiyonel programlamadaki **saf fonksiyon** kavramını besler.

| Saf fonksiyon | Yan etkili fonksiyon |
|---|---|
| Aynı girdiye aynı sonucu verir | Sonuç dış duruma bağlı olabilir |
| Dış veriyi değiştirmez | Dosya, ekran veya global durum değişebilir |
| Test edilmesi kolaydır | Ek kurulum gerekebilir |
| Paralelleştirmeye uygundur | Yarış koşulları oluşabilir |

Örneğin `kare(x) = x²` saf bir fonksiyondur. Buna karşılık global bir sayacı artıran fonksiyon, yalnızca çıktı üretmez; sistemin durumunu da değiştirir.

Lambda calculus bize programlamanın özünde komut listelerinden ibaret olmadığını anlatır. Bir program, ifadelerin başka ifadelere dönüştürülmesi olarak da görülebilir. Bugün `map`, `filter`, anonim fonksiyonlar, higher-order functions ve closure kullanıyorsak Church’ün soyut matematik dünyası hâlâ klavyemizin hemen altındadır.
