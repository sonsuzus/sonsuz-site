---
layout: post
title: "C Temelleri: Tarihten Derleme Modeline Sistem Programlamanın Alfabesi"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - programlama
  - derleyici
  - algoritma
  - sistem programlama
toc: true
image: /img/c-temelleri-tarihten-76.png
---

C, işletim sistemlerinden gömülü cihazlara kadar sayısız teknolojinin görünmeyen motorudur. Sözdizimi ilk bakışta sade görünse de bellek, işlemci ve program arasındaki ilişkiyi doğrudan hissettirmesi onu öğretici ve güçlü kılar. C öğrenmek yalnızca yeni bir dil öğrenmek değil, bilgisayarın perde arkasına küçük ama oldukça aydınlatıcı bir pencere açmaktır.
``
## Kısa Bir Tarih Yolculuğu

C'nin hikâyesi 1970'lerin başında Bell Laboratuvarları'nda başladı. Dennis Ritchie, Ken Thompson'ın geliştirdiği B dilinden esinlenerek daha güçlü ve taşınabilir bir dil tasarladı. Temel amaç, Unix işletim sistemini donanıma bağımlı Assembly kodları yerine daha üst seviyeli bir dille geliştirmekti.

Bu tercih büyük bir dönüşüm yarattı: Unix farklı bilgisayarlara daha kolay taşınırken C de sistem programlamanın ortak dili hâline geldi. Brian Kernighan ve Dennis Ritchie'nin 1978'de yayımladığı kitap, dilin ilk yaygın başvuru kaynağı oldu. Ardından ANSI C ya da C89 standardı geldi; C99, C11, C17 ve C23 sürümleri ise dili modern ihtiyaçlara göre geliştirdi.

| Dönem | Gelişme | Önemi |
|---|---|---|
| 1972 | C'nin ilk sürümü | Unix geliştirmede kullanıldı |
| 1978 | K&R kitabı | Dilin fiilî tanımı yayıldı |
| 1989 | ANSI C (C89) | Taşınabilir bir standart oluştu |
| 1999 | C99 | Yeni veri türleri ve sözdizimi eklendi |
| 2011–2023 | C11, C17, C23 | Güvenlik ve modernleştirme çalışmaları yapıldı |

![c-temelleri-tarihten-76](/img/c-temelleri-tarihten-76.svg)


## Bir C Programının Anatomisi

C programları fonksiyonlardan oluşur ve yürütme genellikle `main` fonksiyonundan başlar. Kütüphaneler başlık dosyalarıyla programa tanıtılır. Değişkenler veriyi, ifadeler hesaplamayı, kontrol yapıları ise programın kararlarını temsil eder.

```c
#include <stdio.h>

int kare(int sayi) {
    return sayi * sayi;
}

int main(void) {
    int deger = 6;
    int sonuc = kare(deger);

    printf("%d sayısının karesi: %d\n", deger, sonuc);
    return 0;
}
```

Burada `#include <stdio.h>` standart giriş-çıkış araçlarını bildirir. `kare` fonksiyonu aldığı tam sayıyı kendisiyle çarpar. Matematiksel olarak işlem

$$f(x)=x^2$$

şeklinde gösterilebilir. `main`, değişkenleri oluşturur, fonksiyonu çağırır ve sonucu `printf` ile ekrana yazar. `return 0` ifadesi de programın başarıyla tamamlandığını işletim sistemine bildirir.

C'de tür bilgisi önemlidir. Örneğin `int` tam sayıları, `char` karakterleri, `float` ve `double` ondalıklı değerleri saklar. Bir dizinin bellekte kapladığı yaklaşık alan şu ilişkiyle düşünülebilir:

$$Bellek = Eleman\ Sayısı \times sizeof(Tür)$$

Bu nedenle C, programcıya hem güç hem de sorumluluk verir; yanlış sınır kullanımı bellek hatalarına yol açabilir.

## Kaynak Kod Nasıl Çalışan Programa Dönüşür?

C çoğunlukla derlenen bir dildir. Yazdığımız kaynak kod işlemci tarafından doğrudan anlaşılmaz. Dönüşüm zinciri genel olarak şöyledir:

$$Kaynak \rightarrow Ön\ İşleme \rightarrow Derleme \rightarrow Assembly \rightarrow Nesne\ Dosyası \rightarrow Bağlama$$

| Aşama | Görevi | Tipik çıktı |
|---|---|---|
| Ön işleme | `#include` ve makroları işler | Genişletilmiş kaynak |
| Derleme | C kodunu düşük seviyeli yapıya çevirir | Assembly kodu |
| Assembler | Assembly komutlarını makine koduna dönüştürür | Nesne dosyası |
| Bağlama | Kütüphane ve nesne dosyalarını birleştirir | Çalıştırılabilir dosya |

GCC ile örnek program şöyle derlenebilir:

```bash
gcc -Wall -Wextra -std=c17 program.c -o program
./program
```

`-Wall` ve `-Wextra`, olası sorunlar hakkında uyarılar üretir; `-std=c17` kullanılacak standardı seçer. Uyarıları görmezden gelmemek, C dünyasında emniyet kemeri takmaya benzer: Program yine ilerleyebilir ama ilk sert virajda farkı anlarsınız.

C'nin kalıcı etkisi; küçük çalışma zamanı, donanıma yakınlık, taşınabilirlik ve öngörülebilir performanstan gelir. Değişkenler, fonksiyonlar, koşullar ve döngüler temeli oluştururken derleme modelini anlamak hataları çözmeyi kolaylaştırır. Kısacası C, bilgisayara yalnızca ne yapacağını değil, bunu kaynakları nasıl kullanarak yapacağını da anlatmayı öğretir.
