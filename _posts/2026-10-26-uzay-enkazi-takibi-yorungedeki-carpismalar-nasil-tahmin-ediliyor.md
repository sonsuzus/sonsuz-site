---
layout: post
title: "Uzay Enkazı Takibi: Yörüngedeki Çarpışmalar Nasıl Tahmin Ediliyor?"
math: true
categories: 
  - Bilgi
tags: 
  - uzay
  - uzay-enkazı
  - yörünge
  - çarpışma-tahmini
  - python
  - astronomi
toc: true
image: /img/uzay-enkazi-takibi-56.png
---

Dünya’nın çevresi, kullanımdaki uyduların yanı sıra görevini tamamlamış araçlar, roket parçaları ve küçücük metal kırıntılarıyla dolu dev bir otoyola benziyor. Üstelik bu otoyolda trafik ışığı yok ve nesneler saatte yaklaşık 28.000 kilometre hızla ilerliyor! Uzay enkazı takibinin amacı, bu parçaların konumlarını ölçmek, gelecekteki yörüngelerini hesaplamak ve çalışan uydularla tehlikeli yakınlaşmaları önceden belirlemektir.

``

## Uzay enkazı neden tehlikeli?

Alçak Dünya yörüngesindeki iki nesnenin bağıl hızı $10\text{–}15\ km/s$ seviyesine çıkabilir. Bu nedenle birkaç santimetrelik bir parça bile uyduya ciddi zarar verebilir. Çarpışmalar ayrıca yeni parçalar oluşturarak **Kessler Sendromu** adı verilen zincirleme süreci tetikleyebilir: Daha çok enkaz, daha fazla çarpışma; daha fazla çarpışma da daha çok enkaz demektir.

| Nesne boyutu | Yaklaşık takip yöntemi | Olası etkisi |
|---|---|---|
| 10 cm’den büyük | Radar ve optik teleskop | Uyduyu tamamen kullanılmaz hâle getirebilir |
| 1–10 cm | Güçlü radar sistemleri | Kritik bileşenleri parçalayabilir |
| 1 cm’den küçük | İstatistiksel modeller | Yüzey ve sensör hasarı oluşturabilir |

![uzay-enkazi-takibi-56](/img/uzay-enkazi-takibi-56.svg)


## Konumlar nasıl ölçülüyor?

Yer tabanlı radarlar nesneye radyo dalgası gönderip yankının dönüş süresini ölçer. Mesafe yaklaşık olarak

$$d = \frac{c\Delta t}{2}$$

formülüyle bulunur. Burada $c$ ışık hızı, $\Delta t$ ise sinyalin gidiş-dönüş süresidir. Optik teleskoplar da özellikle yüksek yörüngelerdeki güneş ışığını yansıtan nesneleri yıldızlara göre görüntüler.

Tek bir ölçüm yeterli değildir. Gürültülü gözlemler; Kalman filtresi, genişletilmiş Kalman filtresi veya daha gelişmiş yörünge belirleme yöntemleriyle birleştirilir. Sonuç yalnızca tahmini konum değil, aynı zamanda belirsizliği temsil eden bir **kovaryans matrisi** olur. Başka bir ifadeyle sistem, “Nesne burada” demek yerine “Büyük olasılıkla bu bölgenin içinde” der.

## Yörünge geleceğe nasıl taşınır?

En temel model Newton’un kütle çekimi denklemidir:

$$a = -\frac{\mu}{r^3}r$$

Ancak gerçek hesaplarda Dünya’nın tam küresel olmaması, atmosferik sürüklenme, Güneş ve Ay’ın çekimi ile güneş ışınım basıncı da hesaba katılır.

| Model | Avantaj | Sınırlama |
|---|---|---|
| İki cisim modeli | Hızlı ve anlaşılır | Gerçek etkileri ihmal eder |
| SGP4 | TLE verileriyle pratiktir | Uzun vadede hata büyür |
| Sayısal integrasyon | Yüksek doğruluk sağlayabilir | Daha fazla işlem gücü ister |

## Yakınlaşma ve çarpışma olasılığı

İki yörünge ileri doğru hesaplanır ve nesnelerin birbirine en çok yaklaştığı an, yani **TCA** bulunur. Merkezler arasındaki en küçük uzaklığa *miss distance* denir. Fakat yalnızca bu mesafeye bakmak yanıltıcıdır; ölçüm belirsizliği de önemlidir.

Basitleştirilmiş bir tarama kodu şöyle yazılabilir:

```python
import numpy as np

def en_yakin_gecis(uydu, enkaz, zamanlar):
    en_kucuk = float("inf")
    kritik_an = None

    for t in zamanlar:
        # Fonksiyonların ilgili anda 3B konum döndürdüğü varsayılır.
        fark = uydu(t) - enkaz(t)
        mesafe = np.linalg.norm(fark)

        if mesafe < en_kucuk:
            en_kucuk = mesafe
            kritik_an = t

    return kritik_an, en_kucuk
```

Bu kod kaba bir ilk eleme yapar. Operasyonel sistemler, binlerce nesne çiftini taradıktan sonra kovaryans matrislerini ortak bir karşılaşma düzlemine aktarır ve çarpışma olasılığı $P_c$ hesaplar. Risk belirlenen eşiği aşarsa uydu operatörüne **Conjunction Data Message** gönderilebilir.

## Manevra yapmak her zaman doğru mu?

Kaçınma manevrası yakıt tüketir, görevi kesintiye uğratabilir ve uyduyu başka bir nesneye yaklaştırabilir. Bu nedenle karar; $P_c$, yaklaşma mesafesi, veri kalitesi, uydu değeri ve manevra kapasitesi birlikte değerlendirilerek verilir. Kısacası uzay trafik yönetimi, gökyüzünde oynanan yüksek hızlı bir satrançtır: Taşlar görünmez olabilir ama kötü bir hamlenin sonucu son derece gerçektir.
