---
layout: post
title: "Gezgin Satıcı Problemi: Açgözlü Algoritmalarla Kısa Yolu Aramak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - tsp
  - np-zor
  - açgözlü-algoritma
  - en-yakın-komşu
  - optimizasyon
  - python
toc: true
image: /img/gezgin-satici-problemi-93.png
---

![gezgin-satici-problemi-93](/img/gezgin-satici-problemi-93.svg)


Bir satıcının ziyaret etmesi gereken şehirler, sınırlı yakıtı ve eve dönmeden önce yetişmesi gereken bir akşam yemeği olduğunu düşünün. Amaç, her şehre tam bir kez uğrayıp başlangıç noktasına dönen en kısa rotayı bulmaktır. Gezgin Satıcı Problemi, yani TSP, basit görünen kurallarının altında devasa bir arama uzayı saklayan klasik bir optimizasyon problemidir.

``

## TSP neden bu kadar zor?

Şehirleri düğüm, aralarındaki yolları da ağırlıklı kenar olarak gösterirsek problem bir grafik üzerinde tanımlanabilir. $n$ şehir için turun toplam maliyeti şöyle yazılır:

$$C(\pi)=\sum_{i=1}^{n-1} d(\pi_i,\pi_{i+1})+d(\pi_n,\pi_1)$$

Burada $\pi$, şehirlerin ziyaret sırasını; $d(a,b)$ ise iki şehir arasındaki uzaklığı temsil eder. Aradığımız sonuç, bütün olası sıralamalar içindeki minimum değerdir:

$$C^*=\min_{\pi} C(\pi)$$

Simetrik uzaklıklarda başlangıç ve yön tekrarları elendiğinde bile yaklaşık $(n-1)!/2$ farklı tur bulunur. Yalnızca 20 şehir için seçenek sayısı astronomik seviyeye çıkar. TSP'nin karar sürümü NP-tam, optimizasyon sürümü ise NP-zordur. Bu nedenle büyük girdilerde bütün turları denemek yerine hızlı ve yeterince iyi yaklaşık çözümler kullanılır.

| Yaklaşım | Temel fikir | Hız | Sonuç kalitesi |
|---|---|---:|---|
| Kaba kuvvet | Bütün turları dener | Çok düşük | Kesin optimum |
| Dinamik programlama | Alt problem sonuçlarını saklar | Düşük | Kesin optimum |
| En yakın komşu | Her adımda en yakın şehri seçer | Yüksek | Başlangıca bağlı |
| Çoklu başlangıç + 2-opt | Birkaç tur üretip iyileştirir | Orta | Genellikle daha iyi |

## Açgözlü düşünce ve en yakın komşu

Açgözlü algoritmalar, gelecekte oluşabilecek etkileri kapsamlı biçimde hesaplamadan o an en avantajlı seçimi yapar. TSP için en bilinen açgözlü yöntem **en yakın komşu algoritmasıdır**:

1. Bir başlangıç şehri seç.
2. Ziyaret edilmemiş en yakın şehre git.
3. Bütün şehirler bitene kadar işlemi tekrarla.
4. Başlangıç şehrine dön.

Bu strateji hızlıdır; ancak kısa adımların toplamı her zaman en kısa tur değildir. Algoritma ucuz yolları erkenden tüketip sona birbirinden çok uzak iki şehir bırakabilir. Başka bir deyişle, yerel olarak iyi karar küresel olarak kötü olabilir.

Aşağıdaki Python kodu uzaklık matrisi üzerinde yöntemi uygular:

```python
def nearest_neighbor(distances, start=0):
    n = len(distances)
    unvisited = set(range(n))
    unvisited.remove(start)
    route = [start]
    total = 0
    current = start

    while unvisited:
        next_city = min(
            unvisited,
            key=lambda city: distances[current][city]
        )
        total += distances[current][next_city]
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    total += distances[current][start]
    route.append(start)
    return route, total
```

`unvisited` henüz gidilmeyen şehirleri tutar. `min` işlemi mevcut konuma en yakın şehri seçer. Bu seçim her şehir için en fazla $O(n)$ karşılaştırma yaptığından toplam zaman karmaşıklığı $O(n^2)$, ek bellek ihtiyacı ise $O(n)$ olur.

## Sonucu biraz daha akıllandırmak

Başlangıç şehri sonucu ciddi biçimde değiştirebilir. Bu nedenle algoritmayı her şehirden başlatıp en kısa turu seçmek, **çoklu başlangıç** adı verilen pratik bir iyileştirmedir. Ardından 2-opt uygulanabilir: Turdaki iki kenar kaldırılır, aradaki rota ters çevrilir ve toplam mesafe azalıyorsa değişiklik korunur.

Örneğin $(A,B)$ ve $(C,D)$ kenarları için şu karşılaştırma yapılır:

$$d(A,C)+d(B,D) < d(A,B)+d(C,D)$$

Eşitsizlik doğruysa kenarlar değiştirilerek gereksiz çaprazlaşmalar giderilebilir. Böylece en yakın komşunun hızlı başlangıcı, yerel aramanın düzeltme yeteneğiyle birleşir.

TSP bize önemli bir algoritma dersi verir: Kusursuz çözüm her zaman pratik çözüm değildir. Navigasyon, lojistik, robot rotalama ve devre tasarımı gibi alanlarda birkaç saniyede bulunan kaliteli bir tur, yıllarca beklenecek optimum turdan çok daha değerlidir.
