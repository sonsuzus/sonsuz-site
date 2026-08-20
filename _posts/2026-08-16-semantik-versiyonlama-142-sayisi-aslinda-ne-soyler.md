---
layout: post
title: "Semantik Versiyonlama: 1.4.2 Sayısı Aslında Ne Söyler?"
math: true
categories: 
  - Bilgi
tags: 
  - semantik versiyonlama
  - semver
  - paket yönetimi
  - yazılım geliştirme
toc: true
---

Bir kütüphanenin yanında görünen `v2.7.1` etiketi, yalnızca geliştiricilerin düzen takıntısını tatmin eden bir sayı dizisi değildir. Bu numara; güncellemenin güvenli olup olmadığını, mevcut kodun kırılma ihtimalini ve yeni yetenekler kazanıp kazanmayacağınızı anlatan küçük bir sözleşmedir. Semantik Versiyonlama ya da yaygın adıyla **SemVer**, bu sözleşmeyi herkesin aynı şekilde okuyabilmesini sağlar.
``
SemVer’in temel biçimi şöyledir:

$$MAJOR.MINOR.PATCH$$

Örneğin `3.12.4` sürümünde `3` major, `12` minor ve `4` patch numarasıdır. Resmî yaklaşım, bir projenin herkese açık bir API’si—yani dışarıdan kullanılan fonksiyonları, sınıfları, HTTP uçlarını veya komutları—olduğunu varsayar. Sürüm numarası, bu API’deki değişimin türüne göre artar. Buradaki ana fikir basittir: **kullanıcının kodu etkileniyorsa bunu sürümden anlayabilmesi gerekir.**

| Bölüm | Ne zaman artar? | Geriye uyumluluk | Örnek |
|---|---|---|---|
| `MAJOR` | Kırıcı değişiklik yapıldığında | Yoktur | `1.9.0` → `2.0.0` |
| `MINOR` | Yeni, uyumlu özellik eklendiğinde | Vardır | `2.3.1` → `2.4.0` |
| `PATCH` | Hata veya güvenlik düzeltildiğinde | Vardır | `2.4.0` → `2.4.1` |

## Major: “Dikkat, taşlar yerinden oynuyor!”

Major numarası, geriye dönük uyumluluğu bozan bir değişiklikte artırılır. Diyelim ki paketinizde yıllardır kullanılan `calculateTotal(items)` fonksiyonunu kaldırıp yerine `calculateInvoiceTotal(invoice)` getirdiniz. Eski fonksiyonu çağıran uygulamalar artık çalışmayacağı için bu, `1.x.x`’ten `2.0.0`’a geçiş gerektirir.

Kırıcı değişiklik yalnızca fonksiyon silmek değildir. Parametre sırasını değiştirmek, dönüş değerinin tipini farklılaştırmak, varsayılan davranışı değiştirmek veya bir REST API yanıtından alan kaldırmak da major artışı gerektirebilir. Major sürümler bu yüzden biraz “ev taşıma” gibidir: mümkündür, faydalı olabilir, ama taşınmadan önce liste yapmak gerekir.

## Minor: Yeni oyuncaklar, eski düzen

Minor sürüm, mevcut kullanıcıları üzmeden yeni özellik eklemek içindir. Örneğin `formatDate(date)` fonksiyonuna dokunmadan `formatRelativeDate(date)` eklemek `1.2.0` → `1.3.0` güncellemesidir. Eski kod aynı şekilde çalışır; isteyen yeni özelliği kullanmaya başlar.

Kullanımdan kaldırma (deprecation) uyarıları da çoğunlukla minor sürümde gelir. Bir API’yi hemen silmek yerine önce alternatifini sunar, eski API’yi “gelecekte kaldırılacak” diye işaretlersiniz. Asıl kaldırma işlemi sonraki major sürüme saklanır. Bu yaklaşım kullanıcıya geçiş zamanı tanır.

## Patch: Küçük ama hayat kurtaran tamirler

Patch, dışarıdan görünen davranışı değiştirmeden hataları gidermek için artar. Tarih biçimlendirme fonksiyonunun şubat ayındaki artık yıl hesabını yanlış yapması veya bir SQL sorgusunun `NULL` değerinde çökmesi buna örnektir. `1.3.0` sürümündeki bu hata `1.3.1` ile düzeltilir.

```js
// 1.3.0: Ay indeksi yanlış yorumlanıyor olabilir
function isLeapYear(date) {
  const year = date.getFullYear();
  return year % 4 === 0;
}

// 1.3.1: Gregoryen takvim kuralı eksiksiz uygulanır
function isLeapYear(date) {
  const year = date.getFullYear();
  return year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
}
```

Bu değişiklik fonksiyonun adını, parametresini veya dönüş tipini değiştirmez; yalnızca doğru sonucu üretmesini sağlar. Bu nedenle patch’tir.

## Sürüm aralıklarını doğru okumak

Paket yöneticilerinde sürüm aralıkları SemVer bilgisini doğrudan kullanır. Örneğin npm’de `^2.4.1`, genel olarak `>=2.4.1` ve `<3.0.0` anlamına gelir: minor ve patch güncellemeleri alınabilir, major güncelleme alınmaz. Buna karşılık `~2.4.1`, yalnızca `<2.5.0` sınırına kadar olan patch güncellemelerini kabul eder.

| İfade | İzin verilen tipik güncellemeler | Risk düzeyi |
|---|---|---|
| `2.4.1` | Yalnızca tam sürüm | En düşük |
| `~2.4.1` | Patch | Düşük |
| `^2.4.1` | Minor ve patch | Dengeli |
| `*` | Her şey, major dahil | Yüksek |

Sonuç olarak SemVer, sürüm numarası vermekten çok beklenti yönetimidir. Kütüphane geliştiricisi değişimin etkisini dürüstçe ilan eder; kullanıcı da güncellemeyi daha bilinçli planlar. Üç sayı, doğru kullanıldığında ekipler arasında oldukça güçlü bir iletişim protokolüne dönüşür.
