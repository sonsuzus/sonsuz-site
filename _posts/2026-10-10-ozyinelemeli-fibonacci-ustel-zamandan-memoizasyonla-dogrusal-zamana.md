---
layout: post
title: "Özyinelemeli Fibonacci: Üstel Zamandan Memoizasyonla Doğrusal Zamana"
math: true
categories: 
  - Bilgi
tags: 
  - fibonacci
  - özyineleme
  - memoizasyon
  - algoritma
  - dinamik programlama
  - python
toc: true
image: /img/ozyinelemeli-fibonacci-ustel-96.png
---

![ozyinelemeli-fibonacci-ustel-96](/img/ozyinelemeli-fibonacci-ustel-96.svg)


Fibonacci dizisi, algoritma öğrenirken karşımıza çıkan en ünlü örneklerden biridir. Tanımı son derece basit görünür: Her sayı, kendisinden önce gelen iki sayının toplamıdır. Ancak bu masum tanımı saf özyineleme ile doğrudan koda çevirdiğimizde bilgisayarımız aynı işlemleri tekrar tekrar yapmaya başlar. Gelin bu performans tuzağının neden oluştuğunu ve memoizasyonun onu nasıl ortadan kaldırdığını inceleyelim.

``

## Fibonacci dizisinin matematiksel tanımı

Dizinin başlangıç değerlerini $F(0)=0$ ve $F(1)=1$ olarak kabul edelim. Geri kalan terimler şu bağıntıyla hesaplanır:

$$
F(n)=F(n-1)+F(n-2), \quad n \ge 2
$$

Böylece dizi $0, 1, 1, 2, 3, 5, 8, 13, \ldots$ biçiminde ilerler. Matematiksel tanımın kendi kendisine başvurması, özyinelemeli bir program yazmayı oldukça doğal hâle getirir.

```python
def fibonacci(n):
    if n <= 1:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(10))  # 55
```

Bu fonksiyon önce taban durumu kontrol eder. $n$, sıfır veya bir olduğunda doğrudan sonucu döndürür; aksi hâlde önceki iki Fibonacci değerini ayrı çağrılarla hesaplar. Kod kısa, okunabilir ve matematiksel tanıma neredeyse birebir uygundur. Ne yazık ki kısa kod her zaman hızlı kod değildir.

## Saf özyineleme neden yavaştır?

$fibonacci(5)$ çağrıldığında fonksiyon hem $fibonacci(4)$ hem de $fibonacci(3)$ çağrılarını oluşturur. Ardından $fibonacci(4)$, kendi içinde $fibonacci(3)$ değerini yeniden hesaplar. Yani aynı alt problem birden fazla kez çözülür.

Çağrı sayısını yaklaşık olarak şu bağıntı ifade eder:

$$
T(n)=T(n-1)+T(n-2)+O(1)
$$

Bu yapı Fibonacci dizisine benzediği için çalışma süresi yaklaşık $O(\varphi^n)$ olur. Buradaki $\varphi \approx 1.618$, altın orandır. Karmaşıklık çoğu zaman daha genel bir üst sınırla $O(2^n)$ şeklinde de gösterilir. Her yeni değer, çağrı ağacını hızla büyütür; bilgisayar adeta daha önce çözdüğü soruların cevaplarını unutup tekrar sınava girer.

| Yaklaşım | Zaman karmaşıklığı | Alan karmaşıklığı | Tekrarlanan hesaplama |
|---|---:|---:|---|
| Saf özyineleme | $O(2^n)$ | $O(n)$ | Çok fazla |
| Memoizasyon | $O(n)$ | $O(n)$ | Yok |
| Döngüsel çözüm | $O(n)$ | $O(1)$ | Yok |

## Memoizasyon ile sonuçları hatırlamak

Memoizasyon, hesaplanan sonuçları bir önbellekte saklar. Fonksiyon aynı $n$ değeriyle yeniden çağrıldığında bütün çağrı ağacını tekrar kurmak yerine hazır sonucu döndürür.

```python
def fibonacci(n, cache=None):
    # Sözlüğü yalnızca ilk çağrıda oluştururuz.
    if cache is None:
        cache = {0: 0, 1: 1}

    # Daha önce hesaplandıysa doğrudan kullanırız.
    if n in cache:
        return cache[n]

    cache[n] = fibonacci(n - 1, cache) + fibonacci(n - 2, cache)
    return cache[n]

print(fibonacci(40))  # 102334155
```

Bu sürümde $F(0)$ ile $F(n)$ arasındaki her değer en fazla bir kez hesaplanır. Her hesaplama sabit zamanlı sözlük erişimleri yaptığı için toplam süre $O(n)$ seviyesine iner. Önbellek ve çağrı yığını ise $O(n)$ alan kullanır.

Python, aynı fikri hazır bir dekoratörle uygulamamıza da izin verir:

```python
from functools import cache

@cache
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

## Hangi yöntemi seçmeliyiz?

Saf özyineleme, algoritmanın matematiksel yapısını göstermek için harikadır; fakat büyük girdilerde pratik değildir. Memoizasyon, okunabilir özyinelemeli yapıyı korurken performansı dramatik biçimde iyileştirir. Yalnızca sonuca ihtiyaç duyuluyorsa döngüsel yaklaşım daha az bellek tüketebilir. Buradaki temel ders Fibonacci’den büyüktür: Bir problem örtüşen alt problemlere sahipse, daha önce hesaplanan sonuçları saklamak üstel bir algoritmayı doğrusal bir çözüme dönüştürebilir.
