---
layout: post
title: "C Önişlemci Komutları: Makrolar ve Koşullu Derleme Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - önişlemci
  - makro
  - koşullu-derleme
  - gcc
  - programlama
toc: true
image: /img/c-onislemci-komutlari-51.png
---

C dilinde kaynak kod, doğrudan makine koduna çevrilmez; önce birkaç aşamadan geçen küçük bir yolculuğa çıkar. Önişlemci, bu yolculuğun derlemeden hemen önceki durağıdır. `#include`, `#define` ve `#if` gibi direktifleri işler; başlık dosyalarını ekler, makroları genişletir ve hangi kod parçalarının derleyiciye ulaşacağını belirler. Kısacası önişlemci, sahne açılmadan önce dekoru hazırlayan görünmez bir ekip gibidir.
``

## Derlemeden önce neler olur?

Tipik bir C programının üretim süreci kabaca dört aşamaya ayrılır:

| Aşama | Girdi | Yapılan işlem | Çıktı |
|---|---|---|---|
| Önişleme | `.c` dosyası | Direktifler ve makrolar işlenir | Genişletilmiş kaynak kod |
| Derleme | Genişletilmiş kod | C kodu assembly diline çevrilir | Assembly kodu |
| Assembly | Assembly kodu | Makine komutları oluşturulur | Nesne dosyası |
| Bağlama | Nesne dosyaları | Kütüphaneler birleştirilir | Çalıştırılabilir program |

Bu süreci sembolik olarak şöyle gösterebiliriz:

$$Kaynak \rightarrow Önişlemci \rightarrow Derleyici \rightarrow Assembler \rightarrow Bağlayıcı$$

GCC kullanırken yalnızca önişlemci çıktısını görmek için şu komut çalıştırılabilir:

```bash
gcc -E program.c -o program.i
```

Oluşan `program.i` dosyası genellikle oldukça uzundur; çünkü eklenen başlıkların içeriği de bu dosyada görünür.

## `#include`: Başlık dosyalarını eklemek

`#include`, belirtilen dosyanın içeriğini mevcut kaynak dosyaya metinsel olarak ekler:

```c
#include <stdio.h>
#include "hesaplama.h"
```

| Yazım | Genel kullanım | Arama davranışı |
|---|---|---|
| `<stdio.h>` | Standart veya sistem başlıkları | Sistem başlık dizinleri aranır |
| `"hesaplama.h"` | Projeye ait başlıklar | Önce mevcut proje dizini aranır |

Aynı başlığın birden fazla kez eklenmesi tanım çakışmalarına yol açabilir. Bu nedenle include guard kullanılır:

```c
#ifndef HESAPLAMA_H
#define HESAPLAMA_H

int topla(int a, int b);

#endif
```

İlk eklemede `HESAPLAMA_H` tanımlanır. Sonraki eklemelerde `#ifndef` koşulu yanlış olacağı için dosyanın gövdesi atlanır.

## `#define`: Metinsel dönüşüm yapan makrolar

Nesne benzeri makrolar sabit değerleri temsil edebilir:

```c
#define PI 3.141592653589793
#define MAKSIMUM_KULLANICI 100
```

Örneğin dairenin alanı $A = \pi r^2$ bağıntısıyla hesaplanabilir:

```c
#define PI 3.141592653589793
#define KARE(x) ((x) * (x))

double alan(double yaricap) {
    return PI * KARE(yaricap);
}
```

Parantezler önemlidir. `#define KARE(x) x * x` yazılsaydı `KARE(a + 1)` ifadesi `a + 1 * a + 1` biçiminde genişleyerek işlem önceliği hatası oluştururdu.

Makroların tür denetimi yapmadığı ve yalnızca metin değiştirdiği unutulmamalıdır. Ayrıca `KARE(i++)` gibi bir kullanım, argümanı iki kez değerlendirebilir. Bu durumda beklenmeyen yan etkiler ortaya çıkar. Tür güvenliği ve tek değerlendirme gerektiğinde `inline` fonksiyon genellikle daha iyi bir seçimdir.

| Özellik | Makro | `inline` fonksiyon |
|---|---|---|
| Tür denetimi | Yok | Var |
| Argüman değerlendirmesi | Birden fazla olabilir | Bir kez |
| Çalıştığı aşama | Önişleme | Derleme |
| Hata ayıklama | Daha zor | Daha kolay |

## Koşullu derleme

Koşullu direktifler, platforma veya yapılandırmaya göre farklı kodların derlenmesini sağlar:

```c
#ifdef DEBUG
    printf("Hata ayıklama modu etkin\n");
#endif

#if defined(_WIN32)
    printf("Windows üzerinde çalışıyor\n");
#elif defined(__linux__)
    printf("Linux üzerinde çalışıyor\n");
#else
    printf("Bilinmeyen platform\n");
#endif
```

Komut satırından bir makro tanımlamak da mümkündür:

```bash
gcc -DDEBUG program.c -o program
```

`#undef DEBUG` ise daha önce tanımlanmış makroyu kaldırır. Önişlemci ifadelerinde `defined`, mantıksal operatörler ve tamsayı sabitleri kullanılabilir; ancak normal C değişkenleri kullanılamaz. Çünkü değişkenler henüz derleyici tarafından işlenmemiştir.

Sonuç olarak C önişlemcisi güçlü fakat dikkatsiz kullanıldığında şaşırtıcıdır. Makroları küçük ve parantezli tutmak, include guard kullanmak, koşullu derlemeyi belgeli yürütmek ve mümkün olduğunda sabitler ile `inline` fonksiyonları tercih etmek daha okunabilir, taşınabilir ve güvenli programlar üretir.

![c-onislemci-komutlari-51](/img/c-onislemci-komutlari-51.svg)

