---
layout: post
title: "Boyer-Moore Algoritması: Metni Sondan Başlayarak Akıllıca Aramak"
math: true
categories: 
  - Bilgi
tags: 
  - boyer-moore
  - algoritma
  - metin-arama
  - python
  - dizgi
  - veri-yapıları
toc: true
image: /img/boyer-moore-algoritmasi-21.png
---

Bir metin içinde kelime ararken her karakteri sırayla karşılaştırmak güvenilir olsa da her zaman akıllıca değildir. Boyer-Moore algoritması, kalıbı sağdan sola inceleyip uyuşmazlıklardan bilgi çıkararak gereksiz karşılaştırmaları atlar. Kısacası yalnızca “eşleşmedi” demez; “buradan birkaç adım öteye sıçrayabilirim” diyerek aramayı hızlandırır.

``

## Temel fikir: Neden sondan başlıyoruz?

Elimizde uzunluğu $n$ olan bir metin ve uzunluğu $m$ olan bir kalıp bulunsun. Naif arama, kalıbı metindeki her olası konuma yerleştirir ve karakterleri soldan sağa karşılaştırır. En kötü durumda yaklaşık $O(nm)$ işlem yapılabilir.

Boyer-Moore ise kalıbı metnin üzerine yerleştirir, fakat karşılaştırmaya kalıbın son karakterinden başlar. Sağ tarafta oluşan bir uyuşmazlık, kalıbın tamamını birkaç konum birden kaydırmaya izin verebilir. Bu davranış özellikle kalıp uzadıkça ve alfabe genişledikçe etkili olur.

| Özellik | Naif arama | Boyer-Moore |
|---|---|---|
| Tarama yönü | Soldan sağa | Kalıp içinde sağdan sola |
| Uyuşmazlık sonrası | Genellikle bir adım kayar | Birden fazla adım sıçrayabilir |
| Ön işleme | Gerekmez | Kaydırma tabloları hazırlanır |
| Pratik performans | Küçük girdilerde yeterli | Uzun metinlerde oldukça hızlı |

## Kötü karakter sezgisi

Algoritmanın en anlaşılır kuralı **kötü karakter kuralıdır**. Kalıbın $j$ indeksindeki karakter ile metindeki karakter uyuşmazsa, karşılaşılan metin karakterinin kalıp içindeki en sağ konumuna bakılır.

Bu konumu $last(c)$ ile gösterirsek kaydırma miktarı şöyle hesaplanabilir:

$$s = max(1, j - last(c))$$

Karakter kalıpta hiç yoksa $last(c)=-1$ kabul edilir. Böylece kalıp, uyuşmayan karakteri tamamen geride bırakacak kadar kaydırılabilir. Örneğin `KOD` kalıbını ararken karşılaştırılan metin karakteri `X` ise ve `X` kalıpta bulunmuyorsa tek tek ilerlemek yerine kalıp birkaç adım ileri taşınır.

Boyer-Moore’un tam sürümünde bir de **iyi sonek kuralı** vardır. Kalıbın sonunda eşleşmiş bir bölüm bulunup daha solda uyuşmazlık yaşanırsa algoritma, eşleşen sonekin kalıptaki başka bir tekrarını veya uygun bir önekini arar. İki kuralın önerdiği kaydırmalardan büyük olanı seçilir. Bu ek mekanizma güçlüdür; ancak kötü karakter kuralı bile tek başına pratik bir hızlanma sağlar.

## Python ile basitleştirilmiş uygulama

Aşağıdaki kod yalnızca kötü karakter sezgisini kullanır. Ön işleme aşaması, kalıptaki her karakterin en sağ indeksini bir sözlükte saklar:

```python
def boyer_moore_ara(metin, kalip):
    if not kalip:
        return 0

    # Her karakterin kalıptaki en sağ konumunu hazırlar.
    son_konum = {karakter: i for i, karakter in enumerate(kalip)}
    n, m = len(metin), len(kalip)
    kayma = 0

    while kayma <= n - m:
        j = m - 1

        # Karakterleri kalıbın sonundan başına doğru karşılaştırır.
        while j >= 0 and kalip[j] == metin[kayma + j]:
            j -= 1

        if j < 0:
            return kayma

        kotu_karakter = metin[kayma + j]
        kayma += max(1, j - son_konum.get(kotu_karakter, -1))

    return -1

metin = "ALGORITMALARLA METIN ARAMA"
print(boyer_moore_ara(metin, "METIN"))
```

Fonksiyon ilk eşleşmenin başlangıç indeksini, eşleşme yoksa `-1` değerini döndürür. Sözlüğün hazırlanması $O(m)$ zaman ve kullanılan farklı karakter sayısı kadar ek alan gerektirir.

## Karmaşıklık ve kullanım alanları

Basitleştirilmiş sürümün en kötü durumu yine $O(nm)$ olabilir. Bununla birlikte Boyer-Moore, ortalama senaryolarda metnin bütün karakterlerini incelemeden ilerleyebilir. Tam algoritmanın dikkatli hazırlanmış sürümleri daha güçlü teorik garantiler sunar.

Algoritma; metin editörlerinde arama, log analizi, DNA dizilerinin incelenmesi ve güvenlik araçlarında imza tarama gibi alanlarda kullanılır. Kalıp kısa veya metin çok küçükse ön işleme maliyeti avantajı azaltabilir. Fakat uzun metinlerde Boyer-Moore’un sıçramaları, arama sürecini karakter karakter yürüyen bir kaplumbağadan engellerin üzerinden atlayan çevik bir tavşana dönüştürür.

![boyer-moore-algoritmasi-21](/img/boyer-moore-algoritmasi-21.svg)

