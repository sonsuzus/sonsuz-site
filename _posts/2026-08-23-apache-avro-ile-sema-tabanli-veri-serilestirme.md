---
layout: post
title: "Apache Avro ile Şema Tabanlı Veri Serileştirme"
math: true
categories: 
  - Bilgi
tags: 
  - apache avro
  - veri serileştirme
  - şema
  - kafka
toc: true
---

Dağıtık sistemlerde servislerin birbiriyle konuşması çoğu zaman “JSON gönder, mutlu ol” kadar basit görünür. Ancak milyonlarca olayın aktığı Kafka hatlarında, veri depolarında veya mikroservis ağlarında metin tabanlı ve şemasız veri hızla maliyetli hâle gelir. Apache Avro; veriyi ikili biçimde kompakt taşıyan, yapısını ise açık bir şema ile tanımlayan bir serileştirme formatıdır. En önemli numarası, yalnızca alan adlarını değil, verinin zaman içindeki değişimini de yönetilebilir kılmasıdır.
``

## Serileştirme Neyi Çözer?

Serileştirme, bellekteki bir nesneyi ağda gönderebileceğimiz ya da diske yazabileceğimiz bayt dizisine dönüştürme işlemidir. Ters işlem ise deserializasyondur. Örneğin bir `User` nesnesi, uygulama içinde alanlara sahipken ağ üzerinde yalnızca baytlardan oluşur. Avro bu dönüşüm sırasında verinin **writer schema**sını (üreten taraf) ve **reader schema**sını (okuyan taraf) dikkate alır.

Kabaca veri taşıma maliyetini şöyle düşünebiliriz:

$$Toplam\ Boyut = Veri\ Değerleri + Meta\ Veri$$

JSON’da alan adları her kayıtta tekrar eder. Avro’da ise alanların sırası ve tipi şemadan bilindiği için ikili veri çoğunlukla değerleri taşır. Bu, özellikle küçük mesajların çok sık üretildiği sistemlerde ağ ve depolama kazancı sağlar.

| Özellik | JSON | Apache Avro |
|---|---|---|
| Temsil biçimi | İnsan okunabilir metin | Kompakt ikili veri |
| Şema | Opsiyonel, genellikle harici | Formatın merkezinde |
| Alan adları | Her mesajda bulunur | Şemadan çıkarılır |
| Şema evrimi | Uygulama kurallarına bağlı | Yerleşik uyumluluk yaklaşımı |
| Hata yakalama | Çoğunlukla çalışma zamanında | Şema doğrulamasıyla erken |

## Şema: Sözleşmenin Kendisi

Avro şemaları yaygın olarak JSON ile yazılır. Aşağıdaki kayıt, bir kullanıcı olayının temel sözleşmesini tanımlar:

```json
{
  "type": "record",
  "name": "UserCreated",
  "namespace": "com.ornek.events",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "createdAt", "type": "long"},
    {"name": "marketingConsent", "type": "boolean", "default": false}
  ]
}
```

Burada `default` alanı küçük ama kritik bir kahramandır. Eski üreticiler `marketingConsent` göndermese bile yeni okuyucular varsayılan `false` ile çalışabilir. Bu yaklaşım, geriye uyumluluğun temelidir. Buna karşılık zorunlu ve varsayılanı olmayan yeni bir alan eklemek, eski mesajları okuyamayan tüketiciler üretebilir.

| Değişiklik | Geriye uyumluluk etkisi | Güvenli yaklaşım |
|---|---|---|
| Varsayılanlı alan eklemek | Genellikle uyumlu | `default` tanımla |
| Alan silmek | Okuyucuya bağlı | Önce kullanımını kaldır |
| Alan adını değiştirmek | Riskli | Alias veya yeni alan kullan |
| Alan tipini değiştirmek | Çoğunlukla riskli | Yeni alanla kademeli geçiş yap |

## Üretici ve Tüketici Aynı Anda Güncellenmez

Gerçek hayatta tüm servisleri tek bir dağıtımla güncellemek nadirdir. Avro’nun değeri tam burada ortaya çıkar: Üretici yeni şemayla yazarken tüketici kendi şemasına göre okuyabilir. Uyumlu bir dönüşüm varsa veri akışı kesilmez. Şema kayıt defterleri (örneğin Schema Registry) şemaları kimliklendirerek mesajlara büyük şemayı eklemek yerine küçük bir şema kimliği koyar.

Python tarafında `fastavro` ile şema doğrulamalı bir kayıt üretmek şöyle görünür:

```python
from fastavro import parse_schema, schemaless_writer
from io import BytesIO

schema = parse_schema({
    "type": "record", "name": "UserCreated",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "email", "type": "string"},
        {"name": "createdAt", "type": "long}
    ]
})

record = {"id": "u-42", "email": "ada@example.com", "createdAt": 1720000000}
buffer = BytesIO()
schemaless_writer(buffer, schema, record)
payload = buffer.getvalue()
```

Bu örnekte `schemaless_writer`, şemayı mesaja gömmek yerine yalnızca kaydı ikili biçimde yazar; şema alıcı tarafından ayrıca bilinmelidir. Üretim ortamında şema kimliği ve kayıt defteri entegrasyonu eklenir.

Avro, her durumda JSON’un yerine geçecek sihirli değnek değildir. İnsanların API yanıtlarını elle incelemesi gereken basit HTTP uçlarında JSON daha pratiktir. Fakat yüksek hacim, uzun ömürlü olay akışları ve bağımsız ekipler söz konusuysa Avro; veri sözleşmesini görünür, boyutu küçük ve değişimi kontrollü hâle getirir. Kısacası, “bu alan neydi?” tartışmasını şemaya devreder.
