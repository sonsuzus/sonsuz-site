---
layout: post
title: "C Göstericiler: Belleğin Adres Defterini Okumak"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - göstericiler
  - bellek
  - pointer
  - işaretçi-aritmetiği
  - programlama
toc: true
image: /img/c-gostericiler-bellegin-75.png
---

C dilinde göstericiler, ilk karşılaşmada belleğin karanlık sokaklarında dolaşmak gibi görünebilir. Oysa bir gösterici yalnızca başka bir nesnenin bellekteki adresini saklayan değişkendir. Bu mekanizmayı kavradığınızda dizilerin, dinamik belleğin, fonksiyon parametrelerinin ve veri yapılarının neden bu kadar verimli çalıştığını da anlamaya başlarsınız.

``

## Değer Değil, Adres Saklamak

Normal bir değişken doğrudan veri taşır. Gösterici ise bu verinin bulunduğu konumu taşır. Örneğin `int sayi = 42;` ifadesi bellekte bir tamsayı oluşturur. `&sayi`, bu değişkenin adresini verir; `*ptr` ise göstericinin tuttuğu adrese giderek oradaki değere erişir.

| İfade | Anlamı | Örnek sonuç |
|---|---|---|
| `sayi` | Değişkenin değeri | `42` |
| `&sayi` | Değişkenin adresi | `0x7ffd...` |
| `ptr` | Göstericide saklanan adres | `0x7ffd...` |
| `*ptr` | Adresteki değer | `42` |

![c-gostericiler-bellegin-75](/img/c-gostericiler-bellegin-75.svg)


```c
#include <stdio.h>

int main(void) {
    int sayi = 42;
    int *ptr = &sayi;

    printf("Deger: %d\n", sayi);
    printf("Adres: %p\n", (void *)ptr);
    printf("Pointer uzerinden deger: %d\n", *ptr);

    *ptr = 99; /* Adresteki gerçek değeri değiştirir. */
    printf("Yeni deger: %d\n", sayi);
    return 0;
}
```

Burada `int *ptr`, `ptr` değişkeninin bir `int` adresi taşıyacağını belirtir. `*ptr = 99` işlemi kopyayı değil, doğrudan `sayi` değişkenini değiştirir. Göstericilerin fonksiyonlara “dışarıdaki” veriyi değiştirme gücü vermesi de bu mantığa dayanır.

## Bellek ve Tür Bilgisi

Bir adresi yalnızca sayı gibi düşünmek eksik kalır. Göstericinin türü, derleyiciye o adreste kaç baytlık ve nasıl yorumlanacak bir veri bulunduğunu söyler. Tipik bir sistemde `char` 1 bayt, `int` 4 bayt olabilir; ancak kesin boyutlar platforma bağlıdır ve `sizeof` ile öğrenilmelidir.

Bir dizinin başlangıç adresi $A$, eleman boyutu $s$ ve erişilecek indis $i$ olsun. İlgili elemanın adresi şu şekilde hesaplanır:

$$\operatorname{adres}(dizi[i]) = A + i \times s$$

Bu nedenle işaretçi aritmetiği sıradan tam sayı aritmetiğinden farklıdır. `ptr + 1`, adresi bir bayt değil, gösterilen türün boyutu kadar ilerletir.

```c
#include <stdio.h>

int main(void) {
    int sayilar[] = {10, 20, 30, 40};
    int *ptr = sayilar;

    for (size_t i = 0; i < 4; i++) {
        printf("%zu: %d\n", i, *(ptr + i));
    }
    return 0;
}
```

`*(ptr + i)` ile `ptr[i]` eşdeğerdir. Hatta `sayilar[i]` ifadesi de temelde başlangıç adresinden uygun miktarda ilerleyip değeri çözme işlemidir.

| İşlem | Etki | Güvenli kullanım |
|---|---|---|
| `ptr++` | Sonraki elemana geçer | Dizi sınırları içinde |
| `ptr--` | Önceki elemana geçer | Başlangıcın gerisine gitmeden |
| `ptr2 - ptr1` | Eleman uzaklığını verir | Aynı dizi üzerinde |
| `ptr + i` | `i` eleman ilerler | Geçerli aralıkta |

## NULL ve Tehlikeli Göstericiler

Başlatılmamış bir gösterici rastgele bir adres taşıyabilir. `NULL`, göstericinin geçerli bir nesneyi göstermediğini açıkça belirtir. Ancak `NULL` göstericiyi çözmek, yani `*ptr` kullanmak tanımsız davranıştır.

```c
int *ptr = NULL;

if (ptr != NULL) {
    /* Yalnızca geçerli adres varsa erişilir. */
    *ptr = 5;
}
```

Benzer şekilde yaşam süresi bitmiş yerel değişkenlerin adresleri ve `free` ile serbest bırakılmış bölgeleri gösteren işaretçiler “sarkan gösterici” oluşturur. Dizi sınırını aşmak da komşunun posta kutusunu kendi kutunuz sanmaya benzer: Adres vardır, fakat erişim hakkınız yoktur.

## Sonuç

Göstericiler C'nin performans ve kontrol gücünün merkezindedir. `&` adres alır, `*` adresteki veriyi çözer, tür bilgisi ise aritmetik adımların boyutunu belirler. Güvenli kullanım için göstericileri başlatmak, `NULL` kontrolü yapmak, nesnelerin yaşam süresini izlemek ve dizi sınırlarını korumak gerekir. Bu kurallar oturduğunda belleğin karanlık sokakları, tabelaları gayet okunaklı bir mahalleye dönüşür.
