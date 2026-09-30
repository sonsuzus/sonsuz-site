---
layout: post
title: "Kırmadan Değiştirmek: Yazılım Mimarilerinde Geriye Dönük Uyumluluk"
math: true
categories: 
  - Bilgi
tags: 
  - yazılım mimarisi
  - geriye dönük uyumluluk
  - api
  - veritabanı
  - mesaj kuyruğu
  - sürümleme
toc: true
image: /img/kirmadan-degistirmek-yazilim-52.png
---

Bir sistemi geliştirmek kolaydır; onu yıllardır kullanan istemcileri kızdırmadan geliştirmek ise mühendislik sanatıdır. Mobil uygulamalar güncellenmeyebilir, başka ekipler eski SDK'ları kullanabilir ve kuyrukta dünün formatıyla üretilmiş mesajlar bekleyebilir. Geriye dönük uyumluluk, değişimi durdurmak değil, eski ve yeni dünyaların bir süre güvenle birlikte yaşamasını sağlamaktır.

``

## Uyumluluk ne anlama gelir?

Bir bileşenin yeni sürümü, önceki sürüm için geçerli girdileri kabul ediyor ve beklenen davranışı koruyorsa geriye dönük uyumludur. Bunu kabaca bir sözleşme kümeleri ilişkisiyle ifade edebiliriz. Eski sürümün kabul ettiği girdiler $I_{eski}$, yeni sürümünkiler $I_{yeni}$ ise güvenli değişimde:

$$I_{eski} \subseteq I_{yeni}$$

Benzer biçimde yeni sürümün çıktıları, eski tüketicinin anlayabileceği sözleşmeyi ihlal etmemelidir. Alan eklemek çoğunlukla güvenliyken alan silmek, tür değiştirmek veya anlamı sessizce dönüştürmek risklidir. Teknik uyumluluk kadar **anlamsal uyumluluk** da önemlidir: `status: active` değerinin anlamını değiştirmek, JSON biçimi aynı kalsa bile sözleşmeyi bozar.

| Değişiklik | Genellikle güvenli | Riskli yaklaşım |
|---|---|---|
| API alanı | İsteğe bağlı alan eklemek | Zorunlu alan eklemek |
| Veritabanı | Nullable sütun eklemek | Sütunu anında silmek |
| Mesaj | Varsayılanlı alan eklemek | Alan türünü değiştirmek |
| Davranış | Yeni endpoint sunmak | Mevcut sonucu değiştirmek |

![kirmadan-degistirmek-yazilim-52](/img/kirmadan-degistirmek-yazilim-52.svg)


## API sürümlerinde sözleşmeyi korumak

API'lerde ilk savunma hattı, açık bir sürümleme politikasıdır. `/api/v1/orders` gibi URL sürümleme görünürdür; header tabanlı sürümleme ise adresleri temiz tutar. Ancak sürüm numarası tek başına sihirli kalkan değildir. Eski sürüme güvenlik düzeltmeleri sağlanmalı, kullanım ölçülmeli ve kaldırma tarihi önceden duyurulmalıdır.

Eski yanıtı yeni modelden üreten bir adaptör, iş mantığının iki kez yazılmasını önler:

```python
def serialize_order(order, api_version):
    current = {
        "id": order.id,
        "total": order.total,
        "currency": order.currency
    }

    if api_version == "v1":
        return {
            "id": current["id"],
            "amount": current["total"]
        }

    return current
```

Bu kodda çekirdek model güncel kalırken `v1` istemcileri eski `amount` alanını almaya devam eder. Adaptörlerin sonsuza dek yaşamaması için telemetri ve sonlandırma planı şarttır.

## Veritabanında genişlet, taşı, daralt

Şema değişikliklerinde güvenli yöntem **expand-migrate-contract** desenidir. Önce yeni sütun eklenir, uygulama bir süre hem eski hem yeni alanı okuyup yazabilir, veriler taşınır ve yalnızca eski kod kalmadığı doğrulandıktan sonra eski sütun kaldırılır.

```sql
ALTER TABLE customers
ADD COLUMN full_name VARCHAR(200) NULL;

UPDATE customers
SET full_name = CONCAT(first_name, ' ', last_name)
WHERE full_name IS NULL;
```

Bu iki işlem dağıtımın tamamı değildir. Eski uygulama örnekleri hâlâ çalışırken `first_name` ve `last_name` sütunlarını silmek yarış koşulu yaratır. Önce çift yazma, ardından okumayı yeni alana geçirme ve en son temizlik yapılmalıdır. Büyük tablolarda kilitlenme süresi de ölçülmelidir.

## Mesaj kuyruklarında zaman yolculuğu

Mesajlar üreticiden daha uzun yaşayabilir. Bu nedenle tüketiciler bilinmeyen alanları yok saymalı, eksik alanlara varsayılan değer vermeli ve şema kimliği taşımalıdır.

```json
{
  "schemaVersion": 2,
  "orderId": "A-42",
  "priority": "normal"
}
```

Eski tüketici `priority` alanını görmezden gelebilir; yeni tüketici ise alan yoksa `normal` kabul edebilir. Avro veya Protobuf gibi şema sistemleri uyumluluk kontrollerini otomatikleştirir. Yine de olayın anlamını değiştirmek yerine `OrderCreatedV2` gibi yeni bir olay yayınlamak daha güvenlidir.

## Sağlam bir değişiklik kontrol listesi

- Tüketici odaklı sözleşme testleri çalıştırın.
- Eski ve yeni sürümleri aynı anda gözlemleyin.
- Kullanım oranı sıfırlanmadan eski sözleşmeyi kaldırmayın.
- Kaldırma tarihlerini dokümantasyon ve header'larla duyurun.
- Geri alma planını dağıtımdan önce hazırlayın.

Başarılı uyumluluk yönetimi, teknik borcu saklamak değil ona son kullanma tarihi vermektir. Sistem değişirken köprüler kurulur; trafik yeni yola geçtiğinde eski köprü kontrollü biçimde kapatılır. Balyoz en hızlı araç olabilir, fakat üretim ortamında nadiren en akıllısıdır.
