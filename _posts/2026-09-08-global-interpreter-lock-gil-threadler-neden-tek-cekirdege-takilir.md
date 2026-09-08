---
layout: post
title: "Global Interpreter Lock (GIL): Thread’ler Neden Tek Çekirdeğe Takılır?"
math: true
categories: 
  - Bilgi
tags: 
  - gıl
  - asenkron programlama
  - python
toc: true
---

Bir programda onlarca iş parçacığı oluşturduğunuz hâlde işlemci kullanımının tek çekirdeğin çevresinde dolaştığını görmek şaşırtıcı olabilir. Bunun yaygın nedenlerinden biri, özellikle CPython gibi yorumlayıcılarda bulunan **Global Interpreter Lock (GIL)** mekanizmasıdır. GIL, belleği korumayı kolaylaştırırken CPU ağırlıklı thread’lerin gerçek paralelliğini sınırlar; ancak doğru eşzamanlılık modeli seçildiğinde bu sınıra takılmadan verimli uygulamalar geliştirilebilir.
``
## GIL tam olarak nedir?

GIL, aynı süreç içinde yalnızca bir iş parçacığının yorumlayıcıya ait bytecode’u belirli bir anda çalıştırmasına izin veren karşılıklı dışlama kilididir. En bilinen örneği CPython’dır; fakat GIL bütün programlama dillerinde veya bütün Python yorumlayıcılarında zorunlu bir özellik değildir.

CPython nesnelerin yaşam süresini ağırlıklı olarak **referans sayımı** ile yönetir. Bir nesnenin referans sayısı kabaca şöyle düşünülebilir:

$$R(x) = \sum_{i=1}^{n} r_i$$

Burada $r_i$, ilgili kod parçasının `x` nesnesine referans verip vermediğini temsil eder. Birden fazla thread bu sayacı aynı anda değiştirseydi yarış koşulları oluşabilirdi. GIL, her nesne için karmaşık kilitler kullanmak yerine yorumlayıcı seviyesinde büyük bir kilit sağlayarak bellek yönetimini ve C eklentilerinin geliştirilmesini basitleştirir.

GIL, işletim sisteminin thread’leri farklı çekirdeklere yerleştirmesini engellemez. Bunun yerine, **Python bytecode’u çalıştırma hakkını** sınırlar. Thread’ler farklı çekirdeklerde zamanlanabilir fakat kilidi sırayla alırlar. Bu nedenle CPU ağırlıklı saf Python kodunda yaklaşık olarak

$$T_p \not\approx \frac{T_1}{p}$$

olur. Buradaki $p$ thread sayısıdır. Hatta kilit değiştirme ve zamanlama maliyetleri yüzünden süre uzayabilir.

## CPU ağırlıklı ve I/O ağırlıklı işler

GIL’in etkisi iş yüküne göre değişir:

| İş yükü | Örnek | Thread kullanımı | Uygun yaklaşım |
|---|---|---:|---|
| CPU ağırlıklı | Görüntü işleme, asal sayı arama | Sınırlı paralellik | Çoklu süreç |
| I/O ağırlıklı | API, dosya, veritabanı | Genellikle yararlı | Thread veya async |
| C eklentisi | NumPy hesaplamaları | Eklentiye bağlı | GIL bırakılıyorsa paralel |

Bir thread ağdan veri beklerken veya desteklenen bir C fonksiyonu uzun işlem sırasında GIL’i bıraktığında başka bir thread çalışabilir. Dolayısıyla “GIL varsa thread tamamen gereksizdir” çıkarımı doğru değildir.

## Asenkron yaklaşım neyi değiştirir?

Asenkron programlama GIL’i kaldırmaz ve CPU işlemlerini paralel hâle getirmez. Bunun yerine bekleme süresini verimli kullanır. Bir görev ağ yanıtını beklediğinde kontrolü olay döngüsüne gönüllü olarak verir; olay döngüsü de hazır olan başka görevi ilerletir.

```python
import asyncio

async def veriyi_getir(adres):
    print(f"İstek başladı: {adres}")
    await asyncio.sleep(1)  # Ağ beklemesini temsil eder
    return f"Yanıt: {adres}"

async def main():
    adresler = ["/kullanicilar", "/urunler", "/siparisler"]
    sonuclar = await asyncio.gather(
        *(veriyi_getir(adres) for adres in adresler)
    )
    print(sonuclar)

asyncio.run(main())
```

Bu örnekte görevler aynı anda hesaplama yapmaz; bekleme aralıkları **örtüştürülür**. Üç işlem ayrı ayrı birer saniye beklese de toplam süre yaklaşık üç saniye yerine bir saniyeye yaklaşır:

$$T_{async} \approx \max(T_1, T_2, \ldots, T_n)$$

Bu avantajın ortaya çıkması için kullanılan HTTP veya veritabanı kütüphanelerinin de asenkron olması gerekir. `async` fonksiyon içinde bloklayan klasik bir çağrı yapmak, bütün olay döngüsünü dondurabilir.

## CPU işi varsa ne yapmalı?

CPU ağırlıklı bir fonksiyonu olay döngüsüne koymak yerine ayrı süreçte çalıştırmak gerekir:

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def hesapla(n):
    return sum(i * i for i in range(n))

async def main():
    dongu = asyncio.get_running_loop()
    with ProcessPoolExecutor() as havuz:
        sonuc = await dongu.run_in_executor(havuz, hesapla, 20_000_000)
        print(sonuc)

asyncio.run(main())
```

Her süreç kendi yorumlayıcısına ve kendi GIL’ine sahip olduğu için işletim sistemi süreçleri farklı çekirdeklerde gerçekten paralel çalıştırabilir. Bedeli ise süreç oluşturma, veri kopyalama ve süreçler arası iletişim maliyetidir.

Kısacası seçim basittir: Çok sayıda bekleyen bağlantı için `asyncio`, bloklayan I/O için thread havuzu, yoğun hesaplama için süreç havuzu kullanın. GIL bir duvar değil; iş yükünü yanlış kapıya yönlendirdiğinizde karşınıza çıkan oldukça seçici bir güvenlik görevlisidir.
