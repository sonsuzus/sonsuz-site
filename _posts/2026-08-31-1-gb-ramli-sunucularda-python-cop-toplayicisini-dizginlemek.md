---
layout: post
title: "1 GB RAM’li Sunucularda Python Çöp Toplayıcısını Dizginlemek"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - bellek yönetimi
  - garbage collector
toc: true
---

Bir Python botu geliştirme bilgisayarında uslu uslu çalışırken 1 GB RAM’li AMD sunucuda neden bir anda bütün belleği yiyen küçük bir canavara dönüşür? Bunun nedeni çoğu zaman tek bir bellek sızıntısı değil; referans sayımı, döngüsel nesneler, Python’ın bellek ayırıcısı ve işletim sisteminin davranışının birleşimidir. Neyse ki doğru ölçüm ve kontrollü çöp toplama ile botu sürekli yeniden başlatmadan belleği sınırlandırmak mümkündür.
``

## Python belleği nasıl boşaltır?

CPython öncelikle **referans sayımı** kullanır. Bir nesneye kaç değişkenin işaret ettiği izlenir; sayı sıfıra düştüğünde nesne hemen temizlenir. Kabaca:

$$R(x)=0 \Rightarrow x\text{ serbest bırakılabilir}$$

Ancak iki nesne birbirine referans veriyorsa dışarıdan erişilemeseler bile referans sayıları sıfır olmaz. Python’ın kuşaklı çöp toplayıcısı, yani `gc`, bu döngüleri bulmak için devreye girer.

| Kuşak | İçerik | Tarama sıklığı | Maliyet |
|---|---|---:|---:|
| 0 | Yeni nesneler | Yüksek | Düşük |
| 1 | Bir taramadan kurtulanlar | Orta | Orta |
| 2 | Uzun ömürlü nesneler | Düşük | Yüksek |

Önemli ayrıntı şudur: Python nesneyi temizlese bile süreç belleği anlamına gelen **RSS** hemen düşmeyebilir. CPython küçük nesneler için arena tabanlı ayırıcı kullanır. Bir arenada yaşayan tek bir nesne bile varsa alan işletim sistemine iade edilmeyebilir. Dolayısıyla `gc.collect()` çalıştırmak, RAM grafiğinin mutlaka aşağı ineceği anlamına gelmez.

## Eşikleri körlemesine düşürmeyin

Varsayılan eşikler `gc.get_threshold()` ile görülebilir. İlk değer, oluşturulan ve silinen nesneler arasındaki fark belirli seviyeye ulaştığında genç kuşağın taranmasını tetikler. Çok düşük eşik daha az geçici bellek, fakat daha fazla CPU tüketimi demektir.

| Yaklaşım | Bellek etkisi | CPU etkisi | Uygun senaryo |
|---|---:|---:|---|
| Düşük GC eşikleri | Daha kontrollü | Daha yüksek | Yoğun nesne üreten bot |
| Periyodik tam tarama | Ani düşüş sağlayabilir | Kısa duraklama | Trafiğin sakin olduğu an |
| GC’yi kapatmak | Riskli büyüme | Daha düşük | Yalnızca ölçülmüş özel iş yükü |
| Süreç yenileme | Kesin temizlik | Başlatma maliyeti | İzole worker mimarisi |

1 GB sınırında hedef, botun teorik maksimumunun sınıra yaklaşmamasıdır. İşletim sistemi ve diğer servisler için en az 200–300 MB pay bırakmak akıllıcadır.

## Kontrollü toplama örneği

Aşağıdaki kod, botun bakım döngüsünde belleği ölçer; eşik aşılırsa tam çöp toplama yapar. Linux ve glibc kullanılan sistemlerde `malloc_trim`, boşta kalan heap sayfalarının işletim sistemine geri verilmesini teşvik eder.

```python
import asyncio
import ctypes
import gc
import os

import psutil

PROCESS = psutil.Process(os.getpid())
SOFT_LIMIT_MB = 650

# Daha erken toplama; üretimde ölçüm yapılarak ayarlanmalıdır.
gc.set_threshold(500, 8, 8)


def rss_mb():
    return PROCESS.memory_info().rss / (1024 ** 2)


def trim_linux_heap():
    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
    except (OSError, AttributeError):
        pass


async def memory_guard():
    while True:
        used = rss_mb()
        if used >= SOFT_LIMIT_MB:
            collected = gc.collect(2)
            trim_linux_heap()
            print(f"GC: {collected} nesne, RSS: {rss_mb():.1f} MB")
        await asyncio.sleep(30)
```

Bu koruma döngüsü mucizevi bir sızıntı tamircisi değildir. Sürekli büyüyen sözlükler, sınırsız önbellekler, geçmiş mesaj listeleri ve kapanmayan HTTP yanıtları hâlâ düzeltilmelidir. `functools.lru_cache` kullanılıyorsa `maxsize`, kuyruklarda `maxsize` ve ağ isteklerinde zaman aşımı tanımlanmalıdır.

## AMD sunucular için özel bir durum var mı?

Çöp toplayıcının temel mantığı AMD veya Intel’e göre değişmez; asıl belirleyiciler Linux çekirdeği, glibc, Python sürümü ve iş yüküdür. Sunucuda systemd kullanılıyorsa `MemoryMax=800M` gibi kesin bir sınır ve otomatik yeniden başlatma eklemek son savunma hattı olabilir. En sağlıklı formül şudur: **ölç, sınır koy, yoğun olmayan anda topla ve sınırsız veri yapılarını ortadan kaldır.** Böylece bot, 1 GB’lık odasında mobilyaları tavana kadar yığmadan yaşamayı öğrenir.
