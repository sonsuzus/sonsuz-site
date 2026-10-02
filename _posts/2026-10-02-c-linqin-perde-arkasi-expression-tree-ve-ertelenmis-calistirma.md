---
layout: post
title: "C# LINQ’in Perde Arkası: Expression Tree ve Ertelenmiş Çalıştırma"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - linq
  - expression-tree
  - entity-framework
  - iqueryable
  - deferred-execution
toc: true
image: /img/c-linqin-perde-26.png
---

LINQ sorguları ilk bakışta koleksiyonlar üzerinde çalışan zarif döngüler gibi görünür. Ancak aynı sözdizimi bazen bellekteki nesneleri filtrelerken bazen de kilometrelerce uzaktaki bir veritabanına SQL gönderir. Bu küçük sihrin arkasında iki önemli mekanizma bulunur: sorguyu veri yerine bir mantık modeli olarak temsil eden **Expression Tree** yapıları ve çalışmayı ihtiyaç duyulana kadar erteleyen **deferred execution** davranışı.
``

## Aynı görünüm, farklı çalışma modeli

Aşağıdaki iki sorgu neredeyse aynı görünür:

```csharp
IEnumerable<Product> memoryQuery = products
    .Where(p => p.Price > 1000);

IQueryable<Product> databaseQuery = db.Products
    .Where(p => p.Price > 1000);
```

İlk sorgudaki lambda çoğunlukla çalıştırılabilir bir temsilciye, yani `Func<Product, bool>` nesnesine dönüşür. İkinci sorguda ise sağlayıcı, lambda ifadesini `Expression<Func<Product, bool>>` biçiminde alabilir. Böylece ifade doğrudan çalıştırılmak yerine incelenebilir bir ağaç olarak saklanır.

| Özellik | `IEnumerable<T>` | `IQueryable<T>` |
|---|---|---|
| Temel çalışma alanı | Uygulama belleği | Harici veri kaynağı |
| Lambda temsili | Derlenmiş temsilci | Expression Tree |
| Filtreyi uygulayan | .NET kodu | Sorgu sağlayıcısı |
| Tipik kullanım | Liste ve diziler | Entity Framework, uzak servisler |

Kavramsal olarak bir sorguyu $Q = S \rightarrow F \rightarrow P$ biçiminde düşünebiliriz. Burada $S$ kaynak, $F$ filtreleme, $P$ ise projeksiyondur. `IQueryable`, bu adımları hemen gerçekleştirmek yerine onların tarifini oluşturur.

## Expression Tree nasıl görünür?

Şu ifade bir koşulu tanımlar:

```csharp
Expression<Func<Product, bool>> filter =
    p => p.Price > 1000 && p.IsActive;

Console.WriteLine(filter.Body);
```

Ağacın kökünde `AndAlso`, dallarında ise `GreaterThan` ve `MemberAccess` gibi düğümler bulunur. Basitleştirilmiş yapı şöyledir:

```text
AndAlso
├── GreaterThan
│   ├── Product.Price
│   └── Constant(1000)
└── Product.IsActive
```

Bu yapı yalnızca sonucu değil, sonuca nasıl ulaşılacağını da anlatır. Entity Framework sağlayıcısı ağacı dolaşır; özellik erişimlerini sütunlara, karşılaştırmaları SQL operatörlerine ve sabitleri parametrelere dönüştürür. Ortaya yaklaşık şu sorgu çıkar:

```sql
SELECT *
FROM Products
WHERE Price > @price AND IsActive = 1;
```

Bu dönüşüm nedeniyle her C# metodu SQL’e çevrilemez. Sağlayıcı `CalculatePopularity()` gibi özel bir metodu tanımıyorsa sorgu çalışma anında çeviri hatası verebilir. Expression Tree bir sihirbaz değil, yalnızca sağlayıcının okuyabildiği bir tarif defteridir.

## Ertelenmiş çalıştırma ne zaman biter?

`Where`, `Select` ve `OrderBy` gibi işlemler çoğunlukla sorguyu çalıştırmaz; mevcut tarife yeni düğümler ekler. Gerçek yürütme, sonuç tüketildiğinde başlar:

```csharp
var query = db.Products
    .Where(p => p.IsActive)
    .OrderBy(p => p.Price); // Henüz SQL gönderilmedi.

var products = await query.ToListAsync(); // SQL şimdi çalışır.
```

`ToList`, `ToArray`, `First`, `Count` veya `foreach` yürütmeyi tetikleyebilir. Bunun önemli bir sonucu, aynı sorgunun iki kez dolaşılması halinde iki kez çalışabilmesidir.

| İşlem | Davranış |
|---|---|
| `Where`, `Select` | Sorguyu oluşturur |
| `ToList`, `First` | Sonucu ister ve yürütür |
| `AsEnumerable` | Sonraki işlemleri bellek tarafına taşır |
| `AsQueryable` | Kaynağı sorgulanabilir arayüzle sunar |

## Performans açısından doğru sınır

Filtreyi veritabanında yapmak genellikle taşınan kayıt sayısını azaltır. Toplam maliyeti kabaca $T = T_{sql} + T_{network} + T_{materialization}$ olarak modelleyebiliriz. Erken çağrılan `ToList`, bütün kayıtları belleğe taşıyarak ağ ve nesne oluşturma maliyetini büyütebilir.

Bu nedenle sorguyu mümkün olduğunca `IQueryable` halinde oluşturmak, yalnızca gereken sütunları `Select` ile seçmek ve sonucu en son noktada materyalleştirmek iyi bir yaklaşımdır. LINQ’i doğru anlamanın anahtarı şudur: Yazdığınız kod her zaman yapılan iş değildir; bazen yalnızca daha sonra başka bir sistemin gerçekleştireceği işin planıdır.

![c-linqin-perde-26](/img/c-linqin-perde-26.svg)

