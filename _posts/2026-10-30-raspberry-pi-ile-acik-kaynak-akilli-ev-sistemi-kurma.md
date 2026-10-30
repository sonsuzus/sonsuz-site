---
layout: post
title: "Raspberry Pi ile Açık Kaynak Akıllı Ev Sistemi Kurma"
math: true
categories: 
  - Proje
tags: 
  - raspberry pi
  - akıllı ev
  - iot
  - mqtt
  - python
  - ev otomasyonu
toc: true
image: /img/raspberry-pi-ile-21.png
---

![raspberry-pi-ile-21](/img/raspberry-pi-ile-21.svg)


Akıllı lambalar, sıcaklık sensörleri ve uzaktan kontrol edilen prizler oldukça kullanışlıdır; fakat farklı markalara ait ürünler çoğu zaman ayrı uygulamalar, bulut üyelikleri ve kapalı protokoller kullanır. Raspberry Pi merkezli bir sistem kurarak verilerinizi evinizde tutabilir, cihazları tek panelden yönetebilir ve otomasyon kurallarını özgürce geliştirebilirsiniz. Üstelik sisteminiz internet bağlantısı kesildiğinde bile çalışmaya devam edebilir.

``

## Sistemin Temel Mantığı

Akıllı ev sistemini üç katmanlı bir yapı olarak düşünebiliriz: sensörler çevreyi gözlemler, merkezi yazılım verileri işler, eyleyiciler ise fiziksel değişiklikleri gerçekleştirir. Örneğin sıcaklık sensörü ölçüm yapar, Raspberry Pi bu değeri belirlenen eşikle karşılaştırır ve gerekirse röleyle vantilatörü çalıştırır.

Basit bir sıcaklık otomasyonu şu mantıkla ifade edilebilir:

$$
u(t)=\begin{cases}1, & T(t)>T_{eşik} \\ 0, & T(t)\leq T_{eşik}\end{cases}$$

Burada $T(t)$ ölçülen sıcaklığı, $T_{eşik}$ belirlediğimiz sınırı, $u(t)$ ise cihazın açık veya kapalı durumunu temsil eder. Sensör değerleri eşik çevresinde dalgalanıyorsa cihaz sürekli açılıp kapanabilir. Bunu önlemek için açma ve kapatma sıcaklıklarını farklı seçen **histerezis** yaklaşımı kullanılabilir.

## Açık Kaynak ve Ticari Sistem Karşılaştırması

| Özellik | Raspberry Pi sistemi | Ticari sistem |
|---|---|---|
| Veri saklama | Yerel ve kullanıcı kontrolünde | Genellikle bulutta |
| Özelleştirme | Çok yüksek | Üreticiyle sınırlı |
| İlk kurulum | Teknik bilgi gerektirir | Genellikle kolaydır |
| İnternetsiz çalışma | Yapılandırmaya bağlı olarak tam | Her üründe bulunmaz |
| Bakım | Kullanıcı sorumluluğunda | Üretici desteği mevcut |

Bu özgürlük biraz sorumluluk getirir. Güncellemeleri takip etmek, yedek almak ve elektrik güvenliğine dikkat etmek sistem sahibinin görevidir.

## Gerekli Donanım ve Yazılım

Başlangıç için Raspberry Pi 4 veya 5, güvenilir bir güç adaptörü, microSD kart ve ağ bağlantısı yeterlidir. Ortam verisi toplamak için BME280; lambaları ya da düşük voltajlı cihazları kontrol etmek için optik izolasyonlu röle modülü kullanılabilir. Şebeke gerilimiyle deneyiminiz yoksa 230 V bağlantılara doğrudan müdahale etmeyin; sertifikalı akıllı prizleri veya bir elektrik uzmanını tercih edin.

Yazılım tarafında **Home Assistant** kontrol panelini ve otomasyon motorunu sağlar. **Mosquitto MQTT** cihazlar arasında hafif mesajlaşma sunarken **Node-RED** sürükle-bırak yöntemiyle akış hazırlamayı kolaylaştırır.

MQTT yapısında sensörler bir konuya mesaj yayımlar, ilgilenen uygulamalar o konuya abone olur. Örneğin sıcaklık verisi `ev/salon/sicaklik` konusunda taşınabilir. Böylece sensör, veriyi kimin kullanacağını bilmek zorunda kalmaz.

## Python ile Sensör Verisi Yayımlamak

Önce gerekli paketleri kurun:

```bash
pip install paho-mqtt adafruit-circuitpython-bme280
```

Aşağıdaki örnek, BME280 sensöründen sıcaklığı okuyup her 30 saniyede MQTT sunucusuna gönderir:

```python
import time
import board
import adafruit_bme280
from paho.mqtt.client import Client

sensor = adafruit_bme280.Adafruit_BME280_I2C(board.I2C())
mqtt = Client()
mqtt.username_pw_set('sensor', 'guclu-parola')
mqtt.connect('192.168.1.20', 1883)

while True:
    temperature = round(sensor.temperature, 2)
    mqtt.publish('ev/salon/sicaklik', temperature, retain=True)
    print(f'Yayımlanan sıcaklık: {temperature} °C')
    time.sleep(30)
```

`retain=True`, son ölçümün MQTT sunucusunda tutulmasını sağlar. Böylece Home Assistant yeniden başladığında yeni ölçümü beklemeden mevcut değeri görebilir.

## Güvenli ve Sağlam Bir Kurulum

MQTT sunucusunu parolasız bırakmayın, Raspberry Pi için sabit IP ayırın ve sistemi düzenli olarak güncelleyin. Dışarıdan erişim gerekiyorsa doğrudan port açmak yerine WireGuard gibi bir VPN kullanın. Ayrıca microSD kart bozulmalarına karşı yapılandırma dosyalarını başka bir diske yedekleyin.

Projeyi önce tek oda ve tek sensörle başlatmak en sağlıklı yaklaşımdır. Sistem kararlı çalıştıkça hareket algılama, enerji takibi, su kaçağı uyarısı ve gün batımına bağlı aydınlatma gibi özellikler ekleyebilirsiniz. Sonuçta yalnızca uzaktan kumandalı bir ev değil, davranışlarını sizin belirlediğiniz yerel, geliştirilebilir ve gerçekten size ait bir otomasyon platformu elde edersiniz.
