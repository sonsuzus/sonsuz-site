---
layout: post
title: "MongoDB’de Sharding ve Replication: Yüksek Erişilebilirlik ile Hızlı Yazmanın Dengesi"
math: true
categories: 
  - Bilgi
tags: 
  - mongodb
  - sharding
  - replication
toc: true
image: /img/mongodbde-sharding-ve-66.png
---

MongoDB, büyüyen uygulamalarda yalnızca daha fazla veri saklama problemiyle değil, aynı anda gelen binlerce isteği güvenle işleme problemiyle de karşılaşır. Bu noktada **replication**, sistemin ayakta kalmasını sağlayan güvenlik ağıdır; **sharding** ise veriyi ve yazma yükünü birden fazla makineye dağıtan ölçekleme motorudur. İkisini birlikte doğru tasarlamak, hem kesintilere dayanıklı hem de yüksek yazma kapasiteli bir mimari oluşturur.
``

## İki kavram, iki farklı sorun

Replication, aynı verinin birden fazla sunucuda kopyalanmasıdır. MongoDB’de bu yapı genellikle **replica set** olarak kurulur: Birincil düğüm (*primary*) yazmaları kabul eder, ikincil düğümler (*secondary*) ise işlemleri oplog üzerinden takip ederek veriyi çoğaltır. Primary devre dışı kalırsa üyeler seçim yapar ve uygun bir secondary yeni primary olur.

Sharding ise koleksiyon verisini parçalara (*chunk*) ayırıp farklı shard’lara dağıtır. Böylece tek bir sunucunun CPU, RAM, disk I/O veya yazma kilidi benzeri kaynak sınırlarına takılmak yerine, iş yükü yatay olarak büyütülebilir.

| Özellik | Replication | Sharding |
|---|---|---|
| Ana amaç | Hata toleransı ve okunabilirlik | Kapasite ve yazma ölçekleme |
| Veri yapısı | Aynı verinin kopyaları | Verinin farklı parçaları |
| Yazma noktası | Replica set primary’si | Her shard’ın kendi primary’si |
| Arıza etkisi | Otomatik failover | Yük diğer shard’lara dağılmıştır |

## Yüksek erişilebilirlik: Replica set’in rolü

Yüksek erişilebilirlik, yalnızca sunucunun açık olması değildir; bir düğüm, veri merkezi veya ağ bağlantısı kaybedildiğinde uygulamanın kabul edilebilir sürede çalışmaya devam etmesidir. MongoDB’de bunun temel aracı, tek sayıda oy hakkına sahip üyelerden oluşan replica set’tir. Örneğin üç üyeli bir yapı, çoğunluğu koruduğu sürece seçim yapabilir:

$$\text{Majority} = \left\lfloor \frac{n}{2} \right\rfloor + 1$$

Üç oy veren üyede çoğunluk 2’dir. Bu nedenle bir düğüm kaybedildiğinde iki üye karar verebilir; ancak iki düğüm birden kaybedilirse yazılabilir primary seçilemez. Üretimde üyeleri farklı kullanılabilirlik bölgelerine yaymak, tek bir altyapı arızasının tüm kopyaları etkilemesini önler.

Yazma dayanıklılığı için `writeConcern: "majority"` kritik bir tercihtir. Bu ayar, işlemin çoğunluk tarafından onaylanmasını bekler. Gecikme biraz artabilir; fakat primary’nin hemen ardından çökmesi durumunda yazının geri alınma riski belirgin biçimde azalır.

```javascript
const result = await db.collection("orders").insertOne(
  { customerId: 42, total: 799, status: "paid" },
  { writeConcern: { w: "majority", j: true } }
);
```

Bu örnekte `w: "majority"`, çoğunluk replikasyonunu; `j: true` ise işlemin primary’nin journal kaydına yazılmasını ister. Ödeme gibi kritik alanlarda bu küçük bekleme, oldukça iyi bir sigortadır.

## Yazma performansı: Shard key her şeydir

Sharded bir kümede uygulama önce `mongos` yönlendiricisine bağlanır. `mongos`, shard key’e göre isteği ilgili shard’a gönderir. Her shard çoğu zaman kendi replica set’idir; dolayısıyla hem dağıtık yazma hem de failover elde edilir.

Ancak kötü shard key, güçlü donanımı bile tek şeritli yola çevirir. Sürekli artan bir `createdAt` alanı seçilirse yeni kayıtlar hep son chunk’a gider ve tek shard sıcak nokta (*hotspot*) olur. Hash tabanlı anahtarlar yazmaları daha dengeli dağıtır; buna karşılık aralık sorgularını pahalılaştırabilir.

| Shard key yaklaşımı | Yazma dağılımı | Aralık sorguları | Risk |
|---|---|---|---|
| Artan tarih | Zayıf | Çok iyi | Son shard’a yığılma |
| Hashed kullanıcı ID | Çok iyi | Zayıf | Scatter-gather sorguları |
| Bileşik anahtar | İyi tasarlanırsa iyi | İyi olabilir | Tasarım karmaşıklığı |

Örneğin siparişlerde kullanıcı odaklı sorgular yaygınsa şu tasarım mantıklıdır:

```javascript
sh.shardCollection(
  "shop.orders",
  { customerId: "hashed", createdAt: 1 }
);
```

İlk alanın hash’lenmesi kullanıcıları shard’lara yayar. `createdAt` ise aynı müşteri içindeki zaman sıralı sorgular için ek bağlam sağlar. Yine de gerçek karar, sorgu örüntülerinin ve veri büyümesinin ölçülmesiyle verilmelidir.

## Dengeli mimari için sonuç

En sağlam pratik, her shard’ı üç üyeli bir replica set olarak çalıştırmaktır. Replication erişilebilirliği, sharding ise yazma paralelliğini getirir. Buna ek olarak shard key’i gerçek sorgulara göre seçmek, majority write concern’i kritik veride kullanmak ve balancer durumunu izlemek gerekir. Kısacası MongoDB’de hız, yalnızca daha çok sunucu eklemekle değil; verinin nereye, hangi garantilerle ve hangi erişim desenine göre yazıldığını bilinçli tasarlamakla gelir.

![mongodbde-sharding-ve-66](/img/mongodbde-sharding-ve-66.svg)

