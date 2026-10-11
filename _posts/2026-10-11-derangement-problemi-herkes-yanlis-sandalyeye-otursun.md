---
layout: post
title: "Derangement Problemi: Herkes Yanlış Sandalyeye Otursun!"
math: true
categories: 
  - Bilgi
tags: 
  - derangement
  - permütasyon
  - kombinatorik
  - python
  - algoritma
  - matematik
toc: true
image: /img/derangement-problemi-herkes-70.png
---

![derangement-problemi-herkes-70](/img/derangement-problemi-herkes-70.svg)


Bir davette herkes şapkasını vestiyere bırakıyor ve çıkışta şapkalar rastgele dağıtılıyor. Acaba hiç kimsenin kendi şapkasını almadığı kaç farklı dağıtım vardır? Kombinatorikte **derangement**, Türkçede düzensizleştirme olarak bilinen problem tam olarak bunu sorar. İlk bakışta yalnızca permütasyon üretip kontrol etmek yeterli görünse de teorik yaklaşım çok daha hızlı ve öğreticidir.

``

## Problemin matematiksel tanımı

$n$ farklı elemanın bir permütasyonunu düşünelim. Bir eleman başlangıçtaki konumunda kalıyorsa buna **sabit nokta** denir. Derangement, sabit noktası bulunmayan permütasyondur.

Derangement sayısı genellikle $!n$, $D_n$ veya $d(n)$ ile gösterilir:

$$
D_n = \left\vert \{\pi \in S_n : \pi(i) \neq i \text{, her } i \text{ için}\}\right\vert 
$$

Küçük değerler problemi somutlaştırır:

| $n$ | Toplam permütasyon $n!$ | Derangement $D_n$ | Örnek |
|---:|---:|---:|---|
| 0 | 1 | 1 | Boş düzenleme |
| 1 | 1 | 0 | İmkânsız |
| 2 | 2 | 1 | `[2, 1]` |
| 3 | 6 | 2 | `[2, 3, 1]`, `[3, 1, 2]` |
| 4 | 24 | 9 | Dokuz farklı düzenleme |

$D_0=1$ tanımı ilk anda garip gelebilir. Ancak boş kümeyi düzenlemenin tek bir yolu vardır ve ortada kendi yerinde kalan eleman bulunmaz. Bu kabul, formüllerin düzgün çalışmasını sağlar.

## Dahil etme–hariç tutma ilkesi

Toplam $n!$ permütasyon vardır. $A_i$, $i$ numaralı elemanın kendi yerinde kaldığı permütasyonlar kümesi olsun. İstenen sonuç, hiçbir $A_i$ kümesine girmeyen permütasyonların sayısıdır.

Bir elemanı sabitlersek kalanlar $(n-1)!$ şekilde, iki elemanı sabitlersek $(n-2)!$ şekilde dizilir. Dahil etme–hariç tutma ilkesi uygulandığında:

$$
D_n=n!-\binom{n}{1}(n-1)!+\binom{n}{2}(n-2)!-\cdots+(-1)^n
$$

$\binom{n}{k}(n-k)!=\frac{n!}{k!}$ olduğundan daha kısa formül şöyledir:

$$
D_n=n!\sum_{k=0}^{n}\frac{(-1)^k}{k!}
$$

Bu toplam, $e^{-1}$ sayısının Taylor açılımını andırır. Dolayısıyla:

$$
D_n \approx \frac{n!}{e}
$$

Hatta tam sayı sonucu en yakın tam sayıya yuvarlayarak bulabiliriz:

$$
D_n=\left\lfloor\frac{n!}{e}+\frac{1}{2}\right\rfloor
$$

Bunun ilginç sonucu şudur: $n$ büyüdükçe rastgele bir permütasyonda hiç sabit nokta bulunmama olasılığı yaklaşık $1/e$, yani yüzde $36{,}79$ olur.

## Daha kullanışlı bağıntı

Derangement sayıları aşağıdaki yinelemeli bağıntıyla da hesaplanabilir:

$$
D_n=(n-1)(D_{n-1}+D_{n-2})
$$

İlk eleman başka bir konuma gönderilir. O konumdaki eleman ya ilk elemanın yerine gelir ya da üçüncü bir konuma gider. Bu iki durum sırasıyla daha küçük derangement problemlerine dönüşür.

| Yaklaşım | Zaman karmaşıklığı | Bellek | Özellik |
|---|---:|---:|---|
| Tüm permütasyonları denemek | $O(n!\cdot n)$ | Yüksek | Yalnızca küçük $n$ için |
| Dahil etme–hariç tutma | $O(n)$ | $O(1)$ | Faktöriyel takibi gerekir |
| Yinelemeli dinamik çözüm | $O(n)$ | $O(1)$ | Tam sayı hesabı için pratik |

## Python ile hesaplama

Aşağıdaki fonksiyon bağıntıyı kullanır. Yalnızca son iki değeri sakladığı için ek diziye ihtiyaç duymaz:

```python
def derangement(n):
    if n < 0:
        raise ValueError("n negatif olamaz")
    if n == 0:
        return 1
    if n == 1:
        return 0

    onceki_iki, onceki = 1, 0  # D0 ve D1

    for i in range(2, n + 1):
        simdiki = (i - 1) * (onceki + onceki_iki)
        onceki_iki, onceki = onceki, simdiki

    return onceki

for n in range(1, 9):
    print(n, derangement(n))
```

Program sırasıyla `0, 1, 2, 9, 44, 265, 1854, 14833` değerlerini üretir. Python tam sayıları otomatik büyüttüğü için büyük sonuçlarda taşma yaşanmaz.

Derangement; görev atama, gizli hediye çekilişi, test sorularını karıştırma ve kimsenin önceki eşleşmesini almaması gereken planlama problemlerinde kullanılır. Kısacası matematiğin düzen kurmak için bazen herkesi özellikle yanlış yere koyduğu eğlenceli örneklerden biridir.
