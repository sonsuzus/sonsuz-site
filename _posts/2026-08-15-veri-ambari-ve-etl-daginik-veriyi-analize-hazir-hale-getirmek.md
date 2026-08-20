---
layout: post
title: "Veri Ambarı ve ETL: Dağınık Veriyi Analize Hazır Hale Getirmek"
math: true
categories: 
  - Bilgi
tags: 
  - veri ambarı
  - etl
  - sql
---

Bir şirketin verileri genellikle tek bir yerde ve kusursuz biçimde yaşamaz: satışlar bir PostgreSQL veritabanında, müşteri kayıtları CRM sisteminde, kampanya sonuçları CSV dosyalarında ve uygulama olayları API günlüklerinde bulunur. Veri ambarı, bu dağınık parçaları karar vermeyi kolaylaştıran tutarlı bir analitik yapıda buluşturur. ETL süreçleri ise bu yapının görünmez ama vazgeçilmez lojistiğidir.
``

ETL, **Extract (çıkarma)**, **Transform (dönüştürme)** ve **Load (yükleme)** kelimelerinin kısaltmasıdır. İlk aşamada veriler kaynaklardan alınır. Ardından biçim, kalite ve iş kuralları bakımından dönüştürülür; son olarak veri ambarına yüklenir. Amaç yalnızca veriyi taşımak değil, aynı soruya herkesin aynı cevabı vermesini sağlamaktır. Örneğin satış ekibinin “gelir” tanımı ile finans ekibinin tanımı farklıysa, en parlak gösterge paneli bile kafa karıştırıcı olur.

Bir veri ambarı çoğunlukla analitik sorgular için modellenir. Operasyonel sistemler günlük işlemleri hızlı kaydetmeye odaklanırken, ambar tarihsel eğilimleri incelemeyi hedefler. Bu farkı aşağıdaki gibi özetleyebiliriz:

| Özellik | Operasyonel Veritabanı (OLTP) | Veri Ambarı (OLAP) |
|---|---|---|
| Ana amaç | Günlük işlem yürütmek | Analiz ve raporlama yapmak |
| Veri yapısı | Genellikle normalize | Yıldız veya kar tanesi şeması |
| Sorgu tipi | Kısa, sık ve kayıt odaklı | Büyük hacimli, toplulaştırmalı |
| Zaman boyutu | Güncel durum ağırlıklı | Tarihsel veri ağırlıklı |

Analitik modellemede sık kullanılan yıldız şemasında bir **olgu tablosu** ölçümleri saklar; **boyut tabloları** ise bu ölçümlere bağlam verir. `fact_sales` tablosunda satış tutarı ve miktar bulunabilir; tarih, ürün ve müşteri tabloları da “hangi gün, hangi ürün, kime?” sorularını cevaplar. Toplam gelir basitçe $R = \sum_{i=1}^{n} fiyat_i \times adet_i$ formülüyle hesaplanabilir. Ancak fiyatın para birimi, iade durumu veya indirim kuralı kaynaklar arasında farklıysa, bu formül ETL dönüşümü tamamlanmadan güvenilir değildir.

Dönüştürme aşamasının önemli görevlerinden biri veri kalitesidir. Yinelenen müşteri kayıtları birleştirilir, eksik değerler iş kuralına göre doldurulur veya işaretlenir, tarih formatları standartlaştırılır. Örneğin `31.07.2026`, `2026-07-31` ve zaman damgalı API değerleri tek bir standartta toplanmalıdır. Kaliteyi ölçmek için eksiksizlik oranı kullanılabilir: $C = \frac{dolu\ alan\ sayısı}{beklenen\ alan\ sayısı} \times 100$.

| Problem | Ham veri örneği | ETL yaklaşımı |
|---|---|---|
| Tekrarlı kayıt | Aynı e-posta ile iki müşteri | Doğal anahtar ve öncelik kuralı ile birleştirme |
| Biçim farkı | `TRY`, `₺`, `Turkish Lira` | Para birimini ISO koduna dönüştürme |
| Eksik değer | Ürün kategorisi boş | Referans tablodan tamamlama veya `Bilinmiyor` etiketi |
| Geçersiz değer | Negatif satış adedi | Karantina tablosuna alma ve doğrulama |

Aşağıdaki SQL örneği, ham sipariş verisini temizleyip analitik tabloya yükleyen basit bir dönüşümü gösterir. Gerçek projelerde bu işlem Airflow, dbt veya bulut orkestrasyon araçlarıyla zamanlanabilir.

```sql
INSERT INTO fact_sales (order_id, date_key, customer_key, revenue, quantity)
SELECT
  o.order_id,
  TO_CHAR(o.order_date, 'YYYYMMDD')::INT AS date_key,
  c.customer_key,
  ROUND(o.unit_price * o.quantity * (1 - COALESCE(o.discount, 0)), 2) AS revenue,
  o.quantity
FROM staging_orders o
JOIN dim_customer c ON LOWER(TRIM(o.customer_email)) = c.email
WHERE o.quantity > 0
  AND o.order_status = 'completed';
```

Burada `staging_orders` ham verinin güvenli iniş alanıdır. `TRIM` gereksiz boşlukları temizler, `LOWER` e-posta eşleştirmesini tutarlı hale getirir, `COALESCE` ise boş indirim değerini sıfır kabul eder. Geçersiz adetler ve tamamlanmamış siparişler özellikle filtrelenir.

Başarılı bir ETL hattı yalnızca çalışmakla kalmaz; izlenebilir de olmalıdır. Her yüklemede kayıt sayısı, hata oranı, kaynak zamanı ve dönüşüm sürümü kaydedilmelidir. Böylece bir rapordaki ani düşüşün gerçek bir iş sonucu mu, yoksa bozuk bir veri akışı mı olduğu anlaşılır. Kısacası veri ambarı rafları düzenler; ETL ise veriye güven duyulmasını sağlayan titiz kütüphanecidir.
