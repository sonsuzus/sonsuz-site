---
layout: post
title: "Dosya Arama Sistemi Kurmak: Elasticsearch, Meilisearch ve Typesense Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - elasticsearch
  - meilisearch
  - typesense
  - arama-motoru
  - dosya-indeksleme
  - backend
toc: true
image: /img/dosya-arama-sistemi-35.png
---

Binlerce PDF, Word belgesi ve metin dosyası arasında doğru dosyayı bulmaya çalışmak, dijital samanlıkta iğne aramaya benzeyebilir. Neyse ki Elasticsearch, Meilisearch ve Typesense gibi arama motorları; dosya içeriklerini indeksleyerek milisaniyeler içinde alakalı sonuçlar sunabilir. Peki bu üçlüden hangisi projenize daha uygun?

``

## Dosya arama sistemi nasıl çalışır?

Bir arama motoru dosyaları doğrudan sihirli biçimde anlamaz. Önce dosyanın metni çıkarılır, temizlenir ve indekslenebilir bir belgeye dönüştürülür. Tipik veri akışı şöyledir:

1. Dosya sisteme yüklenir.
2. Apache Tika, PDF.js veya benzeri bir araçla metin çıkarılır.
3. Başlık, dosya yolu, uzantı ve kullanıcı izinleri gibi metadata eklenir.
4. Belge arama motoruna gönderilir.
5. Kullanıcı sorgusu indeks üzerinde çalıştırılır.

Bu sistemlerin temelinde **ters indeks** bulunur. Geleneksel bir listede her belgenin içindeki kelimeler tutulurken ters indeks, her kelimenin hangi belgelerde geçtiğini saklar:

| Kelime | Geçtiği belgeler |
|---|---|
| docker | belge-1, belge-7 |
| güvenlik | belge-2, belge-7 |
| yedekleme | belge-3 |

![dosya-arama-sistemi-35](/img/dosya-arama-sistemi-35.svg)


Böylece motor, bütün dosyaları tek tek okumak yerine ilgili kayıtları doğrudan bulur. Alaka sıralamasında sık kullanılan BM25 yaklaşımının basitleştirilmiş fikri şöyledir:

$$\text{skor}(q,d) = \sum_{t \in q} IDF(t) \cdot TF(t,d)$$

Burada $TF$, kelimenin belgede ne kadar sık geçtiğini; $IDF$ ise kelimenin tüm koleksiyon içindeki ayırt ediciliğini temsil eder. Örneğin “dosya” kelimesi sıradanken “Kubernetes” daha yüksek ayırt ediciliğe sahip olabilir.

## Üç arama motorunun karşılaştırması

| Özellik | Elasticsearch | Meilisearch | Typesense |
|---|---|---|---|
| Kurulum | Daha karmaşık | Çok kolay | Kolay |
| Ölçeklenebilirlik | Çok yüksek | Orta-yüksek | Yüksek |
| Yazım hatası toleransı | Yapılandırılabilir | Varsayılan olarak güçlü | Varsayılan olarak güçlü |
| Gelişmiş sorgular | Çok kapsamlı | Daha sade | Dengeli |
| Kaynak tüketimi | Görece yüksek | Düşük | Düşük |
| Uygun senaryo | Büyük ve karmaşık sistemler | Hızlı ürün geliştirme | Hızlı, kontrollü arama |

**Elasticsearch**, devasa veri kümeleri, dağıtık mimari ve ayrıntılı sorgu ihtiyacı olduğunda güçlüdür. Ancak shard, analyzer ve mapping gibi kavramları öğrenmek gerekir. Küçük bir proje için uzay mekiğiyle markete gitmek gibi hissedilebilir.

**Meilisearch**, geliştirici deneyimine odaklanır. Yazım hatalarını otomatik tolere eder ve iyi sonuçlara ulaşmak için uzun yapılandırmalar istemez. MVP, kurum içi doküman araması ve içerik siteleri için oldukça pratiktir.

**Typesense** ise sadelik ile kontrol arasında güzel bir denge kurar. Şema tanımı zorunludur; bu yaklaşım ilk aşamada ek iş çıkarsa da veri yapısının tutarlı kalmasını sağlar.

## Örnek belge indeksleme

Aşağıdaki JavaScript kodu, metni çıkarılmış bir dosyayı Meilisearch indeksine ekler:

```javascript
import { MeiliSearch } from 'meilisearch';

const client = new MeiliSearch({
  host: 'http://localhost:7700',
  apiKey: process.env.MEILI_MASTER_KEY
});

const documents = client.index('documents');

await documents.addDocuments([
  {
    id: 'rapor-2026',
    title: '2026 Güvenlik Raporu',
    path: '/raporlar/guvenlik.pdf',
    extension: 'pdf',
    content: 'Sunucu güvenliği, erişim kontrolü ve yedekleme...',
    allowedUsers: ['user-17', 'user-42']
  }
]);

const result = await documents.search('sunucu güvenligi', {
  filter: 'allowedUsers = user-17',
  limit: 10
});

console.log(result.hits);
```

Kod, belgeyi `documents` indeksine ekler ve yazım hatası içeren bir sorgu çalıştırır. Gerçek projede erişim filtresi kritik önemdedir: Kullanıcının göremediği bir dosya, arama sonucunda da görünmemelidir. Ayrıca API anahtarını istemci tarafına koymak yerine backend üzerinde saklamak gerekir.

## Hangisini seçmeli?

Milyonlarca belge, karmaşık filtreler ve ayrıntılı analiz gerekiyorsa **Elasticsearch** doğru adaydır. Birkaç saatte çalışan, kullanıcı dostu bir arama deneyimi hedefleniyorsa **Meilisearch** öne çıkar. Düşük gecikme, güçlü yazım toleransı ve açık bir veri şeması isteniyorsa **Typesense** tercih edilebilir.

Motor seçiminden bağımsız olarak başarıyı belirleyen asıl unsurlar; kaliteli metin çıkarma, doğru metadata, Türkçe dil analizi, yetkilendirme ve düzenli indeks güncellemesidir. Motor arabanın kalbidir; fakat tekerlekler yoksa hiçbir yere gidemezsiniz.
