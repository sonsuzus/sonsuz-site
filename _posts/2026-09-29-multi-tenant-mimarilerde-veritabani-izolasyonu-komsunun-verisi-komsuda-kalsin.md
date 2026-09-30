---
layout: post
title: "Multi-Tenant Mimarilerde Veritabanı İzolasyonu: Komşunun Verisi Komşuda Kalsın"
math: true
categories: 
  - Bilgi
tags: 
  - multi-tenant
  - veritabanı
  - saas
  - güvenlik
  - postgresql
  - bulut mimarisi
toc: true
image: /img/multi-tenant-mimarilerde-93.png
---

Bir SaaS uygulamasında yüzlerce müşteri aynı altyapıyı paylaşabilir; fakat hiçbir müşteri bu paylaşımı verilerinde hissetmemelidir. Multi-tenant mimarinin temel sözü şudur: “Aynı apartmanda yaşayabiliriz, ama anahtarlarımız farklıdır.” Bu sözü tutmanın yolu, doğru veritabanı izolasyon stratejisini seçmek ve izolasyonu yalnızca uygulama koduna bırakmamaktır.
``
## İzolasyon neyi çözer?

Her müşteriye bir **tenant** denir. İzolasyon; bir tenant’ın sorgularının, yedeklerinin, performans yükünün ve yetkilerinin diğer tenant’ları etkilemesini sınırlar. Burada yalnızca gizlilik değil, “gürültülü komşu” problemi de önemlidir: Bir müşterinin ağır raporu herkesin sistemini yavaşlatabilir.

Basitleştirilmiş risk modeli şöyle düşünülebilir:

$$
R = P(sızıntı) \times Etki + P(kesinti) \times Maliyet
$$

İzolasyon güçlendikçe olasılıklar azalır; fakat altyapı ve operasyon maliyeti yükselir. Dolayısıyla en güçlü seçenek her zaman en doğru seçenek değildir.

## Başlıca izolasyon modelleri

| Model | İzolasyon | Maliyet | Operasyon | Uygun kullanım |
|---|---:|---:|---:|---|
| Ortak tablo, `tenant_id` sütunu | Düşük-Orta | Düşük | Kolay | Çok sayıda küçük tenant |
| Tenant başına şema | Orta-Yüksek | Orta | Orta | Orta ölçekli B2B SaaS |
| Tenant başına veritabanı | Çok yüksek | Yüksek | Zor | Kurumsal ve regülasyonlu müşteriler |
| Hibrit model | Ayarlanabilir | Değişken | Zor | Farklı müşteri sınıfları |

![multi-tenant-mimarilerde-93](/img/multi-tenant-mimarilerde-93.svg)


### 1. Ortak tablo ve tenant sütunu

Tüm müşteriler aynı tabloları kullanır; her satırda `tenant_id` bulunur. Ekonomik ve ölçeklenebilir olmasına rağmen tek bir unutulmuş `WHERE` koşulu veri sızıntısına dönüşebilir.

PostgreSQL Row-Level Security, filtreyi geliştiricinin dikkatinden çıkarıp veritabanı politikasına taşır:

```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON invoices
USING (
  tenant_id = current_setting('app.tenant_id')::uuid
)
WITH CHECK (
  tenant_id = current_setting('app.tenant_id')::uuid
);

SET LOCAL app.tenant_id = '7dce0b79-0000-0000-0000-000000000001';
SELECT * FROM invoices;
```

`USING` okunabilecek satırları, `WITH CHECK` ise eklenebilecek veya güncellenebilecek satırları sınırlar. `tenant_id` alanının indekslenmesi de zorunlu sayılmalıdır; aksi hâlde güvenli sorgular pahalı tam tablo taramalarına dönüşebilir.

### 2. Tenant başına şema

Her müşterinin `tenant_a.orders` gibi ayrı şeması vardır. Tablo adları aynı kalırken mantıksal sınırlar belirginleşir. Tenant bazlı taşıma ve yedekleme kolaylaşır; ancak yüzlerce şemaya migration uygulamak dikkatli otomasyon ister. Dinamik şema adları kullanıcı girdisinden doğrudan üretilmemeli, güvenilir bir tenant kataloğundan alınmalıdır.

### 3. Tenant başına veritabanı

Her müşteri ayrı veritabanına yerleştirilir. Erişim bilgileri, yedekler ve kaynak limitleri ayrılabilir. Bu yaklaşım finans, sağlık veya veri yerleşimi kuralları bulunan sistemlerde güçlüdür. Dezavantajı; bağlantı havuzlarının, migration süreçlerinin ve izleme sistemlerinin çoğalmasıdır.

Uygulama, tenant kimliğini doğrulanmış oturumdan alıp doğru bağlantıya yönlendirmelidir:

```typescript
async function databaseFor(session: Session) {
  const tenant = await tenantCatalog.findById(session.tenantId);
  if (!tenant || tenant.status !== "active") throw new Error("Tenant unavailable");
  return connectionPools.get(tenant.databaseKey);
}
```

Burada veritabanı adresi istekte gönderilen başlıktan değil, sunucunun güvenilir kataloğundan seçilir.

## Hibrit yaklaşım ve savunma katmanları

Pratikte küçük müşteriler ortak veritabanında tutulurken büyük müşteriler ayrı veritabanlarına taşınabilir. Buna **pool modeli** ile **silo modelinin** birleşimi denebilir. Seçim; tenant sayısı, regülasyon, kurtarma hedefleri ve bütçe üzerinden yapılmalıdır.

Hangi model kullanılırsa kullanılsın tenant kimliği doğrulanmalı, bileşik indeksler `tenant_id` ile başlamalı, çapraz tenant testleri otomatikleştirilmeli ve loglarda tenant bağlamı bulunmalıdır. Şifreleme anahtarlarını tenant bazında ayırmak da hasarın yayılmasını sınırlar. Sonuçta izolasyon tek bir `WHERE` koşulu değil; kimlik doğrulamadan yedeklemeye kadar uzanan katmanlı bir güvenlik sözleşmesidir.
