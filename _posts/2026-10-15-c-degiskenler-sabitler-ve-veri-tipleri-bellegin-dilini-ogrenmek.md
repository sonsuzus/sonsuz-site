---
layout: post
title: "C Değişkenler, Sabitler ve Veri Tipleri: Belleğin Dilini Öğrenmek"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - değişkenler
  - veri-tipleri
  - sabitler
  - bellek
  - programlama
toc: true
image: /img/c-degiskenler-sabitler-64.png
---

C programında oluşturduğumuz her değişken, bellekte ayrılmış bir alanı temsil eder. Veri tipi ise derleyiciye bu alanın yaklaşık büyüklüğünü, içindeki bitlerin nasıl yorumlanacağını ve hangi işlemlerin uygulanabileceğini söyler. Kısacası değişken bir kutuysa veri tipi kutunun etiketi, sabit ise kapağı kilitlenmiş kutudur.


![c-degiskenler-sabitler-64](/img/c-degiskenler-sabitler-64.svg)

``

## Değişkenin bellekteki yaşamı

Bir değişken tanımlanırken genel olarak `veri_tipi isim = değer;` kalıbı kullanılır. Örneğin `int yas = 25;` ifadesi, `yas` adında bir bellek alanı oluşturur ve buraya 25 değerini yazar.

```c
#include <stdio.h>

int main(void) {
    int yas = 25;
    float sicaklik = 22.5f;
    char seviye = 'A';

    printf("Yaş: %d\n", yas);
    printf("Sıcaklık: %.1f\n", sicaklik);
    printf("Seviye: %c\n", seviye);
    return 0;
}
```

Burada `int` tam sayıları, `float` ondalıklı sayıları, `char` ise tek bir karakteri saklar. Karakterler bellekte aslında sayısal kodlar hâlinde tutulur. Örneğin ASCII sisteminde `'A'` karakterinin karşılığı 65'tir.

## Temel veri tipleri

C standardı bazı tiplerin kesin boyutunu değil, asgari kapasitesini ve birbirleriyle ilişkisini tanımlar. Bu nedenle aşağıdaki boyutlar yaygın sistemlerde görülen değerlerdir; kesin sonuç için `sizeof` kullanılmalıdır.

| Veri tipi | Yaygın boyut | Kullanım amacı | Örnek |
|---|---:|---|---|
| `char` | 1 bayt | Karakter veya küçük tamsayı | `'K'` |
| `short` | 2 bayt | Küçük tamsayı | `1200` |
| `int` | 4 bayt | Genel amaçlı tamsayı | `50000` |
| `long long` | 8 bayt | Büyük tamsayı | `9000000LL` |
| `float` | 4 bayt | Tek duyarlıklı ondalık | `3.14f` |
| `double` | 8 bayt | Daha hassas ondalık | `3.14159` |

Bir tip $n$ bitlik işaretsiz bir tamsayı saklıyorsa değer aralığı genellikle $0$ ile $2^n-1$ arasındadır. İki'nin tümleyeni kullanılan işaretli sistemlerde yaklaşık aralık $-2^{n-1}$ ile $2^{n-1}-1$ olur. Örneğin 8 bitlik işaretsiz değer $0$–$255$ aralığını kapsar.

```c
#include <stdio.h>

int main(void) {
    printf("int: %zu bayt\n", sizeof(int));
    printf("double: %zu bayt\n", sizeof(double));
    printf("char: %zu bayt\n", sizeof(char));
    return 0;
}
```

`sizeof`, türün veya değişkenin kaç bayt kapladığını döndürür. Sonuç `size_t` tipinde olduğu için `%zu` biçim belirteci kullanılır.

## Niteleyiciler neyi değiştirir?

`short`, `long`, `signed` ve `unsigned`, tamsayı tiplerinin kapasitesini veya işaret davranışını düzenler. `const` ve `volatile` ise erişim kurallarını belirtir.

| Niteleyici | Etkisi |
|---|---|
| `unsigned` | Negatif değer yerine daha geniş pozitif aralık sağlar |
| `signed` | Pozitif ve negatif değerleri destekler |
| `short` | Genellikle daha küçük tamsayı tipi oluşturur |
| `long` | Daha geniş sayı türü belirtir |
| `const` | Program kodu üzerinden değiştirilmeyi engeller |
| `volatile` | Değerin dış etkenlerle değişebileceğini derleyiciye bildirir |

`volatile`, özellikle mikrodenetleyici yazmaçlarında veya sinyal işleyicilerinde önemlidir. Derleyicinin değeri bir kez okuyup önbellekte tutmasını engeller; ancak değişkeni eşzamanlı erişime karşı güvenli yapmaz.

## Sabit oluşturma yöntemleri

```c
#include <stdint.h>

#define BUFFER_SIZE 256

enum { MAX_RETRY = 3 };

int main(void) {
    const double pi = 3.1415926535;
    uint32_t paket_no = 42U;
    double alan = pi * 5.0 * 5.0;
    return alan > 0.0 && paket_no < BUFFER_SIZE ? 0 : 1;
}
```

`const`, türü belli salt okunur bir nesne oluşturur. `#define` metinsel ön işlemci değişimidir ve tip denetimi sağlamaz. `enum` ise tamsayı sabitleri için kullanışlıdır. `stdint.h` içindeki `uint32_t` gibi tipler, mevcut olduklarında kesin bit genişliği sağlayarak taşınabilir veri formatlarında belirsizliği azaltır.

Sonuç olarak doğru veri tipi seçimi yalnızca bellek tasarrufu değildir; sayı taşmalarını, hassasiyet kaybını ve platformlar arası sürprizleri önleyen temel bir tasarım kararıdır. C, belleği gizlemek yerine size anahtarları verir; fakat hangi kapıyı açtığınıza dikkat etmek tamamen sizin sorumluluğunuzdadır.
