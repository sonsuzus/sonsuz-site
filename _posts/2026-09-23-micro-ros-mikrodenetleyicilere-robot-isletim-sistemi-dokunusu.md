---
layout: post
title: "Micro-ROS: Mikrodenetleyicilere Robot İşletim Sistemi Dokunuşu"
math: true
categories: 
  - Bilgi
tags: 
  - micro-ros
  - ros2
  - mikrodenetleyici
  - robotik
  - gömülü-sistemler
  - freertos
toc: true
---

Bir robotun motorunu milisaniyeler içinde kontrol etmek isteyen küçücük bir mikrodenetleyici ile harita çıkaran güçlü bir bilgisayar aynı dili konuşabilir mi? Micro-ROS tam olarak bu soruya “Evet!” cevabını verir. ROS 2 ekosisteminin iletişim modelini kaynakları sınırlı mikrodenetleyicilere taşıyarak sensörlerden motor sürücülerine kadar robotun en küçük parçalarını dağıtık sistemin birer üyesi hâline getirir.
``
## Micro-ROS neden var?

ROS 2; düğüm, konu, servis ve eylem gibi güçlü kavramlar sunar. Ancak standart bir ROS 2 kurulumu genellikle Linux çalışan, belleği görece geniş bilgisayarları hedefler. STM32, ESP32 veya RP2040 gibi mikrodenetleyicilerde ise RAM kilobaytlarla, işlemci hızı megahertzlerle ölçülür.

Micro-ROS, ROS 2 davranışlarını bu küçük cihazlara uyarlayan bir istemci mimarisi kullanır. Mikrodenetleyicide çalışan **Micro-ROS Client**, daha güçlü bir cihazdaki **Micro-ROS Agent** ile haberleşir. Agent, istemci ile ROS 2 ağı arasında köprü görevi görür.

| Özellik | Standart ROS 2 düğümü | Micro-ROS istemcisi |
|---|---|---|
| Tipik platform | Linux bilgisayar | Mikrodenetleyici |
| Bellek | MB veya GB | KB veya birkaç MB |
| DDS kullanımı | Doğrudan | Agent üzerinden |
| İşletim sistemi | Ubuntu, Windows | FreeRTOS, Zephyr, NuttX |
| Amaç | Algılama, planlama | Sensör okuma, gerçek zamanlı kontrol |

## İletişimin perde arkası

ROS 2 iletişiminin temelinde DDS bulunur. Tam DDS uygulaması mikrodenetleyici için ağır olabileceğinden Micro-ROS, **DDS-XRCE** protokolünden yararlanır. XRCE, “Extremely Resource Constrained Environments” ifadesinin kısaltmasıdır; yani ismi bile küçük cihazlara göz kırpar.

İstemci ile Agent arasındaki iletişim seri port, UDP veya özel taşıma katmanları üzerinden gerçekleştirilebilir. Basitleştirilmiş veri yolu şöyledir:

```text
Sensör -> Micro-ROS Client -> XRCE -> Agent -> ROS 2 ağı
```

Bir kontrol döngüsünün çalışma frekansı, periyot üzerinden hesaplanabilir:

$$f = \frac{1}{T}$$

Örneğin motor kontrol görevi her $T=0.01$ saniyede çalışıyorsa frekans $f=100\,Hz$ olur. Micro-ROS iletişimi sağlasa da deterministik zamanlama için FreeRTOS gibi gerçek zamanlı işletim sisteminin görev öncelikleri doğru ayarlanmalıdır.

## Basit bir yayıncı örneği

Aşağıdaki C kodu, sayaç değerini ROS 2 konusu olarak yayımlayan sadeleştirilmiş bir Micro-ROS döngüsüdür:

```c
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <std_msgs/msg/int32.h>

rcl_publisher_t publisher;
std_msgs__msg__Int32 message;

void timer_callback(rcl_timer_t *timer, int64_t last_call_time)
{
    (void) last_call_time;
    if (timer != NULL) {
        message.data++;
        rcl_publish(&publisher, &message, NULL);
    }
}
```

`rcl_publish` mesajı doğrudan klasik DDS ağına göndermek yerine istemci çalışma zamanı üzerinden Agent’a iletir. Gerçek projede yayıncı, düğüm, zamanlayıcı ve executor nesneleri ayrıca başlatılır. Sayaç yerine enkoder konumu veya sıcaklık ölçümü koyduğumuzda kod, robotun gerçek bir bileşenine dönüşür.

## Kaynak planlaması neden kritik?

Mikrodenetleyicide her bayt değerlidir. Yaklaşık bellek ihtiyacını şu şekilde düşünebiliriz:

$$M_{toplam} = M_{uygulama} + M_{RTOS} + M_{microROS} + M_{mesajlar}$$

Büyük mesaj dizileri, gereksiz abonelikler ve sık dinamik bellek ayırma RAM tüketimini artırır. Bu nedenle sabit boyutlu mesajlar, önceden ayrılmış bellek ve ölçülü yayın frekansları tercih edilmelidir.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Yüksek yayın hızı | Güncel veri | Ağ ve CPU yükü |
| Statik bellek | Öngörülebilir davranış | Daha az esneklik |
| UDP taşıma | Hızlı iletişim | Paket kaybı |
| Seri bağlantı | Basit ve kararlı | Bant genişliği sınırlı |

## Ne zaman kullanılmalı?

Micro-ROS; tekerlek enkoderleri, IMU sensörleri, motor sürücüleri ve düşük seviyeli güvenlik denetimleri için güçlü bir seçenektir. Görüntü işleme veya rota planlama gibi ağır görevler ise üst bilgisayarda kalmalıdır. Böylece mikrodenetleyici refleksleri, bilgisayar da büyük resmi yönetir. Kısacası Micro-ROS, robotun minik sinir uçlarını ROS 2 beynine bağlayan çevik bir sinir sistemi kurar.
