---
layout: post
title: "Event Sourcing Mimarisi: Durumu Olay Geçmişinden Yeniden İnşa Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - event sourcing
  - yazılım mimarisi
  - domain-driven design
image: /img/event-sourcing-mimarisi-33.png
---

Bir banka hesabının bugünkü bakiyesini yalnızca tek bir `balance` alanında tutmak kolaydır; ancak bu değerin **nasıl** oluştuğunu anlamak zordur. Event Sourcing, sistemin mevcut durumunu doğrudan saklamak yerine, durumu değiştiren olayları kalıcılaştırır. Böylece uygulama geçmişi silmek yerine kaydeder ve istenen anın durumunu olayları tekrar oynatarak oluşturabilir.
``

Klasik CRUD yaklaşımında kayıt çoğunlukla son hâliyle güncellenir. Örneğin siparişin durumu `Kargoda` olur; fakat önce ne zaman oluşturulduğu, hangi ödeme denemesinin başarısız olduğu veya kim tarafından iptal edildiği ayrı bir denetim kaydı yoksa belirsizdir. Event Sourcing'de ise `OrderCreated`, `PaymentFailed`, `PaymentReceived` ve `OrderShipped` gibi alan dilini taşıyan olaylar saklanır.

Temel fikir oldukça nettir: Sistem durumu, sıralı olayların indirgenmiş sonucudur. Matematiksel olarak bunu şöyle ifade edebiliriz:

$$S_n = f(f(f(S_0, E_1), E_2), \dots, E_n)$$

Burada $S_0$ başlangıç durumu, $E_i$ bir olay, $f$ ise olayı mevcut duruma uygulayan fonksiyondur. İdeal durumda bu fonksiyon deterministik olmalıdır: Aynı olay dizisi, her yeniden çalıştırmada aynı durumu üretmelidir. Bu özellik hata araştırırken adeta zaman makinesi etkisi yaratır.

| Özellik | Geleneksel CRUD | Event Sourcing |
|---|---|---|
| Kalıcı veri | Güncel durum | Değişmez olay akışı |
| Geçmişi görme | Ek log gerektirir | Doğal olarak mevcuttur |
| Hata analizi | Sınırlı bağlam | Olay sırası incelenir |
| Veri modeli değişimi | Migrasyon ağırlıklı | Yeni projection üretilebilir |
| Okuma performansı | Genellikle doğrudan | Projection gerekebilir |

![event-sourcing-mimarisi-33](/img/event-sourcing-mimarisi-33.svg)


Örneğin sadeleştirilmiş bir hesap agregası, olayları uygulayarak bakiyesini üretir. Buradaki kritik ayrım şudur: Komutlar niyeti ifade eder (`Para yatır`), olaylar ise gerçekleşmiş ve değişmez gerçekleri (`Para yatırıldı`) temsil eder.

```python
from dataclasses import dataclass

@dataclass
class Account:
    balance: int = 0

    def apply(self, event: dict):
        if event["type"] == "MoneyDeposited":
            self.balance += event["amount"]
        elif event["type"] == "MoneyWithdrawn":
            self.balance -= event["amount"]

events = [
    {"type": "MoneyDeposited", "amount": 500},
    {"type": "MoneyWithdrawn", "amount": 120},
    {"type": "MoneyDeposited", "amount": 80}
]

account = Account()
for event in events:
    account.apply(event)

print(account.balance)  # 460
```

Gerçek projelerde olaylar bir **event store** içinde agregaya ait sürüm numarasıyla tutulur. Sürüm numarası, iki kullanıcının aynı anda aynı hesabı değiştirmesi gibi yarış durumlarında iyimser eşzamanlılık kontrolü sağlar. Beklenen sürüm $v$ iken depodaki sürüm farklıysa işlem reddedilir; istemci güncel olayları okuyup kararını tekrar vermelidir.

Event Sourcing çoğu zaman CQRS ile birlikte anılır. Yazma tarafı iş kurallarını korur ve olay üretir; okuma tarafı ise bu olaylardan hızlı sorgulanabilir projection'lar oluşturur. Örneğin sipariş olaylarından müşteri paneli için ayrı bir `siparis_ozetleri` tablosu üretilebilir.

| Kavram | Görevi | Örnek |
|---|---|---|
| Command | Değişiklik isteği | `ShipOrder` |
| Aggregate | İş kuralı sınırı | `Order` |
| Event | Gerçekleşmiş kayıt | `OrderShipped` |
| Projection | Okuma modeli | Günlük satış özeti |
| Snapshot | Hızlandırılmış ara durum | 500. olaydaki hesap durumu |

Her olaydan başlayarak yeniden oynatma, olay sayısı büyüdüğünde pahalı olabilir. Çözüm snapshot'tır: Belirli bir olay numarasındaki durum saklanır, ardından yalnızca sonraki olaylar uygulanır. Yaklaşık maliyet $O(n)$ iken snapshot sonrası $O(n-k)$ olur; burada $k$ snapshot'ın kapsadığı olay sayısıdır.

Bu mimari her tabloya uygulanacak sihirli değnek değildir. Basit yönetim panellerinde gereksiz karmaşıklık yaratabilir. Ancak finans, stok, rezervasyon, lojistik ve denetlenebilir iş süreçlerinde geçmişin birinci sınıf veri olması büyük avantajdır. İyi isimlendirilmiş, değişmez ve iş diline yakın olaylar sayesinde sistem yalnızca ne olduğunu değil, neden bugünkü hâline geldiğini de anlatır.
