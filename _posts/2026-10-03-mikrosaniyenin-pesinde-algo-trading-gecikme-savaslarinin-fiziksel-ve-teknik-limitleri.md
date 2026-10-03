---
layout: post
title: "Mikrosaniyenin Peşinde: Algo-Trading Gecikme Savaşlarının Fiziksel ve Teknik Limitleri"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmik ticaret
  - düşük gecikme
  - kernel bypass
  - yüksek frekanslı ticaret
  - fpga
  - ağ programlama
toc: true
image: /img/mikrosaniyenin-pesinde-algo-29.png
---

![mikrosaniyenin-pesinde-algo-29](/img/mikrosaniyenin-pesinde-algo-29.svg)


Algoritmik ticarette bazen doğru tahmini yapmak yetmez; aynı tahmini rakipten birkaç mikrosaniye önce borsaya ulaştırmak gerekir. Bu nedenle yüksek frekanslı ticaret şirketleri işlemcilerden özel ağ kartlarına, veri merkezi raflarından mikrodalga kulelerine kadar uzanan pahalı bir mühendislik yarışına girer. Ancak hız sonsuz değildir: yazılım, donanım, piyasa kuralları ve ışık hızı bu yarışın duvarlarını oluşturur.
``

## Gecikme neden bu kadar önemli?

Bir emir borsaya gönderildiğinde ağ üzerinde seyahat eder, borsanın eşleştirme motoruna girer ve fiyat-zaman önceliğine göre sıraya yerleşir. Aynı fiyattan iki alış emri verilmişse önce ulaşan emir genellikle önce gerçekleşir. Dolayısıyla gecikme yalnızca “ekranın hızlı yenilenmesi” değil, doğrudan **kuyruk pozisyonu** demektir.

Basitleştirilmiş toplam gecikme modeli şöyledir:

$$L_{toplam} = L_{strateji} + L_{işletim\ sistemi} + L_{ağ} + L_{borsa}$$

Strateji kararının 8, işletim sisteminin 12, ağın 35 ve borsanın 20 mikrosaniye sürdüğü bir düzende toplam gecikme $75\ \mu s$ olur. Mühendisler her terimi küçültmeye çalışır; fakat bir noktadan sonra bir mikrosaniyelik kazanç bile olağanüstü pahalı hale gelir.

| Katman | Geleneksel yaklaşım | Düşük gecikmeli yaklaşım | Temel bedel |
|---|---|---|---|
| Coğrafya | Uzak veri merkezi | Borsaya yakın sunucu, co-location | Kira ve bağımlılık |
| Ağ | İnternet rotaları | Özel fiber veya mikrodalga | Yüksek altyapı maliyeti |
| İşletim sistemi | Standart socket API | Kernel bypass | Karmaşık geliştirme |
| Hesaplama | Genel amaçlı CPU | FPGA veya özel NIC | Esneklik kaybı |
| Yazılım | Dinamik veri yapıları | Önceden ayrılmış bellek | Bakım zorluğu |

## Coğrafya da algoritmanın parçasıdır

Veri fiber içinde yaklaşık $2 \times 10^8$ metre/saniye hızla ilerler. Tek yönlü teorik alt sınır kabaca:

$$L_{fizik} = \frac{d}{v}$$

Aralarında 1.000 kilometre bulunan iki nokta için yalnızca yayılma gecikmesi yaklaşık 5 milisaniyedir. Yönlendiriciler ve dolambaçlı fiber rotaları eklendiğinde sonuç daha da büyür. Bu yüzden şirketler borsanın eşleştirme motoruna yakın sunucu kiralar. Bazı uzun mesafelerde mikrodalga bağlantıları tercih edilir; çünkü sinyal havada fiberden daha hızlı ilerler. Buna karşılık hava koşulları, kapasite ve güvenilirlik sorunları ortaya çıkar.

## Kernel bypass neyi atlar?

Normal ağ paketleri ağ kartından çekirdeğe, oradan uygulamanın kullanıcı alanına taşınır. Sistem çağrıları, kesmeler, bağlam değişimleri ve veri kopyaları gecikme üretir. DPDK, RDMA ve benzeri yaklaşımlar uygulamanın ağ kartı kuyruklarına daha doğrudan erişmesini sağlar.

Aşağıdaki örnek gerçek bir borsa bağlantısı değildir; yoğun bekleme kullanan düşük gecikmeli döngünün mantığını gösterir:

```c
while (running) {
    int received = poll_nic_queue(packets, 32);

    for (int i = 0; i < received; i++) {
        MarketData md = decode_packet(packets[i]);

        if (md.ask < fair_value(md.symbol)) {
            Order order = build_buy_order(md.symbol, md.ask);
            send_direct(&order);
        }
    }
}
```

Burada program, işletim sisteminin kendisini uyandırmasını beklemek yerine ağ kartı kuyruğunu sürekli tarar. Bu yöntem gecikmeyi ve değişkenliği azaltabilir; ancak bir CPU çekirdeğini tamamen tüketir. Ayrıca güvenlik, sürücü yönetimi ve hata ayıklama sorumluluğunun daha büyük kısmı uygulamaya geçer.

## Kuyruklar, önbellekler ve FPGA’ler

Ortalama gecikme kadar **jitter**, yani gecikmenin ne kadar değiştiği de önemlidir. Emir bazen 10, bazen 200 mikrosaniyede gidiyorsa stratejinin davranışı öngörülemez. Bu nedenle işlemci çekirdekleri sabitlenir, güç tasarrufu durumları kapatılır, bellek önceden ayrılır ve kilitsiz veri yapıları kullanılır.

FPGA’ler piyasa verisini donanım devreleriyle işleyerek son derece düşük ve tutarlı gecikme sağlayabilir. Fakat karmaşık stratejileri güncellemek CPU tabanlı yazılıma göre daha zahmetlidir. Hız kazanılırken geliştirme çevikliği kaybedilir.

## Yarışın gerçek sınırı

Fiziksel sınır ışık hızıdır; ekonomik sınır ise kazanılan mikrosaniyenin maliyetidir. Daha hızlı sistem, yalnızca ek gelir yatırım ve işletme giderini aşıyorsa anlamlıdır:

$$Net\ Fayda = Ek\ Ticaret\ Geliri - Altyapı\ Maliyeti$$

Üstelik borsaların hız tümsekleri, toplu emir işleme yöntemleri ve adil erişim düzenlemeleri salt hız avantajını azaltabilir. Sonuçta algo-trading gecikme savaşı, “en hızlı bilgisayarı satın alma” meselesi değildir. Fizik, elektronik, ağ mühendisliği, işletim sistemleri, piyasa mikro yapısı ve ekonomi aynı denklemde buluşur. Mikrosaniyeler küçüktür; faturaları ise hiç küçük değildir.
