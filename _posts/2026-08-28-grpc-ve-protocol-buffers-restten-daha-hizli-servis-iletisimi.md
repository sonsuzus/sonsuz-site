---
layout: post
title: "gRPC ve Protocol Buffers: REST'ten Daha Hızlı Servis İletişimi"
math: true
categories: 
  - Bilgi
tags: 
  - gRPC
  - Protocol Buffers
  - Mikroservis
  - REST
  - Performans
---

Mikroservis mimarisinde servislerin birbirleriyle konuşma hızı, yalnızca kullanıcı deneyimini değil altyapı maliyetini de belirler. REST ve JSON, okunabilirlikleri sayesinde harika bir başlangıç noktasıdır; fakat yüksek trafikte metin ayrıştırma, büyük istek gövdeleri ve tekrar eden HTTP başlıkları pahalılaşabilir. gRPC, bu noktada Protocol Buffers'ın ikili veri biçimini kullanarak daha kompakt, şemaya bağlı ve hızlı bir iletişim katmanı sunar.

``

## Temel fikir: Metin yerine şemalı ikili veri

REST dünyasında bir kullanıcı nesnesi çoğunlukla JSON olarak taşınır. Alan adları her istekte yeniden yazılır ve alıcı taraf bu metni ayrıştırarak nesneye dönüştürür. Protocol Buffers, yani Protobuf, alanları metinsel isimleri yerine sayısal etiketlerle kodlar. Böylece paket küçülür ve serileştirme işlemi daha az CPU harcar.

Bir ağ çağrısının yaklaşık süresini şu şekilde düşünebiliriz:

$$T_{toplam} = T_{bağlantı} + T_{ağ} + T_{serileştirme} + T_{sunucu}$$

gRPC özellikle $T_{serileştirme}$ bileşenini azaltır. HTTP/2 sayesinde aynı bağlantı üzerinde çoklama (multiplexing), başlık sıkıştırma ve çift yönlü akış özellikleri de sunar. Ancak bu formülün sihirli değnek olmadığını unutmayın: Veritabanı sorgusu 800 ms sürüyorsa 2 ms'lik serileştirme kazancı sistemi bir yarış arabasına dönüştürmez.

| Özellik | REST + JSON | gRPC + Protobuf |
|---|---|---|
| Veri biçimi | İnsan tarafından okunabilir metin | Kompakt ikili format |
| Sözleşme | Genellikle OpenAPI ile ayrı yönetilir | `.proto` dosyası doğrudan sözleşmedir |
| Taşıma | Çoğunlukla HTTP/1.1 veya HTTP/2 | HTTP/2 zorunludur |
| Tarayıcı desteği | Doğrudan güçlü | gRPC-Web veya ara katman gerekir |
| Akış iletişimi | Ek çözümler gerektirebilir | Yerleşik streaming desteği |

## `.proto` dosyası: API'nin tek doğruluk kaynağı

gRPC servisleri önce bir Protobuf sözleşmesiyle tanımlanır. Alan numaraları kritik ayrıntıdır: Bir alanın adını değiştirmek çoğu zaman güvenlidir, ama mevcut alan numarasını farklı anlama sahip başka bir alana vermek uyumluluğu bozabilir.

```proto
syntax = "proto3";

package catalog.v1;

service ProductService {
  rpc GetProduct(ProductRequest) returns (ProductReply);
}

message ProductRequest {
  int64 id = 1;
}

message ProductReply {
  int64 id = 1;
  string name = 2;
  double price = 3;
}
```

Bu tanım, istemci ve sunucu için otomatik kod üretiminin kaynağıdır. Örneğin Go tarafında üretilen istemci, `GetProduct` metodunu sıradan bir fonksiyon çağrısına yakın biçimde kullanmanızı sağlar:

```go
reply, err := client.GetProduct(ctx, &pb.ProductRequest{Id: 42})
if err != nil {
    return fmt.Errorf("ürün servisi çağrısı başarısız: %w", err)
}
fmt.Printf("%s: %.2f\n", reply.Name, reply.Price)
```

Burada ağ çağrısı gerçekte hâlâ vardır; `context` içindeki zaman aşımı ve iptal sinyalleri bu nedenle önemlidir. Dağıtık sistemlerde "fonksiyon gibi görünüyor" diye çağrıyı sınırsız bekletmek klasik bir tuzaktır.

## Dört iletişim modeli

| Model | Açıklama | Örnek kullanım |
|---|---|---|
| Unary | Tek istek, tek yanıt | Ürün detayı getirme |
| Server streaming | Tek istek, yanıt akışı | Log veya fiyat güncellemeleri |
| Client streaming | İstek akışı, tek yanıt | Toplu telemetri gönderimi |
| Bidirectional streaming | İki taraf da akış gönderir | Canlı sohbet, oyun olayları |

Performans testlerini yalnızca ortalama gecikmeyle değerlendirmeyin. p95 ve p99 gecikmeleri, hata oranı, paket boyutu ve CPU kullanımı birlikte izlenmelidir. Ayrıca gRPC'nin hata modeli HTTP durum kodlarından farklıdır; `UNAVAILABLE`, `DEADLINE_EXCEEDED` ve `INVALID_ARGUMENT` gibi durumları anlamlı biçimde eşlemek gerekir.

Sonuç olarak gRPC, servisler arası yoğun ve şeması belirgin iletişim için güçlü bir tercihtir. Buna karşılık herkese açık, tarayıcı merkezli ve elle test edilmesi gereken API'lerde REST hâlâ son derece pratiktir. En iyi mimari çoğu zaman "REST mi gRPC mi?" değil, doğru sınırda doğru protokolü seçmektir.
