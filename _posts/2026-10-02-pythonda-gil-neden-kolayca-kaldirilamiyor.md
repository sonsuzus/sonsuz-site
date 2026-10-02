---
layout: post
title: "Python'da GIL Neden Kolayca Kaldırılamıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - gil
  - çoklu iş parçacığı
  - bellek yönetimi
  - c uzantıları
  - eşzamanlılık
toc: true
image: /img/pythonda-gil-neden-26.png
---

Python geliştiricilerinin performans sohbetlerinde er ya da geç karşılaştığı bir kötü karakter vardır: **Global Interpreter Lock**, yani GIL. İlk bakışta çözüm basit görünür: Kilidi kaldır, bütün işlemci çekirdekleri aynı anda Python kodu çalıştırsın! Ne var ki GIL, kapının önüne yanlışlıkla bırakılmış bir sandalye değildir; CPython'ın bellek yönetimine ve geniş C uzantısı ekosistemine bağlanmış yapısal bir parçadır.


![pythonda-gil-neden-26](/img/pythonda-gil-neden-26.svg)

``

## GIL gerçekte neyi kilitliyor?

GIL, standart Python yorumlayıcısı CPython'da aynı süreç içindeki yalnızca bir iş parçacığının belirli bir anda **Python bytecode** çalıştırmasına izin veren kilittir. Dolayısıyla sekiz çekirdekli bir işlemcide sekiz CPU-yoğun Python iş parçacığı başlatmak, hesaplamayı otomatik olarak sekiz kat hızlandırmaz.

Kabaca ideal paralel hızlanma $S(n)=n$ gibi düşünülebilir. Ancak GIL altında CPU-yoğun saf Python kodu için pratik sonuç çoğu zaman $S(n) \approx 1$ olur; kilit rekabeti nedeniyle daha kötü sonuçlar bile görülebilir.

```python
import threading

def hesapla():
    toplam = 0
    for i in range(5_000_000):
        toplam += i * i

threads = [threading.Thread(target=hesapla) for _ in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
```

Bu kod dört iş parçacığı oluşturur, fakat `hesapla` CPU-yoğun olduğu için Python bytecode'u gerçek anlamda dört çekirdekte paralel çalışmaz. Buna karşılık dosya, ağ veya veritabanı bekleyen iş parçacıkları sırasında GIL serbest bırakılabildiğinden I/O ağırlıklı programlar yine fayda görebilir.

| İş yükü | Thread kullanımı | GIL etkisi | Uygun yaklaşım |
|---|---:|---|---|
| Ağ istekleri | Faydalı | Beklerken azalır | `threading`, `asyncio` |
| Saf Python hesaplaması | Genellikle sınırlı | Yüksek | `multiprocessing` |
| NumPy işlemleri | Çoğu zaman faydalı | C kodu GIL'i bırakabilir | NumPy ve thread'ler |
| Bağımsız görevler | Faydalı | Süreçler GIL paylaşmaz | Süreç havuzu |

## Referans sayımı: küçük ama kritik ayrıntı

CPython, nesnelerin yaşam süresini ağırlıklı olarak **referans sayımıyla** yönetir. Bir nesneye yeni referans verildiğinde sayaç artırılır; referans silindiğinde azaltılır. Sayaç sıfıra ulaştığında nesne çoğunlukla hemen yok edilir:

$$R_{yeni}=R_{eski}+\Delta R$$

İki iş parçacığı aynı sayacı eşzamanlı değiştirirse güncellemeler kaybolabilir. GIL, bu işlemleri büyük ölçüde seri hâle getirerek nesne başına kilit veya her sayaç için pahalı atomik işlem ihtiyacını azaltır. Kilidi yalnızca silmek; yarış koşulları, erken bellek boşaltma ve yorumlayıcı çökmeleri davet etmek demektir.

CPython ayrıca döngüsel referansları temizleyen bir çöp toplayıcı kullanır. Ancak günlük nesne yaşam döngüsünün merkezinde hâlâ referans sayımı bulunur. Bu nedenle mesele yalnızca bir `mutex` satırını kaldırmak değildir.

## C uzantıları neden işi zorlaştırıyor?

NumPy, Pillow ve pek çok veritabanı sürücüsü CPython'ın C API'sini kullanır. Yıllar boyunca bu uzantıların önemli bir bölümü, Python nesnelerine erişirken GIL'in gerekli güvenliği sağladığını varsaydı:

```c
PyObject *item = PyList_GetItem(list, 0);
/* GIL sayesinde item ve list üzerinde güvenli erişim varsayılır. */
```

GIL ortadan kaldırıldığında uzantıların nesne ömrünü, paylaşılan veriyi ve hata durumlarını yeni eşzamanlılık kurallarıyla yönetmesi gerekir. Eski ikili paketlerin uyumluluğu da ayrı bir sorundur. Python'ın dev ekosistemi düşünüldüğünde bu, hareket hâlindeki bir geminin motorunu değiştirmeye benzer.

## GIL gerçekten vazgeçilmez mi?

Tam anlamıyla değil. PEP 703 kapsamında geliştirilen serbest iş parçacıklı CPython, GIL olmadan çalışmayı mümkün kılmak için önyargılı referans sayımı, geciktirilmiş güncellemeler, daha ince kilitler ve C API değişiklikleri kullanır. Fakat karşılığında tek iş parçacıklı performans, bellek tüketimi, hata ayıklama ve uzantı uyumluluğu dikkatle dengelenmelidir.

Özetle GIL kötü tasarlanmış rastgele bir engel değil, CPython'ın yıllarca hızlı ve görece basit kalmasını sağlayan bir mühendislik ödünleşimidir. Kaldırılabilir; ancak bunu güvenli yapmak, yalnızca kilidi açmayı değil, kilidin koruduğu bütün evi yeniden güçlendirmeyi gerektirir.
