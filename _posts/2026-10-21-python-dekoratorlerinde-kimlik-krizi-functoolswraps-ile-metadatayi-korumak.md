---
layout: post
title: "Python Dekoratörlerinde Kimlik Krizi: functools.wraps ile Metadata’yı Korumak"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - dekoratör
  - functools
  - metadata
  - wraps
toc: true
image: /img/python-dekoratorlerinde-kimlik-57.png
---

Python dekoratörleri, bir fonksiyonun davranışını kaynak kodunu değiştirmeden genişletmenin zarif bir yoludur. Ancak dekoratörümüzü dikkatsizce yazarsak orijinal fonksiyonun adı, docstring’i ve diğer metadata bilgileri ortadan kaybolabilir. Fonksiyon çalışmaya devam eder ama sahneye başka birinin kimliğiyle çıkar. Neyse ki `functools.wraps`, bu küçük kimlik krizini çözmek için standart kütüphanede bizi bekler.
``
## Dekoratör aslında ne yapar?

Bir dekoratör, bir fonksiyonu parametre olarak alır ve yerine genellikle başka bir fonksiyon döndürür. Matematiksel olarak dekoratör dönüşümünü şöyle düşünebiliriz:

$$D(f) = g$$

Burada $f$ orijinal fonksiyon, $D$ dekoratör ve $g$ çağrıların yönlendirildiği yeni fonksiyondur. Python’daki `@dekorator` sözdizimi ise temelde şu eşitliğin kısa yazımıdır:

$$f = D(f)$$

Basit bir zamanlama dekoratörü yazalım:

```python
import time

def zaman_olc(func):
    def wrapper(*args, **kwargs):
        baslangic = time.perf_counter()
        sonuc = func(*args, **kwargs)
        sure = time.perf_counter() - baslangic
        print(f"Çalışma süresi: {sure:.6f} saniye")
        return sonuc

    return wrapper

@zaman_olc
def topla(a, b):
    """İki sayıyı toplar."""
    return a + b
```

`wrapper`, farklı imzalara sahip fonksiyonlarla çalışabilmek için `*args` ve `**kwargs` kullanır. Önce zamanı kaydeder, orijinal fonksiyonu çalıştırır ve geçen süreyi ekrana yazar.

## Metadata neden kaybolur?

Dekoratör uygulandıktan sonra `topla` değişkeni artık orijinal fonksiyonu değil, döndürülen `wrapper` fonksiyonunu gösterir. Bu nedenle aşağıdaki sonuçlar şaşırtıcı olabilir:

```python
print(topla.__name__)  # wrapper
print(topla.__doc__)   # None
```

Python açısından ortada gizem yoktur: Yeni nesnenin metadata’sı okunmaktadır. Sorun özellikle dokümantasyon araçlarında, hata ayıklamada, testlerde ve fonksiyon adını kullanan framework’lerde belirginleşir.

| Özellik | Dekoratörsüz | Sıradan dekoratör sonrası |
|---|---|---|
| `__name__` | `topla` | `wrapper` |
| `__doc__` | `İki sayıyı toplar.` | `None` |
| `__module__` | Tanımlandığı modül | Dekoratörün modülü |
| İzleme kolaylığı | Yüksek | Daha düşük |

![python-dekoratorlerinde-kimlik-57](/img/python-dekoratorlerinde-kimlik-57.svg)


## functools.wraps kurtarmaya geliyor

Çözüm, iç fonksiyonun üzerine `@wraps(func)` eklemektir:

```python
import time
from functools import wraps

def zaman_olc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        baslangic = time.perf_counter()
        sonuc = func(*args, **kwargs)
        sure = time.perf_counter() - baslangic
        print(f"Çalışma süresi: {sure:.6f} saniye")
        return sonuc

    return wrapper

@zaman_olc
def topla(a, b):
    """İki sayıyı toplar."""
    return a + b

print(topla.__name__)  # topla
print(topla.__doc__)   # İki sayıyı toplar.
```

`wraps`, kendi başına sihirli bir kopyalama motoru değildir; `functools.update_wrapper` fonksiyonunun dekoratör biçiminde kullanılmasını sağlar. Varsayılan olarak `__module__`, `__name__`, `__qualname__`, `__doc__`, `__annotations__` ve `__type_params__` gibi nitelikleri wrapper’a aktarır. Ayrıca wrapper’ın sözlüğünü günceller.

| Yaklaşım | İsim korunur mu? | Docstring korunur mu? | Orijinale erişim |
|---|---:|---:|---:|
| Düz `wrapper` | Hayır | Hayır | Closure üzerinden |
| Elle kopyalama | Kısmen | Kısmen | Genellikle hayır |
| `@wraps(func)` | Evet | Evet | `__wrapped__` ile |

## Bonus: `__wrapped__` ve introspection

`wraps`, wrapper’a `__wrapped__` niteliğini de ekler. Böylece orijinal fonksiyona doğrudan ulaşılabilir:

```python
print(topla.__wrapped__(3, 4))  # 7; zaman ölçümü yapılmaz
```

`inspect.signature` gibi introspection araçları da bu zinciri takip ederek anlamlı sonuçlar üretir:

```python
from inspect import signature

print(signature(topla))  # (a, b)
```

Bu özellik yalnızca kozmetik değildir. IDE desteği, otomatik API dokümantasyonu, bağımlılık enjeksiyonu ve test araçları doğru metadata’ya güvenir. Özetle dekoratör yazarken `@wraps(func)` kullanmak, emniyet kemeri takmak gibidir: Kod onsuz da ilerleyebilir, fakat ilk sert virajda neden gerekli olduğunu anlarsınız.
