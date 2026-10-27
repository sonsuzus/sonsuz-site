---
layout: post
title: "Akıllı Evin Beyni İçeride: Ev Otomasyonunda Yerel İşleme"
math: true
categories: 
  - Bilgi
tags: 
  - edge computing
  - ev otomasyonu
  - iot
  - yerel işleme
  - mahremiyet
  - home assistant
toc: true
image: /img/akilli-evin-beyni-38.png
---

Akıllı ampuller, hareket sensörleri, kameralar ve termostatlar her gün çok sayıda veri üretir. Bu verilerin tamamını uzak sunuculara göndermek yerine evdeki bir merkez üzerinde işlemek, otomasyonları hızlandırırken internet bağımlılığını ve mahremiyet risklerini azaltır. İşte edge computing, yani uçta veya yerelde işleme yaklaşımı tam olarak bunu sağlar.
``

## Yerel işleme nedir?

Klasik bulut mimarisinde sensörden alınan veri internete çıkar, sağlayıcının sunucusunda değerlendirilir ve sonuç tekrar eve gönderilir. Yerel mimaride ise karar; Home Assistant çalıştıran bir mini bilgisayar, Raspberry Pi, NAS ya da özel bir otomasyon merkezi tarafından evin içinde verilir.

Örneğin koridordaki hareket sensörü etkinleştiğinde ışığın açılması için bulut sunucusundan cevap beklemek gerekmez. Merkez, sensör olayını yerel ağ üzerinden alır ve lambaya anında komut yollar.

Toplam tepki süresini basitçe şöyle düşünebiliriz:

$$T = T_{iletim} + T_{isleme} + T_{cevap}$$

Bulut tabanlı sistemde internet yolculuğu nedeniyle $T_{iletim}$ ve $T_{cevap}$ büyür. Yerel işlemede veri yalnızca ev ağı içinde dolaştığından toplam gecikme çoğu zaman belirgin biçimde azalır.

## Bulut ve edge computing karşılaştırması

| Özellik | Bulut tabanlı işleme | Yerel işleme |
|---|---|---|
| İnternet gereksinimi | Genellikle zorunlu | Çoğu otomasyonda gereksiz |
| Tepki süresi | Ağ durumuna bağlı | Genellikle çok düşük |
| Mahremiyet | Veri dış sunucuya gider | Veri evde kalabilir |
| Kurulum kolaylığı | Çoğunlukla daha kolay | Teknik bilgi gerektirebilir |
| Bakım | Sağlayıcı tarafından yapılır | Kullanıcı sorumluluğundadır |
| Ölçeklenebilirlik | Yüksek sunucu kapasitesi | Donanım kapasitesiyle sınırlı |

Yerel yaklaşım her durumda bulutu çöpe atmak anlamına gelmez. Hava durumu tahmini veya ev dışından bildirim gönderme gibi hizmetlerde bulut yararlıdır. En dengeli çözüm, kritik kararları evde verip yalnızca gerekli verileri dış servislere aktaran hibrit mimaridir.

## Bir otomasyon nasıl çalışır?

Yerel merkezler genellikle olay güdümlü bir model kullanır. Sensör bir olay üretir, sistem koşulları denetler ve uygun eylemi gerçekleştirir:

1. Hareket sensörü `aktif` durumuna geçer.
2. Merkez saatin gece olup olmadığını kontrol eder.
3. Işık seviyesi belirlenen eşikten düşükse lambayı açar.
4. Hareket kesildikten sonra zamanlayıcı başlatır.
5. Süre dolunca lambayı kapatır.

Aşağıdaki Home Assistant otomasyonu bu mantığın sade bir örneğidir:

```yaml
alias: Gece koridor ışığı
trigger:
  - platform: state
    entity_id: binary_sensor.koridor_hareket
    to: "on"
condition:
  - condition: numeric_state
    entity_id: sensor.koridor_aydinlik
    below: 30
action:
  - service: light.turn_on
    target:
      entity_id: light.koridor
  - delay: "00:02:00"
  - service: light.turn_off
    target:
      entity_id: light.koridor
```

Bu kod, hareket algılandığında ortam aydınlığı 30 lüksün altındaysa ışığı açar ve iki dakika sonra kapatır. Sensörler ile merkez aynı yerel ağdaysa işlem internet kesildiğinde de devam edebilir.

## Mahremiyet ve kaynak kullanımı

Kameralar yerel işlemenin değerini daha görünür hâle getirir. Görüntüyü buluta göndermek yerine cihaz üzerinde insan algılama modeli çalıştırılabilir. Böylece dışarıya video yerine yalnızca `insan algılandı` olayı çıkar.

Yerel donanım seçerken işlemci gücü, bellek ve enerji tüketimi birlikte değerlendirilmelidir. Verimlilik kabaca şu oranla yorumlanabilir:

$$E = \frac{islenen\ olay\ sayisi}{enerji\ tuketimi}$$

Basit sensör otomasyonları için düşük güçlü bir Raspberry Pi yeterli olabilir. Birden fazla kamera üzerinde yapay zekâ çalıştırılacaksa mini PC veya donanım hızlandırıcısı gerekebilir.

## Sonuç

Edge computing, akıllı evi yalnızca daha hızlı değil, aynı zamanda daha dayanıklı ve mahremiyet dostu hâle getirir. En iyi başlangıç yöntemi; ışık, sıcaklık ve hareket gibi basit otomasyonları yerelleştirmek, ardından kamera analizi gibi ağır işlemlere geçmektir. Böylece internet gittiğinde akıllı eviniz bir anda oldukça pahalı bir sıradan eve dönüşmez!

![akilli-evin-beyni-38](/img/akilli-evin-beyni-38.svg)

