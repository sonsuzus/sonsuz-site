---
layout: post
title: "BGP Yönlendirme Mantığı: İnternetin Omurgasında Yollar Nasıl Seçilir?"
math: true
categories: 
  - Bilgi
tags: 
  - bgp
  - ağ
  - internet
  - yönlendirme
  - as-path
  - networking
toc: true
---

Bir web sitesini açtığınızda paketleriniz hedefe dümdüz gitmez; farklı operatörlerin, veri merkezlerinin ve ülkelerin ağlarından geçebilir. Bu devasa trafik koreografisini yöneten temel protokollerden biri **BGP’dir (Border Gateway Protocol)**. Ancak BGP, navigasyon uygulamaları gibi yalnızca en kısa yolu aramaz. Ekonomik anlaşmaları, ağ politikalarını ve operatör tercihlerini de hesaba katar. Kısacası internette yol seçmek biraz matematik, biraz diplomasi, biraz da “bu trafiği komşuma vermeyeyim” sanatıdır.
``

## BGP’nin temel yapı taşı: Otonom Sistem

İnternet, **Otonom Sistem (Autonomous System — AS)** adı verilen bağımsız ağlardan oluşur. Her AS, bir internet servis sağlayıcısını, büyük şirketi, üniversiteyi veya bulut platformunu temsil edebilir ve kendine ait bir **ASN** numarasına sahiptir.

BGP bir **path-vector** protokolüdür. Bir yönlendirici, hedef ağın yalnızca hangi yönde olduğunu değil, o ağa ulaşırken geçilecek AS listesini de öğrenir. Örneğin:

```text
203.0.113.0/24 için yol: AS64500 AS64510 AS64520
```

Buradaki `AS_PATH`, paketin hedefe ulaşmadan önce geçeceği otonom sistemleri gösterir. Bir yönlendirici kendi ASN’sini bu listede görürse rotayı reddeder. Böylece yönlendirme döngüleri önlenir.

## En kısa yol neden her zaman kazanmaz?

Bir rota için kaba bir maliyet modeli şöyle düşünülebilir:

$$
C(r)=w_pP(r)+w_aA(r)+w_mM(r)+w_iI(r)
$$

Burada $P$ politika tercihini, $A$ AS_PATH uzunluğunu, $M$ MED değerini ve $I$ iç ağ maliyetini temsil eder. Fakat gerçek BGP uygulaması bu değerleri genellikle tek toplamda birleştirmez; özellikleri **belirli bir öncelik sırasıyla** karşılaştırır.

| Özellik | Tercih | Temel amaç |
|---|---|---|
| Weight | Yüksek değer | Cihaza özel karar vermek |
| Local Preference | Yüksek değer | AS genelinde çıkış seçmek |
| AS_PATH | Kısa liste | Daha az AS üzerinden gitmek |
| Origin | IGP, EGP, Incomplete | Rotanın kaynağını değerlendirmek |
| MED | Düşük değer | Komşuya tercih edilen girişi bildirmek |
| eBGP / iBGP | Genellikle eBGP | Dışarıdan öğrenilen yolu seçmek |
| IGP maliyeti | Düşük değer | Next-hop’a daha yakın çıkışı bulmak |

Kesin seçim sırası üreticiye ve yapılandırmaya göre değişebilir. Örneğin Cisco’ya özgü **Weight**, standart bir BGP niteliği değildir.

## Politika, mesafeden güçlüdür

Bir operatörün iki bağlantısı olduğunu düşünelim: ucuz ama yavaş bir sağlayıcı ve pahalı ama yüksek kapasiteli başka bir sağlayıcı. Kısa AS_PATH ucuz bağlantıyı gösterse bile operatör, kritik trafiği hızlı bağlantıya yönlendirmek için **Local Preference** değerini yükseltebilir.

Örneğin FRRouting üzerinde belirli bir komşudan gelen rotalara öncelik verilebilir:

```frr
route-map HIZLI-HAT permit 10
 set local-preference 200

router bgp 64500
 neighbor 192.0.2.1 remote-as 64510
 neighbor 192.0.2.1 route-map HIZLI-HAT in
```

Bu yapılandırma, `192.0.2.1` komşusundan öğrenilen rotalara `200` Local Preference atar. Varsayılan değer çoğunlukla `100` olduğundan bu yollar, diğer koşullar uygun olduğunda daha cazip hale gelir. Route-map’in gelen rotalara uygulanması, tercihin AS içindeki BGP yönlendiricilerine yayılmasını sağlar.

## MED ile giriş kapısını göstermek

**MED (Multi-Exit Discriminator)**, bir AS’nin komşusuna “trafiği mümkünse şu bağlantıdan gönder” demesidir. Düşük MED tercih edilir:

$$
MED_1 < MED_2 \Rightarrow Route_1 \text{ daha çok tercih edilir}
$$

Bununla birlikte MED çoğunlukla aynı komşu AS’den gelen yollar arasında karşılaştırılır. Ayrıca komşu ağ bu öneriyi kabul etmek zorunda değildir; BGP dünyasında MED bir emirden çok nazik bir ricadır.

## Son karar: politika tabanlı erişilebilirlik

BGP’nin amacı mutlak anlamda en hızlı rotayı bulmak değil, **politikalara uygun ve döngüsüz bir erişilebilirlik yolu** seçmektir. Bu esneklik internetin ticari olarak çalışmasını sağlar; fakat yanlış bir rota ilanı geniş çaplı kesintilere veya trafik kaçırma olaylarına yol açabilir. Bu nedenle operatörler prefix filtreleri, maksimum rota sınırları ve **RPKI** doğrulaması kullanır.

Özetle BGP, internetin trafik polisi değil, deneyimli bir diplomatıdır: yolları bilir, komşularını tanır ve her zaman kurumunun çıkarlarına göre karar verir.
