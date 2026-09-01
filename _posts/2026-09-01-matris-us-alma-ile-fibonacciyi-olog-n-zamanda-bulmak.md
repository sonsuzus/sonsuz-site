---
layout: post
title: "Matris Üs Alma ile Fibonacci’yi O(log n) Zamanda Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - matris üs alma
  - fibonacci
  - rekabetçi programlama
toc: true
---

Fibonacci dizisinin milyarıncı elemanı istendiğinde klasik döngünüz süre sınırına doğru hüzünlü bir yolculuğa çıkar. Neyse ki doğrusal tekrarlayan diziler, matrisler aracılığıyla tek bir dönüşüm şeklinde modellenebilir. Bu dönüşümün kuvvetini hızlı üs alma yöntemiyle hesapladığımızda $O(n)$ adımlık işi $O(\log n)$ zamanda tamamlarız. Başka bir deyişle milyarlarca adım, yaklaşık otuz matris çarpımına dönüşür.
``

## Diziden matrise giden yol

Fibonacci dizisi şu bağıntıyla tanımlanır:

$$F_n = F_{n-1} + F_{n-2}$$

Buradaki önemli ayrıntı, yeni değeri hesaplamak için yalnızca önceki iki değere ihtiyaç duymamızdır. Bu iki değeri bir **durum vektörü** içinde tutabiliriz:

$$S_n = [F_n, F_{n-1}]^T$$

Bir sonraki duruma geçiş ise sabit bir matrisle gerçekleştirilir:

$$S_n = \begin{pmatrix}1 & 1 \\ 1 & 0\end{pmatrix} S_{n-1}$$

Geçiş matrisine $M$ dersek aynı işlemi tekrar tekrar uygulamak şu sonucu verir:

$$S_n = M^{n-1} S_1$$

Dolayısıyla problem artık diziyi sırayla üretmek değil, $M^{n-1}$ matrisini hızlı biçimde hesaplamaktır.

| Yaklaşım | Zaman karmaşıklığı | Ek bellek | Büyük $n$ için durum |
|---|---:|---:|---|
| Özyinelemeli Fibonacci | $O(2^n)$ | $O(n)$ | Tam bir felaket |
| Döngü / dinamik programlama | $O(n)$ | $O(1)$ | Orta büyüklükte iyi |
| Matris üs alma | $O(\log n)$ | $O(1)$ | Yarışmaların gözdesi |

## Hızlı üs alma mantığı

Bir sayıda kullandığımız ikili üs alma fikri matrislerde de geçerlidir. Üs çiftse

$$M^n = (M^{n/2})^2$$

olur. Üs tekse fazladan bir $M$ çarparız. Her adımda üs yarıya indiği için yalnızca $O(\log n)$ tur gerekir. Fibonacci matrisimiz $2 \times 2$ boyutunda olduğundan her matris çarpımı sabit maliyetlidir.

Aşağıdaki C++ kodu işlemleri `MOD` altında yapar. Böylece değerlerin taşması önlenir ve programlama yarışmalarında sık görülen “sonucu modüler yazdırın” koşulu karşılanır:

```cpp
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007;

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
    Matrix transition;
    transition.a[0][0] = transition.a[0][1] = 1;
    transition.a[1][0] = 1;

    return power(transition, n - 1).a[0][0];
}
```

`power` fonksiyonu birim matrisle başlar; çünkü birim matris, çarpmanın etkisiz elemanıdır. Üssün ilgili ikili basamağı `1` olduğunda sonuç güncellenir. Ardından taban karesi alınır ve üs sağa kaydırılarak ikiye bölünür.

## Yalnızca Fibonacci için mi?

Hayır. $k$ önceki terime bağlı her doğrusal dizi, uygun bir $k \times k$ geçiş matrisiyle modellenebilir. Örneğin

$$A_n = 2A_{n-1} + 3A_{n-2}$$

için geçiş matrisi $\begin{pmatrix}2 & 3 \\ 1 & 0\end{pmatrix}$ olur. Matris boyutu büyüdüğünde bir çarpımın maliyeti $O(k^3)$, toplam maliyet ise $O(k^3 \log n)$ olur.

En yaygın hatalar $n=0$ durumunu unutmak, başlangıç vektörünü yanlış seçmek ve çarpma sırasında taşmaya izin vermektir. Bu ayrıntıları kontrol ettiğinizde matris üs alma, devasa indeksleri küçük bir hesaplama problemine çeviren güçlü bir yarışma silahıdır.
