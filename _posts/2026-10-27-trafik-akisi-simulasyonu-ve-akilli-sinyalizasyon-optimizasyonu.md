---
layout: post
title: "Trafik Akışı Simülasyonu ve Akıllı Sinyalizasyon Optimizasyonu"
math: true
categories: 
  - Proje
tags: 
  - trafik simülasyonu
  - sinyalizasyon
  - optimizasyon
  - python
  - akıllı şehirler
  - algoritma
toc: true
image: /img/trafik-akisi-simulasyonu-85.png
---

Sabah işe giderken kırmızı ışıkta bekliyor, fakat diğer yönden tek bir aracın bile geçmediğini görüyorsanız yalnız değilsiniz. Sabit süreli trafik ışıkları, gün boyunca aynı senaryonun yaşandığını varsayar. Akıllı sinyalizasyon sistemleri ise kameralar, sensörler ve optimizasyon algoritmaları yardımıyla kavşağın nabzını ölçer; yeşil ışık sürelerini gerçek zamanlı yoğunluğa göre değiştirir.

``

## Trafik Akışının Matematiksel Temeli

Bir kavşağı modellemek için her şeridi araçların sıraya girdiği bir kuyruk olarak düşünebiliriz. Belirli bir zaman aralığında kuyruğa yeni araçlar eklenirken yeşil ışık sayesinde bazı araçlar sistemden ayrılır. Kuyruk uzunluğunun temel denklemi şöyledir:

$$
q_{t+1} = max(0, q_t + a_t - d_t)
$$

Burada $q_t$ mevcut araç sayısını, $a_t$ kavşağa gelen araçları, $d_t$ ise kavşaktan ayrılan araçları temsil eder. Amaç, toplam kuyruk uzunluğunu ve araçların ortalama bekleme süresini mümkün olduğunca azaltmaktır.

Bir şeridin yoğunluğu sensör verileriyle de hesaplanabilir:

$$
yogunluk = arac\_sayisi / serit\_uzunlugu
$$

Yoğunluk arttıkça ilgili yöne daha uzun yeşil ışık vermek mantıklıdır. Ancak “en kalabalık yön sürekli yeşil kalsın” yaklaşımı doğru değildir; diğer yönlerde açlık oluşmasını önlemek için maksimum bekleme süresi gibi adalet kuralları uygulanmalıdır.

## Sinyalizasyon Yaklaşımlarının Karşılaştırılması

| Yaklaşım | Karar mekanizması | Avantajı | Dezavantajı |
|---|---|---|---|
| Sabit süreli | Önceden tanımlanmış zamanlar | Basit ve ucuzdur | Anlık yoğunluğu göremez |
| Sensör tabanlı | Araç sayısı veya doluluk | Gerçek zamana uyum sağlar | Sensör hatalarından etkilenir |
| Basınç tabanlı | Komşu şerit kuyruklarını karşılaştırır | Ağ genelinde dengelidir | Modelleme daha karmaşıktır |
| Pekiştirmeli öğrenme | Ödül fonksiyonunu optimize eder | Karmaşık örüntüleri öğrenebilir | Eğitim ve güvenlik testi gerektirir |

Basınç tabanlı kontrolde bir yönün giriş ve çıkış kuyrukları karşılaştırılır. Basitleştirilmiş trafik basıncı $P = q_{giris} - q_{cikis}$ biçiminde düşünülebilir. Basıncı yüksek olan harekete öncelik verilmesi, dolu bir çıkış yoluna daha fazla araç gönderilmesini engeller.

## Basit Bir Python Simülasyonu

Aşağıdaki örnek, iki yönlü bir kavşakta araç sayılarına göre yeşil süre üretir. Minimum ve maksimum sınırlar, sistemin hem güvenli hem de adil davranmasını sağlar.

```python
MIN_GREEN = 10
MAX_GREEN = 45
CYCLE_TIME = 60

def green_times(north_south, east_west):
    total = north_south + east_west

    if total == 0:
        return 30, 30

    ns_ratio = north_south / total
    ns_green = round(CYCLE_TIME * ns_ratio)
    ns_green = max(MIN_GREEN, min(MAX_GREEN, ns_green))

    ew_green = CYCLE_TIME - ns_green
    ew_green = max(MIN_GREEN, min(MAX_GREEN, ew_green))
    return ns_green, ew_green

print(green_times(north_south=38, east_west=12))
```

Fonksiyon, kuzey-güney yönündeki yoğunluk daha yüksek olduğunda bu yöne daha fazla süre ayırır. Gerçek bir sistemde sarı ışık, yayaların geçiş süresi ve tüm yönlerin kırmızı olduğu güvenlik aralığı da çevrim süresinden düşülmelidir.

## Gerçek Zamanlı Sistem Nasıl Kurulur?

Uygulama hattı genellikle **algılama, tahmin, karar ve uygulama** aşamalarından oluşur. Endüktif döngüler, radarlar veya görüntü işleme modelleri araçları sayar. Toplanan veriler temizlenir; birkaç dakikalık trafik talebi tahmin edilir ve kontrol algoritması yeni ışık sürelerini üretir. Kararlar trafik denetleyicisine gönderilirken yasal süre sınırları kesinlikle korunur.

Simülasyon tarafında SUMO gibi araçlar kullanılarak ortalama bekleme süresi, kuyruk uzunluğu, dur-kalk sayısı ve karbon salımı ölçülebilir. Başarılı bir optimizasyon yalnızca araçları hızlandırmamalı; yayaları, bisikletlileri, toplu taşımayı ve acil durum araçlarını da hesaba katmalıdır. Kısacası akıllı kavşak, en sabırsız sürücüyü değil, bütün şehrin akışını optimize eder.

![trafik-akisi-simulasyonu-85](/img/trafik-akisi-simulasyonu-85.svg)

