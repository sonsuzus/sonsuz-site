---
layout: post
title: "Kendi Bug Bounty ve Güvenli Hata Bildirim Sistemini Tasarlamak"
math: true
categories: 
  - Proje
tags: 
  - bug bounty
  - siber güvenlik
  - hata bildirimi
  - güvenli yazılım
  - api
  - web geliştirme
toc: true
image: /img/kendi-bug-bounty-46.png
---

![kendi-bug-bounty-46](/img/kendi-bug-bounty-46.svg)


Bir güvenlik araştırmacısı kritik bir açık bulduğunda kime, nasıl ve hangi kanıtlarla ulaşacağını bilmelidir. Open Bug Bounty veya HackerOne benzeri özel bir sistem; araştırmacıları, güvenlik ekiplerini ve ürün sahiplerini aynı iş akışında buluşturur. Fakat bu proje, sıradan bir destek talebi uygulamasından daha fazlasıdır: hassas verileri korumalı, mükerrer raporları yakalamalı ve kontrollü açıklama sürecini yönetmelidir.
``

## Temel iş akışı

Bir raporun yaşam döngüsü durum makinesi olarak modellenebilir:

`Taslak → Gönderildi → İnceleniyor → Doğrulandı → Çözüldü → Açıklandı`

Rapor geçersizse **Reddedildi**, daha önce bildirilmişse **Mükerrer** durumuna taşınır. Durum makinesi kullanmak, örneğin çözülmüş bir raporun yanlışlıkla yeniden “gönderildi” yapılmasını engeller.

| Rol | Yetki | Görememesi gerekenler |
|---|---|---|
| Araştırmacı | Rapor oluşturma, kanıt ekleme | Diğer özel raporlar |
| Triyaj uzmanı | Doğrulama, sınıflandırma | Finansal yönetim ayarları |
| Program sahibi | Kapsam ve ödül yönetimi | Gereksiz kişisel veriler |
| Yönetici | Rol ve sistem yönetimi | Şifresiz gizli içerik |

Bu ayrım, **en az ayrıcalık ilkesi** üzerine kurulmalıdır. Yalnızca giriş yapmış olmak yeterli değildir; her API isteğinde rol, kaynak sahipliği ve program üyeliği ayrıca denetlenmelidir.

## Önem derecesi ve ödül hesabı

Açıkların önceliği CVSS gibi standartlarla belirlenebilir. Daha sade bir özel puanlama için şu model kullanılabilir:

$$Risk = Etki \times İstismarOlasılığı \times VarlıkKatsayısı$$

Her değişken 1 ile 5 arasında seçilirse en yüksek risk puanı $5^3 = 125$ olur. Ödül ise taban tutar ve risk oranıyla hesaplanabilir:

$$Ödül = TabanÖdül \times (Risk / 125)$$

Ancak otomatik sonuç yalnızca öneri olmalıdır. Kaliteli açıklama, çalışan kavram kanıtı ve daha önce raporlanmış olma durumu nihai kararı değiştirebilir.

## Veri modeli ve güvenlik

Temel tablolar `users`, `programs`, `assets`, `reports`, `comments`, `attachments`, `rewards` ve `audit_logs` olabilir. Rapor; başlık, etkilenen varlık, açıklık türü, tekrar üretme adımları, etki açıklaması ve çözüm önerisi içermelidir.

Kanıt dosyaları doğrudan herkese açık klasörlere konulmamalıdır. Nesne depolamada şifrelenmeli, kısa ömürlü imzalı bağlantılarla sunulmalı ve zararlı dosya taramasından geçirilmelidir. Parolalar Argon2id ile özetlenmeli; oturumlarda çok faktörlü kimlik doğrulama desteklenmelidir. Audit log kayıtları da “kim, neyi, ne zaman değiştirdi?” sorusunu yanıtlamalıdır.

## Güvenli durum geçişi örneği

Aşağıdaki FastAPI kodu, istemcinin istediği her duruma serbestçe geçmesini engeller:

```python
from enum import Enum
from fastapi import FastAPI, HTTPException

app = FastAPI()

class Status(str, Enum):
    submitted = "submitted"
    triage = "triage"
    confirmed = "confirmed"
    resolved = "resolved"
    rejected = "rejected"

ALLOWED = {
    Status.submitted: {Status.triage, Status.rejected},
    Status.triage: {Status.confirmed, Status.rejected},
    Status.confirmed: {Status.resolved},
    Status.resolved: set(),
    Status.rejected: set()
}

@app.post("/reports/{report_id}/transition")
def transition(report_id: int, current: Status, target: Status):
    if target not in ALLOWED[current]:
        raise HTTPException(409, "Geçersiz durum geçişi")

    # Burada rol kontrolü ve veritabanı güncellemesi yapılır.
    return {"report_id": report_id, "status": target}
```

Gerçek uygulamada `current` değeri kullanıcıdan alınmamalı, veritabanından okunmalıdır. Güncelleme atomik bir işlem içinde yapılmalı ve audit log kaydı aynı işlemde oluşturulmalıdır.

## Sistemi olgunlaştıran özellikler

Mükerrer rapor tespiti için başlık benzerliği, açıklık türü ve etkilenen varlık birlikte değerlendirilebilir; ancak gizlilik nedeniyle araştırmacıya başka raporun ayrıntıları gösterilmemelidir. Bildirimler e-posta ve uygulama içi kanallardan iletilebilir. Oran sınırlama, CAPTCHA ve kötüye kullanım tespiti de spam saldırılarını azaltır.

Son olarak açık bir kapsam politikası hazırlayın: test edilebilen alan adları, yasak yöntemler, hizmet kesintisi kuralları, yanıt süreleri ve güvenli liman şartları net olsun. İyi bir bug bounty platformunun asıl süper gücü yalnızca kodu değil, araştırmacıyla kurulan güveni de korumasıdır.
