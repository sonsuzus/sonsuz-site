---
layout: post
title: "Monorepo mu Polyrepo mu? Büyük Projelerde Depo Stratejileri"
math: true
categories: 
  - Bilgi
tags: 
  - monorepo
  - polyrepo
  - git
  - yazılım mimarisi
---

Büyüyen bir yazılım organizasyonunda kod depoları yalnızca dosyaların yaşadığı klasörler değildir; ekip sınırlarını, dağıtım hızını ve bağımlılık yönetimini doğrudan etkileyen mimari kararlardır. Monorepo, birçok uygulama ve kütüphaneyi tek Git deposunda toplarken; polyrepo yaklaşımı her servis, uygulama veya bileşen için ayrı depo kullanır. Doğru tercih, moda olan aracı seçmekten çok ürününüzün değişim ritmini anlamaktır.

``

## Temel fark: paylaşım mı, izolasyon mu?

Monorepo'da örneğin web arayüzü, mobil uygulama, API, tasarım sistemi ve ortak yardımcı paketler aynı sürüm geçmişini paylaşır. Böylece bir API sözleşmesini değiştiren geliştirici, istemciyi de aynı pull request içinde güncelleyebilir. Polyrepo'da ise bu bileşenler bağımsız depolardır; her biri kendi erişim politikalarına, sürümleme sürecine ve yayın döngüsüne sahiptir.

Basit bir maliyet modeliyle kararın mantığını görünür kılabiliriz:

$$C = C_{build} + C_{coordination} + C_{dependency}$$

Monorepo çoğu zaman $C_{coordination}$ ve $C_{dependency}$ değerlerini azaltır; ancak büyük depo, güçlü CI altyapısı yoksa $C_{build}$ değerini artırabilir. Polyrepo ise bağımsız derleme ve yayın sayesinde belirli projelerde derleme maliyetini düşürür, fakat sürümler arası koordinasyon maliyetini büyütebilir.

| Ölçüt | Monorepo | Polyrepo |
|---|---|---|
| Kod paylaşımı | Çok kolay, doğrudan import | Paket yayınlama veya Git bağımlılığı gerekir |
| Bağımsız dağıtım | Araç ve kuralla sağlanır | Doğal olarak güçlüdür |
| Erişim kontrolü | İnce ayar daha zordur | Depo bazında nettir |
| Büyük çaplı refactor | Tek değişiklik setinde yapılır | Birden fazla sürüm ve PR gerekir |
| CI gereksinimi | Akıllı önbellek ve etki analizi önemlidir | Daha basit, fakat çok sayıda pipeline vardır |

## Monorepo ne zaman parıldar?

Ortak tiplerin, bileşenlerin ve iş kurallarının sıkça değiştiği ürün ekiplerinde monorepo güçlüdür. Özellikle TypeScript tabanlı bir web platformunda `apps` ve `packages` ayrımı, paylaşımı düzenli hale getirir:

```text
repository/
├── apps/
│   ├── web/
│   └── api/
├── packages/
│   ├── ui/
│   ├── types/
│   └── config/
└── package.json
```

Bu yapı, `packages/types` içindeki bir sözleşme değiştiğinde hem API hem web uygulamasının aynı commit'te doğrulanmasını sağlar. Ancak herkesin her klasöre dokunabilmesi kaos yaratabilir. Bu yüzden CODEOWNERS, klasör bazlı testler, etkilenen paket analizi ve uzak önbellek gibi pratikler lüks değil, zorunluluktur. Nx, Turborepo, Bazel veya Pants gibi araçlar burada devreye girer.

Örneğin yalnızca değişen pakete bağlı uygulamaları test etmek için pipeline mantığı şu hedefe yaklaşmalıdır:

```bash
# Araçtan bağımsız fikir: sadece etkilenen hedefleri çalıştır
npm run test -- --affected
npm run build -- --affected
```

Amaç her commit'te tüm dünyayı yeniden derlemek değil, değişimin etki grafiğini hesaplamaktır.

## Polyrepo ne zaman daha sağlıklı?

Farklı ekiplerin farklı müşterilere, güvenlik alanlarına veya yayın takvimlerine hizmet verdiği yapılarda polyrepo temiz bir sınır oluşturur. Örneğin ödeme servisi, makine öğrenmesi platformu ve pazarlama sitesi aynı anda değişmek zorunda değilse ayrı depolar operasyonel bağımsızlık sağlar. Her depo kendi semantic versioning politikasını uygulayabilir: $MAJOR.MINOR.PATCH$.

| Senaryo | Daha uygun yaklaşım | Neden |
|---|---|---|
| Ortak UI ve tiplerin sık değişmesi | Monorepo | Atomik değişiklik ve hızlı refactor |
| Güvenlik açısından ayrık ekipler | Polyrepo | Yetki ve erişim sınırları |
| Çok sayıda küçük, bağımsız servis | Polyrepo | Ayrı yayın ve yaşam döngüsü |
| Tek ürün etrafında çalışan ekipler | Monorepo | Ortak görünürlük ve standartlar |

## Kararı araç değil, akış versin

Monorepo, mikroservis kullanamayacağınız anlamına gelmez; çalışma alanı ile dağıtım birimi farklı kavramlardır. Benzer biçimde polyrepo da paylaşımı yasaklamaz; yalnızca paylaşımı paket sözleşmeleri üzerinden daha disiplinli hale getirir. Başlangıçta ekip küçük ve ürün sınırları belirsizse monorepo geliştirme hızını artırabilir. Ekipler ve güvenlik gereksinimleri olgunlaştıkça polyrepo ya da hibrit bir model mantıklı olabilir.

En iyi strateji, geliştiricinin bir değişikliği üretime taşıma süresini, yani yaklaşık $Lead\ Time = Review + Build + Test + Deploy$ değerini düşürendir. Depo düzeninizi bu metrikle ölçün; çünkü klasör yapısından daha önemli olan, değişimin güvenle akabilmesidir.
