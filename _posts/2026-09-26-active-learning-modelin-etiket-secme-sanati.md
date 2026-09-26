---
layout: post
title: "Active Learning: Modelin Etiket Seçme Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - active learning
  - makine öğrenmesi
  - yapay zeka
  - veri etiketleme
  - python
  - belirsizlik örneklemesi
toc: true
image: /img/active-learning-modelin-37.png
---

![active-learning-modelin-37](/img/active-learning-modelin-37.svg)


Elinizde milyonlarca kedi, köpek ve muhtemelen ne olduğu yalnızca biyologların anlayabileceği canlı fotoğrafı olduğunu düşünün. Bunların hepsini insanlara etiketletmek pahalı ve yavaştır. Active Learning, yani aktif öğrenme, modelin kalabalığın içinden öğrenmeye en çok katkı sağlayacak örnekleri seçip uzmana “Şuna bir bakar mısın?” demesidir.
``

## Active Learning nedir?

Klasik denetimli öğrenmede etiketli bir veri kümesi hazırlanır ve model bu kümenin tamamıyla eğitilir. Aktif öğrenmede ise başlangıçta yalnızca küçük bir etiketli küme bulunur. Model eğitildikten sonra etiketsiz veri havuzunu inceler, en faydalı gördüğü örnekleri seçer ve bunları bir insan uzmana gönderir.

Döngü genel olarak şöyledir:

1. Küçük bir başlangıç kümesini etiketle.
2. Modeli bu verilerle eğit.
3. Etiketsiz örnekler üzerinde tahmin yap.
4. En belirsiz veya bilgilendirici örnekleri seç.
5. İnsan uzmanından etiket iste.
6. Yeni etiketleri eğitim kümesine ekleyip modeli yeniden eğit.

Bu süreç, etiket bütçesi bitene veya model hedeflenen başarıya ulaşana kadar devam eder. Amaç daha fazla veri kullanmak değil, **doğru veriyi etiketlemektir**.

| Yaklaşım | Etiketlenecek veriyi kim seçer? | Maliyet | Veri verimliliği |
|---|---|---:|---:|
| Rastgele örnekleme | Rastgele seçim | Orta | Düşük |
| Tam etiketleme | İnsan veya veri sağlayıcı | Çok yüksek | Değişken |
| Active Learning | Model ve uzman birlikte | Daha düşük | Yüksek |

## Model hangi örnekleri sorar?

En yaygın yöntem **belirsizlik örneklemesi**dir. İkili sınıflandırmada model bir örnek için $P(y=1\mid x)=0.51$ üretiyorsa oldukça kararsızdır. Buna karşılık $0.99$ olasılıklı bir tahmin model açısından kolaydır. Etiket bütçesini kolay örneğe harcamak yerine kararsız örneği uzmana göndermek daha mantıklıdır.

Çok sınıflı problemlerde entropi kullanılabilir:

$$
H(x)=-\sum_{i=1}^{K}p_i(x)\log p_i(x)
$$

Burada $K$ sınıf sayısını, $p_i(x)$ ise örneğin $i$ sınıfına ait olma olasılığını gösterir. Entropi büyüdükçe tahmin dağılımı daha kararsız hâle gelir.

| Strateji | Temel fikir | Güçlü yönü | Riski |
|---|---|---|---|
| En düşük güven | En düşük maksimum olasılığı seçer | Basit ve hızlı | Dağılımı tam değerlendirmez |
| Marjin örnekleme | En yüksek iki olasılığın farkına bakar | Sınıf sınırlarını bulur | Gürültüden etkilenebilir |
| Entropi | Tüm sınıf olasılıklarını kullanır | Çok sınıflı işlerde etkilidir | Kalibre edilmemiş olasılıklar yanıltabilir |
| Komiteyle sorgulama | Birden fazla modelin anlaşamadığı örnekleri seçer | Model çeşitliliğinden yararlanır | Hesaplama maliyeti yüksektir |

## Python ile basit seçim

Aşağıdaki kod, sınıf olasılıklarının entropisini hesaplar ve en belirsiz üç örneği seçer:

```python
import numpy as np

# Her satır bir örneğin sınıf olasılıklarını temsil eder.
probabilities = np.array([
    [0.90, 0.08, 0.02],
    [0.34, 0.33, 0.33],
    [0.55, 0.40, 0.05],
    [0.45, 0.10, 0.45],
    [0.80, 0.10, 0.10]
])

def entropy(probs):
    safe_probs = np.clip(probs, 1e-12, 1.0)
    return -np.sum(safe_probs * np.log(safe_probs), axis=1)

scores = entropy(probabilities)
query_indices = np.argsort(scores)[-3:][::-1]

print("Uzmanlara gönderilecek örnekler:", query_indices)
print("Belirsizlik puanları:", scores[query_indices])
```

`np.clip`, sıfır olasılığın logaritmasını alma sorununu önler. En yüksek entropiye sahip indeksler, insan uzmanına gönderilecek adaylardır. Gerçek projede bu indekslere karşılık gelen metinler, görüntüler veya kayıtlar bir etiketleme arayüzünde gösterilir.

## Her belirsiz örnek faydalı mı?

Hayır. Model bazen bozuk görüntülere, anlamsız metinlere veya dağılım dışı verilere de aşırı belirsizlik gösterebilir. Bu nedenle çeşitlilik örneklemesi, kümeleme ve kalite filtreleri kullanılmalıdır. Aynı türden yüz kararsız örneği seçmek yerine farklı bölgeleri temsil eden örnekler tercih edilmelidir.

Ayrıca insan uzmanların hata yapabileceği unutulmamalıdır. Birden fazla uzmanın görüşü, uzlaşma ölçümleri ve düzenli kalite kontrolleri sürece eklenebilir. Başarılı bir Active Learning sistemi yalnızca akıllı bir sorgu algoritması değil; model, veri altyapısı ve insan uzman arasında kurulmuş geri bildirim döngüsüdür. Böylece model sessizce veri yutmak yerine, gerçekten merak ettiği soruları sormayı öğrenir.
