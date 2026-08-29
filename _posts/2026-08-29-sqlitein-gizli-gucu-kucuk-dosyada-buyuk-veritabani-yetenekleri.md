---
layout: post
title: "SQLite'ın Gizli Gücü: Küçük Dosyada Büyük Veritabanı Yetenekleri"
math: true
categories: 
  - Bilgi
tags: 
  - SQLite
  - Veritabanı
  - SQL
  - Gömülü Sistemler
  - Performans
---

SQLite, çoğu geliştiricinin telefonunda, masaüstü uygulamasında veya küçük bir projede kullandığı “tek dosyalık veritabanı” olarak bilinir. Ancak onu yalnızca basit bir `SELECT` ve `INSERT` aracı saymak büyük haksızlık olur. Sunucu gerektirmemesi, yapılandırma maliyetinin düşük olması ve ACID garantileri sunması; SQLite’ı prototiplerden üretim sistemlerine uzanan etkileyici bir seçenek hâline getirir.

``

SQLite bir istemci-sunucu veritabanı değildir: uygulamanız doğrudan veritabanı dosyasıyla konuşur. Bu tasarım ağ gecikmesini ve ayrı bir servis yönetme zorunluluğunu kaldırır. Veriler çoğunlukla tek bir `.db` dosyasında saklanır; dolayısıyla yedek almak, taşımak veya test verisi hazırlamak şaşırtıcı derecede kolaydır. Küçük olması, yeteneklerinin küçük olduğu anlamına gelmez.

## ACID: Verinin Emniyet Kemeri

SQLite işlemleri ACID ilkelerine göre yürütür: Atomiklik, Tutarlılık, İzolasyon ve Dayanıklılık. Örneğin bir banka transferinde para gönderen hesaptan düşülürken alıcı hesaba ekleme başarısız olursa, işlem tamamen geri alınmalıdır. Matematiksel olarak bakiye korunumunu şöyle ifade edebiliriz:

$$\sum_{i=1}^{n} bakiye_{önceki} = \sum_{i=1}^{n} bakiye_{sonraki}$$

`BEGIN`, `COMMIT` ve `ROLLBACK` komutları bu güvenliği açıkça yönetmenizi sağlar:

```sql
BEGIN TRANSACTION;

UPDATE hesaplar
SET bakiye = bakiye - 250
WHERE id = 1 AND bakiye >= 250;

UPDATE hesaplar
SET bakiye = bakiye + 250
WHERE id = 2;

COMMIT;
```

Bu örnek, iki güncellemenin tek bir mantıksal operasyon gibi davranmasını sağlar. Uygulamada ayrıca ilk `UPDATE` satırının etkilediği kayıt sayısını kontrol ederek yetersiz bakiye durumunu `ROLLBACK` ile ele almak gerekir.

## WAL Modu: Okumalar Hız Kesmiyor

Varsayılan rollback journal yaklaşımı güvenlidir, fakat eşzamanlı okuma-yazma senaryolarında sınırlayıcı olabilir. Write-Ahead Logging (WAL) modunda değişiklikler önce ayrı bir günlük dosyasına yazılır. Böylece okuyucular, bir yazma işlemi sürerken eski ve tutarlı görüntüyü okumaya devam edebilir.

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
```

WAL özellikle mobil uygulamalar, yerel analiz araçları ve birden fazla okuma yapan masaüstü programları için kullanışlıdır. Yine de önemli bir ayrıntı vardır: SQLite aynı anda çok sayıda okuyucuyu desteklese de, temel olarak **tek yazıcı** modeline sahiptir. Çok yoğun paralel yazma gerektiren dağıtık servislerde PostgreSQL gibi sunucu tabanlı çözümler daha uygun olabilir.

| Özellik | SQLite | Sunucu Tabanlı Veritabanı |
|---|---|---|
| Kurulum | Tek kütüphane ve dosya | Servis, kullanıcı, ağ ayarı |
| Eşzamanlı yazma | Tek aktif yazıcı | Çoklu yazıcı için güçlü yapı |
| Taşınabilirlik | Çok yüksek | Dışa aktarma gerekir |
| İdeal kullanım | Yerel veri, edge, mobil | Merkezi ve yoğun sistemler |

## JSON, Tam Metin Arama ve Pencere Fonksiyonları

SQLite’ın modern yüzü burada parlar. JSON1 fonksiyonları, yarı yapılandırılmış veriyi SQL içinde sorgulamanıza imkân verir. Örneğin ayarları JSON olarak saklayıp belirli bir temayı filtreleyebilirsiniz:

```sql
SELECT kullanici_adi,
       json_extract(ayarlar, '$.tema') AS tema
FROM kullanicilar
WHERE json_extract(ayarlar, '$.bildirimler') = 1;
```

Arama kutusu yapıyorsanız FTS5 tam metin araması daha da etkileyicidir. `LIKE '%kelime%'` büyük metinlerde yorucu olabilirken, FTS5 ters indeks kullanarak kelimelere göre hızlı arama yapar. Pencere fonksiyonları da sıralama, hareketli ortalama ve grup içi derecelendirme gibi raporlama görevlerini sadeleştirir.

| İhtiyaç | SQLite özelliği | Kazanç |
|---|---|---|
| Ayar ve metadata saklama | JSON fonksiyonları | Esnek şema |
| Belge arama | FTS5 | Hızlı metin sorguları |
| Analitik rapor | Window functions | Daha okunur SQL |
| Veri bütünlüğü | Foreign key, trigger | Uygulama hatalarına direnç |

Son olarak indeksleri bilinçli kullanın. Sorgu maliyeti kabaca taranan satır sayısıyla büyür: $O(n)$. Uygun bir B-tree indeks ise birçok aramayı yaklaşık $O(\log n)$ seviyesine indirebilir. `EXPLAIN QUERY PLAN` ile SQLite’ın gerçekten indeks kullanıp kullanmadığını kontrol edin. Küçük başlayan SQLite veritabanınız, doğru işlem yönetimi, WAL, indeksler ve gelişmiş uzantılarla düşündüğünüzden çok daha uzun süre güçlü kalabilir.
