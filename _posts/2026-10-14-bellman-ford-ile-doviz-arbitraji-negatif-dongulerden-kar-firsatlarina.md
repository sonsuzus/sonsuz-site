---
layout: post
title: "Bellman-Ford ile Döviz Arbitrajı: Negatif Döngülerden Kâr Fırsatlarına"
math: true
categories: 
  - Proje
tags: 
  - bellman-ford
  - algoritma
  - graf teorisi
  - arbitraj
  - python
  - finans
toc: true
image: /img/bellman-ford-ile-81.png
---

Bir para birimini diğerine, onu da başka bir para birimine çevirip başlangıçtaki paranızdan daha fazlasıyla geri dönebilir misiniz? Teorik olarak evet! **Arbitraj**, farklı döviz kurları arasındaki tutarsızlıklardan risksiz kâr elde etme fikridir. Bu finans problemini bir graf problemine dönüştürdüğümüzde ise sahneye Bellman-Ford algoritması ve onun meşhur negatif döngü tespiti çıkar.

``

## Döviz piyasasını graf olarak modellemek

Her para birimini bir **düğüm**, mümkün olan her döviz dönüşümünü de yönlü bir **kenar** olarak düşünebiliriz. Örneğin USD'den EUR'ya geçiş ayrı, EUR'dan USD'ye geçiş ayrı bir kenardır; çünkü bu iki kur birbirinin tam tersi olmak zorunda değildir.

Elimizde şu dönüşüm zinciri olsun:

$$USD \rightarrow EUR \rightarrow GBP \rightarrow USD$$

Başlangıçta 1 USD varsa zincirin sonunda elde edeceğimiz miktar:

$$1 \times r_{USD,EUR} \times r_{EUR,GBP} \times r_{GBP,USD}$$

Kurların çarpımı 1'den büyükse başlangıçtakinden daha fazla USD elde ederiz:

$$r_1 \times r_2 \times \cdots \times r_n > 1$$

Ancak graf algoritmaları toplama işlemleriyle çalışmayı sever. Çarpımları toplama çevirmek için logaritmadan yararlanırız:

$$w(u,v) = -\ln(r_{u,v})$$

Negatif logaritma uygulandığında kârlılık koşulu şu hâle gelir:

$$\sum w_i < 0$$

Yani arbitraj fırsatı, dönüştürülmüş graf üzerindeki **negatif ağırlıklı bir döngüdür**.

| Finans kavramı | Graf karşılığı |
|---|---|
| Para birimi | Düğüm |
| Döviz dönüşümü | Yönlü kenar |
| Döviz kuru | Kenar ağırlığının kaynağı |
| Kârlı dönüşüm zinciri | Negatif döngü |
| Komisyon | Efektif kurda azalma |

## Neden Bellman-Ford?

Dijkstra algoritması negatif kenar ağırlıklarıyla güvenilir biçimde çalışmaz. Bellman-Ford ise negatif ağırlıkları destekler ve ulaşılabilir negatif döngüleri belirleyebilir.

Algoritma, $V$ düğümlü bir grafta bütün kenarları $V-1$ kez gevşetir. Bu işlemlerden sonra herhangi bir mesafe hâlâ küçültülebiliyorsa negatif döngü vardır. Zaman karmaşıklığı $O(VE)$ seviyesindedir; para birimi sayısının genellikle sınırlı olması nedeniyle pratik bir seçimdir.

| Algoritma | Negatif kenar | Negatif döngü tespiti | Karmaşıklık |
|---|---:|---:|---:|
| Dijkstra | Hayır | Hayır | $O(E\log V)$ |
| Bellman-Ford | Evet | Evet | $O(VE)$ |
| Floyd-Warshall | Evet | Evet | $O(V^3)$ |

## Python ile arbitraj tespiti

Aşağıdaki fonksiyon kurları negatif logaritmik ağırlıklara dönüştürür. Bütün düğümlerin başlangıç mesafesini sıfır yapmak, bağlantısız bileşenlerdeki döngüleri de aramamızı sağlar.

```python
import math


def find_arbitrage(currencies, rates):
    n = len(currencies)
    edges = []

    for source, target, rate in rates:
        weight = -math.log(rate)
        edges.append((source, target, weight))

    distance = [0.0] * n
    parent = [-1] * n
    changed = -1

    for _ in range(n):
        changed = -1
        for source, target, weight in edges:
            if distance[target] > distance[source] + weight:
                distance[target] = distance[source] + weight
                parent[target] = source
                changed = target

    if changed == -1:
        return None

    # Düğümü döngünün içine taşır.
    vertex = changed
    for _ in range(n):
        vertex = parent[vertex]

    cycle = [vertex]
    current = parent[vertex]
    while current != vertex:
        cycle.append(current)
        current = parent[current]

    cycle.append(vertex)
    cycle.reverse()
    return [currencies[i] for i in cycle]


currencies = ["USD", "EUR", "GBP"]
rates = [
    (0, 1, 0.92),
    (1, 2, 0.87),
    (2, 0, 1.27),
]

print(find_arbitrage(currencies, rates))
```

Fonksiyon `None` döndürürse negatif döngü bulunamamıştır. Bir liste döndürürse listedeki para birimleri olası arbitraj rotasını gösterir. Örnekte kurların çarpımı yaklaşık $0.92 \times 0.87 \times 1.27 = 1.016$ olduğundan teorik olarak yüzde 1,6 civarında brüt kazanç vardır.

## Gerçek hayattaki küçük ama önemli canavarlar

Teorik arbitraj ile uygulanabilir arbitraj aynı şey değildir. Alış-satış farkı, işlem komisyonu, ağ gecikmesi, likidite ve kur değişimleri kârı yok edebilir. Komisyon oranı $c$ ise dönüşümde çıplak kur yerine efektif kur kullanılmalıdır:

$$r_{efektif} = r(1-c)$$

Ayrıca kayan nokta hataları yüzünden karşılaştırmalara küçük bir tolerans eklemek faydalıdır. Bellman-Ford fırsatı matematiksel olarak bulur; fırsatın gerçekten cüzdanınıza ulaşması ise veri kalitesine ve işlem hızına bağlıdır. Kısacası algoritma hazine haritasını çizer, fakat hazinenin yerinde duracağını garanti etmez!

![bellman-ford-ile-81](/img/bellman-ford-ile-81.svg)

