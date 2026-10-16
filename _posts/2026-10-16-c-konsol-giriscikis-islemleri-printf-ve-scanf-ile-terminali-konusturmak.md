---
layout: post
title: "C Konsol Giriş/Çıkış İşlemleri: printf ve scanf ile Terminali Konuşturmak"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - programlama
  - printf
  - scanf
  - konsol
  - giriş-çıkış
toc: true
image: /img/c-konsol-giriscikis-31.png
---

C programında değişkenler bellekte sessizce bekler; onları kullanıcıyla buluşturan ise konsol giriş/çıkış fonksiyonlarıdır. Ekrana biçimli veri yazdırmak için çoğunlukla `printf`, klavyeden veri almak için `scanf` kullanılır. Ancak doğru format belirteçlerini seçmek, giriş hatalarını yakalamak ve metinleri güvenli biçimde okumak en az fonksiyonların kendisi kadar önemlidir.

``

## Standart giriş ve çıkış nedir?

C, konsol işlemlerini birer **akış** olarak ele alır. Program başladığında standart giriş `stdin`, standart çıkış `stdout` ve hata çıkışı `stderr` otomatik olarak açılır. Klavye çoğunlukla `stdin` akışına, terminal ekranı ise `stdout` akışına bağlıdır.

Bu fonksiyonları kullanmak için başlık dosyası eklenir:

```c
#include <stdio.h>
```

Bir giriş/çıkış işleminin basit modeli şöyle düşünülebilir:

$$\text{Kullanıcı} \rightarrow \text{stdin} \rightarrow \text{Program} \rightarrow \text{stdout} \rightarrow \text{Ekran}$$

## printf ile formatlı çıktı

`printf`, metin içindeki format belirteçlerini ilgili değişkenlerin değerleriyle değiştirir.

```c
#include <stdio.h>

int main(void) {
    char ad[] = "Ada";
    int yas = 25;
    double ortalama = 87.456;

    printf("Ad: %s\n", ad);
    printf("Yas: %d\n", yas);
    printf("Ortalama: %.2f\n", ortalama);

    return 0;
}
```

Burada `%s` karakter dizisini, `%d` tam sayıyı ve `%.2f` ondalıklı değeri virgülden sonra iki basamakla yazdırır. `\n` ise imleci yeni satıra taşır.

| Belirteç | Veri türü | Örnek çıktı |
|---|---|---|
| `%d` | `int` | `42` |
| `%u` | `unsigned int` | `42` |
| `%f` | `double` | `3.140000` |
| `%.2f` | `double` | `3.14` |
| `%c` | `char` | `A` |
| `%s` | Karakter dizisi | `Merhaba` |
| `%x` | Onaltılık tam sayı | `ff` |

Alan genişliği de çıktıyı hizalamayı sağlar. Örneğin `%8d`, sayıyı sekiz karakterlik alanda sağa yaslar; `%-8d` sola yaslar. Sayısal bir değeri $w$ genişliğinde göstermek, tablo biçimindeki çıktılarda sütunların düzenli kalmasını sağlar.

## scanf ile klavyeden veri okuma

`scanf`, girilen karakterleri belirtilen türe dönüştürerek değişkenlere yazar. Değişkenin bellekteki adresi gerektiğinden çoğu kullanımda `&` operatörü zorunludur.

```c
#include <stdio.h>

int main(void) {
    int adet;
    double fiyat;

    printf("Adet ve birim fiyat girin: ");

    if (scanf("%d %lf", &adet, &fiyat) == 2) {
        double toplam = adet * fiyat;
        printf("Toplam: %.2f TL\n", toplam);
    } else {
        fprintf(stderr, "Gecersiz veri girdiniz.\n");
    }

    return 0;
}
```

`scanf` başarıyla doldurduğu alanların sayısını döndürür. İki değer bekleniyorsa dönüş değerinin `2` olması gerekir. Matematiksel olarak hesaplanan sonuç:

$$\text{toplam} = \text{adet} \times \text{birim fiyat}$$

Önemli bir ayrıntı: `printf` içinde `double` için `%f`, `scanf` içinde ise `%lf` kullanılır. Yanlış belirteç seçmek tanımsız davranışa yol açabilir.

| İşlem | Fonksiyon | Güçlü yönü | Dikkat edilmesi gereken |
|---|---|---|---|
| Formatlı çıktı | `printf` | Esnek biçimlendirme | Tür ve belirteç uyumu |
| Formatlı giriş | `scanf` | Sayıları kolay dönüştürür | Hatalı giriş akışta kalabilir |
| Satır okuma | `fgets` | Uzunluğu sınırlar | Satır sonunu saklayabilir |
| Tek karakter | `getchar` | Basit karakter okuma | `int` dönüş türü kullanılır |
| Tek karakter yazma | `putchar` | Hafif ve anlaşılır | Yalnızca bir karakter yazar |

## Metin okurken daha güvenli yaklaşım

`scanf("%s", metin)` boşlukta durur ve genişlik belirtilmezse taşma riski doğurur. Tam bir satır okumak için `fgets` daha güvenlidir:

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char ad[40];

    printf("Ad ve soyad: ");
    if (fgets(ad, sizeof ad, stdin) != NULL) {
        ad[strcspn(ad, "\n")] = '\0';
        printf("Hos geldin, %s!\n", ad);
    }

    return 0;
}
```

`sizeof ad`, okunabilecek karakter miktarını sınırlar. `strcspn` ise `fgets` tarafından saklanabilen satır sonunu bulup `\0` ile değiştirir. Kısacası `printf` sunum ustası, `scanf` hızlı veri dönüştürücüsü, `fgets` ise metin girişlerinin emniyet kemeridir.

![c-konsol-giriscikis-31](/img/c-konsol-giriscikis-31.svg)

