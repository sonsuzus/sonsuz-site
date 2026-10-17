---
layout: post
title: "C Operatörler ve İfadeler: Sayılardan Bitlere İşlem Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - operatörler
  - ifadeler
  - aritmetik
  - mantıksal işlemler
  - bitsel işlemler
toc: true
image: /img/c-operatorler-ve-63.png
---

C dilinde değişkenler verileri saklarken operatörler bu verileri harekete geçirir. Toplama yapmak, iki değeri karşılaştırmak, koşulları birleştirmek veya sayının bitlerini değiştirmek için operatörlerden yararlanırız. Kısacası değişkenler mutfağın malzemeleriyse operatörler bıçak, kaşık ve mikserdir; doğru aracı doğru yerde kullanmak gerekir.

``

## İfade ve operatör nedir?

Bir **operatör**, bir veya daha fazla değer üzerinde işlem yapan semboldür. İşleme katılan değerlere **operand**, operatör ve operandların oluşturduğu yapıya ise **ifade** denir.

```c
int sonuc = 8 + 4 * 2;
```

Burada `+` ve `*` operatör, sayılar operand, `8 + 4 * 2` ise bir ifadedir. İşlem önceliği nedeniyle önce çarpma yapılır:

$$8 + 4 \times 2 = 16$$

Sonucun 24 olmasını isteseydik `(8 + 4) * 2` yazmamız gerekirdi. Kararsız kaldığınızda parantez kullanmak, hem derleyiciyi hem de kodu okuyacak insanı mutlu eder.

## Aritmetik operatörler

Aritmetik operatörler sayısal hesaplamalarda kullanılır.

| Operatör | İşlem | Örnek | Sonuç |
|---|---|---|---|
| `+` | Toplama | `7 + 3` | `10` |
| `-` | Çıkarma | `7 - 3` | `4` |
| `*` | Çarpma | `7 * 3` | `21` |
| `/` | Bölme | `7 / 3` | `2` |
| `%` | Kalan | `7 % 3` | `1` |

![c-operatorler-ve-63](/img/c-operatorler-ve-63.svg)


C dilinde iki `int` değerin bölümü tam sayı üretir. Ondalıklı sonuç için operandlardan en az biri kayan noktalı olmalıdır.

```c
#include <stdio.h>

int main(void) {
    int a = 7, b = 3;

    printf("Tam sayi bolme: %d\n", a / b);
    printf("Ondalikli bolme: %.2f\n", (double)a / b);
    printf("Kalan: %d\n", a % b);
    return 0;
}
```

Tür dönüşümü yapan `(double)a`, bölmenin `2.33` üretmesini sağlar. `%` operatörü ise bir sayının tek veya çift olduğunu belirlemek gibi işlerde oldukça kullanışlıdır.

## İlişkisel operatörler

İlişkisel operatörler iki değeri karşılaştırır ve doğruysa `1`, yanlışsa `0` üretir.

| Operatör | Anlamı | Örnek |
|---|---|---|
| `==` | Eşittir | `a == b` |
| `!=` | Eşit değildir | `a != b` |
| `>` / `<` | Büyük / küçük | `a > b` |
| `>=` / `<=` | Büyük eşit / küçük eşit | `a >= b` |

Buradaki klasik tuzak, atama operatörü `=` ile eşitlik operatörü `==` arasındaki farktır. `a = 5` değeri değiştirir; `a == 5` ise karşılaştırma yapar.

## Mantıksal operatörler

Mantıksal operatörler birden fazla koşulu birleştirir.

| Operatör | Anlamı | Matematiksel karşılık |
|---|---|---|
| `&&` | VE | $A \land B$ |
| `||` | VEYA | $A \lor B$ |
| `!` | DEĞİL | $\neg A$ |

```c
int yas = 22;
int biletiVar = 1;

if (yas >= 18 && biletiVar) {
    printf("Giris onaylandi.\n");
}
```

`&&` kullanıldığında bütün koşullar doğru olmalıdır. C ayrıca **kısa devre değerlendirmesi** yapar: `A && B` ifadesinde `A` yanlışsa `B` çalıştırılmaz. `A || B` ifadesinde ise `A` doğruysa ikinci koşula bakılmaz.

## Bitsel operatörler

Bitsel operatörler sayıların ikili gösterimi üzerinde çalışır. Örneğin $12_{10}=1100_2$ ve $10_{10}=1010_2$ olur.

| Operatör | İşlem | `12` ve `10` sonucu |
|---|---|---|
| `&` | Bitsel VE | `8` |
| `|` | Bitsel VEYA | `14` |
| `^` | Bitsel XOR | `6` |
| `~` | Bitleri ters çevirme | Türe bağlı |
| `<<` | Sola kaydırma | `12 << 1` → `24` |
| `>>` | Sağa kaydırma | `12 >> 1` → `6` |

```c
unsigned int izinler = 0;
const unsigned int OKUMA = 1u << 0;
const unsigned int YAZMA = 1u << 1;

izinler |= OKUMA;             // Okuma bitini açar.
izinler |= YAZMA;             // Yazma bitini açar.
izinler &= ~YAZMA;            // Yazma bitini kapatır.

if ((izinler & OKUMA) != 0) {
    printf("Okuma izni var.\n");
}
```

Bu yaklaşım izinler, donanım kayıtları ve performans odaklı yapılarda kullanılır. Bitsel işlemlerde işaretli sayıların davranışına takılmamak için çoğunlukla `unsigned` türler tercih edilir.

## Öncelik konusunda son uyarı

Aritmetik, ilişkisel, mantıksal ve bitsel operatörlerin öncelikleri farklıdır. `x & 1 == 0` gibi belirsiz görünen ifadeler yerine `(x & 1) == 0` yazmak daha güvenlidir. C operatörlerini ezberlemek faydalıdır; ancak okunabilir parantezler kullanmak çok daha değerlidir.
