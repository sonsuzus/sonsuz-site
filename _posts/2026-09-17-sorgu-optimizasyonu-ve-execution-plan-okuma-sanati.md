---
layout: post
title: "Sorgu Optimizasyonu ve Execution Plan Okuma Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - sql
  - veritabanı
  - sorgu optimizasyonu
  - execution plan
  - postgresql
  - performans
toc: true
image: /img/sorgu-optimizasyonu-ve-95.png
---

Bir SQL sorgusunun çalışması, garsona sipariş vermeye benzer: ne istediğinizi söylersiniz, fakat mutfakta hangi adımların izleneceğine şef karar verir. Veritabanındaki bu şef **query optimizer**, hazırladığı tarif ise **execution plan** olarak adlandırılır. Performans sorunlarını çözmek için yalnızca SQL yazmak değil, bu tarifi okuyup şefin neden o yolu seçtiğini anlamak gerekir.
``
## Sorgu optimizer gerçekte ne yapar?

SQL bildirimseldir; veriye *nasıl* ulaşılacağını değil, hangi sonucun istendiğini tarif eder. Optimizer tabloların istatistiklerini, indeksleri, olası birleştirme sıralarını ve tahmini veri miktarını değerlendirerek farklı planlar üretir. Ardından maliyeti en düşük görünen planı seçer.

Basitleştirilmiş biçimde toplam maliyet şöyle düşünülebilir:

$$C_{toplam} = C_{IO} + C_{CPU} + C_{bellek} + C_{ağ}$$

Buradaki maliyet doğrudan saniye değildir; planları karşılaştırmaya yarayan göreli bir puandır. Diskten çok sayfa okumak, milyonlarca satırı karşılaştırmak veya belleğe sığmayan bir sıralama yapmak bu puanı yükseltir.

## EXPLAIN ve EXPLAIN ANALYZE farkı

PostgreSQL üzerinde şu sorguyu inceleyelim:

```sql
EXPLAIN ANALYZE
SELECT o.id, o.total_amount
FROM orders AS o
WHERE o.customer_id = 42
  AND o.status = 'completed';
```

`EXPLAIN` sorguyu çalıştırmadan tahmini planı gösterir. `EXPLAIN ANALYZE` ise sorguyu gerçekten çalıştırarak tahminlerle gerçek sonuçları yan yana getirir. Üretim ortamında `UPDATE` veya `DELETE` ile kullanılırken dikkatli olunmalıdır; isimde “explain” bulunması değişikliği engellemez.

| Özellik | EXPLAIN | EXPLAIN ANALYZE |
|---|---|---|
| Sorguyu çalıştırır mı? | Hayır | Evet |
| Tahmini satır sayısı | Var | Var |
| Gerçek süre ve satır | Yok | Var |
| Güvenli inceleme | Genellikle | Yazma sorgularında riskli |

## Plan düğümlerini aşağıdan yukarı okuyun

Execution plan bir ağaçtır. En içteki ve en girintili düğüm önce çalışır; ürettiği satırlar üst düğüme aktarılır. Bu nedenle planı roman gibi yukarıdan aşağı değil, köklerden gövdeye doğru okumak daha doğrudur.

Sık karşılaşılan erişim yöntemleri şunlardır:

| Düğüm | Davranış | Ne zaman mantıklıdır? |
|---|---|---|
| `Seq Scan` | Tablonun tamamını tarar | Tablo küçükse veya satırların çoğu isteniyorsa |
| `Index Scan` | İndeksten satır konumunu bulur | Filtre seçiciliği yüksekse |
| `Index Only Scan` | Veriyi doğrudan indeksten okur | Gerekli sütunların tamamı indeksteyse |
| `Bitmap Heap Scan` | Eşleşmeleri toplu biçimde getirir | Orta miktarda satır seçiliyorsa |

Her `Seq Scan` kötü değildir. Bir sorgu tablonun yüzde 80’ini döndürecekse indeks ile tek tek sıçramak, tabloyu sırayla okumaktan pahalı olabilir. Seçicilik kabaca şu oranla ifade edilir:

$$S = N_{eşleşen} / N_{toplam}$$

$S$ küçüldükçe indeks kullanımı genellikle daha cazip hâle gelir.

## Tahmin ile gerçeği karşılaştırın

Plan okurken en değerli ipucu, `rows` tahmini ile `actual rows` değerinin farkıdır. Optimizer 10 satır beklerken 100.000 satır buluyorsa sonraki join ve sıralama kararları domino taşları gibi bozulabilir. Eski istatistikleri yenilemek için PostgreSQL’de şu komut kullanılabilir:

```sql
ANALYZE orders;
```

Büyük farkların diğer nedenleri ilişkili sütunlar, dengesiz veri dağılımı ve uygun olmayan indekslerdir. Örneğin sık kullanılan filtre için bileşik indeks oluşturulabilir:

```sql
CREATE INDEX idx_orders_customer_status
ON orders (customer_id, status);
```

Sütun sırası önemlidir; indeks bir telefon rehberi gibi soldan başlayarak düzenlenir. Sorgu kalıpları incelenmeden “her sütuna indeks” yaklaşımı uygulamak yazma maliyetini ve disk kullanımını artırır.

## Join algoritmaları ve son kontrol listesi

`Nested Loop` küçük bir sonuç kümesini indeksli tabloyla eşleştirirken etkilidir. `Hash Join`, büyük ve sırasız eşitlik birleştirmelerinde; `Merge Join` ise iki taraf sıralı olduğunda öne çıkar. Tek başına düğüm adına bakarak karar vermek yerine taşınan satır miktarını, döngü sayısını ve süreyi birlikte değerlendirin.

Optimizasyon sırasında önce en pahalı düğümü bulun, tahmini ve gerçek satırları karşılaştırın, filtrelerin erken uygulanıp uygulanmadığını kontrol edin. Sonra indeks, sorgu yazımı veya istatistik güncellemesi deneyin ve planı yeniden ölçün. Altın kural basittir: **tahmin etmeyin, ölçün; planı ezberlemeyin, veri akışını takip edin.**

![sorgu-optimizasyonu-ve-95](/img/sorgu-optimizasyonu-ve-95.svg)

