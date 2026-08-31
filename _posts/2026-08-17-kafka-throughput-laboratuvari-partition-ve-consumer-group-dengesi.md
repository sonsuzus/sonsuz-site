---
layout: post
title: "Kafka Throughput Laboratuvarı: Partition ve Consumer Group Dengesi"
math: true
categories: 
  - Bilgi
tags: 
  - apache kafka
  - throughput
  - consumer group
image: /img/kafka-throughput-laboratuvari-83.png
---

Apache Kafka'da yüksek iş hacmi yalnızca daha güçlü sunucular eklemekle elde edilmez; partition sayısı, consumer group içindeki tüketici sayısı, mesaj boyutu ve disk-ağ kapasitesi birlikte çalışır. En iyi yapılandırma, tahminle değil ölçümle bulunur. Bu yazıda kontrollü deneyler kurarak partition ve consumer group kararlarının üretim (produce) ve tüketim (consume) throughput'unu nasıl değiştirdiğini inceleyeceğiz.

![kafka-throughput-laboratuvari-83](/img/kafka-throughput-laboratuvari-83.svg)

``

Kafka'nın paralellik birimi **partition**'dır. Bir topic içindeki her partition, sıralı ve değiştirilemez bir kayıt günlüğüdür. Aynı consumer group'ta bir partition aynı anda yalnızca tek bir consumer tarafından okunabilir. Bu nedenle etkin tüketim paralelliği kabaca şu formülle sınırlıdır:

$$P_{etkin} = \min(P, C)$$

Burada $P$ partition sayısı, $C$ ise gruptaki aktif consumer sayısıdır. Örneğin 12 partition'lı bir topic'i 4 consumer okursa, her consumer ortalama 3 partition üstlenir. Consumer sayısını 12'ye çıkarınca teorik paralellik artar; 16'ya çıkarınca ise 4 consumer boşta kalır. Fazla consumer, koordinasyon ve rebalance maliyeti dışında sihirli bir hız kazandırmaz.

| Durum | Partition | Consumer | Beklenen sonuç |
|---|---:|---:|---|
| Az paralellik | 3 | 8 | 5 consumer atıl kalır |
| Dengeli yapı | 12 | 12 | Her consumer bir partition okur |
| Consumer eksik | 24 | 6 | Her consumer çok sayıda partition taşır |
| Aşırı partition | 500 | 12 | Metadata, dosya tanıtıcısı ve yönetim maliyeti artar |

Throughput'u basitçe saniye başına işlenen veri olarak düşünebiliriz:

$$T = \frac{N \times S}{t}$$

$N$ işlenen mesaj sayısı, $S$ ortalama mesaj boyutu ve $t$ geçen süredir. Ancak gerçek sistemde $T$, en yavaş bileşen tarafından sınırlandırılır: producer'ın sıkıştırması, broker diski, replikasyon, ağ, consumer'ın iş mantığı veya hedef veritabanı. Bu yüzden deneylerde yalnızca partition sayısını değiştirip diğer değişkenleri mümkün olduğunca sabit tutmak gerekir.

İlk deney için aynı replication factor'a sahip üç topic oluşturun: 3, 12 ve 24 partition. Üretici tarafında sabit mesaj boyutu, örneğin 1 KB, sabit toplam kayıt sayısı ve aynı `acks` değeri kullanın. Ardından consumer group boyutunu 1, 3, 6, 12 ve 24 olarak değiştirin. Kafka'nın kendi performans aracını başlangıç noktası olarak kullanabilirsiniz:

```bash
kafka-producer-perf-test.sh \
  --topic throughput-lab-12 \
  --num-records 5000000 \
  --record-size 1024 \
  --throughput -1 \
  --producer-props bootstrap.servers=localhost:9092 acks=all compression.type=lz4

kafka-consumer-perf-test.sh \
  --bootstrap-server localhost:9092 \
  --topic throughput-lab-12 \
  --group lab-group-12 \
  --messages 5000000
```

Bu komutlar üretim ve tüketim hızını ölçer. `acks=all`, liderin yanı sıra senkron replikaların da yazmayı onaylamasını beklediği için dayanıklılığı artırır; buna karşılık gecikme ve throughput üzerinde baskı oluşturabilir. Deneyin ikinci turunda `acks=1` kullanarak dayanıklılık-performans değiş tokuşunu ayrıca gözlemleyin.

Sonuçları sadece MB/s olarak kaydetmeyin. Consumer lag, p95 gecikme, CPU, disk I/O, ağ kullanımı ve rebalance sayısını da tabloya ekleyin. Özellikle consumer sayısını artırdığınızda lag düşmüyor ama CPU yükseliyorsa darboğaz muhtemelen consumer işleme kodunda veya dış sistemdedir.

| Gözlem | Olası neden | Deneysel aksiyon |
|---|---|---|
| Consumer eklenince hız artmıyor | Partition sayısı yetersiz | Partition sayısını kademeli artırın |
| Lag sürekli büyüyor | Tüketim hızı üretimden düşük | Consumer işini ve batch ayarlarını inceleyin |
| Rebalance sırasında duraklama | Sık üyelik değişimi | Static membership ve cooperative assignor değerlendirin |
| Broker CPU'su yüksek | Çok küçük mesajlar veya aşırı partition | Batching ve sıkıştırma deneyin |

Unutmayın: Daha fazla partition her zaman daha fazla hız değildir. Partition; dosya, indeks, replica trafiği ve controller metadata maliyeti demektir. Başlangıç için beklenen tüketim paralelliğini karşılayan, büyümeye makul pay bırakan bir sayı seçin. Sonra gerçekçi veri, gerçekçi consumer işlemi ve tekrarlanabilir deneylerle eğriyi ölçün. Kafka optimizasyonunda en değerli metrik, teorik maksimum değil; kabul edilebilir gecikmeyle sürdürülebilir throughput'tur.
