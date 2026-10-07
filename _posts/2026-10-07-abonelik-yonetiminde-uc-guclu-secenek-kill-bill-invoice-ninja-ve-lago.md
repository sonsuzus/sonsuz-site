---
layout: post
title: "Abonelik Yönetiminde Üç Güçlü Seçenek: Kill Bill, Invoice Ninja ve Lago"
math: true
categories: 
  - Program
tags: 
  - abonelik
  - faturalandırma
  - kill bill
  - invoice ninja
  - lago
  - saas
  - fintech
toc: true
image: /img/abonelik-yonetiminde-uc-33.png
---

Abonelik tabanlı bir ürün geliştirirken kredi kartından ödeme almak işin yalnızca görünen kısmıdır. Plan değişiklikleri, kullanım ölçümü, vergi, kupon, dönem ortası ücretlendirme ve başarısız tahsilatlar devreye girdiğinde küçük fatura modülü hızla minik bir muhasebe canavarına dönüşür. Kill Bill, Invoice Ninja ve Lago bu canavarı evcilleştirmeyi amaçlar; ancak aynı problemi farklı açılardan ele alırlar.


![abonelik-yonetiminde-uc-33](/img/abonelik-yonetiminde-uc-33.svg)

``

## Önce problemi doğru tanımlayalım

Bir abonelik sisteminde **billing**, müşterinin ne kadar borçlandığını hesaplar; **invoicing**, bu borcu resmi veya ticari bir belgeye dönüştürür; **payment processing** ise paranın tahsil edilmesini sağlar. Bu kavramları tek sepete atmak, ileride mimari karmaşaya yol açabilir.

Basit bir aylık ücret şu şekilde gösterilebilir:

$$T = S + (q \times p) - d + v$$

Burada $S$ sabit abonelik ücreti, $q$ tüketilen miktar, $p$ birim fiyat, $d$ indirim ve $v$ vergi tutarıdır. Kullanım bazlı bir SaaS ürününde asıl zorluk, $q$ değerini güvenilir biçimde toplamak ve doğru döneme yerleştirmektir.

## Üç aracın karakteri

| Araç | Temel odak | Güçlü olduğu senaryo | Dikkat edilmesi gereken nokta |
|---|---|---|---|
| Kill Bill | Abonelik, katalog, ödeme ve faturalandırma altyapısı | Karmaşık yaşam döngüsü ve ödeme akışları | Kurulum ve operasyon bilgisi ister |
| Invoice Ninja | Teklif, fatura ve müşteri yönetimi | Serbest çalışanlar ve hizmet şirketleri | İleri düzey kullanım ölçümü ana odağı değildir |
| Lago | Kullanım bazlı ve hibrit ücretlendirme | API tabanlı modern SaaS ürünleri | Tahsilat ve muhasebe entegrasyonları ayrıca tasarlanmalıdır |

### Kill Bill: Ağır sıklet motor

Kill Bill, abonelik yaşam döngüsünü ayrıntılı yönetmek isteyen ekipler için güçlüdür. Deneme süresi, yükseltme, düşürme, iptal, ödeme eklentileri ve gecikmiş hesap politikaları gibi konularda geniş bir model sunar. Birden fazla ödeme sağlayıcısını destekleyen, kuralları zamanla karmaşıklaşacak bir platform kuruyorsanız iyi bir adaydır.

Bunun bedeli operasyonel karmaşıklıktır. Kill Bill yalnızca birkaç API çağrısı yapıp unutacağınız hafif bir araç değildir. Katalog tasarımı, eklentiler, veri tabanı, olaylar ve sürüm yükseltmeleri için sahiplik gerekir.

### Invoice Ninja: Fatura tarafının pratik ustası

Invoice Ninja daha çok müşteriye teklif hazırlama, fatura gönderme, ödeme takibi ve gider yönetimi gibi iş süreçlerinde parlar. Ajanslar, danışmanlar ve küçük işletmeler için anlaşılır bir merkez oluşturur. Müşteri portalı ve yinelenen faturalar sayesinde klasik abonelik ihtiyaçlarını da karşılayabilir.

Ancak saniyede binlerce kullanım olayı üreten bir API platformunda, karmaşık ölçüm ve kademeli fiyatlama için tek başına ideal motor olmayabilir. Burada Invoice Ninja son belgeyi oluşturan katman olarak değerlendirilebilir.

### Lago: Kullanım bazlı SaaS yaklaşımı

Lago; API çağrısı, depolama miktarı veya aktif kullanıcı sayısı gibi olaylardan ücret üretmeye odaklanır. Sabit ücret ile tüketimi birleştiren hibrit modellerde esnektir. Örneğin ilk 10.000 isteğin pakete dahil, sonraki her 1.000 isteğin ücretli olduğu bir plan modellenebilir.

Uygulamanın Lago'ya tutarlı olay göndermesi gerekir:

```python
import requests

payload = {
    "transaction_id": "evt_98421",
    "external_customer_id": "customer_42",
    "code": "api_request",
    "properties": {"requests": 1250}
}

requests.post(
    "https://billing.example.com/api/v1/events",
    json=payload,
    timeout=5
).raise_for_status()
```

Bu kod, müşterinin ölçülen API kullanımını tekil işlem kimliğiyle faturalandırma sistemine iletir. `transaction_id`, tekrar gönderilen olayların çift ücret üretmesini önlemeye yardımcı olur. Üretimde kuyruk, yeniden deneme ve gözlemlenebilirlik de eklenmelidir.

## Hangisini seçmeli?

Kararı özellik listesinden önce iş modeline göre verin. Karmaşık abonelik ve tahsilat orkestrasyonu için **Kill Bill**, kolay fatura ve müşteri operasyonları için **Invoice Ninja**, olay tabanlı ücretlendirme için **Lago** daha doğal seçimdir. Bazı mimarilerde Lago kullanım tutarını hesaplar, Invoice Ninja belgeyi üretir; Kill Bill ise ödeme yaşam döngüsünü yönetir. Yani bunlar her zaman rakip değil, doğru sınırlar çizildiğinde aynı orkestranın farklı enstrümanlarıdır.
