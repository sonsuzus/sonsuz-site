---
layout: post
title: "SOLID Prensipleri: Nesne Yönelimli Tasarımda Sürdürülebilirliğin Beşli Formülü"
math: true
categories: 
  - Bilgi
tags: 
  - solıd
  - nesne yönelimli programlama
  - yazılım mimarisi
toc: true
---

Bir yazılım projesi ilk gününde çoğu zaman düzenli görünür; sınıflar az, gereksinimler nettir ve herkes mutludur. Asıl sınav, yeni ödeme sağlayıcısı, farklı raporlama isteği veya beklenmedik bir iş kuralı geldiğinde başlar. SOLID, nesne yönelimli tasarımın değişime direnmek yerine değişimi yönetmesine yardım eden beş ilkedir. Amaç “daha çok sınıf” üretmek değil; bağımlılıkları bilinçli kurmak, kodun niyetini görünür kılmak ve değişikliğin etkisini sınırlamaktır.
``

SOLID adındaki her harf bir tasarım ilkesini temsil eder. Bu ilkeler katı kanunlar değil, kod kokularını fark etmeyi sağlayan bir pusuladır. Genel fikir şudur: Bir modülün değişme ihtimali arttıkça, o modülün sorumluluğu ve bağımlılıkları daha dikkatli ayrıştırılmalıdır. Basitçe, değişikliğin maliyetini $C$ ile gösterirsek, iyi ayrıştırılmış bileşenlerde hedef; $C \approx C_{yerel}$ olacak şekilde zincirleme etkileri azaltmaktır.

| İlke | Temel soru | Sağladığı fayda |
|---|---|---|
| SRP | Bu sınıfın değişmesi için kaç neden var? | Odaklı sınıflar |
| OCP | Yeni davranış eklemek için eski kodu bozuyor muyum? | Güvenli genişleme |
| LSP | Alt tür, üst türün yerine sorunsuz geçiyor mu? | Tutarlı kalıtım |
| ISP | İstemci kullanmadığı metotlara zorlanıyor mu? | Küçük arayüzler |
| DIP | İş kuralları somut teknolojiye mi bağlı? | Esnek mimari |

## 1. Single Responsibility Principle (SRP)

**Tek Sorumluluk İlkesi**, bir sınıfın değişmesi için tek bir temel nedeni olması gerektiğini söyler. Örneğin `InvoiceService` hem faturayı hesaplıyor, hem PDF üretiyor, hem de e-posta atıyorsa üç ayrı paydaşın isteğiyle değişebilir: muhasebe, tasarım ve iletişim ekibi. Bu, sınıfı kırılganlaştırır.

| Kötü ayrım | Daha sağlıklı ayrım |
|---|---|
| `InvoiceService`: hesapla, yazdır, gönder | `InvoiceCalculator`, `InvoiceRenderer`, `InvoiceMailer` |

SRP, “her sınıfta yalnızca bir metot olsun” demek değildir. Birbirine sıkı biçimde bağlı iş kuralları aynı sınıfta kalabilir; önemli olan tek bir sorumluluk ekseninde değişmeleridir.

## 2. Open/Closed Principle (OCP)

**Açık/Kapalı İlkesi**, bileşenlerin genişletmeye açık, mevcut kaynak kodunu değiştirmeye kapalı olmasını hedefler. Sürekli `if/else` zincirine yeni ödeme türü eklemek yerine davranışı bir arayüz arkasına alabiliriz.

```python
from typing import Protocol

class PaymentMethod(Protocol):
    def pay(self, amount: float) -> None: ...

class CreditCardPayment:
    def pay(self, amount: float) -> None:
        print(f"Karttan {amount} TL çekildi")

class PaymentService:
    def complete(self, method: PaymentMethod, amount: float) -> None:
        method.pay(amount)
```

Burada `PaymentService` yeni bir `CryptoPayment` sınıfı geldiğinde değişmez. Yeni davranış arayüzü uygulayarak sisteme katılır. Yine de OCP uğruna her olasılık için soyutlama üretmek erken soyutlamadır; değişmesi muhtemel noktaları hedeflemek gerekir.

## 3. Liskov Substitution Principle (LSP)

**Liskov Yerine Geçme İlkesi**, bir alt türün üst tür beklenen her yerde programın doğruluğunu bozmadan kullanılabilmesini ister. Klasik `Kuş`–`Penguen` örneğinde, her kuşa `fly()` zorunluluğu vermek pengueni sahte bir uçuş davranışına iter. Sorun penguende değil, kötü soyutlamadadır.

Matematiksel sezgiyle, alt türün kabul ettiği girdiler üst türden daha dar olmamalı; ürettiği garantiler de daha zayıf olmamalıdır. Yani alt sınıf, üst sınıfın sözleşmesini ihlal edemez.

## 4. Interface Segregation Principle (ISP)

**Arayüz Ayrımı İlkesi**, istemcilerin kullanmadıkları metotlara bağımlı olmamasını söyler. `MultiFunctionPrinter` arayüzünde yazdırma, tarama ve faks varsa yalnızca yazdırabilen cihaz gereksiz metotları uygulamak zorunda kalır. Bunun yerine `Printable`, `Scannable` gibi küçük ve amaca yönelik sözleşmeler tercih edilir.

## 5. Dependency Inversion Principle (DIP)

**Bağımlılıkların Tersine Çevrilmesi İlkesi**, üst seviye iş kurallarının veritabanı, dosya sistemi veya e-posta kütüphanesi gibi ayrıntılara doğrudan bağlanmamasını önerir. Her ikisi de soyutlamaya bağımlı olmalıdır. Örneğin sipariş uygulaması `PostgresOrderRepository` yerine `OrderRepository` arayüzünü bilir; gerçek depo uygulaması dışarıdan enjekte edilir.

SOLID uygulandığında kod otomatik olarak kusursuz olmaz; sınıf sayısı da artabilir. Ancak test edilebilirlik, okunabilirlik ve değişiklik güvenliği yükselir. En iyi başlangıç, büyük bir yeniden yazım değil, her yeni özellikte “bu sorumluluk nereye ait?” sorusunu sormaktır. Bu küçük soru, mimarinin gelecekteki bakım faturalarını ciddi biçimde azaltır.
