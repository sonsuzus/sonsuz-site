---
layout: post
title: "B-tree ve LSM-tree: Okuma mı, Yazma mı Öncelikli?"
math: true
categories: 
  - Bilgi
tags: 
  - b-tree
  - lsm-tree
  - veritabanı
  - depolama-motoru
  - performans
  - indeksleme
toc: true
image: /img/b-tree-ve-58.png
---

Bir veritabanı tasarlarken yalnızca “Veriyi nereye kaydedelim?” diye sormak yetmez; verinin nasıl okunacağını ve yazılacağını da düşünmek gerekir. B-tree ile LSM-tree arasındaki seçim tam olarak bu noktada karşımıza çıkar. B-tree genellikle dengeli ve hızlı okumalarıyla öne çıkarken LSM-tree yoğun yazma trafiğini sıralı işlemlere dönüştürerek depolama aygıtını mutlu eder. Kısacası biri düzenli bir kütüphaneci, diğeri masasına gelen belgeleri önce hızlıca kutulayan enerjik bir arşivcidir.
``

## B-tree nasıl çalışır?

B-tree, anahtarları sıralı biçimde tutan, dengeli ve çok dallı bir arama ağacıdır. Her düğüm çok sayıda anahtar ve çocuk işaretçisi barındırabilir. Bu özellik, ağacın yüksekliğini azaltarak disk erişimlerinin sayısını düşürür.

Bir B-tree içindeki arama maliyeti yaklaşık olarak şöyledir:

$$T_{okuma} = O(\log_B N)$$

Burada $N$ kayıt sayısını, $B$ ise bir düğümün dallanma katsayısını temsil eder. Düğümler çoğunlukla disk sayfası boyutuna göre ayarlandığından tek bir G/Ç işleminde çok sayıda anahtar incelenebilir.

Yeni kayıt eklenirken uygun yaprak sayfası bulunur. Sayfa doluysa bölünür ve üst düğümler güncellenir. Dolayısıyla rastgele yazmalar, sayfa bölünmeleri ve yerinde güncellemeler oluşabilir. Özellikle SSD öncesi mekanik disk dünyasında bu hareketler oldukça pahalıydı.

## LSM-tree nasıl çalışır?

Log-Structured Merge-tree, yazmaları önce bellekteki sıralı bir yapı olan **MemTable** üzerinde toplar. MemTable belirli bir boyuta ulaştığında diske değiştirilemez bir **SSTable** olarak sıralı biçimde yazılır. Arka plandaki compaction işlemi ise SSTable dosyalarını birleştirir, eski sürümleri temizler ve verileri seviyeler arasında taşır.

Basitleştirilmiş yazma maliyeti şu şekilde düşünülebilir:

$$T_{yazma} \approx O(1) + T_{compaction}$$

İlk yazma çok hızlıdır; çünkü genellikle önce bir WAL kaydı ve bellek güncellemesi yapılır. Ancak maliyet yok olmaz, yalnızca compaction aşamasına ertelenir. Bu yüzden LSM-tree sihir değil, zamanlama konusunda iyi bir muhasebecidir.

## Temel karşılaştırma

| Özellik | B-tree | LSM-tree |
|---|---|---|
| Noktasal okuma | Genellikle hızlı ve öngörülebilir | Birden fazla seviyeye bakabilir |
| Yazma | Rastgele G/Ç ve sayfa bölünmesi üretebilir | Sıralı ve toplu yazmalarda güçlüdür |
| Aralık sorgusu | Çok başarılıdır | SSTable düzenine göre başarılı olabilir |
| Alan kullanımı | Daha kararlı | Compaction sırasında geçici alan ister |
| Yazma büyütmesi | Güncellemeye bağlıdır | Compaction nedeniyle yüksek olabilir |
| Operasyonel davranış | Daha dengeli gecikme | Compaction sırasında gecikme sıçrayabilir |

LSM-tree okumalarını hızlandırmak için Bloom filter kullanılır. Bloom filter, bir anahtarın belirli SSTable içinde **kesinlikle bulunmadığını** hızlıca söyleyebilir. Yanlış pozitif üretebilir ama yanlış negatif üretmez. Böylece gereksiz disk okumaları azaltılır.

## Küçük bir LSM-tree benzetimi

Aşağıdaki Python kodu, yazmaları bellekte toplar ve eşik aşılınca sıralı bir tabloya dönüştürür:

```python
class MiniLSM:
    def __init__(self, limit=3):
        self.memtable = {}
        self.sstables = []
        self.limit = limit

    def put(self, key, value):
        self.memtable[key] = value
        if len(self.memtable) >= self.limit:
            self.flush()

    def flush(self):
        table = sorted(self.memtable.items())
        self.sstables.insert(0, table)
        self.memtable.clear()
```

Bu örnek gerçek bir WAL, Bloom filter veya compaction içermez; fakat temel fikri gösterir: Her kayıt için diskte farklı bir konuma atlamak yerine veriler bellekte biriktirilir ve topluca sıralı yazılır.

## Hangisini seçmeliyiz?

İş yükünüz yoğun noktasal okumalar, sık güncellemeler ve düşük gecikme beklentisi içeriyorsa B-tree güçlü bir varsayılandır. PostgreSQL ve birçok ilişkisel veritabanının B-tree indekslerini sevmesi tesadüf değildir.

Saniyede çok yüksek sayıda olay, log, telemetri veya zaman serisi verisi yazıyorsanız LSM-tree daha uygun olabilir. Cassandra, RocksDB ve LevelDB bu yaklaşımın bilinen örnekleridir.

Son karar yalnızca “okuma mı, yazma mı?” sorusuna bağlı değildir. Veri boyutu, aralık sorguları, depolama türü, gecikme yüzdelikleri ve compaction için ayrılabilecek kaynaklar da hesaba katılmalıdır. B-tree bugünün düzenini korur; LSM-tree ise bugünün hızını, yarının temizlik işine dönüştürür.

![b-tree-ve-58](/img/b-tree-ve-58.svg)

