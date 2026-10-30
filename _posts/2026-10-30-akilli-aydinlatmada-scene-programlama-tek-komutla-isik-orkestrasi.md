---
layout: post
title: "Akıllı Aydınlatmada Scene Programlama: Tek Komutla Işık Orkestrası"
math: true
categories: 
  - Program
tags: 
  - akıllı aydınlatma
  - scene programlama
  - iot
  - otomasyon
  - mqtt
  - home assistant
toc: true
image: /img/akilli-aydinlatmada-scene-22.png
---

![akilli-aydinlatmada-scene-22](/img/akilli-aydinlatmada-scene-22.svg)


Bir odadaki beş farklı lambayı film izlemeye uygun hâle getirmek için her birini ayrı ayrı ayarladığınızı düşünün: tavan ışığını kıs, lambaderi mora çevir, LED şeridi yak… Akıllı aydınlatma sistemlerindeki **scene**, yani sahne yaklaşımı, bu küçük kumanda maratonunu tek komuta indirir. “Sinema” sahnesini çağırdığınızda bütün ışıklar önceden belirlenen renk, parlaklık ve geçiş sürelerine senkronize biçimde ulaşır.

``

## Scene tam olarak nedir?

Scene, bir veya daha fazla cihazın hedef durumlarını saklayan mantıksal bir anlık görüntüdür. Bir sahne çalıştırıldığında sistem ilgili cihazlara `açık/kapalı`, parlaklık, renk sıcaklığı veya RGB değeri gibi komutlar gönderir.

Bir ışığın basitleştirilmiş durumu şöyle gösterilebilir:

$$L_i = (p_i, b_i, r_i, g_i, b_i', t_i)$$

Burada $p_i$ güç durumunu, $b_i$ parlaklığı, $(r_i,g_i,b_i')$ renk bileşenlerini, $t_i$ ise geçiş süresini temsil eder. Bir sahne de $n$ adet ışığın durum kümesidir:

$$S = \{L_1, L_2, \ldots, L_n\}$$

Yani scene komutu sihir değil; önceden tanımlanmış durumların topluca uygulanmasıdır. Yine de salon bir anda bilim kurgu filmine dönüşünce biraz sihirli görünebilir.

| Yaklaşım | Komut sayısı | Tutarlılık | Kullanım örneği |
|---|---:|---|---|
| Tekil kontrol | Her ışık için ayrı | Kullanıcıya bağlı | Okuma lambasını açmak |
| Scene | Genellikle tek | Yüksek | Sinema veya yemek modu |
| Otomasyon | Koşula bağlı | Kurallara bağlı | Gün batınca sahneyi çağırmak |

## Senkronizasyon nasıl sağlanır?

Merkezî sistem önce sahne tanımını okur, ardından komutları ağ üzerinden ampullere veya köprüye iletir. Zigbee gibi ağlarda grup adresleme kullanılıyorsa tek yayın mesajı aynı gruptaki cihazlara ulaşabilir. Wi-Fi tabanlı sistemlerde ise komutlar çoğunlukla ayrı ayrı gönderilir.

Gerçek dünyada “aynı anda” ifadesi yaklaşık bir hedeftir. Cihaz $i$ için toplam gecikme şöyle modellenebilir:

$$T_i = T_{işleme} + T_{ağ} + T_{cihaz}$$

Işıklar arasındaki fark $\Delta T = \max(T_i)-\min(T_i)$ küçüldükçe geçiş daha senkron görünür. Grup mesajları, yerel ağ kullanımı ve ortak geçiş süresi bu farkı azaltır. Bulut üzerinden çalışan çözümlerde internet gecikmesi, orkestraya geç kalan bir trompetçi ekleyebilir.

## Home Assistant ile örnek sahne

Aşağıdaki YAML tanımı, üç ışığın hedef özelliklerini saklar. `transition` alanı değişimin iki saniyede yumuşak biçimde yapılmasını sağlar.

```yaml
scene:
  - name: Sinema Modu
    entities:
      light.tavan:
        state: "off"
      light.lambader:
        state: "on"
        brightness: 65
        rgb_color: [90, 30, 140]
        transition: 2
      light.tv_seridi:
        state: "on"
        brightness: 110
        color_temp_kelvin: 3000
        transition: 2
```

Sahneyi bir otomasyondan, panelden veya sesli asistandan çağırabiliriz:

```yaml
service: scene.turn_on
target:
  entity_id: scene.sinema_modu
data:
  transition: 2
```

İlk blok **hangi durumun oluşturulacağını**, ikinci blok ise **bu durumun ne zaman uygulanacağını** ifade eder. Bu ayrım önemlidir: Scene durum tarif eder; otomasyon ise tetikleyici ve koşullarla karar verir.

## MQTT ile kendi denetleyicini yazmak

Özel bir IoT projesinde sahne, JSON olarak MQTT konusuna yayınlanabilir:

```python
import json
import paho.mqtt.publish as publish

scene = {
    "group": "salon",
    "brightness": 35,
    "color": {"r": 80, "g": 20, "b": 130},
    "transition_ms": 2000
}

publish.single(
    "home/lights/scene",
    payload=json.dumps(scene),
    hostname="192.168.1.20"
)
```

Bu kod sahne verisini tek mesaj hâlinde yayımlar. Abone olan denetleyici mesajı ayrıştırıp ilgili ışıklara uygular. Üretim ortamında kimlik doğrulama, TLS, hata kontrolü ve çevrimdışı cihaz yönetimi de eklenmelidir.

## Sağlam sahneler için ipuçları

- Cihazları işlevlerine göre gruplandırın.
- Bulut yerine mümkünse yerel kontrol kullanın.
- Tüm ışıklara ortak geçiş süresi verin.
- Erişilemeyen cihazlarda işlemi tamamen durdurmak yerine kalanları çalıştırın.
- Sahnenin mevcut ayarları mı kaydedeceğine, sabit değerler mi kullanacağına karar verin.

İyi tasarlanmış bir scene sistemi, karmaşık cihaz ayrıntılarını kullanıcıdan saklar. Kullanıcı yalnızca “Çalışma”, “Parti” veya “Uyku” der; arka plandaki yazılım ise ışık orkestrasının şefliğini üstlenir.
