---
layout: post
title: "Apache Kafka'da Exactly-Once Semantics: Mesaj Tekrarını Kayıpsız Engellemek"
math: true
categories: 
  - Bilgi
tags: 
  - apache kafka
  - exactly-once
  - dağıtık sistemler
  - transaction
  - mesajlaşma
  - java
toc: true
image: /img/apache-kafkada-exactly-44.png
---

![apache-kafkada-exactly-44](/img/apache-kafkada-exactly-44.svg)


Dağıtık sistemlerin klasik kâbusu şudur: Servis ödemeyi işler, Kafka'ya onay gönderirken ağ kopar ve mesajın ulaşıp ulaşmadığını öğrenemez. Tekrar gönderirse müşteri iki kez ücretlendirilebilir; göndermezse işlem kaybolabilir. Apache Kafka'nın Exactly-Once Semantics, yani EOS mimarisi, yeniden denemeleri yasaklamak yerine aynı mantıksal işlemin sonuçlarını yalnızca bir kez görünür hâle getirir.

``

## Önce teslimat garantilerini ayıralım

Bir üretici mesajı gönderdiğinde broker yanıtı kaybolabilir. Üretici açısından sonuç belirsizdir: Mesaj gerçekten kaybolmuş veya başarıyla yazılmış olabilir. Bu nedenle dağıtık sistemlerde “tekrar deneme” kaçınılmazdır.

| Garanti | Kayıp olabilir mi? | Tekrar olabilir mi? | Yaklaşım |
|---|---:|---:|---|
| At-most-once | Evet | Hayır | Bir kez dene, başarısızlığı kabul et |
| At-least-once | Hayır | Evet | Onay gelene kadar yeniden dene |
| Exactly-once | Hayır | Mantıksal olarak hayır | Tekilleştirme ve transaction kullan |

Bir mesajın $n$ kez fiziksel olarak gönderilmesine rağmen çıktıda bir kez etkili olması şöyle ifade edilebilir:

$$\text{effect}(m^1, m^2, \ldots, m^n) = \text{effect}(m)$$

Buradaki kritik ayrım, “mesaj ağda yalnızca bir kez dolaşır” değil, “mesajın oluşturduğu sonuç yalnızca bir kez görünür” ifadesidir.

## Kafka bunu nasıl başarıyor?

EOS üç mekanizmanın birlikte çalışmasına dayanır.

### 1. Idempotent producer

`enable.idempotence=true` olduğunda broker üreticiye bir Producer ID verir. Her partition'a gönderilen kayıtlar sıralı sequence numaraları taşır. Broker aynı Producer ID ve sıra numarasını yeniden görürse kaydı ikinci kez eklemez.

$$KayıtKimliği = (ProducerId, Partition, SequenceNumber)$$

Bu mekanizma yeniden denemeden kaynaklanan kopyaları önler; ancak birden fazla partition'a yapılan yazmaları tek başına atomik hâle getirmez.

### 2. Transactional producer

`transactional.id`, üreticinin farklı oturumlarda tanınmasını sağlar. Üretici transaction başlatır, bir veya daha fazla topic-partition'a kayıt yazar ve sonunda tamamını commit ya da abort eder. Böylece “A topic'ine yazıldı ama B topic'ine yazılamadı” biçimindeki yarım sonuçlar görünmez.

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("enable.idempotence", "true");
props.put("transactional.id", "payment-service-1");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.initTransactions();

try {
    producer.beginTransaction();
    producer.send(new ProducerRecord<>("payments", "order-42", "PAID"));
    producer.send(new ProducerRecord<>("notifications", "order-42", "SEND_RECEIPT"));
    producer.commitTransaction();
} catch (Exception error) {
    producer.abortTransaction();
    throw error;
}
```

Kod, ödeme ve bildirim kayıtlarını aynı atomik sınır içine alır. Commit başarısızsa iki kayıt da tüketicilere tamamlanmış işlem olarak sunulmaz.

### 3. Transaction-aware consumer

Tüketicinin yarım kalmış kayıtları okumaması gerekir:

```java
props.put("isolation.level", "read_committed");
```

`read_committed`, yalnızca commit edilmiş transaction kayıtlarını döndürür. Varsayılan `read_uncommitted` ise abort edilecek kayıtları geçici olarak görebilir.

## Consume–transform–produce döngüsü

Bir uygulama girdiyi okuyup yeni çıktı üretiyorsa sadece sonucu değil, tüketici offset'ini de aynı transaction içinde commit etmelidir:

```java
producer.beginTransaction();
producer.send(new ProducerRecord<>("validated-orders", key, result));
producer.sendOffsetsToTransaction(offsets, consumer.groupMetadata());
producer.commitTransaction();
```

Böylece çıktı yazılıp offset ilerlememesi veya offset ilerleyip çıktının kaybolması engellenir. Kafka Streams, `processing.guarantee=exactly_once_v2` ayarıyla bu modeli daha az tesisat koduyla uygular.

## Önemli sınır: Kafka dışı yan etkiler

EOS, Kafka içindeki consume–process–produce zincirinde güçlüdür; banka API'si çağrısını veya bağımsız veritabanı güncellemesini sihirli biçimde transaction'a katmaz. Dış sistemlerde idempotency key, transactional outbox, inbox tablosu ya da uygun bir koordinasyon deseni gerekir. Örneğin `order-42` benzersiz anahtar yapılırsa aynı ödeme talebi tekrar işlense bile ikinci kayıt reddedilir.

Sonuç olarak sağlam mimari; idempotent producer, benzersiz `transactional.id`, atomik offset commit, `read_committed` tüketiciler ve dış yan etkiler için idempotency/outbox katmanından oluşur. Kafka tekrar denemeyi ortadan kaldırmaz; tekrarın sonuçları çoğaltmasını engeller. Dağıtık sistemlerde gerçek süper güç de tam olarak budur.
