---
layout: post
title: "ROS Mimarisine Giriş: Düğümler, Konular ve Servislerle Robotları Konuşturmak"
math: true
categories: 
  - Bilgi
tags: 
  - ros
  - robotik
  - python
  - ros2
  - düğümler
  - konular
  - servisler
toc: true
image: /img/ros-mimarisine-giris-40.png
---

Bir robotun kamerası görüntü üretirken motorları hareket eder, sensörleri çevreyi ölçer ve karar mekanizması bütün bu verileri yorumlar. Tüm bileşenleri tek bir dev programda toplamak mümkün olsa da bakım yapmak kısa sürede kablo yumağı çözmeye dönüşür. ROS, yani Robot Operating System, robot yazılımını küçük ve bağımsız parçalara ayırarak bu karmaşayı yönetilebilir hâle getiren bir iletişim ve araçlar ekosistemidir.
``
ROS, adına rağmen geleneksel anlamda bir işletim sistemi değildir. Linux üzerinde çalışan; mesajlaşma, paket yönetimi, donanım soyutlama, görselleştirme ve hata ayıklama olanakları sunan bir ara katmandır. Bu yazıda modern projelerde yaygın olan **ROS 2** yaklaşımını temel alacağız.

## Temel fikir: Hesaplama grafiği

ROS mimarisi, çalışan bileşenlerin ve aralarındaki bağlantıların oluşturduğu bir **hesaplama grafiği** olarak düşünülebilir. Grafikte düğümler yazılım bileşenlerini, bağlantılar ise veri akışını temsil eder:

$$G = (V, E)$$

Burada $V$ düğüm kümesi, $E$ ise düğümler arasındaki iletişim kanallarıdır. Örneğin kamera düğümünden görüntü işleme düğümüne doğru bir bağlantı bulunabilir. ROS 2, düğümlerin birbirini keşfetmesi ve haberleşmesi için çoğunlukla DDS tabanlı bir altyapı kullanır.

## Düğümler: İş yapan küçük uzmanlar

**Düğüm (node)**, belirli bir görevi yerine getiren çalışan süreç veya mantıksal bileşendir. Bir düğüm kamerayı okuyabilir, diğeri engel algılayabilir, başka biri motor komutu üretebilir. İyi tasarlanmış bir düğüm, tek bir sorumluluğa odaklanır.

Çalışan düğümleri görmek için:

```bash
ros2 node list
ros2 node info /kamera_dugumu
```

İkinci komut, ilgili düğümün yayınladığı ve dinlediği konuları, sunduğu servisleri ve diğer bağlantılarını gösterir. Böylece robotun görünmez iletişim ağı terminalde görünür olur.

## Konular: Sürekli veri akışı

**Konu (topic)**, düğümler arasında asenkron veri taşır. Yayıncı düğüm mesaj gönderir; abone düğümler mesajları alır. Yayıncı, abonelerin kim olduğunu bilmek zorunda değildir. Bu gevşek bağlı yapı, bileşenlerin kolayca değiştirilmesini sağlar.

Örneğin bir LIDAR saniyede 10 tarama yayımlıyorsa frekans $f=10\,Hz$, iki mesaj arasındaki yaklaşık süre ise:

$$T = \frac{1}{f} = 0.1\,s$$

Basit bir ROS 2 Python yayıncısı şöyle yazılabilir:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DurumYayincisi(Node):
    def __init__(self):
        super().__init__('durum_yayincisi')
        self.publisher = self.create_publisher(String, '/robot_durumu', 10)
        self.create_timer(1.0, self.durum_gonder)

    def durum_gonder(self):
        mesaj = String()
        mesaj.data = 'Robot göreve hazır!'
        self.publisher.publish(mesaj)

rclpy.init()
rclpy.spin(DurumYayincisi())
```

Kod, `/robot_durumu` konusuna saniyede bir metin mesajı yollar. `10` değeri, iletişimin QoS kuyruk derinliğini belirtir; yani geçici yoğunluklarda kaç mesajın saklanabileceğini etkiler.

## Servisler: Sor ve cevabı bekle

**Servis (service)**, istek-cevap modelini kullanır. İstemci bir talep gönderir, sunucu işlemi gerçekleştirip tek bir yanıt döndürür. “Haritayı kaydet” veya “sensörü sıfırla” gibi seyrek ve sonucu beklenen işlemler için uygundur. Sürekli kamera görüntüsü taşımak için servis kullanmak ise postacıdan canlı yayın yapmasını istemeye benzer.

```bash
ros2 service list
ros2 service call /reset_sensor std_srvs/srv/Trigger
```

Bu komutlar servisleri listeler ve örnek bir sensör sıfırlama isteği gönderir.

| Özellik | Konu | Servis |
|---|---|---|
| İletişim modeli | Yayıncı-abone | İstek-cevap |
| Zamanlama | Asenkron | Genellikle senkron |
| Alıcı sayısı | Sıfır veya çok | Belirli sunucu |
| Uygun kullanım | Sensör, hız, görüntü | Sıfırlama, sorgulama |
| Sürekli veri | Çok uygun | Uygun değil |

## Hangisini ne zaman seçmeli?

Veri düzenli akıyor ve birden fazla bileşen tarafından tüketilebiliyorsa **konu** seçilir. İşlem belirli bir komutla başlayacak ve kısa sürede cevap verecekse **servis** daha uygundur. Uzun süren, geri bildirim ve iptal gerektiren navigasyon görevlerinde ise ROS 2’nin **action** yapısı tercih edilir.

Özetle düğümler robotun uzman çalışanları, konular ortak anons sistemi, servisler ise danışma masasıdır. Bu ayrımı doğru kurmak; ölçeklenebilir, test edilebilir ve parçaları yeniden kullanılabilir robot yazılımlarının temelini oluşturur.

![ros-mimarisine-giris-40](/img/ros-mimarisine-giris-40.svg)

