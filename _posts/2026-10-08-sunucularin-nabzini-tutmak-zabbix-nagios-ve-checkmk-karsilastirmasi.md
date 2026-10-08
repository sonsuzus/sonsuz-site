---
layout: post
title: "Sunucuların Nabzını Tutmak: Zabbix, Nagios ve Checkmk Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - sunucu izleme
  - zabbix
  - nagios
  - checkmk
  - devops
  - sistem yönetimi
toc: true
image: /img/sunucularin-nabzini-tutmak-61.png
---

![sunucularin-nabzini-tutmak-61](/img/sunucularin-nabzini-tutmak-61.svg)


Bir sunucunun çalışıyor görünmesi, sağlıklı olduğu anlamına gelmez. İşlemci tavana vurmuş, disk dolmak üzere veya ağ gecikmesi kullanıcıları çileden çıkarıyor olabilir. Sunucu izleme sistemleri; altyapının nabzını ölçer, sorunları görünür hâle getirir ve gece telefonunuz çalmadan önce sizi uyarır. Bu alandaki üç güçlü seçenek Zabbix, Nagios ve Checkmk’tir.
``
## İzleme sistemlerinin temel mantığı

Bir izleme platformu belirli aralıklarla **metrik** toplar. CPU kullanımı, boş disk alanı, bellek tüketimi ve HTTP yanıt süresi bu metriklere örnektir. Toplanan değerler önceden belirlenmiş eşiklerle karşılaştırılır; şart sağlandığında olay oluşturulur ve bildirim gönderilir.

Basit bir CPU kullanım oranı şöyle hesaplanabilir:

$$
CPU\ Kullanımı\ (\%) = \frac{T_{toplam} - T_{boşta}}{T_{toplam}} \times 100
$$

Ancak tek bir yüksek ölçüm her zaman sorun değildir. Kısa süreli sıçramaları filtrelemek için hareketli ortalama kullanılabilir:

$$
\bar{x}_n = \frac{1}{n}\sum_{i=1}^{n}x_i
$$

Örneğin son beş ölçümün ortalaması yüzde 90’ı geçerse alarm üretmek, anlık bir yükselişte gereksiz bildirim almaktan daha mantıklıdır. Aksi hâlde izleme sistemi yardımcı olmak yerine dijital bir yangın alarmına dönüşür.

## Üç aracın hızlı karşılaştırması

| Özellik | Zabbix | Nagios | Checkmk |
|---|---|---|---|
| Kurulum yaklaşımı | Bütünleşik platform | Çekirdek ve eklentiler | Otomasyon odaklı platform |
| Arayüz | Modern ve kapsamlı | Core sürümünde sınırlı | Kullanıcı dostu |
| Otomatik keşif | Güçlü | Ek yapılandırma gerekir | Çok güçlü |
| Ölçeklenebilirlik | Yüksek | Doğru mimariyle yüksek | Yüksek |
| Öğrenme eğrisi | Orta | Orta-yüksek | Düşük-orta |
| En uygun kullanım | Büyük ve karma altyapılar | Özelleştirilmiş kontroller | Hızlı devreye alma |

## Zabbix: Her şey tek çatı altında

Zabbix; metrik toplama, grafik çizme, alarm üretme, otomatik keşif ve raporlama özelliklerini birlikte sunar. Agent kullanarak işletim sisteminden ayrıntılı veri alabilir; SNMP, IPMI, JMX ve HTTP kontrolleriyle farklı cihazları izleyebilir.

Linux sunucuya kurulan agent’ın temel durumunu şu komutlarla kontrol edebilirsiniz:

```bash
sudo systemctl enable --now zabbix-agent2
sudo systemctl status zabbix-agent2
```

İlk komut servisi başlatıp sistem açılışına ekler; ikincisi agent’ın düzgün çalışıp çalışmadığını gösterir. Zabbix özellikle merkezi gösterge panelleri ve geçmiş veriler üzerinden kapasite planlaması isteyen ekipler için başarılıdır.

## Nagios: Eklentilerle büyüyen klasik

Nagios, izleme dünyasının deneyimli ustasıdır. Temel felsefesi basittir: Bir eklenti kontrol gerçekleştirir ve durum kodu döndürür. `0` başarılı, `1` uyarı, `2` kritik, `3` ise bilinmeyen durum anlamına gelir.

Örneğin disk kullanımını denetleyen bir eklenti şöyle çağrılabilir:

```bash
/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -p /
```

Bu kontrol, kök bölümde boş alan yüzde 20’nin altına inince uyarı, yüzde 10’un altına inince kritik durum üretir. Nagios son derece esnektir; ancak eklenti ve yapılandırma yönetimi büyüyen ortamlarda ciddi emek isteyebilir.

## Checkmk: Otomasyon sevenlerin seçeneği

Checkmk, Nagios ekosisteminin kontrol mantığından yararlanırken keşif, yapılandırma ve görselleştirme süreçlerini kolaylaştırır. Tek bir agent çıktısından yüzlerce servisi otomatik keşfedebilir. Bu özellik, çok sayıda benzer sunucuyu yöneten ekiplerin tekrar eden işlerini azaltır.

Kural tabanlı yapılandırma sayesinde aynı disk eşiğini her sunucu için ayrı ayrı yazmak yerine sunucu gruplarına uygulayabilirsiniz. Raw Edition açık kaynak odaklıdır; Enterprise Edition ise daha gelişmiş performans ve kurumsal özellikler sunar.

## Hangisini seçmelisiniz?

Hazır grafikler, geniş protokol desteği ve bütünleşik deneyim istiyorsanız **Zabbix** güçlü bir tercihtir. Kontrolleri tamamen özelleştirmek ve geniş eklenti ekosisteminden yararlanmak istiyorsanız **Nagios** uygundur. Hızlı keşif, kolay yönetim ve düşük operasyon yükü önceliğinizse **Checkmk** öne çıkar.

Son kararı özellik listesinden önce ekibinizin deneyimi, izlenecek cihaz sayısı ve alarm yönetimi ihtiyacı belirlemelidir. Çünkü en iyi izleme sistemi, en fazla grafiği çizen değil; doğru sorunu, doğru kişiye, doğru zamanda bildiren sistemdir.
