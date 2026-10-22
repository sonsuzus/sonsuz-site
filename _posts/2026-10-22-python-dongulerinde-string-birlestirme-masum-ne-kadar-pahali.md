---
layout: post
title: "Python Döngülerinde String Birleştirme: Masum += Ne Kadar Pahalı?"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - string
  - performans
  - algoritma
  - optimizasyon
toc: true
image: /img/python-dongulerinde-string-33.png
---

Python’da bir döngünün içinde `metin += parça` yazmak son derece doğal görünür. Kod okunaklıdır, çalışır ve küçük verilerde hiçbir sorun hissettirmez. Ancak metin büyüdükçe bu masum işlem, aynı karakterleri tekrar tekrar taşıyan gizli bir performans faturasına dönüşebilir. Gelin bu faturanın nereden geldiğini, ne zaman önemli olduğunu ve `str.join()` yaklaşımının neden genellikle daha güvenli olduğunu inceleyelim.

``

## Sorunun kaynağı: String’ler değiştirilemez

Python’daki `str` nesneleri **immutable**, yani değiştirilemez yapıdadır. Bir string oluşturulduktan sonra içeriğine yeni karakterler eklenemez. Dolayısıyla aşağıdaki ifade mevcut nesneyi gerçekten genişletmek zorunda değildir:

```python
metin = metin + parça
```

Mantıksal olarak Python, eski `metin` ile `parça` için yeterli büyüklükte yeni bir string oluşturur, içerikleri buraya kopyalar ve `metin` değişkenini yeni nesneye yönlendirir. Döngü ilerledikçe kopyalanması gereken içerik de büyür.

Her parçanın uzunluğu $k$ ve parça sayısı $n$ olsun. Tekrarlanan birleştirmenin yaklaşık kopyalama maliyeti şöyledir:

$$
k + 2k + 3k + \dots + nk = k\frac{n(n+1)}{2}
$$

Bu toplam, teorik olarak $O(n^2)$ davranışına karşılık gelir. Buna karşılık parçaları bir listede toplayıp tek seferde birleştirmek, toplam karakter sayısıyla orantılı olarak yaklaşık $O(n)$ maliyet taşır.

| Yaklaşım | Teorik zaman | Ara bellek kullanımı | Genel tercih |
|---|---:|---:|---|
| Döngüde `+=` | En kötü durumda $O(n^2)$ | Çok sayıda geçici string | Küçük işlemler |
| Liste ve `join()` | $O(n)$ | Liste referansları ve sonuç | Büyük veya belirsiz veri |
| `io.StringIO` | Yaklaşık $O(n)$ | Dahili tampon | Akış benzeri üretim |

## Daha güvenli çözüm: `join()`

Parçaları önce listede toplamak, ardından tek seferde birleştirmek standart çözümdür:

```python
parcalar = []

for sayi in range(100_000):
    # Her adımda yalnızca yeni parçanın referansını saklar.
    parcalar.append(f"Kayıt: {sayi}\n")

# Sonucun uzunluğu hesaplanır ve birleştirme tek geçişte yapılır.
metin = "".join(parcalar)
```

`join()`, tüm parçaların toplam uzunluğunu önceden belirleyebilir ve sonuç için uygun alanı ayırabilir. Böylece giderek büyüyen metnin önceki bölümleri tekrar tekrar kopyalanmaz.

Ayraç kullanmak da oldukça kolaydır:

```python
isimler = ["Ada", "Guido", "Grace"]
sonuc = ", ".join(isimler)
# Ada, Guido, Grace
```

## Performansı ölçmek

Farkı kendi Python sürümünüzde `timeit` ile test edebilirsiniz:

```python
from timeit import timeit

artirarak = '''
sonuc = ""
for i in range(50_000):
    sonuc += str(i)
'''

listeyle = '''
parcalar = []
for i in range(50_000):
    parcalar.append(str(i))
sonuc = "".join(parcalar)
'''

print("+=  :", timeit(artirarak, number=20))
print("join:", timeit(listeyle, number=20))
```

Sonuçlar Python uygulamasına, sürüme ve parça boyutuna göre değişebilir. Özellikle CPython, bazı `+=` senaryolarında referans durumunu inceleyerek yeniden boyutlandırma optimizasyonu yapabilir. Bu nedenle basit testlerde `+=` şaşırtıcı derecede hızlı çıkabilir. Ancak bu optimizasyon dilin garanti ettiği bir davranış değildir; string başka bir değişken tarafından referans edildiğinde veya farklı bir Python uygulaması kullanıldığında etkisi kaybolabilir.

## `StringIO` ne zaman kullanılmalı?

Metin parçaları fonksiyona akış halinde yazılıyorsa `io.StringIO` daha doğal olabilir:

```python
from io import StringIO

buffer = StringIO()
for i in range(100_000):
    buffer.write(f"Satır {i}\n")

metin = buffer.getvalue()
```

Kısacası birkaç küçük string için `+` veya `+=` kullanmak gayet uygundur; performans polisleri kapınızı çalmaz. Fakat uzun süren döngülerde, büyük raporlarda ve veri üretiminde `join()` ya da `StringIO` seçmek hem daha öngörülebilir hem de ölçeklenebilir bir çözümdür. Optimizasyondan önce ölçün, fakat büyüyen string’i her turda yeniden taşımamaya çalışın.

![python-dongulerinde-string-33](/img/python-dongulerinde-string-33.svg)

