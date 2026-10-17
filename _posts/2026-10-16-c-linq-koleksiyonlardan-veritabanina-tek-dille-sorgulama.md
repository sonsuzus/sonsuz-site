---
layout: post
title: "C# LINQ: Koleksiyonlardan Veritabanına Tek Dille Sorgulama"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - linq
  - dotnet
  - sql
  - koleksiyonlar
  - entity-framework
  - xml
toc: true
image: /img/c-linq-koleksiyonlardan-43.png
---

Bir listedeki aktif kullanıcıları bulmak, veritabanından pahalı ürünleri çekmek veya XML belgesindeki düğümleri süzmek için ayrı ayrı sorgulama yöntemleri öğrenmek zorunda olduğunuzu düşünün. C# LINQ, farklı veri kaynaklarını ortak bir sorgulama yaklaşımı altında birleştirerek bu karmaşayı azaltır. Üstelik sorgular doğrudan kodun içinde, tür güvenli ve okunabilir biçimde yazılır.


![c-linq-koleksiyonlardan-43](/img/c-linq-koleksiyonlardan-43.svg)

``

## LINQ tam olarak nedir?

LINQ, **Language Integrated Query** ifadesinin kısaltmasıdır. C# 3.0 ile gelen bu mimari; koleksiyonlar, veritabanları, XML belgeleri ve uygun sağlayıcısı bulunan başka kaynaklar üzerinde sorgu kurulmasını sağlar.

LINQ bir veritabanı değildir. Sorguyu tanımlayan ortak operatörler ve bu sorguyu hedef kaynağın anlayacağı biçime dönüştüren sağlayıcılardan oluşur. Örneğin LINQ to Objects sorguyu bellekte çalıştırırken Entity Framework tarafından kullanılan sağlayıcı, ifadeyi SQL komutuna çevirebilir.

| Yaklaşım | Veri kaynağı | Çalışma biçimi |
|---|---|---|
| LINQ to Objects | Diziler ve koleksiyonlar | Bellekte çalışır |
| LINQ to Entities | İlişkisel veritabanları | Genellikle SQL'e çevrilir |
| LINQ to XML | XML belgeleri | XML düğümlerini işler |
| PLINQ | Bellekteki koleksiyonlar | Paralel çalışabilir |

## Temel sorgulama mantığı

Bir sorgu çoğunlukla **filtreleme**, **dönüştürme**, **sıralama** ve **gruplama** adımlarından oluşur. Matematiksel olarak filtreleme, bir $S$ kümesinden koşulu sağlayan elemanların seçilmesi şeklinde gösterilebilir:

$$R = \{x \in S \mid P(x) = true\}$$

Burada $S$ kaynak koleksiyon, $P(x)$ koşul ve $R$ sonuç kümesidir. LINQ'taki `Where` operatörü tam olarak bu fikri uygular.

```csharp
var sayilar = new[] { 3, 8, 12, 17, 24, 31 };

var sonuc = sayilar
    .Where(sayi => sayi % 2 == 0)
    .OrderByDescending(sayi => sayi)
    .Select(sayi => sayi * sayi);

Console.WriteLine(string.Join(", ", sonuc));
// 576, 144, 64
```

Bu sorgu önce çift sayıları seçer, büyükten küçüğe sıralar ve ardından her sayının karesini üretir. `Select`, SQL dünyasındaki sütun seçiminin ötesinde bir **projeksiyon** aracıdır; sonucu yeni nesnelere de dönüştürebilir.

## İki farklı yazım biçimi

LINQ, metot zinciri ve SQL'e benzeyen sorgu sözdizimi olmak üzere iki biçimde kullanılabilir:

```csharp
var urunler = new List<Urun>();

var metotSozdizimi = urunler
    .Where(u => u.Fiyat > 1000)
    .OrderBy(u => u.Ad);

var sorguSozdizimi =
    from u in urunler
    where u.Fiyat > 1000
    orderby u.Ad
    select u;
```

| Özellik | Metot sözdizimi | Sorgu sözdizimi |
|---|---|---|
| Görünüm | Fonksiyon zinciri | SQL benzeri |
| Esneklik | Tüm operatörlere erişir | Bazı işlemlerde sınırlıdır |
| Tercih | Kısa ve birleşik sorgular | Join ve gruplamalarda okunabilir |

İki yaklaşım rakip değildir; aynı projede birlikte kullanılabilir.

## Ertelenmiş çalıştırma sürprizi

Birçok LINQ operatörü sorguyu tanımlandığı anda çalıştırmaz. İşlem; `foreach`, `ToList`, `Count` veya benzeri bir tüketim gerçekleştiğinde yürütülür. Buna **deferred execution**, yani ertelenmiş çalıştırma denir.

```csharp
var pahaliUrunler = urunler.Where(u => u.Fiyat > 1000);
urunler.Add(new Urun { Ad = "Monitör", Fiyat = 8000 });

var liste = pahaliUrunler.ToList();
```

`Monitör`, sorgu sonradan çalıştırıldığı için sonuçta yer alır. Belirli bir anın görüntüsü gerekiyorsa sorguyu `ToList()` ile hemen somutlaştırmak gerekir.

## Veritabanı ve XML tarafı

`IEnumerable<T>` işlemleri çoğunlukla çalışan C# fonksiyonlarını kullanır. `IQueryable<T>` ise sorguyu bir ifade ağacı olarak saklayarak sağlayıcının SQL üretmesine imkân verir. Bu nedenle veritabanı sorgularında çevrilemeyen özel C# metotları sorun çıkarabilir.

```csharp
var adlar = await dbContext.Musteriler
    .Where(m => m.Aktif)
    .Select(m => m.Ad)
    .ToListAsync();
```

LINQ to XML ile benzer düşünce korunur:

```csharp
var belge = XDocument.Load("urunler.xml");
var adlar = belge.Descendants("urun")
    .Where(x => (decimal)x.Attribute("fiyat")! > 1000)
    .Select(x => (string?)x.Attribute("ad"));
```

LINQ'nun asıl gücü yalnızca daha az kod yazdırması değildir. Tür güvenliği, IntelliSense desteği ve ortak sorgulama modeli sayesinde verinin nerede bulunduğundan çok, **hangi sonucun istendiğine** odaklanmayı sağlar.
