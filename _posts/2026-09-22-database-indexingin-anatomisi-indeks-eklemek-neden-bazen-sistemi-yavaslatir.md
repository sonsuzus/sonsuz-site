---
layout: post
title: "Database Indexing’in Anatomisi: İndeks Eklemek Neden Bazen Sistemi Yavaşlatır?"
math: true
categories: 
  - Bilgi
tags: 
  - veritabanı
  - indeksleme
  - sql
  - performans
  - btree
  - optimizasyon
toc: true
image: /img/database-indexingin-anatomisi-25.png
---

Bir veritabanı indeksi, kitabın sonundaki alfabetik dizine benzer: Aradığınız bilgiye bütün sayfaları okumadan ulaşmanızı sağlar. Ancak kitaba her yeni cümle eklendiğinde dizini de güncellemek zorunda olduğunuzu düşünün. İşte indekslerin karanlık tarafı burada ortaya çıkar: Okumayı hızlandırırken yazma işlemlerine ek maliyet yüklerler.

``

## İndeksin içinde ne var?

Çoğu ilişkisel veritabanı, varsayılan olarak **B-tree** veya onun bir çeşidi olan **B+ tree** kullanır. Bu yapı verileri sıralı tutan, dengeli bir ağaçtır. Milyonlarca satır arasında doğrusal arama yapmak yerine kökten başlayıp uygun dalları izleriz.

İndekssiz bir taramanın yaklaşık maliyeti $O(n)$ iken dengeli bir ağaçta arama maliyeti yaklaşık olarak:

$$T(n) = O(\log_b n)$$

Buradaki $b$, her düğümün taşıyabildiği dal sayısıdır. Veritabanlarında bir düğüm genellikle disk sayfasına karşılık gelir. Dal sayısı yüksek olduğundan milyarlarca kayıt bile birkaç sayfa okumasıyla bulunabilir.

| Özellik | Tablo taraması | B-tree indeks araması |
|---|---|---|
| Yaklaşık maliyet | $O(n)$ | $O(\log n)$ |
| Büyük tablolarda arama | Yavaş | Genellikle hızlı |
| Ek depolama | Yok | Var |
| INSERT/UPDATE maliyeti | Daha düşük | Daha yüksek |
| Sıralama desteği | Ek işlem gerekebilir | İndeks sırası kullanılabilir |

## Okuma hızlanırken yazma neden yavaşlar?

Bir tabloya satır eklemek yalnızca veriyi diske yazmak değildir. Veritabanı, ilgili her indekse yeni anahtarı da yerleştirmelidir. Beş indeksiniz varsa tek `INSERT`, pratikte tabloyla beraber altı yapıyı değiştirebilir.

```sql
CREATE INDEX idx_orders_customer
ON orders (customer_id);

CREATE INDEX idx_orders_status
ON orders (status);
```

Bu indeksler müşteri ve durum sorgularını hızlandırabilir. Fakat her yeni siparişte iki indeks de güncellenir. Uygun ağaç sayfasında yer kalmadığında **page split** gerçekleşebilir: Sayfa bölünür, kayıtlar yeniden dağıtılır ve üst düğümler güncellenir. Bu süreç ek disk I/O’su, CPU kullanımı ve kilit süresi demektir.

Kabaca toplam yazma maliyetini şöyle düşünebiliriz:

$$C_{write} = C_{table} + \sum_{i=1}^{k} C_{index_i}$$

Burada $k$ indeks sayısıdır. İndeks sayısı arttıkça bakım maliyeti de büyür; üstelik bu ilişki yoğun eşzamanlılık altında daha can sıkıcı hâle gelebilir.

## Her indeks sorguyu hızlandırmaz

Seçiciliği düşük sütunlar tek başına kötü aday olabilir. Örneğin milyonlarca satırda yalnızca `active` ve `passive` değerlerini taşıyan bir `status` sütunu düşünün. Sorgu tablonun yarısını döndürecekse optimizer, indeks üzerinden yüz binlerce satıra rastgele erişmek yerine tabloyu baştan sona taramayı seçebilir.

```sql
EXPLAIN ANALYZE
SELECT *
FROM users
WHERE status = 'active';
```

Bu komut sorgunun gerçek çalışma planını ve sürelerini gösterir. Bir indeksin var olması, kullanılacağı anlamına gelmez. Veritabanı istatistikleri eskiyse optimizer yanlış plan bile seçebilir.

## Birleşik indekslerde sıra önemlidir

Aşağıdaki indeks, önce `customer_id`, sonra `created_at` değerine göre düzenlenir:

```sql
CREATE INDEX idx_orders_customer_date
ON orders (customer_id, created_at);
```

Bu yapı `customer_id` içeren sorgular için etkilidir. Yalnızca `created_at` ile filtreleme yapan bir sorgu ise çoğu durumda indeksten tam verim alamaz. Telefon rehberinin soyadına göre sıralıyken sadece adı bilinen kişiyi aramak gibi!

| Senaryo | Muhtemel sonuç |
|---|---|
| Sık okunan, seçici sütun | İndeks faydalı |
| Çok sık güncellenen sütun | Bakım maliyeti yüksek |
| Az sayıda farklı değer | Kazanç sınırlı olabilir |
| Doğru sıralanmış birleşik indeks | Birden fazla sorguyu hızlandırabilir |
| Kullanılmayan indeks | Depolama ve yazma yükü |

## Sağlıklı indeksleme yaklaşımı

Her sütuna indeks eklemek yerine yavaş sorguları ölçün, çalışma planlarını inceleyin ve gerçek iş yükünü temel alın. Kullanılmayan indeksleri veritabanının istatistik görünümleriyle tespit edin. Ayrıca indekslerin disk alanını, önbellek kullanımını ve `UPDATE` maliyetini artırdığını unutmayın.

İyi indeksleme, maksimum indeks sayısına ulaşma yarışı değildir. Amaç; okuma kazancı ile yazma, depolama ve bakım maliyeti arasında dengeli bir anlaşma yapmaktır. Kısacası indeks güçlü bir hızlandırıcıdır, fakat her hızlandırıcı gibi yanlış yerde kullanılırsa motoru yorabilir.

![database-indexingin-anatomisi-25](/img/database-indexingin-anatomisi-25.svg)

