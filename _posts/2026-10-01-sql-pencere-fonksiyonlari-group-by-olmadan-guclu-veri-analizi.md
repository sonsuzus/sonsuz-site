---
layout: post
title: "SQL Pencere Fonksiyonları: GROUP BY Olmadan Güçlü Veri Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - sql
  - veritabanı
  - window-functions
  - veri-analizi
  - postgresql
  - performans
toc: true
image: /img/sql-pencere-fonksiyonlari-39.png
---

Bir satış tablosundaki her kaydı korurken toplam ciroyu, ürün sıralamasını veya önceki güne göre değişimi görmek istediğinizi düşünün. `GROUP BY` satırları özetleyerek detayları ortadan kaldırırken pencere fonksiyonları, satırlara dokunmadan analitik sonuçlar üretir. Başka bir deyişle veri aynı kalır, fakat her satır yanında küçük bir analist taşımaya başlar!


![sql-pencere-fonksiyonlari-39](/img/sql-pencere-fonksiyonlari-39.svg)

``

## Pencere fonksiyonu nedir?

Pencere fonksiyonları, mevcut satırla ilişkili bir satır kümesi üzerinde hesaplama yapar. Bu kümeye **pencere** denir. Temel sözdizimi şöyledir:

```sql
fonksiyon() OVER (
    PARTITION BY kolon
    ORDER BY kolon
    ROWS BETWEEN ... AND ...
)
```

Buradaki parçaların görevleri farklıdır:

- `PARTITION BY`, verileri bağımsız gruplara ayırır.
- `ORDER BY`, pencere içindeki işlem sırasını belirler.
- `ROWS` veya `RANGE`, hesaplamaya hangi komşu satırların katılacağını tanımlar.

Matematiksel olarak bir satırın pencere sonucunu şöyle düşünebiliriz:

$$W_i = f(x_j \mid j \in P_i)$$

Burada $P_i$, $i$ satırı için seçilen pencereyi; $f$ ise toplam, ortalama veya sıralama gibi fonksiyonu temsil eder.

## GROUP BY ile farkı

| Özellik | `GROUP BY` | Pencere fonksiyonu |
|---|---|---|
| Satır sayısı | Azalır | Korunur |
| Detay kolonları | Genellikle kaybolur | Görüntülenmeye devam eder |
| Yürüyen toplam | Dolaylı ve zahmetli | Doğrudan yapılır |
| Sıralama | Tek başına yetersizdir | `RANK`, `ROW_NUMBER` kullanılabilir |
| Önceki kayda erişim | Join gerekebilir | `LAG` ile kolaydır |

Örneğin her satış kaydının yanında ilgili mağazanın toplam cirosunu gösterebiliriz:

```sql
SELECT
    magaza_id,
    tarih,
    tutar,
    SUM(tutar) OVER (PARTITION BY magaza_id) AS magaza_toplami
FROM satislar;
```

Bu sorgu mağaza bazında toplamı hesaplar, ancak satış satırlarını birleştirmez. Böylece hem tekil işlem hem de büyük resim aynı sonuç kümesinde bulunur.

## Yürüyen toplam hesaplamak

Finansal raporların klasik ihtiyacı olan kümülatif toplam, pencere çerçevesiyle oluşturulur:

```sql
SELECT
    tarih,
    tutar,
    SUM(tutar) OVER (
        ORDER BY tarih
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS yuruyen_toplam
FROM satislar;
```

Her $i$ satırındaki sonuç şu formüle karşılık gelir:

$$S_i = \sum_{k=1}^{i} x_k$$

`UNBOUNDED PRECEDING`, ilk satırdan başlanmasını; `CURRENT ROW` ise mevcut satırda durulmasını söyler. Aynı tarih birden fazla kez bulunabiliyorsa deterministik sonuç için `ORDER BY tarih, satis_id` gibi benzersiz bir sıralama tercih edilmelidir.

## Sıralama fonksiyonları

SQL, benzer görünen fakat eşitliklerde farklı davranan üç önemli araç sunar:

| Fonksiyon | Eşit değerlere yaklaşım | Sonraki sıra |
|---|---|---|
| `ROW_NUMBER()` | Her satıra farklı numara verir | Kesintisiz |
| `RANK()` | Eşitlere aynı sıra verir | Sıra atlar |
| `DENSE_RANK()` | Eşitlere aynı sıra verir | Sıra atlamaz |

```sql
SELECT
    urun_adi,
    ciro,
    DENSE_RANK() OVER (ORDER BY ciro DESC) AS ciro_sirasi
FROM urun_ozetleri;
```

Bu sorgu eşit ciroya sahip ürünleri aynı konuma yerleştirir. Özellikle “en yüksek ilk üç değer” gibi raporlarda `DENSE_RANK()` oldukça kullanışlıdır.

## Geçmişe ve geleceğe bakmak

`LAG` önceki, `LEAD` ise sonraki satırdaki değere erişir. Böylece self-join yazmadan dönemsel fark hesaplanabilir:

```sql
SELECT
    tarih,
    tutar,
    LAG(tutar) OVER (ORDER BY tarih) AS onceki_tutar,
    tutar - LAG(tutar) OVER (ORDER BY tarih) AS degisim
FROM gunluk_satislar;
```

Oransal değişim ise $r = (x_i-x_{i-1})/x_{i-1}$ formülüyle hesaplanabilir. Sıfıra bölünmeyi önlemek için SQL tarafında `NULLIF(onceki_tutar, 0)` kullanmak önemlidir.

## Performans ve kapanış

Pencere fonksiyonları sıralama gerektirebildiğinden büyük tablolarda maliyetli olabilir. `PARTITION BY` ve `ORDER BY` kolonlarını destekleyen indeksler, uygun filtreler ve sorgu planı incelemesi performansı iyileştirir. Aynı pencere tanımını birçok kez kullanıyorsanız destekleyen veritabanlarında `WINDOW` ifadesiyle tekrarları azaltabilirsiniz.

Özetle pencere fonksiyonları, detay ile özeti aynı tabloda buluşturur. Yürüyen toplamlar, liderlik tabloları ve dönemsel karşılaştırmalar için karmaşık join zincirleri yerine okunabilir, güçlü ve çoğu zaman daha verimli SQL sorguları sağlar.
