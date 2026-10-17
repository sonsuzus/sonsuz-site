---
layout: post
title: "Async Kodun Gizli Freni: Bloklayan Çağrılar Event Loop'u Nasıl Durdurur?"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - asyncio
  - async-await
  - event-loop
  - eşzamanlılık
  - performans
toc: true
image: /img/async-kodun-gizli-69.png
---

Python’da `async` ve `await` kullanmak, kodun otomatik olarak hızlı veya tamamen eşzamanlı çalışacağı anlamına gelmez. Asenkron bir fonksiyonun içine sıradan, bloklayan bir çağrı yerleştirirseniz diğer görevler beklemeye başlar. Tek şeritli bir yola park edilen kamyon gibi, küçücük görünen bu çağrı bütün event loop trafiğini durdurabilir.
``

## Event loop gerçekte ne yapar?

`asyncio` event loop, çalışmaya hazır görevleri sırayla ilerleten bir koordinatördür. Bir coroutine `await` ile kontrolü gönüllü biçimde bıraktığında loop başka bir göreve geçebilir. Buradaki kritik nokta şudur: Görev kontrolü bırakmazsa event loop onu zorla kenara çekmez.

Yaklaşık toplam bekleme süresini şöyle düşünebiliriz:

$$
T_{toplam} \approx \max(T_1, T_2, \ldots, T_n)
$$

Bu avantaj yalnızca görevler uygun noktalarda kontrolü event loop’a iade ederse geçerlidir. Bloklayan işlemler seri biçimde yürütülürse süre şu modele yaklaşır:

$$
T_{toplam} \approx \sum_{i=1}^{n} T_i
$$

| İşlem | Event loop’a kontrol verir mi? | Sonuç |
|---|---:|---|
| `await asyncio.sleep(1)` | Evet | Diğer görevler çalışır |
| `time.sleep(1)` | Hayır | Tüm loop bir saniye donar |
| Asenkron HTTP isteği | Evet | Ağ beklenirken görev değişir |
| Senkron dosya veya HTTP çağrısı | Hayır | İşlem bitene kadar loop bekler |
| Yoğun CPU hesabı | Hayır | İş parçacığı uzun süre meşgul kalır |

## Masum görünen hata

Aşağıdaki örnekte fonksiyon `async` olsa da içindeki `time.sleep` bloklayıcıdır:

```python
import asyncio
import time

async def is_yap(no: int):
    print(f'{no} başladı')
    time.sleep(2)  # Event loop burada tamamen durur.
    print(f'{no} bitti')

async def main():
    await asyncio.gather(*(is_yap(i) for i in range(3)))

asyncio.run(main())
```

Üç görev oluşturulmasına rağmen yaklaşık altı saniye beklenir. Çünkü ilk görev `time.sleep(2)` çalıştırırken diğer coroutine’ler işlemciye ulaşamaz. Fonksiyon başındaki `async` ifadesi, içindeki senkron kodu sihirli biçimde asenkronlaştırmaz.

Uyku yalnızca beklemeyi temsil ediyorsa doğru çözüm `asyncio.sleep` kullanmaktır:

```python
async def is_yap(no: int):
    print(f'{no} başladı')
    await asyncio.sleep(2)  # Kontrol event loop'a geri verilir.
    print(f'{no} bitti')
```

Bu sürümde görevler birlikte ilerler ve toplam süre yaklaşık iki saniye olur.

## Senkron kütüphaneyi çöpe mi atalım?

Her bloklayan kütüphanenin asenkron alternatifi bulunmayabilir. Python 3.9 ve sonrasında `asyncio.to_thread`, bloklayan I/O işlemini ayrı bir iş parçacığında çalıştırmayı kolaylaştırır:

```python
import asyncio
import time

def eski_raporu_uret():
    time.sleep(3)
    return 'Rapor hazır'

async def main():
    sonuc = await asyncio.to_thread(eski_raporu_uret)
    print(sonuc)

asyncio.run(main())
```

Burada event loop beklerken donmaz; başka görevleri yürütmeye devam eder. Ancak `to_thread` özellikle dosya, ağ veya eski SDK çağrıları gibi I/O ağırlıklı işler için uygundur.

## CPU ağırlıklı işler farklıdır

Büyük görüntü işleme, asal sayı arama veya karmaşık veri dönüşümü gibi CPU ağırlıklı işler de event loop’u bloke eder. Bunları bir thread’e taşımak, Python’ın GIL davranışı nedeniyle her zaman gerçek paralellik sağlamaz. Böyle durumlarda `ProcessPoolExecutor` daha doğru seçim olabilir:

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def agir_hesaplama(n: int):
    return sum(i * i for i in range(n))

async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as havuz:
        sonuc = await loop.run_in_executor(
            havuz, agir_hesaplama, 20_000_000
        )
    print(sonuc)

asyncio.run(main())
```

Kısacası `async/await`, bloklamayı ortadan kaldıran bir büyü değil, bekleme anlarını yönetme protokolüdür. Kod incelemesinde `time.sleep`, senkron HTTP istemcileri, ağır dosya işlemleri ve uzun döngüler özellikle aranmalıdır. Event loop’un sağlıklı kalmasının altın kuralı basittir: Ya kontrolü hızla geri verin ya da bloklayan işi uygun bir thread veya process havuzuna taşıyın.

![async-kodun-gizli-69](/img/async-kodun-gizli-69.svg)

