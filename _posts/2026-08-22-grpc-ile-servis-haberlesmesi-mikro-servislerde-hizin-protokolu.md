---
layout: post
title: "gRPC ile Servis Haberleşmesi: Mikro Servislerde Hızın Protokolü"
math: true
categories: 
  - Bilgi
tags: 
  - gRPC
  - Mikro Servisler
  - Protocol Buffers
---

Mikro servis mimarisinde servisler birbirinden bağımsız çalışır; ancak işin sihirli kısmı bu servislerin güvenilir ve hızlı biçimde konuşabilmesidir. REST, insan tarafından okunabilir JSON yapısıyla harika bir başlangıç noktasıdır. Buna karşın çok yoğun trafik, düşük gecikme ve güçlü tip güvenliği gerektiğinde gRPC sahneye çıkar. HTTP/2 üzerinde çalışan gRPC, veriyi Protocol Buffers (Protobuf) ile ikili formatta taşıyarak ağdaki gereksiz yükü azaltır.
``
## Neden gRPC hızlıdır?

gRPC'nin performans avantajı tek bir nedene dayanmaz. Öncelikle JSON metinsel bir formattır; alan adları da her istekte tekrar taşınır. Protobuf ise şemaya göre serileştirilmiş kompakt ikili mesajlar üretir. Mesaj boyutu küçüldükçe ağ aktarım süresi de genel olarak azalır:

$$T_{toplam} = T_{serileştirme} + \frac{Mesaj\ Boyutu}{Bant\ Genişliği} + T_{ağ} + T_{sunucu}$$

Ayrıca HTTP/2, tek TCP bağlantısı üzerinde birden fazla isteği eşzamanlı taşıyabilen multiplexing özelliğine sahiptir. Böylece bağlantı sayısı ve başlık maliyeti düşer. Header compression da bu hız şölenine küçük ama değerli bir katkı yapar.

| Özellik | REST + JSON | gRPC + Protobuf |
|---|---|---|
| Veri biçimi | Metin tabanlı | İkili, kompakt |
| Sözleşme | Genellikle OpenAPI ile ayrı tutulur | `.proto` dosyasında doğrudan tanımlıdır |
| Taşıma | Çoğunlukla HTTP/1.1 | HTTP/2 |
| Streaming | Ek çözümler gerektirebilir | Yerleşik destek |
| Tarayıcı uyumu | Doğrudan güçlü | gRPC-Web gerekebilir |

## Sözleşme önce gelir: Proto dosyası

gRPC dünyasında API sözleşmesi `.proto` dosyasıdır. Bu dosya; servisleri, metotları ve mesajların alanlarını tanımlar. Kod üretim araçları bu şemadan Java, Go, C#, Python veya Node.js istemci-sunucu sınıfları oluşturur. Böylece `string` bekleyen yere yanlışlıkla nesne göndermek gibi sürprizler derleme aşamasında yakalanabilir.

Aşağıdaki örnek, ürün bilgisini getiren küçük bir katalog servisini tanımlar:

```proto
syntax = "proto3";

package catalog;

service ProductService {
  rpc GetProduct (ProductRequest) returns (ProductReply);
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

Buradaki alan numaraları (`1`, `2`, `3`) Protobuf'un ikili kodlamasında kritik rol oynar. Yayına alınmış bir alanın numarasını değiştirmek uyumluluğu bozabilir. Yeni alan eklemek ise çoğunlukla geriye uyumludur; eski istemciler tanımadıkları alanları görmezden gelir. Bu nedenle silinen alan numaralarını yeniden kullanmamak iyi bir alışkanlıktır.

## Dört farklı iletişim modeli

gRPC sadece klasik istek-cevap yaklaşımına mahkûm değildir. Gerçek zamanlı ihtiyaçlar için streaming modelleri sunar.

| Model | Açıklama | Örnek kullanım |
|---|---|---|
| Unary | Tek istek, tek yanıt | Ürün detayı sorgulama |
| Server streaming | İstemci bir istek, sunucu çok yanıt | Log veya fiyat akışı |
| Client streaming | İstemci çok mesaj, sunucu tek yanıt | Toplu telemetri gönderimi |
| Bidirectional streaming | İki taraf da akış gönderir | Sohbet, canlı koordinasyon |

Örneğin sipariş servisinin stok servisine yaptığı sorgu unary RPC için uygundur. Ancak kurye konumlarını anlık iletmek istiyorsanız çift yönlü akış, sürekli polling yapmaktan çok daha zarif bir çözüm olabilir.

## Üretimde dikkat edilmesi gerekenler

Yüksek performans, sınırsız bekleme anlamına gelmez. Her RPC çağrısına deadline tanımlayın; aksi halde yavaşlayan bir bağımlılık bağlantı havuzlarını tüketerek zincirleme arızaya yol açabilir. Retry işlemlerini ise yalnızca idempotent çağrılarda ve exponential backoff ile uygulayın. Kimlik doğrulama için TLS, JWT veya mTLS tercih edin; servisler arası ağın "zaten güvenli" olduğu varsayımı pahalı bir mittir.

Son olarak gözlemlenebilirlik ekleyin: correlation ID, dağıtık izleme ve metrikler olmadan hızlı bir sistemde bile sorunun nerede olduğunu bulmak yavaş kalır. gRPC, güçlü sözleşmesi, streaming yetenekleri ve HTTP/2 tabanı sayesinde mikro servisler için etkileyici bir araçtır; fakat en iyi sonuç, doğru sınırlar çizilmiş servisler ve disiplinli hata yönetimiyle gelir.
