---
layout: post
title: "Veritabanı Normalizasyonu ve Denormalizasyon: Bütünlük ile Hız Arasında Akıllı Denge"
math: true
categories: 
  - Bilgi
tags: 
  - veritabanı
  - normalizasyon
  - denormalizasyon
toc: true
---

Veritabanı tasarımı, yalnızca tabloları yan yana dizmek değildir; verinin doğru, tutarlı ve hızlı erişilebilir kalmasını sağlayan bir mimari karar sürecidir. Normalizasyon tekrarları azaltarak veri bütünlüğünü korur, denormalizasyon ise bazı tekrarları bilinçli biçimde kabul ederek okuma performansını artırır. İyi tasarımcı, bu iki yaklaşımı rakip değil, farklı ihtiyaçlara hizmet eden araçlar olarak görür.
``

## Normalizasyonun teorik temeli

Normalizasyon, ilişkisel veritabanındaki bağımlılıkları analiz ederek her bilginin mümkün olduğunca **tek bir yerde** tutulmasını hedefler. Böylece aynı müşteri adresi on farklı sipariş satırında güncellenmek zorunda kalmaz. Temel fikir, bir niteliğin yalnızca onu belirleyen anahtara bağlı olmasıdır.

Fonksiyonel bağımlılığı şu şekilde yazabiliriz:

$$MusteriID \rightarrow MusteriAdi, Eposta$$

Bu ifade, `MusteriID` biliniyorsa müşteri adı ve e-posta bilgisinin belirlendiğini anlatır. Buna karşılık sipariş tablosunda müşteri adını da saklamak, aynı olgunun iki farklı yerde yaşamasına neden olur. İşte güncelleme anomalileri burada sahneye çıkar: Müşteri adını değiştirdiniz, ama üç eski siparişte unutuldu. Veritabanı küçük bir tutarsızlık partisindedir.

| Normal Form | Ana amaç | Kısa kontrol sorusu |
|---|---|---|
| 1NF | Atomik alanlar, tekrar eden grup yok | Bir hücrede tek değer var mı? |
| 2NF | Kısmi bağımlılığı kaldırmak | Alanlar bileşik anahtarın tamamına mı bağlı? |
| 3NF | Geçişli bağımlılığı kaldırmak | Anahtar dışı alan başka anahtar dışı alana mı bağlı? |
| BCNF | Daha sıkı belirleyici kuralı | Her belirleyici aday anahtar mı? |

Örneğin `Siparisler(SiparisID, MusteriID, MusteriAdi, UrunID, UrunAdi, Adet)` tasarımı ilk bakışta pratik görünür. Ancak `MusteriAdi` müşteriyle, `UrunAdi` ise ürünle ilişkilidir; sipariş satırına ait değillerdir. Daha sağlıklı yapı, bu verileri `Musteriler`, `Urunler`, `Siparisler` ve `SiparisKalemleri` tablolarına ayırmaktır.

## Denormalizasyon ne zaman mantıklıdır?

Normalleştirilmiş yapı yazma işlemlerinde güvenlidir; fakat raporlar çok sayıda tabloyu birleştiriyorsa (`JOIN`), okuma maliyeti artabilir. Özellikle analiz ekranları, ürün katalogları, liderlik tabloları ve yüksek trafikli API uçları denormalizasyon adaylarıdır.

Basitleştirilmiş maliyet düşüncesi şöyledir:

$$Toplam\ Maliyet = Okuma\ Sayisi \times Okuma\ Maliyeti + Yazma\ Sayisi \times Yazma\ Maliyeti$$

Okuma sayısı yazmadan katbekat fazlaysa, sipariş toplamını her istekte yeniden hesaplamak yerine saklamak avantaj sağlayabilir. Ancak bunun bedeli, toplamın güncel tutulmasıdır.

```sql
CREATE TABLE siparis_ozetleri (
  siparis_id BIGINT PRIMARY KEY,
  musteri_adi VARCHAR(150) NOT NULL,
  toplam_tutar DECIMAL(12,2) NOT NULL,
  kalem_sayisi INT NOT NULL,
  guncellenme_zamani TIMESTAMP NOT NULL
);
```

Bu özet tablo, raporlama ekranının karmaşık birleşimler yerine tek sorguyla çalışmasını sağlar. Fakat `musteri_adi` burada kopyalanmış veridir. Müşteri adı değiştiğinde bu tabloyu güncelleyen bir uygulama akışı, tetikleyici ya da periyodik yenileme mekanizması gerekir.

| Yaklaşım | Avantaj | Risk | Uygun senaryo |
|---|---|---|---|
| Normalizasyon | Tutarlılık, kolay güncelleme | Çoklu JOIN maliyeti | İşlemsel sistemler |
| Denormalizasyon | Hızlı okuma, sade sorgular | Bayat veya çelişkili veri | Raporlama ve analiz |
| Materialized view | Kontrollü özet veri | Yenileme gecikmesi | Dashboard'lar |
| Önbellek | Çok hızlı erişim | Geçersizleştirme sorunu | Sık okunan geçici veri |

## Dengeyi kurmanın pratik yolu

Önce normalleştirin, sonra gerçek ölçümlerle darboğazları bulun. Sadece “JOIN yavaştır” varsayımıyla kopya veri üretmek, geleceğin bakım maliyetini davet eder. Sorgu planlarını inceleyin, doğru indeksleri ekleyin ve yavaş sorgunun gerçekten nerede zaman harcadığını ölçün. Denormalizasyon gerekiyorsa, hangi alanın kaynak veri olduğunu açıkça tanımlayın; güncelleme stratejisini ve tutarlılık beklentisini dokümante edin.

Kısacası normalizasyon varsayılan güvenlik kemerinizdir; denormalizasyon ise yarış pistinde takılan turbo gibidir. Turbo etkileyicidir, ama motorun geri kalanını hesaba katmadan kullanılırsa yolculuğu hızlandırmak yerine karmaşıklaştırır.
