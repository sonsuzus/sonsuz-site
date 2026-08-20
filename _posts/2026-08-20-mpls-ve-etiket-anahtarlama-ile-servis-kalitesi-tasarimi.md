---
layout: post
title: "MPLS ve Etiket Anahtarlama ile Servis Kalitesi Tasarımı"
math: true
categories: 
  - Bilgi
tags: 
  - MPLS
  - QoS
  - Ağ Mimarisi
  - Etiket Anahtarlama
---

Modern ağlarda her paketin IP başlığını tekrar tekrar incelemek, yoğun trafikte gişede kimlik kontrolü yapmaya benzer: güvenlidir ama yavaştır. MPLS (Multiprotocol Label Switching), paketleri sınıflandırılmış kısa etiketlerle taşıyarak bu süreci hızlandırır. Daha önemlisi, ses, video ve kritik iş uygulamalarına öngörülebilir gecikme sağlayan Servis Kalitesi (QoS) politikalarının ağ boyunca tutarlı uygulanmasına yardım eder.
``
## MPLS Mantığı: IP Yönlendirme ile Etiket Anahtarlama Arasındaki Fark

Klasik IP yönlendirmede her yönlendirici hedef IP adresine göre en uzun önek eşleşmesi yapar. MPLS alanına giren paket ise giriş yönlendiricisinde, yani **LER** (Label Edge Router) üzerinde sınıflandırılır ve bir **FEC**'ye (Forwarding Equivalence Class) atanır. Ardından pakete kısa, yerel anlamlı bir etiket eklenir. Omurgadaki **LSR**'ler (Label Switch Router), IP başlığını yorumlamak yerine etikete bakar ve önceden hazırlanmış iletim tablosuna göre etiketi değiştirir.

| Özellik | Geleneksel IP yönlendirme | MPLS etiket anahtarlama |
|---|---|---|
| Karar anahtarı | Hedef IP öneki | MPLS etiketi |
| Ara düğüm işlemi | En uzun önek eşleşmesi | Etiket değiştirme (swap) |
| Trafik mühendisliği | Sınırlı, maliyete bağlı | Açık LSP ve kısıt tabanlı yol seçimi |
| QoS sürekliliği | DSCP yorumuna bağlı | EXP/TC alanıyla sınıf taşınması |

Bir MPLS etiketi 32 bittir: 20 bit etiket değeri, 3 bit **Traffic Class (TC)**, 1 bit yığın sonu ve 8 bit TTL içerir. Eski dokümanlarda TC alanı sıklıkla EXP olarak geçer. QoS tasarımında kritik bölüm bu 3 bittir. Teorik olarak $2^3 = 8$ trafik sınıfı kodlanabilir; ancak kuyruk, düşürme ve zamanlama politikaları bu sekiz değerin nasıl davranacağını belirler.

## Etiket Yaşam Döngüsü ve LSP

Paket MPLS bulutuna girerken **push**, omurgada ilerlerken **swap**, çıkarken **pop** işlemleri uygulanır. Bu yol, Label Switched Path (LSP) olarak adlandırılır. LDP ile IP yönlendirme tablosunu izleyen LSP'ler kurulabilir; RSVP-TE veya Segment Routing ise bant genişliği, gecikme ya da kaçınılacak bağlantılar gibi kısıtlarla daha kontrollü yollar oluşturur.

```text
Müşteri → [LER: classify + push 101] → [LSR: 101→44] → [LSR: 44→18] → [LER: pop] → Hedef
                 EF / TC=5                 EF / TC=5
```

Bu akışta giriş LER'i paketin DSCP değerini veya uygulama/VLAN bilgisini incelemek için doğru noktadır. Sınıflandırma burada yapılmalı, omurgada ise güvenilir etiket davranışı korunmalıdır. Her ara cihazda karmaşık yeniden sınıflandırma yapmak hem yönetimi hem de hata olasılığını büyütür.

## QoS Tasarımında Temel Prensipler

Önce trafiği iş etkisine göre sınıflandırın. Gerçek zamanlı ses, gecikmeye duyarlı video, kurumsal kritik uygulamalar ve en iyi çaba trafiği aynı kuyrukta yarışmamalıdır. Gecikmenin basit modeli şöyledir:

$$D_{toplam}=D_{iletim}+D_{yayılım}+D_{işleme}+D_{kuyruk}$$

MPLS, özellikle değişken olan $D_{kuyruk}$ bileşenini sınıflar ve kuyruklama ile kontrol etmeye yardımcı olur. Ancak MPLS tek başına bant genişliği yaratmaz; tıkanıklık varsa yanlış tasarlanmış öncelik mekanizması düşük öncelikli trafiği aç bırakabilir.

| Trafik sınıfı | Önerilen davranış | Tasarım notu |
|---|---|---|
| Ses (EF) | Düşük gecikmeli öncelikli kuyruk | Sıkı polisleme ile sınırlandırın |
| Etkileşimli video (AF) | Garantili bant genişliği | WRED ile kontrollü düşürme uygulayın |
| Kritik veri | Ağırlıklı adil kuyruk | Minimum bant genişliği tanımlayın |
| Best effort | Artan bant genişliğini kullanır | Taşma anında ilk etkilenen sınıf olur |

Örnek bir mantıksal politika aşağıdaki gibi düşünülebilir:

```text
class VOICE:  match dscp ef     → TC 5, priority 15%
class VIDEO:  match dscp af41   → TC 4, bandwidth 30%
class DATA:   match dscp af21   → TC 2, bandwidth 25%
class DEFAULT:                  → TC 0, fair-queue
```

Bu örnekte yüzde değerleri cihazdan cihaza kopyalanacak evrensel reçeteler değildir; bağlantı kapasitesi, codec hızı ve trafik ölçümleriyle hesaplanmalıdır. Girişte güvenilmeyen işaretleri yeniden yazın, çekirdekte TC değerini koruyun, çıkışta ise müşterinin QoS sözleşmesine uygun DSCP eşlemesi yapın. Son olarak gecikme, jitter, paket kaybı ve kuyruk doluluğunu izleyin. İyi MPLS-QoS tasarımı hızlı anahtarlamayı, kontrollü tıkanıklığı ve ölçülebilir hizmet hedeflerini aynı LSP üzerinde buluşturur.
