---
layout: post
title: "Chord ve Kademlia: Dağıtık Hash Tablolarının Haritasız Yolculuğu"
math: true
categories: 
  - Bilgi
tags: 
  - dht
  - chord
  - kademlia
  - dağıtık-sistemler
  - algoritma
  - p2p
toc: true
image: /img/chord-ve-kademlia-71.png
---

![chord-ve-kademlia-71](/img/chord-ve-kademlia-71.svg)


Merkezi bir veritabanı olmadan milyonlarca anahtarın hangi bilgisayarda tutulduğunu bulabilir miyiz? Dağıtık Hash Tabloları, yani DHT’ler, tam olarak bu problemi çözer. Chord ve Kademlia ise aynı hedefe farklı rotalardan giden iki meşhur protokoldür: Biri düğümleri halka üzerinde yürütür, diğeri XOR uzaklığıyla dijital bir pusula kullanır.
``

## DHT nedir?

Klasik bir hash tablosunda anahtar, bir hash fonksiyonundan geçirilerek dizi konumuna dönüştürülür. DHT’de fikir benzerdir; ancak tablo tek makinede değil, ağa katılan çok sayıda düğüm arasında paylaşılır.

Bir anahtarın kimliği kabaca şöyle hesaplanır:

$$id = H(anahtar) \bmod 2^m$$

Burada $H$ bir hash fonksiyonu, $m$ ise kimlik alanındaki bit sayısıdır. Düğümler de aynı alanda kimlik alır. Böylece “kitap-42” anahtarı ile onu saklayacak bilgisayar matematiksel olarak eşleştirilebilir.

İyi bir DHT’den üç şey beklenir:

- Anahtarların düğümlere dengeli dağılması,
- Düğüm eklenip çıktığında az miktarda verinin taşınması,
- Aramanın bütün ağı dolaşmadan tamamlanması.

## Chord: Kimlik halkasında saat yönünde

Chord, $0$ ile $2^m-1$ arasındaki kimlikleri hayali bir halka üzerine yerleştirir. Bir anahtar, kimliğine saat yönünde eşit veya daha büyük ilk düğümde saklanır. Bu düğüme anahtarın **successor**’ı denir.

Her düğüm yalnızca komşusunu bilseydi arama $O(N)$ adım sürebilirdi. Chord bunun yerine **finger table** kullanır. Düğüm $n$ için tablonun $i$. girdisi yaklaşık olarak şu konumun successor’ını gösterir:

$$finger[i] = successor(n + 2^i)$$

Üstel aralıklarla oluşturulan bu kestirmeler sayesinde arama maliyeti ortalama $O(\log N)$ olur. Yeni düğümler geldiğinde `stabilize`, `notify` ve predecessor kontrolleri halkayı zamanla onarır.

## Kademlia: XOR mesafesiyle hedef avı

Kademlia’da düğüm ve anahtar kimlikleri bit dizileridir. İki kimlik arasındaki uzaklık XOR işlemiyle hesaplanır:

$$d(x,y)=x \oplus y$$

Sonuç küçükse iki kimlik birbirine yakındır. Bu metrik simetriktir ve belirli bir hedef için hangi komşunun daha iyi seçim olduğunu net biçimde gösterir.

Her düğüm, farklı uzaklık aralıklarındaki bağlantıları **k-bucket** adlı listelerde tutar. Arama sırasında hedefe en yakın bilinen birkaç düğüme paralel sorgular gönderilir. Gelen cevaplar daha yakın adaylar sağladıkça süreç tekrarlanır. Paralellik, Kademlia’yı gecikme ve geçici düğüm kayıpları karşısında oldukça pratik yapar.

| Özellik | Chord | Kademlia |
|---|---|---|
| Topoloji | Mantıksal halka | XOR tabanlı uzay |
| Yönlendirme | Finger table | k-bucket |
| Arama | Ardışık kestirmeler | Paralel, yinelemeli sorgular |
| Ortalama maliyet | $O(\log N)$ | $O(\log N)$ |
| Yaygın kullanım | Akademik DHT tasarımları | BitTorrent, IPFS benzeri P2P ağları |

## Basitleştirilmiş Kademlia araması

Aşağıdaki Python kodu, aday düğümleri hedefe olan XOR mesafesine göre sıralar. Gerçek protokol ağ istekleri, zaman aşımı ve bucket güncellemeleri de içerir.

```python
def xor_distance(node_id, target_id):
    # İki kimlik arasındaki Kademlia mesafesini hesaplar.
    return node_id ^ target_id


def closest_nodes(nodes, target_id, count=3):
    # Hedefe en yakın düğümleri seçerek sorgu adaylarını üretir.
    return sorted(
        nodes,
        key=lambda node: xor_distance(node, target_id)
    )[:count]

nodes = [5, 12, 19, 27, 31]
print(closest_nodes(nodes, target_id=18))
```

## Hangisi ne zaman?

Chord, halka modeli sayesinde anlatılması ve doğrulanması kolay, zarif bir tasarımdır. Kademlia ise paralel sorguları, arızalara dayanıklı bucket yapısı ve XOR metriği nedeniyle gerçek P2P uygulamalarında daha sık karşımıza çıkar. İkisinin ortak sihri, herkesin herkesi tanımasına gerek bırakmamalarıdır: Her düğüm yalnızca sınırlı sayıda bağlantı tutar, fakat doğru matematik sayesinde devasa ağlarda bile hedefini birkaç sıçramada bulur.
