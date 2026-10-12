---
layout: post
title: "Lineer Homojen Yinelemeli İlişkiler: Fibonacci’nin Kapalı Formuna Yolculuk"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - algoritma
  - fibonacci
  - yinelemeli ilişkiler
  - python
toc: true
image: /img/lineer-homojen-yinelemeli-29.png
---

![lineer-homojen-yinelemeli-29](/img/lineer-homojen-yinelemeli-29.svg)


Bir dizinin sonraki elemanını önceki elemanlardan üretmek oldukça doğaldır. Fibonacci dizisinde yaptığımız gibi iki sayıyı toplar, yenisini buluruz. Fakat doğrudan milyonuncu terim sorulduğunda bu yöntem biraz yorulur. Lineer homojen yinelemeli ilişkiler, dizinin bütün davranışını tek bir formülde yakalamamızı sağlayarak yinelemeyi adeta cebirsel bir kestirme yola dönüştürür.

``

## Lineer homojen ilişki nedir?

Sabit katsayılı, ikinci dereceden bir lineer homojen yinelemeli ilişki genel olarak

$$a_n=c_1a_{n-1}+c_2a_{n-2}$$

biçimindedir. “Lineer” denmesinin nedeni önceki terimlerin kuvvetlerinin veya birbirleriyle çarpımlarının bulunmamasıdır. “Homojen” ifadesi ise eşitliğe dizi dışından eklenen bağımsız bir fonksiyon olmadığını belirtir.

Örneğin $a_n=3a_{n-1}-2a_{n-2}$ homojendir. Buna karşılık $a_n=3a_{n-1}+n$ homojen değildir; çünkü $n$ biçiminde dışarıdan gelen bir terim vardır.

| Özellik | Homojen örnek | Homojen olmayan örnek |
|---|---|---|
| İlişki | $a_n=2a_{n-1}+a_{n-2}$ | $a_n=2a_{n-1}+n$ |
| Dış kaynaklı terim | Yok | Var |
| Temel çözüm yaklaşımı | Karakteristik denklem | Homojen ve özel çözüm |

## Karakteristik denklem fikri

Çözümün $a_n=r^n$ biçiminde olduğunu varsayalım. Bu tahmin rastgele değildir: Üstel ifadeler kaydırıldıklarında yalnızca sabit bir çarpan kazanır. Varsayımı genel ilişkiye yerleştirirsek

$$r^n=c_1r^{n-1}+c_2r^{n-2}$$

elde ederiz. $r^{n-2}$ ortak çarpanına böldüğümüzde karakteristik denklem ortaya çıkar:

$$r^2-c_1r-c_2=0$$

Denklemin birbirinden farklı iki kökü $r_1$ ve $r_2$ ise genel çözüm

$$a_n=A r_1^n+B r_2^n$$

olur. $A$ ve $B$ sabitleri başlangıç koşullarından bulunur. Böylece her terimi sırayla hesaplamak yerine doğrudan istenen indekse gideriz.

| Kök durumu | Genel çözüm |
|---|---|
| Farklı gerçek kökler | $A r_1^n+B r_2^n$ |
| Çift katlı kök $r$ | $(A+Bn)r^n$ |
| Karmaşık eşlenik kökler | Üstel ve trigonometrik biçimlerin birleşimi |

## Fibonacci’ye uygulayalım

Fibonacci ilişkisi

$$F_n=F_{n-1}+F_{n-2}, \qquad F_0=0,\quad F_1=1$$

şeklindedir. $F_n=r^n$ varsayımı karakteristik denklemi verir:

$$r^2-r-1=0$$

Kökler altın oran $phi$ ve onun eşleniğidir:

$$r_1=\frac{1+\sqrt{5}}{2}=\phi, \qquad r_2=\frac{1-\sqrt{5}}{2}=\psi$$

Dolayısıyla $F_n=A\phi^n+B\psi^n$ yazılır. $F_0=0$ ve $F_1=1$ koşulları kullanıldığında $A=1/\sqrt{5}$ ve $B=-1/\sqrt{5}$ bulunur. Sonuç, Binet formülü olarak bilinen zarif ifadedir:

$$F_n=\frac{\phi^n-\psi^n}{\sqrt{5}}$$

İçinde irrasyonel sayılar bulunmasına rağmen sonuç her doğal $n$ için tam sayıdır. Bunun nedeni, iki üstel terimde oluşan irrasyonel parçaların birbirini tam olarak yok etmesidir. Ayrıca $\vert \psi\vert <1$ olduğu için büyük $n$ değerlerinde $\psi^n$ sıfıra yaklaşır. Bu nedenle yaklaşık olarak $F_n\approx \phi^n/\sqrt{5}$ denebilir.

## Python ile doğrulama

Aşağıdaki kod hem yinelemeli hesaplamayı hem de kapalı formu uygular. `round` kullanılması, kayan noktalı işlemlerde oluşabilecek küçük hassasiyet hatalarını temizler.

```python
from math import sqrt

def fibonacci_iteratif(n):
    onceki, simdiki = 0, 1
    for _ in range(n):
        onceki, simdiki = simdiki, onceki + simdiki
    return onceki

def fibonacci_binet(n):
    phi = (1 + sqrt(5)) / 2
    psi = (1 - sqrt(5)) / 2
    return round((phi**n - psi**n) / sqrt(5))

for n in range(11):
    print(n, fibonacci_iteratif(n), fibonacci_binet(n))
```

Kapalı form teorik olarak doğrudan hesaplama sağlasa da çok büyük indekslerde kayan nokta hassasiyeti sorun çıkarabilir. Bu durumda matris üs alma veya tam sayı aritmetiği daha güvenilirdir. Yine de karakteristik denklem yöntemi, dizinin büyüme hızını ve köklerin davranış üzerindeki etkisini görmenin en güçlü yollarından biridir.
