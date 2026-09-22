---
layout: post
title: "ARP Protokolü: IP Adresinden Ethernet Adresine Yolculuk"
math: true
categories: 
  - Bilgi
tags: 
  - arp
  - ethernet
  - ip
  - ağ
  - mac-adresi
  - tcp-ip
toc: true
image: /img/arp-protokolu-ip-40.png
---

Bilgisayarınız aynı yerel ağdaki bir sunucuya paket göndermek istediğinde hedefin IP adresini biliyor olabilir; fakat Ethernet çerçevesini teslim edebilmek için bir de fiziksel, yani MAC adresine ihtiyaç duyar. İşte ARP (Address Resolution Protocol), “Bu IP adresi kimde ve MAC adresi nedir?” sorusunu ağdaki cihazlara sorarak iki adresleme dünyası arasında köprü kurar.


![arp-protokolu-ip-40](/img/arp-protokolu-ip-40.svg)

``

## İki farklı adres neden var?

IP adresleri ağlar arasında mantıksal yönlendirme yapmak için kullanılır. MAC adresleri ise Ethernet gibi veri bağlantı katmanı teknolojilerinde, aynı yerel ağ segmentindeki teslimatı gerçekleştirir. Basitleştirilmiş biçimde ARP’nin yaptığı dönüşümü şöyle gösterebiliriz:

$$f(IPv4\ adresi) \rightarrow MAC\ adresi$$

Örneğin bilgisayarınız `192.168.1.20` adresine bir IPv4 paketi gönderecek olsun. İşletim sistemi önce hedefin aynı alt ağda bulunup bulunmadığını, kendi IP adresi ve alt ağ maskesiyle hesaplar:

$$Ağ\ adresi = IP\ adresi \land Alt\ ağ\ maskesi$$

Hedef aynı ağdaysa doğrudan hedef cihazın MAC adresi aranır. Farklı ağdaysa hedef sunucunun değil, paketi dış ağa taşıyacak varsayılan ağ geçidinin MAC adresi gerekir.

| Özellik | IP adresi | MAC adresi |
|---|---|---|
| Kullanıldığı katman | Ağ katmanı | Veri bağlantı katmanı |
| Temel görevi | Ağlar arası yönlendirme | Yerel ağda çerçeve teslimi |
| Örnek | `192.168.1.20` | `00:1A:2B:3C:4D:5E` |
| Tipik kapsam | Yerel ve uzak ağlar | Aynı Ethernet segmenti |

## ARP çözümlemesi nasıl çalışır?

Süreç dört temel adımda gerçekleşir:

1. Gönderici, önce işletim sistemindeki **ARP önbelleğini** kontrol eder.
2. Kayıt yoksa hedef IP’yi soran bir **ARP Request** paketi oluşturur.
3. Bu istek Ethernet yayın adresi olan `FF:FF:FF:FF:FF:FF` üzerinden ağdaki herkese gönderilir.
4. İlgili IP’ye sahip cihaz, kendi MAC adresini içeren bir **ARP Reply** cevabı yollar.

Örneğin `192.168.1.10`, `192.168.1.20` adresini arıyorsa istek kabaca “`192.168.1.20` kimde? Cevabı `192.168.1.10` adresine gönder!” der. Ağdaki tüm cihazlar yayını görür, ancak normal şartlarda yalnızca aranan cihaz cevap verir. Gönderici gelen eşleşmeyi kısa süreliğine ARP önbelleğine kaydeder; böylece her Ethernet çerçevesi için yeniden soru sormaz.

| ARP mesajı | Dağıtım biçimi | Amacı |
|---|---|---|
| ARP Request | Broadcast | IP sahibini bulmak |
| ARP Reply | Genellikle unicast | MAC adresini bildirmek |

## ARP tablosunu incelemek

Windows, Linux ve macOS üzerinde önbellekteki eşleşmeler görüntülenebilir:

```bash
# Linux ve modern ağ araçları
ip neigh show

# Windows
arp -a

# Belirli bir komşuyu Linux'ta siler
sudo ip neigh del 192.168.1.20 dev eth0
```

`ip neigh show` çıktısında `REACHABLE`, `STALE` veya `FAILED` gibi durumlar görülebilir. `REACHABLE`, komşunun yakın zamanda doğrulandığını; `STALE`, kaydın bulunduğunu fakat yeniden kontrol gerekebileceğini; `FAILED` ise adres çözümlemesinin başarısız olduğunu belirtir.

## Küçük ama önemli ayrıntılar

ARP yalnızca IPv4 için kullanılır ve yönlendiriciler normalde ARP yayınlarını başka ağlara taşımaz. IPv6 dünyasında aynı görev, ICMPv6 tabanlı **Neighbor Discovery Protocol (NDP)** tarafından gerçekleştirilir. Ayrıca bir cihaz kendi IP-MAC eşleşmesini duyurmak veya adres çakışmasını denetlemek için **Gratuitous ARP** gönderebilir.

ARP’nin yerleşik kimlik doğrulaması bulunmadığından saldırganlar sahte cevaplarla önbellekleri zehirleyebilir. **ARP spoofing** adı verilen bu saldırı, trafiğin saldırgan üzerinden geçirilmesine yol açabilir. Yönetilebilir anahtarlardaki Dynamic ARP Inspection, DHCP Snooping, ağ segmentasyonu ve şifreli protokoller riski azaltır.

Kısacası IP paketi nereye gitmek istediğini söyler, ARP ise yerel ağda paketi teslim edecek Ethernet adresini bulur. Perde arkasında birkaç milisaniyede gerçekleşen bu küçük diyalog olmasaydı, aynı masadaki iki bilgisayar bile birbirine ulaşamazdı.
