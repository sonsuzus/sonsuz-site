---
layout: post
title: "IPv6 Geçiş Stratejileri ve Çift Yığın Mimarisi"
math: true
categories: 
  - Bilgi
tags: 
  - IPv6
  - Ağ Yönetimi
  - Dual Stack
---

IPv4 adreslerinin tükenmesi, interneti bir gecede IPv6’ya taşımadı; bunun yerine iki protokolün uzun süre birlikte yaşadığı hibrit bir dönem başlattı. Çift yığın (dual stack) mimarisi, istemci, sunucu ve ağ cihazlarının aynı anda hem IPv4 hem de IPv6 adresi taşımasını sağlar. Doğru tasarlandığında kullanıcılar fark etmeden modern internete bağlanır; yanlış tasarlandığında ise DNS, güvenlik duvarı ve gecikme sorunları küçük bir ağ macerasını büyük bir operasyona dönüştürebilir.
``

## Neden doğrudan IPv6’ya geçmiyoruz?

IPv4, 32 bitlik adres alanına sahiptir; teorik kapasitesi $2^{32}$, yani yaklaşık 4,29 milyar adrestir. IPv6 ise 128 bit kullanır ve adres uzayı $2^{128}$ seviyesindedir. Bu değer yaklaşık $3,4 \times 10^{38}$ adres eder. Ancak sorun yalnızca adres sayısı değildir: eski uygulamalar, IoT cihazları, VPN uçları, güvenlik politikaları ve üçüncü taraf servisler hâlâ IPv4 bağımlılığı taşıyabilir.

| Özellik | IPv4 | IPv6 |
|---|---|---|
| Adres uzunluğu | 32 bit | 128 bit |
| Örnek adres | `192.0.2.10` | `2001:db8:10::10` |
| Yayın (broadcast) | Vardır | Yoktur; multicast kullanır |
| NAT ihtiyacı | Yaygındır | Temelde gerekli değildir |
| Otomatik yapılandırma | DHCP ağırlıklı | SLAAC ve DHCPv6 |

Çift yığın yaklaşımında cihaz, örneğin `192.0.2.25` ile birlikte `2001:db8:100:1::25` adresini alır. Uygulama bir alan adına erişirken DNS’ten hem `A` hem de `AAAA` kaydı gelebilir. İşletim sistemi, erişilebilirlik ve gecikme ölçümlerine göre uygun yolu seçer. Bu nedenle geçişin ilk kuralı şudur: **IPv6’yı eklemek, IPv4’ü hemen kaldırmak anlamına gelmez.**

## Geçiş stratejilerini karşılaştırmak

| Strateji | Çalışma biçimi | Güçlü yönü | Dikkat edilmesi gereken |
|---|---|---|---|
| Çift yığın | Her iki protokol aynı anda etkin | En uyumlu ve kademeli yöntem | İki ayrı güvenlik yüzeyi yönetilir |
| Tünelleme | IPv6 paketleri IPv4 ağında taşınır | IPv6 omurgası olmayan yerlerde hızlı başlangıç | MTU ve gecikme sorunları doğurabilir |
| Çeviri | IPv6 ve IPv4 uçları NAT64/DNS64 ile konuşturulur | IPv4 bağımlı hedeflere IPv6 erişimi | Uygulama ve loglama karmaşıklaşabilir |
| IPv6-only | İç ağda yalnızca IPv6 kullanılır | Uzun vadede sade mimari | Eski servisler için çeviri gerekir |

Kurumsal ağlar için genellikle en güvenli rota çift yığınla başlamaktır. Önce internet çıkışı, DNS, temel yönlendiriciler ve güvenlik duvarları IPv6’ya hazırlanır. Ardından pilot VLAN’lar, kablosuz ağlar ve belirli sunucu grupları devreye alınır. Her aşama ölçülmeli, geri dönüş planı hazırlanmalı ve kullanıcı deneyimi test edilmelidir.

## Adresleme ve yönlendirme planı

IPv6’da geniş alan, plansız davranma izni vermez. Kurumunuza tahsis edilen `/48` bloğu, çoğunlukla her VLAN veya alt ağ için bir `/64` ayrılacak şekilde bölünür. Örneğin `2001:db8:1200::/48` bloğundan kullanıcı ağına `2001:db8:1200:10::/64`, sunucu ağına `2001:db8:1200:20::/64` verilebilir. `/64`, SLAAC ve birçok IPv6 mekanizması için beklenen standart alt ağ boyutudur.

Aşağıdaki Linux örneği, bir arayüze IPv6 adresi ekler ve varsayılan rotayı tanımlar:

```bash
# eth0 arayüzüne kalıcı olmayan örnek IPv6 adresi ekler
ip -6 addr add 2001:db8:1200:20::10/64 dev eth0

# IPv6 varsayılan ağ geçidini tanımlar
ip -6 route add default via 2001:db8:1200:20::1

# Yapılandırmayı doğrular
ip -6 addr show dev eth0
ip -6 route show
```

Bu komutlar laboratuvar veya geçici test için uygundur; üretimde NetworkManager, systemd-networkd ya da dağıtımın kalıcı ağ yapılandırma aracı kullanılmalıdır.

## DNS, güvenlik ve izleme: görünmeyen kritik katmanlar

Bir servisi IPv6 üzerinden yayınlamak için DNS’e `AAAA` kaydı eklenir. Fakat AAAA kaydı, hizmetin gerçekten IPv6’da erişilebilir olduğu doğrulanmadan yayınlanmamalıdır. Aksi durumda bazı kullanıcılar önce başarısız IPv6 bağlantısı dener ve uygulama yavaş hissedilir. Happy Eyeballs mekanizması bu riski azaltır, ancak kötü yapılandırmayı sihirli biçimde çözmez.

Güvenlik duvarında IPv4 kurallarını kopyalamak da yeterli değildir. ICMPv6 paketleri—özellikle Neighbor Discovery ve Packet Too Big mesajları—IPv6’nın sağlıklı işlemesi için gereklidir. Bunları tamamen engellemek, bağlantıların gizemli biçimde bozulmasına yol açabilir. Son olarak loglar, SIEM kuralları, NetFlow/IPFIX kayıtları ve izleme panelleri hem IPv4 hem IPv6 kaynak adreslerini anlayabilmelidir.

Başarılı geçişin özeti basittir: önce envanter çıkarın, sonra adres planlayın, küçük bir pilotla test edin ve her aşamayı ölçün. Çift yığın, geçici bir karmaşa değil; IPv6-odaklı geleceğe kontrollü bir köprüdür.
