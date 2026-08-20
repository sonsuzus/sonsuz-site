---
layout: post
title: "Assembly ile Bootloader Yazımı: BIOS’tan Kendi Kodunuza İlk Adım"
math: true
categories: 
  - Bilgi
tags: 
  - assembly
  - bootloader
  - x86
  - bıos
  - işletim sistemleri
---

Bir bilgisayarın açılışında işletim sistemi henüz sahnede değildir: ekran kartına görüntü çizdirecek sürücüler, dosya sistemi ve hatta bellek yöneticisi yoktur. Buna rağmen işlemci birkaç talimat çalıştırarak makineyi hayata döndürür. Bootloader yazmak, bu minimal ortamda BIOS, disk ve CPU ile doğrudan konuşmayı öğrenmektir. Küçücük bir 512 baytlık programla ekrana mesaj basmak, donanım ile işletim sistemi arasındaki köprünün ilk tahtasını yerleştirmek gibidir.
``

## Açılış zinciri nasıl çalışır?

Klasik BIOS tabanlı x86 makinelerde güç verildiğinde işlemci, sabit bir bellek adresinden firmware kodunu çalıştırır. BIOS, temel donanım kontrollerini yapar ve önyüklenebilir aygıtları sıralar. Seçilen diskin ilk sektörü belleğe okunur; bu sektör **boot sector** olarak bilinir.

Boot sector’ın fiziksel boyutu tam olarak $512$ bayttır. BIOS, bu veriyi çoğunlukla `0x7C00` adresine yükler ve yürütmeyi buraya devreder. Sektörün son iki baytı sihirli imza olmalıdır:

$$\text{imza} = 0xAA55$$

Diskte bayt sırası küçük uçlu (little-endian) olduğundan kaynakta genellikle `dw 0xAA55` yazılır. Bu imza yoksa BIOS, sektörün açılış kodu olmadığını varsayar ve sıradaki aygıtı denemeye geçer.

| Kavram | BIOS/MBR yaklaşımı | Modern UEFI yaklaşımı |
|---|---|---|
| İlk çalıştırılan kod | Diskin ilk 512 baytı | EFI System Partition içindeki `.efi` dosyası |
| İşlemci başlangıcı | 16-bit real mode | Genellikle 32/64-bit UEFI ortamı |
| Disk düzeni | MBR | GPT |
| Ana kısıt | Çok az alan ve BIOS kesmeleri | Firmware API’leri ve PE biçimi |

Bu yazıda eğitim amacıyla BIOS ve 16-bit real mode kullanılır. Gerçek makinelerde UEFI yaygın olsa da BIOS modeli, önyükleme mantığını çıplak biçimde gösterir.

## Real mode ve segment mantığı

İşlemci boot sector’a geldiğinde 16-bit real mode’dadır. Adresler, segment ve ofset çiftleriyle ifade edilir. Fiziksel adres hesaplaması şöyledir:

$$\text{fiziksel adres} = \text{segment} \times 16 + \text{ofset}$$

Örneğin `0x07C0:0x0000`, fiziksel olarak `0x7C00` adresine karşılık gelir. Bu nedenle bootloader’ın ilk işi, veri segmentlerini tahmin edilebilir hâle getirmektir. Ayrıca BIOS kesmeleri işletim sistemi yokken sunulan küçük servislerdir. `int 0x10`, video; `int 0x13`, disk erişimi için sık kullanılan kesmelerdir.

## İlk boot sector: ekrana mesaj yazdırma

Aşağıdaki NASM kodu, BIOS’un teletype video hizmetini kullanarak karakterleri ekrana gönderir. `lodsb`, `SI` işaretçisinin gösterdiği baytı `AL` kayıtçısına alır; sıfır sonlandırıcı görülene kadar döngü sürer.

```asm
bits 16
org 0x7C00

start:
    xor ax, ax
    mov ds, ax
    mov es, ax

    mov si, message
.print:
    lodsb
    test al, al
    jz .halt
    mov ah, 0x0E       ; BIOS teletype fonksiyonu
    mov bh, 0x00       ; ekran sayfası
    mov bl, 0x07       ; açık gri renk
    int 0x10
    jmp .print

.halt:
    cli
    hlt

message db 'Merhaba, bootloader!', 0

times 510-($-$$) db 0
dw 0xAA55
```

`org 0x7C00`, derleyiciye etiket adreslerinin BIOS’un yükleme konumuna göre hesaplanacağını söyler. `times 510-($-$$) db 0` ise kodu sıfırlarla doldurur; imza için son iki baytı korur. Bu satır bir nevi “512 bayt bütçe denetçisi”dir.

| Talimat/öğe | Görevi | Neden önemlidir? |
|---|---|---|
| `xor ax, ax` | `AX` kayıtçısını sıfırlar | Segmentleri güvenli başlangıç değerine taşır |
| `int 0x10` | BIOS video hizmetini çağırır | Ekran sürücüsü olmadan çıktı üretir |
| `times ...` | Sektörü doldurur | Kodun BIOS’un beklediği boyutta olmasını sağlar |
| `dw 0xAA55` | Önyükleme imzası yazar | BIOS’un sektörü kabul etmesini sağlar |

Kodu `nasm -f bin boot.asm -o boot.bin` ile derleyebilir, ardından `qemu-system-i386 -drive format=raw,file=boot.bin` ile güvenle test edebilirsiniz. Bir sonraki aşama, `int 0x13` ile diskin başka sektörlerini okuyup ikinci aşama yükleyicisini belleğe almaktır. İşte o noktada 512 baytlık merhaba mesajı, gerçek bir işletim sistemi başlangıcına dönüşür.
