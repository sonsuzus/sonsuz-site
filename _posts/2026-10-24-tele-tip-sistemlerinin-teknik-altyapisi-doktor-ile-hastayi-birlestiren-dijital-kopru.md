---
layout: post
title: "Tele-Tıp Sistemlerinin Teknik Altyapısı: Doktor ile Hastayı Birleştiren Dijital Köprü"
math: true
categories: 
  - Bilgi
tags: 
  - tele-tıp
  - sağlık teknolojileri
  - webrtc
  - siber güvenlik
  - bulut bilişim
  - yazılım mimarisi
toc: true
image: /img/tele-tip-sistemlerinin-67.png
---

Tele-tıp, doktorun ekrandan el salladığı basit bir görüntülü görüşme değildir. Kameranın arkasında gerçek zamanlı iletişim servisleri, elektronik sağlık kayıtları, güvenlik katmanları, tıbbi cihaz entegrasyonları ve hata anında devreye giren yedek sistemler bulunur. Kısacası tele-tıp platformu, çevrim içi toplantı uygulaması ile dijital hastanenin dikkatle birleştirilmiş hâlidir.

``

## Temel mimari nasıl çalışır?

Hasta mobil uygulama veya web tarayıcısı üzerinden sisteme girer. Kimlik doğrulamasının ardından randevu servisi uygun doktoru bulur ve görüşme başladığında gerçek zamanlı iletişim altyapısı devreye girer. Doktorun notları, reçeteler ve ölçüm sonuçları ise elektronik sağlık kaydı sistemine aktarılır.

Tipik bir platform şu bileşenlerden oluşur:

- **İstemci uygulamaları:** Doktor ve hasta arayüzlerini sunar.
- **API katmanı:** Uygulamalar ile arka uç servisleri arasındaki trafiği yönetir.
- **Kimlik servisi:** Kullanıcıyı doğrular ve yetkilerini denetler.
- **Görüşme servisi:** Ses, video ve mesajlaşmayı sağlar.
- **Kayıt sistemi:** Muayene notlarını, reçeteleri ve raporları saklar.
- **Bildirim servisi:** SMS, e-posta veya anlık bildirim gönderir.
- **İzleme altyapısı:** Hataları, gecikmeleri ve servis sağlığını takip eder.

## Görüntülü görüşmenin motoru: WebRTC

Modern tele-tıp uygulamalarında çoğunlukla **WebRTC** kullanılır. WebRTC, tarayıcılar ve mobil uygulamalar arasında düşük gecikmeli ses ve video aktarımına imkân verir. Ancak iki cihaz her zaman doğrudan bağlanamaz. NAT ve güvenlik duvarları nedeniyle **STUN** sunucuları bağlantı adresini keşfeder; doğrudan bağlantı kurulamazsa **TURN** sunucusu trafiği aktarır.

| Teknoloji | Görevi | Ne zaman kullanılır? |
|---|---|---|
| WebRTC | Ses ve video aktarımı | Canlı muayene sırasında |
| STUN | Dış ağ adresini keşfetme | Doğrudan bağlantı kurulurken |
| TURN | Trafiği sunucu üzerinden iletme | Güvenlik duvarı bağlantıyı engellediğinde |
| WebSocket | Anlık olay ve mesaj taşıma | Bekleme odası ve sohbet özelliklerinde |

Görüşme kalitesini etkileyen önemli değerlerden biri gecikmedir. Yaklaşık toplam gecikme şöyle düşünülebilir:

$$L_{toplam} = L_{ağ} + L_{kodlama} + L_{işleme} + L_{tampon}$$

Gecikme yükseldikçe taraflar birbirinin sözünü kesmeye başlar. Sistem bu nedenle bağlantıya göre çözünürlüğü ve bit hızını dinamik olarak düşürebilir. Biraz daha pikselli doktor, üç saniye geriden gelen doktordan genellikle daha kullanışlıdır.

## Sağlık verilerinde güvenlik

Tele-tıp platformları son derece hassas veriler işler. Aktarım sırasında TLS, görüntülü görüşmede ise SRTP gibi şifreleme mekanizmaları kullanılmalıdır. Veriler depolanırken de güçlü şifreleme uygulanmalı; anahtarlar uygulama kodundan ayrı tutulmalıdır.

Rol tabanlı erişim kontrolü sayesinde herkes yalnızca ihtiyacı olan verilere ulaşır. Örneğin doktor klinik kaydı görebilirken teknik destek çalışanı tıbbi içeriği görüntüleyememelidir. Çok faktörlü kimlik doğrulama ve değiştirilemez denetim kayıtları da kritik işlemlerin izlenmesini sağlar.

```javascript
function canViewRecord(user, patientId) {
  const allowedRole = user.roles.includes("doctor");
  const hasConsent = user.consentedPatients.includes(patientId);
  return allowedRole && hasConsent;
}
```

Bu basitleştirilmiş örnek, yalnızca doktor rolüne ve hasta onayına sahip kullanıcının kaydı açabilmesini gösterir. Gerçek sistemlerde kurum, zaman, tedavi ilişkisi ve acil durum yetkisi gibi ek kurallar bulunur.

## Standartlar ve entegrasyon

Hastane sistemleriyle veri alışverişinde **HL7 FHIR** öne çıkar. FHIR; hasta, gözlem, randevu ve reçete gibi sağlık kavramlarını standart kaynaklar hâlinde tanımlar.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Tek parça uygulama | Kurulumu daha kolaydır | Büyüdükçe yönetimi zorlaşır |
| Mikroservis mimarisi | Bağımsız ölçeklenebilir | Operasyonel karmaşıklık getirir |
| Bulut altyapısı | Esnek kapasite sunar | Veri konumu dikkatle yönetilmelidir |
| Kurum içi altyapı | Fiziksel kontrol sağlar | Bakım maliyeti yüksektir |

Başarılı bir tele-tıp sistemi yalnızca bağlantı kurmaz; bağlantı kesildiğinde yeniden bağlanır, yoğunlukta ölçeklenir, hasta onayını kaydeder ve kritik veriyi güvenle taşır. Teknolojinin nihai görevi doktorun yerini almak değil, mesafeyi klinik hizmetin önünden kaldırmaktır.

![tele-tip-sistemlerinin-67](/img/tele-tip-sistemlerinin-67.svg)

