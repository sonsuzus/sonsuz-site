---
layout: post
title: "C Dilinde Yapılar ve Birlikler: struct ile union Arasındaki Farklar"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - struct
  - union
  - veri yapıları
  - bellek yönetimi
  - programlama
toc: true
image: /img/c-dilinde-yapilar-86.png
---

C dilinde bir öğrencinin adı, numarası ve notu gibi birbiriyle ilişkili fakat farklı türlerdeki verileri yönetmek istediğimizi düşünelim. Ayrı ayrı değişkenler kullanabiliriz; ancak veri sayısı arttıkça kodumuz kısa sürede dağınık bir çekmeceye dönüşür. `struct` ve `union`, farklı veri türlerini tek bir isim altında toplayarak bu karmaşayı düzenleyen iki güçlü C aracıdır.

``

## Yapı (`struct`) nedir?

Bir yapı, birbiriyle ilişkili değişkenleri tek bir veri modeli içinde saklar. Yapının her üyesi bellekte kendisine ait bir alana sahiptir. Dolayısıyla bütün üyeler aynı anda geçerli değerler taşıyabilir.

```c
#include <stdio.h>
#include <string.h>

struct Ogrenci {
    char ad[30];
    int numara;
    float notOrtalamasi;
};

int main(void) {
    struct Ogrenci ogrenci;

    strcpy(ogrenci.ad, "Ada");
    ogrenci.numara = 1024;
    ogrenci.notOrtalamasi = 91.5f;

    printf("%s - %d - %.1f\n",
           ogrenci.ad,
           ogrenci.numara,
           ogrenci.notOrtalamasi);

    return 0;
}
```

Burada `ogrenci` tek bir değişkendir; fakat `.` operatörüyle erişilen üç farklı üyeyi taşır. Bir yapı işaretçisi kullanıldığında ise üyelere `->` operatörüyle erişilir: `ogrenciPtr->numara`.

## Birlik (`union`) nedir?

Birlik de farklı türleri aynı referans altında toplar, ancak üyelerin tamamı **aynı bellek alanını paylaşır**. Bir üyeye yeni değer yazıldığında diğer üyenin eski değeri güvenilirliğini kaybeder. Yani birlik, “hepsini aynı anda sakla” değil, “bunlardan birini sakla” yaklaşımıdır.

```c
#include <stdio.h>

union Deger {
    int tamSayi;
    float ondalik;
    char karakter;
};

int main(void) {
    union Deger veri;

    veri.tamSayi = 42;
    printf("Tam sayı: %d\n", veri.tamSayi);

    veri.ondalik = 3.14f;
    printf("Ondalık: %.2f\n", veri.ondalik);

    return 0;
}
```

İkinci atamadan sonra `tamSayi` üyesini okumak anlamlı değildir; çünkü aynı bitler artık `float` biçiminde yorumlanmaktadır.

## Bellek hesabı

Bir yapının teorik boyutu üyelerin boyutları toplamına yakındır:

$$S_{struct} \geq \sum_{i=1}^{n} S_i$$

Eşitsizliğin nedeni **padding** adı verilen hizalama boşluklarıdır. Derleyici, işlemcinin verilere daha verimli erişebilmesi için üyeler arasına kullanılmayan baytlar ekleyebilir.

Bir birlik için temel ilişki şöyledir:

$$S_{union} \geq \max(S_1, S_2, \ldots, S_n)$$

Birliğin boyutu genellikle en büyük üyenin boyutudur; hizalama gereksinimleri sonucu küçük farklılıklar görülebilir. Kesin sonucu öğrenmenin doğru yolu `sizeof` kullanmaktır.

| Özellik | `struct` | `union` |
|---|---|---|
| Bellek kullanımı | Üyelerin toplamına yakındır | En büyük üyeye yakındır |
| Aynı anda geçerli üye | Tüm üyeler | Genellikle yalnızca biri |
| Veri koruma | Bir üyeyi değiştirmek diğerlerini bozmaz | Yeni yazma eski üyeyi ezer |
| Tipik kullanım | Kayıt ve nesne modelleme | Değişken türde veri, donanım ve protokoller |

## Güvenli birlik kullanımı: etiketli birlik

Birliğin hangi üyesinin geçerli olduğunu kendiliğinden bilmesi mümkün değildir. Bu nedenle bir `enum` etiketiyle birlik kullanımını güvenli hâle getirebiliriz:

```c
enum DegerTuru {
    TAM_SAYI,
    ONDALIK
};

struct EtiketliDeger {
    enum DegerTuru tur;
    union {
        int tamSayi;
        float ondalik;
    } veri;
};

void yazdir(struct EtiketliDeger deger) {
    if (deger.tur == TAM_SAYI) {
        printf("%d\n", deger.veri.tamSayi);
    } else {
        printf("%.2f\n", deger.veri.ondalik);
    }
}
```

Bu desen, modern dillerdeki variant veya sum type yapılarına benzer. `tur` alanı hangi üyenin okunacağını söyler; `union` ise gereksiz bellek tüketimini azaltır.

Kısacası, bir varlığın bütün özelliklerine aynı anda ihtiyacınız varsa `struct`; seçeneklerden yalnızca biri tutulacaksa `union` uygundur. İkisini birlikte kullanmak ise hem düzenli hem de bellek açısından ekonomik veri modelleri kurmanın etkili bir yoludur.

![c-dilinde-yapilar-86](/img/c-dilinde-yapilar-86.svg)

