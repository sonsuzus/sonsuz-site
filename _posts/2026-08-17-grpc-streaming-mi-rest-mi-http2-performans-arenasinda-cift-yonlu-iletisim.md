---
layout: post
title: "gRPC Streaming mi REST mi? HTTP/2 Performans Arenasında Çift Yönlü İletişim"
math: true
categories: 
  - Bilgi
tags: 
  - gRPC
  - HTTP/2
  - REST
  - Performans Testi
  - Streaming
---

Modern servisler yalnızca istek alıp JSON döndüren yapılardan ibaret değil: canlı konum, borsa verisi, oyun olayları ve telemetri akışları sürekli iletişim bekliyor. Bu noktada gRPC’nin HTTP/2 üzerinde çalışan streaming modeli, REST’in klasik istek-cevap ritmine güçlü bir alternatif sunar. Ancak “gRPC her zaman hızlıdır” demek yerine; gecikme, mesaj boyutu, eşzamanlı bağlantı ve iş yükü türü üzerinden ölçüm yapmak gerekir.
``
## Aynı bağlantıda daha fazla konuşma

REST çoğunlukla HTTP/1.1 veya HTTP/2 üzerinde, bağımsız HTTP istekleriyle kullanılır. Her çağrı; URL, başlıklar, doğrulama bilgileri ve çoğu zaman metinsel JSON gövdesi taşır. HTTP/2 kullanılsa bile REST tasarımı genellikle tek isteğe tek yanıt semantiğinde kalır.

gRPC ise sözleşmesini `.proto` dosyasıyla tanımlar ve veriyi ikili **Protocol Buffers** biçiminde taşır. HTTP/2'nin stream multiplexing özelliği sayesinde tek TCP bağlantısında çok sayıda mantıksal akış aynı anda ilerler. Bu, özellikle bağlantı sayısını artırmadan yoğun eşzamanlılık elde etmek isteyen servisler için değerlidir.

Dört temel iletişim biçimi vardır:

| Model | İstemci mesajı | Sunucu mesajı | Uygun senaryo |
|---|---:|---:|---|
| Unary | 1 | 1 | Kullanıcı profili sorgulama |
| Server streaming | 1 | N | Log veya fiyat akışı |
| Client streaming | N | 1 | Toplu telemetri yükleme |
| Bidirectional streaming | N | N | Sohbet, oyun, ortak düzenleme |

Çift yönlü akışta taraflar birbirini beklemek zorunda değildir. Sunucu olay gönderirken istemci de yeni komutlar iletebilir. Bu asenkron yapı, polling yaklaşımının ürettiği gereksiz istekleri azaltır.

## Performansı belirleyen teori

Bir çağrının yaklaşık toplam süresini şöyle düşünebiliriz:

$$T_{toplam} = T_{bağlantı} + T_{serileştirme} + T_{ağ} + T_{sunucu} + T_{kuyruk}$$

gRPC, kalıcı bağlantı ve küçük Protobuf paketleri sayesinde özellikle $T_{bağlantı}$ ile $T_{serileştirme}$ bileşenlerini düşürmeyi hedefler. JSON alan adlarını metin olarak tekrar ederken Protobuf alan numaraları ve ikili değerler kullanır. Bunun karşılığında veriyi tarayıcıda doğrudan incelemek zorlaşır; şema yönetimi ve araç desteği daha önemli hâle gelir.

| Kriter | REST + JSON | gRPC + Protobuf |
|---|---|---|
| Veri okunabilirliği | Çok yüksek | Düşük, araç gerekir |
| Paket boyutu | Genellikle daha büyük | Genellikle daha küçük |
| Tarayıcı uyumu | Doğrudan güçlü | gRPC-Web gerekebilir |
| Uzun süreli akış | SSE/WebSocket eklenir | Yerleşik streaming |
| Sözleşme disiplini | Opsiyonel | `.proto` ile güçlü |

## Adil bir benchmark nasıl kurulur?

Karşılaştırmada aynı iş mantığını kullanın: örneğin 1 KB, 10 KB ve 100 KB olay paketleri; 100, 1.000 ve 10.000 eşzamanlı istemci; ayrıca sabit ve değişken ağ gecikmeleri. REST tarafında keep-alive açık olmalı; gRPC tarafında TLS, sıkıştırma ve bağlantı havuzu ayarları açıkça kaydedilmelidir. Aksi hâlde ölçülen şey protokolden çok hatalı yapılandırma olur.

Ölçülecek ana metrikler şunlardır:

- p50, p95 ve p99 gecikme süreleri
- Saniye başına mesaj veya istek sayısı
- CPU kullanımı, bellek tahsisi ve GC duraklamaları
- Ağdan geçen toplam bayt miktarı
- Hata oranı ve yeniden bağlanma davranışı

Örneğin k6 ile REST uç noktasını yükleyebilirsiniz:

```javascript
import http from 'k6/http';

export const options = { vus: 200, duration: '30s' };

export default function () {
  http.post('https://api.example.com/events',
    JSON.stringify({ deviceId: 42, value: 18.7 }),
    { headers: { 'Content-Type': 'application/json' } }
  );
}
```

Bu senaryo 200 sanal kullanıcıyla JSON olay gönderir. gRPC için k6'nın gRPC istemcisi, ghz veya grpcurl tabanlı ayrı bir test kullanılabilir; aynı olay sayısı ve aynı payload anlamı korunmalıdır.

## Sonuç: kazanan iş yüküne bağlı

gRPC streaming; yüksek frekanslı olaylar, servisler arası iletişim ve anlık çift yönlü veri akışında çoğu zaman daha düşük gecikme ve daha az ağ maliyeti sağlar. REST ise insan tarafından okunabilirliği, HTTP ekosistemi ve tarayıcı erişimi sayesinde public API'lerde son derece pratiktir. En sağlıklı mimari hibrit olabilir: dış dünyaya REST, iç servis ağına gRPC; gerçek kararı ise varsayımlar değil p99 grafikleri verir.
