---
layout: post
title: "Docker Bridge, Overlay ve Macvlan: Konteyner İletişimini Deneyle Karşılaştır"
math: true
categories: 
  - Bilgi
tags: 
  - docker
  - ağ
  - konteyner
  - devops
  - linux
toc: true
---

Docker’da ağ sürücüsü seçmek, sadece konteynerlere IP dağıtmak değildir; erişim sınırlarını, servis keşfini, gecikmeyi ve altyapının ölçeklenme biçimini belirler. Aynı uygulamanın yerel bir makinede, çok düğümlü bir kümede veya fiziksel ağda görünür olması gerektiğinde farklı sürücüler anlam kazanır. Bu yazıda `bridge`, `overlay` ve `macvlan` sürücülerini küçük ama tekrarlanabilir deneylerle karşılaştıralım.

``

## Önce ağ modelini zihinde oturtalım

Bir konteynerin başka bir konteynere paket göndermesi kabaca şu zinciri izler: uygulama → ağ arayüzü → Docker ağ sürücüsü → Linux çekirdeği/yönlendirme → hedef arayüz. Sürücü, bu yolun hangi bölümünde sanallaştırma veya kapsülleme yapılacağını belirler.

| Sürücü | Temel çalışma alanı | Tipik kullanım | Dikkat edilmesi gereken nokta |
|---|---|---|---|
| `bridge` | Tek Docker ana makinesi | Yerel geliştirme, küçük servisler | Ana makineler arasında doğrudan çalışmaz |
| `overlay` | Birden fazla Docker düğümü | Swarm ve dağıtık servisler | Kapsülleme nedeniyle ek ağ maliyeti vardır |
| `macvlan` | Fiziksel LAN | Eski sistemler, LAN’da ayrı IP isteyen servisler | Ağ anahtarı ve ana makine erişimi özel ayar isteyebilir |

Teorik olarak paket gecikmesini şöyle düşünebiliriz: $T_{toplam} = T_{uygulama} + T_{çekirdek} + T_{ağ} + T_{enkapsülasyon}$. `bridge` çoğu zaman düşük $T_{enkapsülasyon}$ ile çalışır. Overlay, düğümler arası paketi taşıyabilmek için genellikle VXLAN kapsüllemesi ekler. Macvlan ise konteynere fiziksel ağa aitmiş gibi ayrı bir MAC adresi verir.

## 1. Bridge: yerel laboratuvarın hızlı seçeneği

Önce kullanıcı tanımlı bir bridge ağı oluşturalım. Kullanıcı tanımlı ağlar, konteyner adlarıyla DNS çözümlemesi sunduğu için varsayılan `bridge` ağından daha kullanışlıdır.

```bash
docker network create app-net

docker run -d --name api --network app-net nginx:alpine
docker run -it --rm --network app-net busybox sh
```

İkinci terminalde açılan BusyBox kabında şu komutu çalıştırın:

```bash
ping -c 3 api
wget -qO- http://api
```

`api` adının IP’ye çözülmesi, Docker’ın bu ağ için sağladığı yerleşik DNS davranışını gösterir. Aynı ağdaki konteynerler birbirine erişirken, başka bir bridge ağındaki konteynerler varsayılan olarak erişemez. Bu izolasyon, mikroservislerde veritabanını yalnızca backend’e açmak için oldukça değerlidir.

## 2. Overlay: düğümler arasına görünmez tünel

Overlay deneyi için Docker Swarm etkin iki düğüm gerekir. Yönetici düğümünde Swarm’ı başlatıp diğer düğümü `docker swarm join` çıktısındaki komutla kümeye katın. Ardından şifreli bir overlay ağ oluşturun:

```bash
docker swarm init
docker network create -d overlay --attachable --opt encrypted cluster-net

docker service create --name web --network cluster-net --replicas 2 nginx:alpine
docker service ls
```

Replikaları farklı düğümlere dağıttığınızda servis, tek bir mantıksal ağdaymış gibi davranır. Overlay sürücüsü paketleri düğümler arasında VXLAN ile taşır; `--opt encrypted` seçeneği ise taşıma katmanında ek koruma sağlar. Bunun bedeli CPU kullanımı ve küçük bir gecikme artışıdır. Özellikle yüksek paket sayısında MTU uyumsuzluğu parçalanma sorunları doğurabilir; fiziksel ağın MTU değeri kontrol edilmelidir.

## 3. Macvlan: konteyneri LAN’ın gerçek sakini yapın

Macvlan, her konteynere fiziksel ağınızdan bir IP ve benzersiz MAC adresi verir. Örneğin ana makinenin dış arayüzü `eth0`, LAN ağınız `192.168.1.0/24` ise:

```bash
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 lan-net

docker run -it --rm --network lan-net --ip 192.168.1.220 busybox sh
```

Bu konteyner, LAN’daki diğer cihazlar tarafından bağımsız bir cihaz gibi görülür. Ancak yaygın bir sürpriz vardır: ana makine, macvlan alt arayüzü oluşturmadan kendi macvlan konteynerine erişemeyebilir. Ayrıca switch portu çok sayıda MAC adresini kabul etmiyorsa bağlantı başarısız olabilir.

## Deney sonuçlarını nasıl yorumlamalı?

İletişimi `ping`, HTTP isteği ve `iperf3` ile ölçebilirsiniz. Ölçümde yalnızca ortalamaya değil, $p95$ gecikmesine de bakın; kullanıcı deneyimini çoğu zaman uç değerler bozar.

| Ölçüt | Bridge | Overlay | Macvlan |
|---|---|---|---|
| Servis adıyla keşif | Evet | Evet | Genellikle harici DNS gerekir |
| Çok düğüm desteği | Hayır | Evet | Fiziksel ağ tasarımına bağlı |
| LAN’dan doğrudan görünürlük | Port yayınlama ile | Ingress veya yayınlama ile | Evet |
| Operasyonel karmaşıklık | Düşük | Orta-yüksek | Orta-yüksek |

Özetle, tek sunuculu uygulamalarda bridge güvenli ve pratik başlangıçtır. Dağıtık Docker servislerinde overlay, ağ topolojisini uygulamadan gizler. Konteynerin mevcut LAN’da bağımsız bir cihaz olması şartsa macvlan güçlüdür; fakat IP planı, switch politikaları ve ana makine erişimi önceden test edilmelidir.
