---
layout: post
title: "Stablecoin Teknolojisi: Dijital Paralar Fiyatını Nasıl Sabit Tutuyor?"
math: true
categories: 
  - Bilgi
tags: 
  - stablecoin
  - blockchain
  - kripto para
  - akıllı sözleşme
  - finans teknolojileri
toc: true
image: /img/stablecoin-teknolojisi-dijital-86.png
---

![stablecoin-teknolojisi-dijital-86](/img/stablecoin-teknolojisi-dijital-86.svg)


Kripto para piyasası bazen lunaparktaki hız trenine benzer: Bir anda zirveye çıkar, birkaç dakika sonra midenizi aşağıda bırakır. Stablecoin’ler ise bu hareketli ortamda daha sakin davranmayı hedefleyen dijital varlıklardır. Genellikle 1 ABD doları gibi belirli bir referans varlığa yakın fiyatla işlem görürler. Ancak bu istikrar sihirle değil; rezerv yönetimi, arbitraj, akıllı sözleşmeler ve sürekli çalışan veri sistemleriyle sağlanır.

``

## Fiyat sabitleme mantığı

Bir stablecoin’in hedef fiyatına **peg**, yani sabit kur denir. Örneğin hedef 1 dolar ise sistem şu ilişkiyi korumaya çalışır:

$$P_{coin} \approx 1\text{ USD}$$

Buradaki temel araç arz ve taleptir. Coin’in piyasa fiyatı 1,02 dolara çıktığında yeni coin üretmek ve satmak arzı artırabilir. Fiyat 0,98 dolara düştüğünde ise coin’leri dolaşımdan kaldırmak arzı azaltabilir. Basitleştirilmiş denge düşüncesi şöyledir:

$$Fiyat \propto \frac{Talep}{Arz}$$

Elbette gerçek piyasalar bundan çok daha karmaşıktır. Likidite, kullanıcı güveni, işlem ücretleri ve rezervlerin erişilebilirliği de fiyatı etkiler.

## Başlıca stablecoin modelleri

| Model | İstikrar yöntemi | Avantajı | Temel riski |
|---|---|---|---|
| İtibari para teminatlı | Bankada nakit ve tahvil rezervi | Kolay anlaşılır | Merkezi kuruma güven gerekir |
| Kripto teminatlı | Akıllı sözleşmede kilitli kripto | Zincir üzerinde şeffaflık | Teminat hızla değer kaybedebilir |
| Algoritmik | Arzı yazılımla ayarlama | Sermaye verimliliği hedefler | Güven kaybında ölüm sarmalı oluşabilir |
| Emtia teminatlı | Altın gibi fiziksel varlıklar | Reel varlığa erişim sağlar | Saklama ve denetim riski taşır |

İtibari para teminatlı modelde şirket, üretilen her coin karşılığında rezerv tuttuğunu söyler. Kullanıcı 100 dolar yatırdığında 100 stablecoin basılır; geri ödeme istediğinde coin’ler yakılır. Bu süreçte rezerv raporları ve bağımsız denetimler kritik önemdedir.

Kripto teminatlı sistemlerde ise fiyatı değişken varlıklar kullanıldığı için **aşırı teminatlandırma** gerekir. Örneğin 100 dolarlık stablecoin üretmek için 150 dolarlık kripto kilitlenebilir. Teminat oranı şöyle hesaplanır:

$$Teminat\ Oranı = \frac{Teminat\ Değeri}{Borç\ Değeri} \times 100$$

Oran güvenli seviyenin altına düşerse akıllı sözleşme teminatı otomatik olarak satar. Buna likidasyon denir.

## Akıllı sözleşmeler ne yapar?

Akıllı sözleşmeler basım, yakım ve teminat kontrolünü otomatikleştirir. Aşağıdaki basitleştirilmiş Python benzeri örnek, teminat oranını denetler:

```python
def pozisyonu_kontrol_et(teminat, borc, minimum_oran=1.5):
    oran = teminat / borc

    if oran < minimum_oran:
        return 'Likidasyon başlat'

    return 'Pozisyon güvenli'

print(pozisyonu_kontrol_et(1200, 1000))
```

Kod, teminat değerini borca böler. Sonuç yüzde 150 eşiğinin altındaysa pozisyonun kapatılması gerektiğini bildirir. Gerçek uygulamalarda bu değerler blokzincir dışındaki piyasa fiyatlarını sisteme taşıyan **oracle** ağlarından alınır.

## Arbitraj neden önemlidir?

Stablecoin 0,98 dolara düşerse yatırımcı onu ucuza satın alıp ihraççıya 1 dolar karşılığında iade edebilir. Coin başına yaklaşık 0,02 dolar kazanç oluşurken piyasadaki alım baskısı fiyatı yukarı iter. Fiyat 1,02 dolara çıktığında ise yatırımcı 1 dolardan yeni coin üretip piyasada daha pahalıya satabilir. Bu kez artan arz fiyatı aşağı çeker.

Fakat sistem yalnızca koddan ibaret değildir. Rezervlerin gerçekten var olması, oracle verilerinin manipüle edilmemesi, akıllı sözleşmelerin güvenli yazılması ve geri ödeme mekanizmasının çalışması gerekir. Kısacası stablecoin istikrarı; ekonomi, yazılım ve güven üçlüsünün ortak ürünüdür. İsimlerinde sabit geçse de risksiz değillerdir: En sağlam görünen dijital çıpanın bile düzenli denetime, yeterli likiditeye ve dayanıklı koda ihtiyacı vardır.
