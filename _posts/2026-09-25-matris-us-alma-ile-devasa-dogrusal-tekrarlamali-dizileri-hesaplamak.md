---
layout: post
title: "Matris Üs Alma ile Devasa Doğrusal Tekrarlamalı Dizileri Hesaplamak"
math: true
categories: 
  - Bilgi
tags: 
  - matris
  - fibonacci
  - algoritma
  - dinamik-programlama
  - hızlı-üs-alma
  - c++
toc: true
image: /img/matris-us-alma-18.png
---

Fibonacci dizisinin milyonuncu, hatta milyarıncı terimini hesaplamak istediğimizi düşünelim. Diziyi baştan sona üretmek kolaydır; fakat bilgisayara milyarlarca kez toplama yaptırmak, çay demlenirken başlayıp yeni bir çay plantasyonu kurulunca biten bir plan olabilir. Neyse ki doğrusal tekrarlamaları matris biçiminde ifade ederek problemi $O(n)$ zamandan $O(\log n)$ zamana indirebiliriz.
``
Fibonacci dizisi şu bağıntıyla tanımlanır:

$$F_n = F_{n-1} + F_{n-2}, \qquad F_0=0,\ F_1=1$$

Klasik döngü yaklaşımı, önceki iki değeri saklayıp $F_2$'den $F_n$'e kadar ilerler. Bellek tüketimi $O(1)$ olsa da çalışma süresi $O(n)$ olur. Buradaki kritik gözlem, bir sonraki durumun mevcut durumun **doğrusal dönüşümü** olmasıdır.

Durumumuzu sütun vektörü olarak yazalım:

$$
\begin{bmatrix}
F_n \\
F_{n-1}
\end{bmatrix}
=
\begin{bmatrix}
1 & 1 \\
1 & 0
\end{bmatrix}
\begin{bmatrix}
F_{n-1} \\
F_{n-2}
\end{bmatrix}
$$

Buradaki dönüşüm matrisi $A$ olsun. Aynı dönüşümü tekrar tekrar uyguladığımızda matris kuvvetleri ortaya çıkar:

$$
\begin{bmatrix}
F_n \\
F_{n-1}
\end{bmatrix}
=A^{n-1}
\begin{bmatrix}
F_1 \\
F_0
\end{bmatrix}
$$

Yani artık hedefimiz diziyi adım adım yürütmek değil, $A^{n-1}$ matrisini hızlı hesaplamaktır.

| Yöntem | Zaman karmaşıklığı | Bellek | Temel fikir |
|---|---:|---:|---|
| Özyinelemeli Fibonacci | $O(2^n)$ | $O(n)$ | Aynı alt problemleri tekrar hesaplar |
| Döngü / dinamik programlama | $O(n)$ | $O(1)$ | Terimleri sırayla üretir |
| Matris üs alma | $O(\log n)$ | $O(1)$ | Dönüşüm matrisini karesini alarak yükseltir |

## Hızlı üs alma neden logaritmiktir?

Bir sayının kuvvetini hesaplarken kullanılan ikili üs alma tekniği matrislerde de geçerlidir. Üs çiftse

$$A^n=(A^{n/2})^2$$

olur. Üs tekse bir adet $A$ dışarı alınır:

$$A^n=A\cdot A^{n-1}$$

Her adımda üs yaklaşık yarıya indiği için yalnızca $\log_2 n$ tur gerekir. Matris boyutu Fibonacci için sabit, yani $2\times2$ olduğundan her çarpım sabit maliyetlidir.

Aşağıdaki C++ kodu sonucu bir modüler sayı altında hesaplar. Mod kullanmak önemlidir; çünkü Fibonacci sayıları son derece hızlı büyür ve standart tam sayı türlerine sığmaz.

{% raw %}
```cpp
#include <iostream>
using namespace std;

const long long MOD = 1'000'000'007;

struct Matrix {
    long long a[2][2]{};
};

Matrix multiply(const Matrix& x, const Matrix& y) {
    Matrix result;
    for (int i = 0; i < 2; ++i)
        for (int j = 0; j < 2; ++j)
            for (int k = 0; k < 2; ++k)
                result.a[i][j] =
                    (result.a[i][j] + x.a[i][k] * y.a[k][j]) % MOD;
    return result;
}

Matrix power(Matrix base, long long exponent) {
    Matrix result;
    result.a[0][0] = result.a[1][1] = 1; // Birim matris

    while (exponent > 0) {
        if (exponent & 1)
            result = multiply(result, base);
        base = multiply(base, base);
        exponent >>= 1;
    }
    return result;
}

long long fibonacci(long long n) {
    if (n == 0) return 0;
    Matrix transition{{{1, 1}, {1, 0}}};
    return power(transition, n - 1).a[0][0];
}

int main() {
    cout << fibonacci(1'000'000'000) << '\n';
}
```
{% endraw %}

`multiply` iki dönüşümü birleştirir; `power` ise üssün ikili gösterimini kullanır. Başlangıçta sonuç birim matristir, çünkü $A^0=I$ olmalıdır. Üssün ilgili biti bir olduğunda mevcut taban sonuca katılır.

## Yalnızca Fibonacci değil

Bu yöntem, sabit katsayılı her doğrusal tekrarlamaya uygulanabilir. Örneğin

$$X_n=2X_{n-1}+3X_{n-2}$$

için dönüşüm matrisi

$$
\begin{bmatrix}
2 & 3 \\
1 & 0
\end{bmatrix}
$$

olur. Daha fazla geçmiş terime bağlı bağıntılarda matris boyutu büyür; mantık değişmez. Böylece matris, dizinin hafızasını taşıyan küçük bir zaman makinesine dönüşür: milyarlarca adımı tek tek yürümek yerine onları logaritmik sayıda sıçramayla geçer.

![matris-us-alma-18](/img/matris-us-alma-18.svg)

