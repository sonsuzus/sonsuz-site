---
layout: post
title: "MVCC Mantığı: Veritabanında Zaman Yolculuğu"
math: true
categories: 
  - Bilgi
tags: 
  - mvcc
  - veritabanı
  - eşzamanlılık
  - sql
  - postgresql
  - transaction
toc: true
---

Bir veritabanında aynı anda yüzlerce kullanıcı okuma ve yazma işlemi yaptığında işler kolayca trafik kavgasına dönüşebilir. MVCC, yani Çoklu Sürüm Eşzamanlılık Kontrolü, bu trafiği herkesi tek şeride sokmadan yönetir. Temel fikir şaşırtıcı derecede eğlencelidir: Bir satır değiştirildiğinde eski hâlini hemen yok etmek yerine farklı sürümler saklanır. Böylece okuyucular geçmişteki tutarlı görüntüyü incelerken yazarlar yeni sürüm üzerinde çalışabilir.

``

## MVCC neden gereklidir?

Klasik kilitleme yaklaşımında bir işlem satırı güncellerken diğer işlemler beklemek zorunda kalabilir. Uzun süren bir rapor sorgusu, sipariş eklemeye çalışan uygulamayı yavaşlatabilir. MVCC ise okuma işlemlerinin çoğunlukla yazma işlemlerini, yazmaların da okumaları engellememesini hedefler.

| Yaklaşım | Okuyucu davranışı | Yazar davranışı | Olası sonuç |
|---|---|---|---|
| Yoğun kilitleme | Kilidin açılmasını bekleyebilir | Satırı yerinde değiştirir | Bekleme ve kilitlenme |
| MVCC | Uygun eski sürümü okur | Yeni sürüm oluşturur | Daha yüksek eşzamanlılık |

Buradaki kritik kelime **uygun** kelimesidir. Her işlem, veritabanının belirli bir andaki mantıksal fotoğrafını, yani *snapshot* görüntüsünü görür. İşlem başladıktan sonra başka bir işlem değişiklik yapsa bile mevcut işlem izolasyon seviyesine bağlı olarak eski görüntüyü okumaya devam edebilir.

## Satır sürümleri nasıl çalışır?

Kavramsal olarak her satır sürümünde onu oluşturan ve geçersiz kılan işlem kimlikleri bulunabilir. Bunları $X_{min}$ ve $X_{max}$ ile gösterelim:

- $X_{min}$: Satır sürümünü oluşturan işlemdir.
- $X_{max}$: Satır sürümünü silen veya yerine yenisini koyan işlemdir.
- $S$: Okuma yapan işlemin snapshot bilgisidir.

Basitleştirilmiş görünürlük fikri şöyle ifade edilebilir:

$$Visible(row, S) = CreatedBeforeS \land NotDeletedBeforeS$$

Gerçek veritabanlarında algoritma daha karmaşıktır; işlemin tamamlanıp tamamlanmadığı, geri alınıp alınmadığı ve izolasyon seviyesi de hesaba katılır. Ancak zihinsel model nettir: Satır fiziksel olarak orada bulunsa bile her işlem onu görmek zorunda değildir.

Örneğin ürün stok değeri 10 iken A işlemi okumaya başlasın. B işlemi değeri 8 olarak güncelleyip işlemini tamamlasın. MVCC altında iki sürüm düşünülebilir:

| Sürüm | Stok | Kim görebilir? |
|---|---:|---|
| Eski sürüm | 10 | Değişiklikten önce snapshot alan A |
| Yeni sürüm | 8 | B tamamlandıktan sonra başlayan işlemler |

## SQL ile küçük bir senaryo

Aşağıdaki örnek PostgreSQL benzeri bir sistemde tutarlı okumanın davranışını gösterir:

```sql
-- A oturumu: Aynı snapshot üzerinden iki okuma yapar.
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT stok FROM urunler WHERE id = 42;
-- Sonuç: 10

-- B oturumu bu sırada stok değerini değiştirip COMMIT eder.

SELECT stok FROM urunler WHERE id = 42;
-- A işlemi hâlâ 10 görebilir.
COMMIT;
```

B oturumundaki işlem ise şöyle olabilir:

```sql
BEGIN;
UPDATE urunler SET stok = 8 WHERE id = 42;
COMMIT;
```

`UPDATE`, eski sürümü bütün okuyucular için anında ezmek yerine yeni bir satır sürümü üretir. Bu nedenle A işlemi yarıda farklı sonuç görmez; B sonrasında başlayan uygun işlemler ise 8 değerini okuyabilir.

## İzolasyon seviyesi fark yaratır

MVCC tek başına bütün anomalileri sihirli biçimde ortadan kaldırmaz. Görülecek snapshot, izolasyon seviyesine göre belirlenir.

| İzolasyon seviyesi | Snapshot davranışı | Risk veya maliyet |
|---|---|---|
| Read Committed | Her sorguda yenilenebilir | Aynı işlemde farklı sonuçlar |
| Repeatable Read | İşlem boyunca genellikle sabit | Eski sürümler daha uzun yaşar |
| Serializable | Seri çalışma etkisi hedeflenir | Çakışma ve yeniden deneme olabilir |

Özellikle iki işlemin aynı veriye dayanarak karar verdiği durumlarda yazma çakışmaları oluşabilir. Uygulama, başarısız işlemi yeniden çalıştırmaya hazır olmalıdır.

## Eski sürümler nereye gider?

Zaman yolculuğunun da temizlik faturası vardır. Artık hiçbir aktif snapshot tarafından görülemeyen sürümler temizlenmelidir. PostgreSQL bunu `VACUUM` mekanizmasıyla yönetirken başka sistemler undo alanları veya arka plan temizleyicileri kullanabilir. Çok uzun açık kalan işlemler temizliği geciktirerek tablo şişmesine ve depolama maliyetine yol açabilir.

Kısacası MVCC, veriyi tek bir değişken değil, zaman içinde oluşan sürümler dizisi gibi ele alır. Okuyucular tutarlı geçmişlerini görür, yazarlar geleceği hazırlar ve veritabanı hangi sürümün kime görünür olduğuna karar verir. Güçlü performansın bedeli ise doğru izolasyon seçimi, çakışma yönetimi ve düzenli sürüm temizliğidir.
