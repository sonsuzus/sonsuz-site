---
layout: post
title: "C’de enum ve typedef: Verilere Anlamlı İsimler Vermek"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - enum
  - typedef
  - veri tipleri
  - programlama
toc: true
image: /img/cde-enum-ve-97.png
---

C dilinde her şeyi `int`, `char` veya `float` ile temsil etmek mümkündür; ancak bu yaklaşım büyüyen programlarda kodun anlamını hızla bulanıklaştırır. Örneğin `durum == 2` ifadesindeki 2 neyi anlatır? İşte `enum` sabit değerlere anlamlı adlar verirken, `typedef` karmaşık tip bildirimlerini okunabilir isimlerle sadeleştirir. Bu iki araç programın bellekteki davranışını sihirli biçimde değiştirmez, fakat geliştiricinin kodu anlama hızını ciddi ölçüde artırır.


![cde-enum-ve-97](/img/cde-enum-ve-97.svg)

``

## Numaralandırma: `enum`

`enum`, ilişkili tam sayı sabitlerini tek bir başlık altında toplar. Bir trafik lambasının durumlarını ele alalım:

```c
#include <stdio.h>

enum TrafikIsigi {
    KIRMIZI,
    SARI,
    YESIL
};

int main(void) {
    enum TrafikIsigi aktif = YESIL;

    if (aktif == YESIL) {
        printf("Geçebilirsiniz.\n");
    }

    return 0;
}
```

Değer belirtilmediğinde ilk eleman `0` olur ve sonraki elemanlar birer artar. Yani burada `KIRMIZI = 0`, `SARI = 1` ve `YESIL = 2` kabul edilir. Genel olarak ilk değer $v_0 = 0$ ise sıralama $v_i = v_0 + i$ biçimindedir.

Değerleri kendimiz de belirleyebiliriz:

```c
enum HttpDurumu {
    HTTP_OK = 200,
    HTTP_BULUNAMADI = 404,
    HTTP_SUNUCU_HATASI = 500
};
```

Böylece `durum == 404` yerine `durum == HTTP_BULUNAMADI` yazılır. İki ifade sayısal olarak aynı sonucu üretse de ikincisi niyeti açıklar.

## `typedef` ile tiplere takma ad vermek

`typedef`, mevcut bir tipe yeni bir isim tanımlar. Yeni ve bağımsız bir veri tipi oluşturmaz; derleyici açısından çoğunlukla bir takma addır.

```c
typedef unsigned long KullaniciId;
typedef float Sicaklik;

KullaniciId id = 12045;
Sicaklik oda = 23.5f;
```

Burada `KullaniciId`, `unsigned long` ile aynı temsile sahiptir. Dolayısıyla bellek boyutu için şu ilişki geçerlidir:

$$sizeof(KullaniciId) = sizeof(unsigned\ long)$$

Asıl avantaj, değişkenin ne amaçla kullanıldığını göstermesidir. Yine de `typedef` güçlü tip güvenliği sağlamaz; `KullaniciId` ile başka bir `unsigned long` değer yanlışlıkla karıştırılabilir.

| Özellik | `enum` | `typedef` |
|---|---|---|
| Temel amaç | İsimlendirilmiş sabitler oluşturmak | Bir tipe alternatif isim vermek |
| Yeni değer kümesi | Evet, sembolik sabitler tanımlar | Hayır |
| Okunabilirlik katkısı | Durum ve seçenekleri açıklar | Karmaşık bildirimleri sadeleştirir |
| Yaygın kullanım | Durumlar, modlar, hata kodları | Yapılar, işaretçiler, platform tipleri |

## `struct`, `enum` ve `typedef` birlikte

C dilinde yapı değişkeni tanımlarken normalde `struct` anahtar kelimesi tekrar edilir. `typedef` bu gürültüyü azaltabilir:

```c
typedef enum {
    ROL_MISAFIR,
    ROL_EDITOR,
    ROL_YONETICI
} KullaniciRolu;

typedef struct {
    unsigned int id;
    char ad[40];
    KullaniciRolu rol;
} Kullanici;

void rolYazdir(Kullanici kullanici) {
    switch (kullanici.rol) {
        case ROL_MISAFIR:
            printf("Misafir\n");
            break;
        case ROL_EDITOR:
            printf("Editör\n");
            break;
        case ROL_YONETICI:
            printf("Yönetici\n");
            break;
        default:
            printf("Geçersiz rol\n");
    }
}
```

Bu örnekte `KullaniciRolu`, numaralandırmanın; `Kullanici` ise yapının kısa tip ismidir. `switch` kullanımı olası değerleri görmeyi kolaylaştırır. `default` dalı eklemek de dışarıdan veya hatalı dönüşümle gelebilecek geçersiz değerlere karşı savunma sağlar.

## Dikkat edilmesi gerekenler

C, `enum` değişkenine yalnızca listelenen değerlerin atanmasını kesin olarak engellemez. Örneğin açık bir dönüşüm veya doğrudan atama sonucunda beklenmeyen sayılar oluşabilir. Bu nedenle giriş doğrulaması hâlâ gereklidir. Ayrıca bir `enum` türünün boyutunun her platformda mutlaka `int` boyutunda olduğunu varsaymak taşınabilir kod açısından doğru değildir.

İsim çakışmalarını önlemek için sabitlerde `ROL_`, `HTTP_` veya `RENK_` gibi önekler kullanmak iyi bir alışkanlıktır. Özetle `enum`, “hangi seçenek?” sorusunu; `typedef` ise “bu veri neyi temsil ediyor?” sorusunu yanıtlar. Birlikte kullanıldıklarında C kodu yalnızca çalışan değil, aynı zamanda kendi hikâyesini anlatan bir yapıya kavuşur.
