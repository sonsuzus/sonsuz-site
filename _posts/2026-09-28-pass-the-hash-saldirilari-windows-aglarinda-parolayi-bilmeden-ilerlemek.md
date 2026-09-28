---
layout: post
title: "Pass-the-Hash Saldırıları: Windows Ağlarında Parolayı Bilmeden İlerlemek"
math: true
categories: 
  - Bilgi
tags: 
  - pass-the-hash
  - active-directory
  - windows
  - ntlm
  - siber-güvenlik
  - kimlik-doğrulama
toc: true
image: /img/pass-the-hash-66.png
---

Bir saldırganın parolayı çözmeden kullanıcı gibi davranabilmesi kulağa sihirli gelebilir. Pass-the-Hash (PtH), Windows ağlarında parolanın kendisi yerine ondan türetilen NT hash değerinin kimlik doğrulamada kötüye kullanılmasına dayanır. Özellikle ayrıcalıklı hesapların birden fazla sisteme giriş yaptığı Active Directory ortamlarında tek bir ele geçirilmiş uç nokta, saldırgan için tehlikeli bir sıçrama tahtasına dönüşebilir.


![pass-the-hash-66](/img/pass-the-hash-66.svg)

``

## Parola ile hash aynı şey değildir

Windows, belirli kimlik doğrulama senaryolarında parolayı doğrudan karşılaştırmak yerine paroladan türetilmiş kriptografik bir değer kullanır. Basitleştirilmiş NT hash üretimi şöyle gösterilebilir:

$$K_{NT} = MD4(UTF16LE(Parola))$$

Normal koşullarda kullanıcı parolasını girer, istemci gerekli anahtarı üretir ve sunucunun gönderdiği sınamaya cevap verir. NTLMv2 sürecinin sadeleştirilmiş modeli ise şöyledir:

$$K_{v2} = HMAC\text{-}MD5(K_{NT}, Kullanıcı \Vert EtkiAlanı)$$

$$Cevap = HMAC\text{-}MD5(K_{v2}, SunucuSınaması \Vert İstemciVerisi)$$

Kritik nokta şudur: Bazı protokol ve uygulama akışlarında saldırganın açık metin parolayı bilmesi gerekmez. Kullanılabilir hash veya ilişkili kimlik doğrulama materyali ele geçirilmişse geçerli bir cevap üretilebilir. Yani hash, yalnızca kontrol amacıyla saklanan zararsız bir parmak izi değil; uygun koşullarda parolaya eşdeğer bir kimlik doğrulama sırrıdır.

| Özellik | Parola hırsızlığı | Pass-the-Hash |
|---|---|---|
| Ele geçirilen veri | Açık parola | NT hash veya ilişkili materyal |
| Parolayı çözmek gerekir mi? | Zaten bilinir | Hayır |
| Başlıca hedef | Kullanıcı hesabı | NTLM kabul eden sistemler |
| Parola değişince etkisi | Erişim kesilir | Eski hash geçersizleşir |
| MFA etkisi | Akışa göre değişir | Eski protokollerde sınırlı kalabilir |

## Saldırı zincirinin mantığı

PtH çoğunlukla üç aşamada değerlendirilir. Önce saldırgan bir istemcide yerel yönetici veya SYSTEM düzeyinde yetki kazanır. Ardından işletim sisteminin kimlik bilgisi işleyen bileşenlerinde bulunan yeniden kullanılabilir materyali hedefler. Son aşamada bu materyal; dosya paylaşımı, uzaktan yönetim veya NTLM destekleyen başka bir servis üzerinden yatay hareket için denenir.

Bu anlatım, her hash'in her yerde çalışacağı anlamına gelmez. Hesabın yetkileri, hedefte NTLM desteği, güvenlik duvarı kuralları, yönetim paylaşımı politikaları, oturum türü ve Credential Guard gibi korumalar sonucu belirler. Kerberos biletlerinin çalınmasına dayanan Pass-the-Ticket ise benzer amaçlı fakat teknik olarak farklı bir saldırıdır.

## Belirtiler nasıl aranır?

Savunma ekipleri başarılı ağ oturumlarını, NTLM kullanımını ve yönetici hesaplarının beklenmeyen cihazlardan bağlanmasını birlikte incelemelidir. Aşağıdaki PowerShell örneği, son 24 saatteki başarılı ağ oturumlarını görünür kılar; tek başına saldırı kanıtı değildir:

```powershell
$start = (Get-Date).AddHours(-24)
Get-WinEvent -FilterHashtable @{
    LogName   = 'Security'
    Id        = 4624
    StartTime = $start
} | Where-Object {
    $_.Message -match 'Logon Type:\s+3' -and
    $_.Message -match 'NTLM'
} | Select-Object TimeCreated, MachineName, Id, Message
```

Üretim ortamında olay 4624; kaynak IP, hedef cihaz, hesap ayrıcalığı ve 4672 gibi özel yetki olaylarıyla ilişkilendirilmelidir. Servis hesaplarında olağan NTLM trafiği bulunabileceğinden körlemesine alarm üretmek yerine davranış tabanı oluşturmak önemlidir.

## Savunma: Hash'i yeni parola gibi koruyun

| Önlem | Sağladığı fayda |
|---|---|
| Windows Defender Credential Guard | Kimlik bilgisi materyalini yalıtır |
| Windows LAPS | Her cihazda farklı yerel yönetici parolası sağlar |
| NTLM'yi denetleme ve kademeli kısıtlama | Yeniden kullanım yüzeyini azaltır |
| Ayrı yönetici hesapları ve PAW | Ayrıcalıklı sırların kullanıcı cihazlarına taşınmasını önler |
| SMB imzalama ve ağ segmentasyonu | Yatay hareket seçeneklerini sınırlar |
| EDR ve merkezi olay toplama | Şüpheli erişim zincirlerini görünür kılar |

En etkili yaklaşım tek bir ürüne güvenmek değil, ayrıcalık katmanlaması uygulamaktır. Etki alanı yöneticileri e-posta okunan sıradan bilgisayarlarda oturum açmamalı; servis hesapları en az yetkiyle çalışmalı ve mümkünse yönetilen servis hesaplarına geçirilmelidir. NTLM bir anda kapatılmadan önce bağımlılıklar denetlenmelidir. Özetle PtH'nin panzehiri, saldırganın hash'i ele geçirmesini zorlaştırmak, ele geçirilen değerin başka sistemlerde işe yaramamasını sağlamak ve anormal kullanımı hızla yakalamaktır.
