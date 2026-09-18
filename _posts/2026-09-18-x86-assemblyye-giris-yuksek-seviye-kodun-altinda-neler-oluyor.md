---
layout: post
title: "x86 Assembly’ye Giriş: Yüksek Seviye Kodun Altında Neler Oluyor?"
math: true
categories: 
  - Bilgi
tags: 
  - x86
  - assembly
  - işlemci
  - derleyici
  - bellek
  - düşük-seviye-programlama
toc: true
---

Python, C veya JavaScript ile bir değişkeni artırmak tek satırlık iştir. Fakat işlemci; değişkenleri, döngüleri ya da fonksiyonları bizim anladığımız biçimde tanımaz. Onun dünyasında yazmaçlar, bellek adresleri ve son derece küçük komutlar vardır. x86 assembly öğrenmek, bilgisayarla onun ana diline yakın bir seviyede konuşmak ve yüksek seviye kodun perde arkasını görmek demektir.

``

## Assembly nedir?

Assembly, makine kodunun insanlar tarafından okunabilir sembolik gösterimidir. İşlemcinin çalıştırdığı gerçek komutlar bitlerden oluşur; assembly ise bu bitlere `mov`, `add` ve `jmp` gibi isimler verir.

Örneğin aşağıdaki C ifadesini düşünelim:

```c
int sonuc = a + b;
```

İşlemci doğrudan “iki değişkeni topla” fikrini uygulamaz. Değerlerin önce yazmaçlara alınması, toplamanın yapılması ve sonucun uygun yere yazılması gerekir:

```asm
mov eax, DWORD PTR [a]   ; a değerini EAX yazmacına yükle
add eax, DWORD PTR [b]   ; b değerini EAX üzerine ekle
mov DWORD PTR [sonuc], eax ; sonucu belleğe yaz
```

Bu örnek kavramsaldır; gerçek çıktı derleyiciye, optimizasyon seviyesine ve kullanılan sözdizimine göre değişebilir.

## Yüksek seviye ile düşük seviye arasındaki fark

| Yüksek seviye kavram | x86 tarafındaki karşılığı |
|---|---|
| Değişken | Yazmaç veya bellek konumu |
| Fonksiyon çağrısı | Argüman aktarımı, `call` ve `ret` |
| `if` koşulu | Karşılaştırma ve koşullu sıçrama |
| Döngü | Etiket, sayaç ve geri sıçrama |
| Nesne | Bellekte belirli düzene sahip veri |

Bir programın çalışma süresini kabaca şu fikirle ifade edebiliriz:

$$T \approx N \times CPI \times \frac{1}{f}$$

Burada $N$ çalıştırılan komut sayısı, $CPI$ komut başına ortalama saat çevrimi, $f$ ise işlemcinin saat frekansıdır. Ancak önbellek kaçırmaları, dallanma tahmini ve paralel yürütme nedeniyle modern işlemciler bu formülü epey renklendirir.

## Yazmaçlar: İşlemcinin çalışma masası

Yazmaçlar, işlemcinin içindeki çok hızlı ve küçük depolama alanlarıdır. 64 bit x86-64 mimarisinde `RAX`, `RBX`, `RCX`, `RDX`, `RSP` ve `RIP` gibi yazmaçlarla karşılaşırız. `RAX` genel amaçlı işlemlerde kullanılabilirken `RSP` yığının tepesini, `RIP` ise sıradaki komutun adresini gösterir.

Aynı yazmacın farklı büyüklükteki bölümlerine erişilebilir:

| Ad | Boyut | İlişki |
|---|---:|---|
| `RAX` | 64 bit | Yazmacın tamamı |
| `EAX` | 32 bit | Alt 32 bit |
| `AX` | 16 bit | Alt 16 bit |
| `AL` | 8 bit | En düşük 8 bit |

Bu ilişki önemlidir; `EAX` üzerine yazmak, x86-64 mimarisinde `RAX` yazmacının üst yarısını sıfırlar.

## Koşullar nasıl çalışır?

Yüksek seviyedeki bir `if`, genellikle karşılaştırma ve sıçrama komutlarına dönüşür:

```asm
cmp eax, ebx       ; EAX ile EBX değerini karşılaştır
jle kucuk_esit     ; EAX <= EBX ise etikete git
mov ecx, 1         ; koşul yanlışsa ECX = 1
jmp devam

kucuk_esit:
mov ecx, 0         ; koşul doğruysa ECX = 0

devam:
```

`cmp`, çıkarma işlemi yapıyormuş gibi bayrakları günceller fakat sonucu saklamaz. `jle` ise sıfır, işaret ve taşma bayraklarını inceleyerek karar verir. Yani işlemcinin “kararı”, birkaç bitlik durum bilgisinden ibarettir.

## Fonksiyonlar ve yığın

Fonksiyon çağrısında `call`, dönüş adresini yığına koyar ve hedef adrese gider. `ret` bu adresi yığından alarak çağıran koda döner. Yerel değişkenler de çoğu zaman yığın üzerinde tutulur. Ancak argümanların hangi yazmaçlardan geçtiği kullanılan çağrı sözleşmesine bağlıdır. Linux x86-64 System V düzeninde ilk tamsayı argümanları `RDI`, `RSI`, `RDX`, `RCX`, `R8` ve `R9` üzerinden taşınır.

```asm
kare:
    mov rax, rdi   ; ilk argümanı dönüş yazmacına kopyala
    imul rax, rdi  ; değeri kendisiyle çarp
    ret            ; sonuç RAX içinde döner
```

Buradaki fonksiyon matematiksel olarak $f(x)=x^2$ işlemini gerçekleştirir.

## Nasıl pratik yapılır?

C kodunu `gcc -S program.c` ile assembly çıktısına dönüştürebilir, `objdump -d` ile çalıştırılabilir dosyayı inceleyebilir ve GDB kullanarak komutları adım adım izleyebilirsin. Başlangıçta optimizasyonu kapatmak için `-O0`, derleyicinin gerçek becerilerini görmek için `-O2` kullanmak öğretici bir karşılaştırmadır. Assembly’nin amacı her programı elle yazmak değil; derleyiciyi, belleği, performansı ve hataların gerçek kaynağını daha iyi anlayabilmektir.
