---
layout: post
title: "ACID Özellikleri ve İşlem Yönetimi: Veritabanlarının Güven Sözleşmesi"
math: true
categories: 
  - Bilgi
tags: 
  - veritabanı
  - acıd
  - sql
  - işlem yönetimi
toc: true
image: /img/acid-ozellikleri-ve-70.png
---

Bir banka hesabından para transferi düşünün: Gönderenin bakiyesi azalırken alıcının bakiyesi artmalıdır; arada elektrik kesilse, iki kullanıcı aynı hesaba erişse veya sistem yeniden başlasa bile sonuç güvenilir kalmalıdır. Veritabanı işlemleri (transaction), birden fazla sorguyu tek bir mantıksal iş olarak paketler. ACID ise bu paketin kaotik gerçek dünyada güvenle çalışmasını sağlayan dört temel ilkedir.


![acid-ozellikleri-ve-70](/img/acid-ozellikleri-ve-70.svg)

``

## İşlem nedir ve neden gereklidir?

Bir işlem, genellikle `BEGIN` ile başlayıp `COMMIT` ya da `ROLLBACK` ile biten sorgu grubudur. Başarılıysa tüm değişiklikler kalıcılaşır; hata varsa sistem önceki güvenli duruma döner. Transfer örneğinde temel değişmez (invariant) şudur:

$$B_{gönderen} + B_{alıcı} = Sabit$$

Tek tek `UPDATE` sorgularını bağımsız çalıştırmak bu eşitliği geçici veya kalıcı biçimde bozabilir. İşlem yönetimi, bu sorguları birbirinden koparılamayan bir bütün hâline getirir.

| Kavram | Sorduğu soru | Koruduğu şey |
|---|---|---|
| Atomiklik | İşin tamamı bitti mi? | Yarım kalmış değişiklikler |
| Tutarlılık | Kurallar hâlâ geçerli mi? | Veri bütünlüğü |
| İzolasyon | Eşzamanlı işler birbirini görüyor mu? | Yarış koşulları |
| Kalıcılık | Onaylanan veri kaybolur mu? | Çökme sonrası veri |

## A: Atomiklik — ya hep ya hiç

Atomiklik, işlemin bölünemez olmasıdır. Transferde ilk bakiye güncellenip ikinci güncelleme başarısız olursa, ilk değişiklik de geri alınmalıdır. Bu davranış genellikle hata kayıtları, undo log’lar veya MVCC sürüm mekanizmalarıyla desteklenir. Uygulama tarafında da başarısızlığı yakalayıp geri alma çağrısı yapmak gerekir.

```sql
BEGIN;

UPDATE hesaplar
SET bakiye = bakiye - 500
WHERE id = 10 AND bakiye >= 500;

UPDATE hesaplar
SET bakiye = bakiye + 500
WHERE id = 24;

COMMIT;
```

Bu örnek iki bakiyeyi birlikte değiştirir. İkinci sorguda kısıt ihlali oluşursa veritabanı `ROLLBACK` uygulayabilir; ancak üretim kodunda etkilenen satır sayısını kontrol etmek de önemlidir.

## C: Tutarlılık — kuralların korunması

Tutarlılık, bir işlemin veritabanını geçerli bir durumdan başka geçerli duruma taşımasıdır. Bu ilke yalnızca veritabanının değil, uygulama kurallarının da sorumluluğundadır. `NOT NULL`, `CHECK`, `FOREIGN KEY`, benzersiz indeksler ve tetikleyiciler veritabanı seviyesindeki korumalardır. Örneğin bakiye için `CHECK (bakiye >= 0)` tanımlanabilir.

| Kural türü | Örnek | En uygun katman |
|---|---|---|
| Alan doğrulaması | Tutar pozitif olmalı | CHECK / uygulama |
| Referans bütünlüğü | Siparişin müşterisi olmalı | FOREIGN KEY |
| İş kuralı | Günlük limit aşılmamalı | İşlem içindeki uygulama mantığı |

## I: İzolasyon — eşzamanlılığın görünmez savaşı

Birçok kullanıcı aynı anda işlem başlatabilir. İzolasyon, bir işlemin ara durumlarının diğer işlemler tarafından yanlış yorumlanmasını engeller. Zayıf izolasyon seviyelerinde kirli okuma, tekrarlanamayan okuma ve phantom read gibi sorunlar oluşabilir. Daha güçlü izolasyon daha fazla kilit, bekleme veya yeniden deneme maliyeti yaratabilir.

| Seviye | Avantaj | Olası risk |
|---|---|---|
| Read Committed | Yaygın, dengeli | Tekrarlanamayan okuma |
| Repeatable Read | Aynı satır için kararlı görünüm | Phantom davranışı motorla değişir |
| Serializable | En güçlü mantıksal koruma | Çakışma ve retry maliyeti |

Örneğin iki kullanıcı son ürünü aynı anda satın almaya çalışıyorsa, `SELECT ... FOR UPDATE` veya seri hale getirilebilir işlem seviyesi stok değerinin eksiye düşmesini önleyebilir.

## D: Kalıcılık — COMMIT sonrası güven

`COMMIT` döndükten sonra değişiklik, makine çöksa bile korunmalıdır. Veritabanları bunu write-ahead logging (WAL), disk flush işlemleri, kontrol noktaları ve kurtarma günlükleriyle sağlar. Basitçe, veri sayfası diske yazılmadan önce değişikliği yeniden oluşturacak günlük güvenli depolamaya alınır. Çökme sonrası motor bu günlüğü kullanarak onaylanmış işlemleri yeniden uygular, yarım kalanları geri alır.

ACID sihir değildir: uzun işlemler kilit rekabetini artırır, dağıtık sistemlerde maliyet yükselir ve yanlış uygulama mantığı yine hatalı sonuç üretebilir. Yine de doğru kısıtlar, kısa işlemler, uygun izolasyon seviyesi ve hata durumunda retry stratejisiyle ACID; veriyi yalnızca saklayan değil, ona güven veren bir temel oluşturur.
