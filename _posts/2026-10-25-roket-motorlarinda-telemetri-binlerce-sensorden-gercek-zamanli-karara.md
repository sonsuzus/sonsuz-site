---
layout: post
title: "Roket Motorlarında Telemetri: Binlerce Sensörden Gerçek Zamanlı Karara"
math: true
categories: 
  - Bilgi
tags: 
  - telemetri
  - roket
  - sensör
  - veri-analizi
  - gerçek-zamanlı-sistemler
  - python
toc: true
image: /img/roket-motorlarinda-telemetri-54.png
---

![roket-motorlarinda-telemetri-54](/img/roket-motorlarinda-telemetri-54.svg)


Bir roket motoru ateşlendiğinde yalnızca yakıt yanmaz; aynı anda devasa bir veri nehri akmaya başlar. Basınç, sıcaklık, titreşim, yakıt debisi ve valf konumu gibi binlerce ölçüm, saniyenin küçük dilimlerinde kontrol bilgisayarlarına ulaşır. Telemetri sistemi bu gürültülü akışı anlamlı bilgilere dönüştürerek mühendislerin motorun sağlığını izlemesini ve kritik durumları erkenden fark etmesini sağlar.

``

## Sensörden başlayan yolculuk

Bir ölçüm zinciri sensörle başlar. Termokupl sıcaklığı, piezoelektrik sensör titreşimi, basınç dönüştürücü ise yanma odası basıncını elektrik sinyaline çevirir. Bu analog sinyaller önce yükseltilir ve filtrelenir, ardından ADC kullanılarak sayısallaştırılır.

Örnekleme hızı rastgele seçilemez. Nyquist ilkesine göre ölçülmek istenen en yüksek frekans $f_{max}$ ise örnekleme frekansı şu koşulu sağlamalıdır:

$$f_s > 2f_{max}$$

Örneğin 5 kHz seviyesindeki titreşimleri gözlemlemek için teorik olarak 10 kHz’den yüksek bir hız gerekir. Pratikte filtreleme ve güvenlik payı nedeniyle daha yüksek değerler seçilir. Sıcaklık gibi yavaş değişen veriler ise saniyede birkaç örnekle izlenebilir. Her sensörü aynı hızda okumak, veri hattını gereksiz yere şişirir.

| Ölçüm türü | Tipik örnekleme yaklaşımı | İzlenen durum |
|---|---:|---|
| Sıcaklık | Düşük hız | Aşırı ısınma |
| Oda basıncı | Orta-yüksek hız | Yanma kararlılığı |
| Titreşim | Çok yüksek hız | Rezonans ve mekanik hasar |
| Valf konumu | Orta hız | Komut-tepki uyumu |
| Yakıt debisi | Orta hız | Karışım oranı |

## Gerçek zamanlı veri hattı

Ham ölçümler çoğunlukla sensör düğümlerinde zaman damgası alır. Paketler CAN, Ethernet veya uzay sistemlerine özel dayanıklı haberleşme protokolleri üzerinden uçuş bilgisayarına taşınır. Burada temel işlem sırası şöyledir:

1. Paket bütünlüğü ve sıra numarası kontrol edilir.
2. Ölçümler ortak bir zaman ekseninde hizalanır.
3. Kalibrasyon katsayıları uygulanır.
4. Gürültü filtrelenir ve özellikler çıkarılır.
5. Eşik ya da model tabanlı sağlık kontrolleri çalıştırılır.
6. Özet veriler yer istasyonuna gönderilirken ham veriler kaydedilir.

Binlerce kanalın toplam veri hızı yaklaşık olarak

$$R = N \times f_s \times b$$

ile hesaplanabilir. Burada $N$ sensör sayısı, $f_s$ örnekleme hızı, $b$ ise örnek başına bit miktarıdır. 2.000 sensörün 1 kHz’de ve 16 bit çözünürlükte okunması, protokol yükleri hariç 32 Mbit/s üretir. Bu nedenle sıkıştırma, önceliklendirme ve uçta işleme hayati önem taşır.

## Gürültü mü, arıza mı?

Tek bir yüksek değer her zaman motorun sorun yaşadığı anlamına gelmez. Elektriksel parazit veya sensör temassızlığı da ani sıçrama oluşturabilir. Basit bir hareketli ortalama, kısa süreli gürültüyü azaltabilir:

```python
from collections import deque

pencere = deque(maxlen=5)

def filtrele(olcum):
    pencere.append(olcum)
    return sum(pencere) / len(pencere)
```

Bu kod son beş ölçümün ortalamasını üretir. Ancak hızlı basınç değişimlerini geciktirebileceği için güvenlik kararlarında tek başına kullanılmamalıdır. Gerçek sistemlerde Kalman filtreleri, bant geçiren filtreler ve sensör füzyonu gibi yöntemler tercih edilir.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Sabit eşik | Hızlı ve anlaşılır | Değişen koşullara uyumsuz olabilir |
| İstatistiksel model | Sapmaları yakalar | Geçmiş veriye ihtiyaç duyar |
| Makine öğrenmesi | Karmaşık ilişkileri bulur | Açıklanabilirlik ve doğrulama zordur |
| Sensör füzyonu | Yanlış alarmı azaltır | Hesaplama maliyeti yüksektir |

## Milisaniyeler içinde karar

Roket telemetrisi yalnızca grafik çizmek değildir. Kritik basınç artışı algılandığında kontrol sistemi valfleri ayarlayabilir veya güvenli kapatma sürecini başlatabilir. Bu nedenle yazılımın gecikmesi öngörülebilir olmalı; bellek tahsisi, görev öncelikleri ve hata yönetimi titizlikle tasarlanmalıdır.

Fırlatma sonrasında kaydedilen ham veriler dijital ikizlerle karşılaştırılır. Böylece küçük titreşim değişimleri, verim kayıpları ve sensör sapmaları bulunur. Kısacası telemetri, roket motorunun nabzını ölçen bir stetoskop; gerçek zamanlı analiz ise bu nabzın ne anlattığını milisaniyeler içinde yorumlayan doktordur.
