---
layout: post
title: "Linkerd ile Hafif Servis Ağı: mTLS, Yük Dengeleme ve İzleme"
math: true
categories: 
  - Proje
tags: 
  - linkerd
  - kubernetes
  - service mesh
toc: true
image: /img/linkerd-ile-hafif-30.png
---

Mikroservis mimarisinde servis sayısı arttıkça ağ trafiğini güvenli, görünür ve dayanıklı yönetmek zorlaşır. Linkerd, uygulama koduna dokunmadan servisler arasına küçük bir veri düzlemi ekleyen, Kubernetes odaklı ve kaynak tüketimi düşük bir service mesh çözümüdür. Her pod’a eklenen hafif proxy sayesinde otomatik mTLS, gecikme ölçümü, başarı oranı takibi ve akıllı yük dengeleme sunar. Ağ katmanındaki bu işleri merkezi bir altyapıya taşıdığı için geliştiriciler iş mantığına odaklanabilir.

![linkerd-ile-hafif-30](/img/linkerd-ile-hafif-30.svg)

``

## Service mesh neden gereklidir?

Klasik Kubernetes Service nesnesi, pod’lara trafik yönlendirmek için yeterlidir; ancak bağlantının şifreli olup olmadığı, hangi sürümün hata verdiği veya isteğin ne kadar sürdüğü gibi sorulara tek başına cevap vermez. Linkerd’in yaklaşımı, her uygulama konteynerinin yanına bir **sidecar proxy** yerleştirmektir. Uygulama gelen ve giden trafiği bu proxy üzerinden geçirir.

Bir isteğin toplam gecikmesini basitçe şöyle ifade edebiliriz:

$$T_{toplam} = T_{ağ} + T_{kuyruk} + T_{uygulama}$$

Linkerd, özellikle $T_{ağ}$ ve $T_{kuyruk}$ bileşenlerini gözlemleyerek yavaş veya sorunlu endpoint’leri görünür yapar. Ayrıca uç noktaları yalnızca sırayla seçmek yerine gecikme sinyallerinden yararlanır; böylece yoğun bir pod yerine daha sağlıklı olana yönelme şansı artar.

| Özellik | Sadece Kubernetes Service | Linkerd ile Service Mesh |
|---|---|---|
| Servisler arası şifreleme | Manuel TLS yapılandırması | Otomatik mTLS |
| Başarı oranı | Uygulama metriklerine bağlı | Proxy seviyesinde hazır |
| Yük dengeleme | Temel endpoint dağıtımı | Gecikme farkındalıklı seçim |
| Hata analizi | Dağınık loglar | Canlı `stat` ve dashboard |
| Kod değişikliği | Gerekebilir | Genellikle gerekmez |

## Kurulum: kontrol düzlemi ve enjeksiyon

Önce Linkerd CLI aracını kurup ön denetim yapın. Bu denetim, küme yetkileri ve Kubernetes sürümü gibi kritik noktaları daha kuruluma geçmeden yakalar.

```bash
curl -sL https://run.linkerd.io/install | sh
export PATH=$PATH:$HOME/.linkerd2/bin

linkerd check --pre
linkerd install | kubectl apply -f -
linkerd check
```

Bu komutlar kontrol düzlemini kurar. Kontrol düzlemi sertifikaları, proxy yapılandırmasını ve telemetri bileşenlerini yönetir; uygulama trafiğinin tamamını merkezi bir noktadan geçirmez. Bu ayrım, Linkerd’in hem dayanıklı hem de hafif kalmasının önemli nedenidir.

Sırada uygulama namespace’ini mesh’e dahil etmek vardır:

```bash
kubectl annotate namespace production \
  linkerd.io/inject=enabled
kubectl rollout restart deployment -n production
```

Yeni oluşturulan pod’lara `linkerd-proxy` otomatik eklenir. Enjeksiyonu tüm namespace yerine yalnızca seçili deployment’larda yapmak da mümkündür; bu, kademeli geçiş senaryolarında güvenli bir yaklaşımdır.

## mTLS ve trafik davranışını doğrulama

Linkerd, mesh içindeki proxy’ler arasında kimlik doğrulamalı ve şifreli bağlantılar kurar. Buradaki amaç yalnızca veriyi gizlemek değildir: iletişim kuran tarafın gerçekten beklenen iş yükü olduğunu doğrulamak da önemlidir. mTLS etkinliğini aşağıdaki komutla kontrol edebilirsiniz:

```bash
linkerd viz install | kubectl apply -f -
linkerd check
linkerd viz stat deploy -n production
```

`viz stat` çıktısı istek hacmi, başarı oranı, P50/P95 gecikmeleri ve TCP bağlantıları hakkında anlık bilgi verir. Örneğin P95 değeri yükselirken ortalama gecikmenin sabit kalması, az sayıdaki isteğin ciddi biçimde yavaşladığını gösterebilir. Bu nedenle yalnızca ortalamaya bakmak yerine yüzdelik değerleri izlemek daha gerçekçidir.

| Metrik | Ne anlatır? | Alarm için örnek sinyal |
|---|---|---|
| Başarı oranı | Hatasız yanıt yüzdesi | %99’un altına düşüş |
| P50 gecikme | Tipik kullanıcı deneyimi | Sürekli artış |
| P95 gecikme | Yavaş isteklerin deneyimi | Ani sıçrama |
| RPS | Saniyedeki istek | Beklenmeyen trafik artışı |

Linkerd’i üretimde başarıyla kullanmanın anahtarı, mesh’i bir sihirli değnek olarak görmemektir. Kaynak isteklerini tanımlayın, kritik servisleri önce küçük bir namespace’te deneyin ve metrikleri SLO hedefleriyle ilişkilendirin. Böylece minimal proxy maliyeti karşılığında daha şifreli, gözlemlenebilir ve dengeli bir mikroservis ağı elde edersiniz.
