---
layout: post
title: "Linux Netfilter Kancaları: Iptables Arka Planda Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - netfilter
  - iptables
  - ağ
  - güvenlik
  - çekirdek
toc: true
image: /img/linux-netfilter-kancalari-38.png
---

Bir Linux makinesi yalnızca paketleri alan bir posta kutusu değildir; gerektiğinde yönlendirici, güvenlik duvarı ve NAT geçidi olabilir. Bu yeteneklerin merkezinde, ağ paketleri çekirdek içinde ilerlerken belirli kontrol noktalarında onları yakalayan **Netfilter kancaları** bulunur. `iptables` ise bu altyapıyı yapılandırmak için kullanılan kullanıcı alanı aracıdır. Başka bir deyişle iptables trafik polisi, Netfilter ise yolların ve kontrol noktalarının kendisidir.
``

## Netfilter ve iptables aynı şey mi?

Netfilter, Linux çekirdeğine gömülü bir paket işleme çatısıdır. Çekirdek modülleri, paketlerin geçtiği kancalara fonksiyon kaydedebilir. Iptables komutu ise kuralları Netfilter tarafından anlaşılacak biçimde çekirdeğe iletir.

Bir kuralı basitçe şu karar fonksiyonu gibi düşünebiliriz:

$$
f(p) = \begin{cases}
ACCEPT, & p \text{ kurala uyuyorsa} \\
DROP, & p \text{ engelleniyorsa} \\
CONTINUE, & \text{eşleşme yoksa}
\end{cases}
$$

Buradaki $p$; kaynak adresi, hedef adresi, protokolü, portları ve bağlantı durumunu taşıyan pakettir. Paket bir zincirdeki kuralları sırasıyla gezer; bu nedenle kural sırası sonucu doğrudan etkiler.

## Beş temel kanca

Netfilter, IPv4 ve IPv6 paket akışında beş ana kanca sunar:

| Kanca | Ne zaman çalışır? | İlişkili iptables zinciri |
|---|---|---|
| `PREROUTING` | Paket gelir gelmez, rota kararı verilmeden önce | PREROUTING |
| `INPUT` | Hedef yerel makineyse | INPUT |
| `FORWARD` | Paket başka bir makineye aktarılacaksa | FORWARD |
| `OUTPUT` | Paket yerel bir süreç tarafından üretildiyse | OUTPUT |
| `POSTROUTING` | Paket arayüzden çıkmadan hemen önce | POSTROUTING |

Dışarıdan gelen bir paketin yolu, rota kararına göre ikiye ayrılır:

$$
PREROUTING \rightarrow \begin{cases}
INPUT, & \text{yerel hedef} \\
FORWARD \rightarrow POSTROUTING, & \text{uzak hedef}
\end{cases}
$$

Yerel bir uygulamanın ürettiği paket ise çoğunlukla `OUTPUT → POSTROUTING` yolunu izler. Dolayısıyla bir web sunucusuna gelen trafiği `INPUT`, yönlendiriciden geçen trafiği ise `FORWARD` zincirinde filtrelemek gerekir.

## Tablolar ne işe yarar?

Kancalar paketin **nerede**, tablolar ise **hangi amaçla** işleneceğini açıklar.

| Tablo | Temel görev | Örnek kullanım |
|---|---|---|
| `filter` | İzin verme ve engelleme | SSH erişimini sınırlamak |
| `nat` | Adres veya port çevirmek | DNAT, SNAT, MASQUERADE |
| `mangle` | Paket alanlarını değiştirmek | TTL veya işaret ayarlamak |
| `raw` | Connection tracking öncesi işlem | `NOTRACK` uygulamak |
| `security` | Güvenlik etiketleri | SELinux tabanlı denetim |

Her tablo bütün zincirlere sahip değildir. Örneğin `filter` tablosu INPUT, FORWARD ve OUTPUT zincirlerini kullanırken NAT işlemleri çoğunlukla PREROUTING ve POSTROUTING çevresinde gerçekleşir.

## Bir kural çekirdekte nasıl işler?

Aşağıdaki komut, TCP üzerinden gelen 22 numaralı porta yalnızca belirli ağdan erişim sağlar:

```bash
iptables -A INPUT -p tcp --dport 22 \
  -s 192.168.10.0/24 -m conntrack --ctstate NEW \
  -j ACCEPT
```

`-A INPUT` kuralı zincirin sonuna ekler. `-p tcp` protokolü, `--dport 22` hedef portu seçer. `conntrack` modülü ise paketi tek başına değerlendirmek yerine ait olduğu bağlantının durumunu inceler.

Durum bilgili filtreleme genellikle şu kuralla tamamlanır:

```bash
iptables -A INPUT -m conntrack \
  --ctstate ESTABLISHED,RELATED -j ACCEPT
```

Böylece izin verilmiş bağlantıların cevap paketleri yeniden tek tek sorgulanmadan kabul edilir. Paket hiçbir kuralla eşleşmezse zincirin varsayılan politikası uygulanır:

```bash
iptables -P INPUT DROP
```

Bu komut güçlüdür; uzaktaki sunucuda SSH kabul kuralını önce eklemezseniz dijital kapıyı kendi üzerinize kilitleyebilirsiniz.

## Öncelik ve modern Linux gerçeği

Aynı kancaya raw, conntrack, mangle, nat ve filter gibi birden fazla işlem bağlanabilir. Çekirdek bunları öncelik değerlerine göre çağırır; küçük öncelik değeri genellikle daha erken çalışır. Bu sıralama, NAT’ın rota kararından önce veya sonra uygulanabilmesini sağlar.

Modern dağıtımlarda `iptables` komutu çoğu zaman `nftables` arka ucunu kullanır. Bunu `iptables --version` ile görebilirsiniz. Arayüz değişse bile temel fikir aynıdır: paket kancaya gelir, ilgili zincirlerdeki kurallarla eşleştirilir ve `ACCEPT`, `DROP`, `REJECT` ya da yön değiştirme kararlarından biriyle yolculuğuna devam eder.

![linux-netfilter-kancalari-38](/img/linux-netfilter-kancalari-38.svg)

