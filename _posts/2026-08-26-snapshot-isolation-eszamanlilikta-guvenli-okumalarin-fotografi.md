---
layout: post
title: "Snapshot Isolation: Eşzamanlılıkta Güvenli Okumaların Fotoğrafı"
math: true
categories: 
  - Bilgi
tags: 
  - veritabanı
  - snapshot isolation
  - eşzamanlılık
---

Bir veritabanında aynı anda yüzlerce kullanıcının işlem yaptığını düşünün: biri bakiyesini güncellerken diğeri rapor alıyor, üçüncüsü aynı ürünü satın almaya çalışıyor. Snapshot Isolation (SI), her işleme verinin tutarlı bir “anlık görüntüsünü” vererek bu karmaşayı yönetmeye yardımcı olan izolasyon seviyesidir. Okuyucuların yazarları beklememesi sayesinde özellikle yoğun okuma yüklerinde oldukça akıcı bir deneyim sunar.
``

## Temel fikir: İşlemin kendi zaman kapsülü

SI altında bir işlem başladığında, veritabanının o ana kadarki **commit edilmiş** sürümlerinden mantıksal bir fotoğraf alınır. İşlem boyunca yapılan tüm okumalar bu fotoğrafa göre gerçekleştirilir. Başka bir işlem daha sonra değişiklik yapıp commit etse bile, ilk işlem bu yeni değişiklikleri kendi okuma kümesinde görmez.

Bir işlemin görünür veri kümesini kabaca şöyle ifade edebiliriz:

$$V(T) = \{x \mid commit(x) \leq start(T)\}$$

Burada $start(T)$ işlemin başladığı anı, $commit(x)$ ise bir veri sürümünün kesinleşme zamanını temsil eder. İşlem kendi yazdıklarını elbette görür; fakat diğer işlemlerin sonradan tamamlanan yazıları, onun fotoğrafına dahil değildir.

Bu yaklaşım çoğunlukla **MVCC** (Multi-Version Concurrency Control) ile uygulanır. Tek bir satırın üzerine yazmak yerine sistem, satırın birden fazla sürümünü tutar. Böylece rapor sorgusu eski ama tutarlı sürümü okurken güncelleme işlemi yeni sürümü hazırlayabilir. Aynı masada herkesin konuşması yerine, herkesin elinde toplantı başlangıcındaki notların olması gibi düşünebilirsiniz.

| Özellik | Read Committed | Snapshot Isolation | Serializable |
|---|---|---|---|
| Her sorguda yeni veriyi görme | Evet | Hayır | Uygulamaya bağlı |
| İşlem boyunca tutarlı görünüm | Hayır | Evet | Evet |
| Okuma-yazma bekleşmesi | Değişken | Genellikle düşük | Daha yüksek olabilir |
| Write skew riski | Var | Var | Yok |
| Performans maliyeti | Düşük | Dengeli | Görece yüksek |

## Çatışma anında ne olur?

SI, özellikle **lost update** sorununu azaltır. İki işlem aynı satırı değiştirmeye çalışırsa, ilk commit eden kazanır; diğer işlem çoğu sistemde hata alır ve yeniden denenmelidir. PostgreSQL gibi MVCC kullanan sistemlerde bu durum sıklıkla `could not serialize access due to concurrent update` benzeri bir hata olarak uygulamaya yansır.

Örneğin stok düşme işlemi için koşullu güncelleme kullanmak, iş mantığını veritabanına yaklaştırır:

```sql
BEGIN;

UPDATE products
SET stock = stock - 1
WHERE id = 42
  AND stock > 0;

-- Etkilenen satır sayısı 1 ise rezervasyon başarılıdır.
COMMIT;
```

Bu kod, stok negatif olmasın kuralını atomik biçimde uygular. Ancak uygulama, güncellemeden etkilenen satır sayısını mutlaka kontrol etmelidir. `0` satır etkilenmişse ürün bitmiştir ya da işlem görünür sürüm nedeniyle yeniden denenmelidir.

## SI her derde deva mı? Hayır: Write skew

SI, aynı satıra yazma çatışmasını yakalasa da farklı satırlara yazan işlemlerin birlikte bir iş kuralını bozmasını engellemeyebilir. Buna **write skew** denir. Klasik örnekte nöbette en az bir doktor bulunmalıdır. İki doktor da aynı anda “diğer doktor nöbette” bilgisini kendi snapshot’ında görür ve kendi satırındaki nöbet durumunu kapatır. Farklı satırları değiştirdikleri için doğrudan çakışma oluşmaz; ama sonuçta nöbette kimse kalmaz.

| Senaryo | SI davranışı | Önerilen çözüm |
|---|---|---|
| Aynı ürün satırını güncelleme | Çatışan yazı engellenir | Retry mekanizması |
| Rapor ve güncelleme eşzamanlılığı | Tutarlı eski görünüm | SI/MVCC uygundur |
| Satırlar arası iş kuralı | Write skew oluşabilir | Serializable veya kilit |
| Para transferi | Kural karmaşıksa riskli | Serializable + kısıtlar |

Kritik kurallarda `SERIALIZABLE` izolasyon seviyesine geçmek, uygun satırları `SELECT ... FOR UPDATE` ile kilitlemek veya benzersiz kısıtlar ve tetikleyiciler kullanmak gerekir. En iyi seçim, “hız mı, en güçlü doğruluk garantisi mi?” sorusunun cevabına bağlıdır.

Sonuç olarak Snapshot Isolation, okuma ağırlıklı sistemlerde tutarlılık ve performans arasında güçlü bir denge kurar. Fakat sihirli değnek değildir: uygulamanın iş kurallarını, tekrar deneme stratejisini ve olası write skew senaryolarını tasarlarken açıkça modellemek gerekir.
