---
layout: post
title: "DHCP'nin Anatomisi: Bilgisayar Açıldığında IP Adresini Nasıl Buluyor?"
math: true
categories: 
  - Bilgi
tags: 
  - dhcp
  - ağ
  - ip adresi
  - tcp-ip
  - network
  - udp
toc: true
image: /img/dhcpnin-anatomisi-bilgisayar-47.png
---

Bilgisayarınızı açtığınızda tarayıcı hemen çalışır, mesajlar gelir ve internet sanki musluktan akan su gibi hazırdır. Oysa cihazınızın ağda konuşabilmesi için önce bir IP adresi, ağ maskesi, ağ geçidi ve DNS sunucusu edinmesi gerekir. Bu otomatik tanışma törenini yöneten protokolün adı **DHCP**, yani Dynamic Host Configuration Protocol'dür.

``

## IP adresi neden gerekli?

IP adresi, cihazın ağ üzerindeki mantıksal konumudur. Posta benzetmesi yaparsak MAC adresi binanın değişmeyen seri numarası, IP adresi ise o gün kullanılan teslimat adresidir. Bir cihaz yalnızca IP adresine değil, aşağıdaki bilgilere de ihtiyaç duyar:

- **IP adresi:** Cihazın ağdaki kimliği
- **Alt ağ maskesi:** Hangi adreslerin yerel olduğunu belirleyen sınır
- **Varsayılan ağ geçidi:** Diğer ağlara açılan kapı
- **DNS sunucusu:** Alan adlarını IP adreslerine çeviren rehber
- **Kira süresi:** Yapılandırmanın ne kadar süre kullanılabileceği

Örneğin `192.168.1.42/24` adresinde `/24`, ilk 24 bitin ağ bölümünü gösterir. Bu ağdaki kullanılabilir adres sayısı teorik olarak şöyle hesaplanır:

$$2^{32-24} - 2 = 254$$

Çıkarılan iki adres, ağ adresi ile broadcast adresidir.

## DORA: Dört mesajlık tanışma

Bilgisayar ilk açıldığında henüz IP adresini ve DHCP sunucusunun konumunu bilmez. Bu nedenle süreci broadcast mesajıyla başlatır. DHCP'nin temel akışı **DORA** kısaltmasıyla hatırlanır:

| Aşama | Mesaj | Kim gönderir? | Amaç |
|---|---|---|---|
| 1 | Discover | İstemci | Ağdaki DHCP sunucularını arar |
| 2 | Offer | Sunucu | Kullanılabilecek bir IP önerir |
| 3 | Request | İstemci | Seçtiği teklifi ilan eder |
| 4 | Acknowledge | Sunucu | Kiralamayı onaylar ve ayarları yollar |

![dhcpnin-anatomisi-bilgisayar-47](/img/dhcpnin-anatomisi-bilgisayar-47.svg)


İlk pakette kaynak IP `0.0.0.0`, hedef IP ise `255.255.255.255` olabilir. Bir başka deyişle bilgisayar, “Ben daha kim olduğumu bilmiyorum; burada bana adres verecek biri var mı?” diye bağırır.

DHCP, taşıma katmanında UDP kullanır. Sunucu **67**, istemci ise **68** numaralı portu dinler. UDP bağlantı kurma zorunluluğu taşımadığı için henüz tam yapılandırılmamış bir istemci açısından oldukça uygundur.

## Teklif nasıl seçiliyor?

Ağda birden fazla DHCP sunucusu varsa istemci birden fazla `DHCPOFFER` alabilir. Genellikle ilk uygun teklifi seçer ve `DHCPREQUEST` mesajıyla seçimini broadcast olarak duyurur. Böylece diğer sunucular ayırdıkları adresleri tekrar havuza bırakabilir.

Sunucu son olarak `DHCPACK` gönderir. Bu pakette IP adresinin yanında ağ maskesi, ağ geçidi, DNS ve kira süresi gibi **DHCP seçenekleri** bulunur. Adres kalıcı olarak verilmez; belirli süreliğine kiralanır.

Kira süresi $L$ ise istemci çoğunlukla şu iki zamanda yenileme dener:

$$T_1 = 0.5L \qquad T_2 = 0.875L$$

$T_1$ aşamasında doğrudan eski sunucuyla konuşur. Yanıt alamazsa $T_2$ aşamasında diğer DHCP sunucularına da ulaşmayı dener.

## Trafiği gözlemlemek

Linux üzerinde DHCP paketlerini görmek için aşağıdaki komut kullanılabilir:

```bash
sudo tcpdump -i eth0 -n -vv 'udp port 67 or udp port 68'
```

Bu komut `eth0` arayüzünü dinler, isim çözümlemesi yapmadan ayrıntılı çıktı verir ve yalnızca DHCP'nin kullandığı UDP portlarını filtreler. Ardından bağlantıyı yenileyerek DORA mesajlarını canlı biçimde izleyebilirsiniz:

```bash
sudo dhclient -r eth0
sudo dhclient -v eth0
```

İlk komut mevcut kirayı bırakır; ikincisi yeni adres ister ve süreci ayrıntılı gösterir. Üretim sunucusunda çalıştırmadan önce dikkatli olun: bağlantınızı kendi ellerinizle kesebilirsiniz!

## Sunucu başka ağdaysa ne olur?

Broadcast paketleri yönlendiricilerden normalde geçmez. DHCP sunucusu farklı bir alt ağdaysa yönlendirici üzerindeki **DHCP Relay Agent**, istemcinin mesajını sunucuya unicast olarak iletir. Sunucu da isteğin geldiği alt ağı relay bilgisinden anlayarak doğru adres havuzunu seçer.

Hiçbir DHCP sunucusu bulunamazsa bazı sistemler `169.254.0.0/16` aralığından otomatik bir adres seçer. Bu durum yerel iletişime izin verebilir ancak genellikle internete çıkış sağlamaz. Kısacası internete bağlanamayan cihazınız `169.254.x.x` aldıysa, suçlu çoğu zaman kablo, Wi-Fi erişimi veya DHCP hizmetidir; tarayıcı masum olabilir.
