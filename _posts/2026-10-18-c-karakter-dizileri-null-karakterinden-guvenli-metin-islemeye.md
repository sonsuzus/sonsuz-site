---
layout: post
title: "C Karakter Dizileri: Null Karakterinden Güvenli Metin İşlemeye"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - string
  - karakter-dizileri
  - bellek
  - pointer
  - programlama
toc: true
image: /img/c-karakter-dizileri-59.png
---

C dilinde metinlerle çalışmak ilk bakışta birkaç kelimeyi bir değişkende saklamak kadar basit görünür. Fakat C, hazır ve bağımsız bir `string` veri türü sunmaz. Bunun yerine metinleri, bellekte art arda bulunan karakterlerden oluşan ve özel bir null karakteriyle sonlandırılan diziler şeklinde işler. Bu yaklaşım hem yüksek performans hem de etkileyici bir kontrol sağlar; ancak sınırlar unutulduğunda programı küçük bir bellek mayın tarlasına çevirebilir.


![c-karakter-dizileri-59](/img/c-karakter-dizileri-59.svg)

``

## C string'inin temel yapısı

Bir C karakter dizisinin her elemanı `char` türündedir. Metnin bittiği yer, sayısal değeri sıfır olan `\0` karakteriyle belirtilir. Örneğin `"Kod"` metni bellekte şu şekilde tutulur:

| İndis | Karakter | Sayısal değer |
|---:|:---:|---:|
| 0 | `K` | 75 |
| 1 | `o` | 111 |
| 2 | `d` | 100 |
| 3 | `\0` | 0 |

Görünen karakter sayısı $n$ ise gereken en düşük bellek miktarı yaklaşık olarak şöyledir:

$$B = (n + 1) \times sizeof(char)$$

C standardında `sizeof(char)` her zaman 1 olduğundan, üç karakterli `"Kod"` için dört baytlık alan gerekir. Fazladan bayt, null karakterinin koltuğudur; görünmez ama yolculuk onsuz tamamlanmaz.

```c
#include <stdio.h>

int main(void) {
    char metin[] = "Kod";

    printf("%s\n", metin);
    printf("Ilk karakter: %c\n", metin[0]);
    printf("Sonlandirici deger: %d\n", metin[3]);
    return 0;
}
```

Derleyici burada dizinin boyutunu otomatik olarak dört seçer ve sona `\0` ekler. `%s`, karakterleri null sonlandırıcıya ulaşıncaya kadar ekrana yazar.

## Dizi mi, işaretçi mi?

Aşağıdaki iki tanım benzer görünse de aynı davranışı garanti etmez:

| Tanım | Veri konumu | Değiştirilebilir mi? |
|---|---|---|
| `char ad[] = "Ada";` | Yazılabilir dizi | Evet |
| `const char *ad = "Ada";` | String sabitini gösterir | Hayır |

```c
char dil[] = "C dili";
dil[0] = 'c';  /* Gecerli: dizi degistirilebilir. */

const char *mesaj = "Merhaba";
/* mesaj[0] = 'm';  Hatali: string sabiti degistirilmemeli. */
```

İkinci kullanımda `const`, yanlışlıkla salt okunur veriyi değiştirmeye çalışmamızı engeller. Yalın `char *mesaj = "Merhaba";` bazı derleyicilerde kabul edilse bile karakterleri değiştirmek tanımsız davranıştır.

## Uzunluk ve kapasite aynı şey değildir

`strlen()` yalnızca `\0` öncesindeki karakterleri sayar. `sizeof()` ise erişilebilen dizi nesnesinin toplam boyutunu verir.

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char kutu[20] = "Merhaba";

    printf("Uzunluk: %zu\n", strlen(kutu)); /* 7 */
    printf("Kapasite: %zu\n", sizeof(kutu)); /* 20 */
    return 0;
}
```

Bu örnekte metin uzunluğu $L=7$, dizinin kapasitesi $C=20$ bayttır. Güvenli bir string için temel koşul $L < C$ olmalıdır; çünkü bir hücre `\0` için ayrılır. İşaretçi bir fonksiyona gönderildiğinde `sizeof()` artık dizinin kapasitesini değil, işaretçinin boyutunu verebilir. Bu nedenle kapasiteyi fonksiyona ayrıca göndermek iyi bir alışkanlıktır.

## Güvenli girdi alma

`scanf("%s", ...)` boşlukta okumayı keser ve sınır belirtilmezse taşmaya yol açabilir. `fgets()` ise kapasiteyi bildiği için daha güvenli bir seçenektir.

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char ad[32];

    printf("Adinizi girin: ");
    if (fgets(ad, sizeof ad, stdin) != NULL) {
        ad[strcspn(ad, "\n")] = '\0';
        printf("Merhaba, %s!\n", ad);
    }
    return 0;
}
```

`fgets()` satır sonunu diziye ekleyebilir. `strcspn()` ilk `\n` karakterinin konumunu bulur ve bu karakter null sonlandırıcıyla değiştirilir.

## Akılda tutulacaklar

C string'leri, null karakteriyle sonlanan `char` dizileridir. Her zaman kapasiteyi hesaba katın, sonlandırıcı için yer bırakın ve sınır kontrollü fonksiyonları tercih edin. `strlen`, `strcmp`, `strchr` ve dikkatli kullanıldığında `snprintf`, metin işlemlerinde güçlü yardımcılarınızdır. C size emniyet kemerini zorla takmaz; fakat kemerin nerede olduğunu bilmek programınızı çöküşlerden korur.
