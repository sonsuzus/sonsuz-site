---
layout: post
title: "Akıllı Evin Ortak Dili: Zigbee, Z-Wave ve Matter Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı ev
  - zigbee
  - z-wave
  - matter
  - thread
  - iot
toc: true
image: /img/akilli-evin-ortak-54.png
---

Bir hareket sensörü lambaya “Biri geldi!” derken, termostat kombiden yardım ister. Peki farklı markaların cihazları aynı evde birbirini nasıl anlar? Akıllı ev protokolleri, bu dijital apartmanın haberleşme kurallarını belirler. Zigbee, Z-Wave ve Matter ise benzer ihtiyaçları farklı katmanlarda çözer. Doğru seçim, yalnızca kutudaki logoya bakmaktan biraz daha fazlasını gerektirir.

``

## Önce katmanları ayıralım

Haberleşmenin iki temel sorusu vardır: “Veriyi nasıl taşıyoruz?” ve “Taşınan veri ne anlama geliyor?” Radyo teknolojisi ilk soruya, uygulama protokolü ikinci soruya yanıt verir. Ortak frekans kullanmak, ortak dili konuşmak anlamına gelmez; cihazların komutları, güvenlik kurallarını ve katılım süreçlerini de anlaması gerekir.

Zigbee ve Z-Wave kendi ağ ve uygulama yapılarını sunar. Matter ise IP üzerinde çalışan bir uygulama standardıdır; veriyi Thread, Wi-Fi veya Ethernet taşıyabilir. Bluetooth LE genellikle ilk kurulumda yardımcı olur, normal Matter haberleşmesinin taşıyıcısı değildir.

Örgü, yani *mesh* ağlarda mesajlar ara cihazlardan geçebilir. Her atlamanın bağımsız başarı olasılığı $p$ ise, $h$ atlamalı basitleştirilmiş bir yol için $P = p^h$ olur. Örneğin $0.99^3 = 0.970299$. Bu, yeniden denemeleri dışlayan öğretici bir modeldir; gerçek performansı yerleşim, parazit ve alternatif yollar belirler.

| Özellik | Zigbee | Z-Wave | Matter |
|---|---|---|---|
| Temel yaklaşım | IP dışı cihaz ağı | IP dışı cihaz ağı | IP tabanlı uygulama standardı |
| Taşıma | Genellikle 2,4 GHz | Bölgesel sub-GHz bantları | Thread, Wi-Fi, Ethernet |
| Ağ düzeni | Mesh | Klasik ağlarda mesh | Taşıyıcıya bağlı |
| Temel altyapı | Koordinatör | Denetleyici | Matter denetleyicisi |
| Güçlü taraf | Geniş ürün seçeneği | Bölgesel, düşük frekanslı haberleşme | Ekosistemler arası ortak dil |

## Zigbee: Kalabalık ve ekonomik mahalle

Zigbee, sensörlerden ampullere uzanan geniş ürün çeşitliliğiyle dikkat çeker. Koordinatör ağı oluşturur; yönlendirici cihazlar mesajları aktarır. Pilli uç cihazlar çoğunlukla uyuyarak enerji tasarrufu yapar ve başkalarının mesajlarını taşımaz. Şebekeden beslenen her cihazın yönlendirici olduğunu varsaymamak gerekir.

Dezavantajı, yaygın kullanılan 2,4 GHz bandını Wi-Fi ile paylaşmasıdır. Kanal planlaması önemlidir. Ayrıca “Zigbee destekli” etiketi, her cihazın her merkezde bütün özellikleriyle çalışacağını garanti etmez. Satın almadan önce merkezin uyumluluk listesini kontrol edin.

## Z-Wave: Daha sakin frekansların komşusu

Z-Wave, bölgeye göre değişen sub-GHz frekanslarını kullanır. Avrupa ürünlerinde sıklıkla 868 MHz çevresi görülür; ABD ürünleri farklı bantlardadır. Bu yüzden yurt dışından alınan cihazın yerel denetleyiciyle ve mevzuatla uyumunu kontrol etmek şarttır.

Düşük frekans, benzer koşullarda yayılım açısından avantaj sağlayabilir; ancak beton duvarları sihirli biçimde ortadan kaldırmaz. Sertifikasyon birlikte çalışabilirliği destekler, yine de denetleyicinin özellik desteği önemlidir. Ayrıca Z-Wave Long Range, klasik mesh yaklaşımından farklı olarak yıldız topolojisi kullanır.

## Matter: Ortak sözlük, farklı yollar

Matter’ın büyük vaadi, markalar arasındaki uygulama dilini standartlaştırmaktır. Desteklenen cihazlar Multi-Admin özelliğiyle birden fazla ekosisteme eklenebilir. Ancak uygulamaların sunduğu özellikler, cihaz türü desteği ve Matter sürümleri hâlâ kontrol edilmelidir.

Thread kullanan Matter cihazları, evin diğer IP ağlarına ulaşmak için bir Thread sınır yönlendiricisinden yararlanır. Matter denetleyicisi ise cihazın kurulumu ve yönetimiyle ilgilenir. Bu roller aynı üründe bulunabilir ama aynı şey değildir.

Eski Zigbee veya Z-Wave cihazları kendiliğinden Matter cihazına dönüşmez. Uyumlu bir köprü, yalnızca desteklediği cihaz türlerini ve özelliklerini Matter tarafına sunabilir.

## Yazılım tarafında ortak komut modeli

Bir otomasyon uygulaması, cihazın protokolünü her iş kuralına taşımak yerine adaptör seçimini merkezileştirebilir. Aşağıdaki Python örneği gerçek radyo iletişimi yapmaz; komutun hangi entegrasyona yönlendirileceğini planlar:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Device:
    name: str
    protocol: str
    online: bool

ADAPTERS = {
    'zigbee': 'zigbee_gateway',
    'z-wave': 'zwave_controller',
    'matter': 'matter_controller',
}

def plan_command(device: Device, enabled: bool) -> dict:
    if not device.online:
        raise ConnectionError('Cihaz çevrimdışı')
    if device.protocol not in ADAPTERS:
        raise ValueError('Desteklenmeyen protokol')
    return {
        'adapter': ADAPTERS[device.protocol],
        'device': device.name,
        'action': 'set_power',
        'value': enabled,
    }

lamp = Device('salon_lambası', 'matter', True)
print(plan_command(lamp, True))
```

Gerçek adaptör, ortak `set_power` isteğini cihazın desteklediği komuta çevirir. Kimlik doğrulama, zaman aşımı, yeniden deneme ve durum doğrulaması ayrıca uygulanmalıdır. Böylece otomasyon mantığı, haberleşme ayrıntılarından bağımsız kalır.

## Hangisini seçmeli?

Uygun fiyatlı sensör çeşitliliğinde Zigbee, bölgesel frekans avantajında Z-Wave, ekosistemler arası kullanımda Matter güçlü adaylardır. Yeni kurulumda yalnızca protokolü değil, gereken denetleyiciyi, çevrimdışı çalışma davranışını ve güncelleme politikasını da değerlendirin. Güvenli eşleştirme kullanın, yazılımı güncel tutun ve otomasyonlarınızı internet kesildiğinde sınayın. En akıllı ev, internet gidince ev olmayı unutmayan evdir.

![akilli-evin-ortak-54](/img/akilli-evin-ortak-54.svg)

