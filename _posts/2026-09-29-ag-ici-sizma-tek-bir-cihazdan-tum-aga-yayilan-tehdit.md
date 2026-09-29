---
layout: post
title: "Ağ İçi Sızma: Tek Bir Cihazdan Tüm Ağa Yayılan Tehdit"
math: true
categories: 
  - Bilgi
tags: 
  - siber güvenlik
  - lateral movement
  - kimlik güvenliği
  - ağ güvenliği
  - tehdit avcılığı
  - zero trust
toc: true
image: /img/ag-ici-sizma-89.png
---

Bir saldırganın ağa girmesi çoğu zaman filmin başlangıcıdır, finali değil. Ele geçirilen dizüstü bilgisayar yalnızca bir sıçrama tahtası olabilir: saldırgan daha değerli hesapları, dosya sunucularını, yönetim sistemlerini ve etki alanı denetleyicilerini arar. Bu kontrollü ilerleyişe **ağ içi sızma**, yani *lateral movement* denir. Savunma açısından amaç, saldırganın yöntemlerini operasyonel olarak taklit etmek değil; bıraktığı izleri anlayıp zinciri mümkün olduğunca erken kırmaktır.
``

## Ağ içinde ilerleme mantığı

Lateral movement genellikle keşif, kimlik elde etme, erişim kurma ve kalıcılık adımlarından oluşur. İlk cihazdaki kullanıcı düşük yetkili olsa bile kayıtlı oturumlar, servis hesapları, erişim belirteçleri veya yanlış yapılandırılmış paylaşımlar daha güçlü sistemlere giden yolu açabilir.

Bir saldırganın beklenen kazancı basitçe şöyle modellenebilir:

$$R = P_{başarı} \times V_{hedef} - C_{tespit}$$

Burada $P_{başarı}$ erişimin başarı ihtimalini, $V_{hedef}$ hedef sistemin değerini, $C_{tespit}$ ise yakalanma riskini temsil eder. Bu nedenle saldırganlar çoğunlukla normal yönetici davranışına benzeyen, düşük gürültülü yolları tercih eder.

| Aşama | Saldırganın amacı | Savunma sinyali |
|---|---|---|
| Keşif | Kullanıcıları ve sunucuları öğrenmek | Olağandışı dizin, paylaşım veya port sorguları |
| Kimlik hırsızlığı | Parola, hash, bilet ya da token edinmek | Hassas süreç erişimi, beklenmedik oturum açma |
| Sıçrama | Başka cihaza uzaktan bağlanmak | Yeni kaynak-hedef kombinasyonları |
| Tünelleme | Trafiği ara cihaz üzerinden geçirmek | Uzun ömürlü, şifreli ve alışılmadık bağlantılar |
| Kalıcılık | Erişimi yeniden kullanmak | Yeni servisler, görevler veya yetki değişiklikleri |

## Kimlik hırsızlığı neden merkezde?

Modern ağlarda sınırlar cihazlardan çok **kimlikler** tarafından belirlenir. Bellekte kalan erişim belirteçleri, tekrar kullanılan yerel yönetici parolaları, servis hesabı sırları ve Kerberos biletleri saldırgan için anahtar görevi görebilir. Hash veya oturum belirtecinin kötüye kullanılması durumunda parolanın açık metnini bilmek bile gerekmeyebilir.

Koruma tarafında Credential Guard benzeri izolasyon özellikleri, benzersiz yerel yönetici parolaları, çok faktörlü kimlik doğrulama ve ayrıcalıklı hesapların normal iş istasyonlarında kullanılmaması önemlidir. Servis hesapları da etkileşimli oturum açamayacak şekilde sınırlandırılmalı ve sırları düzenli döndürülmelidir.

## Tünelleme: Ağ içinde görünmez koridor

SSH port yönlendirme, SOCKS vekilleri ve ters bağlantı tabanlı proxy araçları meşru yönetim amaçları taşır; ancak ele geçirilmiş bir cihazı ağ geçidine dönüştürmek için de kötüye kullanılabilir. Böylece saldırgan, doğrudan erişemediği bir iç servise ara cihaz üzerinden ulaşır.

| Normal kullanım | Şüpheli kullanım |
|---|---|
| Onaylı yönetim sunucusundan bağlantı | Kullanıcı dizüstüsünden sunucu yönetimi |
| Bilinen hedef ve çalışma saatleri | Çok sayıda iç hedefe gece bağlantısı |
| Kısa süreli bakım oturumu | Saatlerce açık kalan şifreli kanal |
| Kayıtlı yönetici hesabı | Yeni veya sıradan kullanıcı hesabı |

## Telemetriyle zinciri yakalamak

Aşağıdaki savunma odaklı KQL örneği, kısa sürede çok sayıda cihaza uzaktan oturum açan hesapları bulmaya yardımcı olur:

```kql
DeviceLogonEvents
| where Timestamp > ago(1h)
| where LogonType in ("RemoteInteractive", "Network")
| summarize
    HedefSayisi=dcount(DeviceName),
    Hedefler=make_set(DeviceName, 20)
  by AccountName, bin(Timestamp, 10m)
| where HedefSayisi >= 5
| order by HedefSayisi desc
```

Bu sorgu tek başına saldırı kanıtı değildir; dağıtım sistemleri ve destek ekipleri benzer davranabilir. Sonuçlar cihaz rolü, hesap ayrıcalığı, mesai saati ve geçmiş davranışla zenginleştirilmelidir.

## Yayılmayı durdurma

Etkili savunma; ağ segmentasyonu, en az ayrıcalık, yönetim katmanlarının ayrılması ve doğu-batı trafiğinin izlenmesini birlikte gerektirir. Şüpheli hareket görüldüğünde cihazı izole etmek, ilgili oturumları sonlandırmak, kimlik bilgilerini güvenli sırayla döndürmek ve tünelin bağlandığı hedefleri incelemek gerekir. Kısacası saldırganın bir cihaz kazanması kaçınılmaz olabilir; fakat tüm ağı kazanması, mimari ve görünürlük sayesinde engellenebilir.

![ag-ici-sizma-89](/img/ag-ici-sizma-89.svg)

