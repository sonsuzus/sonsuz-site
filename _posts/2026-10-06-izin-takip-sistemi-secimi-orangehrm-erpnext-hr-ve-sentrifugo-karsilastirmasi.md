---
layout: post
title: "İzin Takip Sistemi Seçimi: OrangeHRM, ERPNext HR ve Sentrifugo Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - izin yönetimi
  - orangehrm
  - erpnext
  - sentrifugo
  - insan kaynakları
  - açık kaynak
toc: true
image: /img/izin-takip-sistemi-42.png
---

![izin-takip-sistemi-42](/img/izin-takip-sistemi-42.svg)


Çalışan izinlerini elektronik tablolarla yönetmek, ekip büyüdükçe küçük bir insan kaynakları macerasına dönüşebilir. Kimin kaç günü kaldı, hangi talep onay bekliyor ve aynı tarihte kaç kişi yok? OrangeHRM, ERPNext HR ve Sentrifugo bu soruları merkezi bir izin takip sistemiyle yanıtlayan üç önemli açık kaynak seçenektir.
``
## İzin takip sisteminin temel mantığı

Bir izin sistemi yalnızca başlangıç ve bitiş tarihlerini saklamaz. Çalışanın hakkını, kullanılan günleri, hafta sonlarını, resmî tatilleri ve onay akışını birlikte değerlendirmelidir. En basit bakiye hesabı şöyle gösterilebilir:

$$Kalan\ İzin = Toplam\ Hak + Devreden\ İzin - Kullanılan\ İzin$$

Örneğin yıllık hakkı 20 gün, devreden izni 3 gün ve kullandığı izin 8 gün olan bir çalışanın bakiyesi $20+3-8=15$ gündür. Ancak yarım gün izinler, farklı ülke takvimleri ve kıdeme bağlı hak ediş kuralları devreye girdiğinde hesaplama katmanı hızla karmaşıklaşır.

İyi bir sistemde süreç genellikle dört adımdan oluşur: çalışan talep oluşturur, sistem bakiyeyi ve tarih çakışmalarını denetler, yönetici talebi değerlendirir, onaylanan günler bakiyeden düşülür. Denetim kaydı tutulması da sonradan gelen “Ben bunu onaylamamıştım!” sürprizlerini azaltır.

## Üç sistemin karşılaştırması

| Özellik | OrangeHRM | ERPNext HR | Sentrifugo |
|---|---|---|---|
| Temel yaklaşım | İnsan kaynakları odaklı | Bütünleşik ERP yaklaşımı | Modüler İK yönetimi |
| İzin politikaları | Güçlü ve anlaşılır | Esnek, iş akışlarıyla bağlantılı | Temel ihtiyaçlar için yeterli |
| Bordro ve muhasebe | Sınırlı veya sürüme bağlı | ERP modülleriyle güçlü | Sınırlı |
| Kullanım kolaylığı | Başlangıç için rahat | Öğrenme eğrisi daha yüksek | Sade fakat arayüzü eski görünebilir |
| Uygun senaryo | Küçük ve orta ölçekli ekipler | Süreçlerini tek platformda birleştiren şirketler | Düşük bütçeli temel İK projeleri |

### OrangeHRM

OrangeHRM, personel bilgileri, izin türleri, tatil takvimleri ve yönetici onaylarını düzenli bir arayüzde toplar. Sadece İK operasyonuna odaklanan kuruluşlar için kurulumu ve anlaşılması görece kolaydır. Topluluk sürümü temel gereksinimleri karşılar; gelişmiş raporlama veya kurumsal özellikler için ticari seçenekleri incelemek gerekebilir.

### ERPNext HR

ERPNext HR, izin yönetimini muhasebe, bordro, proje ve zaman çizelgesi gibi modüllerle aynı veri modeli içinde ele alır. Bir çalışanın iznini ücret hesaplamasına veya proje kapasitesine bağlamak isteyen şirketler için güçlüdür. Buna karşılık yalnızca izin kaydı arayan küçük bir ekip için kapsamı gereğinden büyük olabilir.

### Sentrifugo

Sentrifugo; izinler, çalışan bilgileri, performans ve self servis özellikleri sunan açık kaynaklı bir İK çözümüdür. Temel süreçleri düşük lisans maliyetiyle dijitalleştirmek isteyen ekipler açısından değerlidir. Yine de proje güncelliği, eklenti ekosistemi, güvenlik yamaları ve kullanılan teknoloji yığını kurulumdan önce dikkatle araştırılmalıdır.

## Basit bakiye kontrolü

Aşağıdaki Python fonksiyonu, talep edilen izin miktarının mevcut bakiyeyi aşıp aşmadığını denetler. Gerçek uygulamada tarihlerin hafta sonu ve tatil takvimine göre ayrıca hesaplanması gerekir.

```python
def izin_talebi_kontrol(bakiye, talep_edilen_gun):
    if talep_edilen_gun <= 0:
        return 'Geçersiz izin süresi'

    if talep_edilen_gun > bakiye:
        return 'Yetersiz izin bakiyesi'

    kalan = bakiye - talep_edilen_gun
    return f'Talep uygun, kalan bakiye: {kalan} gün'

print(izin_talebi_kontrol(15, 4))
```

Bu kontrol, üç ürünün de arka planda uyguladığı iş kurallarının sadeleştirilmiş hâlidir. Kurumsal sistemler buna rol tabanlı yetkilendirme, çok aşamalı onay ve bildirim mekanizmaları ekler.

## Hangisini seçmeli?

Hızlı devreye alma ve doğrudan İK odağı için OrangeHRM; izin verisini bordro, muhasebe ve projelerle bütünleştirmek için ERPNext HR daha mantıklıdır. Sentrifugo ise temel özellikleri kendi sunucusunda çalıştırmak isteyen teknik ekiplerce değerlendirilebilir. Son kararı vermeden önce mobil erişim, yerelleştirme, yedekleme, API desteği ve aktif bakım durumu test edilmelidir. En iyi sistem, en fazla özelliğe sahip olan değil, şirketin izin politikasını çalışanlara ek eğitim maratonu yaşatmadan uygulayabilendir.
