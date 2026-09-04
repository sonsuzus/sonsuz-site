---
layout: post
title: "LSP Mimarisi: Bir Protokol, Yüzlerce Dil ve Daha Akıllı Editörler"
math: true
categories: 
  - Bilgi
tags: 
  - lsp
  - editör
  - yazılım mimarisi
toc: true
---

Bir zamanlar her kod editörünün, desteklediği her programlama dili için ayrı bir eklenti geliştirmesi gerekiyordu. Kod tamamlama, hata tespiti ve sembol bulma gibi özellikler editör ile dil arasında tekrar tekrar yazılıyordu. Language Server Protocol, yani LSP, bu zahmetli ilişkiye standart bir iletişim katmanı ekleyerek modern editörlerin yüzlerce dili destekleyebilmesini sağladı.
``

## LSP hangi problemi çözer?

Bir editörün $M$ farklı dili, her dilin de $N$ farklı editörü desteklediğini düşünelim. Doğrudan entegrasyon yaklaşımında yaklaşık olarak

$$M \times N$$

adet bağlantı geliştirmek gerekir. LSP kullanıldığında diller birer **dil sunucusu**, editörler ise birer **LSP istemcisi** uygular. Böylece ihtiyaç duyulan bileşen sayısı yaklaşık

$$M + N$$

olur. Örneğin 20 dil ve 10 editör için teorik entegrasyon sayısı 200'den 30'a düşebilir. Protokolün en büyük kazancı tam olarak bu ayrıştırmadır.

| Geleneksel yaklaşım | LSP yaklaşımı |
|---|---|
| Her editör-dil çifti için özel entegrasyon | Ortak ve açık protokol |
| Dil analizi editör eklentisine gömülebilir | Analiz ayrı bir süreçte yapılır |
| Özelliklerin taşınması zordur | Sunucu farklı editörlerde kullanılabilir |
| Bakım maliyeti yüksektir | Sorumluluklar daha nettir |

## Mimarinin oyuncuları

LSP mimarisinde iki temel taraf bulunur. **İstemci**, VS Code, Neovim veya başka bir geliştirme ortamıdır. Kullanıcının belge açması, karakter yazması ya da imleci hareket ettirmesi gibi olayları sunucuya iletir. **Dil sunucusu** ise kaynak kodu ayrıştırır; tür sistemi, sembol tablosu ve proje bağımlılıkları gibi dile özgü bilgileri yönetir.

İletişim çoğunlukla JSON-RPC 2.0 mesajlarıyla yapılır. Taraflar standart giriş/çıkış akışlarını, soketleri veya başka taşıma kanallarını kullanabilir. JSON-RPC, taşıma yönteminden çok mesajların biçimini ve istek-cevap ilişkisini tanımlar.

Basitleştirilmiş bir tamamlama isteği şöyledir:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "textDocument/completion",
  "params": {
    "textDocument": { "uri": "file:///proje/app.py" },
    "position": { "line": 12, "character": 8 }
  }
}
```

Bu mesaj, belirtilen belgenin 12. satırındaki konum için öneri ister. `id` alanı sayesinde istemci, sunucudan dönen cevabı doğru istekle eşleştirir.

## Yaşam döngüsü ve yetenek pazarlığı

Bağlantı başladığında istemci `initialize` isteğini gönderir. Her iki taraf desteklediği yetenekleri açıklar. Örneğin bir sunucu otomatik tamamlama sunabilir fakat kod biçimlendirmeyi desteklemeyebilir. Bu **capability negotiation** mekanizması, istemcinin olmayan bir özelliği çağırmasını engeller.

Belge açıldığında `textDocument/didOpen`, değiştirildiğinde `textDocument/didChange`, kapatıldığında ise `textDocument/didClose` bildirimi gönderilir. Bildirimlerin normal isteklerden farkı cevap beklememeleridir. Hata ve uyarılar çoğunlukla sunucunun gönderdiği `textDocument/publishDiagnostics` bildirimiyle editörde renkli dalgalara dönüşür.

| LSP işlemi | Kullanıcıya görünen sonuç |
|---|---|
| `completion` | Kod tamamlama önerileri |
| `hover` | Sembol üzerinde bilgi kutusu |
| `definition` | Tanıma gitme |
| `references` | Kullanım yerlerini bulma |
| `rename` | Güvenli sembol yeniden adlandırma |
| `diagnostics` | Hata ve uyarı işaretleri |

## Her şey sihirli mi?

LSP yalnızca iletişimi standartlaştırır; dil sunucusunun kaliteli analiz yapacağını garanti etmez. Büyük projelerde indeksleme, bellek tüketimi ve gecikme hâlâ önemli mühendislik problemleridir. Ayrıca satır ve karakter konumlarının UTF-8 veya UTF-16 biçiminde yorumlanması gibi ayrıntılar, uyumsuzluklara yol açabilir.

Buna rağmen LSP son derece güçlü bir mimari fikirdir: Editör kullanıcı deneyimine, dil sunucusu ise programlama dilinin karmaşık kurallarına odaklanır. Sonuçta yeni bir editör geliştiren ekip yüzlerce dil motoru yazmak zorunda kalmaz; mevcut sunucularla aynı dili konuşması yeterlidir. Kısacası LSP, editörler ile diller arasındaki evrensel tercümandır.
