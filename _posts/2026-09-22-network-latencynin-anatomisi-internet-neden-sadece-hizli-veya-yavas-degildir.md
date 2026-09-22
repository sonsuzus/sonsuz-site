---
layout: post
title: "Network Latency’nin Anatomisi: İnternet Neden Sadece Hızlı veya Yavaş Değildir?"
math: true
categories: 
  - Bilgi
tags: 
  - network
  - latency
  - internet
  - performans
  - tcp
  - dns
toc: true
---

Bir web sitesinin geç açılması, görüntülü görüşmenin robot sesine dönüşmesi veya çevrim içi oyunda karakterinizin duvara doğru koşmaya devam etmesi genellikle “internet yavaş” cümlesiyle açıklanır. Oysa ağ performansı tek bir hız göstergesinden ibaret değildir. Bant genişliği, gecikme, jitter ve paket kaybı birlikte çalışır; bunlardan yalnızca biri kötü olduğunda bile kullanıcı deneyimi dramatik biçimde değişebilir.

``

## Bant genişliği ile gecikme aynı şey değildir

**Bant genişliği**, bir bağlantının saniyede taşıyabildiği veri miktarıdır ve genellikle Mbps veya Gbps ile ölçülür. **Latency**, bir paketin kaynaktan hedefe ulaşması için geçen süredir. Bu nedenle 1 Gbps bağlantı, uzak bir sunucuya otomatik olarak anında erişeceğiniz anlamına gelmez.

Bir veri aktarımının basitleştirilmiş süresi şöyle modellenebilir:

$$
T_{toplam} = T_{iletim} + T_{yayılım} + T_{işleme} + T_{kuyruk}
$$

Burada iletim süresi, paketin bağlantıya yerleştirilme süresidir:

$$
T_{iletim} = \frac{Paket\ Boyutu\ (bit)}{Bağlantı\ Hızı\ (bit/s)}
$$

Yayılım gecikmesi ise sinyalin fiziksel ortamda yol almasıdır. Fiber optikte veri ışık hızında değil, ışığın fiber içindeki daha düşük hızıyla ilerler. İstanbul’daki kullanıcı ile ABD’deki sunucu arasındaki mesafe, ne kadar pahalı modem alırsanız alın, ortadan kalkmaz. Fizik bu konuda pazarlığa pek açık değildir.

| Kavram | Neyi ölçer? | Kullanıcıya etkisi |
|---|---|---|
| Bant genişliği | Birim zamanda taşınan veri | Büyük indirmelerin süresi |
| Latency | Paketin ulaşma süresi | Tıklama sonrası bekleme |
| Jitter | Gecikmedeki değişkenlik | Ses ve görüntü kesintileri |
| Paket kaybı | Ulaşmayan paket oranı | Donma ve yeniden iletim |

## Gecikmenin dört temel bileşeni

**Yayılım gecikmesi**, coğrafi mesafeden kaynaklanır. **İletim gecikmesi**, paket boyutu ve bağlantı kapasitesiyle ilişkilidir. **İşleme gecikmesi**, yönlendiricilerin paket başlıklarını incelemesi, güvenlik kurallarını uygulaması veya NAT işlemleri gerçekleştirmesi sırasında oluşur. **Kuyruk gecikmesi** ise ağ cihazının aynı anda taşıyabileceğinden fazla paket almasıyla ortaya çıkar.

Özellikle kuyruk gecikmesi sürprizlidir. Evde biri büyük bir dosya yüklerken oyun ping’inin yükselmesi, çoğu zaman **bufferbloat** adı verilen aşırı tamponlama problemidir. Paketler kaybolmak yerine uzun kuyruklarda bekler. Sonuç: Hız testi harika görünürken oyun deneyimi çamura saplanır.

## RTT, DNS ve bağlantı kurma maliyeti

`ping` araçlarının çoğu **Round-Trip Time (RTT)** ölçer: Paketin hedefe gidip cevabın geri dönme süresi. Tek yönlü gecikme yaklaşık olarak $RTT/2$ kabul edilebilir; ancak gidiş ve dönüş rotaları farklı olabileceğinden bu yalnızca tahmindir.

Bir web isteği yalnızca veri indirmez. Önce DNS çözümlemesi yapılabilir, ardından TCP bağlantısı ve TLS oturumu kurulabilir. Her aşama ek ağ turları demektir. HTTP/2, HTTP/3, bağlantı yeniden kullanımı ve TLS oturum devam ettirme gibi teknolojiler bu turları azaltmaya çalışır.

## Kendi bağlantını incele

Aşağıdaki komutlar sorunun nerede oluştuğuna dair ilk ipuçlarını verir:

```bash
# Hedefe RTT ve paket kaybını ölçer
ping -c 10 example.com

# Paketlerin geçtiği ağ duraklarını gösterir
traceroute example.com

# DNS, TCP, TLS ve toplam süreleri ayrı ayrı raporlar
curl -o /dev/null -s -w 'DNS: %{time_namelookup}\nTCP: %{time_connect}\nTLS: %{time_appconnect}\nTotal: %{time_total}\n' https://example.com
```

Tek ölçüme güvenmek yerine farklı saatlerde, kablolu ve kablosuz bağlantılarda test yapmak gerekir. Wi-Fi paraziti, yoğun ISS omurgası, uzak sunucu veya yavaş DNS çözümleyicisi birbirine benzeyen belirtiler üretebilir.

## Doğru soru: Neresi yavaş?

İnternet performansını değerlendirirken “Kaç Mbps?” sorusu tek başına yetersizdir. Oyun ve görüntülü görüşmeler düşük latency ile istikrarlı jitter isterken, büyük dosya indirmeleri yüksek bant genişliğinden daha çok yararlanır. İyi bir ağ; yalnızca çok veri taşıyan değil, paketleri zamanında, düzenli ve kayıpsız ulaştıran ağdır. Kısacası internet bir otoyolsa bant genişliği şerit sayısı, latency yolculuk süresi, jitter trafik akışındaki düzensizlik, paket kaybı ise yolda kaybolan kargolardır.
