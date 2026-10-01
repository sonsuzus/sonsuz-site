---
layout: post
title: "Monorepo vs Polyrepo: Google Neden Tüm Kodlarını Aynı Çatı Altında Tutuyor?"
math: true
categories: 
  - Bilgi
tags: 
  - monorepo
  - polyrepo
  - git
  - google
  - bazel
  - refactoring
  - yazılım mimarisi
toc: true
image: /img/monorepo-vs-polyrepo-33.png
---

Bir şirketin yüzlerce uygulaması, kütüphanesi ve servisi olduğunu düşünün. Bunları ayrı depolara bölmek düzenli görünür; ancak ortak bir kütüphane değiştiğinde işler hızla “hangi servis hangi sürümü kullanıyor?” bulmacasına dönüşebilir. Monorepo yaklaşımı, bütün kodları tek bir kaynak ağacında toplayarak bu problemi farklı bir yerden çözer. Google’ın yaklaşımı bunun en ünlü örneğidir; fakat küçük bir düzeltme yapalım: Google, dev kod tabanı için Git yerine ağırlıklı olarak kendi geliştirdiği Piper altyapısını kullanır.

``

## Monorepo ve polyrepo nedir?

**Monorepo**, birden fazla proje veya servisin aynı depo içerisinde yönetilmesidir. Polyrepo modelindeyse her projenin kendine ait deposu, sürüm geçmişi ve yayın süreci bulunur. Buradaki ayrım yalnızca klasör sayısıyla ilgili değildir; bağımlılıkların, erişim politikalarının ve ekiplerin nasıl koordine edildiğini belirler.

| Özellik | Monorepo | Polyrepo |
|---|---|---|
| Bağımlılık yönetimi | Tek kaynak ve uyumlu sürümler | Sürümleme ve paket yayını gerekir |
| Büyük refactoring | Tek değişiklikle tamamlanabilir | Depolar arası koordinasyon ister |
| Erişim kontrolü | Daha karmaşık olabilir | Depo bazında daha kolaydır |
| CI süresi | Akıllı önbellekleme gerektirir | Projeler bağımsız çalıştırılabilir |
| Kod keşfi | Merkezi ve kolaydır | Kod birçok yerde dağınıktır |
| Araç maliyeti | Büyük ölçekte yüksektir | Başlangıçta daha düşüktür |

![monorepo-vs-polyrepo-33](/img/monorepo-vs-polyrepo-33.svg)


## Google neden tek kaynak ağacını seviyor?

En önemli kazanç **bağımlılık uyumudur**. Polyrepo dünyasında A servisi bir kütüphanenin 2. sürümünü, B servisi ise 7. sürümünü kullanabilir. Bu durum güvenlik açıklarının kapanmasını ve eski API’lerin kaldırılmasını zorlaştırır. Monorepoda ekip, kütüphane ile onu kullanan kodları aynı değişiklik paketi içinde güncelleyebilir.

Basitleştirilmiş biçimde koordinasyon maliyetini şöyle düşünebiliriz:

$$C = R \times D \times V$$

Burada $R$ depo sayısını, $D$ depolar arası bağımlılık sayısını, $V$ ise eş zamanlı sürüm çeşitliliğini temsil eder. Polyrepoda bu değişkenlerin çarpımı büyüyebilir. Monorepo, özellikle $R$ ve $V$ etkisini azaltır; fakat karşılığında derleme ve yetkilendirme altyapısının karmaşıklığını artırır.

## Dev refactoring süper gücü

Bir API metodunun adını değiştirdiğinizi düşünün. Polyrepoda önce yeni sürümü yayımlar, tüketicileri sırayla günceller, geçiş döneminde eski API’yi korur ve son olarak kullanımdan kaldırırsınız. Monorepoda ise tanımı ve yüzlerce çağrı noktasını tek atomik değişiklikle düzenlemek mümkündür. Kod incelemesi başarısız olursa değişikliklerin tamamı geri alınır; sistem yarı güncellenmiş durumda kalmaz.

Bu avantaj, merkezi kod arama ve otomatik dönüşüm araçlarıyla birleştiğinde etkileyicidir. Milyonlarca satırdaki eski kullanım desenleri bulunabilir ve mekanik olarak yenileriyle değiştirilebilir.

## Peki derleme patlamıyor mu?

Her değişiklikte bütün sistemi derlemek pratik değildir. Bu nedenle Google’ın açık kaynaklı hale getirdiği **Bazel**, hedefler arasında açık bir bağımlılık grafiği kurar:

```python
# BUILD dosyası: yalnızca gerekli bağımlılıkları tanımlar.
java_library(
    name = "payment_core",
    srcs = glob(["src/**/*.java"]),
    deps = ["//shared/logging:logger"],
)
```

Bu tanım sayesinde araç, `logger` değiştiğinde hangi hedeflerin etkilendiğini hesaplar. Değişmeyen çıktılar önbellekten alınır ve testler seçici biçimde çalıştırılır. Yani monorepo, “her seferinde her şeyi derle” anlamına gelmez; doğru bağımlılık grafiği sayesinde yalnızca gerekli işler yapılır.

## Bedava öğle yemeği yok

Monorepo; devasa klonlama maliyeti, karmaşık CI yapılandırması, ince taneli yetkilendirme ve sahiplik sorunları doğurabilir. Git’in standart iş akışları da Google ölçeğindeki milyonlarca dosya için tek başına yeterli olmayabilir. Sanal dosya sistemleri, uzak önbellek, dağıtık derleme ve güçlü kod sahipliği kuralları gerekir.

Küçük ve orta ekiplerde projeler yoğun biçimde kod paylaşıyor ve birlikte yayınlanıyorsa monorepo güçlü bir seçimdir. Tamamen bağımsız ürünler, farklı güvenlik sınırları veya ayrı yayın takvimleri varsa polyrepo daha sade kalabilir. Sonuçta Google’ın dersi “her şeyi tek repoya koyun” değil, **merkezi kodun avantajlarını taşıyabilecek araçlara yatırım yapın** mesajıdır.
