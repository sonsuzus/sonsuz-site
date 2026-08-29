---
layout: post
title: "ETL Süreçlerinde Data Profiling ve Doğrulama Kuralları Tasarlama"
math: true
categories: 
  - Bilgi
tags: 
  - etl
  - veri kalitesi
  - data profiling
---

ETL hattı, veriyi bir kaynaktan alıp dönüştürerek hedef sisteme taşıyan lojistik bir bant gibidir. Ancak bant hızlı çalışırken yanlış ürünleri paketliyorsa hızın pek anlamı kalmaz. Data profiling (veri profilleme), verinin istatistiksel ve yapısal röntgenini çekerek bu riski görünür yapar; doğrulama kuralları ise röntgen sonucuna göre kapıda bekleyen kalite kontrol ekibidir.
``

Veri kalitesi tek bir ölçüden ibaret değildir. Bir müşteri tablosunda e-posta alanının dolu olması **tamlık**, aynı müşterinin iki kez bulunmaması **benzersizlik**, ülke kodunun izinli listede olması **geçerlilik**, sipariş tarihinin müşteri oluşturulma tarihinden önce olmaması ise **tutarlılık** örneğidir. Bu boyutları sayısallaştırmak, “veri iyi görünüyor” gibi tehlikeli bir sezgiyi ölçülebilir bir hedefe dönüştürür.

Basit bir kalite skoru, her boyutun başarı oranını ağırlıklandırabilir:

$$Q = w_c C + w_v V + w_u U + w_t T$$

Burada $C$ tamlık, $V$ geçerlilik, $U$ benzersizlik, $T$ tutarlılık oranıdır; ağırlıkların toplamı $[1m1[0m olmalıdır. Örneğin finansal bir tabloda tutarlılık, pazarlama listesinden daha yüksek ağırlık alabilir. Kritik nokta şudur: Mükemmel kalite hedefi yerine, iş etkisine göre kabul edilebilir eşikler belirlenmelidir.

\vert  Boyut \vert  Profilde incelenen sinyal \vert  Örnek doğrulama \vert  Tipik eşik \vert 
\vert ---\vert ---\vert ---\vert ---\vert 
\vert  Tamlık \vert  Null ve boş değer oranı \vert  `email` boş olmamalı \vert  ≥ %99 \vert 
\vert  Benzersizlik \vert  Tekil değer sayısı \vert  `customer_id` yinelenmemeli \vert  %100 \vert 
\vert  Geçerlilik \vert  Desen, aralık, sözlük \vert  Tutar negatif olmamalı \vert  %100 \vert 
\vert  Tutarlılık \vert  Alanlar arası ilişki \vert  `end_date >= start_date` \vert  ≥ %99,9 \vert 
\vert  Güncellik \vert  Son yükleme zamanı \vert  Veri 24 saatten eski olmamalı \vert  ≤ 24 saat \vert 

Profil çıkarma araçları, kolon tipi, minimum-maksimum değerler, dağılımlar, boşluk oranları ve aykırı değerler gibi metrikleri otomatik üretir. **Great Expectations**, beklentileri test edilebilir veri sözleşmelerine dönüştürmek için güçlüdür. **Amazon Deequ** büyük Spark kümelerinde metrik hesaplama ve kural önerme avantajı sağlar. **Soda** ise SQL odaklı kontrolleri pipeline içine kolayca yerleştirir. Araç seçerken veri hacmi, işlem motoru, ekipteki SQL/Python yetkinliği ve uyarı altyapısı birlikte değerlendirilmelidir.

Aşağıdaki Great Expectations benzeri Python örneği, müşteri verisi için temel kalite kapısını gösterir:

```python
import great_expectations as gx

context = gx.get_context()
validator = context.sources.pandas_default.read_dataframe(
    asset_name="customers",
    dataframe=df
)

validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_unique("customer_id")
validator.expect_column_values_to_match_regex(
    "email", r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)
validator.expect_column_values_to_be_between(
    "age", min_value=18, max_value=120, mostly=0.995
)

results = validator.validate()
if not results.success:
    raise RuntimeError("Veri kalite kontrolü başarısız")
```

Bu kuralların görevi yalnızca hatayı bulmak değildir; hatalı verinin hedef tabloya ulaşmasını engellemektir. Yine de her kuralı “başarısızsa hattı durdur” şeklinde tasarlamak operasyonu kilitleyebilir. Kritik anahtar alanlarda **hard fail**, adres satırı gibi ikincil alanlarda ise uyarı üretip karantina tablosuna yönlendirme daha dengeli bir yaklaşımdır.

| Kural yaklaşımı | Davranış | Uygun kullanım |
|---|---|---|
| Hard fail | İş akışını durdurur | Birincil anahtar, muhasebe tutarı |
| Soft fail | Uyarı verir, akışı sürdürür | Opsiyonel açıklama alanları |
| Quarantine | Hatalı kayıtları ayırır | Tekil kayıt hataları |
| Drift alert | Dağılım değişimini bildirir | Ani fiyat veya hacim sıçramaları |

Son olarak profiling işlemini yalnızca ilk yüklemede çalıştırmayın. Referans metrikleri saklayın; satır sayısı, null oranı veya kategori dağılımı normal davranıştan sapınca alarm üretin. Böylece ETL süreci sadece veri taşıyan bir boru değil, veriye güveni sürekli ölçen akıllı bir kalite sistemi hâline gelir.
