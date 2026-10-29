---
layout: post
title: "IoT Sensör Ağlarıyla Akıllı Sera Otomasyonu"
math: true
categories: 
  - Proje
tags: 
  - iot
  - sera otomasyonu
  - sensör ağları
  - python
  - mqtt
  - kontrol algoritmaları
toc: true
image: /img/iot-sensor-aglariyla-52.png
---

Bir serayı sağlıklı tutmak, yalnızca bitkileri sulamaktan ibaret değildir. Sıcaklık yükseldiğinde havalandırmayı açmak, nem azaldığında sulamayı başlatmak ve gün ışığı yetersiz kaldığında yetiştirme lambalarını devreye almak gerekir. IoT sensör ağları sayesinde bu kararlar sürekli ölçüm yapan, verileri paylaşan ve çevresel koşulları otomatik olarak dengeleyen akıllı bir sistem tarafından alınabilir.

``

## Sistemin Temel Mimarisi

Akıllı sera sistemi üç katmandan oluşur. Sensör katmanında sıcaklık ve hava nemi için DHT22, toprak nemi için kapasitif sensör, ışık seviyesi için BH1750 kullanılabilir. Kontrol katmanındaki ESP32 veya Raspberry Pi verileri işler. Eyleyici katmanında ise fan, sulama pompası, sisleme sistemi, ısıtıcı ve LED lambalar bulunur.

Sensör düğümleri MQTT gibi hafif bir mesajlaşma protokolüyle merkezi denetleyiciye veri gönderir. Örneğin `sera/sicaklik` konusu sıcaklık ölçümlerini, `sera/toprak_nemi` konusu ise sulama kararında kullanılacak değerleri taşıyabilir.

| Değişken | Sensör | Hedef aralık | Kontrol edilen cihaz |
|---|---|---:|---|
| Sıcaklık | DHT22 | 20–28 °C | Fan ve ısıtıcı |
| Hava nemi | DHT22 | %60–80 | Sisleyici ve fan |
| Toprak nemi | Kapasitif sensör | %40–70 | Su pompası |
| Işık | BH1750 | 10.000–25.000 lux | LED yetiştirme lambası |

## Kontrol Mantığının Teorisi

En basit yöntem eşik tabanlı kontroldür. Ölçülen değer $x$, alt sınır $L$ ve üst sınır $U$ ile karşılaştırılır:

$$
u(x)=
\begin{cases}
1, & x < L \\
0, & x > U
\end{cases}
$$

Buradaki $u$, cihazın açık veya kapalı olmasını temsil eder. Ancak tek bir eşik kullanılırsa ölçüm sınır çevresinde dalgalandığında röle sürekli açılıp kapanabilir. Bunu önlemek için histerezis uygulanır. Örneğin pompa, toprak nemi %40’ın altına düşünce açılır; %55’e ulaşınca kapanır.

Daha hassas sıcaklık kontrolünde PID algoritması kullanılabilir:

$$u(t)=K_p e(t)+K_i\int e(t)dt+K_d\frac{de(t)}{dt}$$

Burada $e(t)$, hedef sıcaklık ile ölçülen sıcaklık arasındaki farktır. Oransal bileşen mevcut hataya, integral bileşen birikmiş hataya, türev bileşeni ise değişim hızına tepki verir.

| Yöntem | Avantaj | Dezavantaj | Uygun kullanım |
|---|---|---|---|
| Eşik kontrolü | Basit ve hızlıdır | Dalgalanma oluşturabilir | Sulama ve aydınlatma |
| Histerezis | Röle ömrünü uzatır | Çok hassas değildir | Pompa ve fan kontrolü |
| PID | Kararlı ve hassastır | Ayarlama gerektirir | Isıtma ve havalandırma |

## Örnek Kontrol Algoritması

Aşağıdaki Python kodu, sensör verilerine göre fanı, pompayı ve lambayı yönetir. Gerçek projede değişkenler MQTT mesajlarından veya sensör sürücülerinden alınabilir.

```python
sicaklik = 30.2
toprak_nemi = 37
isik = 7200

pompa_acik = False

if sicaklik > 28:
    fan = True
elif sicaklik < 24:
    fan = False

# Histerezisli sulama kontrolü
if toprak_nemi < 40:
    pompa_acik = True
elif toprak_nemi > 55:
    pompa_acik = False

# Yetersiz doğal ışıkta destek aydınlatması
lamba = isik < 10000

print({'fan': fan, 'pompa': pompa_acik, 'lamba': lamba})
```

Kodun belirli aralıklarla çalıştırılması yerine olay tabanlı MQTT mesajlarıyla tetiklenmesi ağ trafiğini ve enerji tüketimini azaltabilir. Kablosuz sensörler pille çalışıyorsa ölçümlerin her saniye değil, örneğin her 30 saniyede bir gönderilmesi daha mantıklıdır.

## Daha Güvenilir Bir Sera İçin

Otomasyon sistemi yalnızca anlık ölçümlere güvenmemelidir. Hareketli ortalama kullanılarak gürültü azaltılabilir:

$$\bar{x}_n=\frac{1}{N}\sum_{i=0}^{N-1}x_{n-i}$$

Ayrıca sensör kopması, aşırı sıcaklık veya uzun süre çalışan pompa için güvenlik kuralları tanımlanmalıdır. Verilerin InfluxDB gibi zaman serisi veritabanında saklanması, Grafana üzerinden izlenmesi ve kritik durumlarda telefona bildirim gönderilmesi sistemi tamamlar. Böylece sera, bitkilerin ihtiyaçlarını tahmin eden küçük ama çalışkan bir dijital bahçıvana dönüşür.

![iot-sensor-aglariyla-52](/img/iot-sensor-aglariyla-52.svg)

