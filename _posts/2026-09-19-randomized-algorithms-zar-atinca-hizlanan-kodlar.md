---
layout: post
title: "Randomized Algorithms: Zar Atınca Hızlanan Kodlar"
math: true
categories: 
  - Bilgi
tags: 
  - randomized algorithms
  - algoritmalar
  - olasılık
  - python
  - karmaşıklık
  - bilgisayar bilimi
toc: true
image: /img/randomized-algorithms-zar-78.png
---

Bir algoritmanın karar verirken yazı tura attığını düşünün. İlk bakışta bu yaklaşım, ciddi bir mühendislik yönteminden çok şans oyununa benzeyebilir. Oysa rastgele seçimler; kötü girdilerden kaçınmak, karmaşık kararları basitleştirmek ve yüksek performansa daha az kodla ulaşmak için güçlü bir araçtır. Randomized algorithms dünyasında rastgelelik, belirsizlik yaratan bir kusur değil, kontrollü biçimde kullanılan bir kaynaktır.
``

## Rastgelelik algoritmaya neden yardım eder?

Deterministik bir algoritma, aynı girdi için daima aynı adımları izler. Bu durum tahmin edilebilirlik sağlar; ancak algoritmanın zayıf noktasını bilen girdiler de en kötü çalışma süresini sürekli tetikleyebilir. Rastgele algoritma ise çalışma sırasında bir veya daha fazla seçimi rastgele yapar. Böylece girdinin algoritmanın davranışını yönlendirmesi zorlaşır.

Bir algoritmanın çalışma süresini rastgele değişken $T$ ile gösterirsek performansı genellikle beklenen değer üzerinden inceleriz:

$$E[T] = \sum_i P(T=t_i)\,t_i$$

Buradaki amaç her çalıştırmanın kusursuz olması değil, çok sayıda çalıştırma boyunca maliyetin düşük kalmasıdır. Örneğin rastgele pivot kullanan QuickSort'un beklenen karmaşıklığı $O(n\log n)$ iken kötü durumu $O(n^2)$ olabilir. Fakat kötü durumu art arda üretme olasılığı oldukça düşüktür.

| Özellik | Deterministik algoritma | Rastgele algoritma |
|---|---|---|
| Aynı girdide davranış | Her zaman aynı | Çalıştırmaya göre değişebilir |
| Analiz ölçütü | En iyi, ortalama, en kötü | Beklenen süre ve hata olasılığı |
| Kötü girdiye dayanıklılık | Tasarıma bağlı | Genellikle daha yüksek |
| Tekrarlanabilirlik | Doğrudan | Sabit seed ile sağlanabilir |

## İki temel aile: Las Vegas ve Monte Carlo

Rastgele algoritmalar iki eğlenceli isimli grupta incelenir. Las Vegas algoritmaları her zaman doğru sonuç üretir; yalnızca çalışma süreleri değişir. Rastgele pivotlu QuickSort buna örnektir. Sonuç doğru sıralanır, fakat kaç karşılaştırma yapılacağı şansa bağlıdır.

Monte Carlo algoritmalarında ise çalışma süresi genellikle sınırlıdır, ancak küçük bir hata ihtimali bulunur. Asallık testleri ve yaklaşık sayım yöntemleri bu gruptadır. Bir denemenin hata olasılığı $p$ ise bağımsız olarak $k$ kez tekrarlamanın hata olasılığı çoğu senaryoda

$$P(\text{hata}) \leq p^k$$

seviyesine iner. Yani birkaç tekrar, hatayı adeta matematiksel mikroskopla aranacak kadar küçültebilir.

| Tür | Sonuç doğruluğu | Çalışma süresi |
|---|---|---|
| Las Vegas | Her zaman doğru | Rastgele değişir |
| Monte Carlo | Küçük hata ihtimali vardır | Genellikle öngörülebilir |

## Python ile rastgele QuickSort

Aşağıdaki uygulama, pivotu rastgele seçerek belirli giriş düzenlerinin sürekli kötü bölünme oluşturmasını engeller:

```python
import random

def randomized_quicksort(items):
    if len(items) <= 1:
        return items

    pivot = random.choice(items)
    smaller = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    larger = [x for x in items if x > pivot]

    return (
        randomized_quicksort(smaller)
        + equal
        + randomized_quicksort(larger)
    )

numbers = [9, 2, 7, 2, 5, 1, 8]
print(randomized_quicksort(numbers))
```

Burada rastgelelik sonucun doğruluğunu etkilemez; yalnızca özyinelemeli bölümlerin büyüklüğünü değiştirir. Pivot çoğunlukla dengeli bölmeler oluşturduğunda çağrı ağacı yaklaşık $\log n$ derinliğinde kalır. List comprehension kullanımı örneği okunaklı kılar, ancak ek listeler nedeniyle bellek tüketir; üretim ortamında yerinde bölümleme tercih edilebilir.

## Rastgele demek kontrolsüz demek değildir

Testlerde sonuçların yeniden üretilebilmesi için sözde rastgele sayı üreticisine sabit bir başlangıç değeri verilebilir:

```python
import random

random.seed(42)
print(random.randint(1, 100))
```

Aynı seed, aynı rastgele sayı dizisini oluşturur. Bununla birlikte güvenlik amacıyla token veya parola üretirken `random` yerine kriptografik olarak güvenli `secrets` modülü kullanılmalıdır.

Randomized algorithms; sıralama, grafikler, yük dengeleme, makine öğrenmesi, kriptografi ve büyük veri akışlarında karşımıza çıkar. Ana fikir basittir: Her seçimi kusursuz hesaplamak pahalıysa, iyi bir seçimi rastgele yap ve başarı olasılığını analiz et. Bazen algoritmaya bir zar vermek, ona daha büyük bir beyin vermekten daha etkilidir.

![randomized-algorithms-zar-78](/img/randomized-algorithms-zar-78.svg)

