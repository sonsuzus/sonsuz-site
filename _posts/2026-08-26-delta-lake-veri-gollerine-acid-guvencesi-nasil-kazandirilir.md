---
layout: post
title: "Delta Lake: Veri Göllerine ACID Güvencesi Nasıl Kazandırılır?"
math: true
categories: 
  - Bilgi
tags: 
  - delta lake
  - veri mühendisliği
  - acıd
  - apache spark
  - data lake
---

Veri gölleri; CSV, JSON, Parquet ve log dosyaları gibi büyük hacimli verileri ekonomik biçimde saklamak için harikadır. Ancak klasik bir veri gölü, aynı tabloya eşzamanlı yazan işler, yarıda kalan yüklemeler veya değişen şemalar karşısında kolayca karmaşaya dönüşebilir. Delta Lake, açık kaynaklı depolama katmanıyla bu esnek dünyaya veri ambarı disiplinini getirir: ACID işlemleri, sürüm geçmişi, şema denetimi ve güvenilir güncellemeler.
``

Delta Lake bir veritabanı değildir; mevcut bulut depolamasının ya da HDFS'in üzerinde çalışan bir **tablo formatı ve işlem günlüğü** yaklaşımıdır. Verinin kendisi çoğunlukla Parquet dosyalarında bulunur. Tablo klasöründeki `_delta_log` dizini ise hangi dosyaların tabloya ait olduğunu, hangi işlemin ne zaman yapıldığını ve tablonun hangi sürümde bulunduğunu kaydeder. Böylece klasörde fiziksel olarak duran her Parquet dosyası otomatik olarak “geçerli veri” sayılmaz.

Temel fikir, her değişikliğin atomik bir taahhüt (commit) olarak günlüğe yazılmasıdır. Örneğin bir ETL işi yeni dosyalar üretir; ardından Delta günlüğüne bu dosyaları ekleyen bir kayıt oluşturur. İşlem günlüğe yazılmadan önce çökerse okuyucular eski sürümü görmeye devam eder. Bu yaklaşım, basitçe şöyle özetlenebilir:

$$\text{Yeni Tablo Durumu} = \text{Eski Durum} + \text{Eklenen Dosyalar} - \text{Kaldırılan Dosyalar}$$

Bu modelin kalbinde **ACID** özellikleri vardır. Atomicity, bir yazmanın ya tamamen görünür olmasını ya da hiç görünmemesini sağlar. Consistency, şema ve kısıtların korunmasına yardım eder. Isolation, eşzamanlı okuyucu ve yazıcıların tutarlı bir görünümle çalışmasını sağlar. Durability ise başarıyla tamamlanan işlemlerin kalıcı depolamada korunmasıdır.

| Özellik | Klasik Parquet klasörü | Delta Lake tablosu |
|---|---|---|
| Eşzamanlı yazma | Dosya çakışması riski | İşlem günlüğüyle denetim |
| `UPDATE` / `DELETE` | Genellikle tüm veriyi yeniden üretme | Mantıksal dosya ekleme-kaldırma |
| Şema değişimi | Sessiz veri bozulması riski | Şema doğrulama ve evrim |
| Geçmişe erişim | Manuel yedek gerektirebilir | Time travel ile sürüm okuma |
| Hatalı işlem geri alma | Zor ve maliyetli | Sürüm tabanlı inceleme |

Delta Lake çoğunlukla Apache Spark ile kullanılır. Aşağıdaki örnek, bir DataFrame'i Delta formatında yazıp tabloyu yeniden okur. `mode("append")`, mevcut tabloya yeni kayıtlar eklemek için kullanılır; Delta ise eklenen dosyaları transaction log üzerinden görünür hale getirir.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("delta-ornek") \
    .getOrCreate()

veri = [(1, "Ada", 95), (2, "Deniz", 88)]
df = spark.createDataFrame(veri, ["id", "ad", "puan"])

konum = "/data/ogrenci_delta"
df.write.format("delta").mode("append").save(konum)

sonuc = spark.read.format("delta").load(konum)
sonuc.show()
```

Delta'nın dikkat çekici özelliği **time travel**dır. Her commit bir sürüm oluşturduğu için geçmişteki tutarlı bir tablo anı okunabilir. Bu, hatalı bir veri yüklemesinin etkisini analiz ederken son derece kullanışlıdır. Örneğin aşağıdaki kod, tablonun sıfırıncı sürümünü okur:

```python
eski_df = spark.read.format("delta") \
    .option("versionAsOf", 0) \
    .load("/data/ogrenci_delta")
```

Burada önemli bir ayrım vardır: Delta, satırları yerinde değiştirmek yerine çoğu zaman etkilenen Parquet dosyalarını yeni sürümleriyle değiştirir. Eski dosyalar bir süre saklanabilir; `VACUUM` komutu artık gerekli olmayan fiziksel dosyaları temizler. Bu nedenle saklama süresi politikaları düşünülmeden agresif temizlik yapmak, time travel yeteneğini azaltabilir.

Şema denetimi de veri kalitesinin görünmez kahramanıdır. Beklenmeyen bir sütun tipiyle gelen veri, sessizce tabloya karışmak yerine reddedilebilir. Kontrollü şema evrimi sayesinde yeni sütun eklemek mümkündür; fakat bu esneklik, veri sözleşmeleri ve testlerle birlikte kullanılmalıdır.

Sonuç olarak Delta Lake, veri gölünü yalnızca “dosyaların yaşadığı yer” olmaktan çıkarır. Parquet'in açık ve verimli yapısını korurken işlem günlüğüyle güven, tekrar üretilebilirlik ve analiz edilebilir geçmiş sağlar. Özellikle lakehouse mimarisinde, ham veriden güvenilir raporlama katmanına uzanan yolun sağlam zeminidir.
