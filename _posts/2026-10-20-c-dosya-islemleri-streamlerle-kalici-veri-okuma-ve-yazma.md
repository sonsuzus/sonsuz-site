---
layout: post
title: "C Dosya İşlemleri: Stream’lerle Kalıcı Veri Okuma ve Yazma"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - dosya işlemleri
  - file io
  - stream
  - stdio
  - programlama
toc: true
image: /img/c-dosya-islemleri-83.png
---

Bir C programı çalışırken değişkenler çoğunlukla RAM’de yaşar ve program sonlandığında sahneden sessizce çekilir. Oysa kullanıcı kayıtları, ayarlar veya ölçüm sonuçları gibi verilerin yeniden kullanılabilmesi için diske yazılması gerekir. C’nin File I/O araçları, geçici bellek ile kalıcı depolama arasında bir köprü kurar.

``

## Stream mantığı nedir?

C, dosya ve aygıtlarla iletişimi **stream**, yani veri akışı soyutlaması üzerinden gerçekleştirir. Program açısından stream, sırayla okunabilen veya yazılabilen karakter ve bayt dizisidir. Bunun arkasında SSD, terminal ya da başka bir aygıt bulunabilir; temel işlemler büyük ölçüde aynı kalır.

`<stdio.h>` kütüphanesindeki `FILE` yapısı bir stream’i temsil eder. Bu yapı dosyanın konumu, erişim modu, tampon bilgisi ve hata durumu gibi ayrıntıları yönetir. Genellikle yapının iç alanlarına doğrudan dokunulmaz; onun yerine `fopen`, `fclose`, `fprintf` ve `fread` gibi fonksiyonlar kullanılır.

Bir dosyanın toplam boyutu kabaca

$$S = n \times b$$

ile düşünülebilir. Burada $n$ kayıt sayısını, $b$ ise her kaydın bayt cinsinden ortalama boyutunu gösterir. Metin dosyalarında karakter kodlaması ve ayraçlar nedeniyle gerçek boyut değişebilir.

C programları açıldığında üç standart stream hazırdır:

| Stream | Görevi | Varsayılan aygıt |
|---|---|---|
| `stdin` | Veri okumak | Klavye |
| `stdout` | Normal çıktı yazmak | Terminal |
| `stderr` | Hata mesajı yazmak | Terminal |

## Dosya açma modları

Dosya işlemi, `fopen` ile bir stream açarak başlar. Fonksiyon başarısız olursa `NULL` döndürür; bu kontrolü atlamak, programı hata festivaline dönüştürebilir.

| Mod | Anlamı | Dosya yoksa | Mevcut içerik |
|---|---|---|---|
| `r` | Okuma | Hata | Korunur |
| `w` | Yazma | Oluşturulur | Silinir |
| `a` | Sona ekleme | Oluşturulur | Korunur |
| `r+` | Okuma ve yazma | Hata | Korunur |
| `w+` | Okuma ve yazma | Oluşturulur | Silinir |
| `a+` | Okuma ve sona ekleme | Oluşturulur | Korunur |

İkili dosyalarda moda `b` eklenebilir: `rb`, `wb` veya `ab` gibi.

## Metin dosyasına yazma ve okuma

Aşağıdaki örnek, bir puanı dosyaya yazar ve ardından geri okur:

```c
#include <stdio.h>

int main(void) {
    FILE *dosya = fopen("puan.txt", "w");

    if (dosya == NULL) {
        perror("Dosya acilamadi");
        return 1;
    }

    fprintf(dosya, "%s %d\n", "Ada", 95);
    fclose(dosya);

    dosya = fopen("puan.txt", "r");
    if (dosya == NULL) {
        perror("Dosya okunamadi");
        return 1;
    }

    char isim[32];
    int puan;

    if (fscanf(dosya, "%31s %d", isim, &puan) == 2) {
        printf("Ogrenci: %s, puan: %d\n", isim, puan);
    }

    fclose(dosya);
    return 0;
}
```

`fprintf`, biçimlendirilmiş veriyi stream’e gönderir. `fscanf` ise veriyi belirtilen formata göre ayrıştırır. `%31s` sınırı, 32 elemanlı dizide taşmayı önlemek için en fazla 31 karakter okur. Her açılan dosyanın `fclose` ile kapatılması tamponlanmış verilerin diske aktarılmasını ve sistem kaynaklarının serbest bırakılmasını sağlar.

## Metin mi, ikili dosya mı?

| Özellik | Metin dosyası | İkili dosya |
|---|---|---|
| Okunabilirlik | İnsan tarafından kolay okunur | Özel araç gerekebilir |
| Boyut | Genellikle daha büyük | Genellikle daha küçük |
| Taşınabilirlik | Yüksek | Veri tiplerine bağlı |
| Fonksiyonlar | `fprintf`, `fgets` | `fwrite`, `fread` |

İkili yazmada temel denklem aktarılan bayt miktarı için $B = adet \times sizeof(tür)$ biçimindedir. Örneğin `fwrite(dizi, sizeof(int), 10, dosya)` on tamsayıyı yazar.

Son olarak `feof` akış sonunu, `ferror` ise okuma veya yazma hatasını denetler. Sağlam bir File I/O kodu yalnızca mutlu senaryoyu değil; eksik dosyayı, bozuk veriyi ve başarısız yazmayı da hesaba katar. Böylece veriler program kapandığında buharlaşmak yerine diskte güvenle yaşamaya devam eder.

![c-dosya-islemleri-83](/img/c-dosya-islemleri-83.svg)

