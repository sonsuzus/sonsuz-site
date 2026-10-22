---
layout: post
title: "Eklem Sınırları Robotu Tekilliğe Nasıl Sürükler?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - yörünge-planlama
  - tekillik
  - eklem-sınırları
  - jacobian
  - kinematik
toc: true
image: /img/eklem-sinirlari-robotu-40.png
---

Bir robot kolu hedefe giderken yalnızca “Nereye ulaşmalıyım?” sorusunu sormaz; eklemlerinin ne kadar dönebileceğini de hesaba katmak zorundadır. Yörünge geometrik olarak kusursuz görünse bile eklem sınırları alternatif hareketleri kapatarak robotu tekil veya tekilliğe çok yakın bir konfigürasyona zorlayabilir. Sonuçta hızların büyüdüğü, kontrolün zorlaştığı ve robotun dramatik biçimde “Ben buradan dönemiyorum!” dediği bir durum ortaya çıkar.

![eklem-sinirlari-robotu-40](/img/eklem-sinirlari-robotu-40.svg)

``

## Eklem sınırı ile tekillik aynı şey mi?

Hayır. Eklem sınırı, bir eklemin izin verilen konum aralığıdır:

$$q_i^{\min} \le q_i \le q_i^{\max}$$

Tekillik ise robotun Jacobian matrisinin rank kaybettiği konfigürasyondur. Uç efektör hızı ile eklem hızları arasındaki ilişki

$$\dot{x}=J(q)\dot{q}$$

şeklindedir. Kare bir Jacobian için $\det(J)=0$ olduğunda matematiksel tekillik oluşur. Kare olmayan sistemlerde en küçük tekil değer $\sigma_{\min}$ sıfıra yaklaştıkça tekillik riski artar.

Eklem sınırı doğrudan Jacobian’ı tekil yapmaz. Ancak planlayıcının kullanabileceği konfigürasyon uzayını daraltır. Normalde robot, tekil bölgenin çevresinden farklı bir dirsek veya bilek duruşuyla dolaşabilir. Bu alternatif eklem sınırını aşıyorsa planlayıcı tekilliğe yakın rotayı seçmek zorunda kalabilir.

| Durum | Matematiksel gösterge | Pratik sonuç |
|---|---|---|
| Eklem sınırı | $q_i \approx q_i^{\min}$ veya $q_i^{\max}$ | Hareket seçeneği azalır |
| Tekillik | $\sigma_{\min}(J) \approx 0$ | Eklem hızları büyür |
| İkisi birlikte | Dar uygulanabilir bölge ve kötü Jacobian | Planlama ya başarısız olur ya da riskli yol üretir |

## Yörünge neden tehlikeli hâle gelir?

Ters hız kinematiğinde genellikle

$$\dot{q}=J^{\dagger}(q)\dot{x}$$

kullanılır. Tekilliğe yaklaşırken sözde ters $J^{\dagger}$ çok büyük değerler üretebilir. Robot küçük bir Kartezyen hız için bile aşırı eklem hızı ister. İstenen kaçış yönü eklem sınırı tarafından engelleniyorsa durum daha da kötüleşir.

Örneğin altı eksenli bir kolun bilek eklemi üst sınıra dayanmış olsun. Uç efektör yönelimini korumak için aynı hareketi başka eklemler paylaşabilir; fakat kol tamamen uzanmışsa Jacobian da rank kaybedebilir. Böylece hem hareket serbestliği azalır hem de sayısal çözüm kararsızlaşır.

## Planlayıcı bunu nasıl fark eder?

Manipülebilirlik ölçütü yaygın bir erken uyarıdır:

$$w(q)=\sqrt{\det(JJ^T)}$$

$w(q)$ küçüldükçe robot tekilliğe yaklaşır. Eklem sınırına yakınlık için ayrıca ceza fonksiyonu tanımlanabilir:

$$C_{limit}(q)=\sum_i \left(\frac{q_i-q_i^{mid}}{q_i^{max}-q_i^{min}}\right)^2$$

Aşağıdaki Python kodu, bir aday konfigürasyonun en küçük tekil değerini ve eklem sınırı cezasını hesaplar:

```python
import numpy as np

def trajectory_cost(q, J, q_min, q_max):
    # Küçük sigma, tekilliğe yakınlığı gösterir.
    sigma_min = np.linalg.svd(J, compute_uv=False)[-1]

    # Eklem aralığının merkezinden uzaklaşmayı cezalandırır.
    q_mid = (q_min + q_max) / 2.0
    span = q_max - q_min
    limit_cost = np.sum(((q - q_mid) / span) ** 2)

    singularity_cost = 1.0 / (sigma_min + 1e-4)
    return singularity_cost + 2.0 * limit_cost
```

Bu maliyet, RRT*, CHOMP veya optimizasyon tabanlı planlayıcılarda aday yolları karşılaştırmak için kullanılabilir. Katsayılar robotun hız, güvenlik ve görev önceliklerine göre ayarlanmalıdır.

## Kaçınma stratejileri

| Yöntem | Avantaj | Sınırlama |
|---|---|---|
| Sönümlü en küçük kareler | Tekillikte hız patlamasını azaltır | Kartezyen hata oluşturabilir |
| Null-space hareketi | Fazladan serbestliği eklem merkezleme için kullanır | Redundant robot gerektirir |
| Tekillik maliyeti | Riskli bölgeleri önceden dışlar | Optimizasyonu zorlaştırabilir |
| Yeniden yol planlama | Alternatif dirsek ve bilek duruşu bulur | Hesaplama süresini artırır |

Özetle eklem sınırları tekilliğin matematiksel sebebi değildir; fakat güvenli kaçış yollarını kapatan güçlü bir tetikleyicidir. Sağlam bir planlayıcı konum sınırlarını, Jacobian kondisyonunu, hız limitlerini ve alternatif kinematik dalları birlikte değerlendirmelidir. Robotun hedefe ulaşması yetmez; hedefe eklemlerini düğüm yapmadan ulaşması gerekir.
