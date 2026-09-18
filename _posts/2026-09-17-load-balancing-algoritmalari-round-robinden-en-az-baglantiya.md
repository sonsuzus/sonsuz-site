---
layout: post
title: "Load Balancing Algoritmaları: Round Robin’den En Az Bağlantıya"
math: true
categories: 
  - Bilgi
tags: 
  - load balancing
  - round robin
  - least connections
  - dağıtık sistemler
  - yüksek erişilebilirlik
  - backend
toc: true
image: /img/load-balancing-algoritmalari-67.png
---

Bir uygulama büyüdüğünde tek bir sunucu, gelen isteklerin ağırlığı altında terlemeye başlayabilir. Load balancer, bu noktada trafiği birden fazla sunucuya dağıtan akıllı bir trafik polisi gibi çalışır. Fakat bütün trafik polisleri aynı yöntemi kullanmaz: bazıları sırayla yönlendirir, bazıları sunucuların gücünü hesaba katar, bazılarıysa o anda en az meşgul olanı seçer.

``

## Load balancing neden gereklidir?

Bir sisteme saniyede $R$ adet istek geliyor ve sistemde $N$ eş kapasiteli sunucu bulunuyorsa ideal durumda her sunucunun yükü yaklaşık olarak şöyledir:

$$L_i = R / N$$

Örneğin saniyede 900 istek alan üç sunuculu bir sistemde hedef, her sunucuya yaklaşık 300 istek göndermektir. Gerçek hayatta ise isteklerin çalışma süreleri, sunucu kapasiteleri ve ağ gecikmeleri aynı değildir. Bu nedenle yalnızca istek sayısını eşitlemek her zaman gerçek yükü eşitlemez.

Load balancer ayrıca sağlık kontrolleri yapabilir. Yanıt vermeyen bir sunucu havuzdan çıkarılır; iyileştiğinde yeniden trafiğe dahil edilir. Böylece hem ölçeklenebilirlik hem de yüksek erişilebilirlik sağlanır.

## Temel algoritmaların karşılaştırması

| Algoritma | Karar ölçütü | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Round Robin | Sıradaki sunucu | Basit ve hızlıdır | İstek sürelerini önemsemez |
| Weighted Round Robin | Sunucu ağırlığı | Farklı kapasiteleri destekler | Anlık yoğunluğu göremez |
| Least Connections | Aktif bağlantı sayısı | Uzun bağlantılarda etkilidir | Bağlantı maliyetlerini eşit varsayabilir |
| Weighted Least Connections | Bağlantı ve kapasite | Heterojen sistemlere uygundur | Daha fazla ölçüm gerektirir |
| IP Hash | İstemci IP adresi | Oturum sürekliliği sağlar | Dağılım dengesiz olabilir |

![load-balancing-algoritmalari-67](/img/load-balancing-algoritmalari-67.svg)


## Round Robin: herkes sırasını beklesin

Round Robin, istekleri sunuculara döngüsel biçimde gönderir. Üç sunucu varsa sıra A, B, C, A, B, C şeklinde ilerler. Zaman karmaşıklığı $O(1)$ düzeyindedir; yani seçim son derece ucuzdur.

```python
class RoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.index = 0

    def select(self):
        server = self.servers[self.index]
        self.index = (self.index + 1) % len(self.servers)
        return server
```

Bu kod, mevcut indeksteki sunucuyu seçer ve mod işlemiyle listenin başına döner. Sunucular benzer donanıma sahipse ve istekler yaklaşık aynı sürede tamamlanıyorsa oldukça başarılıdır. Ancak bir istek 20 milisaniye, diğeri 20 saniye sürüyorsa sıra adil görünse bile iş yükü adil değildir.

## Weighted Round Robin: güçlü sunucu daha çok çalışsın

Her sunucuya kapasitesini temsil eden bir ağırlık atanır. A sunucusunun ağırlığı 3, B sunucusunun ağırlığı 1 ise uzun vadede trafik oranı yaklaşık $3:1$ olur. Genel seçim payı şu şekilde düşünülebilir:

$$P_i = w_i / \sum_j w_j$$

Bu yöntem, farklı işlemci veya bellek kapasitesine sahip sunucuların bulunduğu havuzlarda kullanışlıdır. Yine de ağırlıklar statikse ani CPU yükselişlerine tepki veremez.

## Least Connections: en sakin kasaya ilerleyin

Least Connections, yeni isteği aktif bağlantı sayısı en düşük sunucuya yollar. Mantığı, markette en kısa kuyruğu seçmeye benzer:

```python
def select_least_connected(servers):
    healthy = [s for s in servers if s.is_healthy]
    if not healthy:
        raise RuntimeError('Kullanılabilir sunucu yok')
    return min(healthy, key=lambda s: s.active_connections)
```

Bu yaklaşım WebSocket, dosya aktarımı ve uzun süren API çağrılarında Round Robin’den daha dengeli sonuç verebilir. Seçim basit taramayla $O(N)$ maliyetindedir; büyük havuzlarda öncelik kuyruğu gibi veri yapıları kullanılabilir.

Weighted Least Connections sürümünde bağlantı sayısı kapasiteye bölünür:

$$S_i = c_i / w_i$$

Burada $c_i$ aktif bağlantı, $w_i$ kapasite ağırlığıdır. En düşük $S_i$ değerine sahip sunucu seçilir.

## Hangisini seçmeli?

Eş sunucular ve kısa istekler için Round Robin iyi bir başlangıçtır. Donanımlar farklıysa Weighted Round Robin, bağlantılar uzun ömürlüyse Least Connections daha mantıklıdır. Oturumun aynı sunucuda kalması gerekiyorsa IP Hash düşünülebilir; ancak mümkünse oturum verisini Redis gibi ortak bir depoya taşımak daha esnek ölçekleme sağlar.

En iyi algoritma, en karmaşık olan değil; ölçülen trafik davranışına en uygun olandır. Gecikme, hata oranı, aktif bağlantı ve CPU kullanımı izlenmeden yapılan seçim, karanlıkta dart atmaya benzer.
