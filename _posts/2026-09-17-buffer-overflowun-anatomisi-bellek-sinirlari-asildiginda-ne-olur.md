---
layout: post
title: "Buffer Overflow’un Anatomisi: Bellek Sınırları Aşıldığında Ne Olur?"
math: true
categories: 
  - Bilgi
tags: 
  - buffer overflow
  - bellek güvenliği
  - c programlama
  - siber güvenlik
  - stack
  - güvenli kodlama
toc: true
---

Bir programa “Şu kutuya en fazla 16 bayt koyabilirsin” dediğimizi, ardından 40 bayt veri gönderdiğimizi düşünelim. Güvenli bir dil taşan kısmı reddedebilir; C veya C++ gibi düşük seviyeli dillerdeyse veri komşu bellek alanlarına doğru ilerleyebilir. İşte **buffer overflow**, yani tampon taşması, ayrılan bellek sınırlarının dışına veri yazılmasıdır. Sonuç basit bir çökmeden program akışının değiştirilmesine kadar uzanabilir.
``

## Tampon ve sınır kavramı

Buffer, veriyi geçici olarak saklayan ardışık bir bellek bölgesidir. Başlangıç adresi $A$, kapasitesi $N$ bayt olan bir tamponun geçerli adresleri şu aralıktadır:

$$A \leq adres < A + N$$

Programa $L$ bayt veri yazdırılırsa taşan miktar kabaca şöyle ifade edilir:

$$T = \max(0, L-N)$$

Örneğin 8 baytlık alana 13 bayt yazılırsa $T=5$ bayt komşu alanlara taşar. Bellek bunu “Bu veri yanlış yerde!” diyerek otomatik olarak durdurmaz; işlemci çoğunlukla yalnızca verilen adrese yazma talimatını uygular. Kontrol sorumluluğu dile, derleyiciye ve geliştiriciye kalır.

| Durum | Yazılan veri | Olası sonuç |
|---|---:|---|
| Sınır içinde | $L \leq N$ | Normal çalışma |
| Küçük taşma | $L > N$ | Komşu değişkenlerin bozulması |
| Kritik taşma | Çok daha büyük $L$ | Çökme veya kontrol akışının değişmesi |
| Koruma etkin | Sınır ihlali algılanır | Program kontrollü biçimde sonlandırılır |

## Stack üzerinde neler yaşanır?

Fonksiyon çağrıldığında yerel değişkenler, bazı kayıt değerleri ve dönüş bilgileri çoğunlukla **stack frame** içinde bulunur. Küçük bir karakter dizisinin yanına başka bir değişken veya dönüş adresi yerleşebilir. Tampon sınırı aşılırsa taşan baytlar bunları bozabilir.

Basitleştirilmiş görünüm şöyledir:

```text
Yüksek adresler
+------------------+
| Dönüş bilgisi    |
+------------------+
| Diğer değişkenler|
+------------------+
| char buffer[8]   |
+------------------+
Düşük adresler
```

Gerçek yerleşim; mimariye, derleyiciye, optimizasyona ve işletim sistemine göre değişir. Bu nedenle taşma davranışı C standardında **tanımsız davranış** sayılır: Program çökebilir, görünürde düzgün çalışabilir veya beklenmedik sonuç üretebilir.

## Küçük bir C örneği

Aşağıdaki kod, `strcpy` kaynak uzunluğunu denetlemediği için tehlikelidir. Örnek saldırı üretmek için değil, hatanın kaynağını göstermek içindir:

```c
#include <stdio.h>
#include <string.h>

void mesaj_yaz(const char *girdi) {
    char tampon[8];
    strcpy(tampon, girdi); // Uzunluk kontrolü yok!
    printf("Mesaj: %s\n", tampon);
}
```

Daha güvenli yaklaşım, hedef kapasitesini açıkça hesaba katmaktır:

```c
#include <stdio.h>

void mesaj_yaz(const char *girdi) {
    char tampon[8];
    snprintf(tampon, sizeof tampon, "%s", girdi);
    printf("Mesaj: %s\n", tampon);
}
```

`snprintf`, en fazla tampon kapasitesi kadar çıktı üretir ve sonlandırıcı `\0` karakteri için yer ayırır. Veri kesilebilir; bu yüzden kesilmenin uygulama mantığı açısından ayrıca kontrol edilmesi gerekir.

## Her taşma aynı değildir

| Tür | Bölge | Tipik risk |
|---|---|---|
| Stack overflow | Fonksiyon yığını | Yerel veri ve dönüş bilgilerinin bozulması |
| Heap overflow | Dinamik bellek | Başka nesnelerin veya ayırıcı bilgilerinin bozulması |
| Off-by-one | Sınırın bir bayt aşılması | Sonlandırıcı ya da bayrak değerinin değişmesi |
| Integer kaynaklı taşma | Boyut hesabı | Gereğinden küçük buffer ayrılması |

## Savunma katmanları

Modern sistemler tek bir önleme güvenmez. **Stack canary**, dönüş bilgisine ulaşılmadan önce değişip değişmediği kontrol edilen bekçi değeridir. **ASLR**, bellek adreslerini rastgeleleştirir. **DEP/NX**, veri bölgelerinin kod gibi çalıştırılmasını zorlaştırır. Derleyicilerin sınır denetimleri ve AddressSanitizer gibi araçlar da hataları geliştirme sırasında görünür kılar.

Yine de en güçlü savunma, doğru boyut hesaplamak, kullanıcı girdisini doğrulamak, güvensiz fonksiyonlardan kaçınmak ve mümkün olduğunda Rust, Java veya C# gibi bellek güvenliği sağlayan dilleri tercih etmektir. Kısacası buffer overflow, “birkaç fazla karakter” değil; bellek düzeni ile program kontrolünün birbirine ne kadar yakın olduğunun çarpıcı bir hatırlatıcısıdır.
