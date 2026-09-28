---
layout: post
title: "Buffer Overflow Savunmaları: Stack Canary ve ASLR Nasıl Çalışır, Nasıl Zorlanır?"
math: true
categories: 
  - Bilgi
tags: 
  - buffer-overflow
  - stack-canary
  - aslr
  - bellek-güvenliği
  - siber-güvenlik
  - c-programlama
toc: true
image: /img/buffer-overflow-savunmalari-37.png
---

Bellek taşırma açıkları, bir programın ayırdığı alanın dışına veri yazılmasıyla ortaya çıkar. Sonuç bazen masum bir çökme, bazen de program akışının saldırgan tarafından yönlendirilmesidir. Modern derleyiciler ve işletim sistemleri bu riski azaltmak için Stack Canary, ASLR, NX ve PIE gibi katmanlar kullanır. Ancak hiçbir katman tek başına sihirli kalkan değildir; asıl güç, savunmaların birlikte çalışmasından gelir.

``

## Taşma neden program akışını etkiler?

C gibi bellek yönetimini geliştiriciye bırakan dillerde diziler genellikle sınır kontrolü yapmaz. Yığında bir tampon ile dönüş adresi birbirine yakınsa, fazla veri komşu alanları bozabilir:

```c
#include <stdio.h>
#include <string.h>

void mesaj(const char *girdi) {
    char tampon[16];
    strcpy(tampon, girdi); // Uzunluk denetimi yapmaz.
    printf("%s\n", tampon);
}
```

Bu örnek yalnızca hatanın kaynağını gösterir; gerçek sistemlerde kullanılmamalıdır. Güvenli yaklaşım, hedef boyutunu dikkate alan işlevler kullanmak ve girdiyi doğrulamaktır.

Taşmanın temel koşulu şöyle ifade edilebilir:

$$L_{girdi} > C_{tampon}$$

Burada $L_{girdi}$ giriş uzunluğu, $C_{tampon}$ ise tampon kapasitesidir. Fakat taşmanın güvenlik açığına dönüşmesi; bellek düzenine, derleyici seçeneklerine ve etkin korumalara bağlıdır.

## Stack Canary: Madendeki dijital kanarya

Stack Canary, yerel değişkenlerle kritik kontrol verileri arasına yerleştirilen rastgele bir değerdir. Fonksiyon sona ererken bu değer kontrol edilir. Değişmişse program, dönüş adresini kullanmadan sonlandırılır.

$$C_{başlangıç} \neq C_{çıkış} \Rightarrow \text{programı durdur}$$

Derleyici desteği GCC ve Clang üzerinde şu şekilde etkinleştirilebilir:

```bash
gcc -O2 -fstack-protector-strong -D_FORTIFY_SOURCE=3 \
    -fPIE -pie -Wl,-z,relro,-z,now program.c -o program
```

Bu komut güçlü canary denetimi, bazı standart kütüphane sınır kontrolleri, PIE ve RELRO korumaları ekler. Yine de kaynak koddaki hatayı düzeltmez; yalnızca sömürülmesini zorlaştırır.

## ASLR: Adresleri sürekli karıştırmak

ASLR, yığın, heap, kütüphaneler ve uygun şekilde derlenmiş çalıştırılabilir dosyanın adreslerini her çalıştırmada değiştirir. Bir saldırganın belirli bir adresi önceden bilme olasılığı yaklaşık olarak

$$P = \frac{1}{2^H}$$

şeklinde düşünülebilir. $H$, etkili rastgelelik entropisidir. Entropi arttıkça kör tahmin zorlaşır.

| Koruma | Temel amaç | Tek başına sınırlılığı |
|---|---|---|
| Canary | Yığın üzerindeki bozulmayı fark etmek | Gizli değer sızarsa etkisi azalır |
| ASLR | Adresleri öngörülemez yapmak | Adres sızıntıları belirsizliği azaltır |
| NX/DEP | Veri bölgelerinden kod çalıştırmayı engellemek | Mevcut kodun yeniden kullanılması mümkündür |
| PIE | Ana programı da rastgele konumlandırmak | ASLR ve yeterli entropi gerektirir |
| RELRO | Dinamik bağlama yapılarını korumak | Bellek hatasının kendisini gidermez |

![buffer-overflow-savunmalari-37](/img/buffer-overflow-savunmalari-37.svg)


## İleri teknikler korumaları nasıl zorlar?

Canary genellikle doğrudan tahmin edilmez. İleri saldırılar önce bir **bilgi sızıntısı** arayarak süreç belleğindeki canary veya adresleri öğrenmeye çalışır. Format-string hataları, sınır dışı okumalar ve başlatılmamış bellek kullanımı bu nedenle en az yazma hataları kadar tehlikelidir.

ASLR karşısında da temel fikir adres tahmin etmek yerine bir sızıntıyla modül taban adresini belirlemektir. Sonrasında saldırganlar, NX nedeniyle yeni kod çalıştırmak yerine programda zaten bulunan küçük komut dizilerini birleştiren ROP benzeri kod-yeniden-kullanım tekniklerine yönelebilir. Kısmi adres üzerine yazma ve düşük entropili ortamlarda tekrarlı denemeler de teorik zayıflıklardır. Bunlar sürüm, mimari ve süreç modeli gibi ayrıntılara bağımlıdır; dolayısıyla evrensel bir “koruma kapatma düğmesi” yoktur.

| Saldırı fikri | Hedeflenen varsayım | Savunma yaklaşımı |
|---|---|---|
| Bilgi sızıntısı | Gizli değerler okunamaz | Okuma sınırlarını ve biçim dizelerini denetlemek |
| Kod yeniden kullanımı | NX tek başına yeterlidir | CFI, CET ve gölge yığın kullanmak |
| Tekrarlı tahmin | Süreçler bağımsız ve entropi yüksektir | Hız sınırlama, yeniden rastgeleleştirme, izleme |

## Sonuç: Katmanlı savunma kazandırır

En sağlam çözüm, bellek hatasını kaynağında kaldırmaktır. Rust gibi bellek güvenli diller, statik analiz, fuzzing, AddressSanitizer testleri ve güncel derleyici sertleştirmeleri birlikte kullanılmalıdır. Canary alarm sistemi, ASLR sis perdesidir; fakat kapıyı gerçekten kilitleyen şey güvenli kod, en az ayrıcalık ve katmanlı mimaridir.
