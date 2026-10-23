---
layout: post
title: "MMORPG Sunucu Mimarisi: Binlerce Oyuncu Tek Dünyada Nasıl Buluşuyor?"
math: true
categories: 
  - Bilgi
tags: 
  - mmorpg
  - sunucu-mimarisi
  - dağıtık-sistemler
  - oyun-programlama
  - ağ-programlama
  - ölçeklenebilirlik
toc: true
image: /img/mmorpg-sunucu-mimarisi-78.png
---

Bir MMORPG dünyasına bağlanıp kalabalık bir şehre girdiğinizde yüzlerce oyuncuyu koşarken, ticaret yaparken ve devasa yaratıklarla savaşırken görebilirsiniz. Ekrandaki bu canlılığın arkasında ise tek bir süper bilgisayar değil; görevleri paylaşan, birbirleriyle sürekli haberleşen ve arızalara karşı hazırlıklı çalışan dağıtık sunucular bulunur.

![mmorpg-sunucu-mimarisi-78](/img/mmorpg-sunucu-mimarisi-78.svg)

``
## Tek Sunucu Neden Yetmez?

Her oyuncu hareket, yetenek kullanımı, envanter yönetimi ve sohbet gibi olaylar üretir. Oyuncu başına saniyede ortalama $r$ mesaj, eşzamanlı oyuncu sayısı da $N$ ise sistemin karşılaması gereken yaklaşık mesaj yükü şöyledir:

$$M = N \times r$$

Örneğin 10.000 oyuncunun saniyede 15 mesaj ürettiği bir dünyada sunucular saniyede yaklaşık 150.000 mesajı işlemelidir. Üstelik bazı hareketler çevredeki diğer oyunculara da gönderilir. Her veriyi herkese yayınlamak maliyeti hızla $O(N^2)$ seviyesine taşıyabileceğinden MMORPG mimarileri dünyayı mantıksal parçalara ayırır.

## Sunucu Katmanları

Oyuncu genellikle doğrudan oyun dünyasının merkezine bağlanmaz. İstek, uzmanlaşmış servislerden oluşan bir yolculuk yapar.

| Bileşen | Temel görev | Örnek veri |
|---|---|---|
| Gateway | Bağlantıyı kabul eder ve yönlendirir | Oturum, paket, IP |
| Kimlik servisi | Hesabı doğrular | Token, karakter listesi |
| World server | Dünya kurallarını yönetir | Saat, hava, global etkinlik |
| Zone server | Belirli bir bölgeyi simüle eder | Oyuncu, NPC, savaş |
| Veritabanı | Kalıcı veriyi saklar | Envanter, görev, ekonomi |
| Chat servisi | Mesajlaşmayı yönetir | Kanal ve özel mesaj |

Bu ayrım sayesinde sohbet sistemindeki yoğunluk savaş hesaplamalarını durdurmaz. Ayrıca her servis bağımsız biçimde ölçeklenebilir.

## Shard, Zone ve Instance Farkı

**Shard**, aynı oyunun ayrı bir kopyasıdır; oyuncular bunu genellikle “sunucu seçimi” olarak görür. **Zone**, tek dünyanın coğrafi bölümlere ayrılmasıdır. **Instance** ise zindan gibi belirli bir grup için geçici oluşturulan özel alandır.

| Yöntem | Avantaj | Dezavantaj |
|---|---|---|
| Shard | Güçlü izolasyon | Oyuncu topluluğunu böler |
| Zone | Kesintisiz dünya hissi | Sınır geçişleri karmaşıktır |
| Instance | Talebe göre kolay ölçeklenir | Ortak dünya hissini azaltabilir |

Bir karakter bölge sınırını geçtiğinde eski zone sunucusu karakter durumunu yeni sunucuya aktarır. Bu **handoff** işlemi sırasında iki sunucunun kısa süreli koordinasyon kurması gerekir; aksi hâlde karakter kopyalanabilir veya kaybolabilir.

## Interest Management: Herkesi Herkese Gösterme

Bir oyuncunun kıtanın diğer ucundaki hareketleri bilmesine gerek yoktur. Sunucu, dünyayı hücrelere böler ve yalnızca görüş alanındaki nesneleri gönderir. Görüş yarıçapı $d$ olan bir oyuncu için ilgi alanı kabaca $A = \pi d^2$ olur.

Basitleştirilmiş bir yayın mantığı şöyle yazılabilir:

```python
def broadcast_movement(player, spatial_grid):
    nearby = spatial_grid.query(player.position, radius=80)

    for entity in nearby:
        if entity.id != player.id:
            entity.connection.send({
                "type": "movement",
                "player_id": player.id,
                "position": player.position
            })
```

Bu kod, hareket paketini yalnızca yakındaki varlıklara göndererek bant genişliği ve işlemci tüketimini azaltır. Gerçek sistemlerde grid, quadtree veya spatial hashing kullanılabilir.

## Sunucu Otoritesi ve Tutarlılık

İstemciye tamamen güvenilirse oyuncu “Ben ışınlandım ve boss'u tek vuruşta yendim” diyebilir. Bu nedenle çoğu MMORPG **server-authoritative** çalışır: İstemci niyeti bildirir, sonucu sunucu hesaplar. İstemci gecikmeyi gizlemek için tahmin yapabilir; ancak son söz sunucudadır.

Tüm veriler aynı tutarlılık seviyesine ihtiyaç duymaz. Hasar ve eşya transferi güçlü tutarlılık isterken oyuncunun birkaç santimetrelik konumu eventual consistency ile yönetilebilir. Kritik ekonomi işlemlerinde idempotency anahtarları ve veritabanı transaction'ları, aynı satın alma paketinin iki kez işlenmesini önler.

## Gecikme, Tick ve Dayanıklılık

Zone sunucuları dünyayı belirli aralıklarla günceller. Tick hızı $f$ ise bir tick süresi yaklaşık $T = 1/f$ saniyedir. 20 Hz çalışan bir sistem dünyayı her 50 milisaniyede bir hesaplar.

Sunucu çökmesine karşı karakter durumu periyodik kaydedilir; kritik olaylar mesaj kuyruğuna veya event log'a yazılır. Load balancer yeni bağlantıları sağlıklı sunuculara gönderirken izleme araçları CPU, gecikme ve paket kaybını takip eder. Sonuçta kesintisiz görünen fantastik dünya; bölümlendirme, ilgi alanı filtreleme, otoriter simülasyon ve dikkatli veri yönetiminin birlikte yaptığı oldukça gerçek bir mühendislik büyüsüdür.
