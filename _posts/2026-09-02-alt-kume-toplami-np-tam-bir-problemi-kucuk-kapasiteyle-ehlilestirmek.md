---
layout: post
title: "Alt Küme Toplamı: NP-Tam Bir Problemi Küçük Kapasiteyle Ehlileştirmek"
math: true
categories: 
  - Bilgi
tags: 
  - dinamik programlama
  - np-tam
  - algoritma optimizasyonu
toc: true
---

Elimizde pozitif tam sayılardan oluşan bir liste ve hedef toplam $T$ var. Soru basit: Bazı elemanları en fazla bir kez seçerek toplamı tam olarak $T$ yapabilir miyiz? Bu masum soru, Alt Küme Toplamı Problemi’nin karar sürümüdür ve NP-tamdır. Yine de hedef kapasite küçük olduğunda dinamik programlama sayesinde problem, pratikte oldukça uysal bir hâle gelir.
``
## NP-tam ama hangi ölçüye göre?

Sayılar $a_1,a_2,\ldots,a_n$ ve hedef $T$ olsun. Aradığımız bir $S$ indeks kümesi için:

$$
\sum_{i \in S} a_i = T
$$

Koşulu sağlayan bir seçim bulunmalıdır. Kaba kuvvet yaklaşımı, her elemanı “al” veya “alma” şeklinde değerlendirir. Böylece $2^n$ olasılık oluşur ve zaman karmaşıklığı $O(2^n)$ olur.

Buradaki kritik ayrıntı, $T$ sayısının girişte yaklaşık $\log_2 T$ bit ile temsil edilmesidir. Dinamik programlamanın $O(nT)$ süresi, $T$ değerine göre polinom görünse de giriş uzunluğuna göre üstel olabilir. Bu nedenle algoritma **sözde polinom zamanlıdır**. NP-tamlık ortadan kalkmaz; yalnızca küçük sayısal değerlerden yararlanılır.

| Yaklaşım | Zaman | Bellek | Uygun durum |
|---|---:|---:|---|
| Kaba kuvvet | $O(2^n)$ | $O(n)$ | Çok küçük $n$ |
| Klasik DP | $O(nT)$ | $O(nT)$ | Çözüm kümesini izlemek gerektiğinde |
| Tek boyutlu DP | $O(nT)$ | $O(T)$ | Yalnızca sonuç gerektiğinde |
| Bitset yöntemi | Yaklaşık $O(nT/w)$ | $O(T)$ | Küçük veya orta hedeflerde |
| Ortadan bölme | $O(2^{n/2})$ | $O(2^{n/2})$ | $T$ büyük, $n$ görece küçükken |

## Kapasiteyi durum uzayı yapmak

`dp[s]`, işlenen elemanlarla $s$ toplamına ulaşılıp ulaşılamadığını göstersin. Başlangıçta yalnızca boş kümenin toplamı olan sıfır mümkündür:

$$
dp[0]=\text{true}
$$

Her $a_i$ için geçiş şöyledir:

$$
dp_i[s] = dp_{i-1}[s] \lor dp_{i-1}[s-a_i]
$$

Belleği tek boyuta indirirken toplamları **azalan sırada** dolaşmak zorunludur. Artan sırada gidersek aynı eleman bir tur içinde tekrar kullanılabilir; problem farkında olmadan sınırsız bozuk para problemine dönüşür.

```python
def alt_kume_toplami(sayilar, hedef):
    # dp[s]: s toplamına ulaşılabiliyorsa True olur.
    dp = [False] * (hedef + 1)
    dp[0] = True

    for sayi in sayilar:
        # Geriye doğru ilerlemek, sayının yalnızca bir kez kullanılmasını sağlar.
        for toplam in range(hedef, sayi - 1, -1):
            dp[toplam] = dp[toplam] or dp[toplam - sayi]

        # Hedef bulunduysa kalan elemanları işlemeye gerek yoktur.
        if dp[hedef]:
            return True

    return False
```

Bu çözüm $O(nT)$ zamanda ve $O(T)$ bellekte çalışır. Örneğin $n=10\,000$ olsa bile $T=500$ ise yalnızca 501 Boolean durum tutulur. Ancak $T=10^{12}$ olduğunda tablo oluşturmak bile gerçekçi değildir.

## Bitset ile kelime düzeyinde paralellik

Ulaşılabilir toplamları bir tamsayının bitleriyle gösterebiliriz. Bit $s$ açıksa, $s$ toplamına ulaşılmıştır. Yeni bir $a$ sayısını eklemek, bitleri $a$ konum sola kaydırmak anlamına gelir:

$$
bits \leftarrow bits \lor (bits \ll a)
$$

```python
def bitset_alt_kume_toplami(sayilar, hedef):
    bits = 1  # Yalnızca sıfırıncı bit açık.
    maske = (1 << (hedef + 1)) - 1

    for sayi in sayilar:
        bits |= bits << sayi
        bits &= maske  # Hedeften büyük toplamları at.

    return bool(bits & (1 << hedef))
```

Python’ın büyük tamsayı işlemleri alt seviyede birçok biti birlikte işlediğinden bu sürüm çoğu zaman klasik döngüden belirgin biçimde hızlıdır.

Sonuç olarak optimizasyonun anahtarı NP-tamlığı “yenmek” değil, parametreyi doğru seçmektir. Hedef küçükse kapasite tabanlı DP, hedef büyük ama eleman sayısı küçükse ortadan bölme daha uygundur. Algoritma tasarımında bazen problemin etiketi değil, kısıtların gerçek boyutu patron koltuğunda oturur.
