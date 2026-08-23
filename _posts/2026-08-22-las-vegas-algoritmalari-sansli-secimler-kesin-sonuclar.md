---
layout: post
title: "Las Vegas Algoritmaları: Şanslı Seçimler, Kesin Sonuçlar"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - rastgeleleştirilmiş algoritmalar
  - olasılık
  - quicksort
toc: true
---

Bazı algoritmalar yazı tura atar, rastgele sayılar üretir ve buna rağmen cevabı asla yanlış vermez. İlk bakışta çelişki gibi duran bu fikir, **Las Vegas algoritmalarının** temelidir: Rastgelelik sonucun doğruluğunu değil, çalışmanın süresini ve izlediği yolu etkiler. Yani algoritma biraz şans oyunları şehrinden esinlenmiş gibi davranır; bazen hızlıca kazanır, bazen biraz daha uzun bekletir, fakat masadan yanlış cevapla kalkmaz.
``

## Temel fikir: Doğruluk sabit, maliyet değişken

Bir Las Vegas algoritması için aynı girdi üzerinde farklı çalıştırmalar farklı süreler alabilir. Ancak üretilen sonuç, algoritma sona erdiğinde mutlaka doğrudur. Bu niteliği matematiksel olarak şöyle ifade edebiliriz:

$$P(\text{çıktı doğru} \mid \text{algoritma sonlandı}) = 1$$

Buradaki rastgele değişken genellikle çalışma süresidir. Eğer $T$ çalışma süresini temsil ediyorsa, analizde tek bir en kötü senaryoya odaklanmak yerine beklenen süreyi inceleriz:

$$E[T] = \sum_i P(T=i) \cdot i$$

Bu yaklaşım, özellikle girdilerin kötü niyetli seçilebildiği sistemlerde değerlidir. Deterministik bir algoritmanın sürekli kötü örneklerle karşılaşması mümkündür; rastgele seçimler ise saldırganın veya girdinin algoritmanın iç kararlarını tahmin etmesini zorlaştırır.

## Monte Carlo ile karıştırmayın

Rastgeleleştirilmiş algoritmaların en bilinen iki ailesi Las Vegas ve Monte Carlo'dur. Aralarındaki fark, hata ve zaman arasındaki takastır.

| Özellik | Las Vegas | Monte Carlo |
|---|---|---|
| Sonucun doğruluğu | Her zaman doğrudur | Küçük bir hata olasılığı vardır |
| Çalışma süresi | Değişkendir | Çoğunlukla önceden sınırlandırılır |
| Rastgeleliğin etkisi | Performansı değiştirir | Sonucu etkileyebilir |
| Tipik örnek | Rastgele pivotlu Quicksort | Miller-Rabin asal sayılık testi |

Örneğin Monte Carlo yaklaşımı, “çok büyük olasılıkla asal” diyebilir. Las Vegas yaklaşımı ise “asal” demeden önce doğruluğu garanti edecek kontrolü tamamlar. Kısacası: Monte Carlo zamanı korumak için bazen doğruluktan ödün verir; Las Vegas doğruluğu korumak için zamanı değişken bırakır.

## Klasik örnek: Rastgele pivotlu Quicksort

Quicksort, diziden bir **pivot** seçer; küçük elemanları sola, büyükleri sağa ayırır ve aynı işlemi alt dizilerde tekrarlar. Pivot hep ilk eleman seçilirse, zaten sıralı bir dizi algoritmayı $O(n^2)$ maliyete sürükleyebilir. Pivotu rastgele seçmek ise bu kötü düzenin etkisini büyük ölçüde azaltır.

```python
from random import randrange

def quicksort(dizi):
    if len(dizi) <= 1:
        return dizi

    pivot = dizi[randrange(len(dizi))]
    kucukler = [x for x in dizi if x < pivot]
    esitler = [x for x in dizi if x == pivot]
    buyukler = [x for x in dizi if x > pivot]

    return quicksort(kucukler) + esitler + quicksort(buyukler)
```

Bu kodda rastgele olan tek kritik karar `pivot` seçimidir. Buna rağmen sonuç her çalıştırmada sıralı bir dizidir; çünkü bölümleme kuralı sıralama mantığını bozmaz. Rastgelelik yalnızca alt problemlerin ne kadar dengeli oluşacağını belirler.

| Pivot seçimi | En iyi durum | Beklenen/pratik davranış | Kötü durum |
|---|---:|---:|---:|
| İlk eleman | $O(n \log n)$ | Girdi düzenine hassas | $O(n^2)$ |
| Rastgele eleman | $O(n \log n)$ | $E[T]=O(n \log n)$ | $O(n^2)$ olası ama seyrek |

Dikkat edilmesi gereken nokta şudur: Rastgele pivot, $O(n^2)$ olasılığını matematiksel olarak sıfırlamaz. Buna karşılık beklenen çalışma süresini $O(n \log n)$ seviyesine taşır ve belirli kötü girdi kalıplarına bağımlılığı azaltır.

## Ne zaman tercih edilir?

Las Vegas algoritmaları; doğruluğun vazgeçilmez, performansın ise ortalama durumda güçlü olmasının yeterli olduğu alanlarda kullanışlıdır. Rastgele dengeli ikili arama ağaçları, rastgeleleştirilmiş seçim algoritmaları ve bazı grafik algoritmaları bu düşünceden yararlanır. Özellikle web servisleri veya yarışma programları gibi, girdinin algoritmanın zayıf noktalarını hedefleyebileceği ortamlarda rastgelelik koruyucu bir katman sağlar.

Elbette rastgele sayı üretecinin kalitesi, tekrarlanabilir testler için sabit tohum kullanımı ve beklenen sürenin gerçekten kabul edilebilir olması ayrıca değerlendirilmelidir. Las Vegas yaklaşımının özeti nettir: Algoritma yolu zarlarla seçebilir, fakat ulaştığı cevap mantıkla doğrulanır.
