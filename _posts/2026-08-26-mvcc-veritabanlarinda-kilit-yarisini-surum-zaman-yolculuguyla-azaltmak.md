---
layout: post
title: "MVCC: Veritabanlarında Kilit Yarışını Sürüm Zaman Yolculuğuyla Azaltmak"
math: true
categories: 
  - Bilgi
tags: 
  - MVCC
  - Veritabanı
  - Eşzamanlılık
---

Bir veritabanında aynı müşteri kaydını yüzlerce kullanıcının aynı anda okumak ve güncellemek istediğini düşünün. Geleneksel kilitleme yaklaşımında bir yazma işlemi, okuyucuları bekletebilir; okuyucular da yazarı geciktirebilir. MVCC (Multi-Version Concurrency Control), yani Çok Sürümlü Eşzamanlılık Denetimi, bu trafik sıkışıklığını azaltmak için verinin tek bir kopyası yerine zaman damgalı birden fazla mantıksal sürümünü kullanır. PostgreSQL, MySQL InnoDB ve SQLite gibi sistemlerin farklı biçimlerde kullandığı bu fikir, yüksek eşzamanlılığın temel araçlarından biridir.
``

MVCC'nin ana fikri şaşırtıcı derecede sezgiseldir: Okuyucu, işlem başladığı anda veritabanının tutarlı bir fotoğrafını görür; yazar ise satırı yerinde ezmek yerine yeni bir sürüm üretir. Böylece uzun süren bir raporlama sorgusu, sipariş durumunu güncelleyen uygulamayı çoğu durumda durdurmaz. Elbette bu bir zaman makinesi değildir: Her işlem, **izolasyon seviyesi** tarafından izin verilen ölçüde geçmişin tutarlı bir görünümünü okur.

## Görünürlük: Hangi satır sürümü okunur?

Her satır sürümünü oluşturma ve silinme/geçersizleşme bilgileriyle modelleyebiliriz. Bir işlemin başlangıç anını $T$ kabul edelim. Sürümün oluşturulma zamanı $c$ ve geçersizleşme zamanı $d$ ise, basitleştirilmiş görünürlük kuralı şöyledir:

$$
visible(v, T) = (c \leq T) \land (d > T \;\text{veya}\; d = \infty)
$$

Gerçek veritabanları yalnızca zaman değil, işlem kimlikleri, commit durumları ve snapshot listeleri de kullanır. Yine de formül kritik fikri taşır: Bir okuyucu kendi başlangıç anında geçerli olan son sürümü seçer. Örneğin Ayşe'nin raporu 10:00'da başladıysa, 10:01'de yapılan fiyat güncellemesi rapora sonradan "sızmaz"; rapor kendi snapshot'ını korur.

| Özellik | Klasik kilitleme ağırlıklı yaklaşım | MVCC |
|---|---|---|
| Okuma-yazma ilişkisi | Sıkça bekleme oluşabilir | Okumalar çoğunlukla yazarı engellemez |
| Veri temsili | Genellikle tek güncel değer | Eski ve yeni sürümler birlikte bulunabilir |
| Tutarlılık | Kilit süresine bağlıdır | Snapshot üzerinden sağlanır |
| Bakım maliyeti | Kilit yönetimi baskındır | Eski sürüm temizliği gerekir |

## Küçük bir işlem senaryosu

Aşağıdaki PostgreSQL örneğinde iki oturum aynı ürüne dokunur. İlk oturum uzun süreli bir okuma yaparken ikinci oturum fiyatı günceller:

```sql
-- Oturum A: Tutarlı bir anlık görüntü alır
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT price FROM products WHERE id = 42;
-- Sonuç: 100

-- Oturum B: A devam ederken ayrı bir sürüm yazar
BEGIN;
UPDATE products SET price = 120 WHERE id = 42;
COMMIT;

-- Oturum A, kendi snapshot'ı nedeniyle hâlâ eski sürümü görür
SELECT price FROM products WHERE id = 42;
-- Sonuç: 100
COMMIT;
```

Bu kodun amacı, `REPEATABLE READ` altında aynı işlemin aynı satırı tekrar okuduğunda kararlı sonuç almasını göstermektir. A işlemi bittikten sonra başlatılan yeni bir işlem ise `120` değerini görür. Ancak MVCC, her yarış koşulunu sihirli biçimde çözmez. İki işlem aynı satırı güncellerse yazma-yazma çatışması hâlâ vardır; biri bekleyebilir veya hata/yeniden deneme alabilir.

| İzolasyon seviyesi | Tipik okuma davranışı | Dikkat edilmesi gereken risk |
|---|---|---|
| Read Committed | Her sorgu daha yeni snapshot görebilir | Tek işlemde tekrar okuma farklı sonuç verebilir |
| Repeatable Read | İşlem boyunca snapshot sabittir | Bazı motorlarda serialization hatası oluşabilir |
| Serializable | Sonuç, işlemler sırayla çalışmış gibi görünür | Yeniden deneme mantığı şarttır |

## Eski sürümlerin bedeli

MVCC'nin bedava öğle yemeği olmadığı noktası burada başlar. Eski sürümler, onları görebilecek aktif işlemler kalmayana kadar silinemez. PostgreSQL'de `VACUUM`, InnoDB'de purge mekanizması bu temizliğin parçasıdır. Çok uzun açık kalan transaction'lar, temizliği geciktirip disk şişmesine ve performans düşüşüne yol açabilir. Bu nedenle uygulamalarda transaction'ları kısa tutmak, indeksleri doğru seçmek ve serialization failure gibi geçici hatalarda kontrollü retry uygulamak önemlidir.

Özetle MVCC, okuyuculara tutarlı bir geçmiş, yazarlara ise daha az engellenen bir çalışma alanı sunar. Doğru izolasyon seviyesi ve sağlıklı bakım süreçleriyle birleştiğinde, yoğun veritabanı trafiğini kilit kuyruğundan çok daha akıcı bir sürüm akışına dönüştürür.
