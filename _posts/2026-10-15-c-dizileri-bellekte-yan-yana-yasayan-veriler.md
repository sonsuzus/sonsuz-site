---
layout: post
title: "C Dizileri: Bellekte Yan Yana Yaşayan Veriler"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - diziler
  - bellek-yönetimi
  - programlama
  - pointer
  - veri-yapıları
toc: true
image: /img/c-dizileri-bellekte-85.png
---

C dilinde çok sayıda aynı tür veriyi ayrı ayrı değişkenlerle yönetmek, her yolcu için ayrı otobüs çağırmaya benzer. Diziler ise tüm yolcuları tek araca bindirir: Veriler ardışık bellek hücrelerinde saklanır, ortak bir adla yönetilir ve indeksler sayesinde hızlıca erişilebilir hâle gelir.

![c-dizileri-bellekte-85](/img/c-dizileri-bellekte-85.svg)

``

## Dizi Nedir?

Dizi, **aynı veri türüne sahip sabit sayıda elemanın** bellekte art arda tutulduğu veri yapısıdır. Beş öğrencinin notlarını saklamak için beş değişken tanımlamak yerine şöyle bir dizi oluşturabiliriz:

```c
int notlar[5] = {78, 85, 92, 64, 90};
```

Burada `notlar` dizinin adı, `int` eleman türü ve `5` kapasitesidir. C dizilerinde indeksler sıfırdan başladığı için ilk eleman `notlar[0]`, son eleman ise `notlar[4]` olur.

| Özellik | Ayrı değişkenler | Dizi |
|---|---|---|
| Tanımlama | `n1`, `n2`, `n3` | `notlar[3]` |
| Döngüyle işleme | Zor | Kolay |
| Bellek düzeni | Ardışık olması garanti değil | Ardışık |
| Eleman erişimi | Değişken adıyla | İndeksle |
| Veri türü | Farklı olabilir | Tamamı aynıdır |

## Bellekte Yerleşim Mantığı

Bir dizinin en önemli özelliği, elemanlarının ardışık adreslerde bulunmasıdır. Dizinin başlangıç adresi $B$, her elemanın boyutu $s$ bayt ise $i$ indeksli elemanın adresi şu formülle hesaplanır:

$$Adres(A[i]) = B + i \times s$$

Örneğin `int` türünün 4 bayt olduğu bir sistemde başlangıç adresi 1000 olan dizinin `A[3]` elemanı şu adrestedir:

$$1000 + 3 \times 4 = 1012$$

Bu doğrudan hesaplama sayesinde herhangi bir elemana erişim sabit zamanda gerçekleşir: $O(1)$. Bilgisayarın önceki elemanları tek tek gezmesi gerekmez.

```c
#include <stdio.h>

int main(void) {
    int sayilar[4] = {10, 20, 30, 40};

    for (int i = 0; i < 4; i++) {
        printf("sayilar[%d] = %d, adres = %p\n",
               i, sayilar[i], (void *)&sayilar[i]);
    }

    return 0;
}
```

Bu program her elemanın değerini ve adresini gösterir. Çıktıdaki adres farklarının genellikle `sizeof(int)` kadar olduğunu görebilirsiniz. Böylece ardışık yerleşim yalnızca teori olmaktan çıkar, terminalde görünür hâle gelir.

## Dizi Adı ve Pointer İlişkisi

Çoğu ifadede dizi adı, ilk elemanın adresine dönüşür. Bu nedenle `sayilar` ile `&sayilar[0]` aynı başlangıç konumunu gösterir. İndeksleme de pointer aritmetiğiyle yakından ilişkilidir:

$$A[i] \equiv *(A + i)$$

```c
int degerler[] = {5, 10, 15};
printf("%d\n", degerler[1]);
printf("%d\n", *(degerler + 1));
```

İki satır da `10` yazdırır. Ancak dizi ve pointer tamamen aynı kavram değildir. Dizi için ayrılmış alan sabittir; dizi adına yeni bir adres atanamaz. Pointer ise farklı adresleri gösterebilen ayrı bir değişkendir.

## Dizileri Döngülerle Yönetmek

Dizilerin asıl gücü döngülerle ortaya çıkar. Aşağıdaki kod, notların toplamını ve ortalamasını hesaplar:

```c
#include <stdio.h>

int main(void) {
    int notlar[] = {78, 85, 92, 64, 90};
    int adet = sizeof(notlar) / sizeof(notlar[0]);
    int toplam = 0;

    for (int i = 0; i < adet; i++) {
        toplam += notlar[i];
    }

    double ortalama = (double) toplam / adet;
    printf("Ortalama: %.2f\n", ortalama);
    return 0;
}
```

`sizeof(notlar) / sizeof(notlar[0])` ifadesi toplam dizi boyutunu tek elemanın boyutuna bölerek eleman sayısını bulur. Bu yöntem yalnızca gerçek dizi aynı kapsamdayken güvenilirdir; fonksiyona aktarılan dizi parametresi pointer gibi davranır.

## Sınırların Dışına Çıkma Tehlikesi

C, indeksleri otomatik olarak denetlemez. Beş elemanlı bir dizide `notlar[5]` kullanmak tanımsız davranıştır. Program çökebilir, yanlış sonuç üretebilir veya çalışıyor gibi görünebilir. En sinsi ihtimal de sonuncusudur!

Bu nedenle döngü koşullarında `i < adet` tercih edilmeli, `i <= adet` hatasından kaçınılmalıdır. Diziler hızlı ve verimlidir; fakat güvenlik kemerini programcı takar.
