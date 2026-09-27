---
layout: post
title: "eBPF ile Çekirdeği Yeniden Derlemeden Ağ Paketlerini Manipüle Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - ebpf
  - linux
  - xdp
  - ağ güvenliği
  - paket işleme
  - gözlemlenebilirlik
toc: true
image: /img/ebpf-ile-cekirdegi-78.png
---

Linux ağ yığınında paketleri yakalamak, filtrelemek veya yönlendirmek eskiden çekirdek modülü geliştirmeyi ve bazen çekirdeği yeniden derlemeyi gerektiriyordu. eBPF sayesinde artık doğrulanmış küçük programları çekirdek içinde güvenli biçimde çalıştırabiliyoruz. Böylece DDoS filtrelerinden gecikme ölçümüne kadar pek çok işi, kaynak koduna neşter vurmadan gerçekleştirmek mümkün.

``

## eBPF tam olarak nedir?

eBPF, kullanıcı alanında hazırlanan programların Linux çekirdeğindeki belirli kancalara yüklenmesini sağlayan bir çalışma ortamıdır. İsmindeki BPF, tarihsel olarak “Berkeley Packet Filter” anlamına gelse de teknoloji bugün ağ paketlerinin çok ötesine uzanır: sistem çağrıları, süreçler, dosya erişimleri ve performans olayları da izlenebilir.

“Çekirdeğe dokunmadan” ifadesi, kodun çekirdek dışında çalıştığı anlamına gelmez. eBPF programı çekirdek bağlamında çalışır; ancak çekirdek kaynak kodunu değiştirmeye veya özel bir modül yüklemeye gerek bırakmaz. Program yüklenmeden önce **verifier** tarafından incelenir. Geçersiz bellek erişimi, güvensiz işaretçi kullanımı veya sonlanmama riski varsa program reddedilir.

| Yaklaşım | Çalışma noktası | Performans | Risk ve esneklik |
|---|---|---:|---|
| Kullanıcı alanı yakalama | Ağ yığınından sonra | Orta | Güvenli, kopyalama maliyetli |
| Netfilter/iptables | Çekirdek ağ yığını | Yüksek | Kurallarla sınırlı |
| Çekirdek modülü | Çekirdek içinde | Çok yüksek | Hata tüm sistemi etkileyebilir |
| eBPF/XDP | Sürücüye çok yakın | Çok yüksek | Verifier ile denetimli |

## XDP neden bu kadar hızlı?

XDP, yani **eXpress Data Path**, paketi ağ sürücüsünden gelir gelmez işleyebilir. Paket henüz `sk_buff` yapısına dönüştürülmeden karar verildiği için ayırma, kopyalama ve ağ yığını maliyetleri azaltılır.

Bir paketin yaklaşık işlem maliyetini şöyle düşünebiliriz:

$$T_{toplam} = T_{alma} + T_{ayrıştırma} + T_{karar} + T_{yönlendirme}$$

XDP özellikle $T_{ayrıştırma}$ ve $T_{yönlendirme}$ bileşenlerini küçültür. Program paketi kabul etmek için `XDP_PASS`, düşürmek için `XDP_DROP`, başka arayüze göndermek için `XDP_REDIRECT` döndürebilir.

Aşağıdaki orta düzey örnek, IPv4 UDP paketlerini erken aşamada düşürür:

```c
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/udp.h>
#include <bpf/bpf_helpers.h>

SEC("xdp")
int drop_udp(struct xdp_md *ctx)
{
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;
    struct ethhdr *eth = data;

    if ((void *)(eth + 1) > data_end)
        return XDP_ABORTED;

    if (eth->h_proto != __constant_htons(ETH_P_IP))
        return XDP_PASS;

    struct iphdr *ip = (void *)(eth + 1);
    if ((void *)(ip + 1) > data_end)
        return XDP_ABORTED;

    return ip->protocol == IPPROTO_UDP ? XDP_DROP : XDP_PASS;
}

char LICENSE[] SEC("license") = "GPL";
```

Sınır kontrolleri yalnızca iyi programlama alışkanlığı değildir; verifier, `data_end` kontrolü bulunmayan paket erişimini kabul etmez. Kod Clang ile eBPF bytecode’una çevrilip bir arayüze bağlanabilir:

```bash
clang -O2 -g -target bpf -c filter.c -o filter.o
sudo ip link set dev eth0 xdp obj filter.o sec xdp
sudo ip link set dev eth0 xdp off
```

İlk komut programı derler, ikincisi `eth0` arayüzüne yükler, sonuncusu ise bağlantıyı kaldırır. Uzaktan bağlı bir sunucuda bütün UDP trafiğini düşürmeden önce DNS ve VPN kullanımını düşünmek iyi fikirdir; aksi hâlde güvenlik demosu hızla bağlantı kesme demosuna dönüşebilir.

## Haritalar ve gözlemlenebilirlik

eBPF haritaları, çekirdek ve kullanıcı alanı arasında paylaşılan anahtar-değer depolarıdır. IP başına paket sayacı tutmak, engelli adresleri dinamik olarak güncellemek veya CPU başına istatistik toplamak için kullanılabilirler. Üretimde C ile doğrudan uğraşmak yerine libbpf, BCC, bpftrace, Cilium ve Rust tabanlı Aya gibi araçlardan yararlanılabilir.

TC kancaları paket değişikliği ve trafik şekillendirme konusunda daha esnekken XDP mümkün olan en erken kararı hedefler. Sonuç olarak eBPF, klasik çekirdek modüllerinin bütün risklerini üstlenmeden çekirdek hızına yaklaşan, programlanabilir bir ağ güvenliği ve izleme katmanı sunar.

![ebpf-ile-cekirdegi-78](/img/ebpf-ile-cekirdegi-78.svg)

