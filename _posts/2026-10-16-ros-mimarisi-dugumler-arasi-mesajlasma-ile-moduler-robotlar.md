---
layout: post
title: "ROS Mimarisi: Düğümler Arası Mesajlaşma ile Modüler Robotlar"
math: true
categories: 
  - Bilgi
tags: 
  - ros
  - robotik
  - düğümler
  - mesajlaşma
  - ros2
  - dağıtık-sistemler
toc: true
image: /img/ros-mimarisi-dugumler-64.png
---

Bir robotu tek parça hâlinde programlamak, bütün müzisyenlerin aynı enstrümanı çaldığı bir orkestra kurmaya benzer: Gürültü çıkar ama yönetmesi zordur. ROS (Robot Operating System), robot yazılımını küçük ve bağımsız **düğümlere (node)** ayırır. Sensör okuma, haritalama, rota planlama ve motor kontrolü gibi görevler farklı düğümlerde çalışır; aralarındaki iletişim ise standart mesajlaşma mekanizmalarıyla sağlanır.

![ros-mimarisi-dugumler-64](/img/ros-mimarisi-dugumler-64.svg)

``
## Düğüm nedir?

Düğüm, belirli bir sorumluluğu yerine getiren çalışan süreçtir. Örneğin bir mobil robotta şu düğümler bulunabilir:

- Kamera görüntüsünü yayımlayan kamera düğümü
- Engelleri belirleyen algılama düğümü
- Hedefe rota oluşturan planlama düğümü
- Tekerlek hızlarını yöneten motor düğümü

Bu yaklaşım **tek sorumluluk ilkesini** robotik dünyasına taşır. Bir düğümün iç algoritması değiştirildiğinde, iletişim sözleşmesi aynı kaldığı sürece diğer düğümlerin değiştirilmesi gerekmez. Başka bir deyişle modülerliği sağlayan şey yalnızca kodun bölünmesi değil, parçaların standart mesajlarla haberleşmesidir.

## Mesajlaşma modülerliği nasıl oluşturur?

ROS'ta bir mesaj, alanları önceden tanımlanmış veri paketidir. Örneğin hız komutu doğrusal ve açısal hız içerebilir:

$$
\mathbf{u} = \begin{bmatrix} v \\ \omega \end{bmatrix}
$$

Burada $v$ doğrusal, $\omega$ ise açısal hızdır. Motor düğümü bu değerlerin hangi algoritmayla hesaplandığını bilmez; yalnızca mesajı alıp uygular. Böylece rota planlayıcı A* yerine başka bir algoritmaya geçirilse bile motor katmanı çalışmaya devam eder.

Gönderici ve alıcı arasındaki bağımlılık şu şekilde düşünülebilir:

$$
Bağımlılık = Arayüz\ Bilgisi - İç\ Uygulama\ Bilgisi
$$

İyi tasarlanmış bir ROS sisteminde düğümler birbirlerinin iç uygulamasını değil, yalnızca mesaj tipini ve iletişim kanalını bilir.

| İletişim türü | Çalışma biçimi | Uygun kullanım |
|---|---|---|
| Topic | Yayıncı-abone, asenkron | Sensör akışları ve hız komutları |
| Service | İstek-cevap, kısa işlem | Ayar değiştirme veya harita kaydetme |
| Action | Uzun görev, geri bildirimli | Navigasyon ve robot kolu hareketi |
| Parameter | Düğüm yapılandırması | Eşik, hız limiti ve çalışma modu |

## Topic ile gevşek bağlı iletişim

Topic sisteminde yayıncı, mesajı hangi düğümün dinlediğini bilmez. Abone de verinin iç sistemde nasıl üretildiğiyle ilgilenmez. Örneğin ROS 2 üzerinde basit bir hız yayıncısı şöyle yazılabilir:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class HizYayinci(Node):
    def __init__(self):
        super().__init__('hiz_yayinci')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.hiz_gonder)

    def hiz_gonder(self):
        mesaj = Twist()
        mesaj.linear.x = 0.4
        mesaj.angular.z = 0.1
        self.publisher.publish(mesaj)

def main():
    rclpy.init()
    node = HizYayinci()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

Bu düğüm her yarım saniyede `/cmd_vel` konusuna hız komutu gönderir. Aynı konuya gerçek motor sürücüsü, simülatör veya test düğümü abone olabilir. Yayıncı kodunun bunların hangisinin kullanıldığını bilmesine gerek yoktur. Bu özellik donanımın simülasyonla değiştirilmesini ve birim testlerinin hazırlanmasını kolaylaştırır.

## ROS 1 ve ROS 2 açısından fark

ROS 1 merkezi keşif için `roscore` kullanırken ROS 2, DDS tabanlı dağıtık keşiften yararlanır. ROS 2 ayrıca QoS ayarlarıyla güvenilirlik, mesaj geçmişi ve teslim davranışını yapılandırabilir. Örneğin kamera görüntüsünde en güncel kare tercih edilirken kritik kontrol komutlarında güvenilir teslim seçilebilir.

Modülerliğin korunması için düğümleri küçük tutmak, standart mesaj tiplerini tercih etmek ve topic adlarını anlamlı belirlemek gerekir. Her şeyi yapan dev bir “mega node”, ROS kullanılsa bile sıkı bağımlılık yaratır. İyi bir ROS mimarisinde düğümler bağımsız müzisyenler, mesajlar notalar, topic'ler ise orkestranın iletişim kanallarıdır; uyum doğru arayüzlerden doğar.
