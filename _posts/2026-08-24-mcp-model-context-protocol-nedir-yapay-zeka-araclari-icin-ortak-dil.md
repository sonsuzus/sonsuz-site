---
layout: post
title: "MCP (Model Context Protocol) Nedir? Yapay Zekâ Araçları İçin Ortak Dil"
math: true
categories: 
  - Bilgi
tags: 
  - MCP
  - Yapay Zekâ
  - LLM
  - API
  - Model Context Protocol
---

Büyük dil modelleri metin üretmekte çok başarılıdır; ancak tek başlarına takviminize bakamaz, veritabanınızdan müşteri kaydı çekemez veya GitHub’daki bir depoyu analiz edemezler. Bu noktada **MCP (Model Context Protocol)**, yapay zekâ uygulamalarının harici araçlar ve veri kaynaklarıyla güvenli, düzenli ve standart bir biçimde konuşmasını sağlayan açık bir protokol olarak devreye girer.
``
Bir LLM’i çok yetenekli ama dış dünyaya kapalı bir uzman gibi düşünebilirsiniz. Ona güncel bir satış raporu sorarsanız, rapor dosyasına erişmediği sürece yalnızca tahmin yürütür. MCP ise modele “hangi araçlar var?”, “bu aracı nasıl çağırırım?” ve “gelen sonucu nasıl yorumlarım?” sorularının ortak cevabını verir. Böylece her entegrasyon için sıfırdan özel bağlantı kodu yazma ihtiyacı azalır.

## MCP’nin temel mantığı

MCP mimarisi çoğunlukla üç oyuncudan oluşur: **host**, **client** ve **server**. Host, kullanıcıyla etkileşen yapay zekâ uygulamasıdır; örneğin bir masaüstü asistanı veya kod editörü. Client, host içinde MCP sunucusuyla iletişimi yöneten bileşendir. Server ise dosya sistemi, PostgreSQL, Slack veya özel şirket API’leri gibi kaynaklara erişim sağlayan taraftır.

İletişim, genellikle JSON-RPC mesajları üzerinden gerçekleşir. Sunucu; kullanılabilir araçlarını, kaynaklarını ve istemlerini tanımlar. Model bir görevi çözmek için araca ihtiyaç duyduğunda host, uygun MCP çağrısını yapar ve sonucu modele bağlam olarak geri verir.

Bu akışı basitçe şöyle ifade edebiliriz:

$$Yanıt = LLM(Sistem\ Bağlamı + Kullanıcı\ İsteği + Araç\ Sonucu)$$

Buradaki kritik nokta, modelin doğrudan veritabanına bağlanmamasıdır. Model araç seçimi yapabilir; fakat yetkili MCP sunucusu işlemi yürütür. Bu ayrım, hem mimariyi temizler hem de güvenlik sınırlarını belirginleştirir.

| Kavram | Görevi | Örnek |
|---|---|---|
| Host | Kullanıcı deneyimini ve modeli yönetir | Kod editörü asistanı |
| MCP Client | Protokol mesajlarını iletir | Host içindeki bağlantı katmanı |
| MCP Server | Araç ve veri erişimini sunar | GitHub veya PostgreSQL sunucusu |
| Tool | İşlem yapan fonksiyon | `issue_olustur` |
| Resource | Okunabilir bağlam verisi | Proje dokümantasyonu |

## Neden klasik API entegrasyonundan farklı?

Klasik yaklaşımda her yapay zekâ uygulaması, her servis için ayrı SDK, kimlik doğrulama akışı ve araç şeması geliştirmek zorunda kalabilir. MCP, bunu “USB-C mantığına” yaklaştırır: Her cihaz aynı şeyi yapmaz, fakat ortak bir bağlantı standardını konuşur.

| Özellik | Özel API Entegrasyonu | MCP Yaklaşımı |
|---|---|---|
| Araç keşfi | Kod içinde sabit tanım gerekir | Sunucu araçları dinamik bildirebilir |
| Tekrar kullanım | Uygulamaya bağımlıdır | Farklı MCP uyumlu host’larda kullanılabilir |
| Bağlam paylaşımı | Genellikle özel tasarlanır | Resource ve prompt yapıları standarttır |
| Güvenlik denetimi | Her projede yeniden ele alınır | Yetki sınırları sunucu katmanında yönetilebilir |

Örneğin bir “proje durumu” asistanı, önce GitHub MCP sunucusundan açık işleri alabilir, ardından takvim sunucusundan yaklaşan teslim tarihlerini okuyabilir. Model bu sonuçları birleştirerek anlamlı bir özet oluşturur. Bu işlemde modelin araç çağırması ile gerçek işlemin yürütülmesi birbirinden ayrıdır.

## Küçük bir araç örneği

Aşağıdaki TypeScript benzeri örnek, bir MCP sunucusunun model için araç tanımlama fikrini gösterir:

```ts
server.tool(
  "hava_durumu_getir",
  {
    city: z.string().describe("Hava durumu istenecek şehir")
  },
  async ({ city }) => {
    const weather = await weatherApi.current(city);

    return {
      content: [{
        type: "text",
        text: `${city}: ${weather.temp}°C, ${weather.summary}`
      }]
    };
  }
);
```

Bu araç tanımı, modele fonksiyonun adını, beklediği parametreyi ve sonucunun metinsel içeriğini bildirir. Model “Ankara’da hava nasıl?” isteğini görünce uygun aracı seçebilir. Ancak önemli bir güvenlik kuralı vardır: Araçların yalnızca gerekli yetkilere sahip olması gerekir. Örneğin dosya silen bir araç, kullanıcı onayı olmadan çalıştırılmamalıdır.

MCP’nin değeri yalnızca teknik kolaylık değildir. Araçları standartlaştırarak yapay zekâ sistemlerini daha taşınabilir, denetlenebilir ve genişletilebilir hâle getirir. Kısacası MCP, LLM’lerin dış dünyayla konuşurken kullandığı ortak sözleşmedir; doğru tasarlandığında “sohbet eden model”i gerçek iş akışlarına katkı sağlayan bir asistana dönüştürür.
