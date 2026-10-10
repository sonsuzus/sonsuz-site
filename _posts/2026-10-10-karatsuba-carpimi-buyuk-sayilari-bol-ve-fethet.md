---
layout: post
title: "Karatsuba Çarpımı: Büyük Sayıları Böl ve Fethet"
math: true
categories: 
  - Bilgi
tags: 
  - karatsuba
  - algoritma
  - böl-ve-fethet
  - python
  - matematik
  - büyük-sayılar
toc: true
image: /img/karatsuba-carpimi-buyuk-26.png
---

Bilgisayarınız iki küçük sayıyı göz açıp kapayıncaya kadar çarpabilir. Ancak binlerce veya milyonlarca basamak içeren sayılar söz konusu olduğunda, ilkokulda öğrendiğimiz klasik çarpma yöntemi pahalı hâle gelir. 1960 yılında Anatoly Karatsuba tarafından geliştirilen algoritma, zekice bir cebirsel dönüşüm kullanarak gereken küçük çarpma sayısını azaltır. Böylece büyük tam sayılarla çalışan kriptografi, matematik yazılımları ve bilimsel hesaplama sistemleri önemli ölçüde hızlanır.

![karatsuba-carpimi-buyuk-26](/img/karatsuba-carpimi-buyuk-26.svg)

``

## Klasik çarpmanın maliyeti

Her biri $n$ basamaklı iki sayıyı klasik yöntemle çarptığımızı düşünelim. Birinci sayının her basamağı, ikinci sayının bütün basamaklarıyla çarpılır. Yaklaşık olarak $n \times n = n^2$ tek basamaklı çarpma yapılır. Bu nedenle klasik yöntemin zaman karmaşıklığı $O(n^2)$ olur.

Karatsuba ise sayıları iki parçaya ayırır. Tabanı $B$ olan ve yaklaşık $2m$ basamak taşıyan iki sayı şöyle yazılabilir:

$$x = aB^m + b$$

$$y = cB^m + d$$

Normal açılım yapıldığında:

$$xy = acB^{2m} + (ad + bc)B^m + bd$$

Bu ifade doğrudan uygulanırsa $ac$, $ad$, $bc$ ve $bd$ olmak üzere dört çarpma gerekir. Karatsuba'nın numarası tam burada ortaya çıkar: ortadaki terim ayrı ayrı hesaplanmak zorunda değildir.

$$ad + bc = (a+b)(c+d) - ac - bd$$

Böylece yalnızca şu üç çarpım hesaplanır:

- $z_2 = ac$
- $z_0 = bd$
- $z_1 = (a+b)(c+d) - z_2 - z_0$

Sonuç ise $z_2B^{2m} + z_1B^m + z_0$ biçiminde birleştirilir. Dört çarpma yerine üç çarpma yapmak küçük sayılarda önemsiz görünebilir; fakat işlem her seviyede özyinelemeli tekrarlandığında fark kartopu gibi büyür.

| Özellik | Klasik yöntem | Karatsuba |
|---|---:|---:|
| Alt problem sayısı | 4 | 3 |
| Alt problem boyutu | $n/2$ | $n/2$ |
| Zaman karmaşıklığı | $O(n^2)$ | $O(n^{\log_2 3})$ |
| Yaklaşık üs | 2 | 1,585 |
| Küçük sayılardaki ek yük | Düşük | Daha yüksek |

Karatsuba'nın bağıntısı $T(n)=3T(n/2)+O(n)$ şeklindedir. Buradan karmaşıklık yaklaşık $O(n^{1.585})$ çıkar. Sayılar büyüdükçe bu üs farkı ciddi bir avantaj sağlar.

## Python ile uygulama

Aşağıdaki fonksiyon sayıları onluk tabanda böler. Sayılar yeterince küçük olduğunda özyinelemeyi durdurup Python'ın normal çarpımını kullanır:

```python
def karatsuba(x, y):
    # Küçük değerlerde ek özyineleme maliyetinden kaçın.
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2
    taban = 10 ** m

    a, b = divmod(x, taban)
    c, d = divmod(y, taban)

    z2 = karatsuba(a, c)
    z0 = karatsuba(b, d)
    z1 = karatsuba(a + b, c + d) - z2 - z0

    return z2 * (taban ** 2) + z1 * taban + z0

print(karatsuba(12345678, 87654321))
```

`divmod`, bir sayının yüksek ve düşük basamaklarını tek adımda ayırır. Üç özyinelemeli çağrı gerekli ara çarpımları üretir; son satır da basamak kaydırmalarını onluk tabanın kuvvetleriyle gerçekleştirir.

## Her durumda daha mı hızlı?

Hayır. Özyinelemeli çağrılar, sayıları parçalama ve ara sonuçları toplama işlemleri ek maliyet oluşturur. Bu yüzden pratik kütüphaneler hibrit davranır: küçük sayılarda klasik çarpma, belirli bir basamak eşiğinden sonra Karatsuba kullanılır.

| Durum | Mantıklı tercih |
|---|---|
| Birkaç basamaklı sayılar | Klasik çarpma |
| Yüzlerce veya binlerce basamak | Karatsuba |
| Aşırı büyük sayılar | Toom-Cook veya FFT tabanlı yöntemler |

Karatsuba'nın asıl güzelliği, daha güçlü donanım istemeden cebir sayesinde işi azaltmasıdır. Böl ve fethet yaklaşımının yalnızca problemi küçültmek değil, gereksiz hesaplamaları ortadan kaldırmak anlamına da geldiğini gösteren klasik ve hâlâ etkileyici bir algoritmadır.
