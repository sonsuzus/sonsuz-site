---
layout: post
title: "EBOB ve Öklid Algoritması: Özyinelemenin Sayılarla Dansı"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - algoritmalar
  - python
---

İki sayının ortak bölenlerini tek tek aramak, küçük sayılarda masum görünen ama sayılar büyüdükçe sabrımızı sınayan bir iştir. En Büyük Ortak Bölen (EBOB), iki ya da daha fazla tam sayıyı kalansız bölen en büyük pozitif sayıdır. Öklid algoritması ise bu değeri bulmak için binlerce yıldır kullanılan, şaşırtıcı derecede zarif ve verimli bir yöntemdir. Dahası, algoritmanın mantığı özyinelemeli fonksiyonlar için mükemmel bir uygulama alanı sunar.
``

Matematiksel olarak iki tam sayının EBOB'u $\gcd(a,b)$ biçiminde gösterilir. Örneğin $18$ ve $48$ sayılarının ortak bölenleri $1, 2, 3, 6$ olduğundan sonuç $\gcd(18,48)=6$ olur. Ancak ortak bölenleri listelemek yerine Öklid'in temel gözleminden yararlanırız:

$$\gcd(a,b) = \gcd(b, a \bmod b)$$

Buradaki $a \bmod b$, $a$ sayısının $b$'ye bölümünden kalan değerdir. Bunun nedeni basittir: $a$ ve $b$'yi bölen her sayı, $a - q \cdot b$ ifadesini de böler. Bu ifade tam olarak bölme işleminden kalan sayıdır. Yani büyük sayıyı küçük sayıya bölüp kalana geçmek, ortak bölen kümesini değiştirmez; yalnızca problemi küçültür.

Örneğin $\gcd(252,105)$ hesabı şu basamaklarla ilerler:

$$
\begin{aligned}
252 \bmod 105 &= 42 \\
105 \bmod 42 &= 21 \\
42 \bmod 21 &= 0
\end{aligned}
$$

Kalanın sıfır olduğu anda son sıfır olmayan bölen sonuçtur: $\gcd(252,105)=21$. Bu süreçte sayılar hızla küçülür; algoritmanın gücü de burada saklıdır.

| Yaklaşım | Temel fikir | Büyük sayılardaki durum |
|---|---|---|
| Bölenleri tarama | Küçük sayıdan başlayarak ortak bölen aramak | Fazla deneme gerektirir |
| Asal çarpanlara ayırma | Ortak asal çarpanları seçmek | Çarpanlara ayırma maliyetli olabilir |
| Öklid algoritması | Kalanı kullanarak problemi küçültmek | Çok hızlı ve pratiktir |

Özyineleme, bir fonksiyonun daha küçük bir problem için kendisini çağırmasıdır. Öklid algoritmasında her çağrıdaki ikinci sayı, bir önceki adımdaki kalandır. Kalan sıfır olduğunda artık daha fazla küçültülecek problem kalmaz; bu da **temel durum**dur. Fonksiyon tasarımında temel durum unutulursa çağrılar sonsuza kadar devam eder ve program hata verir.

Python ile özyinelemeli çözüm oldukça okunaklıdır:

```python
def ebob(a, b):
    """a ve b sayılarının EBOB'unu Öklid algoritmasıyla döndürür."""
    a, b = abs(a), abs(b)

    if b == 0:
        return a

    return ebob(b, a % b)

print(ebob(252, 105))  # 21
```

Kodun ilk satırı negatif girdileri güvenli biçimde pozitif hale getirir; çünkü EBOB genellikle negatif olmayan bir değer olarak tanımlanır. Ardından `b == 0` kontrolü özyinelemenin durma koşuludur. Aksi durumda fonksiyon, `(b, a % b)` ikilisiyle kendisini çağırır. Her adımda ikinci argüman küçüldüğü için algoritma mutlaka sona ulaşır.

| Kavram | Kod karşılığı | Görevi |
|---|---|---|
| Temel durum | `if b == 0` | Özyinelemeyi bitirir |
| Küçültme adımı | `a % b` | Daha küçük alt problem üretir |
| Özyinelemeli çağrı | `ebob(b, a % b)` | Öklid eşitliğini uygular |

Algoritmanın çalışma süresi kabaca $O(\log(\min(a,b)))$ düzeyindedir. Bu, sayıların basamak sayısı arttıkça çalışma süresinin çok daha yavaş büyüdüğü anlamına gelir. Örneğin milyonlarca basamaklı sayılarda bile ortak bölen aramak için her olası böleni denemek zorunda kalmazsınız.

EBOB yalnızca bir ders kitabı konusu değildir. Kesirleri sadeleştirme, modüler aritmetik, kriptografi ve en küçük ortak katı (EKOK) hesaplama gibi alanlarda sıkça kullanılır. İki pozitif sayı için ilişki şöyledir:

$$\operatorname{ekok}(a,b)=\frac{|a \cdot b|}{\gcd(a,b)}$$

Kısacası Öklid algoritması, iyi bir algoritmanın küçük bir özeti gibidir: Doğru matematiksel gözlemi bulur, problemi her adımda küçültür ve net bir bitiş koşuluyla sonucu güvenle üretir.
