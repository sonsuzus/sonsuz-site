---
layout: post
title: "SQL’den NoSQL’e Veri Göçü: Dönüşüm Tuzakları ve Sağlam Çözüm Desenleri"
math: true
categories: 
  - Bilgi
tags: 
  - sql
  - nosql
  - veri göçü
toc: true
---

SQL ve NoSQL arasında veri göçü, yalnızca bir tablodan diğerine kayıt kopyalamak değildir; veri modelinin dünyayı yorumlama biçimini değiştirmektir. İlişkisel sistemler tutarlılığı tablolar, anahtarlar ve kısıtlarla korurken; NoSQL sistemleri ölçeklenebilirlik, esnek şema ve erişim desenlerini öne çıkarır. Bu nedenle başarılı bir göçün temel sorusu “Veriyi nasıl taşırım?” değil, “Uygulama bu veriyi hangi sorgularla kullanacak?” olmalıdır.
``

## Temel fark: Normalizasyon ile erişim odaklı modelleme

SQL dünyasında veri tekrarını azaltmak için normalizasyon uygulanır. Örneğin müşteri, sipariş ve sipariş kalemleri ayrı tablolardadır. NoSQL belge veritabanlarında ise bir sipariş okunurken kalemler de çoğunlukla gerektiğinden, bu bilgiler aynı belgenin içine gömülebilir. Bu yaklaşım okuma maliyetini azaltırken güncelleme karmaşıklığını yükseltebilir.

| Özellik | İlişkisel SQL | Belge tabanlı NoSQL |
|---|---|---|
| Şema | Önceden tanımlı ve katı | Esnek, alanlar değişken olabilir |
| İlişkiler | Foreign key ve JOIN | Gömme veya referans verme |
| Tutarlılık | Genellikle güçlü ACID | Ürüne göre eventual consistency olası |
| Modelleme odağı | Veri bütünlüğü | Sorgu ve erişim deseni |

Göç kararında basit bir maliyet modeli faydalıdır. Bir kaydın gömülmesiyle oluşan yaklaşık maliyet şöyle düşünülebilir: $C = R \times S + U \times D$. Burada $R$ okuma sayısını, $S$ belge boyutunu, $U$ güncelleme sayısını ve $D$ tekrar edilen veri miktarını temsil eder. Okumalar çok, güncellemeler azsa gömme genellikle avantajlıdır; tersi durumda referans kullanmak daha güvenlidir.

## En yaygın dönüşüm sorunları

İlk büyük problem, JOIN işlemleridir. SQL’de tek sorguyla müşteri-sipariş-kalem raporu üretmek kolaydır; NoSQL’de aynı sonuç için uygulama tarafında birden fazla sorgu gerekebilir. Çözüm, kritik okuma senaryoları için önceden birleştirilmiş belgeler veya materialized view koleksiyonları üretmektir.

İkinci sorun veri tipleridir. `DECIMAL(18,2)` alanının JavaScript tabanlı bir sürücüde `float` olarak işlenmesi para tutarlarında hassasiyet kaybına yol açabilir. Para değerlerini veritabanının decimal türünde ya da en küçük birimle tamsayı olarak saklamak daha güvenlidir: $12.34 \text{ TL} \rightarrow 1234 \text{ kuruş}$.

Üçüncü sorun boş değerlerdir. SQL’de `NULL`, bilinmeyen veya geçersiz değer anlamına gelebilir. NoSQL’de ise alanın hiç bulunmaması ayrı bir semantik taşır. Göç kuralları açıkça belirlenmelidir: `NULL` alanı korunacak mı, kaldırılacak mı, yoksa varsayılan değer mi atanacak?

| Sorun | Risk | Önerilen çözüm |
|---|---|---|
| JOIN bağımlılığı | Çoklu sorgu ve gecikme | Gömülü belge veya okuma modeli |
| Tür dönüşümü | Hassasiyet ve tarih kaybı | Tip eşleme sözleşmesi ve test |
| NULL / eksik alan | Yanlış iş kuralı | Açık null politikası |
| Kimlik üretimi | Çakışma veya izlenebilirlik kaybı | Kaynak ID’yi koruma, eşleme tablosu |
| Büyük koleksiyon | Uzun kesinti süresi | Batch, checkpoint ve artımlı taşıma |

## Kontrollü ETL yaklaşımı

Göç sürecini Extract, Transform, Load adımlarına ayırmak işi görünür kılar. Dönüşüm kodu, denetlenebilir ve tekrar çalıştırılabilir olmalıdır. Aşağıdaki örnek, SQL satırını sipariş belgesine dönüştüren basit bir Python fonksiyonudur:

```python
def order_to_document(order, items):
    return {
        "_id": str(order["id"]),
        "customerId": str(order["customer_id"]),
        "createdAt": order["created_at"].isoformat(),
        "totalCents": int(order["total"] * 100),
        "items": [
            {"productId": str(i["product_id"]), "quantity": i["qty"],
             "unitPriceCents": int(i["unit_price"] * 100)}
            for i in items
        ]
    }
```

Bu kodun amacı yalnızca format değiştirmek değildir; fiyat hassasiyetini, kimlik izlenebilirliğini ve sipariş-kalem bütünlüğünü korumaktır. Gerçek projede dönüşüm fonksiyonları için örnek kayıt testleri, beklenen JSON çıktıları ve hata günlükleri eklenmelidir.

Son aşama doğrulamadır. Kaynak ve hedefte kayıt sayısı karşılaştırılmalı, toplam tutarlar kontrol edilmeli ve rastgele örneklerde alan bazlı karşılaştırma yapılmalıdır. Kesintisiz geçiş gereken sistemlerde başlangıç aktarımından sonra değişiklik verisi yakalama (CDC) uygulanır. Böylece eski sistemdeki yeni işlemler hedefe akar; kısa bir son senkronizasyondan sonra trafik yeni veritabanına alınır. Başarılı göçün sırrı sihirli bir dönüştürücü değil, ölçülebilir kurallar, geri alma planı ve gerçek erişim desenlerine göre tasarlanmış bir hedeftir.
