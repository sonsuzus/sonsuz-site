---
layout: post
title: "Euler Yolu ve Euler Turu: Her Kenardan Tam Bir Kez Geçebilir miyiz?"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - euler yolu
  - euler turu
  - algoritma
  - python
toc: true
---

Bir şehrin bütün köprülerinden yalnızca bir kez geçip yürüyüşü tamamlamak mümkün müdür? 18. yüzyılda Königsberg halkının merak ettiği bu soru, bugün graf teorisinin en meşhur problemlerinden biridir. Leonhard Euler’in çözümü yalnızca köprü bilmecesini açıklamakla kalmadı; ağlar, rotalar ve bağlantılar üzerine düşünme biçimimizi de değiştirdi.
``

## Problemi grafa dönüştürmek

Bir ulaşım ağını **graf** olarak modellediğimizde kavşaklar veya kara parçaları **düğüm**, bunları bağlayan yollar veya köprüler ise **kenar** olur. Aradığımız rota her kenarı tam bir kez kullanmalıdır. Düğümlerden kaç kez geçtiğimiz önemli değildir; aynı düğüme tekrar tekrar uğrayabiliriz.

Burada iki temel kavram bulunur:

| Kavram | Başlangıç ve bitiş | Koşul |
|---|---|---|
| Euler yolu | Farklı olabilir | Tam 2 düğümün derecesi tek olmalı |
| Euler turu | Aynı düğüm | Bütün düğümlerin derecesi çift olmalı |
| İmkânsız durum | Rota kurulamaz | Tek dereceli düğüm sayısı 2’den fazla |

Bir düğümün derecesi, ona bağlı kenarların sayısıdır ve $d(v)$ ile gösterilebilir. Yönsüz bir grafta tüm derecelerin toplamı

$$\sum_{v \in V} d(v) = 2\vert E\vert $$

şeklindedir. Her kenar iki uca dokunduğu için toplam derece daima çifttir. Bunun önemli sonucu, tek dereceli düğümlerin sayısının da her zaman çift olmasıdır.

## Neden tek ve çift dereceler belirleyici?

Bir rotanın ortasındaki düğüme bir kenardan giriyorsak başka bir kenardan çıkmamız gerekir. Yani kullanılan kenarlar çiftler hâlinde eşleşir. Bu nedenle ara düğümlerin dereceleri çift olmalıdır.

Euler yolunda başlangıç düğümünden yalnızca çıkış, bitiş düğümüne ise yalnızca giriş artabilir. Dolayısıyla bu iki düğüm tek dereceli olabilir. Euler turunda başlangıç ve bitiş aynı olduğundan böyle bir istisna yoktur.

Ancak derece koşulu tek başına yeterli değildir. Kenarı bulunan bütün düğümler aynı bağlantılı bileşende yer almalıdır. Birbirinden kopuk iki adadaki yolları, ışınlanma özelliğimiz yoksa, tek rotada gezemeyiz.

## Hierholzer algoritması

Euler rotasını gerçekten üretmek için **Hierholzer algoritması** kullanılabilir. Algoritma bir düğümden başlayarak kullanılmamış kenarlarda ilerler. Çıkmaz noktaya ulaştığında rotayı tersten oluşturur. Her kenar bir kez işlendiğinden zaman karmaşıklığı $O(\vert V\vert +\vert E\vert )$ düzeyindedir.

```python
def euler_rotasi(graf):
    # graf: {dugum: [komsu, ...]} biçiminde yönsüz komşuluk listesi
    tekler = [v for v in graf if len(graf[v]) % 2 == 1]
    if len(tekler) not in (0, 2):
        return None

    baslangic = tekler[0] if tekler else next(
        (v for v in graf if graf[v]), None
    )
    if baslangic is None:
        return []

    kopya = {v: komsular[:] for v, komsular in graf.items()}
    yigin, rota = [baslangic], []

    while yigin:
        v = yigin[-1]
        if kopya[v]:
            u = kopya[v].pop()
            kopya[u].remove(v)  # Aynı yönsüz kenarın diğer ucunu sil
            yigin.append(u)
        else:
            rota.append(yigin.pop())

    rota.reverse()
    kenar_sayisi = sum(len(x) for x in graf.values()) // 2
    return rota if len(rota) == kenar_sayisi + 1 else None
```

Kod önce tek dereceli düğümleri sayar. Uygun bir başlangıç seçtikten sonra kenarları geçici graf üzerinden silerek ilerler. Son kontroldeki $\vert E\vert +1$ düğüm şartı, kopuk bileşenler yüzünden bazı kenarların ziyaret edilmeden kalmasını yakalar.

## Küçük bir karar rehberi

- Tek dereceli düğüm yoksa ve graf bağlantılıysa **Euler turu** vardır.
- Tam iki tek dereceli düğüm varsa **Euler yolu** vardır; rota bunlardan birinde başlayıp diğerinde biter.
- İkiden fazla tek dereceli düğüm varsa görev imkânsızdır.
- Kenarlı düğümler bağlantılı değilse dereceler uygun görünse bile rota kurulamaz.

Königsberg probleminde dört kara parçasının dereceleri de tekti. Dört, izin verilen iki sınırını aştığı için bütün köprülerden tam bir kez geçmek mümkün değildi. Bazen en iyi rota, hiç aramadan önce neden var olamayacağını kanıtladığımız rotadır!
