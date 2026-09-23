---
layout: post
title: "ACID Gerçekte Ne Anlama Geliyor? Veritabanları Neden Bu Kadar Katı?"
math: true
categories: 
  - Bilgi
tags: 
  - acid
  - veritabanı
  - sql
  - transaction
  - backend
  - yazılım
toc: true
image: /img/acid-gercekte-ne-90.png
---

![acid-gercekte-ne-90](/img/acid-gercekte-ne-90.svg)


Bir banka hesabından diğerine para gönderdiğinizi düşünün. Para sizin hesabınızdan çıktı ama karşı tarafa ulaşmadıysa sistemin hızlı çalışması pek teselli olmaz. Veritabanlarının katılığı tam burada anlam kazanır: ACID, işlemlerin yalnızca çalışmasını değil, hata, elektrik kesintisi ve eşzamanlı kullanıcı baskısı altında bile doğru kalmasını sağlayan ilkeler bütünüdür.
``

## ACID bir temizlik ürünü değildir

ACID; **Atomicity, Consistency, Isolation ve Durability** kelimelerinin baş harflerinden oluşur. Türkçede bunlar atomiklik, tutarlılık, izolasyon ve kalıcılık olarak karşılanır. Birlikte, transaction adı verilen mantıksal işlemin güvenilirlik sözleşmesini oluştururlar.

Bir para transferini şu denklemle ifade edebiliriz:

$$B_{toplam}=B_A+B_B$$

A hesabından 100 TL düşüp B hesabına 100 TL eklediğimizde toplam bakiye değişmemelidir. İşlem ortada kesilir ve yalnızca ilk adım uygulanırsa denklem bozulur. ACID tam olarak bu tür yarım gerçeklikleri engeller.

| İlke | Temel soru | Engellediği sorun |
|---|---|---|
| Atomicity | İşlem tamamen gerçekleşti mi? | Yarım kalan güncelleme |
| Consistency | Kurallar işlem sonunda korunuyor mu? | Geçersiz veri |
| Isolation | Eşzamanlı işlemler birbirini görüyor mu? | Kirli veya kayıp okuma |
| Durability | Onaylanan veri kalıcı mı? | Çökme sonrası veri kaybı |

## Atomicity: Ya hep ya hiç

Atomiklik, transaction içindeki adımların tek parça kabul edilmesidir. İki sorgudan biri başarısız olursa başarılı olan da geri alınır. Veritabanı burada pazarlık yapmaz; biraz transfer diye bir durum yoktur.

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

Bu kod iki bakiyeyi aynı transaction içinde günceller. İkinci sorgu hata verirse uygulama `ROLLBACK` çalıştırarak ilk değişikliği geri almalıdır. Bazı sistemler hata durumunda transaction'ı otomatik olarak başarısız kabul eder.

## Consistency: Kurallar bozulamaz

Tutarlılık, verinin önceden tanımlanmış kurallara uygun kalmasıdır. Örneğin bakiye negatif olamaz, e-posta benzersiz olmalıdır veya sipariş mutlaka mevcut bir kullanıcıya bağlanmalıdır.

$$balance \geq 0$$

Bu koşul `CHECK`, `UNIQUE`, `FOREIGN KEY` gibi kısıtlarla veritabanına öğretilebilir:

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    balance DECIMAL(12, 2) NOT NULL,
    CHECK (balance >= 0)
);
```

Kuralları yalnızca uygulama koduna bırakmak risklidir. Çünkü aynı veritabanına başka servisler, yönetim araçları veya unutulmuş bir gece görevi de erişebilir.

## Isolation: Herkes aynı anda konuşmasın

İzolasyon, eşzamanlı transaction'ların birbirinin ara sonuçlarını görmesini sınırlar. İki müşterinin son ürünü aynı anda satın aldığını düşünün. İkisi de stok değerini 1 okuyup sipariş oluşturursa olmayan bir ürün satılabilir.

| İzolasyon seviyesi | Performans | Anomali riski |
|---|---:|---:|
| Read Uncommitted | Çok yüksek | Çok yüksek |
| Read Committed | Yüksek | Orta |
| Repeatable Read | Orta | Düşük |
| Serializable | Daha düşük | En düşük |

`Serializable`, işlemler sırayla çalışmış gibi sonuç üretir; ancak kilit beklemeleri veya yeniden denemeler yaratabilir. Yani daha güçlü doğruluk çoğu zaman daha fazla maliyet demektir.

## Durability: COMMIT sözünün ağırlığı

Kalıcılık, `COMMIT` cevabı alındıktan sonra verinin çökme yaşansa bile korunmasıdır. Veritabanları bunu çoğunlukla write-ahead log kullanarak sağlar. Değişiklik veri sayfasına yazılmadan önce günlük dosyasına kaydedilir. Sistem yeniden başladığında bu günlük oynatılarak onaylanmış işlemler kurtarılır.

Kabaca güvenilirliği şöyle düşünebiliriz:

$$Güvenilirlik = Doğruluk + Kurtarılabilirlik - Belirsizlik$$

Bu matematiksel bir veritabanı yasası değil, ACID'in amacını özetleyen zihinsel bir modeldir.

## Peki neden bu kadar katı?

Çünkü veritabanı, sistemin ortak hafızasıdır. Uygulama sunucusu yeniden başlatılabilir; fakat kaybolan ödeme, iki kez satılan bilet veya sahipsiz sipariş gerçek dünyada maliyet üretir. Yine de her işlem en yüksek izolasyona ihtiyaç duymaz. Beğeni sayacı geçici olarak birkaç sayı şaşabilirken banka bakiyesi şaşmamalıdır.

ACID'in mesajı basittir: Katılık bürokrasi değil, öngörülebilirliktir. Doğru transaction sınırları ve uygun izolasyon seviyesi seçildiğinde veritabanı yavaş bir bekçi değil, kaosun sisteme dönüşmesini engelleyen güvenilir bir hakem olur.
