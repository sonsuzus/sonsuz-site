---
layout: post
title: "Ring 0'dan Ring 3'e: Kullanıcı Modu ve Çekirdek Modu Arasındaki Duvar"
math: true
categories: 
  - Bilgi
tags: 
  - işletim sistemi
  - çekirdek
  - işlemci mimarisi
  - güvenlik
  - x86
  - sistem programlama
toc: true
image: /img/ring-0dan-ring-41.png
---

Bir müzik uygulamasının yanlışlıkla diskin tamamını silmesini veya sıradan bir oyunun klavye sürücüsünü yeniden programlamasını istemeyiz. İşletim sistemleri bu felaketleri yalnızca yazılım kurallarıyla değil, işlemcinin uyguladığı **ayrıcalık seviyeleriyle** engeller. x86 mimarisinde bunlar Ring 0 ile Ring 3 arasında numaralandırılan güvenlik halkalarıdır: Sayı küçüldükçe yetki büyür, sorumluluk ağırlaşır.
``

## Halkaların temel mantığı

İşlemci, çalışan kodun hangi ayrıcalık seviyesinde olduğunu takip eder. x86 terminolojisinde mevcut seviye **CPL** (Current Privilege Level) olarak adlandırılır. Kaynakların ve kod bölümlerinin erişim seviyesi ise **DPL** (Descriptor Privilege Level) gibi alanlarla belirtilir.

Basitleştirilmiş erişim düşüncesi şu eşitsizlikle anlatılabilir:

$$
P_{etkin} \leq P_{gerekli}
$$

Burada küçük sayı daha yüksek yetkiyi temsil eder. Dolayısıyla Ring 0 kodu pek çok ayrıcalıklı kaynağa ulaşabilirken Ring 3 kodu aynı işlemi yapmaya çalıştığında işlemci bir koruma hatası üretir.

| Halka | Tipik kullanım | Yetki düzeyi | Modern sistemlerde durum |
|---|---|---:|---|
| Ring 0 | Çekirdek ve temel sürücüler | En yüksek | Yoğun biçimde kullanılır |
| Ring 1 | Yardımcı sistem servisleri | Yüksek | Genellikle kullanılmaz |
| Ring 2 | Bazı sürücüler | Orta | Genellikle kullanılmaz |
| Ring 3 | Tarayıcı, oyun, editör | En düşük | Kullanıcı uygulamalarının evidir |

Linux, Windows ve çoğu genel amaçlı işletim sistemi pratikte iki seviyeli bir model kullanır: çekirdek Ring 0'da, uygulamalar Ring 3'te çalışır. Ring 1 ve Ring 2 donanımda bulunsa da taşınabilirlik ve tasarım sadeliği nedeniyle çoğunlukla boş bırakılır.

## Duvar işlemci seviyesinde nasıl kurulur?

Duvarın ilk tuğlası **ayrıcalıklı komutlardır**. Kesme sistemini kapatan `cli`, kontrol yazmaçlarını değiştiren talimatlar veya sayfa tablolarını yöneten işlemler Ring 3'te yürütülemez. Bir uygulama bunları denerse CPU işlemi reddeder ve çekirdeğe bir istisna bildirir.

İkinci tuğla **bellek korumasıdır**. Sanal bellekteki her sayfa için sayfa tablosu girdileri bulunur. x86 mimarisindeki U/S biti, sayfanın kullanıcı modundan erişilebilir olup olmadığını belirtir:

| U/S biti | Ring 3 erişimi | Ring 0 erişimi |
|---:|---|---|
| 0 | Yasak | İzinli |
| 1 | İzinlere bağlı | İzinlere bağlı |

Buna yazılabilirlik ve çalıştırılabilirlik bitleri de eklenir. Böylece bir süreç başka bir sürecin ya da çekirdeğin belleğine yalnızca adresini tahmin ederek ulaşamaz.

## Uygulamalar hizmeti nasıl ister?

Ring 3 tamamen çaresiz değildir; çekirdekten kontrollü biçimde yardım ister. Bunun kapısı **sistem çağrısıdır**. x86-64 sistemlerinde `syscall` komutu işlemciyi önceden belirlenmiş çekirdek giriş noktasına taşır, ayrıcalık seviyesini değiştirir ve kullanıcı bağlamının geri yüklenebilmesi için gerekli bilgileri saklar.

```c
#include <unistd.h>

int main(void) {
    const char mesaj[] = "Merhaba, cekirdek!\n";
    write(1, mesaj, sizeof(mesaj) - 1);
    return 0;
}
```

Buradaki `write`, ekrana doğrudan erişmez. Standart kütüphane uygun sistem çağrısını başlatır; çekirdek dosya tanımlayıcısını ve kullanıcı belleğindeki adresi doğrular. İstek güvenliyse terminal sürücüsüne kadar uzanan işi çekirdek gerçekleştirir.

Geçişin maliyeti kabaca şöyle düşünülebilir:

$$
T_{toplam} = T_{geçiş} + T_{doğrulama} + T_{işlem} + T_{dönüş}
$$

Bu nedenle her küçük işlem için sistem çağrısı yapmak yerine tamponlama kullanılır. Örneğin yüzlerce karakter tek tek değil, bir blok hâlinde yazılabilir.

## Kesintiler, hatalar ve kontrollü dönüş

Donanım kesintileri ve sayfa hataları da kontrolü çekirdeğe aktarabilir. İşlemci, **IDT** içindeki hedef kapının yetki kurallarını denetler; rastgele bir adrese sıçramaz. Çekirdek olayı işledikten sonra özel dönüş talimatlarıyla Ring 3 bağlamını geri yükler.

Sonuç olarak kullanıcı modu ile çekirdek modu arasındaki duvar basit bir programlama geleneği değildir. Ayrıcalıklı komutlar, sayfa tabloları, kesme kapıları ve sistem çağrısı mekanizması birlikte çalışır. Uygulama kontrolden çıksa bile işlemci ona nazikçe ama kesin biçimde şunu söyler: Donanıma dokunmak istiyorsan önce çekirdekten izin al.

![ring-0dan-ring-41](/img/ring-0dan-ring-41.svg)

