---
layout: post
title: "Order Book Algoritmaları: Alış ve Satış Emirlerinden Piyasanın Yapısını Okumak"
math: true
categories: 
  - Bilgi
tags: 
  - order book
  - algoritmik işlem
  - piyasa mikro yapısı
  - python
  - finans
  - veri analizi
toc: true
image: /img/order-book-algoritmalari-36.png
---

![order-book-algoritmalari-36](/img/order-book-algoritmalari-36.svg)


Bir finansal piyasayı yalnızca son işlem fiyatından izlemek, futbol maçını sadece skor tabelasından takip etmeye benzer. Order book, yani emir defteri ise sahanın tamamını gösterir: Hangi fiyatlarda alıcılar bekliyor, satıcılar nerede yoğunlaşıyor ve likidite hangi tarafta inceliyor? Doğru algoritmalarla bu hareketli tabloyu inceleyerek piyasanın kısa vadeli yapısı hakkında değerli ipuçları çıkarabiliriz.

``

## Emir defterinin temel mantığı

Emir defteri, gerçekleşmeyi bekleyen limit alış ve satış emirlerinin fiyat seviyelerine göre sıralanmış hâlidir. En yüksek alış fiyatına **best bid**, en düşük satış fiyatına ise **best ask** denir. Bu iki fiyat arasındaki fark spread olarak tanımlanır:

$$S = P_{ask} - P_{bid}$$

Spread küçüldükçe piyasanın genellikle daha likit olduğu düşünülür. Ancak tek başına spread yeterli değildir. En iyi fiyat seviyesinde yalnızca birkaç birim emir varsa büyük bir piyasa emri fiyatı hızla kaydırabilir.

Çoğu borsada eşleştirme motoru **fiyat-zaman önceliği** kullanır. Daha iyi fiyat önceliklidir; aynı fiyattaki emirler arasında önce giren emir önce gerçekleşir. Piyasa emirleri ise beklemez, defterdeki uygun limit emirlerini tüketir.

| Gösterge | Ne anlatır? | Olası yorum |
|---|---|---|
| Dar spread | Alış ve satış fiyatları yakın | Yüksek likidite |
| Derin bid tarafı | Alış emirleri yoğun | Kısa vadeli destek ihtimali |
| İnce ask tarafı | Satış likiditesi düşük | Yukarı hareket kolaylaşabilir |
| Hızlı emir iptali | Likidite kalıcı değil | Manipülasyon riski olabilir |

## Dengesizlik ve mikro fiyat

Defter analizinin popüler ölçülerinden biri **order book imbalance** değeridir. En iyi seviyedeki alış miktarı $B$, satış miktarı $A$ olsun:

$$I = \frac{B-A}{B+A}$$

$I$ değeri $1$ seviyesine yaklaştığında alış tarafı, $-1$ seviyesine yaklaştığında satış tarafı daha ağırdır. Sıfıra yakın değerler dengeli bir görünüm sunar. Bununla birlikte büyük alış miktarı kesin yükseliş anlamına gelmez; emir gerçekleşmeden iptal edilebilir.

Bir başka ölçü olan mikro fiyat, orta noktayı mevcut miktarlarla ağırlıklandırır:

$$P_{micro} = \frac{P_{ask}B + P_{bid}A}{A+B}$$

Mikro fiyat orta fiyattan yukarıdaysa alış baskısının, aşağıdaysa satış baskısının daha güçlü olduğu düşünülebilir.

## Python ile basit analiz

Aşağıdaki fonksiyon, en iyi alış ve satış seviyelerinden spread, orta fiyat, dengesizlik ve mikro fiyat hesaplar:

```python
def book_metrics(bids, asks):
    # Her eleman: (fiyat, miktar)
    best_bid, bid_qty = max(bids, key=lambda x: x[0])
    best_ask, ask_qty = min(asks, key=lambda x: x[0])

    spread = best_ask - best_bid
    midpoint = (best_bid + best_ask) / 2
    total_qty = bid_qty + ask_qty

    imbalance = (bid_qty - ask_qty) / total_qty
    microprice = (
        best_ask * bid_qty + best_bid * ask_qty
    ) / total_qty

    return {
        'spread': spread,
        'midpoint': midpoint,
        'imbalance': imbalance,
        'microprice': microprice
    }

bids = [(99.90, 12), (99.80, 25)]
asks = [(100.00, 5), (100.10, 18)]
print(book_metrics(bids, asks))
```

Bu örnek yalnızca ilk seviyeyi inceler. Gerçek sistemlerde ilk 5, 10 veya 20 fiyat seviyesi ağırlıklı olarak değerlendirilir. Yakın seviyelere daha fazla önem vermek için $w_i=e^{-\lambda i}$ gibi azalan bir ağırlık kullanılabilir.

## Gürültü, spoofing ve doğru yorum

Order book bir niyet tablosudur; gerçekleşmiş işlemlerin kaydı değildir. Büyük bir emir güçlü destek gibi görünürken aniden iptal edilebilir. **Spoofing**, yatırımcıları yanıltmak amacıyla büyük emir gösterip bunları gerçekleşmeden kaldırma davranışıdır. Bu nedenle algoritma; emir ekleme, iptal ve gerçekleşme hızlarını birlikte izlemelidir.

Sağlam bir yaklaşım, order book verisini işlem hacmi, order flow imbalance ve fiyat değişimiyle birleştirir. Ayrıca sonuçlar farklı piyasa koşullarında geriye dönük test edilmelidir. Emir defteri geleceği söyleyen kristal küre değildir; fakat doğru ölçümlerle piyasanın kısa vadeli baskısını gösteren oldukça hassas bir radar olabilir.
