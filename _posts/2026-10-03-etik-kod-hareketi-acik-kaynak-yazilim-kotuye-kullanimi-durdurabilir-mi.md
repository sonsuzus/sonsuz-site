---
layout: post
title: "Etik Kod Hareketi: Açık Kaynak Yazılım Kötüye Kullanımı Durdurabilir mi?"
math: true
categories: 
  - Bilgi
tags: 
  - etik-kod
  - açık-kaynak
  - yazılım-lisansları
  - insan-hakları
  - ethical-source
  - hukuk
toc: true
image: /img/etik-kod-hareketi-45.png
---

Bir kütüphane geliştirdiğinizi ve onu herkes yararlansın diye yayımladığınızı düşünün. Bir süre sonra kodunuzun kitlesel gözetim, ayrımcı karar sistemleri veya çalışanları baskılayan yazılımlar içinde kullanıldığını öğreniyorsunuz. “Açık kaynak” özgürlüğü tam da bunu mu gerektirir, yoksa geliştiricinin ahlaki sınırlar koyma hakkı var mıdır? **Etik Kod (Ethical Source)** hareketi, özgür yazılım dünyasının en rahatsız edici sorularından birini masaya yatırıyor.

![etik-kod-hareketi-45](/img/etik-kod-hareketi-45.svg)

``

## Açık kaynak neden kullanımı sınırlamaz?

Geleneksel açık kaynak lisansları; kodu kullanma, inceleme, değiştirme ve dağıtma özgürlüklerini korur. Open Source Initiative’in tanımındaki önemli ilkelerden biri, kişi, grup veya faaliyet alanına karşı ayrımcılık yapılmamasıdır. Bu nedenle “askerî amaçlarla kullanılamaz” ya da “insan haklarını ihlal eden şirketler kullanamaz” gibi hükümler içeren bir lisans, kaynak kodu erişilebilir olsa bile OSI ölçütlerine göre açık kaynak sayılmaz.

Felsefi çatışmayı basitçe şöyle gösterebiliriz:

$$Özgürlük = Kullanım\ Hakkı - Kullanım\ Kısıtları$$

Etik Kod yaklaşımı ise özgürlüğün tek değişken olmadığını savunur:

$$Toplumsal\ Değer = Özgürlük + Fayda - Zarar\ Riski$$

Buradaki güçlük, “zarar” kavramının hukukta ve farklı kültürlerde aynı biçimde yorumlanmamasıdır.

| Yaklaşım | Temel öncelik | Kullanım kısıtlaması | OSI açık kaynak mı? |
|---|---|---:|---:|
| MIT / BSD | En geniş kullanım özgürlüğü | Çok az | Evet |
| GPL | Kullanıcı özgürlüğü ve copyleft | Dağıtım koşulları | Evet |
| Hippocratic License | İnsan haklarının korunması | Etik kısıtlar | Hayır |
| Anti-996 License | Adil çalışma koşulları | İşveren davranışına bağlı | Hayır |

## Yeni nesil lisanslar ne öneriyor?

**Hippocratic License**, yazılımın uluslararası kabul gören insan hakları ilkelerini ihlal eden faaliyetlerde kullanılmasını engellemeyi hedefler. Lisansın farklı sürümleri; çevre, işçi hakları ve gözetim gibi alanlara yönelik ek hükümler sunabilir.

**Anti-996 License** ise özellikle teknoloji sektöründeki “sabah 9’dan akşam 9’a, haftada 6 gün” çalışma kültürüne tepki olarak doğdu. Yazılımı kullanan kuruluşların yürürlükteki çalışma yasalarına ve temel işçi haklarına uymasını ister.

Bu lisanslar etik bir mesaj vermekte güçlüdür; ancak belirsiz tanımlar, ülkeler arası hukuk farkları ve yaptırım maliyetleri nedeniyle uygulanmaları zordur. Bir ihlali tespit etmek başka, dünyanın farklı bir bölgesindeki kuruma karşı dava açmak bambaşka bir meseledir.

## Lisans politikasını otomatik denetlemek

Projeler, bağımlılık lisanslarını CI sürecinde kontrol ederek hukuki sürprizleri azaltabilir. Aşağıdaki JavaScript örneği, izin verilen lisanslar dışındaki paketleri raporlar:

```javascript
const dependencies = [
  { name: "web-core", license: "MIT" },
  { name: "fair-ai", license: "Hippocratic-3.0" },
  { name: "data-kit", license: "GPL-3.0" }
];

const allowed = new Set(["MIT", "GPL-3.0"]);
const conflicts = dependencies.filter(
  dependency => !allowed.has(dependency.license)
);

if (conflicts.length > 0) {
  console.error("İncelenmesi gereken lisanslar:", conflicts);
  process.exitCode = 1;
} else {
  console.log("Lisans politikasıyla uyumlu.");
}
```

Kod, etik lisansı otomatik olarak “kötü” ilan etmez; yalnızca kuruluşun önceden belirlediği politikayla uyuşmayan bağımlılıkları insan incelemesine gönderir. Çünkü lisans uyumluluğu basit bir metin eşleştirmeden fazlasıdır.

## Peki kötüye kullanımı gerçekten engelleyebilir miyiz?

Tam anlamıyla engellemek güçtür. Kötü niyetli aktör lisansı görmezden gelebilir, kodu gizlice çatallayabilir veya yargı yetkisinin dışında kalabilir. Yine de lisanslar yalnızca dava araçları değildir; topluluk normu oluşturur, yatırımcıları ve kurumları hesap vermeye zorlar, geliştiricinin rızasını görünür kılar.

En gerçekçi yaklaşım; etik lisansı teknik erişim kontrolleri, şeffaf yönetişim, müşteri denetimi ve açık katkı ilkeleriyle birleştirmektir. Sonuçta kod tarafsız görünebilir, fakat onu üretme ve kullanıma sunma kararlarımız tarafsız değildir. Etik Kod hareketinin asıl başarısı da kesin bir bariyer kurmaktan çok, “Yapabiliyor muyuz?” sorusunun yanına “Yapmalı mıyız?” sorusunu eklemesidir.
