---
layout: post
title: "Ham Soketlerle Özel TCP El Sıkışması ve Pencere Yönetimi"
math: true
categories: 
  - Proje
tags: 
  - linux
  - tcp
  - raw socket
  - ağ programlama
  - python
---

Linux’un TCP yığını çoğu uygulama için harika bir güvenlik ağıdır: bağlantıyı kurar, paketleri yeniden iletir ve pencereyi otomatik ayarlar. Fakat paket düzeyinde deney yapmak, özel bir protokol laboratuvarı kurmak veya TCP’nin iç işleyişini gerçekten anlamak istiyorsanız ham soketler ilginç bir kapı açar. Buradaki önemli düzeltme şudur: `SOCK_RAW`, ağ kartını ve çekirdeği tamamen atlamaz; paketi yine Linux üzerinden gönderir. Ancak çekirdeğin sizin adınıza TCP durum makinesi yönetmesini atlayıp TCP başlığını kendiniz üretmenizi sağlar.
``

Bu yaklaşımda uygulamanız küçük bir TCP motoruna dönüşür. Üçlü el sıkışmada istemci önce `SYN`, sunucu `SYN+ACK`, istemci ise son `ACK` paketini üretir. Her baytın sıra numarası vardır; `SYN` ve `FIN` bayrakları da birer sıra numarası tüketir. Başlangıç sıra numarası $ISN_c$ olan istemci için temel ilişki şöyledir:

$$ACK_c = ISN_s + 1$$

Sunucunun ilk veri baytını kabul etmeye hazır olduğu sıra değeri ise $ISN_c + 1$ olur. Bu basit görünen `+1`, el sıkışmada en sık yapılan off-by-one hatalarının başrol oyuncusudur.

| Aşama | İstemci alanları | Sunucu alanları | Amaç |
|---|---|---|---|
| 1 | `SYN`, `seq=ISN_c` | — | Bağlantı talebi |
| 2 | — | `SYN,ACK`, `seq=ISN_s`, `ack=ISN_c+1` | Talebi onaylama |
| 3 | `ACK`, `seq=ISN_c+1`, `ack=ISN_s+1` | — | Bağlantıyı kurma |

Ham soket açmak için süreçte `CAP_NET_RAW` yetkisi gerekir; geliştirme ortamında bu genellikle root olarak çalışmak anlamına gelir. Ayrıca işletim sisteminin aynı dörtlü için (`kaynak IP`, `kaynak port`, `hedef IP`, `hedef port`) otomatik `RST` göndermesi deneyinizi bozabilir. Bu yüzden en güvenlisi, size ait bir ağ ad alanında veya izole bir sanal laboratuvarda çalışmaktır. Gerçek sistemlere izinsiz paket göndermek hem etik hem de operasyonel açıdan kötü bir fikirdir.

Aşağıdaki Python parçası, IP başlığını uygulamanın sağlayacağını belirten temel gönderim soketini gösterir. Bu kod tam bir TCP istemcisi değildir; `build_ipv4_tcp_syn` fonksiyonunun IP/TCP başlıklarını, seçenekleri ve checksum değerlerini ürettiği varsayılır.

```python
import socket

src_ip = "192.0.2.10"
dst_ip = "192.0.2.20"
src_port, dst_port = 40000, 8080
isn = 0x13572468

raw = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
raw.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

syn = build_ipv4_tcp_syn(
    src_ip, dst_ip, src_port, dst_port,
    seq=isn, window=32768,
    options=[("MSS", 1460), ("WS", 7)]
)
raw.sendto(syn, (dst_ip, 0))
```

Asıl emek `build_ipv4_tcp_syn` içinde saklıdır. IPv4 başlık checksum’ı yalnızca IP başlığını kapsarken, TCP checksum’ı TCP başlığına ek olarak pseudo-header kullanır. Pseudo-header; kaynak/hedef IP, protokol ve TCP uzunluğu içerir. Böylece yanlış hedefe yönelen veya taşıma katmanında bozulan paketlerin yakalanması kolaylaşır. Checksum hesabı 16 bitlik one’s-complement toplamına dayanır:

$$checksum = \sim \left(\sum_{i=1}^{n} word_i\right)$$

Pencere yönetimi ise alıcının tampon kapasitesini ilan etmesidir. Göndericinin uçuşta tutabileceği veri yaklaşık olarak $min(cwnd, rwnd)$ ile sınırlıdır. Kendi mekanizmanızda `rwnd` değerini TCP başlığındaki 16 bitlik `window` alanına yazarsınız. Window Scale seçeneği etkinse gerçek pencere $window \times 2^{scale}$ olur.

| Kavram | Çekirdek TCP’si | Özel ham-soket TCP’si |
|---|---|---|
| Yeniden iletim | Otomatik zamanlayıcılar | RTO ve sayaçları siz yazarsınız |
| Sıra takibi | Durum makinesi yönetir | `seq` ve `ack` elle güncellenir |
| Pencere | Otomatik ayarlanabilir | Buffer durumuna göre siz ilan edersiniz |
| Kayıp paket | Hızlı yeniden iletim uygulanır | DupACK/SACK mantığını siz kurarsınız |

Alım tarafında `AF_PACKET` ya da uygun bir raw receive soketiyle yalnızca hedef akışın paketlerini filtreleyin. Gelen `SYN+ACK` için hem bayrakları hem de `ack == isn + 1` koşulunu doğrulayın; ardından son ACK’yi üretin. Daha ileri aşamada gecikmiş ACK, sıfır pencere, persist timer ve SACK eklemek bu mini projeyi gerçek bir taşıma katmanı laboratuvarına dönüştürür. Başarı ölçütünüz sadece bağlantı kurmak değil; paket kaybı ve sıralama bozulması altında da tutarlı kalmaktır.
