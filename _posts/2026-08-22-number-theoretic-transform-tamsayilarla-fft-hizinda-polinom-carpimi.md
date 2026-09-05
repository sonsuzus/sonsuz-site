---
layout: post
title: "Number Theoretic Transform: Tamsayılarla FFT Hızında Polinom Çarpımı"
math: true
categories: 
  - Bilgi
tags: 
  - number theoretic transform
  - ntt
  - algoritmalar
  - modüler aritmetik
  - fft
toc: true
image: /img/number-theoretic-transform-70.png
---

Büyük tamsayıları, polinomları veya konvolüsyonları hızlı çarpmak istediğinizde klasik FFT ilk akla gelen araçtır. Ancak FFT genellikle kayan noktalı sayılarla çalışır; yuvarlama hataları, özellikle katsayılar büyüdüğünde can sıkıcı sonuçlar doğurabilir. Number Theoretic Transform (NTT), FFT’nin aynı böl-ve-yönet fikrini sonlu bir cisimde, yani tamamen tamsayı ve modüler aritmetikle uygular. Sonuç: deterministik, hassas ve yarışma programlamacıları için oldukça keyifli bir algoritma.
``

## FFT’nin modüler kuzeni

FFT, karmaşık sayılardaki birim köklerini kullanarak bir dizinin frekans gösterimini hesaplar. NTT ise karmaşık sayılar yerine asal modül altında çalışan **ilkel kökleri** kullanır. Amaç yine aynıdır: iki polinomun katsayılarını doğrudan $O(n^2)$ yerine dönüşüm, noktasal çarpım ve ters dönüşüm yoluyla $O(n\log n)$ sürede çarpmak.

Örneğin

$$A(x)=\sum_{i=0}^{n-1}a_ix^i, \qquad B(x)=\sum_{j=0}^{m-1}b_jx^j$$

için istenen sonuç $C(x)=A(x)B(x)$ olur. Katsayı düzeyinde bu işlem konvolüsyondur:

$$c_k=\sum_{i=0}^{k}a_i b_{k-i}$$

NTT, bu toplamları tek tek hesaplamak yerine polinomları uygun noktalarda değerlendirir. Değerlendirme uzayında çarpım son derece basittir: $\widehat{C}_i=\widehat{A}_i\widehat{B}_i$.

| Özellik | FFT | NTT |
|---|---|---|
| Sayı alanı | Karmaşık sayılar | Modüler tamsayılar |
| Hassasiyet | Yuvarlama hatası olabilir | Tam ve deterministik |
| Modül gereksinimi | Yok | Uygun asal gerekir |
| Yaygın kullanım | Sinyal işleme | Polinom, kombinatorik, büyük tamsayı |

![number-theoretic-transform-70](/img/number-theoretic-transform-70.svg)


## Neden her asal modül çalışmaz?

Uzunluğu $N=2^k$ olan bir NTT için modül $p$ altında $N$ mertebeli bir köke ihtiyaç vardır. Bunun için genellikle

$$p \equiv 1 \pmod N$$

koşulu aranır. Popüler seçimlerden biri $p=998244353$ sayısıdır. Çünkü

$$998244353=119\cdot 2^{23}+1$$

şeklindedir. Böylece $2^{23}$ uzunluğa kadar ikinin kuvveti boyutlarında dönüşüm yapılabilir. Bu modül için sık kullanılan ilkel kök $g=3$ tür.

Bir aşamada kullanılan kök, $w=g^{(p-1)/len}$ formülüyle üretilir. Buradaki `len`, o aşamadaki kelebek bloğunun uzunluğudur. Ters dönüşümde kökün modüler tersi kullanılır; en sonunda da tüm değerler $N^{-1}\bmod p$ ile çarpılır.

## Kelebek operasyonu: algoritmanın kalbi

NTT’nin temel adımı FFT’dekiyle aynıdır. İki değer $u$ ve $v$ için:

$$x=u+v\pmod p, \qquad y=u-v\pmod p$$

hesaplanır; fakat $v$ değeri önce uygun kökün kuvvetiyle çarpılır. Bu “kelebek” düzeni, diziyi çift ve tek indisli parçalara ayırarak tekrar tekrar uygular. Uygulamada giriş dizisi önce bit-reversal sırasına alınır.

Aşağıdaki C++ parçası, dönüşümün orta seviye özünü gösterir. `invert` bayrağı ters NTT’yi seçer:

```cpp
const int MOD = 998244353, G = 3;

long long modPow(long long a, long long e) {
    long long r = 1;
    while (e) {
        if (e & 1) r = r * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return r;
}

void ntt(vector<int>& a, bool invert) {
    int n = (int)a.size();
    for (int len = 2; len <= n; len <<= 1) {
        int wlen = modPow(G, (MOD - 1) / len);
        if (invert) wlen = modPow(wlen, MOD - 2);
        for (int i = 0; i < n; i += len) {
            long long w = 1;
            for (int j = 0; j < len / 2; ++j) {
                int u = a[i + j];
                int v = w * a[i + j + len / 2] % MOD;
                a[i + j] = (u + v) % MOD;
                a[i + j + len / 2] = (u - v + MOD) % MOD;
                w = w * wlen % MOD;
            }
        }
    }
    if (invert) {
        long long invN = modPow(n, MOD - 2);
        for (int& x : a) x = x * invN % MOD;
    }
}
```

Gerçek bir polinom çarpımında iki diziyi sonuç uzunluğunu kapsayan en küçük $2$ kuvvetine kadar doldurur, ikisine de NTT uygular, eleman eleman çarpar ve ters NTT çalıştırırsınız. Negatif ara sonuçlar için `+ MOD` eklenmesi özellikle önemlidir.

NTT’nin küçük bir sınırı vardır: sonuçlar seçilen modüle göre alınır. Katsayılar modülü aşacak kadar büyükse birden fazla NTT asalı kullanıp Çin Kalan Teoremi (CRT) ile sonuçları birleştirebilirsiniz. Böylece tamsayı kesinliğinden vazgeçmeden FFT ölçeğinde hız elde edersiniz.
