---
layout: post
title: "RISC-V: Açık İşlemci Mimarisinin Sessiz Devrimi"
math: true
categories: 
  - Bilgi
tags: 
  - risc-v
  - işlemci
  - açık kaynak
  - donanım
  - assembly
  - bilgisayar mimarisi
toc: true
---

Bir işlemcinin hangi komutları anlayacağını hiç merak ettiniz mi? Yazılım ile silikon arasındaki bu sözleşme, komut kümesi mimarisi yani ISA olarak adlandırılır. RISC-V, herkesin inceleyebildiği ve lisans ücreti ödemeden kullanabildiği açık bir ISA sunarak işlemci dünyasındaki yerleşik düzeni değiştiriyor. Üniversite laboratuvarından veri merkezlerine uzanan bu yükseliş, yalnızca teknik değil, ekonomik bir dönüşümü de temsil ediyor.

``

## ISA ile işlemci tasarımı aynı şey değildir

RISC-V çoğu zaman açık kaynaklı işlemci şeklinde tanıtılsa da önemli bir ayrım vardır: RISC-V doğrudan bir işlemci devresi değil, işlemcinin uyması gereken komut sözleşmesidir. Tasarımcılar bu sözleşmeyi kullanarak basit mikrodenetleyiciler, yüksek performanslı çekirdekler veya özel yapay zekâ hızlandırıcıları geliştirebilir.

Bir ISA; yazmaçları, veri türlerini, komut biçimlerini ve komutların davranışlarını tanımlar. Mikro mimari ise bu komutların boru hattı, önbellek ve yürütme birimleriyle fiziksel olarak nasıl gerçekleştirileceğini belirler. Aynı RISC-V programı, birbirinden tamamen farklı iki işlemci tasarımında çalışabilir.

| Kavram | Tanımladığı şey | RISC-V örneği |
|---|---|---|
| ISA | Yazılım-donanım sözleşmesi | `ADD`, `LOAD`, `JAL` komutları |
| Mikro mimari | Komutların uygulanma yöntemi | Beş aşamalı boru hattı |
| Çekirdek | Gerçekleştirilmiş işlemci tasarımı | Rocket, BOOM, CVA6 |
| Yonga | Çekirdek ve çevre birimlerinin bütünü | Bellek, UART ve zamanlayıcı içeren SoC |

## RISC yaklaşımının matematiği

RISC, yani azaltılmış komut kümesi yaklaşımı, az sayıda ve düzenli komutla karmaşık işleri gerçekleştirmeyi hedefler. İşlemci performansı kabaca şu denklemle ifade edilebilir:

$$T = N \times CPI \times t$$

Burada $N$ çalıştırılan komut sayısı, $CPI$ komut başına ortalama saat çevrimi ve $t$ bir saat çevriminin süresidir. Daha karmaşık bir komut $N$ değerini azaltabilir; fakat devreyi zorlaştırarak $CPI$ veya $t$ değerini büyütebilir. RISC-V, düzenli komut biçimleri sayesinde kod çözücülerin sadeleşmesine ve yüksek frekanslı tasarımların kolaylaşmasına yardımcı olur.

| Özellik | RISC-V | Geleneksel kapalı ISA |
|---|---|---|
| Lisanslama | ISA ücretsiz ve açık | Genellikle ücretli veya kısıtlı |
| Özelleştirme | Özel komut eklenebilir | Üretici izni gerekebilir |
| Temel yapı | Küçük ve modüler | Tarihsel olarak daha karmaşık olabilir |
| Ekosistem | Hızla gelişiyor | Genellikle daha olgun |

## Modüler komut kümeleri

RISC-V’nin gücü, her işlemciye bütün özellikleri zorla yüklememesidir. `RV32I`, 32 bitlik temel tamsayı komutlarını içerir. `M` çarpma ve bölme, `A` atomik işlemler, `F` kayan nokta, `V` ise vektör işlemleri ekler. Böylece küçük bir sensör gereksiz kayan nokta devreleri taşımazken güçlü bir sunucu ihtiyaç duyduğu uzantıları kullanabilir.

Aşağıdaki RISC-V assembly kodu, 1’den 10’a kadar olan sayıları toplar:

```asm
    li   t0, 1          # Sayaç: 1
    li   t1, 10         # Üst sınır
    li   t2, 0          # Toplam
loop:
    add  t2, t2, t0     # Toplama ekle
    addi t0, t0, 1      # Sayacı artır
    ble  t0, t1, loop   # Sınır aşılmadıysa dön
```

Kodda işlemler küçük ve belirgindir: veri yazmaca yüklenir, toplama yapılır ve dallanma kararı ayrı bir komutla verilir. Bu düzenlilik hem derleyicilerin hem de donanım tasarımcılarının işini kolaylaştırır.

## Neden şimdi yükseliyor?

RISC-V’nin yükselişinde lisans maliyetleri, tedarik bağımsızlığı ve özel hızlandırıcılara duyulan ihtiyaç etkili oldu. Şirketler kendi komutlarını ekleyebilir, araştırmacılar mimariyi deneyebilir ve öğrenciler gerçekçi çekirdekler tasarlayabilir. GCC, LLVM ve Linux desteği de yazılım tarafındaki engelleri giderek azaltıyor.

Yine de açık ISA, her uygulamanın otomatik olarak açık kaynaklı olduğu anlamına gelmez. Bir şirket RISC-V uyumlu fakat kapalı bir çekirdek üretebilir. Ayrıca güçlü hata ayıklama araçları, sürücüler ve optimize kütüphaneler hâlâ kritik önemdedir. Kısacası RISC-V sihirli bir değnek değil; işlemci tasarımına katılım eşiğini düşüren güçlü, ortak ve büyüyen bir dildir.
