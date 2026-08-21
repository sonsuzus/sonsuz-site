---
layout: post
title: "Manacher Algoritması ile Doğrusal Zamanda En Uzun Palindrom"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - string
  - palindrom
---

Bir metindeki en uzun palindromik alt diziyi bulmak, ilk bakışta her karakteri merkez kabul edip iki yana açılma fikriyle kolay görünür. Ancak uzun metinlerde bu yaklaşım pahalılaşır. Manacher algoritması, daha önce hesaplanan palindromların simetrisini akıllıca yeniden kullanarak problemi $O(n)$ zamanda çözer. Adı biraz sihirbazlık çağrıştırsa da arkasındaki fikir oldukça sistematiktir.
``

Palindrom, tersten ve düzden aynı okunan karakter dizisidir: `aba`, `kayak` ve `abccba` gibi. Burada önemli ayrım **alt dizi** ile **alt dizi dizisi (subsequence)** arasındadır: Manacher, karakterlerin metinde bitişik olduğu en uzun palindromik **substring** problemini çözer. Örneğin `abacdfgdcaba` içinde `aba` geçerli bir palindromik alt dizidir.

Naif merkezden genişletme yönteminde her konumdan sola ve sağa ilerleriz. Tek uzunluklu palindromlar için karakterin kendisi, çift uzunluklular için iki karakterin arası merkezdir. Fakat `aaaaaa...` gibi bir metinde her merkez neredeyse tüm metni tekrar tarar; toplam maliyet $O(n^2)$ olur.

| Yaklaşım | Temel fikir | Zaman karmaşıklığı | Ek bellek |
|---|---|---:|---:|
| Brute force | Tüm alt dizileri palindrom mu diye kontrol eder | $O(n^3)$ | $O(1)$ |
| Merkezden genişletme | Her olası merkezden iki yana gider | $O(n^2)$ | $O(1)$ |
| Manacher | Simetrik sonuçları yeniden kullanır | $O(n)$ | $O(n)$ |

Algoritmanın ilk numarası, tek ve çift uzunluktaki palindromları aynı biçime sokmaktır. Bunun için metnin karakterleri arasına ayraç yerleştirilir. `abba` metni `^#a#b#b#a#$` biçimine dönüştürülebilir. Baştaki `^` ve sondaki `$`, sınır kontrollerini sadeleştiren bekçi karakterleridir. `#` sayesinde artık her palindromun merkezi bir karakter konumudur.

Dönüştürülmüş metinde `p[i]`, `i` merkezindeki palindromun yarıçapını tutar. Algoritma ayrıca şu iki bilgiyi taşır: Şimdiye kadar bulunan en sağa uzanan palindromun merkezi $C$ ve sağ sınırı $R$. Bir indeks $i < R$ ise onun aynadaki karşılığı şöyledir:

$$mirror = 2C - i$$

Ayna konumunda daha önce hesaplanan yarıçap, yeni merkez için bedava bir başlangıç tahmini verir:

$$p[i] = \min(R-i,\ p[mirror])$$

Ardından yalnızca bu bilginin dışına taşabilecek karakterler karşılaştırılır. Başarı tam burada gelir: Sağ sınır $R$ her karşılaştırmada sürekli geri dönmez; genel olarak yalnızca metin boyunca ileri gider. Bu nedenle tüm genişletmelerin toplam maliyeti doğrusal kalır.

Aşağıdaki Python uygulaması, en uzun palindromik alt diziyi döndürür:

```python
def longest_palindrome(text: str) -> str:
    if not text:
        return ""

    transformed = "^#" + "#".join(text) + "#$"
    p = [0] * len(transformed)
    center = right = 0

    for i in range(1, len(transformed) - 1):
        mirror = 2 * center - i

        if i < right:
            p[i] = min(right - i, p[mirror])

        while transformed[i + p[i] + 1] == transformed[i - p[i] - 1]:
            p[i] += 1

        if i + p[i] > right:
            center, right = i, i + p[i]

    best_center = max(range(len(p)), key=lambda i: p[i])
    start = (best_center - p[best_center]) // 2
    return text[start:start + p[best_center]]

print(longest_palindrome("babad"))  # "bab" veya "aba"
```

Kodda `while` döngüsü korkutucu görünebilir; ancak her merkezde sıfırdan başlamaz. `right` sınırının içindeyken ayna yarıçapından yararlanırız. Sadece mevcut en sağ palindromun ötesine çıkma ihtimali olan karakterler yeni karşılaştırma üretir. Bu, $O(n)$ garantisinin pratik karşılığıdır.

Son olarak dönüşümden orijinal metne geri geçişte indeks hesabı önemlidir. Ayraçlar nedeniyle dönüştürülmüş dizideki yarıçap, orijinal dizideki palindrom uzunluğuna eşittir; başlangıç indeksi ise $\lfloor(center - radius)/2\rfloor$ ile bulunur. Manacher, özellikle DNA dizileri, metin analizi ve büyük günlük kayıtları gibi uzun string verilerinde klasik yöntemlere karşı güçlü bir araçtır.
