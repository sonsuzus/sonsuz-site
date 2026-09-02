---
layout: post
title: "Euler Totient Fonksiyonu Pratikleri: Sayma, Şifreleme ve Bulmaca Çözme"
math: true
categories: 
  - Bilgi
tags: 
  - euler totient
  - sayı teorisi
  - kriptografi
toc: true
---

Bir sayıyla aralarında asal kaç pozitif tam sayı bulunduğunu bilmek, ilk bakışta yalnızca matematik olimpiyatlarında işe yarayan bir beceri gibi görünebilir. Oysa Euler Totient fonksiyonu; modüler aritmetikten RSA şifrelemesine, periyodik sayı bulmacalarından programlama yarışmalarına kadar pek çok yerde karşımıza çıkar. Üstelik doğru formül öğrenildiğinde yüzlerce sayıyı tek tek kontrol etmek yerine asal çarpanlarla sonuca hızla ulaşabiliriz.

``

## Totient fonksiyonu neyi sayar?

Euler Totient fonksiyonu $\phi(n)$, $1$ ile $n$ arasındaki sayılardan $n$ ile aralarında asal olanların adedidir. İki sayının aralarında asal olması, en büyük ortak bölenlerinin 1 olması demektir:

$$\gcd(a,n)=1$$

Örneğin $n=10$ için uygun sayılar $1,3,7,9$ olduğundan $\phi(10)=4$ elde edilir. Burada 10 sayısının kendisi sayılmaz; zaten $\gcd(10,10)=10$ olur.

| $n$ | Aralarında asal sayılar | $\phi(n)$ |
|---:|---|---:|
| 6 | 1, 5 | 2 |
| 8 | 1, 3, 5, 7 | 4 |
| 9 | 1, 2, 4, 5, 7, 8 | 6 |
| 10 | 1, 3, 7, 9 | 4 |

## Asal çarpan formülü

$n$ sayısının farklı asal bölenleri biliniyorsa temel formül şöyledir:

$$\phi(n)=n\prod_{p\mid n}\left(1-\frac{1}{p}\right)$$

Örneğin $36=2^2\cdot3^2$ olduğundan yalnızca farklı asal çarpanlar olan 2 ve 3 kullanılır:

$$\phi(36)=36\left(1-\frac12\right)\left(1-\frac13\right)=12$$

Formülün mantığı eleme yöntemine dayanır. Önce 2'nin katlarını, ardından 3'ün katlarını eleriz. Çakışan katların iki kez çıkarılmasını önleyen yapı, çarpım biçiminde doğal olarak ortaya çıkar.

Bazı özel durumları tanımak hesaplamayı daha da hızlandırır:

| Sayı türü | Sonuç |
|---|---|
| $p$ asal | $\phi(p)=p-1$ |
| $p^k$ asal kuvvet | $\phi(p^k)=p^k-p^{k-1}$ |
| $\gcd(a,b)=1$ | $\phi(ab)=\phi(a)\phi(b)$ |

## Python ile hızlı hesaplama

Aşağıdaki fonksiyon, sayıyı deneme bölmesiyle çarpanlarına ayırır. Her farklı asal bölen bulunduğunda sonucu $p$ oranında azaltır:

```python
def totient(n):
    result = n
    p = 2

    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1

    if n > 1:
        result -= result // n

    return result

print(totient(36))  # 12
```

İçteki döngü aynı asal çarpanın bütün kuvvetlerini temizler. Böylece formüldeki her asal bölen yalnızca bir kez uygulanır. Algoritmanın yaklaşık karmaşıklığı $O(\sqrt n)$ düzeyindedir ve tekil sorgular için oldukça pratiktir.

Çok sayıda sorgu varsa Eratosthenes eleğine benzeyen bir totient eleği daha uygundur:

```python
def totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:  # p asaldır
            for multiple in range(p, limit + 1, p):
                phi[multiple] -= phi[multiple] // p
    return phi
```

## Şifreleme ve bulmacalarda kullanım

RSA'da genellikle iki asal sayı seçilip $n=pq$ oluşturulur. Bu durumda:

$$\phi(n)=(p-1)(q-1)$$

Açık anahtar üssü $e$, $\phi(n)$ ile aralarında asal seçilir; gizli üs ise $ed\equiv1\pmod{\phi(n)}$ koşulunu sağlar. Gerçek RSA anahtarları çok büyük asal sayılar kullandığı için $n$ değerini çarpanlarına ayırmak zordur. Güvenliğin önemli bir bölümü tam da bu zorluğa dayanır.

Bulmacalarda ise Euler teoremi güçlü bir kısayoldur. Eğer $\gcd(a,n)=1$ ise:

$$a^{\phi(n)}\equiv1\pmod n$$

Örneğin devasa bir üssün son basamağını veya modüler kalanını ararken üs, $\phi(n)$ üzerinden küçültülebilir. Ancak önce aralarında asallık koşulunu kontrol etmek şarttır; aksi hâlde teoremi doğrudan kullanmak yanlış sonuç verebilir. Kısacası strateji nettir: sayıyı çarpanlarına ayır, totient değerini hesapla, koşulları doğrula ve büyük problemi küçük bir modüler bulmacaya dönüştür.
