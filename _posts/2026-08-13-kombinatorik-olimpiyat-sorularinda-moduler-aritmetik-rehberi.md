---
layout: post
title: "Kombinatorik Olimpiyat Sorularında Modüler Aritmetik Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - kombinatorik
  - modüler aritmetik
  - olimpiyat soruları
image: /img/kombinatorik-olimpiyat-sorularinda-44.png
toc: true
---

Kombinatorik olimpiyat sorularında ilk bakışta masum görünen $n!$, $\binom{n}{k}$ ve permütasyon ifadeleri, $n$ büyüdükçe devasa sayılara dönüşür. Neyse ki çoğu sorunun gerçekten istediği şey sayının tamamı değil, belirli bir sayıya bölümünden kalanıdır. İşte modüler aritmetik burada sahneye çıkar: Büyük sayıları yazmak yerine kalıntıları yönetir, akıllı sadeleştirmelerle imkânsız görünen hesapları birkaç satıra indirir.
``

## Temel fikir: Sayıyı değil kalanı takip et

Bir sayının $m$ ile bölümünden kalanı için $a \equiv b \pmod m$ yazılır. Bu gösterim, $a$ ve $b$ sayılarının $m$'ye bölündüğünde aynı kalanı verdiğini anlatır. Toplama ve çarpma işlemleri kalıntılar üzerinde güvenle yapılabilir:

$$
(a+b) \bmod m = ((a \bmod m)+(b \bmod m)) \bmod m
$$

$$
(ab) \bmod m = ((a \bmod m)(b \bmod m)) \bmod m
$$

Örneğin $17! \bmod 13$ hesaplanacaksa, $13$ çarpanı zaten $17!$ içinde bulunduğu için cevap anında $0$ olur. Bu, olimpiyatların sevdiği ilk kısa yoldur: Çarpımın içinde modülün çarpanı var mı?

| İfade | Doğrudan yaklaşım | Modüler yaklaşım |
|---|---|---|
| $100! \bmod 97$ | 158 basamaklı sayıyı üretmek | $97 \mid 100!$ olduğu için $0$ |
| $2^{1000} \bmod 7$ | Bin kez çarpma | Kuvvet döngüsünü kullanmak |
| $\binom{1000}{500} \bmod p$ | Dev kesir hesaplamak | Faktöriyel ve ters eleman kullanmak |

![kombinatorik-olimpiyat-sorularinda-44](/img/kombinatorik-olimpiyat-sorularinda-44.svg)


## Permütasyonlarda döngüler ve Fermat'nın küçük teoremi

Üs içeren sayma ifadelerinde kuvvetlerin periyodik davranışı önemlidir. Örneğin $2^3 \equiv 1 \pmod 7$ olduğundan:

$$
2^{1000}=2^{3\cdot333+1}\equiv (2^3)^{333}\cdot2\equiv2\pmod7.
$$

Modül $p$ asal ve $a$ sayısı $p$'ye bölünmüyorsa, Fermat'nın küçük teoremi güçlü bir araç verir:

$$
a^{p-1}\equiv1\pmod p.
$$

Daha da önemlisi, bölme işlemi modüler dünyada **ters eleman** ile yapılır. $a^{-1}$, $a\cdot a^{-1}\equiv1\pmod p$ koşulunu sağlayan sayıdır. Asal modülde bu ters eleman $a^{p-2}$ ile bulunabilir. Yani $\frac{1}{a}$ yazmak yerine $a^{p-2}$ ile çarparız.

## Kombinasyonlar: Bölme tuzağına dikkat

Kombinasyon formülü şöyledir:

$$
\binom{n}{k}=\frac{n!}{k!(n-k)!}.
$$

Fakat mod aldıktan sonra payda ile doğrudan bölmek yanlış olabilir. Örneğin $10/2 \bmod 6$ ifadesinde önce kalıntıları bölmeye çalışmak anlamsızdır; çünkü $2$'nin mod $6$'da tersi yoktur. Ters elemanın var olması için $\gcd(a,m)=1$ gerekir. Bu nedenle klasik faktöriyel-ters faktöriyel yöntemi en rahat biçimde modül asal olduğunda kullanılır.

Aşağıdaki Python kodu, asal $p$ için $\binom{n}{k}\bmod p$ hesaplar. Hızlı üs alma sayesinde tersler verimli biçimde bulunur.

```python
def mod_pow(a, e, p):
    sonuc = 1
    while e:
        if e & 1:
            sonuc = sonuc * a % p
        a = a * a % p
        e >>= 1
    return sonuc

def nCr_mod_p(n, k, p):
    if k < 0 or k > n:
        return 0
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % p

    payda = fact[k] * fact[n - k] % p
    ters_payda = mod_pow(payda, p - 2, p)
    return fact[n] * ters_payda % p
```

Bu yöntem $n < p$ iken özellikle temizdir. $n$ modülü aşıyorsa faktöriyellerin içinde $p$ çarpanı oluşur ve sonuç sıfır gibi görünse bile paydadaki çarpanlar durumu değiştirebilir. Bu noktada **Lucas teoremi** devreye girer: $n$ ve $k$ sayılarını $p$ tabanında basamaklarına ayırır, büyük kombinasyonu küçük kombinasyonların çarpımına dönüştürür.

| Durum | Uygun araç | Ana fikir |
|---|---|---|
| $n<p$, $p$ asal | Ters faktöriyel | Fermat ile modüler ters |
| Çok büyük üs | Hızlı üs alma | Kareleme ile $O(\log e)$ |
| $n\ge p$, $p$ asal | Lucas teoremi | $p$ tabanındaki basamaklar |
| Modül bileşik | Asal çarpanlara ayırma/CRT | Terslerin her zaman olmadığını unutma |

Olimpiyat çözümünde hedef yalnızca formülü uygulamak değildir: Önce modülün asal mı bileşik mi olduğunu, faktöriyel içinde hangi çarpanların kaybolduğunu ve bir periyot bulunup bulunmadığını sorgulayın. Doğru gözlem, çoğu zaman hesap makinesinden çok daha güçlüdür.
