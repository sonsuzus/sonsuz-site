---
layout: post
title: "Şehir İçi Atık Yönetiminde Rota Optimizasyonu Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - rota optimizasyonu
  - atık yönetimi
  - graf algoritmaları
  - python
  - akıllı şehirler
  - operasyon araştırması
toc: true
image: /img/sehir-ici-atik-75.png
---

Bir çöp kamyonunun sabah belediye garajından çıkıp gelişigüzel sokaklarda dolaştığını düşünün. Sonuç; fazla yakıt tüketimi, taşan konteynerler, gereksiz karbon salımı ve uzayan çalışma saatleri olurdu. Modern atık yönetimi sistemleri bu karmaşayı önlemek için şehir haritasını matematiksel bir probleme dönüştürür. Araçların hangi konteynerleri, hangi sırayla ve hangi yolları kullanarak ziyaret edeceği rota optimizasyonu algoritmalarıyla belirlenir.

![sehir-ici-atik-75](/img/sehir-ici-atik-75.svg)

``
## Şehri Bir Graf Olarak Düşünmek

Rota optimizasyonunun temelinde **graf teorisi** bulunur. Şehirdeki kavşaklar, garajlar ve konteyner noktaları birer düğüm; yollar ise bu düğümleri bağlayan kenarlar olarak modellenir. Her kenara mesafe, tahmini yolculuk süresi veya yakıt tüketimi gibi bir maliyet atanır.

Bir yol ağını $G=(V,E)$ biçiminde gösterebiliriz. Burada $V$ düğümleri, $E$ ise yolları temsil eder. İki nokta arasındaki en ucuz güzergahın maliyeti şu şekilde ifade edilebilir:

$$d(s,t)=\min_{p \in P(s,t)} \sum_{e \in p} w(e)$$

Buradaki $P(s,t)$, başlangıç ile hedef arasındaki olası yolları; $w(e)$ ise yolun maliyetini belirtir. Dijkstra ve A* gibi algoritmalar bu en kısa yol hesaplamasında sıkça kullanılır.

| Yaklaşım | Amaç | Atık yönetimindeki kullanımı |
|---|---|---|
| Dijkstra | En düşük maliyetli yolu bulmak | İki konteyner arasındaki güzergah |
| A* | Sezgisel bilgiyle aramayı hızlandırmak | Büyük şehir haritalarında hızlı yönlendirme |
| Çinli Postacı | Gerekli yol parçalarını kapsamak | Sokak bazlı toplama operasyonları |
| CVRP | Kapasiteli araç rotaları oluşturmak | Birden fazla kamyon ve konteyner planlaması |

## Sadece En Kısa Yol Yetmez

Gerçek dünyada hedef yalnızca kilometreyi azaltmak değildir. Bir kamyonun kapasitesi, konteynerlerin doluluk oranı, trafik, vardiya süresi ve atık tesisinin çalışma saatleri de hesaba katılmalıdır. Bu problem genellikle **Kapasiteli Araç Rotalama Problemi**, yani CVRP olarak modellenir.

Toplam maliyet kabaca şöyle yazılabilir:

$$C = \alpha D + \beta T + \gamma F + \delta P$$

Burada $D$ toplam mesafe, $T$ süre, $F$ yakıt tüketimi ve $P$ gecikme cezasıdır. Katsayılar belediyenin önceliklerini temsil eder. Örneğin karbon salımını azaltmak isteyen bir yönetim, yakıt katsayısı olan $\gamma$ değerini yükseltebilir.

## Basit Bir Sezgisel Algoritma

Araç rotalama problemleri, durak sayısı arttıkça çok hızlı biçimde zorlaşır. Bu nedenle her olasılığı denemek yerine açgözlü algoritmalar, genetik algoritmalar, tabu araması veya karınca kolonisi optimizasyonu gibi sezgisel yöntemlerden yararlanılır.

Aşağıdaki Python örneği, aracın kapasitesini aşmadan kendisine en yakın uygun konteyneri seçer:

```python
from math import hypot

def mesafe(a, b):
    return hypot(a[0] - b[0], a[1] - b[1])

def rota_olustur(depo, konteynerler, kapasite):
    rota = [depo]
    konum = depo
    kalan = konteynerler.copy()
    yuk = 0

    while kalan:
        uygunlar = [k for k in kalan if yuk + k[2] <= kapasite]

        if not uygunlar:
            rota.append(depo)
            konum, yuk = depo, 0
            continue

        secilen = min(uygunlar, key=lambda k: mesafe(konum, k))
        rota.append(secilen)
        konum = secilen
        yuk += secilen[2]
        kalan.remove(secilen)

    rota.append(depo)
    return rota
```

Her konteyner `(x, y, atık_miktarı)` biçiminde tutulur. Algoritma anlaşılır ve hızlıdır; ancak en yakın noktayı seçmek her zaman küresel olarak en iyi rotayı üretmez. Bu nedenle sonuç, 2-opt gibi yerel iyileştirme yöntemleriyle geliştirilebilir.

## Dinamik ve Akıllı Rotalar

Güncel sistemlerde konteynerlere yerleştirilen IoT sensörleri doluluk oranını merkeze iletir. Yalnızca belirli bir eşiği aşan konteynerler plana eklenir. Trafik API’leri yol maliyetlerini güncellerken GPS verileri aracın rotadan sapıp sapmadığını gösterir.

Böylece rota, sabah bir kez hazırlanıp unutulan sabit bir liste olmaktan çıkar. Yol kapanması, arıza veya beklenmedik doluluk durumunda yeniden hesaplanabilir. İyi tasarlanmış bir optimizasyon sistemi; daha az kilometre, düşük işletme maliyeti, daha temiz sokaklar ve daha küçük bir karbon ayak izi sağlar. Kısacası çöp kamyonunun arkasında yalnızca atık değil, oldukça ciddi bir matematik de taşınır!
