---
layout: post
title: "PostgreSQL JSONB: İlişkisel Veritabanında NoSQL Esnekliği ve Performansı"
math: true
categories: 
  - Bilgi
tags: 
  - postgresql
  - jsonb
  - nosql
  - sql
  - veritabanı
  - gin-indeksi
toc: true
image: /img/postgresql-jsonb-iliskisel-90.png
---

Bir uygulamanın ürün kataloğunda telefonların ekran boyutu, ayakkabıların numarası, kahvelerin kavurma derecesi olabilir. Her kategori için onlarca nullable sütun açmak istemiyorsanız PostgreSQL’in `JSONB` tipi imdada yetişir. JSONB, değişken yapılı verileri saklarken SQL, transaction ve ilişkisel bütünlük gibi PostgreSQL güçlerinden vazgeçmeden doküman yaklaşımından yararlanmanızı sağlar.
``
## JSON ile JSONB aynı şey değil

PostgreSQL’de `JSON`, girilen metni büyük ölçüde olduğu gibi saklar. `JSONB` ise belgeyi ayrıştırıp optimize edilmiş ikili bir yapıya dönüştürür. Bu dönüşüm yazma sırasında küçük bir maliyet oluşturur; buna karşılık sorgulama ve indeksleme çok daha verimli hâle gelir.

| Özellik | JSON | JSONB |
|---|---|---|
| Saklama biçimi | Metinsel | Ayrıştırılmış ikili yapı |
| Anahtar sırası | Korunur | Korunmaz |
| Yinelenen anahtarlar | Metinde kalabilir | Son değer geçerli olur |
| İndeksleme | Sınırlı | GIN ve ifade indeksleri |
| Okuma performansı | Yeniden ayrıştırma gerekir | Genellikle daha hızlı |
| Uygun kullanım | Ham belgenin korunması | Arama ve filtreleme |

![postgresql-jsonb-iliskisel-90](/img/postgresql-jsonb-iliskisel-90.svg)


Bir belgenin ayrıştırma maliyetini $P$, tek sorgunun erişim maliyetini $Q$ ve sorgu sayısını $n$ kabul edersek metinsel JSON’un yaklaşık maliyeti $n(P+Q)$ olur. JSONB’de ayrıştırma yazma anında bir kez yapıldığından maliyet kabaca

$$P + nQ$$

şeklindedir. Belge sık okunuyorsa başlangıç maliyeti hızla karşılığını verir.

## JSONB sütunu oluşturmak

Aşağıdaki tablo, sabit alanları ilişkisel sütunlarda; ürüne göre değişen özellikleri ise JSONB içinde tutar:

```sql
CREATE TABLE products (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    category_id BIGINT NOT NULL,
    attributes  JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO products (name, category_id, attributes)
VALUES (
    'Mekanik Klavye',
    12,
    '{"switch":"brown","wireless":true,"keys":84}'
);
```

Bu hibrit model önemli bir denge kurar: kimlik, kategori ve tarih gibi düzenli alanlar normal sütunlarda kalırken esnek özellikler tek bir belgede toplanır. Her şeyi JSONB’ye doldurmak mümkün olsa da bu yaklaşım veritabanını pahalı bir dosya dolabına çevirebilir.

## Operatörlerle belgeyi sorgulamak

`->` sonucu JSONB olarak, `->>` ise metin olarak döndürür. `@>` operatörü soldaki belgenin sağdaki yapıyı içerip içermediğini kontrol eder.

```sql
-- Brown switch kullanan ürünleri bulur.
SELECT id, name
FROM products
WHERE attributes @> '{"switch":"brown"}';

-- Sayısal karşılaştırma için metni integer'a dönüştürür.
SELECT name, attributes->>'keys' AS key_count
FROM products
WHERE (attributes->>'keys')::integer >= 80;
```

JSONB şema esnekliği sağlar ancak şemasızlık, doğrulamasızlık anlamına gelmemelidir. Örneğin tuş sayısının gerçekten sayı olmasını `CHECK` ile güvenceye alabiliriz:

```sql
ALTER TABLE products ADD CONSTRAINT valid_keys
CHECK (
    NOT attributes ? 'keys'
    OR jsonb_typeof(attributes->'keys') = 'number'
);
```

## GIN indeksi: Asıl performans numarası

Tablo büyüdüğünde her JSONB belgesini taramak yerine GIN indeksi kullanılabilir. GIN, bir belgedeki anahtar ve değerleri ters indeks mantığıyla arama terimlerine bağlar.

```sql
CREATE INDEX products_attributes_gin
ON products USING GIN (attributes);
```

Varsayılan `jsonb_ops`, `?`, `@>` ve JSONPath dâhil daha geniş operatör desteği sunar. Yalnızca içerme sorguları yoğun kullanılıyorsa daha küçük ve çoğu durumda daha hızlı `jsonb_path_ops` seçilebilir:

```sql
CREATE INDEX products_attributes_path_gin
ON products USING GIN (attributes jsonb_path_ops);
```

| Strateji | Avantaj | Dezavantaj |
|---|---|---|
| `jsonb_ops` | Daha fazla operatörü destekler | İndeks daha büyük olabilir |
| `jsonb_path_ops` | `@>` sorgularında kompakt ve hızlıdır | Operatör desteği daha dardır |
| İfade indeksi | Belirli alanda çok etkilidir | Yalnızca seçilen ifadeyi hızlandırır |

Sık sorgulanan tek bir alan için `(attributes->>'switch')` üzerinde B-tree ifade indeksi kurmak, dev bir genel GIN indeksinden daha ekonomik olabilir. Kararı tahminle değil, `EXPLAIN ANALYZE` çıktısıyla vermek gerekir.

JSONB, PostgreSQL’i MongoDB’ye dönüştürmez; daha ilginç bir şey yapar: doküman esnekliğini JOIN, foreign key, transaction ve güçlü SQL sorgularıyla aynı sistemde buluşturur. Düzenli veriyi sütunlarda, değişken nitelikleri JSONB’de tutup doğru indeksi seçtiğinizde iki dünyanın da sevilen taraflarını elde edebilirsiniz.
