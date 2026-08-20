---
layout: post
title: "Yük Dengeleme Algoritmaları: Round-Robin ve En Az Bağlantı Stratejileri"
math: true
categories: 
  - Bilgi
tags: 
  - yük dengeleme
  - round-robin
  - sunucu mimarisi
toc: true
---

Bir uygulama tek bir sunucuda kusursuz çalışabilir; ancak kullanıcı sayısı arttığında aynı sunucu, yoğun saatlerde dar boğaza dönüşebilir. Yük dengeleme (load balancing), gelen istekleri birden fazla sunucuya akıllıca dağıtarak performansı, erişilebilirliği ve hata toleransını yükselten mimari yaklaşımdır. Buradaki kritik soru şudur: Yeni gelen isteği hangi sunucu karşılamalıdır?
``

Yük dengeleyici, istemci ile uygulama sunucuları arasında duran bir trafik yöneticisidir. İstekleri karşılayan sunucu kümesine **backend pool** denir. Dengeleyici; HTTP isteği, TCP bağlantısı, kaynak IP adresi ya da coğrafi konum gibi sinyallere bakarak karar verebilir. İdeal durumda hiçbir sunucu gereksiz yere beklemezken, diğerleri aşırı yük altında kalmaz.

Temel kapasite fikri basitçe şöyle ifade edilebilir. Toplam istek hızı $\lambda$, her sunucunun işleme kapasitesi $\mu$ ve sunucu sayısı $n$ ise sistemin kararlı kalması için kabaca şu koşul hedeflenir:

$$\lambda < n \cdot \mu$$

Bu formül tek başına yeterli değildir; çünkü isteklerin maliyetleri farklı olabilir. Bir sunucuya gelen kısa API sorgusu ile uzun süren rapor üretimi aynı kaynak tüketimini yapmaz. Algoritma seçiminin önemi tam da burada ortaya çıkar.

## Round-Robin: Sıradaki Sunucu Sahneye

**Round-robin**, sunucuları sabit bir sırayla dolaşır. Üç sunuculuk bir kümede istekler sırasıyla A, B, C, A, B, C şeklinde yönlendirilir. Uygulaması son derece kolaydır ve tüm sunucuların benzer kapasitede, isteklerin de yaklaşık eşit maliyette olduğu sistemlerde başarılı sonuç verir.

```python
servers = ["api-1", "api-2", "api-3"]
current = 0

def select_server():
    global current
    server = servers[current]
    current = (current + 1) % len(servers)
    return server
```

Bu örnekte `current` indeksi her istekte ilerler; mod alma işlemi listenin sonuna gelince tekrar ilk sunucuya dönülmesini sağlar. Gerçek dünyada eşzamanlı istekler nedeniyle bu sayacın thread-safe olması gerekir.

## En Az Bağlantı: Meşgul Olanı Rahat Bırak

**Least Connections** algoritması, aktif bağlantı sayısı en düşük olan sunucuyu seçer. Özellikle WebSocket, dosya indirme veya uzun süren sorgular gibi bağlantı sürelerinin değişken olduğu işlerde round-robin'e göre daha dengeli davranır. Her yeni bağlantıda sayaç artırılır, bağlantı sona erdiğinde azaltılır.

| Özellik | Round-Robin | En Az Bağlantı |
|---|---|---|
| Karar mekanizması | Sıradaki sunucuyu seçer | En az aktif bağlantılı sunucuyu seçer |
| Durum takibi | Gerekmez | Bağlantı sayaçları gerekir |
| En iyi kullanım | Benzer süreli, stateless istekler | Uzun ve değişken süreli bağlantılar |
| Uygulama maliyeti | Çok düşük | Orta düzey |
| Risk | Ağır istekler eşitsizlik yaratabilir | Bağlantı sayısı gerçek CPU yükünü yansıtmayabilir |

Örneğin A sunucusunda 2, B'de 7, C'de 4 aktif bağlantı varsa yeni istek A'ya gider. Fakat iki bağlantı sayısı az olsa bile A'nın CPU'su yoğun bir veri işleme görevi yüzünden %95 kullanımdaysa, yalnızca bağlantı sayısına bakmak yanıltıcı olabilir.

## Ağırlıklı Seçenekler ve Sağlık Kontrolleri

Sunucular eşit güçte değilse **Weighted Round-Robin** kullanılabilir. Kapasitesi iki kat olan bir sunucuya ağırlık $w=2$, diğerlerine $w=1$ verilirse, dağıtım oranı yaklaşık olarak ağırlıklarla orantılı olur:

$$P_i = \frac{w_i}{\sum_{j=1}^{n} w_j}$$

Bunun yanında her yük dengeleme çözümü sağlık kontrolü yapmalıdır. Belirli aralıklarla `/health` gibi bir uç noktaya istek atılır; başarısız veya yavaş yanıt veren düğümler havuzdan geçici olarak çıkarılır. Böylece algoritma ne kadar iyi olursa olsun çökmüş bir sunucuya trafik gönderilmez.

Doğru seçim, uygulamanın davranışına bağlıdır. Kısa REST çağrıları için round-robin güçlü bir başlangıçtır. Uzun ömürlü bağlantılar için least connections daha mantıklıdır. CPU, bellek ve gecikme gibi metriklerin önemli olduğu karmaşık platformlarda ise dinamik ağırlıklar ve gözlemlenebilirlik araçlarıyla desteklenen hibrit stratejiler en sağlıklı sonucu verir.
